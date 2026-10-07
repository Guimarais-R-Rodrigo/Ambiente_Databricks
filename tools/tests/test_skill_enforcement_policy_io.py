#!/usr/bin/env python3
"""Regressões de I/O da policy; fixtures sintéticas, sem workspace ou credenciais."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from skill_enforcement import se07_policy as policy
from project_policy import EXPECTED_SKILL_NAMES


class PolicyIOTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sef-policy-io-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills = self.root / "skills"
        self.skills.mkdir()
        self.path = self.root / "policy.json"

    def valid_policy(self):
        entries = []
        for index in range(len(EXPECTED_SKILL_NAMES)):
            name = f"hub-ml-synthetic-{index:02d}"
            folder = self.skills / name
            folder.mkdir(exist_ok=True)
            (folder / "SKILL.md").write_text("Fixture sintética.\n", encoding="utf-8")
            entries.append({
                "skill": name, "risk_class": "low", "current_level": "L0",
                "target_level": "L0", "scope_mode": "whole_skill",
                "rollout_mode": "guidance", "policy_status": "implemented",
                "implemented_artifacts": [f"skills/{name}/SKILL.md"],
                "protected_surfaces": [{"id": "fixture", "level": "L0",
                    "evidence": "static", "rationale": "Teste de leitura; não é catálogo real."}],
                "known_debt": [],
            })
        raw = {"schema_version": "1.0", "policy_id": "SE07-skill-enforcement-policy",
               "skills": entries}
        self.path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        return raw

    def assert_unreadable(self):
        issues = policy.validate_policy_registry(self.path, assistant_root=self.root)
        self.assertEqual([item.code for item in issues], ["POLICY_UNREADABLE"])
        result = policy.summarize(self.path, assistant_root=self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["policy_entries"], 0)
        self.assertEqual([item["code"] for item in result["issues"]], ["POLICY_UNREADABLE"])

    def test_invalid_utf8_api_and_summary(self):
        for value in (b"\xff", b"\xc3(", b'{"skills": "\x80"}'):
            with self.subTest(value=value.hex()):
                self.path.write_bytes(value)
                self.assert_unreadable()

    def test_missing_file(self):
        self.assert_unreadable()

    def test_directory_instead_of_file(self):
        self.path.mkdir()
        self.assert_unreadable()

    def test_malformed_json(self):
        self.path.write_text('{"skills":', encoding="utf-8")
        self.assert_unreadable()

    def test_permission_error(self):
        # Injeção explícita: não depende de chmod, root ou semântica Windows.
        with patch.object(Path, "read_text", side_effect=PermissionError("synthetic denied")):
            self.assert_unreadable()

    def test_non_object_json_is_policy_root_not_unreadable(self):
        for value in (None, [], 7, "fixture"):
            with self.subTest(value=value):
                self.path.write_text(json.dumps(value), encoding="utf-8")
                result = policy.summarize(self.path, assistant_root=self.root)
                self.assertEqual(result["status"], "FAIL")
                self.assertEqual(result["issues"][0]["code"], "POLICY_ROOT")

    def test_valid_synthetic_registry(self):
        self.valid_policy()
        self.assertEqual(policy.validate_policy_registry(self.path, assistant_root=self.root), [])
        result = policy.summarize(self.path, assistant_root=self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["catalog_skills"], len(EXPECTED_SKILL_NAMES))
        self.assertEqual(result["policy_entries"], len(EXPECTED_SKILL_NAMES))
        self.assertEqual(result["issues"], [])

    def test_catalog_can_grow_with_matching_policy(self):
        raw = self.valid_policy()
        name = "hub-ml-synthetic-new"
        folder = self.skills / name
        folder.mkdir()
        (folder / "SKILL.md").write_text("Fixture sintética.\n", encoding="utf-8")
        entry = dict(raw["skills"][0])
        entry["skill"] = name
        entry["implemented_artifacts"] = [f"skills/{name}/SKILL.md"]
        raw["skills"].append(entry)
        self.path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(policy.validate_policy_registry(self.path, assistant_root=self.root), [])

    def test_summary_reads_exactly_once(self):
        self.valid_policy()
        text = self.path.read_text(encoding="utf-8")
        with patch.object(Path, "read_text", side_effect=[text, OSError("synthetic second read")]) as read:
            result = policy.summarize(self.path, assistant_root=self.root)
        self.assertEqual(read.call_count, 1, "Resumo deve reutilizar o parse validado.")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["policy_entries"], len(EXPECTED_SKILL_NAMES))

    def test_validation_reads_exactly_once(self):
        self.valid_policy()
        text = self.path.read_text(encoding="utf-8")
        with patch.object(Path, "read_text", return_value=text) as read:
            self.assertEqual(policy.validate_policy_registry(self.path, assistant_root=self.root), [])
        self.assertEqual(read.call_count, 1)

    def test_summary_does_not_mix_validated_snapshot_with_second_payload(self):
        self.valid_policy()
        text = self.path.read_text(encoding="utf-8")
        with patch.object(Path, "read_text", side_effect=[text, '{"skills": []}']):
            result = policy.summarize(self.path, assistant_root=self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["policy_entries"], len(EXPECTED_SKILL_NAMES))

    def test_summary_unreadable_does_not_retry_read(self):
        with patch.object(Path, "read_text", side_effect=[PermissionError("synthetic denied"), '{}']) as read:
            result = policy.summarize(self.path, assistant_root=self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["policy_entries"], 0)
        self.assertEqual(read.call_count, 1)

    def test_cli_valid_uses_explicit_assistant_root(self):
        self.valid_policy()
        process = self.cli("--assistant-root", str(self.root), "--json")
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["policy_entries"], len(EXPECTED_SKILL_NAMES))
        self.assertEqual(result["catalog_skills"], len(EXPECTED_SKILL_NAMES))

    def cli(self, *arguments):
        # Copia o módulo real para uma raiz sintética mínima, não um clone Git.
        script = self.root / "cli" / "tools" / "skill_enforcement" / "se07_policy.py"
        script.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(policy.__file__), script)
        shutil.copyfile(ROOT / "tools" / "project_policy.py", script.parents[1] / "project_policy.py")
        (self.root / "cli" / "ambiente_databricks" / ".assistant" / "skills").mkdir(parents=True, exist_ok=True)
        return subprocess.run([sys.executable, "-B", str(script), "--policy", str(self.path), *arguments],
                              capture_output=True, text=True, encoding="utf-8", timeout=30)

    def test_cli_invalid_utf8_json(self):
        self.path.write_bytes(b"\xff\xfe\x80")
        process = self.cli("--json")
        self.assertEqual(process.returncode, 1)
        self.assertNotIn("Traceback", process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["issues"][0]["code"], "POLICY_UNREADABLE")

    def test_cli_invalid_utf8_text(self):
        self.path.write_bytes(b"\xc3(")
        process = self.cli()
        self.assertEqual(process.returncode, 1)
        self.assertNotIn("Traceback", process.stderr)
        self.assertIn("SE07_POLICY = FAIL", process.stdout)
        self.assertIn("POLICY_UNREADABLE", process.stdout)

    def test_cli_missing_and_malformed_json(self):
        for value in (None, b'{"skills":'):
            with self.subTest(value=value):
                if value is not None:
                    self.path.write_bytes(value)
                process = self.cli("--json")
                self.assertEqual(process.returncode, 1)
                self.assertNotIn("Traceback", process.stderr)
                self.assertEqual(json.loads(process.stdout)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
