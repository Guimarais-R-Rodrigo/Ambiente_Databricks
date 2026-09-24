from __future__ import annotations
import argparse, json
from pathlib import Path
SELECTIVE={"pilot.alpha.pass":"PASS","pilot.beta.fail":"FAIL","pilot.beta.dependent":"BLOCKED_DEPENDENCY","pilot.gamma.independent":"PASS","pilot.publication.blocked":"BLOCKED_DEPENDENCY"}
GLOBAL={"pilot.global.arm":"PASS","pilot.global.fail":"FAIL","pilot.global.anchor":"PASS","pilot.global.must_not_start":"BLOCKED_GLOBAL_STOP","pilot.global.integrator":"BLOCKED_GLOBAL_STOP"}
def verify(summary:dict,scenario:str="selective")->dict:
 if scenario not in {"selective","global"}: return {"valid":False,"issues":["PILOT_SCENARIO_INVALID"],"classification":"B0_PILOT_FAIL"}
 expected=SELECTIVE if scenario=="selective" else GLOBAL; issues=[]
 if not isinstance(summary,dict): return {"valid":False,"issues":["PILOT_SUMMARY_INVALID"],"classification":f"B0_{scenario.upper()}_PILOT_FAIL"}
 if summary.get("issues") not in (None,[]): issues.append("PILOT_MECHANISM_ISSUES_PRESENT")
 results=summary.get("results")
 if not isinstance(results,dict): return {"valid":False,"issues":["PILOT_RESULTS_MISSING"],"classification":f"B0_{scenario.upper()}_PILOT_FAIL"}
 verification=summary.get("verification")
 if not isinstance(verification,dict) or verification.get("valid") is not True or verification.get("issues")!=[]: issues.append("PILOT_CAMPAIGN_VERIFICATION_NOT_VALID")
 if summary.get("status")!="FAIL": issues.append("PILOT_NORMAL_CAMPAIGN_MUST_FAIL")
 if not isinstance(summary.get("round_id"),str) or not summary.get("round_id"): issues.append("PILOT_ROUND_ID_MISSING")
 if not isinstance(summary.get("release_spec_digest"),str) or len(summary.get("release_spec_digest",""))!=64: issues.append("PILOT_RELEASE_SPEC_DIGEST_MISSING")
 if set(results)!=set(expected): issues.append("PILOT_TASK_SET_MISMATCH")
 for tid,status in expected.items():
  row=results.get(tid) or {}; observed=row.get("status")
  if observed!=status: issues.append(f"PILOT_STATUS:{tid}:{observed}:{status}")
  if status.startswith("BLOCKED") and row.get("command_records"): issues.append(f"PILOT_BLOCKED_TASK_EXECUTED:{tid}")
 if scenario=="selective":
  if (results.get("pilot.beta.dependent") or {}).get("blocked_by")!=["pilot.beta.fail"]: issues.append("PILOT_DEPENDENCY_PROPAGATION_INVALID")
  if (results.get("pilot.publication.blocked") or {}).get("blocked_by")!=["pilot.beta.dependent"]: issues.append("PILOT_PUBLICATION_NOT_BLOCKED")
  if summary.get("first_failure")!="pilot.beta.fail": issues.append("PILOT_FIRST_FAILURE_INVALID")
  if summary.get("global_stop") is not None: issues.append("PILOT_SELECTIVE_UNEXPECTED_GLOBAL_STOP")
 else:
  for tid in ("pilot.global.must_not_start","pilot.global.integrator"):
   if (results.get(tid) or {}).get("blocked_by")!=["pilot.global.fail"]: issues.append(f"GLOBAL_STOP_BLOCKER_INVALID:{tid}")
  if summary.get("global_stop")!="pilot.global.fail": issues.append("GLOBAL_STOP_NOT_RECORDED")
  if summary.get("first_failure")!="pilot.global.fail": issues.append("GLOBAL_FIRST_FAILURE_INVALID")
 return {"valid":not issues,"issues":issues,"classification":f"B0_{scenario.upper()}_PILOT_PASS" if not issues else f"B0_{scenario.upper()}_PILOT_FAIL"}
def main():
 p=argparse.ArgumentParser(); p.add_argument("--summary",required=True,type=Path); p.add_argument("--scenario",choices=["selective","global"],default="selective"); a=p.parse_args(); result=verify(json.loads(a.summary.read_text(encoding="utf-8")),a.scenario); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result["valid"] else 1
if __name__=="__main__": raise SystemExit(main())
