"""Ajuste one-shot: reutiliza o patcher V05, preservando o bloco Hub já existente."""
from __future__ import annotations

import v05_finalize_docs_once as base


def patch_hub_readme() -> str:
    if base.SOURCE_README.is_symlink() or base.blob_sha(base.SOURCE_README) != base.EXPECTED_SOURCE_README:
        raise RuntimeError("README .assistant mudou; reconciliar antes de escrever")

    hub = base.SOURCE_README.read_text(encoding="utf-8")
    existing = "### 🎨 Visual Lab do Sistema de Temas — V05 candidata\n"
    base.require_once(hub, existing, "bloco V05 já reconciliado no README do Hub")

    map_row = "| experimentar aparência de notebook sem publicar tema | [Visual Lab](hub_snippets/visual/theme_lab/README.md) |\n"
    if map_row in hub:
        raise RuntimeError("linha do Visual Lab já existe no mapa de uso")

    anchor = "| conferir runtime, dependências e segurança | [Compute e Segurança](#️-dependências-compute-e-segurança) |\n"
    base.require_once(hub, anchor, "âncora do mapa do Hub")
    return hub.replace(anchor, map_row + anchor)


base.patch_hub_readme = patch_hub_readme
raise SystemExit(base.main())
