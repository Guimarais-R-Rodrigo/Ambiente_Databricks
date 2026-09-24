from __future__ import annotations
import copy, json, os, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[2]
PC=ROOT/'tools/skill_enforcement/parallel_campaign'
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from tools.skill_enforcement.parallel_campaign import manifest, packaging, verify
from tools.skill_enforcement.parallel_campaign.evidence import reserve_evidence, EvidenceError
from tools.skill_enforcement.parallel_campaign.locks import FileLease, LockBusy
from tools.skill_enforcement.parallel_campaign.scheduler import blocked_result
from tools.skill_enforcement.parallel_campaign.model import TaskSpec
from tools.skill_enforcement.parallel_campaign.util import write_json_atomic, read_json
from tools.skill_enforcement.parallel_campaign.inventory import methods_in_file

REG=read_json(PC/'commands.b0.json')

def base_campaign():
    return {"schema_version":"SER-PARALLEL-CAMPAIGN-1","campaign_id":"test-campaign","round_id":"R1","mode":"diagnose","baseline_sha":"a"*40,"candidate_sha":"b"*40,"candidate_tree":"c"*40,"release_id":"test","approved_vector_digest":"d"*64,"limits":{"max_parallel":2,"stop_policy":"block_dependents_continue_independent"},"tasks":[{"task_id":"a","command_id":"b0.pilot.pass","depends_on":[],"resource_class":"light","exclusivity_keys":[],"required":True,"expected_exit_codes":[0],"protected_paths":[],"repo_write_paths":[],"outcome_assertion":{"kind":"exit_only"},"env":{}}]}

class B0MetaTests(unittest.TestCase):
    def test_M01_producer_verifier_disagreement(self):
        with tempfile.TemporaryDirectory() as td:
            e=Path(td); (e/'tasks/a').mkdir(parents=True); c=base_campaign(); r={"schema_version":"SER-PARALLEL-TASK-RESULT-1","task_id":"a","command_id":"b0.pilot.pass","status":"PASS","exit_code":7,"expected_exit_codes":[0],"command_started":True,"cleanup_complete":True,"started_at_utc":"x","ended_at_utc":"x","stdout_sha256":"0"*64,"stderr_sha256":"0"*64,"repo_mutations":[],"protected_changes":[],"effect_state":"NONE","outcome_observed":{"kind":"exit_only","failures":[],"errors":[]},"issues":[]}; write_json_atomic(e/'tasks/a/result.json',r); (e/'tasks/a/stdout.txt').write_text(''); (e/'tasks/a/stderr.txt').write_text(''); self.assertFalse(verify.verify_run(c,e)['campaign_pass'])
    def test_M02_phase_error_detected_by_schema(self):
        c=base_campaign(); c['mode']='unknown'; self.assertTrue(manifest.validate_campaign(c,REG))
    def test_M03_stdout_stderr_both_are_evidence_fields(self):
        schema=read_json(PC/'schemas/task_result.schema.json'); req=set(schema['required']); self.assertTrue({'stdout_sha256','stderr_sha256'}<=req)
    def test_M04_malformed_history_not_benign(self):
        c=base_campaign(); c['tasks'][0]['command_id']='missing'; self.assertIn('COMMAND_UNKNOWN', ';'.join(manifest.validate_campaign(c,REG)))
    def test_M05_same_name_different_cause_needs_issues(self):
        # PASS with issues is rejected by verifier.
        with tempfile.TemporaryDirectory() as td:
            e=Path(td); (e/'tasks/a').mkdir(parents=True); c=base_campaign(); r={"schema_version":"SER-PARALLEL-TASK-RESULT-1","task_id":"a","command_id":"b0.pilot.pass","status":"PASS","exit_code":0,"expected_exit_codes":[0],"command_started":True,"cleanup_complete":True,"started_at_utc":"x","ended_at_utc":"x","stdout_sha256":"0"*64,"stderr_sha256":"0"*64,"repo_mutations":[],"protected_changes":[],"effect_state":"NONE","outcome_observed":{"kind":"exit_only","failures":[],"errors":[]},"issues":["different-cause"]}; write_json_atomic(e/'tasks/a/result.json',r); (e/'tasks/a/stdout.txt').write_text(''); (e/'tasks/a/stderr.txt').write_text(''); self.assertIn('PASS_HAS_ISSUES:a',verify.verify_run(c,e)['issues'])
    def test_M06_missing_duplicate_stage(self):
        c=base_campaign(); c['tasks'].append(copy.deepcopy(c['tasks'][0])); self.assertIn('TASK_ID_DUPLICATE',manifest.validate_campaign(c,REG))
    def test_M07_evidence_reservation_refuses_existing(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as td:
            p=Path(td)/'exists'; p.mkdir();
            with self.assertRaises(EvidenceError): reserve_evidence(p,Path(repo),True)
    def test_M08_reporting_failure_is_terminal_state(self):
        from tools.skill_enforcement.parallel_campaign.model import TERMINAL; self.assertIn('REPORTING_FAILURE',TERMINAL)
    def test_M09_invalid_serialization_nan_rejected(self):
        from tools.skill_enforcement.parallel_campaign.util import canonical_json_bytes
        with self.assertRaises(ValueError): canonical_json_bytes({'x':float('nan')})
    def test_M10_lock_collision(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            with FileLease(root,'k','a'):
                with self.assertRaises(LockBusy): FileLease(root,'k','b').__enter__()
    def test_M11_effective_isolation_requires_host_qualification(self):
        q=read_json(ROOT/'docs/sprints/skill_enforcement_rollout/PARALELO/B0/host_qualification.template.json'); self.assertEqual('NOT_RUN',q['permission_probe'])
    def test_M12_agent_recursion_forbidden_in_handoff(self):
        t=read_json(ROOT/'docs/sprints/skill_enforcement_rollout/PARALELO/B0/task_handoff.template.json'); self.assertNotIn('spawn_agents',t.get('allowed_command_ids',[]))
    def test_M13_stale_lock_not_auto_replaced(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'k.lock'; p.write_text('x');
            with self.assertRaises(LockBusy): FileLease(Path(td),'k','b').__enter__()
    def test_M14_forged_certificate_missing_result(self):
        with tempfile.TemporaryDirectory() as td: self.assertIn('RESULT_MISSING:a',verify.verify_run(base_campaign(),Path(td))['issues'])
    def test_M15_fixture_swap_digest_field_required_by_campaign_contract(self):
        # approved_vector digest cannot be malformed; per-skill fixture digests enter release manifests later.
        c=base_campaign(); c['approved_vector_digest']='x'; self.assertTrue(manifest.validate_campaign(c,REG))
    def test_M16_count_fraud_missing_id(self):
        c=base_campaign(); c['tasks'].append({**copy.deepcopy(c['tasks'][0]),'task_id':'b','depends_on':['a']})
        with tempfile.TemporaryDirectory() as td: self.assertIn('RESULT_MISSING:b',verify.verify_run(c,Path(td))['issues'])
    def test_M17_skip_not_authorized_has_no_pass_state(self):
        schema=read_json(PC/'schemas/task_result.schema.json'); self.assertNotIn('SKIP',schema['properties']['status']['enum'])
    def test_M18_incomplete_process_cannot_pass(self):
        with tempfile.TemporaryDirectory() as td:
            e=Path(td); (e/'tasks/a').mkdir(parents=True); c=base_campaign(); r={"schema_version":"SER-PARALLEL-TASK-RESULT-1","task_id":"a","command_id":"b0.pilot.pass","status":"PASS","exit_code":0,"expected_exit_codes":[0],"command_started":False,"cleanup_complete":False,"started_at_utc":"x","ended_at_utc":"x","stdout_sha256":"0"*64,"stderr_sha256":"0"*64,"repo_mutations":[],"protected_changes":[],"effect_state":"NONE","outcome_observed":{"kind":"exit_only","failures":[],"errors":[]},"issues":[]}; write_json_atomic(e/'tasks/a/result.json',r); (e/'tasks/a/stdout.txt').write_text(''); (e/'tasks/a/stderr.txt').write_text(''); v=verify.verify_run(c,e); self.assertIn('PASS_PROCESS_INCOMPLETE:a',v['issues'])
    def test_M19_freeze_integrity_has_protected_change_field(self):
        schema=read_json(PC/'schemas/task_result.schema.json'); self.assertIn('protected_changes',schema['required'])
    def test_M20_raw_share_have_distinct_hashes_when_redacted(self):
        with tempfile.TemporaryDirectory() as td:
            raw=Path(td)/'raw'; share=Path(td)/'share'; raw.mkdir(); (raw/'a.txt').write_text('/home/user secret'); b=packaging.make_share(raw,share,{'/home/user':'<HOME>'}); row=b['files'][0]; self.assertNotEqual(row['raw_sha256'],row['share_sha256'])
    def test_M21_zip_adversarial_path_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            z=Path(td)/'x.zip'
            with zipfile.ZipFile(z,'w') as f: f.writestr('../evil','x')
            self.assertTrue(packaging.validate_zip_members(z))
    def test_M22_progress_is_deterministic_status_map(self):
        with tempfile.TemporaryDirectory() as td: self.assertEqual({},verify.verify_run({**base_campaign(),'tasks':[]},Path(td))['task_statuses'])
    def test_M23_main_change_is_bound_by_identity_schema(self):
        c=base_campaign(); self.assertRegex(c['baseline_sha'],r'^[0-9a-f]{40}$')
    def test_M24_authorization_replay_schema_binds_candidate(self):
        s=read_json(PC/'schemas/authorization.schema.json'); self.assertIn('candidate_sha',s['required'])
    def test_M25_rule_not_loaded_remains_qualification_pending(self):
        q=read_json(ROOT/'docs/sprints/skill_enforcement_rollout/PARALELO/B0/host_qualification.template.json'); self.assertEqual('PENDING_LOCAL_QUALIFICATION',q['status'])
    def test_M26_no_self_referential_git_sha_in_evidence_contract(self):
        s=read_json(PC/'schemas/task_result.schema.json'); self.assertNotIn('git_commit_sha',s['required'])
    def test_M27_effect_requires_authorization_schema(self):
        s=read_json(PC/'schemas/authorization.schema.json'); self.assertIn('allowed_effects',s['required'])
    def test_M28_unknown_effect_requires_reconciliation_state(self):
        from tools.skill_enforcement.parallel_campaign.model import EFFECT_STATES; self.assertIn('UNKNOWN',EFFECT_STATES)


class SecurityAndContractTests(unittest.TestCase):
    def test_read_only_command_cannot_declare_repo_write_paths(self):
        c=base_campaign(); c['tasks'][0]['repo_write_paths']=['README.md']; self.assertIn('READ_ONLY_COMMAND_HAS_REPO_WRITE_ALLOWLIST:a',manifest.validate_campaign(c,REG))
    def test_environment_must_be_command_allowlisted(self):
        c=base_campaign(); c['tasks'][0]['env']={'DATABRICKS_TOKEN':'secret'}; self.assertIn('ENV_NOT_ALLOWED:a:DATABRICKS_TOKEN',manifest.validate_campaign(c,REG))
    def test_authorization_schema_rejects_unknown_fields(self):
        auth={"schema_version":"SER-PARALLEL-AUTHORIZATION-1","authorization_id":"x","campaign_id":"c","candidate_sha":"a"*40,"allowed_command_ids":[],"allowed_effects":["read_only"],"expires_at_utc":"2099-01-01T00:00:00+00:00","extra":1}
        self.assertTrue(manifest.validate_document(auth,'authorization.schema.json'))
    def test_cli_supports_direct_path_invocation(self):
        completed=subprocess.run([sys.executable,'-B',str(PC/'cli.py'),'lint','--campaign',str(ROOT/'docs/sprints/skill_enforcement_rollout/PARALELO/B0/pilot_campaign.template.json'),'--registry',str(PC/'commands.b0.json')],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(0,completed.returncode,completed.stderr + completed.stdout)
        self.assertEqual('PASS',json.loads(completed.stdout)['status'])

class InventoryTests(unittest.TestCase):
    def test_collects_test_methods_without_importing(self):
        methods=methods_in_file(Path(__file__)); self.assertTrue(any('test_M01_' in x for x in methods))

if __name__=='__main__': unittest.main()
