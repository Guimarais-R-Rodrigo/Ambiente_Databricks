from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from tools.skill_enforcement.parallel import bundle, contract, coverage, registry, scheduler, verifier
from tools.skill_enforcement.parallel import pilot_verify


def task(task_id="task.a", deps=None, key="k", role="executor", resource="light"):
    return {
        "task_schema": contract.TASK_SCHEMA_VERSION,
        "task_id": task_id,
        "role": role,
        "stage": "B0.6",
        "skill": "synthetic",
        "candidate_sha": "a" * 40,
        "command_ids": ["b0:pilot:pass"],
        "depends_on": deps or [],
        "read_roots": ["tools"],
        "write_roots": [],
        "protected_paths": ["ambiente_fonte"],
        "resource_class": resource,
        "exclusivity_key": key,
        "required": True,
        "expected_effect": "NONE",
    }


def campaign(tasks=None):
    return {
        "schema_version": contract.CAMPAIGN_SCHEMA_VERSION,
        "campaign_id": "SER-B0-TEST",
        "baseline_sha": "b" * 40,
        "candidate_sha": "a" * 40,
        "state": "PLANNED",
        "max_parallel": 2,
        "max_auditors": 1,
        "resource_limits": {"light": 2, "audit": 1},
        "tasks": tasks or [task()],
        "command_registry_digest": "1" * 64,
        "coverage_digest": "2" * 64,
        "policy_before_digest": "3" * 64,
        "human_gates": ["B0_RELEASE"],
        "external_gates": [],
    }


def result(task_id="task.a", status="PASS", exit_code=0):
    return {
        "result_schema": contract.RESULT_SCHEMA_VERSION,
        "task_id": task_id,
        "candidate_sha": "a" * 40,
        "status": status,
        "effect_state": "NONE",
        "command_records": [] if status.startswith("BLOCKED") else [{"exit_code": exit_code}],
        "first_failure": None,
        "started_at_utc": "2026-09-24T00:00:00Z",
        "ended_at_utc": "2026-09-24T00:00:01Z",
        "protected_fingerprint_before": "4" * 64,
        "protected_fingerprint_after": "4" * 64,
        "issues": [],
    }


class ContractTests(unittest.TestCase):
    def test_valid_task(self): self.assertEqual([], contract.validate_task(task()))
    def test_unknown_task_key_rejected(self):
        x=task(); x["surprise"]=1; self.assertIn("TASK:UNKNOWN:surprise", contract.validate_task(x))
    def test_task_sha_rejected(self):
        x=task(); x["candidate_sha"]="abc"; self.assertIn("TASK_CANDIDATE_SHA_INVALID", contract.validate_task(x))
    def test_task_role_rejected(self):
        x=task(); x["role"]="architect"; self.assertIn("TASK_ROLE_INVALID", contract.validate_task(x))
    def test_task_read_write_overlap_rejected(self):
        x=task(); x["write_roots"]=["tools"]; self.assertIn("TASK_READ_WRITE_ROOT_OVERLAP", contract.validate_task(x))
    def test_task_protected_write_overlap_rejected(self):
        x=task(); x["write_roots"]=["ambiente_fonte"]; self.assertIn("TASK_PROTECTED_WRITE_OVERLAP", contract.validate_task(x))
    def test_task_path_traversal_rejected(self):
        x=task(); x["read_roots"]=["../outside"]; self.assertTrue(any("UNSAFE" in issue for issue in contract.validate_task(x)))
    def test_task_absolute_path_rejected(self):
        x=task(); x["protected_paths"]=["/tmp"]; self.assertTrue(any("UNSAFE" in issue for issue in contract.validate_task(x)))
    def test_valid_campaign(self): self.assertEqual([], contract.validate_campaign(campaign()))
    def test_campaign_duplicate_task_id_rejected(self):
        self.assertIn("CAMPAIGN_TASK_ID_DUPLICATE", contract.validate_campaign(campaign([task(),task()])))
    def test_campaign_unknown_dependency_rejected(self):
        issues=contract.validate_campaign(campaign([task("aaa",["missing"]) ])); self.assertTrue(any(x.startswith("CAMPAIGN_DEPENDENCY_UNKNOWN") for x in issues))
    def test_campaign_self_dependency_rejected(self):
        issues=contract.validate_campaign(campaign([task("aaa",["aaa"]) ])); self.assertTrue(any(x.startswith("CAMPAIGN_SELF_DEPENDENCY") for x in issues))
    def test_campaign_parallel_limit_rejected(self):
        x=campaign(); x["max_parallel"]=99; self.assertIn("CAMPAIGN_MAX_PARALLEL_INVALID", contract.validate_campaign(x))
    def test_campaign_resource_limit_rejected(self):
        x=campaign(); x["resource_limits"]={"gpu":99}; self.assertTrue(any(i.startswith("CAMPAIGN_RESOURCE_LIMIT_INVALID") for i in contract.validate_campaign(x)))
    def test_valid_result(self): self.assertEqual([], contract.validate_result(result()))
    def test_result_unknown_status_rejected(self):
        x=result(); x["status"]="GREEN"; self.assertIn("RESULT_STATUS_INVALID", contract.validate_result(x))
    def test_digest_is_stable(self): self.assertEqual(contract.digest_json({"b":2,"a":1}),contract.digest_json({"a":1,"b":2}))


class RegistryTests(unittest.TestCase):
    def test_registry_loads(self): self.assertIn("b0:pilot:pass", registry.load_registry()["commands"])
    def test_python_placeholder_resolves_current_interpreter(self):
        self.assertEqual(sys.executable, registry.resolve_command("b0:pilot:pass")[0])
    def test_unknown_command_rejected(self):
        with self.assertRaises(registry.RegistryError): registry.resolve_command("missing")
    def test_shell_registry_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"r.json"
            p.write_text(json.dumps({"schema_version":"SER-PARALLEL-COMMANDS-1","commands":[{"command_id":"x","argv":["bash","-c","echo x"]}]}))
            with self.assertRaises(registry.RegistryError): registry.load_registry(p)


class SchedulerTests(unittest.TestCase):
    def test_acyclic(self): self.assertFalse(scheduler.detect_cycle([task("aaa"),task("bbb",["aaa"],"k2")]))
    def test_cycle_detected(self): self.assertTrue(scheduler.detect_cycle([task("aaa",["bbb"]),task("bbb",["aaa"],"k2")]))
    def test_ready_respects_dependencies(self):
        d=scheduler.decide([task("aaa"),task("bbb",["aaa"],"k2")],{},limit=2); self.assertEqual(("aaa",),d.ready)
    def test_failed_dependency_blocks_only_dependent(self):
        d=scheduler.decide([task("aaa"),task("bbb",["aaa"],"k2"),task("ccc",[],"k3")],{"aaa":"FAIL"},limit=2)
        self.assertIn("bbb",d.blocked_dependency); self.assertIn("ccc",d.ready)
    def test_exclusivity_key_serializes(self):
        d=scheduler.decide([task("aaa",[],"same"),task("bbb",[],"same")],{},limit=2); self.assertEqual(1,len(d.ready))
    def test_second_order_dependency_can_be_recomputed_after_block(self):
        tasks=[task("aaa"),task("bbb",["aaa"],"k2"),task("ccc",["bbb"],"k3")]
        first=scheduler.decide(tasks,{"aaa":"FAIL"},limit=2)
        self.assertEqual(("bbb",),first.blocked_dependency)
        second=scheduler.decide(tasks,{"aaa":"FAIL","bbb":"BLOCKED_DEPENDENCY"},limit=2)
        self.assertEqual(("ccc",),second.blocked_dependency)
    def test_resource_limit_serializes(self):
        d=scheduler.decide([task("aaa",[],"k1",resource="cpu"),task("bbb",[],"k2",resource="cpu")],{},limit=2,resource_limits={"cpu":1})
        self.assertEqual(1,len(d.ready))
    def test_auditor_limit_is_separate(self):
        d=scheduler.decide([
            task("aaa",[],"k1",role="domain_auditor",resource="audit"),
            task("bbb",[],"k2",role="evidence_auditor",resource="audit"),
            task("ccc",[],"k3",role="executor",resource="light"),
        ],{},limit=3,auditor_limit=1,resource_limits={"audit":2,"light":2})
        self.assertEqual(2,len(d.ready))
        self.assertIn("ccc",d.ready)


class VerifierTests(unittest.TestCase):
    def test_valid_campaign_run(self): self.assertTrue(verifier.verify_campaign_run(campaign(),{"task.a":result()})["valid"])
    def test_result_set_mismatch(self): self.assertIn("RESULT_SET_MISMATCH",verifier.verify_campaign_run(campaign(),{})["issues"])
    def test_candidate_binding_mismatch(self):
        r=result(); r["candidate_sha"]="c"*40
        self.assertTrue(any("CANDIDATE_BINDING_MISMATCH" in x for x in verifier.verify_campaign_run(campaign(),{"task.a":r})["issues"]))
    def test_protected_mutation_rejected(self):
        r=result(); r["protected_fingerprint_after"]="5"*64
        self.assertTrue(any("PROTECTED_PATH_MUTATED" in x for x in verifier.verify_campaign_run(campaign(),{"task.a":r})["issues"]))
    def test_pass_nonzero_rejected(self):
        self.assertTrue(any("PASS_WITH_NONZERO_COMMAND" in x for x in verifier.verify_campaign_run(campaign(),{"task.a":result(exit_code=1)})["issues"]))
    def test_blocked_by_exactness(self):
        c=campaign([task("aaa"),task("bbb",["aaa"],"k2")])
        ra=result("aaa",status="FAIL",exit_code=1)
        rb=result("bbb",status="BLOCKED_DEPENDENCY"); rb["blocked_by"]=[]
        self.assertTrue(any("BLOCKED_BY_MISMATCH" in x for x in verifier.verify_campaign_run(c,{"aaa":ra,"bbb":rb})["issues"]))
    def test_bundle_detects_hash_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/"a.txt").write_text("a"); bundle.write_manifest(root); (root/"a.txt").write_text("b")
            self.assertIn("HASH_MISMATCH:a.txt",verifier.verify_bundle(root)["issues"])


class BundleTests(unittest.TestCase):
    def test_raw_share_identity_is_distinct(self): self.assertTrue(bundle.raw_share_binding(b"raw",b"share")["identities_are_distinct"])
    def test_secret_scan(self): self.assertTrue(bundle.scan_text("Bearer abcdefghijklmnopqrstuvwxyz"))
    def test_clean_scan(self): self.assertEqual([],bundle.scan_text("safe placeholder"))
    def test_manifest_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/"a.txt").write_text("a"); bundle.write_manifest(root)
            self.assertTrue(verifier.verify_bundle(root)["valid"])


class CoverageTests(unittest.TestCase):
    def test_test_methods_parser(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"t.py"; p.write_text("import unittest\nclass X(unittest.TestCase):\n def test_a(self): pass\n")
            self.assertEqual(["X.test_a"],coverage.test_methods(p))
    def test_registry_declares_21_se08_policies(self):
        cfg=json.loads(coverage.REGISTRY.read_text()); self.assertEqual(21,len(cfg["step_policy"]))


class PilotVerifierTests(unittest.TestCase):
    def test_expected_deliberate_failure_is_mechanism_pass(self):
        summary={"first_failure":"pilot.beta.fail","results":{
            "pilot.alpha.pass":{"status":"PASS"},
            "pilot.beta.fail":{"status":"FAIL"},
            "pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"]},
            "pilot.publication.blocked":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.dependent"]},
        }}
        self.assertTrue(pilot_verify.verify(summary)["valid"])
    def test_publication_not_blocked_is_rejected(self):
        summary={"first_failure":"pilot.beta.fail","results":{
            "pilot.alpha.pass":{"status":"PASS"},
            "pilot.beta.fail":{"status":"FAIL"},
            "pilot.beta.dependent":{"status":"BLOCKED_DEPENDENCY","blocked_by":["pilot.beta.fail"]},
            "pilot.publication.blocked":{"status":"PASS","blocked_by":[]},
        }}
        self.assertFalse(pilot_verify.verify(summary)["valid"])


if __name__ == "__main__":
    unittest.main()
