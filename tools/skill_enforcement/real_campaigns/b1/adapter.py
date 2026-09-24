from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from tools.skill_enforcement.parallel import launcher as b0_launcher
from tools.skill_enforcement.parallel import verifier as b0_verifier
from tools.skill_enforcement.real_campaigns.b1.identity import (
    assert_release_spec_current,
    validate_release_spec,
)
from tools.skill_enforcement.real_campaigns.b1.registry import resolve_command


def execute(campaign: dict[str, Any], evidence_root: Path, release_spec: Mapping[str, Any]) -> dict[str, Any]:
    """Reuse the qualified B0 engine while binding it to the closed B1 registry.

    The injection is process-local and restored even if the campaign fails. No
    file under tools/skill_enforcement/parallel is modified.
    """
    old = {
        "launcher_resolve": b0_launcher.resolve_command,
        "launcher_validate_spec": b0_launcher.validate_release_spec,
        "launcher_assert_spec": b0_launcher.assert_release_spec_current,
        "verifier_resolve": b0_verifier.resolve_command,
    }
    try:
        b0_launcher.resolve_command = resolve_command
        b0_launcher.validate_release_spec = validate_release_spec
        b0_launcher.assert_release_spec_current = assert_release_spec_current
        b0_verifier.resolve_command = resolve_command
        return b0_launcher.execute(campaign, evidence_root, release_spec)
    finally:
        b0_launcher.resolve_command = old["launcher_resolve"]
        b0_launcher.validate_release_spec = old["launcher_validate_spec"]
        b0_launcher.assert_release_spec_current = old["launcher_assert_spec"]
        b0_verifier.resolve_command = old["verifier_resolve"]


def main() -> int:
    parser = argparse.ArgumentParser(description="SER B1 adapter over qualified B0 launcher/verifier")
    parser.add_argument("--campaign", required=True, type=Path)
    parser.add_argument("--release-spec", required=True, type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
        release_spec = json.loads(args.release_spec.read_text(encoding="utf-8"))
        summary = execute(campaign, args.evidence_dir, release_spec)
    except Exception as exc:
        summary = {
            "schema_version": "SER-PARALLEL-RUN-3",
            "status": "FAIL",
            "issues": ["B1_ADAPTER_EXCEPTION:" + type(exc).__name__ + ":" + str(exc)],
            "results": {},
            "verification": None,
        }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if summary.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
