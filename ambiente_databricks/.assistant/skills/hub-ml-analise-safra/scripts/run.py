from __future__ import annotations

import importlib
import io
import json
import sys
import uuid
from contextlib import redirect_stdout
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-analise-safra"
ENTRYPOINT = "skills/hub-ml-analise-safra/scripts/run.py::run"
PRIMITIVE_ID = "vintage_core"
PRIMITIVE_MODULE = "hub_snippets.ml.vintage_analysis"
TABLE_COLUMNS = ("safra", "mob", "n_contratos_safra", "n_contratos_observados",
                 "n_eventos_acumulados", "cobertura_observada", "taxa_acumulada", "taxa")
LOCAL_FILES = {"input.schema.json", "execution_contract.json", "scripts/preflight.py", "scripts/run.py", "scripts/verify.py"}
DEPENDENCIES = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_snippets/ml/vintage_analysis/__init__.py",
    "hub_snippets/ml/vintage_analysis/vintage_analysis.py",
}
REQUIRED_RELEASE_PATHS = {f"skills/{SKILL}/{name}" for name in LOCAL_FILES} | DEPENDENCIES


def _preflight_module():
    return load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser03_domain_preflight")


def _canonical_primitive():
    module = importlib.import_module(PRIMITIVE_MODULE)
    expected_file = ASSISTANT_ROOT / "hub_snippets/ml/vintage_analysis/__init__.py"
    if Path(module.__file__).resolve() != expected_file.resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    primitive = getattr(module, "build_vintage_table", None)
    if not callable(primitive):
        raise RuntimeError("CANONICAL_PRIMITIVE_UNAVAILABLE")
    implementation = ASSISTANT_ROOT / "hub_snippets/ml/vintage_analysis/vintage_analysis.py"
    if Path(primitive.__code__.co_filename).resolve() != implementation.resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return primitive


def _normalize_table(frame) -> list[dict]:
    import pandas as pd
    if not isinstance(frame, pd.DataFrame) or set(frame.columns) != set(TABLE_COLUMNS):
        raise RuntimeError("PRIMITIVE_OUTPUT_SCHEMA_MISMATCH")
    rows = []
    for _, source in frame.sort_values(["safra", "mob"]).iterrows():
        row = {name: source[name] for name in TABLE_COLUMNS}
        row["safra"] = str(row["safra"])
        for key in ("mob", "n_contratos_safra", "n_contratos_observados", "n_eventos_acumulados"):
            raw = row[key]
            if isinstance(raw, bool) or pd.isna(raw) or float(raw) != int(raw):
                raise RuntimeError("PRIMITIVE_COUNT_INVALID:" + key)
            row[key] = int(raw)
        for key in ("cobertura_observada", "taxa_acumulada", "taxa"):
            raw = row[key]
            row[key] = None if pd.isna(raw) else float(raw)
        rows.append(row)
    digest(rows)  # Reject non-finite values instead of emitting nonstandard JSON.
    return rows


def run(request: object, *, run_id: str | None = None) -> dict:
    """Candidate L3 monthly/binary facade. Returned artifacts are not authorization.

    The primitive, SEF preflight, and Receipt V1 are reused, not reimplemented.
    Filesystem persistence belongs to a separately authorized evidence collector.
    """
    trace = {"trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
             "run_id": run_id if run_id is not None else str(uuid.uuid4()),
             "status": "BLOCKED", "preflight_status": "NOT_RUN",
             "manifest": "release_manifest.json", "manifest_digest": None,
             "contract_digest": None, "runner_digest": None,
             "input_digest": None, "output_digest": None,
             "resources_resolved": [], "resources_called": [], "resources_completed": [],
             "decisions": [], "context_provenance": {}, "blocking_issues": [],
             "fallback_used": False, "writes_performed": False, "primitive_stdout": ""}
    preflight_result = None
    try:
        if not isinstance(trace["run_id"], str) or not trace["run_id"].strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/execution_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run.py"]
        preflight_result = _preflight_module().preflight(request)
        trace["preflight_status"] = preflight_result["status"]
        if preflight_result["status"] != "PASS":
            trace["blocking_issues"] = list(preflight_result["issues"])
            return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                    "result": None, "receipt": None}
        trace["input_digest"] = digest(request)
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": item["item_id"], "item_type": "resource",
                               "applicable": item["applicable"], "resolved": item["resolved"]}
                              for item in preflight_result["sef"]["resources"]]
        import pandas as pd
        frame = pd.DataFrame(request["rows"], columns=["id", "originated_at", "observed_at", "mob", "target"])
        primitive = _canonical_primitive()
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False,
                                "value": len(frame.select_dtypes(include="number").columns)},
            "population": {"source": "user_intent", "conflict": False},
            "calendar": {"source": "runtime_derived", "conflict": False},
        }
        trace["resources_called"] = [PRIMITIVE_ID]
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            table = primitive(frame, contract_id="id", dt_originacao="originated_at",
                              dt_referencia="observed_at", target="target", safra_grain="month",
                              mob_col="mob", target_is_cumulative=request["semantic_mode"] == "CUMULATIVE")
        trace["primitive_stdout"] = buffer.getvalue()
        trace["resources_completed"] = [PRIMITIVE_ID]
        result = {"schema_version": "SER03-RESULT-1", "profile": preflight_result["profile"],
                  "population_id": request["population_id"], "cutoff": request["cutoff"],
                  "semantic_mode": request["semantic_mode"], "estimand": request["estimand"],
                  "table": _normalize_table(table), "coverage_grid": preflight_result["coverage_grid"],
                  "promotion_authorized": False, "business_readiness": "NOT_EVALUATED"}
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        if Path(build_execution_receipt.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_IMPORT_ORIGIN_MISMATCH")
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT, protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": preflight_result, "trace": trace,
                "result": result, "receipt": receipt}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                "result": None, "receipt": None}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="SER03 candidate: canonical monthly binary calculation")
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        payload = run(loads_strict(args.request.read_text(encoding="utf-8")), run_id=args.run_id)
    except (OSError, UnicodeError, ValueError) as exc:
        payload = {"status": "BLOCKED", "issues": [type(exc).__name__], "receipt": None}
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
