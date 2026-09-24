from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from .contract import digest_json, validate_campaign
from .coverage import inventory
from .registry import DEFAULT_REGISTRY, load_registry

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "tools/skill_enforcement/parallel/pilot_campaign.json"
POLICY = ROOT / "ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json"

def _git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=20)
    if p.returncode != 0:
        raise RuntimeError("GIT_FAILED:" + " ".join(args) + ":" + p.stderr.strip())
    return p.stdout.strip()

def prepare(output: Path) -> dict:
    campaign = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    head = _git("rev-parse", "HEAD")
    baseline = _git("merge-base", "HEAD", "origin/main")
    campaign["candidate_sha"] = head
    campaign["baseline_sha"] = baseline
    for task in campaign["tasks"]:
        task["candidate_sha"] = head
    registry = load_registry(DEFAULT_REGISTRY)
    campaign["command_registry_digest"] = digest_json(registry)
    cov = inventory()
    campaign["coverage_digest"] = digest_json(cov)
    campaign["policy_before_digest"] = hashlib.sha256(POLICY.read_bytes()).hexdigest()
    issues = validate_campaign(campaign)
    if issues:
        raise RuntimeError("CAMPAIGN_INVALID:" + ",".join(issues))
    output.write_text(json.dumps(campaign, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return campaign

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--output",required=True,type=Path); a=p.parse_args(); payload=prepare(a.output)
    print(json.dumps({"status":"PASS","campaign_id":payload["campaign_id"],"candidate_sha":payload["candidate_sha"],"output":str(a.output)},indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
