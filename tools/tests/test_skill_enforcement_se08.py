"""Regressões operacionais da SE08 — gates permanentes sem promoção implícita."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
SOURCE = ROOT / "ambiente_databricks"
ASSISTANT = SOURCE / ".assistant"
POLICY = ASSISTANT / "hub_padroes" / "skill_enforcement" / "policy.json"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ci_local  # noqa: E402
import publicar_free  # noqa: E402
import validate_assistant  # noqa: E402
from skill_enforcement import certify_local, se07_policy, validate_contracts  # noqa: E402


class SE08OperationalTests(unittest.TestCase):
    def test_validate_assistant_runs_contract_and_policy_gates_on_selected_root(self):
        problems: list[str] = []
        total, valid, policy_issues = validate_assistant.check_skill_enforcement(
            SOURCE, problems
        )
        self.assertGreater(total, 0)
        self.assertEqual(total, valid)
        self.assertEqual(0, policy_issues)
        self.assertEqual([], problems)

    def test_policy_validator_uses_explicit_assistant_root(self):
        with tempfile.TemporaryDirectory(prefix="sef-se08-root-") as tmp:
            empty_assistant = Path(tmp) / ".assistant"
            empty_assistant.mkdir()
            issues = se07_policy.validate_policy_registry(
                POLICY, assistant_root=empty_assistant
            )
        codes = {issue.code for issue in issues}
        self.assertIn("POLICY_ARTIFACT_MISSING", codes)
        self.assertIn("POLICY_CATALOG_COUNT", codes)

    def test_invalid_utf8_contract_is_structured_unreadable(self):
        with tempfile.TemporaryDirectory(prefix="sef-se08-contract-") as tmp:
            skill_dir = Path(tmp) / "hub-ml-invalid-utf8"
            skill_dir.mkdir()
            path = skill_dir / "execution_contract.json"
            path.write_bytes(b'{"value":"\xff"}')
            result = validate_contracts.validate_contract(
                path, assistant_root=ASSISTANT
            )
        self.assertFalse(result.ok)
        self.assertEqual(["CONTRACT_UNREADABLE"], [issue.code for issue in result.issues])

    def test_ci_local_and_full_certifier_point_to_se08(self):
        self.assertIn("se08", certify_local.PROFILE_STEPS)
        names = [name for name, _ in certify_local.PROFILE_STEPS["se08"]]
        self.assertIn("se07_policy_validation", names)
        self.assertIn("se07_policy_tests", names)
        self.assertIn("se08_policy_io_tests", names)
        self.assertIn("se08_operational_tests", names)
        self.assertIn("se08_storage_cleanup_tests", names)
        self.assertIn("se08_windows_corrective_tests", names)
        self.assertIn("se08_cleanup_diagnostics_tests", names)
        self.assertLess(names.index("se08_operational_tests"), names.index("se08_storage_cleanup_tests"))
        self.assertLess(names.index("se08_storage_cleanup_tests"), names.index("certifier_regression"))
        self.assertIn("assistant_structure", names)
        self.assertIn("render_simulado", names)
        self.assertIn("render_diff", names)
        self.assertIn("readme_snapshot", names)

        sef_stage = next(stage for stage in ci_local.ETAPAS if stage[0] == "sef")
        command = list(sef_stage[2])
        self.assertIn("--profile", command)
        self.assertEqual("se08", command[command.index("--profile") + 1])
        self.assertIn("--skip-render", command)
        self.assertIn("--no-evidence", command)
        self.assertIn("--allow-dirty", command)

    def test_create_object_existing_level_is_preserved(self):
        payload = json.loads(POLICY.read_text(encoding="utf-8"))
        item = next(
            row for row in payload["skills"] if row["skill"] == "hub-ml-criar-objeto"
        )
        self.assertEqual("L3", item["current_level"])
        self.assertEqual("L3", item["target_level"])
        self.assertEqual("stage_specific", item["scope_mode"])
        self.assertEqual("audit", item["rollout_mode"])

    def test_operational_docs_preserve_policy_semantics_and_promotion_blocker(self):
        template = (ASSISTANT/"hub_padroes"/"skill"/"template.md").read_text(encoding="utf-8")
        skills_readme = (ASSISTANT/"skills"/"README.md").read_text(encoding="utf-8")
        policy_readme = (ASSISTANT/"hub_padroes"/"skill_enforcement"/"README.md").read_text(encoding="utf-8")
        manual = (ASSISTANT/"MANUAL_TECNICO_V2.md").read_text(encoding="utf-8")
        root_manual = ROOT/"MANUAL_TECNICO.md"
        playbook = (ROOT/"docs"/"playbooks"/"replicacao-trabalho.md").read_text(encoding="utf-8")
        checklist = (ROOT/"docs"/"playbooks"/"checklist-replicacao.md").read_text(encoding="utf-8")
        root_readme = (ROOT/"README.md").read_text(encoding="utf-8")

        for text in (template, skills_readme, policy_readme, manual):
            self.assertIn("current_level", text)
            self.assertIn("target_level", text)
        # Maintenance execution belongs to its owner; V2 may describe historical command semantics.
        maintainer = (ROOT/"tools"/"skill_enforcement"/"README.md").read_text(encoding="utf-8")
        self.assertIn("--profile se08", maintainer)
        self.assertNotIn("--profile se08", manual.split('<a id="contratos-operacionais-integrados">', 1)[1])
        with self.assertRaises(AssertionError):
            self.assertIn("--profile se08", maintainer.replace("--profile se08", "REMOVED"))
        self.assertFalse(root_manual.exists())
        self.assertIn("S06-A1-R4=NOT_RUN", playbook)
        self.assertIn("SE06_DOD=INCOMPLETE", playbook)
        self.assertIn("15 skills", playbook)
        self.assertIn("PROMOÇÃO", playbook.upper())
        self.assertIn("skill enforcement  : 14/14 contratos válidos", root_readme)
        self.assertIn("BLOQUEADA", checklist)
        self.assertIn("publicar_free.py", checklist)

    def test_se08_minimum_document_set_exists(self):
        root = ROOT/"docs"/"sprints"/"skill_enforcement"/"SE08"
        for name in ("README.md", "TESTES.md", "RESULTADOS.md", "CHECKPOINT.md", "RUNBOOK_LOCAL.md"):
            self.assertTrue((root/name).is_file(), name)

    def test_free_publisher_rejects_corporate_identity_before_auth(self):
        calls: list[tuple[str, ...]] = []

        def fake_databricks_json(*args: str):
            calls.append(tuple(args))
            if args[:2] == ("current-user", "me"):
                # Fixture sintética montada em runtime para não acionar a
                # varredura estática de identidades no próprio teste.
                return {"userName": "@".join(("tester", "bank.example"))}
            self.fail(f"auth should not be queried after corporate identity: {args}")

        with mock.patch.object(publicar_free, "databricks_json", side_effect=fake_databricks_json):
            with self.assertRaises(SystemExit) as ctx:
                publicar_free.resolve_home(
                    expected_host="https://example.invalid",
                    require_explicit_target=True,
                )
        self.assertIn("corporativa", str(ctx.exception))
        self.assertEqual([("current-user", "me", "-o", "json")], calls)


if __name__ == "__main__":
    unittest.main()
