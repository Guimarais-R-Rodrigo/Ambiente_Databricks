from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from .contract import digest_json, validate_campaign
from .coverage import inventory
from .registry import DEFAULT_REGISTRY, load_registry
ROOT=Path(__file__).resolve().parents[3]
POLICY=ROOT/"ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json"
TEMPLATES={"selective":ROOT/"tools/skill_enforcement/parallel/pilot_campaign.json","global":ROOT/"tools/skill_enforcement/parallel/pilot_global_stop_campaign.json"}

def _git(*args):
 p=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,text=True,timeout=20)
 if p.returncode!=0: raise RuntimeError("GIT_FAILED:"+" ".join(args))
 return p.stdout.strip()

def prepare(output:Path,scenario:str="selective") -> dict:
 campaign=json.loads(TEMPLATES[scenario].read_text(encoding="utf-8")); head=_git("rev-parse","HEAD"); baseline=_git("merge-base","HEAD","origin/main")
 campaign["candidate_sha"]=head; campaign["baseline_sha"]=baseline
 for task in campaign["tasks"]: task["candidate_sha"]=head
 campaign["command_registry_digest"]=digest_json(load_registry(DEFAULT_REGISTRY)); cov=inventory()
 if cov["status"]!="PASS": raise RuntimeError("COVERAGE_NOT_PASS:"+",".join(cov["issues"]))
 campaign["coverage_digest"]=digest_json(cov); campaign["policy_before_digest"]=hashlib.sha256(POLICY.read_bytes()).hexdigest()
 issues=validate_campaign(campaign)
 if issues: raise RuntimeError("CAMPAIGN_INVALID:"+",".join(issues))
 output.write_text(json.dumps(campaign,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8"); return campaign

def main():
 p=argparse.ArgumentParser(); p.add_argument("--output",required=True,type=Path); p.add_argument("--scenario",choices=sorted(TEMPLATES),default="selective"); a=p.parse_args(); payload=prepare(a.output,a.scenario); print(json.dumps({"status":"PASS","campaign_id":payload["campaign_id"],"candidate_sha":payload["candidate_sha"],"output":str(a.output)},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
