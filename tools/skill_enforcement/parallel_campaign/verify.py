from __future__ import annotations
from pathlib import Path
from typing import Any
from .util import read_json, sha256_file
from .process_adapter import _observe_outcome
from .manifest import validate_document

def verify_run(campaign:dict,evidence:Path)->dict[str,Any]:
    issues=[]; tasks={x['task_id']:x for x in campaign['tasks']}; seen={}; first_failure=None
    for tid,task in tasks.items():
        p=evidence/'tasks'/tid/'result.json'
        if not p.is_file(): issues.append(f"RESULT_MISSING:{tid}"); continue
        result=read_json(p); errs=validate_document(result,'task_result.schema.json'); issues.extend(f"{tid}:{x}" for x in errs)
        if result.get('task_id')!=tid or result.get('command_id')!=task['command_id']: issues.append(f"RESULT_BINDING:{tid}")
        if result.get('status')=='PASS' and result.get('exit_code') not in task['expected_exit_codes']: issues.append(f"PASS_EXIT_MISMATCH:{tid}")
        if result.get('status')=='PASS' and (result.get('issues') or result.get('protected_changes')): issues.append(f"PASS_HAS_ISSUES:{tid}")
        if result.get('status')=='PASS' and (result.get('command_started') is not True or result.get('cleanup_complete') is not True): issues.append(f"PASS_PROCESS_INCOMPLETE:{tid}")
        stdout_path=evidence/'tasks'/tid/'stdout.txt'; stderr_path=evidence/'tasks'/tid/'stderr.txt'
        if not stdout_path.is_file() or not stderr_path.is_file(): issues.append(f"LOG_MISSING:{tid}")
        else:
            stdout=stdout_path.read_text(encoding='utf-8'); stderr=stderr_path.read_text(encoding='utf-8')
            import hashlib
            if hashlib.sha256(stdout.encode()).hexdigest()!=result.get('stdout_sha256') or hashlib.sha256(stderr.encode()).hexdigest()!=result.get('stderr_sha256'): issues.append(f"LOG_HASH_MISMATCH:{tid}")
            observed,assert_issues=_observe_outcome(task['outcome_assertion'],stdout,stderr)
            if observed!=result.get('outcome_observed'): issues.append(f"OUTCOME_OBSERVED_MISMATCH:{tid}")
            issues.extend(f"{tid}:{x}" for x in assert_issues)
        seen[tid]=result
    for tid,task in tasks.items():
        r=seen.get(tid)
        if not r: continue
        bad=[d for d in task['depends_on'] if seen.get(d,{}).get('status')!='PASS']
        if bad and r.get('status') not in {'BLOCKED_DEPENDENCY'}: issues.append(f"DEPENDENCY_SEMANTICS:{tid}")
        if task['required'] and r.get('status')=='FAIL':
            key=(r.get('ended_at_utc') or '', tid)
            if first_failure is None or key < first_failure[0]: first_failure=(key,tid)
    required_missing=[tid for tid,t in tasks.items() if t['required'] and tid not in seen]
    issues.extend('REQUIRED_RESULT_MISSING:'+x for x in required_missing)
    valid=not issues
    # A blocked required task makes campaign non-pass even if structurally valid.
    campaign_pass=valid and all(seen.get(tid,{}).get('status')=='PASS' for tid,t in tasks.items() if t['required'])
    first_id=first_failure[1] if isinstance(first_failure,tuple) else None
    return {"verification_version":"SER-PARALLEL-VERIFY-1","valid":valid,"campaign_pass":campaign_pass,"issues":issues,"first_failure":first_id,"task_statuses":{k:v.get('status') for k,v in seen.items()}}

def verify_manifest(evidence:Path)->dict:
    p=evidence/'manifest.json'
    if not p.is_file(): return {"valid":False,"issues":["MANIFEST_MISSING"]}
    m=read_json(p); issues=[]
    listed={row.get('path') for row in m.get('files',[])}
    actual={q.relative_to(evidence).as_posix() for q in evidence.rglob('*') if q.is_file() and q.name!='manifest.json'}
    if listed!=actual:
        for x in sorted(listed-actual): issues.append('FILE_MISSING_FROM_TREE:'+str(x))
        for x in sorted(actual-listed): issues.append('FILE_EXTRA_NOT_MANIFESTED:'+str(x))
    for row in m.get('files',[]):
        target=evidence/row.get('path','')
        if not target.is_file(): issues.append('FILE_MISSING:'+str(row.get('path'))); continue
        if target.stat().st_size!=row.get('size') or sha256_file(target)!=row.get('sha256'): issues.append('FILE_HASH_MISMATCH:'+str(row.get('path')))
    return {"valid":not issues,"issues":issues}
