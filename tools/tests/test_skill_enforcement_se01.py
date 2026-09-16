#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressões da SE01 — contrato estático, retirada do probe e publicação Free."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "validate_contracts.py"
SCHEMA_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "execution_contract.schema.json"
PUBLISHER_PATH = REPO_ROOT / "tools" / "publicar_free.py"
CONTRACT_PATH = (
    REPO_ROOT
    / "ambiente_fonte"
    / ".assistant"
    / "skills"
    / "hub-ml-eda-profissional"
    / "execution_contract.json"
)
SKILL_PATH = CONTRACT_PATH.parent / "SKILL.md"
PROBE_PATH = CONTRACT_PATH.parent / "scripts" / "capability_probe.py"
ASSISTANT_ROOT = REPO_ROOT / "ambiente_fonte" / ".assistant"

spec = importlib.util.spec_from_file_location("sef_validate_contracts", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

publisher_spec = importlib.util.spec_from_file_location("sef_publicar_free", PUBLISHER_PATH)
publisher = importlib.util.module_from_spec(publisher_spec)
assert publisher_spec and publisher_spec.loader
sys.modules[publisher_spec.name] = publisher
publisher_spec.loader.exec_module(publisher)


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def validate_mutant(self, mutator):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "hub-ml-eda-profissional"
            skill_dir.mkdir(parents=True)
            for template in self.canonical["templates"]:
                target = skill_dir / template["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# fixture\n", encoding="utf-8")
            payload = copy.deepcopy(self.canonical)
            mutator(payload, skill_dir)
            path = skill_dir / "execution_contract.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return validator.validate_contract(path, assistant_root=ASSISTANT_ROOT)

    def assert_has_code(self, result, code):
        self.assertIn(code, {issue.code for issue in result.issues}, result.to_dict())

    def test_canonical_contract_is_valid(self):
        result = validator.validate_contract(CONTRACT_PATH)
        self.assertTrue(result.ok, result.to_dict())
        self.assertEqual(result.resources, 10)
        self.assertEqual(result.templates, 4)
        self.assertEqual(result.mode, "audit")

    def test_schema_vocabularies_match_validator(self):
        self.assertEqual(
            {self.schema["properties"]["schema_version"]["const"]},
            validator.SUPPORTED_SCHEMA_VERSIONS,
        )
        self.assertEqual(
            {self.schema["properties"]["mode"]["const"]},
            validator.SUPPORTED_MODES,
        )
        resource_props = self.schema["$defs"]["resource"]["properties"]
        self.assertEqual(set(resource_props["policy"]["enum"]), validator.SUPPORTED_POLICIES)
        self.assertEqual(set(resource_props["evidence"]["enum"]), validator.SUPPORTED_EVIDENCE)
        condition_kinds = set(
            self.schema["$defs"]["condition"]["properties"]["kind"]["enum"]
        )
        self.assertEqual(condition_kinds, set(validator.SUPPORTED_CONDITIONS))

    def test_missing_helper_module_fails(self):
        result = self.validate_mutant(
            lambda payload, _: payload["resources"][0].update(
                module="hub_scripts.helper_inexistente"
            )
        )
        self.assert_has_code(result, "RESOURCE_MODULE_NOT_FOUND")

    def test_non_exported_symbol_fails(self):
        result = self.validate_mutant(
            lambda payload, _: payload["resources"][0].update(
                symbol="simbolo_nao_exportado"
            )
        )
        self.assert_has_code(result, "RESOURCE_SYMBOL_NOT_EXPORTED")

    def test_missing_template_fails(self):
        def mutate(payload, skill_dir):
            (skill_dir / payload["templates"][0]["path"]).unlink()
        result = self.validate_mutant(mutate)
        self.assert_has_code(result, "TEMPLATE_NOT_FOUND")

    def test_unsupported_schema_version_fails(self):
        result = self.validate_mutant(
            lambda payload, _: payload.update(schema_version="9.9")
        )
        self.assert_has_code(result, "SCHEMA_VERSION_UNSUPPORTED")

    def test_duplicate_resource_fails(self):
        def mutate(payload, _):
            payload["resources"].append(copy.deepcopy(payload["resources"][0]))
        result = self.validate_mutant(mutate)
        self.assert_has_code(result, "RESOURCE_DUPLICATE")

    def test_invalid_condition_fails(self):
        def mutate(payload, _):
            payload["resources"][3]["condition"] = {"kind": "python_eval", "value": 2}
        result = self.validate_mutant(mutate)
        self.assert_has_code(result, "CONDITION_INVALID")

    def test_skill_folder_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "hub-ml-outra-skill"
            skill_dir.mkdir(parents=True)
            payload = copy.deepcopy(self.canonical)
            for template in payload["templates"]:
                target = skill_dir / template["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# fixture\n", encoding="utf-8")
            path = skill_dir / "execution_contract.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = validator.validate_contract(path, assistant_root=ASSISTANT_ROOT)
        self.assert_has_code(result, "SKILL_FOLDER_MISMATCH")

    def test_enforce_mode_is_rejected_in_se01(self):
        result = self.validate_mutant(
            lambda payload, _: payload.update(mode="enforce")
        )
        self.assert_has_code(result, "MODE_INVALID")

    def test_index_generator_uses_real_public_package(self):
        row = next(
            item for item in self.canonical["resources"] if item["id"] == "index_generator"
        )
        self.assertEqual(row["module"], "hub_snippets.visual.index_generator")
        self.assertEqual(row["symbol"], "gerar_indice_eda")


class ProbeRetirementTests(unittest.TestCase):
    def test_temporary_probe_is_retired_from_product(self):
        self.assertFalse(PROBE_PATH.exists(), "probe temporário deve sair do produto final da SE01")
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertNotIn("Capability probe SE01", skill_text)
        self.assertNotIn("scripts/capability_probe.py", skill_text)


class FreePublisherCompatibilityTests(unittest.TestCase):
    def _run_plan(self, remote_status):
        calls = []

        def fake_databricks(*args):
            calls.append(args)
            return 0, "", ""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            notebook = root / ".assistant" / "hub_padroes" / "notebook" / "template.py"
            notebook.parent.mkdir(parents=True)
            notebook.write_text("# Databricks notebook source\nprint('fixture')\n", encoding="utf-8")
            with (
                mock.patch.object(publisher, "conferir_fonte_espelho", return_value=[]),
                mock.patch.object(publisher, "eh_notebook", return_value=True),
                mock.patch.object(publisher, "databricks", side_effect=fake_databricks),
                mock.patch.object(publisher, "databricks_json", return_value=remote_status),
            ):
                result = publisher.cmd_plan(root, [notebook], "/Users/tester", True)
        return result, calls

    def test_import_dir_notebook_materialized_skips_redundant_import(self):
        result, calls = self._run_plan({"object_type": "NOTEBOOK", "language": "PYTHON"})
        self.assertEqual(result, 0)
        self.assertTrue(any(call[:2] == ("workspace", "import-dir") for call in calls))
        self.assertFalse(any(call[:2] == ("workspace", "import") for call in calls))

    def test_import_dir_without_notebook_uses_source_fallback(self):
        result, calls = self._run_plan({"object_type": "FILE"})
        self.assertEqual(result, 0)
        fallback = [call for call in calls if call[:2] == ("workspace", "import")]
        self.assertEqual(len(fallback), 1)
        self.assertIn("SOURCE", fallback[0])
        self.assertIn("PYTHON", fallback[0])
        self.assertIn("--overwrite", fallback[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
