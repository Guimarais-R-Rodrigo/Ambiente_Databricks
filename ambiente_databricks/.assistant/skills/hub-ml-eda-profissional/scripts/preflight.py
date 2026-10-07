from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do script")


def _load_context(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context-json inválido: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("context-json deve ser objeto JSON")
    return parsed


def preflight(context: Mapping[str, Any]) -> dict[str, Any]:
    """Executa somente o gate L2 da skill; não roda a EDA nem escreve no workspace."""
    assistant_root = _resolve_assistant_root()
    assistant_root_text = str(assistant_root)
    if assistant_root_text not in sys.path:
        sys.path.insert(0, assistant_root_text)

    from hub_scripts.skill_execution import run_preflight

    skill_dir = Path(__file__).resolve().parents[1]
    result = run_preflight(
        skill_dir / "execution_contract.json",
        assistant_root=assistant_root,
        context=context,
    )
    return result.to_dict()


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight L2 da skill hub-ml-eda-profissional")
    parser.add_argument(
        "--context-json",
        required=True,
        help="Objeto JSON com as condições objetivas exigidas pelo execution_contract",
    )
    args = parser.parse_args()

    try:
        context = _load_context(args.context_json)
        payload = preflight(context)
    except (RuntimeError, ValueError) as exc:
        payload = {
            "status": "BLOCKED",
            "blocking_issues": [
                {
                    "code": "PREFLIGHT_INPUT_INVALID",
                    "message": str(exc),
                    "item_type": "preflight",
                    "item_id": "$",
                }
            ],
            "writes_performed": False,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
