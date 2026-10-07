from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_databricks" / ".assistant"
SKILL = "hub-ml-eda-profissional"
SKILL_DIR = SOURCE_ASSISTANT / "skills" / SKILL
CONTRACT_PATH = SKILL_DIR / "execution_contract.json"
ENTRYPOINT = "skills/hub-ml-eda-profissional/scripts/run.py::run"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))

from hub_scripts.skill_execution.postflight import (  # noqa: E402
    build_postflight,
    sha256_digest,
    verify_postflight,
)
from hub_scripts.skill_execution.receipt import (  # noqa: E402
    build_execution_receipt,
    verify_execution_receipt,
)


HANDOFF = {
    "sources_snapshot": "catalog.schema.synthetic @ snapshot-test",
    "unit_keys_target": "1 linha por id; chave=id; target=N/A",
    "quality_risks": ["nenhum risco material no fixture sintético"],
    "feature_candidates_leakage": ["sem features candidatas no fixture"],
    "filters_sample": "sem filtros; amostra não requerida",
    "open_questions": [],
}


def _contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _decision(
    item_type: str,
    item_id: str,
    policy: str,
    applicable: bool,
    *,
    reason: str,
) -> dict:
    return {
        "item_type": item_type,
        "item_id": item_id,
        "policy": policy,
        "applicable": applicable,
        "resolved": True if applicable or policy == "optional" else None,
        "target": f"synthetic:{item_id}",
        "reason": reason,
        "condition": None,
    }


def _full_trace(*, numeric_columns: int = 3) -> dict:
    decisions = [
        _decision("resource", "quick_profile", "required", True, reason="requisito obrigatório"),
        _decision("resource", "data_quality_check", "required", True, reason="requisito obrigatório"),
        _decision("resource", "null_summary", "required", True, reason="requisito obrigatório"),
        _decision("resource", "smart_sample", "conditional", False, reason="local_sample_required=false"),
        _decision("resource", "safe_display", "conditional", False, reason="tabular_preview_required=false"),
        _decision(
            "resource",
            "correlation_matrix",
            "conditional",
            numeric_columns >= 2,
            reason=f"numeric_columns={numeric_columns}; limiar=2",
        ),
        _decision("resource", "distribution_grid", "conditional", False, reason="numeric_distributions_requested=false"),
        _decision("resource", "theme_plotly", "conditional", False, reason="resolved_theme_selected=false"),
        _decision("resource", "index_generator", "optional", False, reason="recurso opcional"),
        _decision("resource", "format_br", "optional", False, reason="recurso opcional"),
        _decision("template", "roteiro_eda", "required", True, reason="requisito obrigatório"),
        _decision("template", "matriz_graficos_eda", "conditional", False, reason="visual_diagnostics_requested=false"),
        _decision("template", "relatorio_executivo_eda", "required", True, reason="requisito obrigatório"),
        _decision("template", "estilo_visual_eda", "conditional", False, reason="visual_diagnostics_requested=false"),
    ]
    called = ["quick_profile", "data_quality_check", "null_summary"]
    if numeric_columns >= 2:
        called.append("correlation_matrix")
    artifacts = {
        "data_quality_check": {"status": "pass"},
        "null_summary": {"columns": 4},
        "correlation_matrix": {"strong_pairs": []},
    }
    return {
        "trace_version": "0.1",
        "run_id": "run-se05-test",
        "skill": SKILL,
        "entrypoint": ENTRYPOINT,
        "manifest": "release_manifest.json",
        "manifest_digest": "a" * 64,
        "contract_digest": "b" * 40,
        "runner_digest": "c" * 40,
        "input_digest": "d" * 64,
        "output_digest": None,
        "artifacts_digest": sha256_digest(artifacts),
        "preflight_status": "PASS",
        "context_provenance": {
            "numeric_columns": {
                "value": numeric_columns,
                "source": "runtime_derived",
                "evidence": "synthetic_schema",
                "conflict": False,
            }
        },
        "decisions": decisions,
        "resources_resolved": list(called),
        "resources_imported": list(called),
        "resources_called": list(called),
        "resources_completed": list(called),
        "templates_loaded": ["roteiro_eda", "relatorio_executivo_eda"],
        "template_digests": {
            "roteiro_eda": "e" * 64,
            "relatorio_executivo_eda": "f" * 64,
        },
        "fallback_used": False,
        "writes_performed": False,
        "blocking_issues": [],
        "status": "PASS",
    }


def _payload(trace: dict | None = None, *, result=None, artifacts=None) -> dict:
    trace = copy.deepcopy(trace if trace is not None else _full_trace())
    result = {"profile": "ok"} if result is None else result
    artifacts = (
        {
            "data_quality_check": {"status": "pass"},
            "null_summary": {"columns": 4},
            "correlation_matrix": {"strong_pairs": []},
        }
        if artifacts is None
        else artifacts
    )
    trace["output_digest"] = sha256_digest(result)
    trace["artifacts_digest"] = sha256_digest(artifacts)
    receipt = build_execution_receipt(
        trace,
        result,
        expected_skill=SKILL,
        expected_entrypoint=ENTRYPOINT,
        protected_primitive="quick_profile",
    )
    return {"trace": trace, "receipt": receipt, "result": result, "artifacts": artifacts}


def _receipt_verification(payload: dict, *, expected_run_id: str | None = None) -> dict:
    return verify_execution_receipt(
        payload,
        expected_skill=SKILL,
        expected_entrypoint=ENTRYPOINT,
        protected_primitive="quick_profile",
        expected_run_id=expected_run_id,
    ).to_dict()


class SkillEnforcementSE05Tests(unittest.TestCase):
    def test_p01_full_evidence_and_handoff_pass(self):
        payload = _payload()
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("PASS", postflight["status"])
        self.assertTrue(postflight["completion_authorized"])
        self.assertEqual([], postflight["issues"])
        self.assertTrue(postflight["postflight_id"].startswith("pf1:"))

    def test_p02_manual_output_without_receipt_is_blocked(self):
        payload = {"result": {"profile": "manual"}, "artifacts": {}}
        verification = _receipt_verification(payload)
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=verification,
            handoff=HANDOFF,
        )
        self.assertEqual("BLOCKED", postflight["status"])
        self.assertFalse(postflight["completion_authorized"])
        self.assertTrue(any(issue["code"] == "RECEIPT_NOT_VALID" for issue in postflight["issues"]))

    def test_p03_missing_required_resource_fails(self):
        trace = _full_trace()
        for key in ("resources_imported", "resources_called", "resources_completed"):
            trace[key].remove("data_quality_check")
        payload = _payload(trace)
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("FAIL", postflight["status"])
        self.assertFalse(postflight["completion_authorized"])
        self.assertTrue(any(issue["code"] == "REQUIRED_RESOURCE_NOT_CALLED" for issue in postflight["issues"]))

    def test_p04_applicable_conditional_missing_fails(self):
        trace = _full_trace(numeric_columns=3)
        for key in ("resources_imported", "resources_called", "resources_completed"):
            trace[key].remove("correlation_matrix")
        payload = _payload(trace)
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("FAIL", postflight["status"])
        self.assertTrue(any(issue["item_id"] == "correlation_matrix" for issue in postflight["issues"]))

    def test_p05_conditional_skip_requires_reason(self):
        trace = _full_trace(numeric_columns=1)
        decision = next(item for item in trace["decisions"] if item["item_id"] == "correlation_matrix")
        decision["reason"] = ""
        payload = _payload(trace, artifacts={
            "data_quality_check": {"status": "pass"},
            "null_summary": {"columns": 4},
        })
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("REVIEW", postflight["status"])
        self.assertTrue(any(issue["code"] == "CONDITIONAL_SKIP_UNJUSTIFIED" for issue in postflight["issues"]))

    def test_p06_missing_required_template_fails(self):
        trace = _full_trace()
        trace["templates_loaded"].remove("relatorio_executivo_eda")
        trace["template_digests"].pop("relatorio_executivo_eda")
        payload = _payload(trace)
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("FAIL", postflight["status"])
        self.assertTrue(any(issue["code"] == "REQUIRED_TEMPLATE_NOT_LOADED" for issue in postflight["issues"]))

    def test_p07_incomplete_handoff_requires_review(self):
        payload = _payload()
        handoff = dict(HANDOFF)
        handoff.pop("quality_risks")
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=handoff,
        )
        self.assertEqual("REVIEW", postflight["status"])
        self.assertFalse(postflight["completion_authorized"])
        self.assertTrue(any(issue["code"] == "HANDOFF_FIELD_MISSING" for issue in postflight["issues"]))

    def test_p08_open_questions_may_be_explicitly_empty(self):
        payload = _payload()
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=dict(HANDOFF, open_questions=[]),
        )
        self.assertEqual("PASS", postflight["status"])

    def test_p09_artifact_tamper_is_blocked(self):
        payload = _payload()
        payload["artifacts"]["data_quality_check"] = {"status": "tampered"}
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("BLOCKED", postflight["status"])
        self.assertTrue(any(issue["code"] == "ARTIFACTS_DIGEST_MISMATCH" for issue in postflight["issues"]))

    def test_p10_stale_receipt_is_blocked(self):
        payload = _payload()
        verification = _receipt_verification(payload, expected_run_id="different-run")
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=verification,
            handoff=HANDOFF,
        )
        self.assertEqual("BLOCKED", postflight["status"])
        self.assertTrue(any(issue["code"] == "RECEIPT_NOT_VALID" for issue in postflight["issues"]))

    def test_p11_optional_resources_do_not_block(self):
        payload = _payload()
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertNotIn("resource:index_generator", postflight["coverage"]["checked_required"])
        self.assertNotIn("resource:format_br", postflight["coverage"]["checked_required"])
        self.assertEqual("PASS", postflight["status"])

    def test_p12_current_se04_style_receipt_cannot_claim_full_completion(self):
        trace = _full_trace()
        trace["resources_imported"] = ["quick_profile"]
        trace["resources_called"] = ["quick_profile"]
        trace["resources_completed"] = ["quick_profile"]
        trace["templates_loaded"] = []
        trace["template_digests"] = {}
        payload = _payload(trace, artifacts={})
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("FAIL", postflight["status"])
        self.assertFalse(postflight["completion_authorized"])

    def test_p13_postflight_tamper_is_invalid(self):
        payload = _payload()
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        final_payload = dict(payload, handoff=HANDOFF, postflight=postflight)
        final_payload["postflight"]["completion_authorized"] = False
        verification = verify_postflight(
            final_payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
        )
        self.assertEqual("INVALID", verification.status)
        self.assertFalse(verification.valid)

    def test_p14_valid_postflight_reverifies(self):
        payload = _payload()
        postflight = build_postflight(
            payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        final_payload = dict(payload, handoff=HANDOFF, postflight=postflight)
        verification = verify_postflight(
            final_payload,
            contract=_contract(),
            receipt_verification=_receipt_verification(payload),
        )
        self.assertEqual("VALID", verification.status)
        self.assertTrue(verification.valid)
        self.assertTrue(verification.completion_authorized)

    def test_p15_missing_postflight_config_is_blocked(self):
        payload = _payload()
        contract = _contract()
        contract["metadata"].pop("postflight")
        postflight = build_postflight(
            payload,
            contract=contract,
            receipt_verification=_receipt_verification(payload),
            handoff=HANDOFF,
        )
        self.assertEqual("BLOCKED", postflight["status"])
        self.assertTrue(any(issue["code"] == "POSTFLIGHT_CONFIG_MISSING" for issue in postflight["issues"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
