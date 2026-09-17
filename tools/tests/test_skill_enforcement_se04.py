from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_fonte" / ".assistant"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))

from hub_scripts.skill_execution import receipt


SKILL = "hub-ml-eda-profissional"
ENTRYPOINT = "skills/hub-ml-eda-profissional/scripts/run.py::run"
PRIMITIVE = "quick_profile"


def canonical_payload(run_id: str = "run-1", result=None):
    if result is None:
        result = {"rows": 10, "columns": 4}
    trace = {
        "trace_version": "0.1",
        "run_id": run_id,
        "skill": SKILL,
        "entrypoint": ENTRYPOINT,
        "manifest": "release_manifest.json",
        "manifest_digest": "a" * 64,
        "contract_digest": "b" * 40,
        "runner_digest": "c" * 40,
        "input_digest": "d" * 64,
        "output_digest": receipt.sha256_digest(result),
        "preflight_status": "PASS",
        "context_provenance": {
            "numeric_columns": {
                "value": 3,
                "source": "runtime_derived",
                "evidence": "synthetic",
                "declared_value": None,
                "conflict": False,
            },
            "visual_diagnostics_requested": {
                "value": True,
                "source": "agent_declared",
                "evidence": "runner_input",
            },
        },
        "decisions": [
            {
                "item_id": "quick_profile",
                "item_type": "resource",
                "applicable": True,
                "resolved": True,
            },
            {
                "item_id": "roteiro_eda",
                "item_type": "template",
                "applicable": True,
                "resolved": True,
            },
        ],
        "resources_resolved": ["quick_profile", "data_quality_check"],
        "resources_called": ["quick_profile"],
        "resources_completed": ["quick_profile"],
        "fallback_used": False,
        "writes_performed": False,
        "blocking_issues": [],
        "status": "PASS",
    }
    execution_receipt = receipt.build_execution_receipt(
        trace,
        result,
        expected_skill=SKILL,
        expected_entrypoint=ENTRYPOINT,
        protected_primitive=PRIMITIVE,
    )
    assert execution_receipt is not None
    return {"trace": trace, "receipt": execution_receipt, "result": result}


def verify(payload, **kwargs):
    return receipt.verify_execution_receipt(
        payload,
        expected_skill=SKILL,
        expected_entrypoint=ENTRYPOINT,
        protected_primitive=PRIMITIVE,
        **kwargs,
    )


class ReceiptUnitTests(unittest.TestCase):
    def test_r01_valid_receipt(self):
        payload = canonical_payload()
        result = verify(
            payload,
            expected_run_id="run-1",
            expected_release={
                "manifest_sha256": "a" * 64,
                "contract_git_blob_sha1": "b" * 40,
                "runner_git_blob_sha1": "c" * 40,
            },
        )
        self.assertTrue(result.valid)
        self.assertEqual("VALID", result.status)
        self.assertEqual("PASS", result.canonical_compliance)

    def test_r02_manual_output_is_absent(self):
        result = verify({"result": {"rows": 10, "columns": 4}})
        self.assertEqual("ABSENT", result.status)
        self.assertFalse(result.valid)

    def test_r03_direct_helper_without_receipt_is_absent(self):
        result = verify({"trace": None, "result": {"ok": True}, "receipt": None})
        self.assertEqual("ABSENT", result.status)

    def test_r05_tampered_receipt_is_invalid(self):
        payload = canonical_payload()
        payload["receipt"]["fallback_used"] = True
        result = verify(payload)
        self.assertEqual("INVALID", result.status)
        self.assertIn("RECEIPT_ID_MISMATCH", result.issues)

    def test_r06_tampered_output_is_incompatible(self):
        payload = canonical_payload(result={"metric": 1})
        payload["result"] = {"metric": 999}
        self.assertEqual("INCOMPATIBLE", verify(payload).status)

    def test_r07_stale_receipt_is_rejected(self):
        payload = canonical_payload(run_id="old-run")
        self.assertEqual("STALE_REPLAYED", verify(payload, expected_run_id="new-run").status)

    def test_r08_wrong_skill_is_incompatible_even_with_recomputed_receipt_id(self):
        payload = canonical_payload()
        payload["trace"]["skill"] = "other-skill"
        body = dict(payload["receipt"])
        body.pop("receipt_id")
        body["skill"] = "other-skill"
        payload["receipt"] = {
            **body,
            "receipt_id": receipt.RECEIPT_ID_PREFIX + receipt.sha256_digest(body),
        }
        self.assertEqual("INCOMPATIBLE", verify(payload).status)

    def test_r09_wrong_current_release_is_incompatible(self):
        payload = canonical_payload()
        result = verify(payload, expected_release={"runner_git_blob_sha1": "f" * 40})
        self.assertEqual("INCOMPATIBLE", result.status)
        self.assertIn("CURRENT_RELEASE_MISMATCH:runner_git_blob_sha1", result.issues)

    def test_r10_provenance_conflict_refuses_emission(self):
        payload = canonical_payload()
        trace = copy.deepcopy(payload["trace"])
        trace["context_provenance"]["numeric_columns"]["conflict"] = True
        self.assertIsNone(
            receipt.build_execution_receipt(
                trace,
                payload["result"],
                expected_skill=SKILL,
                expected_entrypoint=ENTRYPOINT,
                protected_primitive=PRIMITIVE,
            )
        )

    def test_r11_release_integrity_failure_invalidates_current_receipt(self):
        payload = canonical_payload()
        result = verify(payload, release_integrity_ok=False)
        self.assertEqual("INCOMPATIBLE", result.status)
        self.assertIn("CURRENT_RELEASE_INTEGRITY_FAILED", result.issues)

    def test_r12_failed_primitive_or_fallback_refuses_emission(self):
        payload = canonical_payload()
        for mutation in ("failed", "fallback"):
            trace = copy.deepcopy(payload["trace"])
            if mutation == "failed":
                trace["status"] = "FAIL"
                trace["resources_completed"] = []
            else:
                trace["fallback_used"] = True
            with self.subTest(mutation=mutation):
                self.assertIsNone(
                    receipt.build_execution_receipt(
                        trace,
                        payload["result"],
                        expected_skill=SKILL,
                        expected_entrypoint=ENTRYPOINT,
                        protected_primitive=PRIMITIVE,
                    )
                )

    def test_r13_copied_receipt_does_not_bind_different_output(self):
        payload = canonical_payload(result={"metric": 1})
        copied = copy.deepcopy(payload["receipt"])
        other = canonical_payload(run_id="run-2", result={"metric": 2})
        other["receipt"] = copied
        self.assertEqual("INCOMPATIBLE", verify(other).status)

    def test_r14_partial_receipt_is_malformed(self):
        payload = canonical_payload()
        payload["receipt"].pop("bindings")
        self.assertEqual("MALFORMED", verify(payload).status)

        nested = canonical_payload()
        nested["receipt"]["release"].pop("runner_git_blob_sha1")
        self.assertEqual("MALFORMED", verify(nested).status)

    def test_r15_unknown_version_is_rejected(self):
        payload = canonical_payload()
        payload["receipt"]["receipt_version"] = "9.9"
        self.assertEqual("UNSUPPORTED_VERSION", verify(payload).status)

    def test_r16_trace_tamper_is_incompatible(self):
        payload = canonical_payload()
        payload["trace"]["resources_resolved"].append("unexpected")
        self.assertEqual("INCOMPATIBLE", verify(payload).status)

    def test_r17_old_release_receipt_rejected_against_current_release(self):
        payload = canonical_payload()
        result = verify(payload, expected_release={"manifest_sha256": "9" * 64})
        self.assertEqual("INCOMPATIBLE", result.status)

    def test_r18_json_order_does_not_change_digest_or_receipt(self):
        first = canonical_payload(result={"a": 1, "b": 2})
        second = canonical_payload(result={"b": 2, "a": 1})
        second["trace"]["run_id"] = first["trace"]["run_id"]
        second["receipt"] = receipt.build_execution_receipt(
            second["trace"],
            second["result"],
            expected_skill=SKILL,
            expected_entrypoint=ENTRYPOINT,
            protected_primitive=PRIMITIVE,
        )
        self.assertEqual(first["trace"]["output_digest"], second["trace"]["output_digest"])
        self.assertEqual(first["receipt"], second["receipt"])

    def test_r19_agent_declared_cannot_replace_runtime_provenance(self):
        payload = canonical_payload()
        trace = copy.deepcopy(payload["trace"])
        trace["context_provenance"]["numeric_columns"]["source"] = "agent_declared"
        self.assertIsNone(
            receipt.build_execution_receipt(
                trace,
                payload["result"],
                expected_skill=SKILL,
                expected_entrypoint=ENTRYPOINT,
                protected_primitive=PRIMITIVE,
            )
        )

    def test_receipt_does_not_copy_business_payload(self):
        payload = canonical_payload(result={"secret": "do-not-copy"})
        self.assertNotIn("secret", str(payload["receipt"]))
        self.assertNotIn("do-not-copy", str(payload["receipt"]))

    def test_import_and_template_consumption_are_not_fabricated(self):
        payload = canonical_payload()
        self.assertEqual(
            "NOT_OBSERVABLE",
            payload["receipt"]["resources"]["imported"]["status"],
        )
        self.assertEqual(
            "NOT_OBSERVABLE",
            payload["receipt"]["templates_consumed"]["status"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
