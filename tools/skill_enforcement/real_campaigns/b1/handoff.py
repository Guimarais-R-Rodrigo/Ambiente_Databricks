from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from tools.skill_enforcement.parallel.contract import digest_json


def _profile_digest(campaign: Mapping[str, Any], release_spec: Mapping[str, Any]) -> str:
    return digest_json({
        "command_registry_digest": release_spec["command_registry_digest"],
        "coverage_digest": release_spec["coverage_digest"],
        "b0_mechanism_digest": release_spec["b0_mechanism_digest"],
        "adapter_id": release_spec["adapter_id"],
        "max_parallel": campaign["max_parallel"],
        "max_auditors": campaign["max_auditors"],
        "resource_limits": campaign.get("resource_limits"),
        "approved_target_vector": campaign.get("approved_target_vector"),
    })


def _assert_campaign_release_binding(campaign: Mapping[str, Any], release_spec: Mapping[str, Any]) -> None:
    if campaign.get("round_id") != release_spec.get("round_id"):
        raise ValueError("HANDOFF_ROUND_MISMATCH")
    for key in (
        "candidate_sha", "candidate_tree_sha", "baseline_sha",
        "command_registry_digest", "coverage_digest", "policy_before_digest",
    ):
        if campaign.get(key) != release_spec.get(key):
            raise ValueError("HANDOFF_RELEASE_FIELD_MISMATCH:" + key)
    if campaign.get("release_spec_digest") != digest_json(dict(release_spec)):
        raise ValueError("HANDOFF_RELEASE_SPEC_DIGEST_MISMATCH")
    python_executable = release_spec.get("python_executable")
    if not isinstance(python_executable, str) or not python_executable:
        raise ValueError("HANDOFF_PYTHON_EXECUTABLE_MISSING")


def build_handoff(
    campaign: Mapping[str, Any],
    release_spec: Mapping[str, Any],
    *,
    campaign_path: Path,
    release_spec_path: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    _assert_campaign_release_binding(campaign, release_spec)
    profile_digest = _profile_digest(campaign, release_spec)
    release_id = campaign["campaign_id"] + ":" + campaign["round_id"]
    tasks = []
    for task in campaign.get("tasks", []):
        tasks.append({
            "task_id": task["task_id"],
            "role_id": task["role"],
            "release_id": release_id,
            "candidate_sha": campaign["candidate_sha"],
            "profile_digest": profile_digest,
            "stage": task["stage"],
            "allowed_command_ids": list(task["command_ids"]),
            "read_roots": list(task["read_roots"]),
            "write_roots": list(task["write_roots"]),
            "forbidden_effects": ["REPO_WRITE", "NETWORK", "SUBPROCESS_CHILD", "EXTERNAL_EFFECT", "POLICY_CHANGE"],
            "output_contract": "SER-PARALLEL-RESULT-3 + command stdout/stderr SHA256",
            "stop_rules": [
                "ONE_ATTEMPT_PER_FORMAL_GATE",
                "FAIL_FAST_WITH_NO_RETRY_UNTIL_GREEN",
                "GLOBAL_CAMPAIGN_FAILURE_STOPS_NEW_TASKS",
                "NO_READY_NO_MERGE_NO_PROMOTION",
            ],
            "resource_lease": {
                "resource_class": task["resource_class"],
                "exclusivity_key": task["exclusivity_key"],
                "max_parallel_total": campaign["max_parallel"],
                "max_auditors_subset": campaign["max_auditors"],
            },
            "evidence_dir": str(evidence_dir / task["task_id"]),
            "authorization_ref": "issue#114:P2_LOCAL_CAMPAIGN_ONLY",
        })
    return {
        "handoff_schema": "SER-B1-HANDOFF-1",
        "campaign_id": campaign["campaign_id"],
        "round_id": campaign["round_id"],
        "release_id": release_id,
        "candidate_sha": campaign["candidate_sha"],
        "profile_digest": profile_digest,
        "release_spec_digest": campaign["release_spec_digest"],
        "campaign_path": str(campaign_path),
        "release_spec_path": str(release_spec_path),
        "evidence_root": str(evidence_dir),
        "max_parallel": campaign["max_parallel"],
        "max_auditors": campaign["max_auditors"],
        "tasks": tasks,
        "execution_argv": [
            release_spec["python_executable"], "-B", "-m", "tools.skill_enforcement.real_campaigns.b1.adapter",
            "--campaign", str(campaign_path),
            "--release-spec", str(release_spec_path),
            "--evidence-dir", str(evidence_dir),
        ],
        "prohibited": [
            "EDIT_CANDIDATE_DURING_CAMPAIGN",
            "CHANGE_POLICY",
            "CHANGE_B0_PARALLEL_MECHANISM",
            "RUN_DATABRICKS_FREE_OR_GENIE",
            "MARK_PR_READY",
            "MERGE_PR",
            "PROMOTE_SKILL",
            "USE_3_2_CONCURRENCY",
        ],
    }


def render_markdown(handoff: Mapping[str, Any]) -> str:
    argv = " ".join(handoff["execution_argv"])
    return (
        "# SER B1 P2 — handoff local gerado do manifesto\n\n"
        f"- campaign: `{handoff['campaign_id']}`\n"
        f"- round: `{handoff['round_id']}`\n"
        f"- candidate: `{handoff['candidate_sha']}`\n"
        f"- profile digest: `{handoff['profile_digest']}`\n"
        f"- concorrência: `{handoff['max_parallel']}/{handoff['max_auditors']}` (total/auditores)\n"
        "- finalidade: executar uma única campanha local read-only e produzir evidência; não promover nem integrar.\n\n"
        "## Comando único da campanha\n\n"
        "```text\n" + argv + "\n```\n\n"
        "Antes desse comando, os gates estáticos/metatestes do pacote devem ter passado uma única vez. "
        "Qualquer exit code não zero interrompe a rodada; não corrigir ou repetir no mesmo round.\n"
    )


def write_handoff(
    campaign: Mapping[str, Any],
    release_spec: Mapping[str, Any],
    *,
    campaign_path: Path,
    release_spec_path: Path,
    evidence_dir: Path,
    output_json: Path,
    output_md: Path,
) -> dict[str, Any]:
    payload = build_handoff(
        campaign, release_spec,
        campaign_path=campaign_path,
        release_spec_path=release_spec_path,
        evidence_dir=evidence_dir,
    )
    output_json.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(payload), encoding="utf-8")
    return payload
