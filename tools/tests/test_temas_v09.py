"""V09 — integração explícita do Sistema de Temas ao kit de transição."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from temas_v09_transicao import (  # noqa: E402
    THEME_CONTRACT_VERSION,
    THEME_REQUIRED_PATHS,
    validate_theme_contract,
    validate_theme_inventory,
)

SIM = ROOT / "Novo_Ambiente_Simulado" / "Users" / "usuario-free"


class ThemeTransitionContractTests(unittest.TestCase):
    def entries(self):
        return [{"path": path, "sha256": "0" * 64, "bytes": 1, "object_type": "FILE"}
                for path in THEME_REQUIRED_PATHS]

    def test_required_theme_files_exist_in_simulated_product(self):
        self.assertGreaterEqual(len(THEME_REQUIRED_PATHS), 9)
        for relative in THEME_REQUIRED_PATHS:
            with self.subTest(relative=relative):
                self.assertTrue((SIM / relative).is_file(), relative)

    def test_contract_is_explicit_and_non_publishing(self):
        contract = validate_theme_inventory(self.entries())
        self.assertEqual(contract["contract_version"], THEME_CONTRACT_VERSION)
        self.assertEqual(contract["transport"], "required_and_hashed")
        self.assertEqual(contract["activation"], "manual_opt_in")
        self.assertEqual(contract["publication"], "not_performed")
        self.assertEqual(contract["required_paths"], list(THEME_REQUIRED_PATHS))

    def test_missing_any_required_file_fails_closed(self):
        for missing in THEME_REQUIRED_PATHS:
            with self.subTest(missing=missing):
                entries = [entry for entry in self.entries() if entry["path"] != missing]
                with self.assertRaises(ValueError):
                    validate_theme_inventory(entries)

    def test_manifest_contract_must_match_inventory(self):
        entries = self.entries()
        good = validate_theme_inventory(entries)
        manifest = {"files": entries, "theme_contract": good}
        self.assertEqual(validate_theme_contract(manifest), good)
        manifest["theme_contract"] = {**good, "publication": "published"}
        with self.assertRaises(ValueError):
            validate_theme_contract(manifest)

    def test_bundle_generator_calls_v09_guard_and_writes_contract(self):
        source = (TOOLS / "bundle_implantacao.py").read_text(encoding="utf-8")
        self.assertIn("validate_theme_inventory(entries)", source)
        self.assertIn('"theme_contract": theme_contract', source)
        self.assertLess(source.index("validate_theme_inventory(entries)"), source.index("with zipfile.ZipFile"))

    def test_existing_manifest_schema_version_is_preserved(self):
        source = (TOOLS / "bundle_implantacao.py").read_text(encoding="utf-8")
        self.assertIn('"schema_version": 2', source)

    def test_transition_checklist_names_theme_contract(self):
        text = (ROOT / "docs/playbooks/checklist-replicacao.md").read_text(encoding="utf-8")
        self.assertIn("theme_contract", text)
        self.assertIn("manual/opt-in", text)
        self.assertIn("não é publicação", text.lower())

    def test_v09_workflow_is_read_only(self):
        text = (ROOT / ".github/workflows/temas-v09-ci.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", text)
        self.assertIn("persist-credentials: false", text)
        self.assertNotIn("contents: write", text)


if __name__ == "__main__":
    unittest.main()
