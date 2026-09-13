"""Aplicador R08 compatível com o schema atual de CONTROLE_MIGRACAO.json."""
from __future__ import annotations

import json
from pathlib import Path

from aplicar_r08 import ROOT, OBJECTS, add_backlinks, edit_notebooks, edit_shared_docs, write_sprint_docs


def update_migration() -> None:
    p = ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    pending = data["pending"]
    removed = []
    for obj in OBJECTS:
        key = f"hub_snippets/ml/{obj}"
        assert key in pending, key
        meta = pending[key]
        assert meta["sprint"] == "R08" and meta["lote"] == "A", (key, meta)
        removed.append(key)
        del pending[key]
    assert len(removed) == 6
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    add_backlinks()
    edit_notebooks()
    edit_shared_docs()
    update_migration()
    write_sprint_docs()


if __name__ == "__main__":
    main()
