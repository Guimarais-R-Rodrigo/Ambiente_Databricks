#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import importlib.util, json, sys, unittest
import hashlib
import os
import subprocess
import tempfile
from unittest.mock import patch
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
class CreateObjectL2BoundaryTests(unittest.TestCase):
    """Fixtures próprias: nenhum alvo adversarial aponta ao produto real."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sef_create_l2_")
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name)
        self.root = self.area / ".assistant"
        self.root.mkdir()
        self.module = _load(
            "se07_create_boundary",
            ASSISTANT / "skills/hub-ml-criar-objeto/scripts/preflight.py",
        )
        self.root_patch = patch.object(self.module, "_resolve_assistant_root", return_value=self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        for rel in [*self.module.TEMPLATES.values(), *self.module.README_TEMPLATES.values()]:
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("synthetic template\n", encoding="utf-8")
        (self.root / "old").mkdir()
        (self.root / "old/source.py").write_text("# synthetic\n", encoding="utf-8")
        (self.root / "hub_scripts/same").mkdir(parents=True)
        (self.root / "hub_scripts/same/source.py").write_text("# same\n", encoding="utf-8")
        self.base = dict(operation="create", object_type="snippet", object_name="probe",
                         type_confirmed=True, existing_capability_checked=True,
                         existing_capability_status="not_found", snippet_section="testing")

    def snapshot(self):
        return {p.relative_to(self.area).as_posix():
                ("file", hashlib.sha256(p.read_bytes()).hexdigest()) if p.is_file()
                else ("link", os.readlink(p)) if p.is_symlink() or p.is_junction()
                else ("directory", None)
                for p in self.area.rglob("*")}

    def run_preflight(self, context):
        before = self.snapshot()
        result = self.module.preflight(context)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(result["writes_performed"])
        self.assertEqual([], result["tools_executed"])
        self.assertFalse(result["analytics_executed"])
        return result

    def assert_blocked(self, context, code=None):
        result = self.run_preflight(context)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertTrue(result["blocking_issues"])
        if code:
            self.assertIn(code, {i["code"] for i in result["blocking_issues"]})

    def conversion(self, **changes):
        return {**self.base, "operation": "convert", "object_type": "script",
                "source_relative": "old", "existing_capability_status": "found",
                "overlap_resolution": "convert_existing", **changes}

    def test_six_types_resolve_without_claiming_template_read(self):
        for kind in ("snippet", "script", "prompt", "readme", "notebook", "skill"):
            with self.subTest(kind=kind):
                result = self.run_preflight({**self.base, "object_type": kind,
                    "object_name": "hub-ml-probe" if kind == "skill" else "probe",
                    "readme_scale": "objeto",
                    "destination_relative": "new/README.md" if kind == "readme" else "new/probe.py"})
                self.assertEqual("PASS", result["status"], result)
                self.assertTrue(result["template"]["resolved"])
                self.assertEqual("NOT_OBSERVABLE", result["template"]["read_status"])

    def test_missing_template_is_blocked(self):
        (self.root / self.module.TEMPLATES["snippet"]).unlink()
        self.assert_blocked(self.base, "CANONICAL_TEMPLATE_NOT_FOUND")

    def test_authorized_section_is_still_one_safe_component(self):
        for section in ("../../outside", "..\\../outside", "../hub_scripts", "new/sub",
                        "new\\sub", "C:outside", "/outside", ".", "..", "new\x00section"):
            with self.subTest(section=section):
                self.assert_blocked({**self.base, "snippet_section": section,
                                     "new_snippet_section_authorized": True})
        result = self.run_preflight({**self.base, "snippet_section": "new_section",
                                    "new_snippet_section_authorized": True})
        self.assertEqual("PASS", result["status"])

    def test_unsafe_paths_are_rejected_before_filesystem_probe(self):
        for raw in ("../outside/probe.py", "..\\outside/probe.py", "C:probe.py",
                    "C:/probe.py", "//synthetic.invalid/share/probe.py",
                    "\\\\synthetic.invalid\\share\\probe.py", "new/\x00probe.py",
                    "new/probe:stream.py"):
            with self.subTest(raw=raw):
                self.assertIsNone(self.module._safe_relative(raw))
                with patch.object(Path, "exists", side_effect=AssertionError("unsafe path probed")):
                    self.assert_blocked({**self.base, "object_type": "notebook", "destination_relative": raw})
                    self.assert_blocked(self.conversion(source_relative=raw, object_type="invalid"))

    def make_link(self, link, target):
        link.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            process = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command",
                "New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") +
                "' -Target '" + str(target).replace("'", "''") + "' | Out-Null"],
                capture_output=True, timeout=15)
            if process.returncode:
                self.skipTest("junction indisponível sem ampliar privilégios: " + process.stderr.decode(errors="replace"))
            self.addCleanup(link.rmdir)
        else:
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest("symlink indisponível: " + str(exc))
            self.addCleanup(link.unlink)

    def test_link_escape_blocks_destination_source_and_template(self):
        outside = self.area / "outside"
        outside.mkdir()
        (outside / "template.md").write_text("synthetic outside\n", encoding="utf-8")
        self.make_link(self.root / "hub_snippets/linked", outside)
        self.assert_blocked({**self.base, "snippet_section": "linked", "new_snippet_section_authorized": True})
        self.assert_blocked(self.conversion(source_relative="hub_snippets/linked"))
        template_dir = self.root / "hub_padroes/snippet"
        (template_dir / "template.md").unlink()
        template_dir.rmdir()
        self.make_link(template_dir, outside)
        self.assert_blocked(self.base)

    def test_conversion_same_resolved_path_is_not_a_move(self):
        for source in ("hub_scripts/same", "hub_scripts/./same", "hub_scripts\\same"):
            with self.subTest(source=source):
                self.assert_blocked(self.conversion(source_relative=source, object_name="same"), "CONVERSION_MUST_MOVE")
        if os.name == "nt":
            self.assert_blocked(self.conversion(source_relative="HUB_SCRIPTS/SAME", object_name="same"), "CONVERSION_MUST_MOVE")
        self.make_link(self.root / "alias", self.root / "hub_scripts/same")
        self.assert_blocked(self.conversion(source_relative="alias", object_name="same"), "CONVERSION_MUST_MOVE")

    def test_conversion_accepts_existing_file_and_directory(self):
        for source in ("old", "old/source.py"):
            with self.subTest(source=source):
                result = self.run_preflight(self.conversion(source_relative=source))
                self.assertEqual("PASS", result["status"], result)
                self.assertTrue(result["source_exists"])
                self.assertTrue(result["conversion_behavior_preservation_required"])

    def test_conversion_hardlink_to_same_file_is_not_a_move(self):
        destination = self.root / "new/probe.py"
        destination.parent.mkdir()
        try:
            os.link(self.root / "old/source.py", destination)
        except OSError as exc:
            self.skipTest("hardlink indisponível: " + str(exc))
        self.assert_blocked(self.conversion(object_type="notebook",
            source_relative="old/source.py", destination_relative="new/probe.py"), "CONVERSION_MUST_MOVE")

    def test_invalid_api_root_has_structured_diagnostic(self):
        for value in (None, [], ["create"], "create", False, 1):
            with self.subTest(value=value):
                self.assert_blocked(value, "PREFLIGHT_INPUT_INVALID")

    def test_wrong_discriminant_types_have_structured_diagnostics(self):
        for field in ("operation", "object_type", "existing_capability_status", "overlap_resolution",
                      "readme_scale", "snippet_section", "object_name", "source_relative", "destination_relative"):
            for value in ([], {}, None, False, 1):
                with self.subTest(field=field, value=value):
                    seed = self.conversion() if field in ("source_relative", "overlap_resolution") else self.base
                    if field in ("readme_scale", "destination_relative"):
                        seed = {**self.base, "object_type": "readme", "readme_scale": "objeto", "destination_relative": "new/README.md"}
                    self.assert_blocked({**seed, field: value})

    def test_cli_invalid_json_and_root_exit_two_without_traceback(self):
        script = ASSISTANT / "skills/hub-ml-criar-objeto/scripts/preflight.py"
        for raw in ("{", "[]", '{"operation": []}'):
            with self.subTest(raw=raw):
                p = subprocess.run([sys.executable, "-B", str(script), "--context-json", raw],
                                   capture_output=True, text=True, encoding="utf-8", timeout=15,
                                   env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"})
                self.assertEqual(2, p.returncode, p.stderr)
                self.assertEqual("BLOCKED", json.loads(p.stdout)["status"])
                self.assertEqual("", p.stderr)

    def test_unexpected_internal_error_is_not_input_validation(self):
        with patch.object(self.module, "_resolve_assistant_root", side_effect=RuntimeError("synthetic implementation failure")):
            with self.assertRaisesRegex(RuntimeError, "implementation failure"):
                self.module.preflight(self.base)
            with patch.object(sys, "argv", ["preflight.py", "--context-json", json.dumps(self.base)]):
                with self.assertRaisesRegex(RuntimeError, "implementation failure"):
                    self.module.main()


if __name__=="__main__": unittest.main()
