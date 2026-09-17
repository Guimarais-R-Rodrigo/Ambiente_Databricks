from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Mapping


SKILL = "hub-ml-eda-profissional"
TRACE_VERSION = "0.1"
MANIFEST_VERSION = "0.1"
CANONICAL_ENTRYPOINT = "skills/hub-ml-eda-profissional/scripts/run.py::run"
PROTECTED_PRIMITIVE_ID = "quick_profile"


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do runner")


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")


def _payload_digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _safe_relative_path(raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw:
        return None
    path = Path(raw)
    if path.is_absolute() or raw.startswith(("/", "\\")) or ".." in path.parts:
        return None
    return path


def _load_manifest(manifest_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"manifest ilegível: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("manifest deve ser objeto JSON")
    if payload.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError(f"manifest_version não suportada: {payload.get('manifest_version')!r}")
    if payload.get("skill") != SKILL:
        raise ValueError(f"skill do manifest inválida: {payload.get('skill')!r}")
    if payload.get("algorithm") != "git_blob_sha1":
        raise ValueError(f"algoritmo de fingerprint inválido: {payload.get('algorithm')!r}")
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("manifest.artifacts deve ser lista não vazia")
    return payload


def _verify_release(
    assistant_root: Path,
    manifest_path: Path,
) -> tuple[bool, list[dict[str, str]], dict[str, str]]:
    issues: list[dict[str, str]] = []
    observed: dict[str, str] = {}
    try:
        manifest = _load_manifest(manifest_path)
    except ValueError as exc:
        return False, [{"code": "RELEASE_MANIFEST_INVALID", "message": str(exc)}], observed

    seen_paths: set[str] = set()
    for raw in manifest["artifacts"]:
        if not isinstance(raw, dict):
            issues.append({"code": "RELEASE_MANIFEST_INVALID", "message": "artifact deve ser objeto"})
            continue
        rel = _safe_relative_path(raw.get("path"))
        expected = raw.get("git_blob_sha1")
        role = raw.get("role")
        if rel is None or not isinstance(expected, str) or len(expected) != 40 or not isinstance(role, str):
            issues.append(
                {
                    "code": "RELEASE_MANIFEST_INVALID",
                    "message": f"artifact inválido: {raw!r}",
                }
            )
            continue
        rel_text = rel.as_posix()
        if rel_text in seen_paths:
            issues.append(
                {
                    "code": "RELEASE_MANIFEST_INVALID",
                    "message": f"path duplicado no manifest: {rel_text}",
                }
            )
            continue
        seen_paths.add(rel_text)
        target = assistant_root / rel
        if not target.is_file():
            issues.append(
                {
                    "code": "RELEASE_INTEGRITY_MISMATCH",
                    "message": f"artefato protegido ausente: {rel_text}",
                }
            )
            continue
        actual = _git_blob_sha1(target)
        observed[rel_text] = actual
        if actual != expected:
            issues.append(
                {
                    "code": "RELEASE_INTEGRITY_MISMATCH",
                    "message": f"fingerprint divergente: {rel_text}",
                }
            )

    return not issues, issues, observed


def _numeric_columns_from_dtypes(dtypes: list[tuple[str, str]]) -> int:
    numeric_bases = {
        "tinyint",
        "smallint",
        "int",
        "bigint",
        "float",
        "double",
        "decimal",
    }
    return sum(
        1
        for _, dtype in dtypes
        if dtype.lower().split("(", 1)[0] in numeric_bases
    )


def _derive_numeric_columns(table_name: str) -> tuple[int, str]:
    try:
        from pyspark.sql import SparkSession
    except Exception as exc:
        raise RuntimeError(f"pyspark indisponível para derivar schema: {exc}") from exc

    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    try:
        dtypes = list(spark.table(table_name).dtypes)
    except Exception as exc:
        raise RuntimeError(f"não foi possível observar schema de {table_name}: {exc}") from exc
    return _numeric_columns_from_dtypes(dtypes), "spark.table(...).dtypes"


def _derive_context(
    table_name: str,
    context: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, dict[str, Any]], list[dict[str, str]]]:
    effective = dict(context)
    provenance: dict[str, dict[str, Any]] = {
        key: {
            "value": value,
            "source": "agent_declared",
            "evidence": "runner_input",
        }
        for key, value in effective.items()
    }
    issues: list[dict[str, str]] = []

    try:
        observed_numeric, evidence = _derive_numeric_columns(table_name)
    except RuntimeError as exc:
        issues.append({"code": "RUNTIME_CONTEXT_UNAVAILABLE", "message": str(exc)})
        return None, provenance, issues

    declared_numeric = effective.get("numeric_columns")
    if declared_numeric is not None and (
        not isinstance(declared_numeric, int)
        or isinstance(declared_numeric, bool)
        or declared_numeric < 0
    ):
        issues.append(
            {
                "code": "CONTEXT_PROVENANCE_CONFLICT",
                "message": "numeric_columns declarado deve ser inteiro >= 0 quando informado",
            }
        )
        return None, provenance, issues

    if declared_numeric is not None and declared_numeric != observed_numeric:
        issues.append(
            {
                "code": "CONTEXT_PROVENANCE_CONFLICT",
                "message": (
                    f"numeric_columns declarado={declared_numeric} diverge do "
                    f"runtime_derived={observed_numeric}"
                ),
            }
        )
        provenance["numeric_columns"] = {
            "value": observed_numeric,
            "source": "runtime_derived",
            "evidence": evidence,
            "declared_value": declared_numeric,
            "conflict": True,
        }
        return None, provenance, issues

    effective["numeric_columns"] = observed_numeric
    provenance["numeric_columns"] = {
        "value": observed_numeric,
        "source": "runtime_derived",
        "evidence": evidence,
        "declared_value": declared_numeric,
        "conflict": False,
    }
    return effective, provenance, issues


def _default_quick_profile(
    table_name: str,
    *,
    sample_fraction: float,
    max_categories: int,
    seed: int,
) -> Any:
    module = importlib.import_module("hub_scripts.quick_profile")
    primitive = getattr(module, "quick_profile")
    return primitive(
        table_name,
        sample_fraction=sample_fraction,
        max_categories=max_categories,
        seed=seed,
    )


def _base_trace(
    *,
    run_id: str,
    manifest_path: Path,
    manifest_digest: str | None,
    observed_fingerprints: Mapping[str, str],
) -> dict[str, Any]:
    contract_key = f"skills/{SKILL}/execution_contract.json"
    runner_key = f"skills/{SKILL}/scripts/run.py"
    return {
        "trace_version": TRACE_VERSION,
        "run_id": run_id,
        "skill": SKILL,
        "entrypoint": CANONICAL_ENTRYPOINT,
        "manifest": manifest_path.name,
        "manifest_digest": manifest_digest,
        "contract_digest": observed_fingerprints.get(contract_key),
        "runner_digest": observed_fingerprints.get(runner_key),
        "input_digest": None,
        "output_digest": None,
        "preflight_status": "NOT_RUN",
        "context_provenance": {},
        "decisions": [],
        "resources_resolved": [],
        "resources_called": [],
        "resources_completed": [],
        "fallback_used": False,
        "writes_performed": False,
        "blocking_issues": [],
        "status": "BLOCKED",
    }


def _trace_issue(trace: dict[str, Any], code: str, message: str, *, status: str) -> None:
    trace["blocking_issues"].append({"code": code, "message": message})
    trace["status"] = status


def _payload(trace: Mapping[str, Any], result: Any, execution_receipt: Any = None) -> dict[str, Any]:
    return {"trace": dict(trace), "receipt": execution_receipt, "result": result}


def run(
    table_name: str,
    context: Mapping[str, Any],
    *,
    assistant_root: Path | str | None = None,
    manifest_path: Path | str | None = None,
    sample_fraction: float = 0.1,
    max_categories: int = 20,
    seed: int = 42,
) -> dict[str, Any]:
    """Executa o core protegido da EDA e emite Receipt V1 quando a rota é canônica."""
    run_id = uuid.uuid4().hex
    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    manifest = Path(manifest_path) if manifest_path is not None else skill_dir / "release_manifest.json"

    if not isinstance(table_name, str) or not table_name.strip():
        trace = _base_trace(
            run_id=run_id,
            manifest_path=manifest,
            manifest_digest=None,
            observed_fingerprints={},
        )
        _trace_issue(trace, "RUN_INPUT_INVALID", "table_name deve ser string não vazia", status="BLOCKED")
        return _payload(trace, None)

    if not isinstance(context, Mapping):
        trace = _base_trace(
            run_id=run_id,
            manifest_path=manifest,
            manifest_digest=None,
            observed_fingerprints={},
        )
        _trace_issue(trace, "RUN_INPUT_INVALID", "context deve ser mapping", status="BLOCKED")
        return _payload(trace, None)

    integrity_ok, integrity_issues, observed = _verify_release(root, manifest)
    manifest_digest = _sha256(manifest) if manifest.is_file() else None
    trace = _base_trace(
        run_id=run_id,
        manifest_path=manifest,
        manifest_digest=manifest_digest,
        observed_fingerprints=observed,
    )
    if not integrity_ok:
        for issue in integrity_issues:
            _trace_issue(trace, issue["code"], issue["message"], status="BLOCKED")
        return _payload(trace, None)

    effective_context, provenance, provenance_issues = _derive_context(table_name, context)
    trace["context_provenance"] = provenance
    if provenance_issues or effective_context is None:
        for issue in provenance_issues:
            _trace_issue(trace, issue["code"], issue["message"], status="BLOCKED")
        return _payload(trace, None)

    trace["input_digest"] = _payload_digest(
        {
            "table_name": table_name,
            "context": effective_context,
            "sample_fraction": sample_fraction,
            "max_categories": max_categories,
            "seed": seed,
        }
    )

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from hub_scripts.skill_execution import run_preflight

    contract_path = skill_dir / "execution_contract.json"
    preflight = run_preflight(
        contract_path,
        assistant_root=root,
        context=effective_context,
    )
    preflight_payload = preflight.to_dict()
    trace["preflight_status"] = preflight.status
    trace["decisions"] = [
        {
            "item_id": item["item_id"],
            "item_type": item["item_type"],
            "applicable": item["applicable"],
            "resolved": item["resolved"],
        }
        for item in (*preflight_payload["resources"], *preflight_payload["templates"])
    ]
    trace["resources_resolved"] = [
        item["item_id"]
        for item in preflight_payload["resources"]
        if item["applicable"] is True and item["resolved"] is True
    ]

    if preflight.status != "PASS":
        trace["blocking_issues"].extend(preflight_payload["blocking_issues"])
        trace["status"] = "BLOCKED"
        return _payload(trace, None)

    trace["resources_called"].append(PROTECTED_PRIMITIVE_ID)
    try:
        result = _default_quick_profile(
            table_name,
            sample_fraction=sample_fraction,
            max_categories=max_categories,
            seed=seed,
        )
    except Exception as exc:
        _trace_issue(
            trace,
            "REQUIRED_PRIMITIVE_FAILED",
            f"{PROTECTED_PRIMITIVE_ID} falhou: {type(exc).__name__}: {exc}",
            status="FAIL",
        )
        return _payload(trace, None)

    trace["resources_completed"].append(PROTECTED_PRIMITIVE_ID)
    trace["output_digest"] = _payload_digest(result)
    trace["status"] = "PASS"

    from hub_scripts.skill_execution.receipt import build_execution_receipt

    execution_receipt = build_execution_receipt(
        trace,
        result,
        expected_skill=SKILL,
        expected_entrypoint=CANONICAL_ENTRYPOINT,
        protected_primitive=PROTECTED_PRIMITIVE_ID,
    )
    return _payload(trace, result, execution_receipt)


def is_canonically_compliant(
    payload: Mapping[str, Any],
    *,
    expected_run_id: str | None = None,
) -> bool:
    """Classifica evidência L3 da SE03; preservado para regressão histórica."""
    trace = payload.get("trace")
    if not isinstance(trace, Mapping):
        return False
    if expected_run_id is not None and trace.get("run_id") != expected_run_id:
        return False
    if not isinstance(trace.get("output_digest"), str):
        return False
    if trace.get("output_digest") != _payload_digest(payload.get("result")):
        return False
    provenance = trace.get("context_provenance")
    if not isinstance(provenance, Mapping):
        return False
    numeric = provenance.get("numeric_columns")
    if not isinstance(numeric, Mapping) or numeric.get("source") != "runtime_derived":
        return False
    return bool(
        trace.get("trace_version") == TRACE_VERSION
        and trace.get("skill") == SKILL
        and trace.get("entrypoint") == CANONICAL_ENTRYPOINT
        and trace.get("status") == "PASS"
        and trace.get("preflight_status") == "PASS"
        and trace.get("fallback_used") is False
        and isinstance(trace.get("manifest_digest"), str)
        and isinstance(trace.get("contract_digest"), str)
        and isinstance(trace.get("runner_digest"), str)
        and isinstance(trace.get("input_digest"), str)
        and PROTECTED_PRIMITIVE_ID in trace.get("resources_called", [])
    )


def verify_receipt(
    payload: Mapping[str, Any],
    *,
    expected_run_id: str | None = None,
    assistant_root: Path | str | None = None,
    manifest_path: Path | str | None = None,
) -> dict[str, Any]:
    """Verifica Receipt SE04 contra payload e release corrente; não é postflight SE05."""
    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    manifest = Path(manifest_path) if manifest_path is not None else skill_dir / "release_manifest.json"
    integrity_ok, _, observed = _verify_release(root, manifest)
    manifest_digest = _sha256(manifest) if manifest.is_file() else ""
    contract_key = f"skills/{SKILL}/execution_contract.json"
    runner_key = f"skills/{SKILL}/scripts/run.py"
    expected_release = {
        "manifest_sha256": manifest_digest,
        "contract_git_blob_sha1": observed.get(contract_key, ""),
        "runner_git_blob_sha1": observed.get(runner_key, ""),
    }

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from hub_scripts.skill_execution.receipt import verify_execution_receipt

    return verify_execution_receipt(
        payload,
        expected_skill=SKILL,
        expected_entrypoint=CANONICAL_ENTRYPOINT,
        protected_primitive=PROTECTED_PRIMITIVE_ID,
        expected_run_id=expected_run_id,
        expected_release=expected_release,
        release_integrity_ok=integrity_ok,
    ).to_dict()


def _load_context(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context-json inválido: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("context-json deve ser objeto JSON")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner estrutural SE04 da skill hub-ml-eda-profissional")
    parser.add_argument("--table-name", required=True)
    parser.add_argument("--context-json", required=True)
    parser.add_argument("--sample-fraction", type=float, default=0.1)
    parser.add_argument("--max-categories", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        context = _load_context(args.context_json)
        payload = run(
            args.table_name,
            context,
            sample_fraction=args.sample_fraction,
            max_categories=args.max_categories,
            seed=args.seed,
        )
    except (RuntimeError, ValueError) as exc:
        payload = {
            "trace": {
                "trace_version": TRACE_VERSION,
                "skill": SKILL,
                "entrypoint": CANONICAL_ENTRYPOINT,
                "status": "BLOCKED",
                "blocking_issues": [{"code": "RUN_INPUT_INVALID", "message": str(exc)}],
                "fallback_used": False,
                "writes_performed": False,
            },
            "receipt": None,
            "result": None,
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0 if payload.get("trace", {}).get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
