"""Guardas de rotas e limites editoriais reconciliados em 07/10/2026."""
from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
VISUAL = Path("ambiente_fonte/.assistant/hub_readmes_visual_assets")


class ReadmeAuditRoutesTests(unittest.TestCase):
    def test_visual_operational_guides_point_to_current_maintenance_owner(self):
        for rel in ("README.md", "headers/README.md", "visual_system/guia_visual.md"):
            with self.subTest(rel=rel):
                text = (ROOT / VISUAL / rel).read_text(encoding="utf-8")
                links = re.findall(r"https://github\.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/[^)\s]+", text)
                guides = [url for url in links if url.endswith("/tools/readme_visuals/README.md")]
                self.assertEqual(1, len(guides))
                path = unquote(urlparse(guides[0]).path)
                self.assertIn("/blob/main/", path)
                self.assertTrue((ROOT / path.split("/blob/main/", 1)[1]).is_file())

    def test_header_provenance_is_linked_outside_installed_payload(self):
        text = (ROOT / VISUAL / "headers/README.md").read_text(encoding="utf-8")
        provenance = "tools/readme_visuals/assets/headers/src/PROMPT_FUNDO.md"
        self.assertIn("/blob/main/" + provenance + ")", text)
        self.assertTrue((ROOT / provenance).is_file())
        self.assertNotIn("em `src/PROMPT_FUNDO.md`", text)
        self.assertIn("fora do pacote instalado", text)

    def test_exemplars_keep_operational_limits_without_undated_sprint_references(self):
        for rel, limit in (
            ("snippet/taxa_resposta_campanha/README.md", "não certifica o runtime Databricks"),
            ("script/checar_base_campanha/README.md", "não resultados de uma execução observada"),
            ("prompt/analisar_campanha/README.md", "não certifica uma nova execução"),
        ):
            with self.subTest(rel=rel):
                text = (ROOT / "ambiente_fonte/.assistant/hub_padroes" / rel).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"esta R01|desta sprint")
                self.assertIn(limit, text)
                self.assertIn("ambiente", text)

    def test_adr_index_has_no_orphan_catalog_rows(self):
        lines = (ROOT / "docs/decisions/README.md").read_text(encoding="utf-8").splitlines()
        adr_rows = [i for i, line in enumerate(lines) if re.match(r"\| \[\d{4}\]\(ADR-\d+", line)]
        self.assertTrue(adr_rows)
        self.assertEqual(list(range(adr_rows[0], adr_rows[-1] + 1)), adr_rows)
        self.assertTrue(any("(ADR-0026" in lines[i] for i in adr_rows))


if __name__ == "__main__":
    unittest.main()
