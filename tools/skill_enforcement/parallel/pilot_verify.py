from __future__ import annotations
import argparse, json
from pathlib import Path
SELECTIVE={"pilot.alpha.pass":"PASS","pilot.beta.fail":"FAIL","pilot.beta.dependent":"BLOCKED_DEPENDENCY","pilot.gamma.independent":"PASS","pilot.publication.blocked":"BLOCKED_DEPENDENCY"}
GLOBAL={"pilot.global.arm":"PASS","pilot.global.fail":"FAIL","pilot.global.anchor":"PASS","pilot.global.must_not_start":"BLOCKED_GLOBAL_STOP"}

def verify(summary:dict,scenario:str="selective") -> dict:
 expected=SELECTIVE if scenario=="selective" else GLOBAL; issues=[]; results=summary.get("results") if isinstance(summary,dict) else None
 if not isinstance(results,dict): return {"valid":False,"issues":["PILOT_RESULTS_MISSING"]}
 if set(results)!=set(expected): issues.append("PILOT_TASK_SET_MISMATCH")
 for tid,status in expected.items():
  observed=(results.get(tid) or {}).get("status")
  if observed!=status: issues.append(f"PILOT_STATUS:{tid}:{observed}:{status}")
 if scenario=="selective":
  if (results.get("pilot.beta.dependent") or {}).get("blocked_by") != ["pilot.beta.fail"]: issues.append("PILOT_DEPENDENCY_PROPAGATION_INVALID")
  if "pilot.beta.dependent" not in ((results.get("pilot.publication.blocked") or {}).get("blocked_by") or []): issues.append("PILOT_PUBLICATION_NOT_BLOCKED")
  if summary.get("first_failure")!="pilot.beta.fail": issues.append("PILOT_FIRST_FAILURE_INVALID")
 else:
  later=results.get("pilot.global.must_not_start") or {}
  if later.get("command_records"): issues.append("GLOBAL_STOP_LATE_TASK_EXECUTED")
  if later.get("blocked_by") != ["pilot.global.fail"]: issues.append("GLOBAL_STOP_BLOCKER_INVALID")
  if summary.get("global_stop")!="pilot.global.fail": issues.append("GLOBAL_STOP_NOT_RECORDED")
 return {"valid":not issues,"issues":issues,"classification":f"B0_{scenario.upper()}_PILOT_PASS" if not issues else f"B0_{scenario.upper()}_PILOT_FAIL"}

def main():
 p=argparse.ArgumentParser(); p.add_argument("--summary",required=True,type=Path); p.add_argument("--scenario",choices=["selective","global"],default="selective"); a=p.parse_args(); result=verify(json.loads(a.summary.read_text(encoding="utf-8")),a.scenario); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result["valid"] else 1
if __name__=="__main__": raise SystemExit(main())
