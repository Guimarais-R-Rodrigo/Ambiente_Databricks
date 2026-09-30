from __future__ import annotations

import copy
import sys
from datetime import timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, utc_instant
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity
from hub_scripts.skill_execution.postflight import build_postflight, verify_postflight
from hub_scripts.skill_execution.receipt import verify_execution_receipt

def _runner():
    return load_sibling(SKILL_DIR / "scripts/run_pit.py", "_ser06_pit_verifier_runner")

def _contract():
    from hub_scripts.skill_execution.domain_context import loads_strict
    return loads_strict((SKILL_DIR / "pit_contract.json").read_text(encoding="utf-8"))

def _oracle(context: dict, datasets: dict, *, window_days: int) -> tuple[list[dict], dict]:
    """Independent Python as-of oracle; never invokes Spark/pit_join."""
    anchor = context["anchor"]
    history_id = next(s["id"] for s in context["sources"] if s["id"] != anchor)
    facts = datasets[anchor]
    history = datasets[history_id]
    lag = timedelta(days=context["temporal"]["lag_days"])
    window = timedelta(days=window_days)
    by_entity = {}
    for row in history:
        by_entity.setdefault(row["entity_id"], []).append(row)
    records = []
    categories = {"com_feature": 0, "sem_chave_ou_data": 0,
                  "entidade_sem_historico": 0, "sem_feature_disponivel_na_data": 0}
    for fact in facts:
        decision = utc_instant(fact["decision_at"], "decision_at")
        versions = by_entity.get(fact["entity_id"], [])
        eligible = [row for row in versions if
                    decision - window <= utc_instant(row["reference_at"], "reference_at")
                    and utc_instant(row["reference_at"], "reference_at") + lag <= decision]
        selected = max(eligible, key=lambda row: utc_instant(row["reference_at"], "reference_at")) if eligible else None
        category = "com_feature" if selected else (
            "sem_feature_disponivel_na_data" if versions else "entidade_sem_historico")
        categories[category] += 1
        records.append({"decision_id": fact["decision_id"], "entity_id": fact["entity_id"],
                        "decision_at": decision.isoformat(timespec="microseconds").replace("+00:00", "Z"),
                        "feature_value": selected["feature_value"] if selected else None,
                        "available_at": (
                            (utc_instant(selected["reference_at"], "reference_at") + lag)
                            .isoformat(timespec="microseconds").replace("+00:00", "Z")
                        ) if selected else None})
    records.sort(key=lambda row: row["decision_id"])
    n = len(facts)
    diagnostic = {"linhas_fato": n, **categories,
                  "cobertura_pct_linhas_validas": round(100.0 * categories["com_feature"] / n, 2),
                  "linhas_feature_com_ts_nulo": 0,
                  "linhas_com_empate_de_instante": 0,
                  "atraso_publicacao_dias": context["temporal"]["lag_days"],
                  "janela_maxima_dias": window_days, "fuso_da_sessao": "UTC",
                  "colunas_trazidas": ["feature_value"]}
    return records, diagnostic

def verify_result(payload: object, *, expected_context: dict, expected_datasets: dict,
                  expected_window_days: int, expected_run_id: str) -> dict:
    issues = []
    try:
        runner = _runner()
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        prepared = runner.prepare(expected_context, expected_datasets,
                                  window_days=expected_window_days)
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        if not isinstance(payload, dict) or payload.get("status") != "PASS":
            raise ValueError("PAYLOAD_NOT_PASS")
        if set(payload) != {"status", "preflight", "trace", "result", "artifacts",
                            "receipt", "handoff", "postflight", "scope_completion_authorized"}:
            raise ValueError("PAYLOAD_SHAPE_INVALID")
        if digest(payload["preflight"]) != digest(prepared["domain"]):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace, result = payload["trace"], payload["result"]
        if not isinstance(trace, dict) or trace.get("input_digest") != digest({
                "context": expected_context, "datasets": expected_datasets,
                "window_days": expected_window_days}):
            issues.append("INPUT_BINDING_MISMATCH")
        records, diagnostic = _oracle(expected_context, expected_datasets,
                                      window_days=expected_window_days)
        expected = {"schema_version": "SER06-PIT-1", "scope": "LOCAL_SYNTHETIC_PIT_V1",
                    "context_sha256": digest(expected_context),
                    "source_content_sha256": prepared["source_hashes"],
                    "window_days": expected_window_days, "records": records,
                    "diagnostic": diagnostic, "pit_executed": True,
                    "writes_performed": False, "ml_readiness": "NOT_EVALUATED",
                    "promotion_authorized": False}
        if digest(result) != digest(expected):
            issues.append("INDEPENDENT_PIT_ORACLE_MISMATCH")
        if digest(payload["artifacts"]) != digest({runner.PRIMITIVE_ID: result}):
            issues.append("ARTIFACT_BINDING_MISMATCH")
        receipt_verification = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={
                "manifest_name": "release_manifest.json",
                "manifest_sha256": release["manifest_sha256"],
                "contract_git_blob_sha1": release["artifacts"][runner.BASE + "pit_contract.json"],
                "runner_git_blob_sha1": release["artifacts"][runner.BASE + "scripts/run_pit.py"],
            }, release_integrity_ok=True).to_dict()
        if not receipt_verification["valid"]:
            issues.extend(receipt_verification["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(type(exc).__name__ + ":" + str(exc))
        receipt_verification = {"status": "INVALID", "valid": False}
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "receipt_verification": receipt_verification,
            "scope": "LOCAL_SYNTHETIC_PIT_V1"}

def finalize(payload: object, *, expected_context: dict, expected_datasets: dict,
             expected_window_days: int, expected_run_id: str) -> dict:
    """Explicit local profile finalizer, independent of business readiness."""
    check = verify_result(payload, expected_context=expected_context,
                          expected_datasets=expected_datasets,
                          expected_window_days=expected_window_days,
                          expected_run_id=expected_run_id)
    if not isinstance(payload, dict) or payload.get("status") != "PASS":
        raise ValueError("FINALIZE_REQUIRES_PASS")
    final = copy.deepcopy(payload)
    final["handoff"] = {
        "scope": "LOCAL_SYNTHETIC_PIT_V1",
        "source_content_sha256": final["result"]["source_content_sha256"],
        "decision_rows": len(final["result"]["records"]),
        "temporal_contract": expected_context["temporal"],
        "limitations": ["constant lag", "UTC", "LE", "no bitemporal history", "no business readiness"],
    }
    receipt_check = check["receipt_verification"] if check["valid"] else {"status": "INVALID", "valid": False}
    final["postflight"] = build_postflight(final, contract=_contract(),
                                          receipt_verification=receipt_check,
                                          handoff=final["handoff"])
    final["scope_completion_authorized"] = (check["valid"] and
                                            final["postflight"]["status"] == "PASS" and
                                            final["postflight"]["completion_authorized"] is True)
    return final

def verify_finalized(payload: object, *, expected_context: dict, expected_datasets: dict,
                     expected_window_days: int, expected_run_id: str) -> dict:
    check = verify_result(payload, expected_context=expected_context,
                          expected_datasets=expected_datasets,
                          expected_window_days=expected_window_days,
                          expected_run_id=expected_run_id)
    issues = list(check["issues"])
    try:
        if not isinstance(payload, dict) or not isinstance(payload.get("handoff"), dict):
            raise ValueError("HANDOFF_MISSING")
        expected_handoff = {
            "scope": "LOCAL_SYNTHETIC_PIT_V1",
            "source_content_sha256": payload["result"]["source_content_sha256"],
            "decision_rows": len(payload["result"]["records"]),
            "temporal_contract": expected_context["temporal"],
            "limitations": ["constant lag", "UTC", "LE", "no bitemporal history", "no business readiness"],
        }
        if digest(payload["handoff"]) != digest(expected_handoff):
            issues.append("HANDOFF_ORACLE_MISMATCH")
        post = verify_postflight(payload, contract=_contract(),
                                 receipt_verification=check["receipt_verification"]).to_dict()
        if not post["valid"] or not post["completion_authorized"]:
            issues.extend(post["issues"] or ["POSTFLIGHT_NOT_PASS"])
        if payload.get("scope_completion_authorized") is not True:
            issues.append("SCOPE_COMPLETION_NOT_AUTHORIZED")
    except Exception as exc:
        issues.append(type(exc).__name__ + ":" + str(exc))
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "LOCAL_SYNTHETIC_PIT_V1",
            "business_readiness": "NOT_EVALUATED", "promotion_authorized": False}
