from __future__ import annotations
import hashlib, os, platform, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from .fingerprint import fingerprint_paths
from .git_state import status_paths
from .model import CommandSpec, TaskSpec, TaskResult
from .util import write_json_atomic

def _utc(): return datetime.now(timezone.utc).isoformat()
def _sha(s:str)->str: return hashlib.sha256(s.encode("utf-8",errors="replace")).hexdigest()

def render_argv(spec:CommandSpec,repo:Path,evidence:Path,task_id:str)->list[str]:
    mapping={"{python}":sys.executable,"{repo}":str(repo),"{evidence}":str(evidence),"{task_id}":task_id}
    out=[]
    for token in spec.argv:
        if token in mapping: out.append(mapping[token])
        elif "{" in token or "}" in token: raise ValueError(f"UNSUPPORTED_PLACEHOLDER:{token}")
        else: out.append(token)
    return out


def _observe_outcome(assertion:dict,stdout:str,stderr:str)->tuple[dict,list[str]]:
    kind=assertion.get("kind"); combined=stdout+"\n"+stderr; issues=[]
    if kind=="exit_only": return {"kind":kind,"failures":[],"errors":[]},issues
    if kind=="unittest_exact_failures":
        failures=sorted(set(re.findall(r"(?m)^FAIL: (test_[A-Za-z0-9_]+)",combined)))
        errors=sorted(set(re.findall(r"(?m)^ERROR: (test_[A-Za-z0-9_]+)",combined)))
        expected=sorted(assertion.get("expected_failures") or [])
        if failures!=expected: issues.append("UNITTEST_FAILURE_SET_MISMATCH:expected="+",".join(expected)+";observed="+",".join(failures))
        if errors: issues.append("UNITTEST_UNEXPECTED_ERRORS:"+",".join(errors))
        return {"kind":kind,"failures":failures,"errors":errors},issues
    return {"kind":str(kind),"failures":[],"errors":[]},["OUTCOME_ASSERTION_KIND_UNKNOWN"]

def _allowed_mutation(path:str,allowed:tuple[str,...])->bool:
    return any(path==a or path.startswith(a.rstrip('/')+'/') for a in allowed)

def run_task(repo:Path,evidence_root:Path,task:TaskSpec,command:CommandSpec)->TaskResult:
    task_dir=evidence_root/'tasks'/task.task_id; task_dir.mkdir(parents=True,exist_ok=False)
    started=_utc(); before_status=status_paths(repo); protected_before=fingerprint_paths(repo,task.protected_paths)
    stdout=stderr=""; code=None; command_started=False; cleanup=True; issues=[]
    safe_keys=("PATH","SYSTEMROOT","WINDIR","COMSPEC","TEMP","TMP","HOME","USERPROFILE","LANG","LC_ALL")
    env={k:os.environ[k] for k in safe_keys if k in os.environ}
    env.update({"PYTHONDONTWRITEBYTECODE":"1","PYTHONUTF8":"1","PYTHONIOENCODING":"utf-8"})
    for key,value in task.env.items():
        if key not in command.env_allowlist: issues.append(f"ENV_NOT_ALLOWED:{key}")
        else: env[key]=value
    if issues:
        status="BLOCKED_DESIGN"
    else:
        argv=render_argv(command,repo,task_dir,task.task_id)
        write_json_atomic(task_dir/'invocation.json',{"argv":argv,"cwd":str(repo),"env_keys":sorted(env),"command_id":command.command_id,"platform":platform.platform()})
        try:
            command_started=True
            p=subprocess.run(argv,cwd=repo,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=command.timeout_seconds,env=env)
            code=p.returncode; stdout=p.stdout or ""; stderr=p.stderr or ""
        except subprocess.TimeoutExpired as exc:
            code=124; stdout=(exc.stdout or "") if isinstance(exc.stdout,str) else ""; stderr=(exc.stderr or "") if isinstance(exc.stderr,str) else ""; issues.append("PROCESS_TIMEOUT")
        except BaseException as exc:
            cleanup=False; issues.append(f"PROCESS_EXCEPTION:{type(exc).__name__}:{exc}")
        observed,outcome_issues=_observe_outcome(task.outcome_assertion,stdout,stderr); issues.extend(outcome_issues)
        status="PASS" if cleanup and code in task.expected_exit_codes and not issues else "FAIL"
    if 'observed' not in locals(): observed={"kind":task.outcome_assertion.get("kind"),"failures":[],"errors":[]}
    (task_dir/'stdout.txt').write_text(stdout,encoding='utf-8'); (task_dir/'stderr.txt').write_text(stderr,encoding='utf-8')
    after_status=status_paths(repo); protected_after=fingerprint_paths(repo,task.protected_paths)
    mutations=sorted(set(after_status)-set(before_status)); protected_changes=sorted(k for k in set(protected_before)|set(protected_after) if protected_before.get(k)!=protected_after.get(k))
    forbidden=[p for p in mutations if not _allowed_mutation(p,task.repo_write_paths)]
    if forbidden: issues.append("UNAUTHORIZED_REPO_MUTATION:"+",".join(forbidden)); status="FAIL"
    if protected_changes: issues.append("PROTECTED_PATH_CHANGED:"+",".join(protected_changes)); status="FAIL"
    result=TaskResult(task.task_id,task.command_id,status,code,list(task.expected_exit_codes),command_started,cleanup,started,_utc(),_sha(stdout),_sha(stderr),mutations,protected_changes,"NONE",observed,issues)
    write_json_atomic(task_dir/'result.json',result.as_dict())
    return result
