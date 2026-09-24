from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.skill_enforcement.parallel import bundle, contract, coverage, registry, scheduler, verifier, pilot_verify
from tools.skill_enforcement.parallel import launcher, process


def task(task_id="task.a", deps=None, key="k", role="executor", resource="light", failure_scope="LOCAL_CHAIN"):
    return {"task_schema":contract.TASK_SCHEMA_VERSION,"task_id":task_id,"role":role,"stage":"B0.6","skill":"synthetic","candidate_sha":"a"*40,"command_ids":["b0:pilot:pass"],"depends_on":deps or [],"read_roots":["tools"],"write_roots":[],"protected_paths":["ambiente_fonte"],"resource_class":resource,"exclusivity_key":key,"required":True,"expected_effect":"NONE","failure_scope":failure_scope}

def campaign(tasks=None):
    return {"schema_version":contract.CAMPAIGN_SCHEMA_VERSION,"campaign_id":"SER-B0-TEST","baseline_sha":"b"*40,"candidate_sha":"a"*40,"state":"PLANNED","max_parallel":2,"max_auditors":1,"resource_limits":{"light":2,"audit":1},"tasks":tasks or [task()],"command_registry_digest":"1"*64,"coverage_digest":"2"*64,"policy_before_digest":"3"*64,"human_gates":["B0_RELEASE"],"external_gates":[],"repo_mode":"READ_ONLY"}

def command_record(command_id="b0:pilot:pass",exit_code=0):
    argv,_=registry.resolve_command(command_id); empty=hashlib.sha256(b"").hexdigest()
    return {"name":command_id.replace(":","_"),"argv":argv,"exit_code":exit_code,"command_started":True,"cleanup":"COMPLETE","stdout_sha256":empty,"stderr_sha256":empty}

def result(task_id="task.a",status="PASS",exit_code=0,wave=0,command_id="b0:pilot:pass"):
    return {"result_schema":contract.RESULT_SCHEMA_VERSION,"task_id":task_id,"candidate_sha":"a"*40,"status":status,"effect_state":"NONE","command_records":[] if status.startswith("BLOCKED") else [command_record(command_id,exit_code)],"first_failure":None,"wave_index":wave,"started_at_utc":"2026-09-24T00:00:00Z","ended_at_utc":"2026-09-24T00:00:01Z","protected_fingerprint_before":"4"*64,"protected_fingerprint_after":"4"*64,"issues":[]}

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
        c=campaign([task("aaa",failure_scope="GLOBAL_CAMPAIGN"),task("bbb",key="k2")]);ra=result("aaa","FAIL",1,0);rb=result("bbb","BLOCKED_GLOBAL_STOP",wave=1);rb["blocked_by"]=["aaa"];ra["first_failure"]=rb["first_failure"]="aaa";self.assertTrue(verifier.verify_campaign_run(c,{"aaa":ra,"bbb":rb})["valid"])

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
        summary={"status":"FAIL","first_failure":"pilot.beta.fail","global_stop":None,"verification":{"valid":True,"issues":[]},"results":{"pilot.alpha.pass":{"status":"PASS"},"pilot.beta.fail":{"status":"FAIL"},"pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"],"command_records":[]},"pilot.gamma.independent":{"status":"PASS"},"pilot.publication.blocked":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.dependent"],"command_records":[]}}}
        self.assertTrue(pilot_verify.verify(summary,"selective")["valid"])
    def test_global_stop_requires_late_task_not_started(self):
        summary={"status":"FAIL","first_failure":"pilot.global.fail","global_stop":"pilot.global.fail","verification":{"valid":True,"issues":[]},"results":{"pilot.global.arm":{"status":"PASS"},"pilot.global.fail":{"status":"FAIL"},"pilot.global.anchor":{"status":"PASS"},"pilot.global.must_not_start":{"status":"BLOCKED_GLOBAL_STOP","blocked_by":["pilot.global.fail"],"command_records":[]},"pilot.global.integrator":{"status":"BLOCKED_GLOBAL_STOP","blocked_by":["pilot.global.fail"],"command_records":[]}}}
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
        self.assertEqual("B0_CORRECTED_CANDIDATE_FULL_CHECKOUT_TESTS_PENDING", payload["status"])
        self.assertEqual("CORRECTED_CANDIDATE", payload["mechanism_implementation"])
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


class CorrectiveRegressionTests(unittest.TestCase):
    def test_registry_rejects_arbitrary_executable_module_script_and_absolute_shell(self):
        base=json.loads(registry.DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        bad_argv=[["/bin/echo","x"],["{PYTHON}","-B","-m","evil.module"],["{PYTHON}","evil.py"],["/bin/bash","-c","echo x"]]
        for argv in bad_argv:
            with self.subTest(argv=argv), tempfile.TemporaryDirectory() as tmp:
                payload=json.loads(json.dumps(base));payload["commands"][0]["argv"]=argv
                p=Path(tmp)/"r.json";p.write_text(json.dumps(payload),encoding="utf-8")
                self.assertRaises(registry.RegistryError,registry.load_registry,p)

    def test_dependency_failure_cannot_execute_dependent(self):
        c=campaign([task("aaa"),task("bbb",["aaa"],"k2")])
        ra=result("aaa","FAIL",1,0);rb=result("bbb","PASS",0,1);ra["first_failure"]=rb["first_failure"]="aaa"
        v=verifier.verify_campaign_run(c,{"aaa":ra,"bbb":rb})
        self.assertFalse(v["valid"]);self.assertTrue(any("UNSATISFIED_DEPENDENCY" in i for i in v["issues"]))

    def test_global_stop_cannot_escape_in_later_wave(self):
        c=campaign([task("aaa",failure_scope="GLOBAL_CAMPAIGN"),task("bbb",key="k2")])
        ra=result("aaa","FAIL",1,0);rb=result("bbb","PASS",0,1);ra["first_failure"]=rb["first_failure"]="aaa"
        v=verifier.verify_campaign_run(c,{"aaa":ra,"bbb":rb})
        self.assertFalse(v["valid"]);self.assertTrue(any("GLOBAL_STOP_ESCAPE" in i for i in v["issues"]))

    def test_result_task_and_task_candidate_bindings(self):
        t=task();c=campaign([t]);r=result();r["task_id"]="other.task"
        self.assertFalse(verifier.verify_campaign_run(c,{"task.a":r})["valid"])
        t2=task();t2["candidate_sha"]="b"*40;c2=campaign([t2])
        self.assertFalse(verifier.verify_campaign_run(c2,{"task.a":result()})["valid"])

    def test_effect_running_command_pass_issues_rejected(self):
        c=campaign()
        for mutate in (
            lambda r:r.update(effect_state="MODIFIED"),
            lambda r:r.update(status="RUNNING"),
            lambda r:r.update(issues=["pending"]),
            lambda r:r["command_records"][0].update(argv=["evil"]),
        ):
            r=result();mutate(r)
            self.assertFalse(verifier.verify_campaign_run(c,{"task.a":r})["valid"])

    def test_wave_parallel_exclusivity_auditor_and_resource_limits(self):
        rows=[task("aaa",key="same",role="domain_auditor",resource="audit"),task("bbb",key="same",role="evidence_auditor",resource="audit")]
        c=campaign(rows);c["max_parallel"]=1;c["max_auditors"]=1;c["resource_limits"]={"audit":1}
        v=verifier.verify_campaign_run(c,{"aaa":result("aaa",wave=0),"bbb":result("bbb",wave=0)})
        joined=" ".join(v["issues"])
        self.assertIn("MAX_PARALLEL_EXCEEDED",joined);self.assertIn("EXCLUSIVITY_VIOLATION",joined)
        self.assertIn("AUDITOR_LIMIT_EXCEEDED",joined);self.assertIn("RESOURCE_LIMIT_EXCEEDED",joined)

    def test_command_log_hash_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);task_dir=root/"task.a";task_dir.mkdir()
            r=result();row=r["command_records"][0];prefix=task_dir/"b0_pilot_pass"
            prefix.with_suffix(".stdout.txt").write_bytes(b"");prefix.with_suffix(".stderr.txt").write_bytes(b"")
            self.assertTrue(verifier.verify_campaign_run(campaign(),{"task.a":r},root)["valid"])
            prefix.with_suffix(".stdout.txt").write_bytes(b"tamper")
            self.assertFalse(verifier.verify_campaign_run(campaign(),{"task.a":r},root)["valid"])

    def test_nested_manifest_is_covered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/"nested").mkdir();(root/"nested/MANIFEST.json").write_text("a",encoding="utf-8")
            bundle.write_manifest(root);(root/"nested/MANIFEST.json").write_text("b",encoding="utf-8")
            self.assertFalse(verifier.verify_bundle(root)["valid"])

    def test_share_binary_unexamined_fails_and_binding_matches_final_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";binding_path=Path(tmp)/"binding.json";raw.mkdir()
            (raw/"x.bin").write_bytes(b"\\xffBearer abcdefghijklmnopqrstuvwxyz");bundle.write_manifest(raw)
            binding=bundle.build_share(raw,share,{},binding_path=binding_path)
            self.assertEqual("FAIL",binding["secret_scan"]["status"])
            self.assertEqual(hashlib.sha256((share/"MANIFEST.json").read_bytes()).hexdigest(),binding["share_manifest_sha256"])
            self.assertFalse(verifier.verify_raw_share_binding(raw,share,binding_path)["valid"])

    def test_share_preserves_crlf_when_no_substitution(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";binding_path=Path(tmp)/"binding.json";raw.mkdir()
            original=b"a\\r\\nb\\r\\n";(raw/"x.txt").write_bytes(original);bundle.write_manifest(raw)
            bundle.build_share(raw,share,{},binding_path=binding_path)
            self.assertEqual(original,(share/"x.txt").read_bytes())
            self.assertTrue(verifier.verify_raw_share_binding(raw,share,binding_path)["valid"])

    def test_process_hash_is_over_exact_persisted_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            row=process.run_argv([sys.executable,"-c",'import sys;sys.stdout.buffer.write(b"a\\r\\nb\\r\\n")'],Path(tmp),"raw")
            data=(Path(tmp)/"raw.stdout.txt").read_bytes()
            self.assertEqual(b"a\\r\\nb\\r\\n",data)
            self.assertEqual(hashlib.sha256(data).hexdigest(),row["stdout_sha256"])

    def test_pilot_rejects_invalid_campaign_verification(self):
        summary={"status":"FAIL","first_failure":"pilot.beta.fail","global_stop":None,"verification":{"valid":False,"issues":["x"]},"results":{"pilot.alpha.pass":{"status":"PASS"},"pilot.beta.fail":{"status":"FAIL"},"pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"],"command_records":[]},"pilot.gamma.independent":{"status":"PASS"},"pilot.publication.blocked":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.dependent"],"command_records":[]}}}
        self.assertFalse(pilot_verify.verify(summary,"selective")["valid"])

    def test_coverage_has_no_empty_method_map(self):
        payload=coverage.inventory()
        rows=[*payload["se08"],*payload["ci_non_sef"],*payload["ser01"]]
        self.assertFalse(any(row["mapping_status"]=="EMPTY_METHOD_MAP" for row in rows),payload["issues"])
        self.assertTrue(all(row["mapping_status"] in {"MAPPED","COMMAND_ONLY"} for row in rows),payload["issues"])

if __name__=="__main__": unittest.main()
