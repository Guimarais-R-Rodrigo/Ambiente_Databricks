from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
from .evidence import reserve_evidence,write_manifest
from .git_state import git_state
from .manifest import load_campaign,load_registry,validate_authorization
from .scheduler import run_dag
from .util import sha256_file,write_json_atomic,read_json
from .verify import verify_run

def execute(repo:Path,campaign_path:Path,registry_path:Path,evidence_dir:Path,authorized:bool,authorization_path:Path|None=None)->dict:
    commands,reg_raw=load_registry(registry_path); tasks,camp=load_campaign(campaign_path,reg_raw)
    material=[spec for spec in commands.values() if spec.effect_class!="read_only" and any(t.command_id==spec.command_id for t in tasks.values())]
    if material:
        if authorization_path is None: raise RuntimeError("MATERIAL_EFFECT_AUTHORIZATION_REQUIRED")
        auth=read_json(authorization_path); auth_issues=validate_authorization(auth,camp,commands)
        if auth_issues: raise RuntimeError("AUTHORIZATION_INVALID:"+";".join(auth_issues))
    ev=reserve_evidence(evidence_dir,repo,authorized)
    before=git_state(repo)
    if before['head']!=camp['candidate_sha'] or before['tree']!=camp['candidate_tree'] or before['status']:
        raise RuntimeError('CANDIDATE_IDENTITY_PRECONDITION_FAILED')
    if before['origin_main']!=camp['baseline_sha'] or before['merge_base']!=camp['baseline_sha'] or before['behind']!=0 or before['shallow']!='false':
        raise RuntimeError('BASELINE_PRECONDITION_FAILED')
    identity={"engine_version":"SER-PARALLEL-ENGINE-1","campaign_sha256":sha256_file(campaign_path),"registry_sha256":sha256_file(registry_path),"git_before":before,"started_at_utc":datetime.now(timezone.utc).isoformat()}
    write_json_atomic(ev/'identity.json',identity)
    results=run_dag(repo,ev,tasks,commands,camp['limits']['max_parallel'],camp['limits']['stop_policy'])
    after=git_state(repo); identity['git_after']=after; identity['ended_at_utc']=datetime.now(timezone.utc).isoformat(); write_json_atomic(ev/'identity.json',identity)
    if before!=after: # exact identity in certification; diagnose may still preserve output as FAIL
        pass
    verification=verify_run(camp,ev); write_json_atomic(ev/'verification.json',verification)
    summary={"summary_version":"SER-PARALLEL-SUMMARY-1","campaign_id":camp['campaign_id'],"round_id":camp['round_id'],"mode":camp['mode'],"status":"PASS" if verification['campaign_pass'] and before==after else "FAIL","first_failure":verification['first_failure'],"task_statuses":verification['task_statuses'],"git_identity_preserved":before==after,"policy_promotion_authorized":False,"merge_authorized":False}
    write_json_atomic(ev/'summary.json',summary); write_manifest(ev)
    return summary
