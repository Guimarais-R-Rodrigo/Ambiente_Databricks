from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT_ROOT = ROOT / "ambiente_fonte/.assistant"
FIXTURES = ROOT / "tools/tests/fixtures/ser_b1"
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_UNAVAILABLE:" + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _same_table(left: list[dict], right: list[dict]) -> bool:
    if len(left) != len(right):
        return False
    for a, b in zip(left, right):
        if set(a) != set(b):
            return False
        for key in a:
            x, y = a[key], b[key]
            if isinstance(x, float) or isinstance(y, float):
                if x is None or y is None:
                    if x is not y:
                        return False
                elif not math.isclose(float(x), float(y), abs_tol=1e-12, rel_tol=1e-12):
                    return False
            elif x != y:
                return False
    return True


def _manual_vintage(request: dict) -> list[dict]:
    cohort_size: dict[str, int] = defaultdict(int)
    for row in request["cohort_roster"]:
        cohort_size[row["originated_at"][:7]] += 1
    rows_by_cell: dict[tuple[str, int], list[dict]] = defaultdict(list)
    event_history: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
    for row in request["rows"]:
        cohort = row["originated_at"][:7]
        rows_by_cell[(cohort, int(row["mob"]))].append(row)
        event_history[(cohort, row["id"])].append((int(row["mob"]), int(row["target"])))
    out = []
    for (cohort, mob), rows in sorted(rows_by_cell.items()):
        denominator = cohort_size[cohort]
        observed = len(rows)
        if request["semantic_mode"] == "CUMULATIVE":
            accumulated = sum(int(row["target"]) for row in rows)
        else:
            accumulated = 0
            ids = {row["id"] for row in rows}
            for uid in ids:
                accumulated += sum(target for seen_mob, target in event_history[(cohort, uid)] if seen_mob <= mob)
        complete = observed == denominator
        rate = accumulated / denominator if complete else None
        out.append({
            "safra": cohort,
            "mob": mob,
            "n_contratos_safra": denominator,
            "n_contratos_observados": observed,
            "n_eventos_acumulados": accumulated,
            "cobertura_observada": observed / denominator,
            "taxa_acumulada": rate,
            "taxa": rate,
        })
    return out


def audit_ser03() -> dict:
    runner = _load(
        ASSISTANT_ROOT / "skills/hub-ml-analise-safra/scripts/run.py",
        "_b1p2_domain_audit_ser03_runner",
    )
    evidence = []
    for filename in ("vf_cumulative.json", "vf_events.json"):
        fixture = _fixture(filename)
        oracle = _manual_vintage(fixture["request"])
        if not _same_table(oracle, fixture["expected_table"]):
            raise RuntimeError("FIXTURE_ORACLE_MISMATCH:" + filename)
        payload = runner.run(fixture["request"], run_id="B1P2-AUDIT-" + fixture["fixture_id"])
        if payload.get("status") != "PASS" or not _same_table(payload["result"]["table"], oracle):
            raise RuntimeError("RUNTIME_MANUAL_ORACLE_MISMATCH:" + filename)
        if payload["result"].get("promotion_authorized") is not False:
            raise RuntimeError("PROMOTION_AUTHORITY_ESCALATION:" + filename)
        evidence.append({
            "fixture_id": fixture["fixture_id"],
            "manual_oracle_rows": len(oracle),
            "runtime_matches_manual_oracle": True,
            "fixed_denominator": True,
            "missing_observation_not_zero": True,
        })
    return {
        "status": "PASS",
        "audit": "SER03_DOMAIN",
        "scope": "MONTHLY_BINARY_PILOT_V1",
        "evidence": evidence,
        "effect": "NONE",
    }


def audit_ser05() -> dict:
    cross = _load(
        ASSISTANT_ROOT / "skills/hub-ml-cross-eda-ml/scripts/preflight.py",
        "_b1p2_domain_audit_ser05_preflight",
    )
    evidence = []
    for filename in ("ce_l2_temporal.json", "ce_l2_static.json"):
        fixture = _fixture(filename)
        context = fixture["context"]
        payload = cross.preflight(context)
        expected = fixture["expected_context"]
        if payload.get("status") != "PASS":
            raise RuntimeError("SER05_PREFLIGHT_NOT_PASS:" + filename)
        if cross.verify_preflight(payload, expected_context=context).get("valid") is not True:
            raise RuntimeError("SER05_PREFLIGHT_BINDING_INVALID:" + filename)
        checks = {
            "context_status": payload.get("context_status") == expected["context_status"],
            "join_executed": payload.get("join_executed") is expected["join_executed"],
            "ml_readiness": payload.get("ml_readiness") == expected["ml_readiness"],
            "pit": (payload.get("temporal_context") or {}).get("pit") == expected["pit"],
            "effect": context.get("requested_effect") == expected["effect"],
            "source_declared_not_read": payload.get("source_identity_status") == "DECLARED_NOT_READ",
            "coverage_not_measured": payload.get("coverage_measured") is False,
            "writes_none": payload.get("writes_performed") is False,
            "promotion_not_authorized": payload.get("promotion_authorized") is False,
        }
        if not all(checks.values()):
            raise RuntimeError("SER05_DOMAIN_ASSERTION_FAILED:" + filename)
        evidence.append({"fixture_id": fixture["fixture_id"], **checks})
    return {
        "status": "PASS",
        "audit": "SER05_DOMAIN",
        "scope": "CONTEXT_ONLY_PILOT_V1",
        "evidence": evidence,
        "effect": "NONE",
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"ser03", "ser05"}:
        print(json.dumps({"status": "FAIL", "issue": "ACTION_NOT_ALLOWLISTED"}, sort_keys=True))
        return 2
    try:
        result = audit_ser03() if sys.argv[1] == "ser03" else audit_ser05()
    except Exception as exc:
        result = {"status": "FAIL", "issue": type(exc).__name__ + ":" + str(exc)}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
