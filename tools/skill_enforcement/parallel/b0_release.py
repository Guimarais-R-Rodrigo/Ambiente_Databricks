from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from .coverage import inventory
from .host_probe import probe
from .pilot_verify import verify as verify_pilot
from .prepare_pilot import prepare

ROOT = Path(__file__).resolve().parents[3]

def _run(argv: list[str]) -> dict:
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return {"argv": argv, "exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}

def qualify(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=False)
    checks = []

    meta = _run([__import__("sys").executable, "-B", "-m", "unittest", "tools.tests.test_ser_parallel_b0", "-v"])
    checks.append({"name":"metatests","exit_code":meta["exit_code"]})
    (output_dir/"metatests.stdout.txt").write_text(meta["stdout"],encoding="utf-8")
    (output_dir/"metatests.stderr.txt").write_text(meta["stderr"],encoding="utf-8")
    if meta["exit_code"] != 0:
        return {"status":"FAIL","first_failure":"metatests","checks":checks}

    cov = inventory()
    (output_dir/"coverage.json").write_text(json.dumps(cov,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    checks.append({"name":"coverage","exit_code":0 if cov["status"]=="PASS" else 1})
    if cov["status"] != "PASS":
        return {"status":"FAIL","first_failure":"coverage","checks":checks}

    host = probe()
    (output_dir/"host.json").write_text(json.dumps(host,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    checks.append({"name":"host_probe","exit_code":0})

    campaign_path = output_dir/"pilot_campaign.prepared.json"
    campaign = prepare(campaign_path)
    pilot_evidence = output_dir/"pilot_evidence"
    launch = _run([__import__("sys").executable,"-B","-m","tools.skill_enforcement.parallel.launcher","--campaign",str(campaign_path),"--evidence-dir",str(pilot_evidence)])
    checks.append({"name":"pilot_launcher_expected_nonzero","exit_code":launch["exit_code"]})
    (output_dir/"pilot_launcher.stdout.txt").write_text(launch["stdout"],encoding="utf-8")
    (output_dir/"pilot_launcher.stderr.txt").write_text(launch["stderr"],encoding="utf-8")
    summary_path = pilot_evidence/"summary.json"
    if not summary_path.is_file():
        return {"status":"FAIL","first_failure":"pilot_summary_missing","checks":checks}
    pilot = verify_pilot(json.loads(summary_path.read_text(encoding="utf-8")))
    (output_dir/"pilot_verification.json").write_text(json.dumps(pilot,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    checks.append({"name":"pilot_verifier","exit_code":0 if pilot["valid"] else 1})
    status = "PASS" if pilot["valid"] else "FAIL"
    return {
        "status": status,
        "first_failure": None if status=="PASS" else "pilot_verifier",
        "checks": checks,
        "host_sandbox_enforcement": host["sandbox_enforcement"],
        "campaign_id": campaign["campaign_id"],
        "release_scope": "MECHANISM_QUALIFICATION_ONLY_NO_SKILL_PROMOTION",
    }

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",required=True,type=Path); a=p.parse_args()
    result=qualify(a.output_dir)
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
