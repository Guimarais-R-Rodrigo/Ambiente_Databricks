#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ASSISTANT=ROOT/"ambiente_fonte"/".assistant"
POLICY=ASSISTANT/"hub_padroes"/"skill_enforcement"/"policy.json"

def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module); return module

class SE07PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool=_load("se07_policy_test_tool",ROOT/"tools"/"skill_enforcement"/"se07_policy.py")
        cls.runtime=_load("se07_runtime_policy",ASSISTANT/"hub_scripts"/"skill_execution"/"skill_execution.py")
        cls.raw=json.loads(POLICY.read_text(encoding="utf-8")); cls.by={i["skill"]:i for i in cls.raw["skills"]}
    def test_registry_validates_and_covers_catalog(self):
        self.assertEqual([],self.tool.validate_policy_registry(POLICY)); self.assertEqual(14,len(self.tool.discover_skills())); self.assertEqual(self.tool.discover_skills(),set(self.by))
    def test_current_level_is_evidence_based(self):
        expected_current = {
            "hub-ml-eda-profissional": "L4",
            "hub-ml-comentar-notebook": "L1",
            "hub-ml-concierge": "L1",
            "hub-ml-auditoria-skills": "L3",
            "hub-ml-criar-objeto": "L2",
        }
        for skill, policy in self.by.items():
            self.assertEqual(expected_current.get(skill, "L0"), policy["current_level"], skill)

    def test_l1_contracts_are_static_and_proportional(self):
        expected = {
            "hub-ml-comentar-notebook": {
                "preserve_existing_code_cells",
                "documentation_changes_only_around_existing_code",
                "do_not_claim_current_execution_without_validated_outputs",
            },
            "hub-ml-concierge": {
                "discovery_and_routing_only",
                "do_not_execute_final_specialist_analysis",
                "do_not_invent_target_key_threshold_budget_policy_or_authorization",
                "handoff_does_not_expand_authority",
            },
        }
        for skill, invariants in expected.items():
            contract = json.loads(
                (ASSISTANT/"skills"/skill/"execution_contract.json").read_text(encoding="utf-8")
            )
            meta = contract["metadata"]["se07"]
            self.assertEqual("L1", meta["enforcement_level"])
            self.assertEqual("whole_skill", meta["scope"])
            self.assertFalse(meta["runtime_gate"])
            self.assertEqual(invariants, set(meta["static_invariants"]))
            self.assertEqual([], contract["resources"])
            self.assertTrue(contract["templates"])
            self.assertTrue(all(item["policy"] == "optional" for item in contract["templates"]))
            self.assertTrue(all(item["evidence"] == "loaded" for item in contract["templates"]))
    def test_target_classification(self):
        expected={"hub-ml-analise-safra":"L3","hub-ml-auditoria-skills":"L3","hub-ml-baseline-ml":"L4","hub-ml-comentar-notebook":"L1","hub-ml-concierge":"L1","hub-ml-criar-objeto":"L3","hub-ml-cross-eda-ml":"L4","hub-ml-eda-profissional":"L4","hub-ml-explainability":"L3","hub-ml-feature-engineering":"L4","hub-ml-monitoramento-modelo":"L4","hub-ml-pipeline-builder":"L4","hub-ml-tutor-databricks":"L0","hub-ml-validacao-estatistica":"L3"}
        self.assertEqual(expected,{k:v["target_level"] for k,v in self.by.items()})
    def test_audit_debt_and_ladder(self):
        self.assertEqual({"AUDIT_FALSE_REASSURANCE","AUDIT_STATE_LADDER","AUDIT_CONDITIONAL_APPLICABILITY"},set(self.by["hub-ml-auditoria-skills"]["known_debt"]))
        text=(ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"SKILL.md").read_text(encoding="utf-8")
        for token in ("citado","localizado","lido","importado","chamado","concluído","NOT_OBSERVABLE","get_skill_enforcement_policy","verify_finalized"): self.assertIn(token,text)
    def test_criar_objeto_l2_preflight_contract_and_runtime(self):
        skill_dir = ASSISTANT/"skills"/"hub-ml-criar-objeto"
        contract = json.loads((skill_dir/"execution_contract.json").read_text(encoding="utf-8"))
        meta = contract["metadata"]["se07"]
        self.assertEqual("L2", meta["enforcement_level"])
        self.assertEqual("L3", meta["target_level"])
        self.assertTrue(meta["runtime_gate"])

        preflight = _load(
            "se07_create_object_preflight",
            skill_dir/"scripts"/"preflight.py",
        )

        happy = preflight.preflight({
            "operation": "create",
            "object_type": "snippet",
            "object_name": "sef_probe_snippet",
            "type_confirmed": True,
            "existing_capability_checked": True,
            "existing_capability_status": "not_found",
            "snippet_section": "testing",
        })
        self.assertEqual("PASS", happy["status"])
        self.assertEqual(
            "hub_padroes/snippet/template.md",
            happy["template"]["path"],
        )
        self.assertTrue(happy["template"]["resolved"])
        self.assertEqual("NOT_OBSERVABLE", happy["template"]["read_status"])
        self.assertEqual(
            "hub_snippets/testing/sef_probe_snippet",
            happy["destination_relative"],
        )
        self.assertFalse(happy["writes_performed"])
        self.assertEqual([], happy["tools_executed"])
        self.assertFalse(happy["analytics_executed"])

    def test_criar_objeto_l2_blocks_ambiguous_or_unsupported_routes(self):
        preflight = _load(
            "se07_create_object_preflight_negative",
            ASSISTANT/"skills"/"hub-ml-criar-objeto"/"scripts"/"preflight.py",
        )

        bad_type = preflight.preflight({
            "operation": "create",
            "object_type": "auditoria",
            "object_name": "x",
            "type_confirmed": True,
            "existing_capability_checked": True,
            "existing_capability_status": "not_found",
        })
        self.assertEqual("BLOCKED", bad_type["status"])
        self.assertIn(
            "OBJECT_TYPE_INVALID",
            {item["code"] for item in bad_type["blocking_issues"]},
        )

        new_section = preflight.preflight({
            "operation": "create",
            "object_type": "snippet",
            "object_name": "sef_probe_snippet",
            "type_confirmed": True,
            "existing_capability_checked": True,
            "existing_capability_status": "not_found",
            "snippet_section": "nova_secao",
        })
        self.assertEqual("BLOCKED", new_section["status"])
        self.assertIn(
            "NEW_SNIPPET_SECTION_REQUIRES_DECISION",
            {item["code"] for item in new_section["blocking_issues"]},
        )

        overlap = preflight.preflight({
            "operation": "create",
            "object_type": "script",
            "object_name": "sef_probe_script",
            "type_confirmed": True,
            "existing_capability_checked": True,
            "existing_capability_status": "found",
            "overlap_resolution": "extend_existing",
        })
        self.assertEqual("BLOCKED", overlap["status"])
        self.assertIn(
            "NEW_OBJECT_NOT_AUTHORIZED_BY_OVERLAP_DECISION",
            {item["code"] for item in overlap["blocking_issues"]},
        )

    def test_criar_objeto_l2_readme_and_conversion_guards(self):
        preflight = _load(
            "se07_create_object_preflight_readme",
            ASSISTANT/"skills"/"hub-ml-criar-objeto"/"scripts"/"preflight.py",
        )

        readme = preflight.preflight({
            "operation": "create",
            "object_type": "readme",
            "object_name": "guia_sef",
            "type_confirmed": True,
            "existing_capability_checked": True,
            "existing_capability_status": "not_found",
            "readme_scale": "objeto",
            "destination_relative": "hub_scripts/sef_probe/README.md",
        })
        self.assertEqual("PASS", readme["status"])
        self.assertEqual(
            "hub_padroes/readme/template_objeto.md",
            readme["template"]["path"],
        )

        conversion = preflight.preflight({
            "operation": "convert",
            "object_type": "script",
            "object_name": "sef_probe_script",
            "type_confirmed": True,
            "existing_capability_checked": True,
            "existing_capability_status": "found",
            "overlap_resolution": "convert_existing",
            "source_relative": "hub_scripts/quick_profile",
        })
        self.assertEqual("PASS", conversion["status"])
        self.assertTrue(conversion["source_exists"])
        self.assertTrue(conversion["conversion_behavior_preservation_required"])

    def test_audit_l2_preflight_contract_and_runtime(self):
        skill_dir = ASSISTANT/"skills"/"hub-ml-auditoria-skills"
        contract = json.loads((skill_dir/"execution_contract.json").read_text(encoding="utf-8"))
        meta = contract["metadata"]["se07"]
        self.assertEqual("L3", meta["enforcement_level"])
        self.assertEqual("L3", meta["target_level"])
        self.assertTrue(meta["runtime_gate"])
        preflight = _load("se07_audit_preflight", skill_dir/"scripts"/"preflight.py")

        happy = preflight.preflight({
            "audit_mode": "OUTPUT",
            "producer_skill": "hub-ml-eda-profissional",
            "original_request_present": True,
            "artifact_present": True,
        })
        self.assertEqual("PASS", happy["status"])
        self.assertEqual("L4", happy["producer_policy"]["current_level"])
        self.assertFalse(happy["writes_performed"])
        self.assertFalse(happy["analytics_executed"])
        self.assertFalse(happy["verifier_executed"])

        blocked = preflight.preflight({
            "audit_mode": "OUTPUT",
            "producer_skill": "hub-ml-eda-profissional",
            "original_request_present": False,
            "artifact_present": True,
        })
        self.assertEqual("BLOCKED", blocked["status"])
        self.assertIn(
            "ORIGINAL_REQUEST_REQUIRED",
            {item["code"] for item in blocked["blocking_issues"]},
        )

        implementation = preflight.preflight({
            "audit_mode": "IMPLEMENTAÇÃO",
            "target_skills": ["hub-ml-criar-objeto"],
        })
        self.assertEqual("PASS", implementation["status"])
        self.assertEqual(["hub-ml-criar-objeto"], implementation["target_skills"])

    def test_audit_l2_unknown_or_missing_inputs_fail_closed(self):
        preflight = _load(
            "se07_audit_preflight_negative",
            ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"scripts"/"preflight.py",
        )
        unknown_mode = preflight.preflight({"audit_mode": "QUALQUER"})
        self.assertEqual("BLOCKED", unknown_mode["status"])
        self.assertIn(
            "AUDIT_MODE_INVALID",
            {item["code"] for item in unknown_mode["blocking_issues"]},
        )
        missing_target = preflight.preflight({
            "audit_mode": "IMPLEMENTACAO",
            "target_skills": [],
        })
        self.assertEqual("BLOCKED", missing_target["status"])
        self.assertIn(
            "TARGET_SKILLS_REQUIRED",
            {item["code"] for item in missing_target["blocking_issues"]},
        )

    def _audit_l3_evidence(self):
        return {
            "state_ladder": {
                "execution_receipt": {
                    "citado": True,
                    "localizado": True,
                    "lido": None,
                    "importado": None,
                    "chamado": None,
                    "concluido": None,
                }
            },
            "conditional_applicability": {
                "smart_sample": None,
            },
            "persisted_mechanical_state": {
                "postflight.status": "PASS",
                "completion.authorized": True,
            },
        }

    def test_audit_l3_runner_persisted_pass_remains_not_reverified(self):
        runner = _load(
            "se07_audit_l3_runner_not_reverified",
            ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"scripts"/"run.py",
        )
        payload = runner.run(
            {
                "audit_mode": "OUTPUT",
                "producer_skill": "hub-ml-eda-profissional",
                "original_request_present": True,
                "artifact_present": True,
            },
            self._audit_l3_evidence(),
            assistant_root=ASSISTANT,
        )
        self.assertEqual("PASS", payload["trace"]["status"])
        self.assertIsInstance(payload["receipt"], dict)
        self.assertEqual(
            "NOT_REVERIFIED",
            payload["result"]["producer_canonical_compliance"],
        )
        self.assertFalse(payload["result"]["producer_verification"]["executed"])
        self.assertEqual(
            "NOT_OBSERVABLE",
            payload["result"]["state_ladder"]["execution_receipt"]["lido"],
        )
        self.assertEqual(
            "NOT_OBSERVABLE",
            payload["result"]["conditional_applicability"]["smart_sample"],
        )
        verification = runner.verify_receipt(payload, assistant_root=ASSISTANT)
        self.assertEqual("VALID", verification["status"])
        self.assertTrue(verification["valid"])

    def test_audit_l3_runner_calls_real_eda_verifier(self):
        runner = _load(
            "se07_audit_l3_runner_real_verifier",
            ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"scripts"/"run.py",
        )
        payload = runner.run(
            {
                "audit_mode": "OUTPUT",
                "producer_skill": "hub-ml-eda-profissional",
                "original_request_present": True,
                "artifact_present": True,
            },
            self._audit_l3_evidence(),
            producer_final_payload={},
            assistant_root=ASSISTANT,
        )
        observed = payload["result"]["producer_verification"]
        self.assertTrue(observed["executed"])
        self.assertIn("verify_finalized", observed["verifier_name"])
        self.assertNotEqual("NOT_RUN", observed["status"])
        self.assertEqual(
            "NOT_PASS_REVERIFIED",
            payload["result"]["producer_canonical_compliance"],
        )

    def test_audit_l3_runner_reverifies_valid_synthetic_eda(self):
        se05 = _load(
            "se07_se05_fixture",
            ROOT/"tools"/"tests"/"test_skill_enforcement_se05_runner.py",
        )
        fixture = se05.SkillEnforcementSE05RunnerTests()
        producer = fixture._run_enforced()
        finalized = se05.finalizer.finalize(
            producer,
            se05.HANDOFF,
            assistant_root=ASSISTANT,
        )

        runner = _load(
            "se07_audit_l3_runner_valid_verifier",
            ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"scripts"/"run.py",
        )
        payload = runner.run(
            {
                "audit_mode": "OUTPUT",
                "producer_skill": "hub-ml-eda-profissional",
                "original_request_present": True,
                "artifact_present": True,
            },
            self._audit_l3_evidence(),
            producer_final_payload=finalized,
            assistant_root=ASSISTANT,
        )
        self.assertEqual(
            "PASS_REVERIFIED",
            payload["result"]["producer_canonical_compliance"],
        )
        self.assertTrue(payload["result"]["producer_verification"]["executed"])
        self.assertTrue(payload["result"]["producer_verification"]["valid"])
        self.assertTrue(payload["result"]["producer_verification"]["completion_authorized"])

    def test_audit_l3_runner_blocks_invalid_ladder(self):
        runner = _load(
            "se07_audit_l3_runner_invalid_ladder",
            ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"scripts"/"run.py",
        )
        evidence = self._audit_l3_evidence()
        evidence["state_ladder"]["execution_receipt"].pop("lido")
        payload = runner.run(
            {
                "audit_mode": "OUTPUT",
                "producer_skill": "hub-ml-eda-profissional",
                "original_request_present": True,
                "artifact_present": True,
            },
            evidence,
            assistant_root=ASSISTANT,
        )
        self.assertIsNone(payload["receipt"])
        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertIn(
            "STATE_LADDER_INCOMPLETE",
            {item["code"] for item in payload["trace"]["blocking_issues"]},
        )

    def test_audit_l3_receipt_detects_tamper(self):
        runner = _load(
            "se07_audit_l3_runner_tamper",
            ASSISTANT/"skills"/"hub-ml-auditoria-skills"/"scripts"/"run.py",
        )
        payload = runner.run(
            {
                "audit_mode": "OUTPUT",
                "producer_skill": "hub-ml-eda-profissional",
                "original_request_present": True,
                "artifact_present": True,
            },
            self._audit_l3_evidence(),
            assistant_root=ASSISTANT,
        )
        payload["result"]["persisted_mechanical_state"]["postflight.status"] = "FAIL"
        verification = runner.verify_receipt(payload, assistant_root=ASSISTANT)
        self.assertFalse(verification["valid"])
        self.assertIn(verification["status"], {"INCOMPATIBLE", "INVALID"})

    def test_pipeline_authorization(self):
        self.assertIn("authorization",{x["evidence"] for x in self.by["hub-ml-pipeline-builder"]["protected_surfaces"]})
    def test_tutor_remains_l0(self):
        p=self.by["hub-ml-tutor-databricks"]; self.assertEqual(("L0","L0","guidance"),(p["current_level"],p["target_level"],p["rollout_mode"]))
    def test_runtime_resolver(self):
        p=self.runtime.get_skill_enforcement_policy("hub-ml-auditoria-skills",assistant_root=ASSISTANT); self.assertEqual(("L3","L3"),(p.current_level,p.target_level)); self.assertIn("AUDIT_FALSE_REASSURANCE",p.known_debt)
        c=self.runtime.get_skill_enforcement_policy("hub-ml-criar-objeto",assistant_root=ASSISTANT); self.assertEqual(("L2","L3"),(c.current_level,c.target_level))
    def test_unknown_fails_closed(self):
        with self.assertRaises(self.runtime.EnforcementPolicyError): self.runtime.get_skill_enforcement_policy("hub-ml-nao-existe",assistant_root=ASSISTANT)
if __name__=="__main__": unittest.main()
