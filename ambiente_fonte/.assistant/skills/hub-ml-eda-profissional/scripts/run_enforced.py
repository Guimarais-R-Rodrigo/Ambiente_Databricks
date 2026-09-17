from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable, Mapping


SKILL = "hub-ml-eda-profissional"
ENFORCED_ENTRYPOINT = "skills/hub-ml-eda-profissional/scripts/run_enforced.py::run_enforced"


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do executor L4")


def _load_runner(skill_dir: Path):
    path = skill_dir / "scripts" / "run.py"
    spec = importlib.util.spec_from_file_location("sef_se05_core_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar runner canônico: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_contract(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"execution_contract ilegível: {exc}") from exc
    if not isinstance(value, dict) or value.get("skill") != SKILL:
        raise ValueError("execution_contract inválido para a skill piloto")
    return value


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _append_unique(target: list[str], value: str) -> None:
    if value not in target:
        target.append(value)


def _resource_index(contract: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    resources = contract.get("resources")
    if not isinstance(resources, list):
        return {}
    return {
        str(item.get("id")): dict(item)
        for item in resources
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }


def _template_index(contract: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    templates = contract.get("templates")
    if not isinstance(templates, list):
        return {}
    return {
        str(item.get("id")): dict(item)
        for item in templates
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }


def _decision_map(preflight_payload: Mapping[str, Any]) -> dict[tuple[str, str], Mapping[str, Any]]:
    result: dict[tuple[str, str], Mapping[str, Any]] = {}
    for item_type, key in (("resource", "resources"), ("template", "templates")):
        values = preflight_payload.get(key, [])
        if not isinstance(values, list):
            continue
        for item in values:
            if isinstance(item, Mapping) and isinstance(item.get("item_id"), str):
                result[(item_type, item["item_id"])] = item
    return result


def _full_decisions(preflight_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for item_type, key in (("resource", "resources"), ("template", "templates")):
        values = preflight_payload.get(key, [])
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, Mapping):
                continue
            decisions.append(
                {
                    "item_type": item_type,
                    "item_id": item.get("item_id"),
                    "policy": item.get("policy"),
                    "applicable": item.get("applicable"),
                    "resolved": item.get("resolved"),
                    "target": item.get("target"),
                    "reason": item.get("reason"),
                    "condition": item.get("condition"),
                }
            )
    return decisions


def _spark_table(table_name: str):
    from pyspark.sql import SparkSession

    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    return spark.table(table_name)


def _resolve_display_fn(explicit: Callable[[Any], None] | None) -> Callable[[Any], None] | None:
    if callable(explicit):
        return explicit
    try:
        from IPython import get_ipython

        shell = get_ipython()
        candidate = shell.user_ns.get("display") if shell is not None else None
        if callable(candidate):
            return candidate
    except Exception:
        pass
    return None


def _import_symbol(
    item: Mapping[str, Any],
    *,
    trace: dict[str, Any],
    gaps: list[dict[str, str]],
):
    item_id = str(item.get("id"))
    module_name = item.get("module")
    symbol_name = item.get("symbol")
    try:
        module = importlib.import_module(str(module_name))
        symbol = getattr(module, str(symbol_name))
    except Exception as exc:
        gaps.append(
            {
                "code": "RESOURCE_IMPORT_FAILED",
                "item_id": item_id,
                "message": f"{module_name}.{symbol_name}: {type(exc).__name__}: {exc}",
            }
        )
        return None
    _append_unique(trace["resources_imported"], item_id)
    return symbol


def _call_resource(
    item_id: str,
    func,
    *args,
    trace: dict[str, Any],
    artifacts: dict[str, Any],
    gaps: list[dict[str, str]],
    **kwargs,
):
    _append_unique(trace["resources_called"], item_id)
    try:
        value = func(*args, **kwargs)
    except Exception as exc:
        gaps.append(
            {
                "code": "RESOURCE_CALL_FAILED",
                "item_id": item_id,
                "message": f"{type(exc).__name__}: {exc}",
            }
        )
        artifacts[item_id] = {"status": "failed", "error_type": type(exc).__name__}
        return None, False
    _append_unique(trace["resources_completed"], item_id)
    artifacts[item_id] = {"status": "completed"}
    return value, True


def _load_templates(
    *,
    skill_dir: Path,
    template_items: Mapping[str, Mapping[str, Any]],
    decisions: Mapping[tuple[str, str], Mapping[str, Any]],
    trace: dict[str, Any],
    gaps: list[dict[str, str]],
) -> None:
    for item_id, item in template_items.items():
        decision = decisions.get(("template", item_id))
        if not isinstance(decision, Mapping) or decision.get("applicable") is not True:
            continue
        if decision.get("resolved") is not True:
            gaps.append(
                {
                    "code": "TEMPLATE_UNRESOLVED",
                    "item_id": item_id,
                    "message": "preflight não resolveu template aplicável",
                }
            )
            continue
        rel = item.get("path")
        if not isinstance(rel, str):
            gaps.append(
                {
                    "code": "TEMPLATE_PATH_INVALID",
                    "item_id": item_id,
                    "message": "path de template ausente/inválido",
                }
            )
            continue
        path = skill_dir / rel
        try:
            digest = _sha256_file(path)
        except OSError as exc:
            gaps.append(
                {
                    "code": "TEMPLATE_LOAD_FAILED",
                    "item_id": item_id,
                    "message": str(exc),
                }
            )
            continue
        _append_unique(trace["templates_loaded"], item_id)
        trace["template_digests"][item_id] = digest


def _valid_pk_columns(value: Any) -> list[str] | None:
    if not isinstance(value, list) or not value:
        return None
    if any(not isinstance(item, str) or not item for item in value):
        return None
    return list(value)


def run_enforced(
    table_name: str,
    context: Mapping[str, Any],
    *,
    assistant_root: Path | str | None = None,
    sample_fraction: float = 0.1,
    max_categories: int = 20,
    seed: int = 42,
    display_fn: Callable[[Any], None] | None = None,
    resolved_theme: Any = None,
) -> dict[str, Any]:
    """Executa o core SE04 e coleta evidência adicional necessária ao postflight L4."""
    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    contract_path = skill_dir / "execution_contract.json"
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    runner = _load_runner(skill_dir)
    contract = _load_contract(contract_path)
    base = runner.run(
        table_name,
        context,
        assistant_root=root,
        sample_fraction=sample_fraction,
        max_categories=max_categories,
        seed=seed,
    )
    payload = dict(base)
    trace = payload.get("trace")
    if not isinstance(trace, dict) or trace.get("status") != "PASS":
        return payload

    effective_context = dict(context)
    numeric_provenance = trace.get("context_provenance", {}).get("numeric_columns", {})
    if isinstance(numeric_provenance, Mapping) and isinstance(numeric_provenance.get("value"), int):
        effective_context["numeric_columns"] = numeric_provenance["value"]

    from hub_scripts.skill_execution import run_preflight

    preflight = run_preflight(
        contract_path,
        assistant_root=root,
        context=effective_context,
    )
    preflight_payload = preflight.to_dict()
    trace["decisions"] = _full_decisions(preflight_payload)
    trace["resources_resolved"] = [
        item["item_id"]
        for item in preflight_payload.get("resources", [])
        if isinstance(item, Mapping)
        and item.get("applicable") is True
        and item.get("resolved") is True
        and isinstance(item.get("item_id"), str)
    ]
    trace["resources_imported"] = []
    trace["templates_loaded"] = []
    trace["template_digests"] = {}
    trace["enforcement_entrypoint"] = ENFORCED_ENTRYPOINT

    gaps: list[dict[str, str]] = []
    artifacts: dict[str, Any] = {}
    resource_items = _resource_index(contract)
    template_items = _template_index(contract)
    decisions = _decision_map(preflight_payload)

    _load_templates(
        skill_dir=skill_dir,
        template_items=template_items,
        decisions=decisions,
        trace=trace,
        gaps=gaps,
    )

    quick_item = resource_items.get("quick_profile")
    if quick_item is not None:
        _import_symbol(quick_item, trace=trace, gaps=gaps)
        if "quick_profile" in trace.get("resources_completed", []):
            artifacts["quick_profile"] = {"status": "completed", "source": "core_runner"}

    base_df = None
    analysis_df = None

    def ensure_df():
        nonlocal base_df, analysis_df
        if base_df is None:
            base_df = _spark_table(table_name)
            analysis_df = base_df
        return base_df

    dq_item = resource_items.get("data_quality_check")
    if dq_item is not None:
        func = _import_symbol(dq_item, trace=trace, gaps=gaps)
        pk_columns = _valid_pk_columns(context.get("pk_columns"))
        date_column = context.get("date_column")
        if func is None:
            pass
        elif pk_columns is None:
            gaps.append(
                {
                    "code": "RESOURCE_INPUT_MISSING",
                    "item_id": "data_quality_check",
                    "message": "pk_columns explícitas são necessárias para executar data_quality_check",
                }
            )
        elif date_column is not None and not isinstance(date_column, str):
            gaps.append(
                {
                    "code": "RESOURCE_INPUT_INVALID",
                    "item_id": "data_quality_check",
                    "message": "date_column deve ser string ou null",
                }
            )
        else:
            _call_resource(
                "data_quality_check",
                func,
                table_name,
                pk_columns,
                date_column=date_column,
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )

    null_item = resource_items.get("null_summary")
    if null_item is not None:
        func = _import_symbol(null_item, trace=trace, gaps=gaps)
        if func is not None:
            _call_resource(
                "null_summary",
                func,
                ensure_df(),
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )

    smart_decision = decisions.get(("resource", "smart_sample"))
    if isinstance(smart_decision, Mapping) and smart_decision.get("applicable") is True:
        item = resource_items.get("smart_sample")
        func = _import_symbol(item or {}, trace=trace, gaps=gaps)
        if func is not None:
            raw_n = context.get("sample_n", 1000)
            n = raw_n if isinstance(raw_n, int) and not isinstance(raw_n, bool) and raw_n > 0 else 1000
            sampled, ok = _call_resource(
                "smart_sample",
                func,
                ensure_df(),
                n=n,
                seed=seed,
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )
            if ok:
                analysis_df = sampled

    safe_decision = decisions.get(("resource", "safe_display"))
    if isinstance(safe_decision, Mapping) and safe_decision.get("applicable") is True:
        item = resource_items.get("safe_display")
        func = _import_symbol(item or {}, trace=trace, gaps=gaps)
        renderer = _resolve_display_fn(display_fn)
        if func is None:
            pass
        elif renderer is None:
            gaps.append(
                {
                    "code": "RESOURCE_RUNTIME_UNAVAILABLE",
                    "item_id": "safe_display",
                    "message": "display_fn não está disponível; passe display explicitamente no notebook",
                }
            )
        else:
            _call_resource(
                "safe_display",
                func,
                analysis_df if analysis_df is not None else ensure_df(),
                display_fn=renderer,
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )

    representative_figure = None
    corr_decision = decisions.get(("resource", "correlation_matrix"))
    if isinstance(corr_decision, Mapping) and corr_decision.get("applicable") is True:
        item = resource_items.get("correlation_matrix")
        func = _import_symbol(item or {}, trace=trace, gaps=gaps)
        if func is not None:
            value, ok = _call_resource(
                "correlation_matrix",
                func,
                analysis_df if analysis_df is not None else ensure_df(),
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )
            if ok and isinstance(value, tuple) and value:
                representative_figure = value[0]

    dist_decision = decisions.get(("resource", "distribution_grid"))
    if isinstance(dist_decision, Mapping) and dist_decision.get("applicable") is True:
        item = resource_items.get("distribution_grid")
        func = _import_symbol(item or {}, trace=trace, gaps=gaps)
        if func is not None:
            value, ok = _call_resource(
                "distribution_grid",
                func,
                analysis_df if analysis_df is not None else ensure_df(),
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )
            if ok and representative_figure is None:
                representative_figure = value

    theme_decision = decisions.get(("resource", "theme_plotly"))
    if isinstance(theme_decision, Mapping) and theme_decision.get("applicable") is True:
        item = resource_items.get("theme_plotly")
        func = _import_symbol(item or {}, trace=trace, gaps=gaps)
        if func is None:
            pass
        elif resolved_theme is None:
            gaps.append(
                {
                    "code": "RESOURCE_INPUT_MISSING",
                    "item_id": "theme_plotly",
                    "message": "resolved_theme é obrigatório quando resolved_theme_selected=true",
                }
            )
        elif representative_figure is None:
            gaps.append(
                {
                    "code": "RESOURCE_INPUT_MISSING",
                    "item_id": "theme_plotly",
                    "message": "nenhuma figura determinística disponível para aplicar o tema",
                }
            )
        else:
            _call_resource(
                "theme_plotly",
                func,
                representative_figure,
                resolved_theme,
                trace=trace,
                artifacts=artifacts,
                gaps=gaps,
            )

    artifacts["templates"] = dict(sorted(trace["template_digests"].items()))
    artifacts["enforcement"] = {
        "entrypoint": ENFORCED_ENTRYPOINT,
        "gaps": list(gaps),
    }
    trace["evidence_gaps"] = list(gaps)
    trace["enforcement_status"] = "PASS" if not gaps else "INCOMPLETE"
    trace["artifacts_digest"] = runner._payload_digest(artifacts)
    payload["artifacts"] = artifacts

    from hub_scripts.skill_execution.receipt import build_execution_receipt

    payload["receipt"] = build_execution_receipt(
        trace,
        payload.get("result"),
        expected_skill=runner.SKILL,
        expected_entrypoint=runner.CANONICAL_ENTRYPOINT,
        protected_primitive=runner.PROTECTED_PRIMITIVE_ID,
    )
    return payload


def _load_context(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context-json inválido: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("context-json deve ser objeto JSON")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Executor L4 SE05 da hub-ml-eda-profissional")
    parser.add_argument("--table-name", required=True)
    parser.add_argument("--context-json", required=True)
    parser.add_argument("--sample-fraction", type=float, default=0.1)
    parser.add_argument("--max-categories", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        payload = run_enforced(
            args.table_name,
            _load_context(args.context_json),
            sample_fraction=args.sample_fraction,
            max_categories=args.max_categories,
            seed=args.seed,
        )
    except (RuntimeError, ValueError) as exc:
        payload = {
            "trace": {
                "trace_version": "0.1",
                "skill": SKILL,
                "enforcement_entrypoint": ENFORCED_ENTRYPOINT,
                "status": "BLOCKED",
                "blocking_issues": [{"code": "ENFORCED_RUN_INPUT_INVALID", "message": str(exc)}],
                "fallback_used": False,
                "writes_performed": False,
            },
            "receipt": None,
            "result": None,
            "artifacts": {},
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0 if isinstance(payload.get("receipt"), dict) else 2


if __name__ == "__main__":
    raise SystemExit(main())
