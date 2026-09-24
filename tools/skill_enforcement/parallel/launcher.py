from __future__ import annotations
import argparse,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
from typing import Any,Mapping
from .contract import RESULT_SCHEMA_VERSION,digest_json,validate_campaign
from .host_probe import probe
from .lease import HostCampaignLease,HostLeaseBusy
from .process import ROOT,fingerprint_paths,run_argv
from .registry import resolve_command
from .round_identity import assert_release_spec_current,release_spec_digest,validate_release_spec
from .scheduler import decide,detect_cycle
from .verifier import verify_campaign_run
def _utc(): return datetime.now(timezone.utc).isoformat()
def _git(*args):
 p=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,text=True,timeout=20)
 if p.returncode!=0: raise RuntimeError("GIT_FAILED:"+" ".join(args)+":"+(p.stderr or "").strip())
 return p.stdout.strip()
def _repo_status(): return _git("status","--porcelain=v1","--untracked-files=all")
def _preconditions(campaign:Mapping[str,Any],evidence_root:Path,release_spec:Mapping[str,Any]):
 issues=validate_release_spec(release_spec); issues.extend(assert_release_spec_current(release_spec))
 if release_spec_digest(release_spec)!=campaign.get("release_spec_digest"): issues.append("RELEASE_SPEC_DIGEST_MISMATCH")
 for key in ("round_id","candidate_sha","candidate_tree_sha","baseline_sha","command_registry_digest","coverage_digest","policy_before_digest"):
  if campaign.get(key)!=release_spec.get(key): issues.append("CAMPAIGN_RELEASE_SPEC_MISMATCH:"+key)
 try:
  if digest_json(probe())!=release_spec.get("host_digest"): issues.append("HOST_PROFILE_CHANGED")
 except Exception as exc: issues.append("HOST_PROFILE_UNREADABLE:"+type(exc).__name__)
 repo=ROOT.resolve(); target=evidence_root.absolute()
 try: parent=target.parent.resolve(strict=True)
 except OSError: issues.append("EVIDENCE_PARENT_INVALID"); parent=None
 if parent is not None and (parent.is_relative_to(repo) or repo.is_relative_to(target)): issues.append("EVIDENCE_MUST_BE_EXTERNAL")
 if target.exists(): issues.append("EVIDENCE_DIRECTORY_MUST_BE_NEW")
 return issues
def _base_result(task,campaign,status,wave,first_failure):
 fp=fingerprint_paths(ROOT,task["protected_paths"]); now=_utc()
 return {"result_schema":RESULT_SCHEMA_VERSION,"task_id":task["task_id"],"round_id":campaign["round_id"],"release_spec_digest":campaign["release_spec_digest"],"candidate_sha":campaign["candidate_sha"],"status":status,"effect_state":"NONE","command_records":[],"first_failure":first_failure,"wave_index":wave,"started_at_utc":now,"ended_at_utc":now,"protected_fingerprint_before":fp,"protected_fingerprint_after":fp,"issues":[]}
def _blocked_result(task,campaign,status,wave,blockers,first_failure):
 row=_base_result(task,campaign,status,wave,first_failure); row["blocked_by"]=blockers; return row
def _exception_result(task,campaign,wave,exc):
 row=_base_result(task,campaign,"FAIL",wave,None); row["issues"]=[f"TASK_EXECUTION_EXCEPTION:{type(exc).__name__}:{exc}"]; return row
def _run_task_command(argv,task_dir,name,timeout):
 return run_argv(argv,task_dir,name,timeout=timeout,sandbox=True)
def execute(campaign:dict,evidence_root:Path,release_spec:Mapping[str,Any]):
 issues=validate_campaign(campaign)
 if issues: return {"status":"FAIL","issues":issues,"results":{},"verification":None}
 if detect_cycle(campaign["tasks"]): return {"status":"FAIL","issues":["CAMPAIGN_DAG_CYCLE"],"results":{},"verification":None}
 pre=_preconditions(campaign,evidence_root,release_spec)
 if pre: return {"status":"FAIL","issues":pre,"results":{},"verification":None}
 try:
  lease=HostCampaignLease(campaign["round_id"],campaign["campaign_id"]); lease.__enter__()
 except HostLeaseBusy as exc: return {"status":"FAIL","issues":[str(exc)],"results":{},"verification":None}
 try:
  evidence_root.mkdir(parents=True,exist_ok=False); results={}; tasks={t["task_id"]:t for t in campaign["tasks"]}; first_failure=None; global_stop=None; mechanism_issues=[]; wave=0; initial_status=_repo_status()
  while len(results)<len(tasks):
   if global_stop is not None:
    for task_id in sorted(set(tasks)-set(results)): results[task_id]=_blocked_result(tasks[task_id],campaign,"BLOCKED_GLOBAL_STOP",wave,[global_stop],first_failure)
    break
   states={k:v["status"] for k,v in results.items()}
   decision=decide(campaign["tasks"],states,limit=campaign["max_parallel"],auditor_limit=campaign["max_auditors"],resource_limits=campaign.get("resource_limits"))
   for task_id in decision.blocked_dependency:
    task=tasks[task_id]; blockers=[d for d in task["depends_on"] if states.get(d) not in {"PASS","NOT_APPLICABLE"}]; results[task_id]=_blocked_result(task,campaign,"BLOCKED_DEPENDENCY",wave,blockers,first_failure)
   if not decision.ready and decision.blocked_dependency: wave+=1; continue
   if not decision.ready:
    for task_id in decision.pending:
     results[task_id]=_blocked_result(tasks[task_id],campaign,"BLOCKED_RESOURCE",wave,[],first_failure); results[task_id]["issues"]=["NO_PROGRESS"]
    mechanism_issues.append("SCHEDULER_NO_PROGRESS"); break
   current_wave=wave
   def run_task(task_id):
    task=tasks[task_id]; started=_utc(); task_dir=evidence_root/task_id; before=fingerprint_paths(ROOT,task["protected_paths"]); records=[]; status="PASS"; task_issues=[]
    for command_id in task["command_ids"]:
     argv,timeout=resolve_command(command_id); row=_run_task_command(argv,task_dir,command_id.replace(":","_"),timeout); records.append(row); good_exit=type(row.get("exit_code")) is int and row.get("exit_code")==0
     if row.get("command_started") is not True or row.get("timed_out") is not False or row.get("cleanup") not in {"COMPLETE","COMPLETE_ALREADY_EXITED"} or row.get("residual_descendants_detected") is not False or not good_exit:
      status="FAIL"; task_issues.append("COMMAND_FAILED:"+command_id); break
    after=fingerprint_paths(ROOT,task["protected_paths"])
    if before!=after: status="FAIL"; task_issues.append("PROTECTED_PATH_MUTATED")
    return task_id,{"result_schema":RESULT_SCHEMA_VERSION,"task_id":task_id,"round_id":campaign["round_id"],"release_spec_digest":campaign["release_spec_digest"],"candidate_sha":campaign["candidate_sha"],"status":status,"effect_state":"NONE","command_records":records,"first_failure":None,"wave_index":current_wave,"started_at_utc":started,"ended_at_utc":_utc(),"protected_fingerprint_before":before,"protected_fingerprint_after":after,"issues":task_issues}
   wave_results={}
   with ThreadPoolExecutor(max_workers=len(decision.ready)) as pool:
    futures={pool.submit(run_task,task_id):task_id for task_id in decision.ready}
    for future in as_completed(futures):
     task_id=futures[future]
     try:
      returned_id,row=future.result()
      if returned_id!=task_id: raise RuntimeError("TASK_FUTURE_ID_MISMATCH")
     except BaseException as exc:
      row=_exception_result(tasks[task_id],campaign,current_wave,exc); mechanism_issues.append(f"TASK_EXECUTION_EXCEPTION:{task_id}:{type(exc).__name__}")
     wave_results[task_id]=row
   for task_id in sorted(wave_results): results[task_id]=wave_results[task_id]
   failed=sorted(task_id for task_id,row in wave_results.items() if row["status"]=="FAIL")
   if failed and first_failure is None: first_failure=failed[0]
   global_failed=[task_id for task_id in failed if tasks[task_id]["failure_scope"]=="GLOBAL_CAMPAIGN"]
   if global_failed: global_stop=global_failed[0]
   for row in results.values(): row["first_failure"]=first_failure
   if _repo_status()!=initial_status: mechanism_issues.append("REPO_MUTATION_DETECTED"); global_stop="__REPO_MUTATION__"
   wave+=1
  try: verification=verify_campaign_run(campaign,results,evidence_root)
  except Exception as exc:
   verification={"valid":False,"issues":[f"VERIFIER_EXCEPTION:{type(exc).__name__}:{exc}"],"first_failure":first_failure,"first_observed_failure":None,"global_failures":[],"verification_scope":"SER_PARALLEL_LOCAL_CAMPAIGN_INTEGRITY_V3"}; mechanism_issues.append("VERIFIER_EXCEPTION")
  summary={"schema_version":"SER-PARALLEL-RUN-3","campaign_id":campaign["campaign_id"],"round_id":campaign["round_id"],"release_spec_digest":campaign["release_spec_digest"],"candidate_sha":campaign["candidate_sha"],"candidate_tree_sha":campaign["candidate_tree_sha"],"status":"PASS" if not mechanism_issues and verification["valid"] and all(r["status"] in {"PASS","NOT_APPLICABLE"} for r in results.values()) else "FAIL","first_failure":verification.get("first_failure"),"global_stop":global_stop,"issues":mechanism_issues,"results":results,"verification":verification}
  (evidence_root/"summary.json").write_bytes((json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")); return summary
 finally: lease.__exit__(None,None,None)
def main():
 p=argparse.ArgumentParser(); p.add_argument("--campaign",required=True,type=Path); p.add_argument("--release-spec",required=True,type=Path); p.add_argument("--evidence-dir",required=True,type=Path); a=p.parse_args()
 try: summary=execute(json.loads(a.campaign.read_text(encoding="utf-8")),a.evidence_dir,json.loads(a.release_spec.read_text(encoding="utf-8")))
 except Exception as exc: summary={"schema_version":"SER-PARALLEL-RUN-3","status":"FAIL","issues":[f"LAUNCHER_EXCEPTION:{type(exc).__name__}:{exc}"],"results":{},"verification":None}
 print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if summary.get("status")=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
