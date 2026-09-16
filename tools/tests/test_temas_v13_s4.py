from __future__ import annotations

import ast
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import temas_v13_diagnostico as diag  # noqa: E402
from tools import temas_v13_preflight as s2  # noqa: E402
from tools import temas_v13_release as s3  # noqa: E402


class V13S4DiagnosticTests(unittest.TestCase):
    @staticmethod
    def check(code: str, status: str, *, check_id: str = "fixture", message: str = "fixture"):
        return {
            "check_id": check_id,
            "status": status,
            "code": code,
            "message": message,
        }

    def s2_report(self, code: str, status: str, *, operation: bool = False, message="fixture", check_id="fixture"):
        check = self.check(code, status, check_id=check_id, message=message)
        operations = []
        request_checks = []
        if operation:
            operations = [
                {
                    "surface_id": "fixture_surface",
                    "action_id": "fixture_action",
                    "status": status,
                    "checks": [check],
                }
            ]
        else:
            request_checks = [check]
        return {
            "report_version": 1,
            "engine": "V13-S2",
            "mode": "surface",
            "overall_status": status,
            "request_checks": request_checks,
            "operations": operations,
            "network_access": False,
            "remote_mutation_performed": False,
        }

    def s3_report(self, code: str, status: str, *, message="fixture", check_id="fixture", receipt=None):
        report = {
            "report_version": 1,
            "engine": "V13-S3",
            "mode": "release",
            "overall_status": status,
            "checks": [self.check(code, status, check_id=check_id, message=message)],
            "network_access": False,
            "remote_mutation_performed": False,
            "publication_performed": False,
        }
        if status == "PASS":
            report["receipt"] = receipt if receipt is not None else {"fixture": True}
        elif receipt is not None:
            report["receipt"] = receipt
        return report

    @staticmethod
    def request(source_report, evidence=None):
        return {
            "diagnostic_version": 1,
            "source_report": source_report,
            "evidence": evidence or [],
        }

    @staticmethod
    def codes(report):
        return {event["safe_code"] for event in report["events"]}

    @staticmethod
    def stages(report):
        return {event["stage"] for event in report["events"]}

    def test_source_code_registry_matches_s2_owner_exactly(self):
        self.assertEqual(diag.SOURCE_CODES["V13-S2"], s2.STABLE_CODES)

    def test_source_code_registry_matches_s3_owner_exactly(self):
        self.assertEqual(diag.SOURCE_CODES["V13-S3"], s3.STABLE_CODES)

    def test_input_contract_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s2_report("REQUEST_FIELDS", "FAIL")))
        self.assertEqual(report["diagnostic_status"], "FAIL")
        self.assertIn("INPUT_CONTRACT", self.stages(report))

    def test_canonical_contract_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s2_report("THEME_INVALID", "FAIL", operation=True)))
        self.assertIn("CANONICAL_CONTRACT", self.stages(report))

    def test_artifact_integrity_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s2_report("BUNDLE_INCOMPLETE", "FAIL", operation=True)))
        self.assertIn("ARTIFACT_INTEGRITY", self.stages(report))

    def test_git_state_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s3_report("TREE_DIRTY", "FAIL")))
        self.assertIn("GIT_STATE", self.stages(report))

    def test_preflight_readiness_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s3_report("PREFLIGHT_BLOCKED", "BLOCKED")))
        self.assertEqual(report["diagnostic_status"], "BLOCKED")
        self.assertIn("PREFLIGHT_READINESS", self.stages(report))

    def test_authorization_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s2_report("AUTHORIZATION_REQUIRED", "BLOCKED", operation=True)))
        self.assertIn("GOVERNANCE_AUTHORIZATION", self.stages(report))

    def test_environment_identity_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s2_report("IDENTITY_REQUIRED", "BLOCKED", operation=True)))
        self.assertIn("ENVIRONMENT_IDENTITY", self.stages(report))

    def test_rollback_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s2_report("ROLLBACK_NOT_PREPARED", "BLOCKED", operation=True)))
        self.assertIn("RECOVERY_ROLLBACK", self.stages(report))

    def test_lkg_compatibility_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s3_report("UPDATE_INCOMPATIBLE", "FAIL")))
        self.assertIn("COMPATIBILITY_LKG", self.stages(report))

    def test_staging_execution_fixture_is_classified(self):
        report = diag.run_diagnosis(self.request(self.s3_report("LOCAL_OPERATION_FAILED", "FAIL")))
        self.assertIn("STAGING_EXECUTION", self.stages(report))

    def test_missing_evidence_is_a_real_blocker_not_pass(self):
        source = self.s2_report("REQUEST_VALID", "PASS")
        report = diag.run_diagnosis(self.request(source))
        self.assertEqual(report["source_status"], "PASS")
        self.assertEqual(report["diagnostic_status"], "BLOCKED")
        self.assertEqual(report["evidence"]["missing_kinds"], ["git_ci"])
        self.assertEqual(report["evidence"]["completeness"], "INCOMPLETE")
        self.assertIn("EVIDENCE_MISSING", self.codes(report))

    def test_referenced_required_evidence_allows_pass_but_is_not_authenticated(self):
        source = self.s2_report("REQUEST_VALID", "PASS")
        report = diag.run_diagnosis(
            self.request(source, [{"kind": "git_ci", "state": "REFERENCED"}])
        )
        self.assertEqual(report["diagnostic_status"], "PASS")
        self.assertEqual(report["evidence"]["completeness"], "REFERENCED_COMPLETE")
        self.assertFalse(report["evidence"]["references_authenticated"])

    def test_existing_fail_is_not_hidden_by_missing_evidence(self):
        source = self.s2_report("BUNDLE_INCOMPLETE", "FAIL", operation=True)
        report = diag.run_diagnosis(self.request(source))
        self.assertEqual(report["diagnostic_status"], "FAIL")
        self.assertIn("artifact", report["evidence"]["missing_kinds"])

    def test_not_applicable_optional_evidence_stays_not_applicable(self):
        source = self.s2_report("REQUEST_VALID", "PASS")
        evidence = [
            {"kind": "git_ci", "state": "REFERENCED"},
            {"kind": "browser_runtime", "state": "NOT_APPLICABLE"},
        ]
        report = diag.run_diagnosis(self.request(source, evidence))
        self.assertEqual(report["diagnostic_status"], "PASS")
        self.assertIn("NOT_APPLICABLE", {event["status"] for event in report["events"]})
        self.assertIn("EVIDENCE_NOT_APPLICABLE", self.codes(report))

    def test_safe_log_distinguishes_all_four_statuses(self):
        reports = [
            diag.run_diagnosis(self.request(self.s2_report("REQUEST_FIELDS", "FAIL"))),
            diag.run_diagnosis(self.request(self.s2_report("AUTHORIZATION_REQUIRED", "BLOCKED", operation=True))),
            diag.run_diagnosis(
                self.request(
                    self.s2_report("REQUEST_VALID", "PASS"),
                    [
                        {"kind": "git_ci", "state": "REFERENCED"},
                        {"kind": "human", "state": "NOT_APPLICABLE"},
                    ],
                )
            ),
        ]
        rendered = "\n".join(line for report in reports for line in report["safe_log"])
        for status in ("PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"):
            self.assertIn(f"|{status}|", rendered)

    def test_secret_in_source_message_check_id_and_receipt_is_never_echoed(self):
        secret = "sk-proj-SUPER-SECRET-PII@example.com-/Volumes/private"
        source = self.s3_report(
            "REQUEST_VALID",
            "PASS",
            message=secret,
            check_id=secret,
            receipt={"unsafe_fixture": secret},
        )
        report = diag.run_diagnosis(
            self.request(source, [{"kind": "git_ci", "state": "REFERENCED"}])
        )
        rendered = json.dumps(report, ensure_ascii=False)
        self.assertNotIn(secret, rendered)
        self.assertNotIn("Volumes/private", rendered)

    def test_unknown_source_code_is_rejected_without_echo(self):
        secret_code = "SECRET_TOKEN_ABC123"
        source = self.s2_report(secret_code, "FAIL")
        report = diag.run_diagnosis(self.request(source))
        rendered = json.dumps(report, ensure_ascii=False)
        self.assertEqual(report["diagnostic_status"], "FAIL")
        self.assertIn("SOURCE_CODE_UNREGISTERED", self.codes(report))
        self.assertNotIn(secret_code, rendered)

    def test_source_overall_status_mismatch_is_rejected(self):
        source = self.s2_report("REQUEST_VALID", "PASS")
        source["overall_status"] = "FAIL"
        report = diag.run_diagnosis(self.request(source))
        self.assertIn("SOURCE_STATUS_MISMATCH", self.codes(report))

    def test_s2_operation_status_mismatch_is_rejected(self):
        source = self.s2_report("AUTHORIZATION_REQUIRED", "BLOCKED", operation=True)
        source["operations"][0]["status"] = "PASS"
        source["overall_status"] = "PASS"
        report = diag.run_diagnosis(self.request(source))
        self.assertIn("SOURCE_STATUS_MISMATCH", self.codes(report))

    def test_source_boundary_violation_is_rejected(self):
        source = self.s2_report("REQUEST_VALID", "PASS")
        source["network_access"] = True
        report = diag.run_diagnosis(self.request(source))
        self.assertIn("SOURCE_BOUNDARY_VIOLATION", self.codes(report))

    def test_s3_pass_without_receipt_is_rejected(self):
        source = self.s3_report("REQUEST_VALID", "PASS")
        source.pop("receipt")
        report = diag.run_diagnosis(self.request(source))
        self.assertIn("SOURCE_SHAPE_INVALID", self.codes(report))

    def test_s3_non_pass_with_success_receipt_is_rejected(self):
        source = self.s3_report("TREE_DIRTY", "FAIL", receipt={"forged": True})
        report = diag.run_diagnosis(self.request(source))
        self.assertIn("SOURCE_SHAPE_INVALID", self.codes(report))

    def test_bad_evidence_shape_kind_state_and_duplicate_fail_closed(self):
        source = self.s2_report("REQUEST_VALID", "PASS")
        cases = [
            ("EVIDENCE_TYPE", {"kind": "git_ci", "state": "REFERENCED"}),
            ("EVIDENCE_KIND", [{"kind": "secret_bucket", "state": "REFERENCED"}]),
            ("EVIDENCE_STATE", [{"kind": "git_ci", "state": "PASS"}]),
            (
                "EVIDENCE_DUPLICATE",
                [
                    {"kind": "git_ci", "state": "REFERENCED"},
                    {"kind": "git_ci", "state": "MISSING"},
                ],
            ),
        ]
        for expected, evidence in cases:
            with self.subTest(expected=expected):
                report = diag.run_diagnosis(self.request(source, evidence))
                self.assertIn(expected, self.codes(report))

    def test_same_request_produces_identical_diagnosis(self):
        request = self.request(
            self.s2_report("IDENTITY_REQUIRED", "BLOCKED", operation=True),
            [{"kind": "environment_identity", "state": "MISSING"}],
        )
        self.assertEqual(diag.run_diagnosis(request), diag.run_diagnosis(request))

    def test_every_failure_stage_has_fixture_or_mutant(self):
        exercised = {
            "INPUT_CONTRACT",
            "CANONICAL_CONTRACT",
            "ARTIFACT_INTEGRITY",
            "GIT_STATE",
            "PREFLIGHT_READINESS",
            "GOVERNANCE_AUTHORIZATION",
            "ENVIRONMENT_IDENTITY",
            "RECOVERY_ROLLBACK",
            "COMPATIBILITY_LKG",
            "STAGING_EXECUTION",
            "EVIDENCE_GAP",
        }
        self.assertEqual(set(diag.FAILURE_STAGES), exercised)

    def test_s4_tool_has_no_network_databricks_or_mutation_import(self):
        source = (ROOT / "tools/temas_v13_diagnostico.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertTrue(
            imports.isdisjoint(
                {"requests", "socket", "urllib", "httpx", "databricks", "subprocess", "shutil"}
            )
        )
        self.assertNotIn("DATABRICKS_TOKEN", source)
        self.assertNotIn("secrets.", source)

    def test_workflow_keeps_s1_s2_s3_history_and_runs_s4_read_only(self):
        workflow = (ROOT / ".github/workflows/temas-v13-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        for name in (
            "test_temas_v13_s1.py",
            "test_temas_v13_s2.py",
            "test_temas_v13_s3.py",
            "test_temas_v13_s4.py",
        ):
            self.assertIn(name, workflow)
        self.assertIn("V13_S4_NETWORK=0", workflow)
        self.assertIn("V13_S4_REMOTE_MUTATION=0", workflow)
        self.assertIn("V13_S4_DIAGNOSIS_READ_ONLY=1", workflow)
        self.assertIn("V13_S5_NOT_STARTED=1", workflow)
        historical = [line.strip() for line in workflow.splitlines() if "V13_S4_NOT_STARTED=1" in line]
        self.assertEqual(len(historical), 1)
        self.assertTrue(historical[0].startswith("# Historical S3 checkpoint assertion:"))
        self.assertNotIn("DATABRICKS_TOKEN", workflow)
        self.assertNotIn("secrets.", workflow)

    def test_s4_documentation_covers_all_plan_deliverables(self):
        text = (ROOT / "docs/sprints/sistema_temas/V13/S4_OBSERVABILIDADE_DIAGNOSTICO.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "Taxonomia de falhas",
            "Relatório sanitizado de execução",
            "Runbook de diagnóstico",
            "Checklist de evidência",
            "Logging sem PII/segredo",
        ):
            self.assertIn(heading, text)
        self.assertIn("A11-01", text)
        self.assertIn("S5", text)
        self.assertIn("não altera", text.lower())


if __name__ == "__main__":
    unittest.main()
