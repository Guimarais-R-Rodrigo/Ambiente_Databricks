from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.skill_enforcement.parallel.contract import validate_campaign
from tools.skill_enforcement.parallel.process import ROOT
from tools.skill_enforcement.parallel.registry import load_registry as load_b0_registry
from tools.skill_enforcement.real_campaigns.b1.coverage import build_report
from tools.skill_enforcement.real_campaigns.b1.registry import load_registry

TEMPLATE = ROOT / "tools/skill_enforcement/real_campaigns/b1/campaign_template.json"
POLICY = ROOT / "ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json"
FORBIDDEN_DIFF_PATHS = (
    "ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json",
    "ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis",
    "ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt",
    "ambiente_fonte/.assistant/hub_scripts/skill_execution/skill_execution.py",
    "tools/skill_enforcement/parallel",
)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=30)


def check() -> dict:
    issues: list[str] = []
    try:
        registry = load_registry()
    except Exception as exc:
        registry = {"commands": {}}
        issues.append("B1_REGISTRY_INVALID:" + type(exc).__name__ + ":" + str(exc))
    try:
        b0 = load_b0_registry()
        if any(not command_id.startswith("b0:") for command_id in b0["commands"]):
            issues.append("B0_REGISTRY_NOT_CLOSED")
    except Exception as exc:
        issues.append("B0_REGISTRY_INVALID:" + type(exc).__name__)
    coverage = build_report()
    if coverage.get("status") != "PASS":
        issues.extend("B1_" + x for x in coverage.get("issues", []))
    try:
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        issues.extend("B1_TEMPLATE:" + x for x in validate_campaign(template))
        if template.get("max_parallel") != 2 or template.get("max_auditors") != 1:
            issues.append("B1_CONCURRENCY_NOT_2_1")
        known = set(registry["commands"])
        for task in template.get("tasks", []):
            if task.get("write_roots"):
                issues.append("B1_TASK_WRITE_ROOT_PRESENT:" + str(task.get("task_id")))
            if task.get("expected_effect") != "NONE":
                issues.append("B1_TASK_EFFECT_NOT_NONE:" + str(task.get("task_id")))
            for command_id in task.get("command_ids", []):
                if command_id not in known:
                    issues.append("B1_TASK_COMMAND_UNKNOWN:" + command_id)
    except Exception as exc:
        issues.append("B1_TEMPLATE_UNREADABLE:" + type(exc).__name__ + ":" + str(exc))
    try:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        by_skill = {row.get("skill"): row for row in policy.get("skills", []) if isinstance(row, dict)}
        if (by_skill.get("hub-ml-analise-safra") or {}).get("current_level") != "L0":
            issues.append("B1_SER03_POLICY_LEVEL_CHANGED")
        if (by_skill.get("hub-ml-analise-safra") or {}).get("target_level") != "L3":
            issues.append("B1_SER03_POLICY_TARGET_CHANGED")
        if (by_skill.get("hub-ml-cross-eda-ml") or {}).get("current_level") != "L0":
            issues.append("B1_SER05_POLICY_LEVEL_CHANGED")
        if (by_skill.get("hub-ml-cross-eda-ml") or {}).get("target_level") != "L4":
            issues.append("B1_SER05_POLICY_TARGET_CHANGED")
    except Exception as exc:
        issues.append("B1_POLICY_UNREADABLE:" + type(exc).__name__)
    for rel in FORBIDDEN_DIFF_PATHS:
        p = _git("diff", "--quiet", "origin/main...HEAD", "--", rel)
        if p.returncode == 1:
            issues.append("B1_FORBIDDEN_PATH_DIFF:" + rel)
        elif p.returncode not in (0, 1):
            issues.append("B1_GIT_DIFF_ERROR:" + rel)
    behind = _git("rev-list", "--count", "HEAD..origin/main")
    if behind.returncode != 0:
        issues.append("B1_ORIGIN_MAIN_UNREADABLE")
    else:
        try:
            if int(behind.stdout.strip() or "0") != 0:
                issues.append("B1_BRANCH_BEHIND_ORIGIN_MAIN")
        except ValueError:
            issues.append("B1_BEHIND_PARSE_ERROR")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "command_count": len(registry.get("commands", {})),
        "coverage": coverage,
        "max_parallel": 2,
        "max_auditors": 1,
        "b0_modified": any(x.startswith("B1_FORBIDDEN_PATH_DIFF:tools/skill_enforcement/parallel") for x in issues),
    }


def main() -> int:
    report = check()
    print(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
