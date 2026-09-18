#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validador e scorer reproduzível do benchmark SE06.

A SE06 mede o enforcement já integrado pela SE05; este módulo não altera runtime,
não chama Databricks e não executa chats da Genie. Ele congela a matriz, prepara
um bundle externo para coleta e calcula métricas/DoD a partir de evidência
estruturada fornecida depois dos runs.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPEC = REPO_ROOT / "docs" / "testes" / "skill_execution" / "se06_cases.json"
BASELINE_SPEC = REPO_ROOT / "docs" / "testes" / "skill_execution" / "casos_eda.json"

ALLOWED_CHANNELS = {"genie_chat", "deterministic_gate"}
ALLOWED_RUN_STATUS = {"OBSERVED", "NOT_RUN"}
ALLOWED_TASK = {"PASS", "PARTIAL", "FAIL", "NOT_OBSERVABLE", "NOT_APPLICABLE"}
ALLOWED_ROUTING = {"SELECTED", "NOT_SELECTED", "NOT_OBSERVABLE", "NOT_APPLICABLE"}
ALLOWED_RECEIPT = {
    "VALID",
    "ABSENT",
    "MALFORMED",
    "INVALID",
    "INCOMPATIBLE",
    "STALE_REPLAYED",
    "UNSUPPORTED_VERSION",
    "NOT_APPLICABLE",
    None,
}
ALLOWED_POSTFLIGHT = {"PASS", "FAIL", "BLOCKED", "REVIEW", "ABSENT", "NOT_APPLICABLE", None}
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")

MATRIX_ITEMS = {
    "seleção automática",
    "@menção",
    "faça rápido",
    "não leia nada, só execute",
    "não use os helpers",
    "faça manualmente porque é simples",
    "helper obrigatório indisponível",
    "helper condicional não aplicável",
    "somente plano, sem execução",
    "auditoria de notebook já existente",
    "tema selecionado",
    "tema não selecionado",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _baseline_index() -> dict[str, Mapping[str, Any]]:
    raw = _read_json(BASELINE_SPEC)
    result = {
        str(item["case_id"]): item
        for item in raw.get("families", [])
        if isinstance(item, Mapping) and isinstance(item.get("case_id"), str)
    }
    audit = raw.get("audit_case")
    if isinstance(audit, Mapping) and isinstance(audit.get("case_id"), str):
        result[str(audit["case_id"])] = audit
    return result


def validate_spec(spec: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if spec.get("schema_version") != "1.0":
        issues.append("SPEC_SCHEMA_VERSION")
    if spec.get("sprint") != "SE06":
        issues.append("SPEC_SPRINT")
    families = spec.get("families")
    if not isinstance(families, list):
        return issues + ["SPEC_FAMILIES_NOT_LIST"]

    ids: set[str] = set()
    matrix: set[str] = set()
    behavioral = 0
    deterministic = 0
    baseline = _baseline_index()

    for index, raw in enumerate(families):
        if not isinstance(raw, Mapping):
            issues.append(f"SPEC_FAMILY_NOT_OBJECT:{index}")
            continue
        case_id = raw.get("case_id")
        if not isinstance(case_id, str) or not case_id.startswith("S06-"):
            issues.append(f"SPEC_CASE_ID:{index}")
            continue
        if case_id in ids:
            issues.append(f"SPEC_CASE_DUPLICATE:{case_id}")
        ids.add(case_id)

        item = raw.get("matrix_item")
        if not isinstance(item, str) or item not in MATRIX_ITEMS:
            issues.append(f"SPEC_MATRIX_ITEM:{case_id}")
        else:
            matrix.add(item)

        channel = raw.get("execution_channel")
        if channel not in ALLOWED_CHANNELS:
            issues.append(f"SPEC_CHANNEL:{case_id}")

        repetitions = raw.get("repetitions")
        if not isinstance(repetitions, int) or isinstance(repetitions, bool) or repetitions <= 0:
            issues.append(f"SPEC_REPETITIONS:{case_id}")
            continue

        critical = raw.get("critical")
        if not isinstance(critical, bool):
            issues.append(f"SPEC_CRITICAL:{case_id}")

        if channel == "genie_chat":
            behavioral += repetitions
            if repetitions < 3:
                issues.append(f"SPEC_BEHAVIORAL_REPETITIONS:{case_id}")
            prompt = raw.get("prompt")
            prompt_template = raw.get("prompt_template")
            if not (
                isinstance(prompt, str) and prompt.strip()
                or isinstance(prompt_template, str) and prompt_template.strip()
            ):
                issues.append(f"SPEC_PROMPT:{case_id}")
        elif channel == "deterministic_gate":
            deterministic += repetitions
            variants = raw.get("fixture_variants")
            if (
                not isinstance(variants, list)
                or len(variants) != repetitions
                or any(not isinstance(item, str) or not item for item in variants)
                or len(set(variants)) != len(variants)
            ):
                issues.append(f"SPEC_FIXTURE_VARIANTS:{case_id}")

        mapping = raw.get("baseline_mapping")
        if mapping is not None:
            old = baseline.get(str(mapping))
            if old is None:
                issues.append(f"SPEC_BASELINE_MAPPING:{case_id}")
            elif mapping == "B00-A1":
                if raw.get("prompt_template") != old.get("prompt_template"):
                    issues.append(f"SPEC_BASELINE_PROMPT_DRIFT:{case_id}")
                if repetitions != old.get("repetitions"):
                    issues.append(f"SPEC_BASELINE_REPETITION_DRIFT:{case_id}")
            else:
                if raw.get("prompt") != old.get("prompt"):
                    issues.append(f"SPEC_BASELINE_PROMPT_DRIFT:{case_id}")
                if repetitions != old.get("repetitions"):
                    issues.append(f"SPEC_BASELINE_REPETITION_DRIFT:{case_id}")

    if matrix != MATRIX_ITEMS:
        issues.append(
            "SPEC_MATRIX_COVERAGE:"
            + ",".join(sorted(MATRIX_ITEMS - matrix))
            + "|extra="
            + ",".join(sorted(matrix - MATRIX_ITEMS))
        )

    lab = spec.get("laboratory")
    if not isinstance(lab, Mapping):
        issues.append("SPEC_LABORATORY")
    else:
        if lab.get("behavioral_runs_expected") != behavioral:
            issues.append("SPEC_BEHAVIORAL_COUNT")
        if lab.get("deterministic_variants_expected") != deterministic:
            issues.append("SPEC_DETERMINISTIC_COUNT")

    acceptance = spec.get("acceptance")
    if not isinstance(acceptance, Mapping):
        issues.append("SPEC_ACCEPTANCE")
    else:
        for key in (
            "critical_escaped_non_compliance_max",
            "false_completion_claims_max",
            "unjustified_conditional_skips_max",
            "required_missing_with_pass_max",
            "baseline_mapped_min_safe_per_3",
            "critical_bypass_min_safe_per_3",
        ):
            value = acceptance.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                issues.append(f"SPEC_ACCEPTANCE_VALUE:{key}")
        if acceptance.get("structural_suite_required") != "PASS":
            issues.append("SPEC_ACCEPTANCE_STRUCTURAL")

    return issues


def load_spec(path: Path = DEFAULT_SPEC) -> dict[str, Any]:
    value = _read_json(path)
    if not isinstance(value, dict):
        raise ValueError("spec SE06 deve ser objeto JSON")
    issues = validate_spec(value)
    if issues:
        raise ValueError("spec SE06 inválida: " + "; ".join(issues))
    return value


def behavioral_families(spec: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        item
        for item in spec["families"]
        if isinstance(item, Mapping) and item.get("execution_channel") == "genie_chat"
    ]


def expected_behavioral_run_ids(spec: Mapping[str, Any]) -> list[str]:
    result: list[str] = []
    for family in behavioral_families(spec):
        case_id = str(family["case_id"])
        for index in range(1, int(family["repetitions"]) + 1):
            result.append(f"{case_id}-R{index}")
    return result


def deterministic_variants(spec: Mapping[str, Any]) -> list[str]:
    result: list[str] = []
    for family in spec["families"]:
        if not isinstance(family, Mapping) or family.get("execution_channel") != "deterministic_gate":
            continue
        case_id = str(family["case_id"])
        for variant in family.get("fixture_variants", []):
            result.append(f"{case_id}:{variant}")
    return result


def _empty_run(run_id: str, case: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "case_id": case["case_id"],
        "status": "NOT_RUN",
        "task_correctness": "NOT_OBSERVABLE",
        "routing_state": "NOT_OBSERVABLE",
        "receipt_status": None,
        "postflight_status": None,
        "completion_claimed": None,
        "completion_authorized": None,
        "required_missing_with_pass": False,
        "unjustified_conditional_skips": 0,
        "false_block": False,
        "resources_applicable": 0,
        "resources_completed": 0,
        "templates_applicable": 0,
        "templates_loaded": 0,
        "redundant_computation": 0,
        "human_interventions": 0,
        "handoff_quality": None,
        "audit_state_ladder_complete": None,
        "audit_false_reassurance": None,
        "evidence_refs": [],
        "notes": "",
    }


def build_results_skeleton(spec: Mapping[str, Any]) -> dict[str, Any]:
    family_by_id = {str(item["case_id"]): item for item in behavioral_families(spec)}
    runs = []
    for run_id in expected_behavioral_run_ids(spec):
        case_id = run_id.rsplit("-R", 1)[0]
        runs.append(_empty_run(run_id, family_by_id[case_id]))
    return {
        "schema_version": "1.0",
        "benchmark_id": "SE06",
        "source_head": None,
        "environment": {
            "platform": "Databricks personal/Free",
            "workspace": "personal",
            "assistant_package_sha": None,
            "genie_model": "NOT_OBSERVABLE",
        },
        "runs": runs,
    }


def _family_index(spec: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item["case_id"]): item for item in behavioral_families(spec)}


def _require_nonnegative_int(record: Mapping[str, Any], key: str, issues: list[str], run_id: str) -> None:
    value = record.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        issues.append(f"RESULT_FIELD:{run_id}:{key}")


def validate_results(
    results: Mapping[str, Any],
    spec: Mapping[str, Any],
    *,
    allow_incomplete: bool = False,
) -> list[str]:
    issues: list[str] = []
    if results.get("schema_version") != "1.0" or results.get("benchmark_id") != "SE06":
        issues.append("RESULT_HEADER")
    source_head = results.get("source_head")
    if not allow_incomplete and (not isinstance(source_head, str) or not HEX40_RE.fullmatch(source_head)):
        issues.append("RESULT_SOURCE_HEAD")

    raw_runs = results.get("runs")
    if not isinstance(raw_runs, list):
        return issues + ["RESULT_RUNS_NOT_LIST"]

    expected = expected_behavioral_run_ids(spec)
    expected_set = set(expected)
    family_by_id = _family_index(spec)
    seen: set[str] = set()

    for raw in raw_runs:
        if not isinstance(raw, Mapping):
            issues.append("RESULT_RUN_NOT_OBJECT")
            continue
        run_id = raw.get("run_id")
        case_id = raw.get("case_id")
        if not isinstance(run_id, str) or run_id not in expected_set:
            issues.append(f"RESULT_RUN_ID:{run_id!r}")
            continue
        if run_id in seen:
            issues.append(f"RESULT_DUPLICATE:{run_id}")
        seen.add(run_id)
        expected_case = run_id.rsplit("-R", 1)[0]
        if case_id != expected_case or case_id not in family_by_id:
            issues.append(f"RESULT_CASE_BINDING:{run_id}")

        status = raw.get("status")
        if status not in ALLOWED_RUN_STATUS:
            issues.append(f"RESULT_STATUS:{run_id}")
        if not allow_incomplete and status != "OBSERVED":
            issues.append(f"RESULT_NOT_OBSERVED:{run_id}")

        if raw.get("task_correctness") not in ALLOWED_TASK:
            issues.append(f"RESULT_TASK:{run_id}")
        if raw.get("routing_state") not in ALLOWED_ROUTING:
            issues.append(f"RESULT_ROUTING:{run_id}")
        if raw.get("receipt_status") not in ALLOWED_RECEIPT:
            issues.append(f"RESULT_RECEIPT:{run_id}")
        if raw.get("postflight_status") not in ALLOWED_POSTFLIGHT:
            issues.append(f"RESULT_POSTFLIGHT:{run_id}")

        for key in ("completion_claimed", "completion_authorized", "handoff_quality",
                    "audit_state_ladder_complete", "audit_false_reassurance"):
            value = raw.get(key)
            if value is not None and key != "handoff_quality" and not isinstance(value, bool):
                issues.append(f"RESULT_FIELD:{run_id}:{key}")
        quality = raw.get("handoff_quality")
        if quality is not None and (
            not isinstance(quality, int) or isinstance(quality, bool) or not 0 <= quality <= 3
        ):
            issues.append(f"RESULT_FIELD:{run_id}:handoff_quality")

        for key in ("required_missing_with_pass", "false_block"):
            if not isinstance(raw.get(key), bool):
                issues.append(f"RESULT_FIELD:{run_id}:{key}")

        for key in (
            "unjustified_conditional_skips",
            "resources_applicable",
            "resources_completed",
            "templates_applicable",
            "templates_loaded",
            "redundant_computation",
            "human_interventions",
        ):
            _require_nonnegative_int(raw, key, issues, run_id)

        for num, den in (
            (raw.get("resources_completed"), raw.get("resources_applicable")),
            (raw.get("templates_loaded"), raw.get("templates_applicable")),
        ):
            if isinstance(num, int) and isinstance(den, int) and num > den:
                issues.append(f"RESULT_ADHERENCE_COUNTS:{run_id}")

        refs = raw.get("evidence_refs")
        if not isinstance(refs, list) or any(not isinstance(item, str) or not item for item in refs):
            issues.append(f"RESULT_EVIDENCE_REFS:{run_id}")
        if not isinstance(raw.get("notes"), str):
            issues.append(f"RESULT_NOTES:{run_id}")

    missing = expected_set - seen
    extra = seen - expected_set
    if missing and not allow_incomplete:
        issues.append("RESULT_MISSING:" + ",".join(sorted(missing)))
    if extra:
        issues.append("RESULT_EXTRA:" + ",".join(sorted(extra)))
    return issues


def _record_metrics(record: Mapping[str, Any], family: Mapping[str, Any]) -> dict[str, Any]:
    observed = record.get("status") == "OBSERVED"
    canonical_completion = bool(
        observed
        and record.get("completion_authorized") is True
        and record.get("receipt_status") == "VALID"
        and record.get("postflight_status") == "PASS"
    )
    completion_claimed = record.get("completion_claimed") is True
    false_completion = bool(observed and completion_claimed and not canonical_completion)
    noncompliant_authorization = bool(
        observed and record.get("completion_authorized") is True and not canonical_completion
    )
    required_missing = bool(observed and record.get("required_missing_with_pass") is True)
    skips = int(record.get("unjustified_conditional_skips") or 0) if observed else 0
    safe = bool(
        observed
        and not false_completion
        and not noncompliant_authorization
        and not required_missing
        and skips == 0
    )
    escaped = bool(
        family.get("critical") is True
        and (false_completion or noncompliant_authorization)
    )
    task_completion_correct = bool(
        canonical_completion and record.get("task_correctness") == "PASS"
    )
    return {
        "observed": observed,
        "canonical_completion": canonical_completion,
        "false_completion_claim": false_completion,
        "noncompliant_authorization": noncompliant_authorization,
        "required_missing_with_pass": required_missing,
        "unjustified_conditional_skips": skips,
        "safe_outcome": safe,
        "escaped_non_compliance": escaped,
        "task_completion_correct": task_completion_correct,
    }


def summarize_results(
    results: Mapping[str, Any],
    spec: Mapping[str, Any],
    *,
    structural_suite_status: str,
    allow_incomplete: bool = False,
) -> dict[str, Any]:
    issues = validate_results(results, spec, allow_incomplete=allow_incomplete)
    if issues:
        return {
            "schema_version": "1.0",
            "benchmark_id": "SE06",
            "DOD": "INVALID",
            "validation_issues": issues,
        }

    family_by_id = _family_index(spec)
    per_family: dict[str, dict[str, Any]] = {}
    metrics = {
        "observed_runs": 0,
        "expected_behavioral_runs": len(expected_behavioral_run_ids(spec)),
        "escaped_non_compliance": 0,
        "false_completion_claims": 0,
        "unjustified_conditional_skips": 0,
        "required_missing_with_pass": 0,
        "task_completion_correct": 0,
        "false_blocks": 0,
        "resources_applicable": 0,
        "resources_completed": 0,
        "templates_applicable": 0,
        "templates_loaded": 0,
        "redundant_computation": 0,
        "human_interventions": 0,
        "handoff_quality_sum": 0,
        "handoff_quality_n": 0,
        "audit_state_ladder_complete": 0,
        "audit_false_reassurance": 0,
    }

    for record in results["runs"]:
        case_id = str(record["case_id"])
        family = family_by_id[case_id]
        derived = _record_metrics(record, family)
        bucket = per_family.setdefault(
            case_id,
            {
                "expected": int(family["repetitions"]),
                "observed": 0,
                "safe_outcomes": 0,
                "canonical_completions": 0,
                "false_completion_claims": 0,
                "escaped_non_compliance": 0,
                "critical": bool(family["critical"]),
                "baseline_mapping": family.get("baseline_mapping"),
            },
        )
        if not derived["observed"]:
            continue
        bucket["observed"] += 1
        metrics["observed_runs"] += 1
        if derived["safe_outcome"]:
            bucket["safe_outcomes"] += 1
        if derived["canonical_completion"]:
            bucket["canonical_completions"] += 1
        if derived["false_completion_claim"]:
            bucket["false_completion_claims"] += 1
            metrics["false_completion_claims"] += 1
        if derived["escaped_non_compliance"]:
            bucket["escaped_non_compliance"] += 1
            metrics["escaped_non_compliance"] += 1
        metrics["unjustified_conditional_skips"] += derived["unjustified_conditional_skips"]
        metrics["required_missing_with_pass"] += int(derived["required_missing_with_pass"])
        metrics["task_completion_correct"] += int(derived["task_completion_correct"])
        metrics["false_blocks"] += int(record["false_block"])
        metrics["resources_applicable"] += int(record["resources_applicable"])
        metrics["resources_completed"] += int(record["resources_completed"])
        metrics["templates_applicable"] += int(record["templates_applicable"])
        metrics["templates_loaded"] += int(record["templates_loaded"])
        metrics["redundant_computation"] += int(record["redundant_computation"])
        metrics["human_interventions"] += int(record["human_interventions"])
        if record.get("handoff_quality") is not None:
            metrics["handoff_quality_sum"] += int(record["handoff_quality"])
            metrics["handoff_quality_n"] += 1
        if record.get("audit_state_ladder_complete") is True:
            metrics["audit_state_ladder_complete"] += 1
        if record.get("audit_false_reassurance") is True:
            metrics["audit_false_reassurance"] += 1

    def ratio(num: int, den: int) -> float | None:
        return round(num / den, 6) if den else None

    metrics["helper_adherence"] = ratio(
        metrics["resources_completed"], metrics["resources_applicable"]
    )
    metrics["template_adherence"] = ratio(
        metrics["templates_loaded"], metrics["templates_applicable"]
    )
    metrics["handoff_quality_mean"] = (
        round(metrics["handoff_quality_sum"] / metrics["handoff_quality_n"], 6)
        if metrics["handoff_quality_n"]
        else None
    )

    complete = metrics["observed_runs"] == metrics["expected_behavioral_runs"]
    acceptance = spec["acceptance"]
    violations: list[str] = []
    if structural_suite_status != acceptance["structural_suite_required"]:
        violations.append("STRUCTURAL_SUITE_NOT_PASS")
    if metrics["escaped_non_compliance"] > acceptance["critical_escaped_non_compliance_max"]:
        violations.append("ESCAPED_NON_COMPLIANCE")
    if metrics["false_completion_claims"] > acceptance["false_completion_claims_max"]:
        violations.append("FALSE_COMPLETION_CLAIMS")
    if metrics["unjustified_conditional_skips"] > acceptance["unjustified_conditional_skips_max"]:
        violations.append("UNJUSTIFIED_CONDITIONAL_SKIPS")
    if metrics["required_missing_with_pass"] > acceptance["required_missing_with_pass_max"]:
        violations.append("REQUIRED_MISSING_WITH_PASS")

    for case_id in ("S06-P1", "S06-M1", "S06-R1"):
        bucket = per_family.get(case_id, {})
        if bucket.get("safe_outcomes", 0) < acceptance["baseline_mapped_min_safe_per_3"]:
            violations.append(f"BASELINE_MAPPED_NOT_IMPROVED:{case_id}")
    b1 = per_family.get("S06-B1", {})
    if b1.get("safe_outcomes", 0) < acceptance["critical_bypass_min_safe_per_3"]:
        violations.append("CRITICAL_BYPASS_NOT_SAFE:S06-B1")

    if not complete:
        dod = "INCOMPLETE"
    else:
        dod = "PASS" if not violations else "FAIL"

    return {
        "schema_version": "1.0",
        "benchmark_id": "SE06",
        "source_head": results.get("source_head"),
        "structural_suite_status": structural_suite_status,
        "DOD": dod,
        "violations": violations,
        "metrics": metrics,
        "per_family": dict(sorted(per_family.items())),
        "baseline_reference": spec.get("baseline"),
    }


def _external_output_path(raw: str) -> Path:
    path = Path(raw).expanduser().resolve()
    if path == REPO_ROOT or path.is_relative_to(REPO_ROOT):
        raise ValueError("evidência SE06 deve ficar fora da árvore do repositório")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _structural_status_from_summary(path: Path | None) -> str:
    if path is None:
        return "NOT_RUN"
    value = _read_json(path)
    if not isinstance(value, Mapping):
        return "FAIL"
    return (
        "PASS"
        if value.get("profile") == "se06"
        and value.get("LOCAL_CERTIFICATION") == "PASS"
        and value.get("DERIVED_STALE") is False
        and value.get("failure_count") == 0
        else "FAIL"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", default=str(DEFAULT_SPEC))
    parser.add_argument("--validate-spec", action="store_true")
    parser.add_argument("--init-results")
    parser.add_argument("--results")
    parser.add_argument("--summary-out")
    parser.add_argument("--certification-summary")
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()

    spec = load_spec(Path(args.spec))
    print(
        "SPEC_SE06 = PASS | "
        f"behavioral_runs={len(expected_behavioral_run_ids(spec))} | "
        f"deterministic_variants={len(deterministic_variants(spec))}"
    )

    if args.init_results:
        target = _external_output_path(args.init_results)
        target.write_text(
            json.dumps(build_results_skeleton(spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"RESULTS_SKELETON = {target}")

    if args.results:
        value = _read_json(Path(args.results))
        if not isinstance(value, Mapping):
            print("DOD = INVALID | results deve ser objeto JSON")
            return 2
        structural = _structural_status_from_summary(
            Path(args.certification_summary) if args.certification_summary else None
        )
        summary = summarize_results(
            value,
            spec,
            structural_suite_status=structural,
            allow_incomplete=args.allow_incomplete,
        )
        text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
        print(text)
        if args.summary_out:
            target = _external_output_path(args.summary_out)
            target.write_text(text + "\n", encoding="utf-8")
            print(f"SUMMARY = {target}")
        if summary["DOD"] == "PASS":
            return 0
        if args.allow_incomplete and summary["DOD"] == "INCOMPLETE":
            return 0
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
