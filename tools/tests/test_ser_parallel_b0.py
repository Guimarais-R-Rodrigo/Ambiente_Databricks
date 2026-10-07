from __future__ import annotations

import copy
import types
import hashlib
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tools.skill_enforcement.parallel import bundle, contract, coverage, registry, scheduler, verifier, pilot_verify
from tools.skill_enforcement.parallel import launcher, process, preflight, round_identity, freeze_prepare, host_qualification, b0_release


def task(task_id="task.a", deps=None, key="k", role="executor", resource="light", failure_scope="LOCAL_CHAIN", required=True, command_ids=None):
    row={"task_schema":contract.TASK_SCHEMA_VERSION,"task_id":task_id,"role":role,"stage":"B0.6","skill":"synthetic","candidate_sha":"a"*40,"command_ids":command_ids if command_ids is not None else ["b0:pilot:pass"],"depends_on":deps or [],"read_roots":["tools"],"write_roots":[],"protected_paths":["ambiente_databricks"],"resource_class":resource,"exclusivity_key":key,"required":required,"expected_effect":"NONE","failure_scope":failure_scope}
    if not required: row["not_applicable_reason"]="preapproved synthetic optional case"
    return row

def campaign(tasks=None):
    return {"schema_version":contract.CAMPAIGN_SCHEMA_VERSION,"campaign_id":"SER-B0-TEST","round_id":"B0ROUND-test","release_spec_digest":"9"*64,"baseline_sha":"b"*40,"candidate_sha":"a"*40,"candidate_tree_sha":"c"*40,"state":"PLANNED","max_parallel":2,"max_auditors":1,"resource_limits":{"light":2,"audit":1},"tasks":tasks or [task()],"command_registry_digest":"1"*64,"coverage_digest":"2"*64,"policy_before_digest":"3"*64,"human_gates":["B0_RELEASE"],"external_gates":[],"repo_mode":"READ_ONLY"}

def command_record(command_id="b0:pilot:pass",exit_code=0):
    argv,_=registry.resolve_command(command_id); empty=hashlib.sha256(b"").hexdigest()
    return {"record_schema":contract.COMMAND_RECORD_SCHEMA_VERSION,"name":command_id.replace(":","_"),"argv":argv,"command_started":True,"pid":12345,"exit_code":exit_code,"timed_out":False,"cleanup":"COMPLETE","residual_descendants_detected":False,"supervision":"POSIX_PROCESS_GROUP","duration_seconds":0.1,"started_at_utc":"2026-09-24T00:00:00+00:00","ended_at_utc":"2026-09-24T00:00:01+00:00","stdout_sha256":empty,"stderr_sha256":empty}

def result(task_id="task.a",status="PASS",exit_code=0,wave=0,command_id="b0:pilot:pass"):
    blocked=status.startswith("BLOCKED") or status=="NOT_APPLICABLE"
    start=min(wave*2,8); end=min(wave*2+1,9)
    return {"result_schema":contract.RESULT_SCHEMA_VERSION,"task_id":task_id,"round_id":"B0ROUND-test","release_spec_digest":"9"*64,"candidate_sha":"a"*40,"status":status,"effect_state":"NONE","command_records":[] if blocked else [command_record(command_id,exit_code)],"first_failure":None,"wave_index":wave,"started_at_utc":f"2026-09-24T00:00:0{start}+00:00","ended_at_utc":f"2026-09-24T00:00:0{end}+00:00","protected_fingerprint_before":"4"*64,"protected_fingerprint_after":"4"*64,"issues":[]}

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
    def test_registry_loads(self):
        commands=registry.load_registry()["commands"]
        self.assertIn("b0:pilot:pass",commands)
        self.assertIn("b0:sandbox:probe",commands)
    def test_unknown_command_rejected(self): self.assertRaises(registry.RegistryError,registry.resolve_command,"missing")
    def test_shell_and_inline_code_rejected(self):
        for argv in (["bash","-c","echo x"],["{PYTHON}","-c","print(1)"]):
            with self.subTest(argv=argv), tempfile.TemporaryDirectory() as tmp:
                payload=json.loads(registry.DEFAULT_REGISTRY.read_text(encoding="utf-8"));payload["commands"][0]["argv"]=argv
                p=Path(tmp)/"r.json";p.write_text(json.dumps(payload),encoding="utf-8")
                self.assertRaises(registry.RegistryError,registry.load_registry,p)
    def test_unknown_placeholder_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload=json.loads(registry.DEFAULT_REGISTRY.read_text(encoding="utf-8"));payload["commands"][0]["argv"]=["{SHELL}","x"]
            p=Path(tmp)/"r.json";p.write_text(json.dumps(payload),encoding="utf-8")
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
    def test_raw_share_identity_distinct(self): self.assertTrue(bundle.raw_share_binding(b"a",b"b",{"policy_version":bundle.SECRET_SCAN_POLICY_VERSION,"status":"PASS","findings":[]})["identities_are_distinct"])
    def test_secret_scan(self):
        self.assertTrue(bundle.scan_text("Bearer abcdefghijklmnopqrstuvwxyz"))

    def test_share_scan_rejects_residual_user_home_paths(self):
        windows_home="C:"+"\\Users\\Example\\python.exe"
        posix_home="/home/example/python"
        root_home="/root/python"
        self.assertIn("SENSITIVE_PATH_WINDOWS_HOME",bundle.scan_text(json.dumps({"python":windows_home})))
        self.assertIn("SENSITIVE_PATH_POSIX_HOME",bundle.scan_text(json.dumps({"python":posix_home})))
        self.assertIn("SENSITIVE_PATH_POSIX_HOME",bundle.scan_text(json.dumps({"python":root_home})))

    def test_default_share_substitutions_redact_home_and_repo_variants(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);raw=base/"RAW";share=base/"SHARE";binding=base/"binding.json";raw.mkdir()
            home=str(Path.home().resolve())
            repo=str(base.resolve())
            payload={"python":str(Path.home()/"bin"/"python"),"repo":str(base/"repo"/"x")}
            (raw/"paths.json").write_text(json.dumps(payload),encoding="utf-8")
            bundle.write_manifest(raw)
            built=bundle.build_share(raw,share,bundle.default_share_substitutions(base),binding_path=binding)
            text=(share/"paths.json").read_text(encoding="utf-8")
            self.assertNotIn(home,text)
            self.assertNotIn(json.dumps(home)[1:-1],text)
            self.assertNotIn(repo,text)
            self.assertIn("<HOME>",text)
            self.assertIn("<REPO>",text)
            self.assertEqual("PASS",built["secret_scan"]["status"],built)
            self.assertTrue(verifier.verify_raw_share_binding(raw,share,binding)["valid"])

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
        summary={"status":"FAIL","round_id":"B0ROUND-test","release_spec_digest":"9"*64,"first_failure":"pilot.beta.fail","global_stop":None,"issues":[],"verification":{"valid":True,"issues":[]},"results":{"pilot.alpha.pass":{"status":"PASS"},"pilot.beta.fail":{"status":"FAIL"},"pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"],"command_records":[]},"pilot.gamma.independent":{"status":"PASS"},"pilot.publication.blocked":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.dependent"],"command_records":[]}}}
        self.assertTrue(pilot_verify.verify(summary,"selective")["valid"])
    def test_global_stop_requires_late_task_not_started(self):
        summary={"status":"FAIL","round_id":"B0ROUND-test","release_spec_digest":"9"*64,"first_failure":"pilot.global.fail","global_stop":"pilot.global.fail","issues":[],"verification":{"valid":True,"issues":[]},"results":{"pilot.global.arm":{"status":"PASS"},"pilot.global.fail":{"status":"FAIL"},"pilot.global.anchor":{"status":"PASS"},"pilot.global.must_not_start":{"status":"BLOCKED_GLOBAL_STOP","blocked_by":["pilot.global.fail"],"command_records":[]},"pilot.global.integrator":{"status":"BLOCKED_GLOBAL_STOP","blocked_by":["pilot.global.fail"],"command_records":[]}}}
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
        self.assertIsInstance(payload["status"], str)
        self.assertTrue(payload["status"].startswith("B0_"))
        self.assertEqual("AUDIT_CORRECTIVE_V3", payload["mechanism_implementation"])
        self.assertFalse(payload["launchable"])
        self.assertFalse(payload["policy_changed"])
        self.assertEqual("NOT_STARTED", payload["skill_implementation_under_this_plan"])
        self.assertFalse(payload["merge_performed"])

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
        self.assertIn("LOCAL_QUALIFICATION = NOT_RUN", checkpoint)
        self.assertNotRegex(checkpoint, r"(?m)^LOCAL_QUALIFICATION\s*=\s*(?:PASS|LOCAL_QUALIFIED)\s*$")
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
        self.assertIn("MAX_PARALLEL_INTERVAL_EXCEEDED",joined);self.assertIn("EXCLUSIVITY_INTERVAL_VIOLATION",joined)
        self.assertIn("AUDITOR_INTERVAL_LIMIT_EXCEEDED",joined);self.assertIn("RESOURCE_INTERVAL_LIMIT_EXCEEDED",joined)

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
            (raw/"x.bin").write_bytes(b"\xffBearer abcdefghijklmnopqrstuvwxyz");bundle.write_manifest(raw)
            binding=bundle.build_share(raw,share,{},binding_path=binding_path)
            self.assertEqual("FAIL",binding["secret_scan"]["status"])
            self.assertEqual(hashlib.sha256((share/"MANIFEST.json").read_bytes()).hexdigest(),binding["share_manifest_sha256"])
            self.assertFalse(verifier.verify_raw_share_binding(raw,share,binding_path)["valid"])

    def test_share_preserves_crlf_when_no_substitution(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";binding_path=Path(tmp)/"binding.json";raw.mkdir()
            original=b"a\r\nb\r\n";(raw/"x.txt").write_bytes(original);bundle.write_manifest(raw)
            bundle.build_share(raw,share,{},binding_path=binding_path)
            self.assertEqual(original,(share/"x.txt").read_bytes())
            self.assertTrue(verifier.verify_raw_share_binding(raw,share,binding_path)["valid"])

    def test_process_hash_is_over_exact_persisted_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            row=process.run_argv([sys.executable,"-c",'import sys;sys.stdout.buffer.write(b"a\\r\\nb\\r\\n")'],Path(tmp),"raw")
            data=(Path(tmp)/"raw.stdout.txt").read_bytes()
            self.assertEqual(b"a\r\nb\r\n",data)
            self.assertEqual(hashlib.sha256(data).hexdigest(),row["stdout_sha256"])

    def test_pilot_rejects_invalid_campaign_verification(self):
        summary={"status":"FAIL","round_id":"B0ROUND-test","release_spec_digest":"9"*64,"first_failure":"pilot.beta.fail","global_stop":None,"issues":[],"verification":{"valid":False,"issues":["x"]},"results":{"pilot.alpha.pass":{"status":"PASS"},"pilot.beta.fail":{"status":"FAIL"},"pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"],"command_records":[]},"pilot.gamma.independent":{"status":"PASS"},"pilot.publication.blocked":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.dependent"],"command_records":[]}}}
        self.assertFalse(pilot_verify.verify(summary,"selective")["valid"])

    def test_coverage_has_no_empty_method_map(self):
        payload=coverage.inventory()
        self.assertEqual("PASS",payload["status"],payload.get("issues"))
        rows=[*payload["se08"],*payload["ci_non_sef"],*payload["ser01"]]
        details=[
            {"step_id":row["step_id"],"mapping_status":row["mapping_status"],"collection_errors":row.get("collection_errors",[])}
            for row in rows if row["mapping_status"] not in {"MAPPED","COMMAND_ONLY"}
        ]
        self.assertFalse(any(row["mapping_status"]=="EMPTY_METHOD_MAP" for row in rows),details)
        self.assertTrue(all(row["mapping_status"] in {"MAPPED","COMMAND_ONLY"} for row in rows),details)
        rendered=coverage._json_cli({"text":"L2→L3"})
        self.assertEqual({"text":"L2→L3"},json.loads(rendered))
        rendered.encode("cp1252")


class IndependentAuditRegressionTests(unittest.TestCase):
    def test_result_null_wrong_type_empty_and_missing_are_rejected(self):
        c=campaign()
        for results in ({},{"task.a":None},{"task.a":[]},{"task.a":{}}):
            with self.subTest(results=results):
                self.assertFalse(verifier.verify_campaign_run(c,results)["valid"])

    def test_required_task_cannot_be_empty_or_not_applicable(self):
        self.assertIn("TASK_COMMANDS_EMPTY",contract.validate_task(task(command_ids=[])))
        self.assertFalse(verifier.verify_campaign_run(campaign(),{"task.a":result(status="NOT_APPLICABLE")})["valid"])

    def test_optional_not_applicable_requires_preapproved_reason(self):
        t=task(required=False);c=campaign([t]);r=result(status="NOT_APPLICABLE")
        self.assertTrue(verifier.verify_campaign_run(c,{"task.a":r})["valid"])
        del t["not_applicable_reason"]
        self.assertFalse(verifier.verify_campaign_run(campaign([t]),{"task.a":r})["valid"])

    def test_command_record_rejects_timeout_bool_exit_missing_exit_and_bad_time(self):
        variants=[]
        x=command_record();x["timed_out"]=True;variants.append(x)
        x=command_record();x["exit_code"]=False;variants.append(x)
        x=command_record();del x["exit_code"];variants.append(x)
        x=command_record();x["started_at_utc"]="not-a-time";variants.append(x)
        for row in variants:
            with self.subTest(row=row):
                self.assertTrue(contract.validate_command_record(row))

    def test_temporal_overlap_hidden_by_waves_is_rejected(self):
        c=campaign([task("aaa",key="same"),task("bbb",key="same")]);c["max_parallel"]=1;c["resource_limits"]={"light":1}
        a=result("aaa",wave=0);b=result("bbb",wave=1);b["started_at_utc"]=a["started_at_utc"];b["ended_at_utc"]=a["ended_at_utc"]
        v=verifier.verify_campaign_run(c,{"aaa":a,"bbb":b})
        self.assertFalse(v["valid"]);self.assertTrue(any("TEMPORAL_BARRIER" in i or "INTERVAL" in i for i in v["issues"]))

    def test_global_stop_block_cannot_precede_failure(self):
        c=campaign([task("aaa",failure_scope="GLOBAL_CAMPAIGN"),task("bbb",key="k2")])
        a=result("aaa","FAIL",1,1);b=result("bbb","BLOCKED_GLOBAL_STOP",wave=0);a["first_failure"]=b["first_failure"]="aaa";b["blocked_by"]=["aaa"]
        self.assertFalse(verifier.verify_campaign_run(c,{"aaa":a,"bbb":b})["valid"])

    def test_cycle_cannot_be_hidden_by_not_applicable(self):
        ta=task("aaa",["bbb"],"a",required=False);tb=task("bbb",["aaa"],"b",required=False);c=campaign([ta,tb])
        self.assertFalse(verifier.verify_campaign_run(c,{"aaa":result("aaa","NOT_APPLICABLE"),"bbb":result("bbb","NOT_APPLICABLE")})["valid"])

    def test_secret_scan_cannot_be_resealed_and_filename_is_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";binding=Path(tmp)/"binding.json";raw.mkdir()
            (raw/"safe.txt").write_text("Bearer abcdefghijklmnopqrstuvwxyz",encoding="utf-8");bundle.write_manifest(raw);bundle.build_share(raw,share,{},binding_path=binding)
            payload=json.loads(binding.read_text(encoding="utf-8"));payload["secret_scan"]={"policy_version":bundle.SECRET_SCAN_POLICY_VERSION,"status":"PASS","findings":[]};binding.write_text(json.dumps(payload),encoding="utf-8")
            self.assertFalse(verifier.verify_raw_share_binding(raw,share,binding)["valid"])
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";binding=Path(tmp)/"binding.json";raw.mkdir()
            (raw/"ghp_abcdefghijklmnopqrstuvwxyz.txt").write_text("safe",encoding="utf-8");bundle.write_manifest(raw);built=bundle.build_share(raw,share,{},binding_path=binding)
            self.assertEqual("FAIL",built["secret_scan"]["status"])

    def test_reserved_metadata_collision_and_external_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";raw.mkdir();(raw/"SHARE_METADATA.json").write_text("original",encoding="utf-8");bundle.write_manifest(raw)
            self.assertRaises(ValueError,bundle.build_share,raw,share,{})
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"root";root.mkdir();outside=Path(tmp)/"outside.txt";outside.write_text("x",encoding="utf-8");link=root/"link.txt"
            try: link.symlink_to(outside)
            except (OSError,NotImplementedError): self.skipTest("symlink unavailable")
            self.assertRaises(ValueError,bundle.write_manifest,root)

    def test_real_crlf_and_real_non_utf8_are_discriminant(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/"RAW";share=Path(tmp)/"SHARE";binding=Path(tmp)/"binding.json";raw.mkdir()
            crlf=b"a\r\nb\r\n";(raw/"crlf.txt").write_bytes(crlf);(raw/"binary.bin").write_bytes(b"\xff\xfe\x00");bundle.write_manifest(raw);built=bundle.build_share(raw,share,{},binding_path=binding)
            self.assertEqual(crlf,(share/"crlf.txt").read_bytes());self.assertIn("BINARY_UNEXAMINED"," ".join(built["secret_scan"]["findings"]))

    def test_clean_env_preserves_home_identity_without_credentials(self):
        sample={
            "PATH": os.environ.get("PATH",""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT",""),
            "WINDIR": os.environ.get("WINDIR",""),
            "TEMP": os.environ.get("TEMP",""),
            "TMP": os.environ.get("TMP",""),
            "HOME": r"C:\\Users\\Example",
            "USERPROFILE": r"C:\\Users\\Example",
            "HOMEDRIVE": "C:",
            "HOMEPATH": r"\\Users\\Example",
            "APPDATA": r"C:\\Users\\Example\\AppData\\Roaming",
            "LOCALAPPDATA": r"C:\\Users\\Example\\AppData\\Local",
            "PROGRAMDATA": r"C:\\ProgramData",
            "COMSPEC": r"C:\\Windows\\System32\\cmd.exe",
            "PATHEXT": ".COM;.EXE;.BAT;.CMD",
            "GITHUB_TOKEN": "must-not-leak",
            "OPENAI_API_KEY": "must-not-leak",
        }
        with mock.patch.dict(process.os.environ,sample,clear=True):
            env=process._clean_env()
        self.assertEqual(r"C:\\Users\\Example",env["USERPROFILE"])
        self.assertEqual(r"C:\\Users\\Example",env["HOME"])
        self.assertEqual("C:",env["HOMEDRIVE"])
        self.assertEqual(r"\\Users\\Example",env["HOMEPATH"])
        self.assertEqual(r"C:\\Users\\Example\\AppData\\Roaming",env["APPDATA"])
        self.assertEqual(r"C:\\Users\\Example\\AppData\\Local",env["LOCALAPPDATA"])
        self.assertEqual(r"C:\\Windows\\System32\\cmd.exe",env["COMSPEC"])
        self.assertEqual(".COM;.EXE;.BAT;.CMD",env["PATHEXT"])
        self.assertNotIn("GITHUB_TOKEN",env)
        self.assertNotIn("OPENAI_API_KEY",env)

    def test_clean_env_allows_child_path_home(self):
        completed=process.subprocess.run(
            [sys.executable,"-c","from pathlib import Path; p=Path.home(); assert p.is_absolute(); print(p)"],
            cwd=process.ROOT,
            env=process._clean_env(),
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(0,completed.returncode,completed.stderr.decode("utf-8",errors="replace"))
        self.assertTrue(completed.stdout.strip())

    def test_coverage_cli_passes_under_sanitized_child_environment(self):
        completed=process.subprocess.run(
            [sys.executable,"-B","-m","tools.skill_enforcement.parallel.coverage"],
            cwd=process.ROOT,
            env=process._clean_env(),
            capture_output=True,
            timeout=300,
        )
        stderr=completed.stderr.decode("utf-8",errors="replace")
        stdout=completed.stdout.decode("utf-8",errors="strict")
        self.assertEqual(0,completed.returncode,stderr)
        payload=json.loads(stdout)
        self.assertEqual("PASS",payload["status"],payload.get("issues"))
        cfg=json.loads(coverage.REGISTRY.read_text(encoding="utf-8"))
        for section, expected in (
            ("se08", set(cfg["step_policy"])),
            ("ci_non_sef", set(cfg["ci_step_policy"])),
            ("ser01", {group["group_id"] for group in cfg["ser01_groups"]}),
        ):
            actual=[row["step_id"] for row in payload[section]]
            self.assertTrue(actual, section)
            self.assertEqual(expected, set(actual), section)
            self.assertEqual(len(actual), len(set(actual)), section)
        ci={row["step_id"]:row for row in payload["ci_non_sef"]}
        self.assertEqual("COMMAND_ONLY",ci["ci:ai-controles"]["mapping_status"])
        self.assertEqual("MAPPED",ci["ci:ai-regressoes"]["mapping_status"])
        self.assertTrue(ci["ci:ai-regressoes"]["test_methods"])

    def test_windows_supervisor_assigns_before_child_release(self):
        source=Path(process.__file__).read_text(encoding="utf-8")
        assign=source.index("job.assign(process)")
        release=source.index('process.stdin.write(b"1")')
        self.assertLess(assign,release)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"child.json";p.write_text(json.dumps({"pid":123}),encoding="utf-8")
            self.assertEqual((123,None),process._read_windows_child(p))

    def test_process_tree_residual_is_detected(self):
        if sys.platform=="win32": self.skipTest("Windows job-object proof belongs to host qualification")
        with tempfile.TemporaryDirectory() as tmp:
            code='import subprocess,sys;subprocess.Popen([sys.executable,"-c","import time;time.sleep(5)"]);sys.exit(0)'
            row=process.run_argv([sys.executable,"-c",code],Path(tmp),"tree",timeout=10)
            self.assertTrue(row["residual_descendants_detected"]);self.assertEqual("COMPLETE_DESCENDANTS_TERMINATED",row["cleanup"])

    def test_coverage_missing_target_and_non_collected_ast_test_are_not_mapped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);tests=root/"tools/tests";tests.mkdir(parents=True);p=tests/"test_fake.py";p.write_text("class NotATest:\n def test_x(self): pass\n",encoding="utf-8")
            with mock.patch.object(coverage,"ROOT",root):
                ids,errors,_=coverage._collect_command(["python","-B","-m","unittest","tools.tests.missing","-v"]);self.assertFalse(ids);self.assertTrue(errors)
                ids,errors,_=coverage._collect_command(["python","-B",str(p.relative_to(root)),"-v"]);self.assertFalse(ids)

    def test_command_only_requires_real_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/"tools").mkdir();valid=root/"tools/validate.py";valid.write_text("print('ok')\n",encoding="utf-8")
            with mock.patch.object(coverage,"ROOT",root):
                missing=coverage._row("ci:x","CURRENT_INVARIANT",[sys.executable,"tools/missing.py"],{"ci:x"},{})
                valid_row=coverage._row("ci:x","CURRENT_INVARIANT",[sys.executable,"tools/validate.py"],{"ci:x"},{})
            self.assertEqual("MISSING",missing["mapping_status"]);self.assertTrue(missing["collection_errors"])
            self.assertEqual("COMMAND_ONLY",valid_row["mapping_status"]);self.assertEqual([],valid_row["collection_errors"])

    def test_unittest_discover_collection_uses_loaded_module_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);tests=root/"tools/tests";tests.mkdir(parents=True)
            p=tests/"test_alpha.py";p.write_text("import unittest\nclass X(unittest.TestCase):\n def test_ok(self): pass\n",encoding="utf-8")
            with mock.patch.object(coverage,"ROOT",root):
                ids,errors,_=coverage._collect_command([sys.executable,"-B","-m","unittest","discover","-s","tools/tests","-p","test_*.py","-v"])
            self.assertEqual([],errors)
            self.assertEqual(["tools/tests/test_alpha.py::X.test_ok"],ids)

    def test_direct_test_file_with_nonpackage_path_normalizes_from_module_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);tests=root/"ambiente_databricks/.assistant/hub_snippets/tests";tests.mkdir(parents=True)
            p=tests/"test_core.py";p.write_text("import unittest\nclass X(unittest.TestCase):\n def test_ok(self): pass\n",encoding="utf-8")
            with mock.patch.object(coverage,"ROOT",root):
                ids,errors,_=coverage._collect_command([sys.executable,p.relative_to(root).as_posix()])
            self.assertEqual([],errors)
            self.assertEqual(["ambiente_databricks/.assistant/hub_snippets/tests/test_core.py::X.test_ok"],ids)

    def test_override_schema_is_closed_and_requires_successors(self):
        self.assertTrue(coverage._validate_override("x",{"classification":"OTHER","historical_sha":"x","reason":"","successor_ids":[]}))

    def test_round_binding_mismatch_is_rejected(self):
        c=campaign();c["round_id"]="B0ROUND-other"
        self.assertFalse(verifier.verify_campaign_run(c,{"task.a":result()})["valid"])

    def test_finding_schema_uses_documented_severity_and_closure_states(self):
        schema=json.loads((Path(__file__).resolve().parents[2]/"tools/skill_enforcement/parallel/schemas/finding.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(["F0","F1","F2","F3"],schema["properties"]["severity"]["enum"]);self.assertIn("FIXED_VERIFIED",schema["properties"]["status"]["enum"])

    def test_resource_profile_declares_total_slot_semantics_and_host_lease(self):
        profile=json.loads((Path(__file__).resolve().parents[2]/"tools/skill_enforcement/parallel/resource_profiles.json").read_text(encoding="utf-8"))
        self.assertIn("total number",profile["slot_semantics"]);self.assertEqual("SINGLE_LAUNCHER_OS_LEASE",profile["host_coordination"])

    def test_authoring_preflight_parses_current_tree(self):
        payload=preflight.run()
        self.assertEqual("PASS",payload["status"],payload["issues"])
        self.assertEqual(4,payload["schema_contracts_checked"])

    def test_preflight_hygiene_rejects_short_sha_collision_but_accepts_full_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            short_token="f"+"6516959"
            full_token=short_token+"a2f973ea1e163da80548e8ebb0e235cf"
            short=root/"short.md";short.write_text("freeze "+short_token,encoding="utf-8")
            full=root/"full.md";full.write_text("freeze "+full_token,encoding="utf-8")
            with mock.patch.object(preflight,"ROOT",root):
                short_issues=preflight._hygiene_issues([short])
                full_issues=preflight._hygiene_issues([full])
            self.assertEqual(["REPO_HYGIENE_IDENTIFIER:short.md"],short_issues)
            self.assertEqual([],full_issues)

    def test_freeze_prepare_cli_json_is_cp1252_safe_and_roundtrips_unicode(self):
        rendered=freeze_prepare._json_cli({"status":"FAIL","stdout":"seções · válidas → revisão"})
        rendered.encode("cp1252")
        self.assertEqual({"status":"FAIL","stdout":"seções · válidas → revisão"},json.loads(rendered))

    def test_sandbox_probe_is_effective_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            evidence=root/"evidence"
            denied=root/"denied.txt"
            denied.write_text("UNCHANGED\n",encoding="utf-8")
            argv,_=registry.resolve_command("b0:sandbox:probe")
            with mock.patch.dict(os.environ,{"SER_B0_SECRET_SENTINEL":"must-not-pass"},clear=False):
                row=process.run_argv(
                    argv,evidence,"sandbox_probe_test",timeout=30,
                    sandbox=True,sandbox_probe_target=denied,
                )
            self.assertEqual(0,row["exit_code"],(evidence/"sandbox_probe_test.stderr.txt").read_text(encoding="utf-8",errors="replace"))
            payload=json.loads((evidence/"sandbox_probe_test.stdout.txt").read_text(encoding="utf-8"))
            self.assertEqual("PASS",payload["status"],payload)
            self.assertTrue(payload["scratch_write_allowed"])
            self.assertTrue(payload["outside_write_blocked"])
            self.assertTrue(payload["subprocess_blocked"])
            self.assertTrue(payload["network_blocked"])
            self.assertTrue(payload["credential_sentinel_absent"])
            self.assertEqual("UNCHANGED\n",denied.read_text(encoding="utf-8"))

    def test_launcher_task_helper_always_requests_sandbox(self):
        fake={"ok":True}
        with mock.patch.object(launcher,"run_argv",return_value=fake) as called:
            actual=launcher._run_task_command(["python","x.py"],Path("evidence"),"x",12)
        self.assertIs(fake,actual)
        called.assert_called_once_with(["python","x.py"],Path("evidence"),"x",timeout=12,sandbox=True)

    def test_host_qualification_requires_ntfs_sandbox_job_and_observed_two_slot_pilot(self):
        record={"command_started":True,"supervision":"WINDOWS_JOB_OBJECT","timed_out":False,"residual_descendants_detected":False,"cleanup":"COMPLETE"}
        summary={"results":{
            "a":{"status":"PASS","command_records":[record],"started_at_utc":"2026-09-24T00:00:00+00:00","ended_at_utc":"2026-09-24T00:00:02+00:00"},
            "b":{"status":"FAIL","command_records":[record],"started_at_utc":"2026-09-24T00:00:00.500000+00:00","ended_at_utc":"2026-09-24T00:00:01.500000+00:00"},
        }}
        sandbox={"status":"PASS","scratch_write_allowed":True,"outside_write_blocked":True,"subprocess_blocked":True,"network_blocked":True,"credential_sentinel_absent":True}
        host={"os":"Windows","filesystem":{"family":"windows","type":"NTFS"},"client_model_configuration":"NOT_APPLICABLE_B0_DETERMINISTIC_PYTHON_RUNTIME"}
        resources={"logical_cpus":8,"disk_total_bytes":1000,"disk_free_bytes":500,"memory_total_bytes":1000,"memory_available_bytes":500}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(host_qualification.os,"name","nt"), mock.patch.object(host_qualification,"_resource_snapshot",return_value=resources):
            qualified=host_qualification.qualify(Path(tmp),host,sandbox,summary,summary)
            bad_fs=host_qualification.qualify(Path(tmp),{**host,"filesystem":{"family":"windows","type":"REFS"}},sandbox,summary,summary)
        self.assertEqual("PASS",qualified["status"],qualified)
        self.assertEqual(2,qualified["observed_peak_parallel"]["selective"])
        self.assertEqual("QUALIFIED_BY_OBSERVED_PILOTS",qualified["initial_profile"]["status"])
        self.assertEqual("NOT_QUALIFIED_REQUIRES_SEPARATE_HEADROOM_MEASUREMENT",qualified["post_pilot_candidate_3_2"])
        self.assertEqual("FAIL",bad_fs["status"])
        self.assertEqual("LOCAL_QUALIFIED",b0_release._host_release_status(qualified))
        self.assertEqual("PENDING_HOST_QUALIFICATION",b0_release._host_release_status(bad_fs))

    def test_round_start_detects_clean_head_swap(self):
        row={"candidate_sha":"a"*40,"candidate_tree_sha":"b"*40,"baseline_sha":"c"*40}
        def fake_git(*args):
            if args==("rev-parse","HEAD"): return "d"*40
            if args==("rev-parse","HEAD^{tree}"): return "b"*40
            if args==("merge-base","HEAD","origin/main"): return "c"*40
            if args==("status","--porcelain=v1","--untracked-files=all"): return ""
            raise AssertionError(args)
        with mock.patch.object(round_identity,"_git",side_effect=fake_git):
            self.assertIn("ROUND_HEAD_CHANGED",round_identity.assert_round_start_current(row))

class CoverageIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="b0 coverage ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "tools/tests/test_cases.py"
        self.path.parent.mkdir(parents=True)
        self.path.write_text(
            "import unittest\nclass Checks(unittest.TestCase):\n"
            " def test_one(self): pass\n def test_two(self): pass\n",
            encoding="utf-8",
        )
        (self.root / "tools/check.py").write_text("print('local')\n", encoding="utf-8")
        self.argv = [sys.executable, "-B", "tools/tests/test_cases.py", "-v"]
        self.steps = [
            ("sef", "profile", [sys.executable, "tools/check.py"]),
            ("tests", "regression", self.argv),
            ("command", "guard", [sys.executable, "tools/check.py"]),
        ]
        self.profile = [("suite", self.argv)]
        self.cfg = {
            "schema_version": coverage.REGISTRY_SCHEMA,
            "step_policy": {"suite": "CURRENT_INVARIANT"},
            "ci_step_policy": {
                "ci:tests": {"classification": "CURRENT_INVARIANT", "mapping_mode": "unittest"},
                "ci:command": {"classification": "CURRENT_INVARIANT", "mapping_mode": "command"},
            },
            "method_overrides": {},
            "retired_method_overrides": {},
            "command_only_steps": ["ci:command"],
            "ser01_groups": [{"group_id": name, "path": "tools/tests/test_cases.py"} for name in sorted(coverage.SER01_GROUP_IDS)],
        }
        self.registry = self.root / "coverage.json"

    def inventory(self):
        self.registry.write_text(json.dumps(self.cfg), encoding="utf-8")
        with mock.patch.object(coverage, "ROOT", self.root), mock.patch.object(coverage, "REGISTRY", self.registry), mock.patch.object(
            coverage, "_load", side_effect=[
                types.SimpleNamespace(PROFILE_STEPS={"se08": self.profile}),
                types.SimpleNamespace(ETAPAS=self.steps),
            ],
        ):
            return coverage.inventory()

    def assert_issue(self, expected):
        result = self.inventory()
        self.assertEqual("FAIL", result["status"])
        self.assertIn(expected, result["issues"])
        return result

    def test_valid_inventory_collects_actual_nonempty_methods(self):
        result = self.inventory()
        self.assertEqual("PASS", result["status"], result["issues"])
        self.assertEqual(2, result["counts"]["unique_methods"])
        rows = {row["step_id"]: row for row in result["ci_non_sef"]}
        self.assertEqual("MAPPED", rows["ci:tests"]["mapping_status"])
        self.assertEqual(2, len(rows["ci:tests"]["test_methods"]))
        self.assertEqual("COMMAND_ONLY", rows["ci:command"]["mapping_status"])
        self.assertFalse(rows["ci:command"]["test_methods"])
        self.assertTrue(all(item["classification"] == "CURRENT_INVARIANT" for row in result["ser01"] for item in row["test_methods"]))

    def test_omitted_step_fails(self):
        self.steps = [step for step in self.steps if step[0] != "tests"]
        self.assert_issue("CI_NON_SEF_STEP_MISSING:ci:tests")

    def test_extra_step_fails(self):
        self.steps.append(("extra", "unexpected", self.argv))
        self.assert_issue("CI_NON_SEF_STEP_UNEXPECTED:ci:extra")

    def test_replacement_with_same_count_fails_both_identities(self):
        self.steps[1] = ("replacement", "substitute", self.argv)
        result = self.assert_issue("CI_NON_SEF_STEP_MISSING:ci:tests")
        self.assertIn("CI_NON_SEF_STEP_UNEXPECTED:ci:replacement", result["issues"])

    def test_duplicate_step_fails_even_with_nonempty_collection(self):
        self.steps.append(self.steps[1])
        self.assert_issue("CI_NON_SEF_STEP_DUPLICATE:ci:tests")

    def test_duplicate_sef_cannot_hide_behind_exclusion(self):
        self.steps.append(self.steps[0])
        self.assert_issue("CI_SEF_STEP_NOT_UNIQUE")

    def test_non_sef_discovery_empty_fails(self):
        self.steps = self.steps[:1]
        self.assert_issue("CI_NON_SEF_DISCOVERY_EMPTY")

    def test_omitted_se08_step_fails_identity_contract(self):
        self.profile = []
        self.assert_issue("SE08_STEP_MISSING:suite")

    def test_extra_se08_step_fails_identity_contract(self):
        self.profile.append(("extra", self.argv))
        self.assert_issue("SE08_STEP_UNEXPECTED:extra")

    def test_duplicate_ser_group_fails(self):
        self.cfg["ser01_groups"].append(copy.deepcopy(self.cfg["ser01_groups"][0]))
        self.assert_issue("SER01_STEP_DUPLICATE:" + self.cfg["ser01_groups"][0]["group_id"])

    def test_ser_group_omission_cannot_weaken_previous_five_group_guard(self):
        omitted = self.cfg["ser01_groups"].pop()["group_id"]
        self.assert_issue("SER01_STEP_MISSING:" + omitted)

    def test_ser_group_same_count_replacement_is_rejected(self):
        omitted = self.cfg["ser01_groups"][0]["group_id"]
        self.cfg["ser01_groups"][0]["group_id"] = "other"
        result = self.assert_issue("SER01_STEP_MISSING:" + omitted)
        self.assertIn("SER01_STEP_UNEXPECTED:other", result["issues"])

    def test_empty_suite_is_not_coverage(self):
        self.path.write_text("import unittest\n", encoding="utf-8")
        self.assert_issue("METHOD_MAP_INCOMPLETE:ci:tests:EMPTY_METHOD_MAP")

    def test_ast_only_methods_are_not_coverage(self):
        self.path.write_text("class NotATest:\n def test_one(self): pass\n", encoding="utf-8")
        result = self.assert_issue("METHOD_MAP_INCOMPLETE:ci:tests:EMPTY_METHOD_MAP")
        row = next(row for row in result["ci_non_sef"] if row["step_id"] == "ci:tests")
        self.assertIn("AST_TEST_NOT_COLLECTED:tools/tests/test_cases.py::NotATest.test_one", row["collection_errors"])

    def test_partial_collection_cannot_hide_uncollected_ast_method(self):
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write("class NotATest:\n def test_uncollected(self): pass\n")
        result = self.assert_issue("METHOD_MAP_INCOMPLETE:ci:tests:COLLECTION_ERROR")
        row = next(row for row in result["ci_non_sef"] if row["step_id"] == "ci:tests")
        self.assertEqual(2, len(row["test_methods"]))
        self.assertIn("AST_TEST_NOT_COLLECTED:tools/tests/test_cases.py::NotATest.test_uncollected", row["collection_errors"])

    def test_load_tests_filter_cannot_hide_real_test(self):
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write("def load_tests(loader, tests, pattern):\n return unittest.TestSuite([Checks('test_one')])\n")
        self.assert_issue("METHOD_MAP_INCOMPLETE:ci:tests:COLLECTION_ERROR")

    def test_duplicate_test_ids_fail(self):
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write("def load_tests(loader, tests, pattern):\n return unittest.TestSuite([Checks('test_one'), Checks('test_one'), Checks('test_two')])\n")
        self.assert_issue("DUPLICATE_TEST_ID:ci:tests:tools/tests/test_cases.py::Checks.test_one")

    def test_named_unittest_selector_does_not_require_unselected_sibling(self):
        self.steps[1] = ("tests", "one", [sys.executable, "-m", "unittest", "tools.tests.test_cases.Checks.test_one"])
        result = self.inventory()
        self.assertEqual("PASS", result["status"], result["issues"])
        row = next(row for row in result["ci_non_sef"] if row["step_id"] == "ci:tests")
        self.assertEqual(1, len(row["test_methods"]))

    def test_missing_command_target_is_not_valid_command_only(self):
        (self.root / "tools/check.py").unlink()
        self.assert_issue("METHOD_MAP_INCOMPLETE:ci:command:MISSING")

    def test_classification_cannot_be_omitted(self):
        self.cfg["ci_step_policy"]["ci:tests"].pop("classification")
        self.assert_issue("CI_STEP_POLICY_SCHEMA_INVALID:ci:tests")

    def test_command_classification_must_match_command_only_registry(self):
        self.cfg["command_only_steps"] = []
        self.assert_issue("CI_COMMAND_ONLY_POLICY_MISMATCH")

    def test_unknown_command_only_id_is_not_silently_ignored(self):
        self.cfg["command_only_steps"].append("unknown_se08_step")
        self.assert_issue("COMMAND_ONLY_STEP_NOT_OBSERVED:unknown_se08_step")

    def test_malformed_registry_fails_closed(self):
        self.cfg["ci_step_policy"]["ci:tests"]["mapping_mode"] = []
        self.assert_issue("CI_STEP_POLICY_CLASSIFICATION_INVALID:ci:tests")

    def test_old_schema_requires_explicit_migration(self):
        self.cfg["schema_version"] = "SER-PARALLEL-COVERAGE-3"
        self.assert_issue("COVERAGE_REGISTRY_SCHEMA_INVALID")

    def test_invalid_python_is_structured_collection_failure(self):
        self.path.write_text("def invalid(:\n", encoding="utf-8")
        result = self.assert_issue("METHOD_MAP_INCOMPLETE:ci:tests:COLLECTION_ERROR")
        row = next(row for row in result["ci_non_sef"] if row["step_id"] == "ci:tests")
        self.assertIn("AST_COLLECTION_ERROR:SyntaxError", row["collection_errors"])

    def test_duplicate_json_id_is_not_silently_overwritten(self):
        self.registry.write_text('{"schema_version":"ignored","schema_version":"duplicate"}', encoding="utf-8")
        with mock.patch.object(coverage, "REGISTRY", self.registry):
            result = coverage.inventory()
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(["COVERAGE_REGISTRY_UNREADABLE:ValueError"], result["issues"])

    def retired_record(self, successor):
        return {
            "override": {"classification": "HISTORICAL_TEMPORAL", "historical_sha": "a" * 40, "reason": "previous assertion", "successor_ids": [successor]},
            "retirement_sha": "b" * 40, "reason": "explicit renamed invariant", "successor_ids": [successor],
        }

    def test_retired_override_preserved_with_collectible_current_successor(self):
        successor = "tools/tests/test_cases.py::Checks.test_one"
        self.cfg["retired_method_overrides"]["old::Checks.test_previous"] = self.retired_record(successor)
        result = self.inventory()
        self.assertEqual("PASS", result["status"], result["issues"])
        self.assertIn("old::Checks.test_previous", result["retired_temporal_overrides"])

    def test_retired_override_missing_successor_is_not_a_blanket_exemption(self):
        self.cfg["retired_method_overrides"]["old"] = self.retired_record("missing")
        self.assert_issue("RETIRED_SUCCESSOR_NOT_OBSERVED:old:missing")

    def test_retired_override_cannot_hide_still_collected_test(self):
        method = "tools/tests/test_cases.py::Checks.test_one"
        self.cfg["retired_method_overrides"][method] = self.retired_record(method)
        self.assert_issue("RETIRED_OVERRIDE_OBSERVED:" + method)

    def test_unretired_stale_override_still_fails(self):
        self.cfg["method_overrides"]["old"] = self.retired_record("tools/tests/test_cases.py::Checks.test_one")["override"]
        self.assert_issue("TEMPORAL_OVERRIDE_NOT_OBSERVED:old")

    def replaced_assertion_record(self, method):
        record = self.retired_record(method)
        with mock.patch.object(coverage, "ROOT", self.root):
            digest = coverage.method_ast_digest(method)
        return {**record, "retirement_kind": "assertions_replaced", "historical_method_ast_sha256": "c" * 64, "current_method_ast_sha256": digest}

    def test_same_id_updated_assertion_is_current_not_historical(self):
        method = "tools/tests/test_cases.py::Checks.test_one"
        self.cfg["retired_method_overrides"][method] = self.replaced_assertion_record(method)
        result = self.inventory()
        self.assertEqual("PASS", result["status"], result["issues"])
        found = [item for row in result["se08"] for item in row["test_methods"] if item["test_id"] == method]
        self.assertEqual([{"test_id": method, "classification": "CURRENT_INVARIANT"}], found)
        self.assertEqual("HISTORICAL_TEMPORAL", result["retired_temporal_overrides"][method]["override"]["classification"])

    def test_same_id_current_assertion_drift_is_detected(self):
        method = "tools/tests/test_cases.py::Checks.test_one"
        self.cfg["retired_method_overrides"][method] = self.replaced_assertion_record(method)
        self.path.write_text(self.path.read_text().replace("def test_one(self): pass", "def test_one(self): self.assertTrue(True)"), encoding="utf-8")
        self.assert_issue("RETIRED_OVERRIDE_CURRENT_AST_MISMATCH:" + method)

    def test_same_id_retirement_requires_hashes_and_successor(self):
        method = "tools/tests/test_cases.py::Checks.test_one"
        record = self.replaced_assertion_record(method)
        record["current_method_ast_sha256"] = "not-a-hash"
        self.cfg["retired_method_overrides"][method] = record
        self.assert_issue("RETIRED_OVERRIDE_AST_HASH_INVALID:" + method + ":current_method_ast_sha256")
        record["current_method_ast_sha256"] = "a" * 64
        record["successor_ids"] = ["different"]
        self.assert_issue("RETIRED_OVERRIDE_SAME_ID_SUCCESSOR_REQUIRED:" + method)

    def test_assertion_ast_ignores_comments_but_not_semantics(self):
        method = "tools/tests/test_cases.py::Checks.test_one"
        with mock.patch.object(coverage, "ROOT", self.root):
            original = coverage.method_ast_digest(method)
            self.path.write_text("# harmless location change\n" + self.path.read_text(), encoding="utf-8")
            self.assertEqual(original, coverage.method_ast_digest(method))



if __name__=="__main__": unittest.main()
