#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressões da SE01 — contrato estático e capability probe."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "validate_contracts.py"
SCHEMA_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "execution_contract.schema.json"
CONTRACT_PATH = (
    REPO_ROOT
    / "ambiente_fonte"
    / ".assistant"
    / "skills"
    / "hub-ml-eda-profissional"
    / "execution_contract.json"
)
PROBE_PATH = CONTRACT_PATH.parent / "scripts" / "capability_probe.py"
ASSISTANT_ROOT = REPO_ROOT / "ambiente_fonte" / ".assistant"

spec = importlib.util.spec_from_file_location("sef_validate_contracts", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


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


class CapabilityProbeTests(unittest.TestCase):
    def test_probe_runs_read_only_against_source_assistant(self):
        run = subprocess.run(
            [
                sys.executable,
                "-B",
                str(PROBE_PATH),
                "--assistant-root",
                str(ASSISTANT_ROOT),
            ],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr or run.stdout)
        payload = json.loads(run.stdout.strip())
        self.assertEqual(payload["marker"], "SEF_CAPABILITY_PROBE_V0_1")
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["sample_result"], "1.234")
        self.assertFalse(payload["writes_performed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
