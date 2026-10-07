#!/usr/bin/env python3
"""V06: emite um derivado controlado de um ResolvedTheme para o compositor v2.

A ponte não cria tema, não aplica defaults e não lê JSON arbitrário indicado pelo
usuário. O único seletor externo é ``theme_id``; a configuração correspondente
precisa existir no diretório canônico de exemplos e passar pelo núcleo V02.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = ROOT / "ambiente_databricks" / ".assistant"
TEMA_FILE = ASSISTANT / "hub_snippets" / "visual" / "tema" / "tema.py"
EXAMPLES = ASSISTANT / "hub_padroes" / "identidade_visual" / "exemplos"
THEME_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
ALLOWED_CONTEXTS = {"notebook", "readme", "presentation"}
DERIVATIVE_VERSION = 1


def _load_tema_module():
    spec = importlib.util.spec_from_file_location("hub_tema_v06_bridge", TEMA_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError("THEME_CORE_LOAD: núcleo de temas não pôde ser carregado")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _candidate_for(theme_id: str) -> Path:
    matches: list[Path] = []
    for candidate in sorted(EXAMPLES.glob("*.json")):
        try:
            raw = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"THEME_REGISTRY_INVALID: {candidate.name}") from exc
        if raw.get("theme_id") == theme_id:
            matches.append(candidate)
    if not matches:
        raise RuntimeError("THEME_ID_UNKNOWN: theme_id não existe no conjunto canônico")
    if len(matches) != 1:
        raise RuntimeError("THEME_ID_DUPLICATE: theme_id aparece mais de uma vez")
    return matches[0]


def resolve_derivative(theme_id: str, context: str) -> dict[str, Any]:
    if not isinstance(theme_id, str) or not THEME_ID_RE.fullmatch(theme_id):
        raise RuntimeError("THEME_ID_FORMAT: theme_id fora do formato permitido")
    if context not in ALLOWED_CONTEXTS:
        raise RuntimeError("THEME_CONTEXT: contexto precisa ser notebook, readme ou presentation")

    candidate = _candidate_for(theme_id)
    tema = _load_tema_module()
    relative = candidate.relative_to(ASSISTANT).as_posix()
    resolved = tema.load_theme(ASSISTANT, relative, expected_context=context)
    document = resolved.to_dict()
    if document.get("theme_id") != theme_id:
        raise RuntimeError("THEME_ID_MISMATCH: documento resolvido não corresponde ao seletor")

    # Whitelist deliberada: o compositor recebe somente identidade, rastreabilidade
    # e tokens já validados. Aprovação/publicação nunca atravessam esta fronteira.
    return {
        "derivative_version": DERIVATIVE_VERSION,
        "theme_id": document["theme_id"],
        "theme_version": document["theme_version"],
        "identity_id": document["identity_id"],
        "context": document["context"],
        "mode": document["mode"],
        "asset_set_id": document["asset_set_id"],
        "source": relative,
        "raw_sha256": resolved.raw_sha256,
        "content_sha256": resolved.content_sha256,
        "schema_sha256": resolved.schema_sha256,
        "asset_manifest_sha256": resolved.asset_manifest_sha256,
        "fingerprint": resolved.fingerprint,
        "tokens": document["tokens"],
        "warnings": list(resolved.warnings),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve theme_id para derivado controlado V06")
    parser.add_argument("--theme-id", required=True)
    parser.add_argument("--context", default="readme", choices=sorted(ALLOWED_CONTEXTS))
    args = parser.parse_args()
    try:
        result = resolve_derivative(args.theme_id, args.context)
    except Exception as exc:  # saída curta e fail-closed para consumidor CLI
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
