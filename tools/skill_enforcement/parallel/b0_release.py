from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
from .coverage import inventory
from .host_probe import probe
from .pilot_verify import verify as verify_pilot
from .prepare_pilot import prepare
ROOT=Path(__file__).resolve().parents[3]

def _run(argv):
 p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding="utf-8"); return {"argv":argv,"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr}

def qualify(output_dir:Path) -> dict:
 output_dir.mkdir(parents=True,exist_ok=False); checks=[]
 meta=_run([sys.executable,"-B","-m","unittest","tools.tests.test_ser_parallel_b0","-v"]); checks.append({"name":"metatests","exit_code":meta["exit_code"]}); (output_dir/"metatests.stdout.txt").write_text(meta["stdout"],encoding="utf-8"); (output_dir/"metatests.stderr.txt").write_text(meta["stderr"],encoding="utf-8")
 if meta["exit_code"]!=0: return {"status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":"metatests","checks":checks}
 cov=inventory(); (output_dir/"coverage.json").write_text(json.dumps(cov,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); checks.append({"name":"coverage","exit_code":0 if cov["status"]=="PASS" else 1})
 if cov["status"]!="PASS": return {"status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":"coverage","checks":checks}
 host=probe(); (output_dir/"host.json").write_text(json.dumps(host,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); checks.append({"name":"host_probe","exit_code":0})
 for scenario in ("selective","global"):
  campaign_path=output_dir/f"pilot_{scenario}.prepared.json"; campaign=prepare(campaign_path,scenario); evidence=output_dir/f"pilot_{scenario}_evidence"
  launch=_run([sys.executable,"-B","-m","tools.skill_enforcement.parallel.launcher","--campaign",str(campaign_path),"--evidence-dir",str(evidence)]); checks.append({"name":f"pilot_{scenario}_launcher_expected_nonzero","exit_code":launch["exit_code"]}); (output_dir/f"pilot_{scenario}.stdout.txt").write_text(launch["stdout"],encoding="utf-8"); (output_dir/f"pilot_{scenario}.stderr.txt").write_text(launch["stderr"],encoding="utf-8")
  summary_path=evidence/"summary.json"
  if not summary_path.is_file(): return {"status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":f"pilot_{scenario}_summary_missing","checks":checks}
  pilot=verify_pilot(json.loads(summary_path.read_text(encoding="utf-8")),scenario); (output_dir/f"pilot_{scenario}_verification.json").write_text(json.dumps(pilot,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); checks.append({"name":f"pilot_{scenario}_verifier","exit_code":0 if pilot["valid"] else 1})
  if not pilot["valid"]: return {"status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":f"pilot_{scenario}_verifier","checks":checks}
 sandbox_pending=host["sandbox_enforcement"]=="NOT_PROVEN_BY_HOST_PROBE"
 fs_pending=host["os"]=="Windows" and host["filesystem"]["type"]!="NTFS"
 release="PENDING_HOST_QUALIFICATION" if sandbox_pending or fs_pending else "LOCAL_QUALIFIED"
 return {"status":"PASS","release_status":release,"first_failure":None,"checks":checks,"host":host,"release_scope":"MECHANISM_QUALIFICATION_ONLY_NO_SKILL_PROMOTION"}

def main():
 p=argparse.ArgumentParser(); p.add_argument("--output-dir",required=True,type=Path); a=p.parse_args(); result=qualify(a.output_dir); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
