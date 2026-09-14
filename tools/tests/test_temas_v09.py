"""V09 — integração explícita do Sistema de Temas ao kit de transição."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from temas_v09_transicao import (  # noqa: E402
    THEME_CONTRACT_VERSION,
    THEME_REQUIRED_PATHS,
    validate_theme_contract,
    validate_theme_inventory,
    validate_theme_zip,
)

SIM = ROOT / "Novo_Ambiente_Simulado" / "Users" / "usuario-free"


class ThemeTransitionContractTests(unittest.TestCase):
    def entries(self):
        return [{"path": path, "sha256": "0" * 64, "bytes": 1, "object_type": "FILE"}
                for path in THEME_REQUIRED_PATHS]

    def package_fixture(self):
        payloads = {path: ("v09:" + path).encode("utf-8") for path in THEME_REQUIRED_PATHS}
        entries = [
            {
                "path": path,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "object_type": "FILE",
            }
            for path, raw in payloads.items()
        ]
        manifest = {
            "schema_version": 2,
            "files": entries,
            "theme_contract": validate_theme_inventory(entries),
        }
        return payloads, manifest

    def write_package(self, path: Path, *, omit=None, tamper=None):
        payloads, manifest = self.package_fixture()
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, raw in payloads.items():
                if name == omit:
                    continue
                archive.writestr(name, b"adulterado" if name == tamper else raw)
            archive.writestr("MANIFEST.json", json.dumps(manifest, ensure_ascii=False))
        return manifest

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
        self.assertIn("manual_opt_in", text)
        self.assertIn("não é publicação", text.lower())

    def test_v09_workflow_is_read_only(self):
        text = (ROOT / ".github/workflows/temas-v09-ci.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", text)
        self.assertIn("persist-credentials: false", text)
        self.assertNotIn("contents: write", text)

    def test_valid_zip_verifies_actual_theme_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "01_IMPORTAR_HUB_fixture.zip"
            manifest = self.write_package(package)
            contract = validate_theme_zip(package)
            self.assertEqual(contract, manifest["theme_contract"])
            self.assertEqual(contract["required_paths"], list(THEME_REQUIRED_PATHS))

    def test_zip_missing_or_tampered_required_file_fails(self):
        target = THEME_REQUIRED_PATHS[0]
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.zip"
            self.write_package(missing, omit=target)
            with self.assertRaises(ValueError):
                validate_theme_zip(missing)

            tampered = Path(directory) / "tampered.zip"
            self.write_package(tampered, tamper=target)
            with self.assertRaises(ValueError):
                validate_theme_zip(tampered)

    def test_operational_workflow_prepares_node_dependencies_before_ci_gate(self):
        text = (ROOT / ".github/workflows/kit-transicao-trabalho.yml").read_text(encoding="utf-8")
        setup_node = "actions/setup-node@v4"
        install_pnpm = "npm install --global pnpm@10.34.5"
        install_visuals = "pnpm --dir tools/readme_visuals install --frozen-lockfile"
        ci_gate = "python tools/ci_local.py --verbose"
        for expected in (setup_node, install_pnpm, install_visuals, ci_gate):
            self.assertIn(expected, text)
        self.assertLess(text.index(setup_node), text.index(install_pnpm))
        self.assertLess(text.index(install_pnpm), text.index(install_visuals))
        self.assertLess(text.index(install_visuals), text.index(ci_gate))

    def test_both_workflows_verify_generated_zip_before_use(self):
        command = "python -B tools/temas_v09_transicao.py --kit-dir"
        v09 = (ROOT / ".github/workflows/temas-v09-ci.yml").read_text(encoding="utf-8")
        kit = (ROOT / ".github/workflows/kit-transicao-trabalho.yml").read_text(encoding="utf-8")
        self.assertIn(command, v09)
        self.assertIn(command, kit)
        self.assertLess(kit.index(command), kit.index("actions/upload-artifact@v4"))
        self.assertNotIn("contents: write", kit)


if __name__ == "__main__":
    unittest.main()
