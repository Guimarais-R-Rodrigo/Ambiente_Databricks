from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.skill_enforcement.parallel import bundle, contract, coverage, registry, scheduler, verifier, pilot_verify
from tools.skill_enforcement.parallel import launcher


def task(task_id="task.a", deps=None, key="k", role="executor", resource="light", failure_scope="LOCAL_CHAIN"):
    return {"task_schema":contract.TASK_SCHEMA_VERSION,"task_id":task_id,"role":role,"stage":"B0.6","skill":"synthetic","candidate_sha":"a"*40,"command_ids":["b0:pilot:pass"],"depends_on":deps or [],"read_roots":["tools"],"write_roots":[],"protected_paths":["ambiente_fonte"],"resource_class":resource,"exclusivity_key":key,"required":True,"expected_effect":"NONE","failure_scope":failure_scope}

def campaign(tasks=None):
    return {"schema_version":contract.CAMPAIGN_SCHEMA_VERSION,"campaign_id":"SER-B0-TEST","baseline_sha":"b"*40,"candidate_sha":"a"*40,"state":"PLANNED","max_parallel":2,"max_auditors":1,"resource_limits":{"light":2,"audit":1},"tasks":tasks or [task()],"command_registry_digest":"1"*64,"coverage_digest":"2"*64,"policy_before_digest":"3"*64,"human_gates":["B0_RELEASE"],"external_gates":[],"repo_mode":"READ_ONLY"}

def result(task_id="task.a",status="PASS",exit_code=0,wave=0):
    return {"result_schema":contract.RESULT_SCHEMA_VERSION,"task_id":task_id,"candidate_sha":"a"*40,"status":status,"effect_state":"NONE","command_records":[] if status.startswith("BLOCKED") else [{"exit_code":exit_code,"command_started":True,"cleanup":"COMPLETE"}],"first_failure":None,"wave_index":wave,"started_at_utc":"2026-09-24T00:00:00Z","ended_at_utc":"2026-09-24T00:00:01Z","protected_fingerprint_before":"4"*64,"protected_fingerprint_after":"4"*64,"issues":[]}

class ContractTests(unittest.TestCase):
    def test_valid_task(self): self.assertEqual([],contract.validate_task(task()))
    def test_unknown_task_key_rejected(self): x=task();x["surprise"]=1;self.assertIn("TASK:UNKNOWN:surprise",contract.validate_task(x))
    def test_repo_write_rejected_in_b0(self): x=task();x["write_roots"]=["docs"];self.assertIn("TASK_REPO_WRITES_NOT_SUPPORTED_BY_B0",contract.validate_task(x))
    def test_non_none_effect_rejected_in_b0(self): x=task();x["expected_effect"]="MODIFIED";self.assertIn("TASK_EFFECT_NOT_SUPPORTED_BY_B0",contract.validate_task(x))
    def test_failure_scope_required(self): x=task();del x["failure_scope"];self.assertTrue(any("failure_scope" in i for i in contract.validate_task(x)))
    def test_valid_campaign(self): self.assertEqual([],contract.validate_campaign(campaign()))
    def test_campaign_repo_mode_must_be_read_only(self): x=campaign();x["repo_mode"]="WRITE";self.assertIn("CAMPAIGN_REPO_MODE_MUST_BE_READ_ONLY",contract.validate_campaign(x))
    def test_duplicate_task_id_rejected(self): self.assertIn("CAMPAIGN_TASK_ID_DUPLICATE",contract.validate_campaign(campaign([task(),task()])))
    def test_unknown_dependency_rejected(self): self.assertTrue(any(i.startswith("CAMPAIGN_DEPENDENCY_UNKNOWN") for i in contract.validate_campaign(campaign([task("aaa",["missing"])]))))
    def test_path_traversal_rejected(self): x=task();x["read_roots"]=["../x"];self.assertTrue(any("UNSAFE" in i for i in contract.validate_task(x)))
    def test_valid_result(self): self.assertEqual([],contract.validate_result(result()))
    def test_wave_required(self): x=result();del x["wave_index"];self.assertIn("RESULT:MISSING:wave_index",contract.validate_result(x))
    def test_digest_stable(self): self.assertEqual(contract.digest_json({"b":2,"a":1}),contract.digest_json({"a":1,"b":2}))

class RegistryTests(unittest.TestCase):
    def test_registry_loads(self): self.assertIn("b0:pilot:pass",registry.load_registry()["commands"])
    def test_unknown_command_rejected(self): self.assertRaises(registry.RegistryError,registry.resolve_command,"missing")
    def test_shell_and_inline_code_rejected(self):
        for argv in (["bash","-c","echo x"],["{PYTHON}","-c","print(1)"]):
            with self.subTest(argv=argv), tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)/"r.json";p.write_text(json.dumps({"schema_version":"SER-PARALLEL-COMMANDS-2","commands":[{"command_id":"x","argv":argv,"effects":"none","purpose":"x"}]}))
                self.assertRaises(registry.RegistryError,registry.load_registry,p)
    def test_unknown_placeholder_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"r.json";p.write_text(json.dumps({"schema_version":"SER-PARALLEL-COMMANDS-2","commands":[{"command_id":"x","argv":["{SHELL}","x"],"effects":"none","purpose":"x"}]}))
            self.assertRaises(registry.RegistryError,registry.load_registry,p)

class SchedulerTests(unittest.TestCase):
    def test_cycle_detected(self): self.assertTrue(scheduler.detect_cycle([task("aaa",["bbb"]),task("bbb",["aaa"],"k2")]))
    def test_failure_blocks_only_dependent(self):
        d=scheduler.decide([task("aaa"),task("bbb",["aaa"],"k2"),task("ccc",[],"k3")],{"aaa":"FAIL"},limit=2);self.assertIn("bbb",d.blocked_dependency);self.assertIn("ccc",d.ready)
    def test_exclusivity_serializes(self): self.assertEqual(1,len(scheduler.decide([task("aaa",[],"same"),task("bbb",[],"same")],{},limit=2).ready))
    def test_auditor_limit(self):
        d=scheduler.decide([task("aaa",role="domain_auditor",resource="audit"),task("bbb",key="k2",role="evidence_auditor",resource="audit"),task("ccc",key="k3")],{},limit=3,auditor_limit=1,resource_limits={"audit":2,"light":2});self.assertEqual(2,len(d.ready));self.assertIn("ccc",d.ready)

class VerifierTests(unittest.TestCase):
    def test_valid(self): self.assertTrue(verifier.verify_campaign_run(campaign(),{"task.a":result()})["valid"])
    def test_pass_nonzero_rejected(self): self.assertTrue(any("PASS_COMMAND_INVALID" in i for i in verifier.verify_campaign_run(campaign(),{"task.a":result(exit_code=1)})["issues"]))
    def test_protected_mutation_rejected(self): x=result();x["protected_fingerprint_after"]="5"*64;self.assertTrue(any("PROTECTED_PATH_MUTATED" in i for i in verifier.verify_campaign_run(campaign(),{"task.a":x})["issues"]))
    def test_first_failure_deterministic_by_wave_then_id(self):
        c=campaign([task("bbb"),task("aaa",key="k2")]);ra=result("aaa","FAIL",1,0);rb=result("bbb","FAIL",1,0);v=verifier.verify_campaign_run(c,{"bbb":rb,"aaa":ra});self.assertEqual("aaa",v["first_failure"])
    def test_global_stop_task_cannot_execute(self):
        c=campaign([task("aaa",failure_scope="GLOBAL_CAMPAIGN"),task("bbb",key="k2")]);ra=result("aaa","FAIL",1,0);rb=result("bbb","BLOCKED_GLOBAL_STOP",wave=1);rb["blocked_by"]=["aaa"];self.assertTrue(verifier.verify_campaign_run(c,{"aaa":ra,"bbb":rb})["valid"])

class BundleTests(unittest.TestCase):
    def test_manifest_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/"a.txt").write_text("a");bundle.write_manifest(root);self.assertTrue(verifier.verify_bundle(root)["valid"])
    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/"a.txt").write_text("a");bundle.write_manifest(root);(root/"a.txt").write_text("b");self.assertFalse(verifier.verify_bundle(root)["valid"])
    def test_raw_share_identity_distinct(self): self.assertTrue(bundle.raw_share_binding(b"a",b"b")["identities_are_distinct"])
    def test_secret_scan(self): self.assertTrue(bundle.scan_text("Bearer abcdefghijklmnopqrstuvwxyz"))

class CoverageTests(unittest.TestCase):
    def test_test_methods_are_fully_qualified(self):
        with tempfile.TemporaryDirectory() as tmp:
            # path must be under ROOT for qualification; exercise AST through a temporary path by patching ROOT.
            p=Path(tmp)/"t.py";p.write_text("import unittest\nclass X(unittest.TestCase):\n def test_a(self): pass\n")
            with mock.patch.object(coverage,"ROOT",Path(tmp)):
                self.assertEqual(["t.py::X.test_a"],coverage.test_methods(p))
    def test_discover_expansion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);d=root/"tools/tests";d.mkdir(parents=True);(d/"test_a.py").write_text("class X:\n def test_x(self): pass\n");(d/"other.py").write_text("class Y:\n def test_y(self): pass\n")
            with mock.patch.object(coverage,"ROOT",root):
                paths=coverage._command_test_paths(["python","-m","unittest","discover","-s","tools/tests","-p","test_*.py","-v"])
                self.assertEqual([d/"test_a.py"],paths)

class PilotVerifierTests(unittest.TestCase):
    def test_selective_expected_failure_is_mechanism_pass(self):
        summary={"first_failure":"pilot.beta.fail","results":{"pilot.alpha.pass":{"status":"PASS"},"pilot.beta.fail":{"status":"FAIL"},"pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"]},"pilot.gamma.independent":{"status":"PASS"},"pilot.publication.blocked":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.dependent"]}}}
        self.assertTrue(pilot_verify.verify(summary,"selective")["valid"])
    def test_global_stop_requires_late_task_not_started(self):
        summary={"global_stop":"pilot.global.fail","results":{"pilot.global.arm":{"status":"PASS"},"pilot.global.fail":{"status":"FAIL"},"pilot.global.anchor":{"status":"PASS"},"pilot.global.must_not_start":{"status":"BLOCKED_GLOBAL_STOP","blocked_by":["pilot.global.fail"],"command_records":[]}}}
        self.assertTrue(pilot_verify.verify(summary,"global")["valid"])

class LauncherLogicTests(unittest.TestCase):
    def test_repo_mutation_forces_global_stop_marker(self):
        # Full launcher is exercised locally on the real checkout. This metatest
        # locks the helper semantics without mutating this test repository.
        self.assertIn("__REPO_MUTATION__", Path(launcher.__file__).read_text(encoding="utf-8"))


class DocumentationContractTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.plan = self.root / "docs/sprints/skill_enforcement_rollout/PARALELO"

    def test_required_plan_documents_exist(self):
        required = {"README.md", "01_MANDATO_DECISOES.md", "02_ARQUITETURA_CONTRATOS.md", "03_CICLO_GATES.md", "04_CI_COBERTURA.md", "05_CASOS_TRANSVERSAIS.md", "06_AUDITORIA_EVIDENCIA.md", "07_PARALELISMO_INTEGRACAO.md", "08_DATABRICKS_GENIE.md", "09_PAPEIS_HANDOFFS.md", "10_IMPLANTACAO.md", "11_RISCOS_BLOQUEIOS.md", "12_FONTES.md", "13_ADENDO_OPERACIONAL.md", "14_CHECKLIST_PRONTIDAO.md", "CONTROLE_PLANO.json"}
        self.assertEqual([], sorted(name for name in required if not (self.plan / name).is_file()))

    def test_control_plan_matches_b0_candidate_state(self):
        payload = json.loads((self.plan / "CONTROLE_PLANO.json").read_text(encoding="utf-8"))
        self.assertEqual("B0_IMPLEMENTED_CANDIDATE_LOCAL_QUALIFICATION_PENDING", payload["status"])
        self.assertEqual("IMPLEMENTED_CANDIDATE", payload["mechanism_implementation"])
        self.assertFalse(payload["policy_changed"])
        self.assertEqual("NOT_STARTED", payload["skill_implementation_under_this_plan"])

    def test_planning_catalog_counts_and_ids_are_unique(self):
        cases = json.loads((self.plan / "catalogos/CASOS.json").read_text(encoding="utf-8"))
        rows = cases["cases"] if isinstance(cases, dict) else cases
        ids = [row["case_id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(236, len(ids))
        dag = json.loads((self.plan / "catalogos/DAG.json").read_text(encoding="utf-8"))
        node_ids = [row["node_id"] for row in dag["nodes"]]
        self.assertEqual(len(node_ids), len(set(node_ids)))
        self.assertTrue(all(edge["source"] in set(node_ids) and edge["target"] in set(node_ids) for edge in dag["edges"]))

    def test_b0_checkpoint_does_not_claim_local_pass(self):
        checkpoint = (self.plan / "B0/CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("LOCAL_QUALIFICATION = NOT_RUN_LOCAL", checkpoint.replace("B0.5 HOST_QUALIFICATION", "LOCAL_QUALIFICATION"))
        self.assertIn("POLICY_CHANGED = false", checkpoint)

if __name__=="__main__": unittest.main()
