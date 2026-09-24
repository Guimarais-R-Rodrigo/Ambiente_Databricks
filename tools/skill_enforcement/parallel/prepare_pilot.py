from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any, Mapping
from .contract import validate_campaign
from .process import ROOT
from .round_identity import assert_release_spec_current, release_spec_digest, validate_release_spec
TEMPLATES={"selective":ROOT/"tools/skill_enforcement/parallel/pilot_campaign.json","global":ROOT/"tools/skill_enforcement/parallel/pilot_global_stop_campaign.json"}
def prepare(output:Path,scenario:str="selective",release_spec:Mapping[str,Any]|None=None)->dict:
 if release_spec is None: raise RuntimeError("RELEASE_SPEC_REQUIRED")
 issues=validate_release_spec(release_spec); issues.extend(assert_release_spec_current(release_spec))
 if issues: raise RuntimeError("RELEASE_SPEC_INVALID:"+",".join(issues))
 campaign=json.loads(TEMPLATES[scenario].read_text(encoding="utf-8"))
 campaign["round_id"]=release_spec["round_id"]; campaign["release_spec_digest"]=release_spec_digest(release_spec)
 campaign["candidate_sha"]=release_spec["candidate_sha"]; campaign["candidate_tree_sha"]=release_spec["candidate_tree_sha"]; campaign["baseline_sha"]=release_spec["baseline_sha"]
 campaign["command_registry_digest"]=release_spec["command_registry_digest"]; campaign["coverage_digest"]=release_spec["coverage_digest"]; campaign["policy_before_digest"]=release_spec["policy_before_digest"]
 for task in campaign["tasks"]: task["candidate_sha"]=release_spec["candidate_sha"]
 bad=validate_campaign(campaign)
 if bad: raise RuntimeError("CAMPAIGN_INVALID:"+",".join(bad))
 output.write_bytes((json.dumps(campaign,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")); return campaign
def main():
 p=argparse.ArgumentParser(); p.add_argument("--output",required=True,type=Path); p.add_argument("--release-spec",required=True,type=Path); p.add_argument("--scenario",choices=sorted(TEMPLATES),default="selective"); a=p.parse_args()
 spec=json.loads(a.release_spec.read_text(encoding="utf-8")); payload=prepare(a.output,a.scenario,spec)
 print(json.dumps({"status":"PASS","campaign_id":payload["campaign_id"],"round_id":payload["round_id"],"candidate_sha":payload["candidate_sha"],"output":str(a.output)},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
