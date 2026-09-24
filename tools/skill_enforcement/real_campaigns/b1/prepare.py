from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.skill_enforcement.parallel.contract import digest_json, validate_campaign
from tools.skill_enforcement.real_campaigns.b1.handoff import write_handoff
from tools.skill_enforcement.real_campaigns.b1.identity import (
    build_release_spec,
    capture_round_start,
)
from tools.skill_enforcement.real_campaigns.b1.preflight import check

ROOT = Path(__file__).resolve().parents[4]
TEMPLATE = ROOT / "tools/skill_enforcement/real_campaigns/b1/campaign_template.json"


def prepare(output_dir: Path) -> dict:
    preflight = check()
    if preflight.get("status") != "PASS":
        raise RuntimeError("B1_P2_PREFLIGHT_NOT_PASS")
    output_dir = output_dir.resolve()
    if output_dir.exists():
        if any(output_dir.iterdir()):
            raise RuntimeError("B1_P2_OUTPUT_DIR_MUST_BE_NEW_OR_EMPTY")
    else:
        output_dir.mkdir(parents=True)
    round_start = capture_round_start()
    release_spec = build_release_spec(round_start)
    campaign = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    campaign["round_id"] = release_spec["round_id"]
    campaign["release_spec_digest"] = digest_json(release_spec)
    campaign["candidate_sha"] = release_spec["candidate_sha"]
    campaign["candidate_tree_sha"] = release_spec["candidate_tree_sha"]
    campaign["baseline_sha"] = release_spec["baseline_sha"]
    campaign["command_registry_digest"] = release_spec["command_registry_digest"]
    campaign["coverage_digest"] = release_spec["coverage_digest"]
    campaign["policy_before_digest"] = release_spec["policy_before_digest"]
    campaign["state"] = "AUTHORING_READY"
    for task in campaign["tasks"]:
        task["candidate_sha"] = release_spec["candidate_sha"]
    bad = validate_campaign(campaign)
    if bad:
        raise RuntimeError("B1_P2_CAMPAIGN_INVALID:" + ",".join(bad))
    paths = {
        "round_start": output_dir / "ROUND_START.json",
        "release_spec": output_dir / "RELEASE_SPEC.json",
        "campaign": output_dir / "CAMPAIGN.json",
        "handoff_json": output_dir / "HANDOFF.json",
        "handoff_md": output_dir / "CODEX_HANDOFF.md",
        "evidence": output_dir / "EVIDENCE",
    }
    paths["round_start"].write_text(json.dumps(round_start, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    paths["release_spec"].write_text(json.dumps(release_spec, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    paths["campaign"].write_text(json.dumps(campaign, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    handoff = write_handoff(
        campaign, release_spec,
        campaign_path=paths["campaign"],
        release_spec_path=paths["release_spec"],
        evidence_dir=paths["evidence"],
        output_json=paths["handoff_json"],
        output_md=paths["handoff_md"],
    )
    return {
        "status": "PASS",
        "candidate_sha": release_spec["candidate_sha"],
        "round_id": release_spec["round_id"],
        "output_dir": str(output_dir),
        "campaign": str(paths["campaign"]),
        "release_spec": str(paths["release_spec"]),
        "handoff": str(paths["handoff_md"]),
        "evidence_dir_must_not_exist_before_launch": str(paths["evidence"]),
        "execution_argv": handoff["execution_argv"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare immutable B1 P2 campaign + mechanically derived handoff")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = prepare(args.output_dir)
    except Exception as exc:
        report = {"status": "FAIL", "issue": type(exc).__name__ + ":" + str(exc)}
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if report.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
