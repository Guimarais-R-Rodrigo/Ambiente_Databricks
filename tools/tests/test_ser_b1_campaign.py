from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest import mock

from tools.skill_enforcement.parallel import launcher as b0_launcher
from tools.skill_enforcement.parallel import verifier as b0_verifier
from tools.skill_enforcement.parallel.contract import digest_json, validate_campaign
from tools.skill_enforcement.parallel.registry import load_registry as load_b0_registry
from tools.skill_enforcement.real_campaigns.b1 import adapter, handoff, identity, preflight, registry
from tools.skill_enforcement.real_campaigns.b1.coverage import build_report
from tools.skill_enforcement.real_campaigns.b1.prepare import validate_output_location

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "tools/skill_enforcement/real_campaigns/b1/campaign_template.json"


class RegistryTests(unittest.TestCase):
    def test_b1_registry_is_closed_and_complete(self):
        commands = registry.load_registry()["commands"]
        self.assertEqual(set(registry._ALLOWED_SPECS), set(commands))
        self.assertTrue(all(x.startswith("b1:") for x in commands))

    def test_b0_registry_remains_b0_only(self):
        self.assertTrue(all(x.startswith("b0:") for x in load_b0_registry()["commands"]))

    def test_unknown_command_rejected(self):
        with self.assertRaises(registry.RegistryError):
            registry.resolve_command("b1:unknown")


class CampaignContractTests(unittest.TestCase):
    def setUp(self):
        self.campaign = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    def test_template_valid_under_b0_contract(self):
        self.assertEqual([], validate_campaign(self.campaign))

    def test_concurrency_is_qualified_2_1(self):
        self.assertEqual(2, self.campaign["max_parallel"])
        self.assertEqual(1, self.campaign["max_auditors"])

    def test_read_only_no_effects(self):
        self.assertEqual("READ_ONLY", self.campaign["repo_mode"])
        for task in self.campaign["tasks"]:
            self.assertEqual([], task["write_roots"])
            self.assertEqual("NONE", task["expected_effect"])

    def test_all_task_commands_are_b1_allowlisted(self):
        allowed = set(registry.load_registry()["commands"])
        for task in self.campaign["tasks"]:
            self.assertTrue(set(task["command_ids"]) <= allowed)

    def test_two_fronts_have_no_artificial_dependency(self):
        by_id = {x["task_id"]: x for x in self.campaign["tasks"]}
        self.assertEqual([], by_id["b1.ser03.preflight"]["depends_on"])
        self.assertEqual([], by_id["b1.ser05.preflight"]["depends_on"])
        self.assertNotIn("b1.ser05.preflight", by_id["b1.ser03.execute_verify"]["depends_on"])


class HostQualificationScopeTests(unittest.TestCase):
    def test_preflight_blocks_non_windows_host(self):
        fake = {
            "os": "Linux",
            "filesystem": {"family": "posix", "type": "NOT_OBSERVED"},
        }
        with mock.patch.object(preflight, "probe", return_value=fake):
            report = preflight.check()
        self.assertEqual("FAIL", report["status"])
        self.assertIn("B1_HOST_NOT_QUALIFIED_WINDOWS_REQUIRED", report["issues"])

    def test_preflight_blocks_non_ntfs_windows(self):
        fake = {
            "os": "Windows",
            "filesystem": {"family": "windows", "type": "REFS"},
        }
        with mock.patch.object(preflight, "probe", return_value=fake):
            report = preflight.check()
        self.assertEqual("FAIL", report["status"])
        self.assertIn("B1_HOST_NOT_QUALIFIED_NTFS_REQUIRED", report["issues"])


class CoverageTests(unittest.TestCase):
    def test_case_test_oracle_command_coverage_closes(self):
        report = build_report()
        self.assertEqual("PASS", report["status"], report)
        self.assertEqual(19, report["required_cases"])
        self.assertEqual(5, report["out_of_scope_cases"])


class B0QualificationBindingTests(unittest.TestCase):
    def test_qualified_b0_bytes_are_exact(self):
        self.assertEqual([], identity.qualified_b0_issues())

    def test_b0_blob_mutant_is_detected_without_editing_repository(self):
        real = identity._git_blob
        def fake(path):
            if path.name == "launcher.py":
                return "0" * 40
            return real(path)
        with mock.patch.object(identity, "_git_blob", side_effect=fake):
            self.assertTrue(any("launcher.py" in x for x in identity.qualified_b0_issues()))


class AdapterTests(unittest.TestCase):
    def test_adapter_injects_b1_resolver_and_restores_b0_globals(self):
        campaign = {"sentinel": True}
        spec = {"sentinel": True}
        old_launcher_resolve = b0_launcher.resolve_command
        old_verifier_resolve = b0_verifier.resolve_command
        def fake_execute(received_campaign, evidence_root, received_spec):
            self.assertIs(b0_launcher.resolve_command, registry.resolve_command)
            self.assertIs(b0_verifier.resolve_command, registry.resolve_command)
            self.assertIs(b0_launcher.validate_release_spec, identity.validate_release_spec)
            self.assertIs(b0_launcher.assert_release_spec_current, identity.assert_release_spec_current)
            self.assertEqual(campaign, received_campaign)
            self.assertEqual(spec, received_spec)
            return {"status": "PASS"}
        with mock.patch.object(b0_launcher, "execute", side_effect=fake_execute):
            result = adapter.execute(campaign, Path("unused"), spec)
        self.assertEqual("PASS", result["status"])
        self.assertIs(b0_launcher.resolve_command, old_launcher_resolve)
        self.assertIs(b0_verifier.resolve_command, old_verifier_resolve)

    def test_adapter_restores_globals_after_exception(self):
        old_launcher_resolve = b0_launcher.resolve_command
        old_verifier_resolve = b0_verifier.resolve_command
        with mock.patch.object(b0_launcher, "execute", side_effect=RuntimeError("boom")):
            with self.assertRaisesRegex(RuntimeError, "boom"):
                adapter.execute({}, Path("unused"), {})
        self.assertIs(b0_launcher.resolve_command, old_launcher_resolve)
        self.assertIs(b0_verifier.resolve_command, old_verifier_resolve)


class HandoffTests(unittest.TestCase):
    def test_handoff_contains_profile_digest_and_is_projection(self):
        campaign = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        campaign["candidate_sha"] = "a" * 40
        campaign["round_id"] = "B1ROUND-test"
        campaign["release_spec_digest"] = "b" * 64
        for task in campaign["tasks"]:
            task["candidate_sha"] = campaign["candidate_sha"]
        spec = {
            "candidate_sha": campaign["candidate_sha"],
            "candidate_tree_sha": campaign["candidate_tree_sha"],
            "baseline_sha": campaign["baseline_sha"],
            "round_id": campaign["round_id"],
            "command_registry_digest": campaign["command_registry_digest"],
            "coverage_digest": campaign["coverage_digest"],
            "policy_before_digest": campaign["policy_before_digest"],
            "b0_mechanism_digest": "e" * 64,
            "adapter_id": "SER-B1-ADAPTER-1",
            "python_executable": "C:/Python/python.exe",
        }
        campaign["release_spec_digest"] = digest_json(spec)
        payload = handoff.build_handoff(
            campaign, spec,
            campaign_path=Path("CAMPAIGN.json"),
            release_spec_path=Path("RELEASE_SPEC.json"),
            evidence_dir=Path("EVIDENCE"),
        )
        self.assertEqual(2, payload["max_parallel"])
        self.assertEqual(1, payload["max_auditors"])
        self.assertEqual(64, len(payload["profile_digest"]))
        self.assertTrue(all(x["profile_digest"] == payload["profile_digest"] for x in payload["tasks"]))
        self.assertEqual(spec["python_executable"], payload["execution_argv"][0])
        self.assertEqual(spec["python_executable"], payload["post_run_package_argv"][0])
        self.assertIn("package_evidence", payload["post_run_package_argv"][3])
        self.assertEqual("--output-dir", payload["post_run_package_argv"][4])
        self.assertEqual(
            [x["task_id"] for x in campaign["tasks"]],
            [x["task_id"] for x in payload["tasks"]],
        )
        self.assertIn("USE_3_2_CONCURRENCY", payload["prohibited"])
        broken = dict(campaign)
        broken["release_spec_digest"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "RELEASE_SPEC_DIGEST_MISMATCH"):
            handoff.build_handoff(
                broken, spec,
                campaign_path=Path("CAMPAIGN.json"),
                release_spec_path=Path("RELEASE_SPEC.json"),
                evidence_dir=Path("EVIDENCE"),
            )


class WindowsPythonBootstrapContractTests(unittest.TestCase):
    def test_bootstrap_is_pre_gate_and_has_no_repo_write_commands(self):
        path = ROOT / "tools/skill_enforcement/real_campaigns/b1/resolve_python_windows.ps1"
        text = path.read_text(encoding="utf-8")
        self.assertIn("SER-B1-WINDOWS-PYTHON-RESOLUTION-2", text)
        self.assertIn("sys.executable", text)
        self.assertIn("Python\\PythonCore", text)
        self.assertIn("pyenv-win", text)
        self.assertIn("scoop", text.lower())
        self.assertIn("uv\\python", text)
        self.assertIn("formal_gate_executed = $false", text)
        self.assertNotIn("tools.skill_enforcement.real_campaigns.b1.preflight", text)
        self.assertNotIn("tools.tests.test_ser_b1_campaign", text)
        self.assertNotIn("git commit", text.lower())
        self.assertNotIn("git reset", text.lower())


class OutputLocationTests(unittest.TestCase):
    def test_prepare_rejects_output_inside_repository(self):
        with self.assertRaisesRegex(RuntimeError, "MUST_BE_EXTERNAL"):
            validate_output_location(ROOT / "_b1_evidence")


class IdentityTests(unittest.TestCase):
    def test_release_spec_validator_rejects_b0_schema(self):
        spec = {
            "schema_version": "SER-B0-RELEASE-SPEC-1",
            "round_id": "x", "candidate_sha": "a"*40, "candidate_tree_sha": "b"*40,
            "baseline_sha": "c"*40, "branch": "x",
            "command_registry_digest": "d"*64, "coverage_digest": "e"*64,
            "policy_before_digest": "f"*64, "host_digest": "1"*64,
            "b0_mechanism_digest": "2"*64, "adapter_id": "SER-B1-ADAPTER-1",
            "python_executable": "python", "python_version": "3", "platform": "x",
            "created_at_utc": "now",
        }
        self.assertIn("B1_RELEASE_SPEC_SCHEMA_INVALID", identity.validate_release_spec(spec))


if __name__ == "__main__":
    unittest.main()
