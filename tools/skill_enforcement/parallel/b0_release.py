from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping

from .bundle import build_share, write_manifest
from .pilot_verify import verify as verify_pilot
from .prepare_pilot import prepare
from .process import ROOT, run_argv
from .registry import resolve_command
from .host_qualification import qualify as qualify_host
from .round_identity import assert_release_spec_current, assert_round_start_current, build_release_spec, capture_round_start, release_spec_digest
from .verifier import verify_campaign_run, verify_raw_share_binding

def _json_bytes(value): return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode("utf-8")
def _gate_ok(row:Mapping[str,Any],expected_exit:int):
 return row.get("command_started") is True and type(row.get("exit_code")) is int and row.get("exit_code")==expected_exit and row.get("timed_out") is False and row.get("cleanup") in {"COMPLETE","COMPLETE_ALREADY_EXITED"} and row.get("residual_descendants_detected") is False
def _run_registry_gate(output_dir,command_id,name,expected_exit=0):
 argv,timeout=resolve_command(command_id); gate_dir=output_dir/"release_gates"; row=run_argv(argv,gate_dir,name,timeout=timeout); return row,gate_dir/f"{name}.stdout.txt"
def _run_argv_gate(output_dir,argv,name,timeout,expected_exit):
 gate_dir=output_dir/"release_gates"; row=run_argv(argv,gate_dir,name,timeout=timeout); return row,gate_dir/f"{name}.stdout.txt"
def _run_sandbox_registry_gate(output_dir,command_id,name,probe_target):
 argv,timeout=resolve_command(command_id); gate_dir=output_dir/"release_gates"; row=run_argv(argv,gate_dir,name,timeout=timeout,sandbox=True,sandbox_probe_target=probe_target); return row,gate_dir/f"{name}.stdout.txt"
def _sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def _finish(output_dir,result,*,round_start=None,release_spec=None):
 mechanism_path=output_dir/"MECHANISM_RESULT.json"; mechanism_path.write_bytes(_json_bytes(result)); raw_manifest_path=write_manifest(output_dir)
 share_root=output_dir.parent/f"{output_dir.name}_SHARE"; binding_path=output_dir.parent/f"{output_dir.name}_RAW_SHARE_BINDING.json"; envelope_path=output_dir.parent/f"{output_dir.name}_ENVELOPE_VERIFICATION.json"; verdict_path=output_dir.parent/f"{output_dir.name}_RELEASE_VERDICT.json"
 try:
  build_share(output_dir,share_root,{},binding_path=binding_path); envelope=verify_raw_share_binding(output_dir,share_root,binding_path)
 except Exception as exc: envelope={"valid":False,"issues":[f"EVIDENCE_ENVELOPE_EXCEPTION:{type(exc).__name__}:{exc}"]}
 envelope_path.write_bytes(_json_bytes(envelope))
 final_status="PASS" if result.get("status")=="PASS" and envelope.get("valid") is True else "FAIL"; release_status=result.get("release_status","NOT_QUALIFIED") if final_status=="PASS" else "NOT_QUALIFIED"; identity=release_spec or round_start or {}
 verdict={"schema_version":"SER-B0-RELEASE-VERDICT-1","status":final_status,"release_status":release_status,"first_failure":result.get("first_failure") if final_status=="PASS" else (result.get("first_failure") or "evidence_envelope"),"round_id":identity.get("round_id"),"candidate_sha":identity.get("candidate_sha"),"candidate_tree_sha":identity.get("candidate_tree_sha"),"release_spec_digest":release_spec_digest(release_spec) if release_spec is not None else None,"mechanism_result_sha256":_sha(mechanism_path),"raw_manifest_sha256":_sha(raw_manifest_path),"share_manifest_sha256":_sha(share_root/"MANIFEST.json") if (share_root/"MANIFEST.json").is_file() else None,"binding_sha256":_sha(binding_path) if binding_path.is_file() else None,"envelope_verification_sha256":_sha(envelope_path),"evidence_envelope_valid":envelope.get("valid") is True,"evidence_envelope_issues":envelope.get("issues") or []}
 verdict_path.write_bytes(_json_bytes(verdict)); return verdict
def _fail(output_dir,first_failure,checks,*,round_start=None,release_spec=None,extra=None):
 result={"status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":first_failure,"checks":checks}
 if extra: result.update(extra)
 return _finish(output_dir,result,round_start=round_start,release_spec=release_spec)
def qualify(output_dir:Path):
 siblings=[output_dir,output_dir.parent/f"{output_dir.name}_SHARE",output_dir.parent/f"{output_dir.name}_RAW_SHARE_BINDING.json",output_dir.parent/f"{output_dir.name}_ENVELOPE_VERIFICATION.json",output_dir.parent/f"{output_dir.name}_RELEASE_VERDICT.json"]
 if any(path.exists() for path in siblings): return {"schema_version":"SER-B0-RELEASE-VERDICT-1","status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":"evidence_destination_not_new"}
 output_dir.mkdir(parents=True,exist_ok=False); checks=[]; release_spec=None
 try: round_start=capture_round_start()
 except Exception as exc:
  round_start={"round_id":None,"candidate_sha":None,"candidate_tree_sha":None}; return _fail(output_dir,"round_start",checks,round_start=round_start,extra={"issues":[f"ROUND_START_EXCEPTION:{type(exc).__name__}:{exc}"]})
 (output_dir/"ROUND_START.json").write_bytes(_json_bytes(round_start))
 pre,_=_run_registry_gate(output_dir,"b0:preflight:authoring","authoring_preflight",0); checks.append({"name":"authoring_preflight","exit_code":pre.get("exit_code"),"valid_process":_gate_ok(pre,0)})
 if not _gate_ok(pre,0): return _fail(output_dir,"authoring_preflight",checks,round_start=round_start)
 identity_issues=assert_round_start_current(round_start)
 if identity_issues: return _fail(output_dir,"round_identity_after_preflight",checks,round_start=round_start,extra={"issues":identity_issues})
 meta,_=_run_registry_gate(output_dir,"b0:meta:tests","metatests",0); checks.append({"name":"metatests","exit_code":meta.get("exit_code"),"valid_process":_gate_ok(meta,0)})
 if not _gate_ok(meta,0): return _fail(output_dir,"metatests",checks,round_start=round_start)
 identity_issues=assert_round_start_current(round_start)
 if identity_issues: return _fail(output_dir,"round_identity_after_metatests",checks,round_start=round_start,extra={"issues":identity_issues})
 cov_row,cov_stdout=_run_registry_gate(output_dir,"b0:coverage:inventory","coverage",0); checks.append({"name":"coverage","exit_code":cov_row.get("exit_code"),"valid_process":_gate_ok(cov_row,0)})
 if not _gate_ok(cov_row,0): return _fail(output_dir,"coverage",checks,round_start=round_start)
 try: coverage=json.loads(cov_stdout.read_text(encoding="utf-8"))
 except Exception as exc: return _fail(output_dir,"coverage_parse",checks,round_start=round_start,extra={"issues":[f"COVERAGE_PARSE:{type(exc).__name__}:{exc}"]})
 if coverage.get("status")!="PASS": return _fail(output_dir,"coverage_status",checks,round_start=round_start,extra={"issues":coverage.get("issues") or []})
 (output_dir/"coverage.json").write_bytes(_json_bytes(coverage))
 identity_issues=assert_round_start_current(round_start)
 if identity_issues: return _fail(output_dir,"round_identity_after_coverage",checks,round_start=round_start,extra={"issues":identity_issues})
 host_row,host_stdout=_run_registry_gate(output_dir,"b0:host:probe","host_probe",0); checks.append({"name":"host_probe","exit_code":host_row.get("exit_code"),"valid_process":_gate_ok(host_row,0)})
 if not _gate_ok(host_row,0): return _fail(output_dir,"host_probe",checks,round_start=round_start)
 try: host=json.loads(host_stdout.read_text(encoding="utf-8"))
 except Exception as exc: return _fail(output_dir,"host_parse",checks,round_start=round_start,extra={"issues":[f"HOST_PARSE:{type(exc).__name__}:{exc}"]})
 (output_dir/"host.json").write_bytes(_json_bytes(host))
 gate_dir=output_dir/"release_gates"; gate_dir.mkdir(parents=True,exist_ok=True); sandbox_target=gate_dir/"sandbox_probe.denied.txt"; sandbox_target.write_bytes(b"UNCHANGED\n"); sandbox_target_before=_sha(sandbox_target)
 sentinel_before=os.environ.get("SER_B0_SECRET_SENTINEL"); os.environ["SER_B0_SECRET_SENTINEL"]="MUST_NOT_REACH_CHILD"
 try: sandbox_row,sandbox_stdout=_run_sandbox_registry_gate(output_dir,"b0:sandbox:probe","sandbox_probe",sandbox_target)
 finally:
  if sentinel_before is None: os.environ.pop("SER_B0_SECRET_SENTINEL",None)
  else: os.environ["SER_B0_SECRET_SENTINEL"]=sentinel_before
 checks.append({"name":"sandbox_probe","exit_code":sandbox_row.get("exit_code"),"valid_process":_gate_ok(sandbox_row,0)})
 if not _gate_ok(sandbox_row,0): return _fail(output_dir,"sandbox_probe",checks,round_start=round_start)
 try: sandbox_probe=json.loads(sandbox_stdout.read_text(encoding="utf-8"))
 except Exception as exc: return _fail(output_dir,"sandbox_probe_parse",checks,round_start=round_start,extra={"issues":[f"SANDBOX_PROBE_PARSE:{type(exc).__name__}:{exc}"]})
 if sandbox_probe.get("status")!="PASS" or _sha(sandbox_target)!=sandbox_target_before: return _fail(output_dir,"sandbox_probe_status",checks,round_start=round_start,extra={"issues":["SANDBOX_NEGATIVE_PROBE_FAILED"]})
 (output_dir/"sandbox_probe.json").write_bytes(_json_bytes(sandbox_probe))
 release_spec=build_release_spec(round_start,coverage,host); release_spec_path=output_dir/"RELEASE_SPEC.json"; release_spec_path.write_bytes(_json_bytes(release_spec))
 current_issues=assert_release_spec_current(release_spec)
 if current_issues: return _fail(output_dir,"release_spec_initial_binding",checks,round_start=round_start,release_spec=release_spec,extra={"issues":current_issues})
 pilot_summaries={}
 for scenario in ("selective","global"):
  current_issues=assert_release_spec_current(release_spec)
  if current_issues: return _fail(output_dir,f"release_spec_before_{scenario}",checks,round_start=round_start,release_spec=release_spec,extra={"issues":current_issues})
  campaign_path=output_dir/f"pilot_{scenario}.prepared.json"
  try: prepare(campaign_path,scenario,release_spec)
  except Exception as exc: return _fail(output_dir,f"pilot_{scenario}_prepare",checks,round_start=round_start,release_spec=release_spec,extra={"issues":[f"PILOT_PREPARE:{type(exc).__name__}:{exc}"]})
  evidence=output_dir/f"pilot_{scenario}_evidence"; launch_argv=[sys.executable,"-B","-m","tools.skill_enforcement.parallel.launcher","--campaign",str(campaign_path),"--release-spec",str(release_spec_path),"--evidence-dir",str(evidence)]
  launch,_=_run_argv_gate(output_dir,launch_argv,f"pilot_{scenario}_launcher",1800,1); checks.append({"name":f"pilot_{scenario}_launcher_expected_1","exit_code":launch.get("exit_code"),"valid_process":_gate_ok(launch,1)})
  if not _gate_ok(launch,1): return _fail(output_dir,f"pilot_{scenario}_launcher",checks,round_start=round_start,release_spec=release_spec)
  summary_path=evidence/"summary.json"
  if not summary_path.is_file(): return _fail(output_dir,f"pilot_{scenario}_summary_missing",checks,round_start=round_start,release_spec=release_spec)
  try: campaign_disk=json.loads(campaign_path.read_text(encoding="utf-8")); summary=json.loads(summary_path.read_text(encoding="utf-8"))
  except Exception as exc: return _fail(output_dir,f"pilot_{scenario}_artifact_parse",checks,round_start=round_start,release_spec=release_spec,extra={"issues":[f"PILOT_PARSE:{type(exc).__name__}:{exc}"]})
  independent=verify_campaign_run(campaign_disk,summary.get("results"),evidence); (output_dir/f"pilot_{scenario}_independent_verification.json").write_bytes(_json_bytes(independent))
  if summary.get("verification")!=independent: return _fail(output_dir,f"pilot_{scenario}_producer_verification_mismatch",checks,round_start=round_start,release_spec=release_spec)
  if summary.get("round_id")!=release_spec["round_id"] or summary.get("release_spec_digest")!=release_spec_digest(release_spec): return _fail(output_dir,f"pilot_{scenario}_round_binding",checks,round_start=round_start,release_spec=release_spec)
  if summary.get("issues") not in (None,[]): return _fail(output_dir,f"pilot_{scenario}_mechanism_issues",checks,round_start=round_start,release_spec=release_spec,extra={"issues":summary.get("issues")})
  pilot_input=dict(summary); pilot_input["verification"]=independent; pilot=verify_pilot(pilot_input,scenario); (output_dir/f"pilot_{scenario}_verification.json").write_bytes(_json_bytes(pilot)); checks.append({"name":f"pilot_{scenario}_verifier","exit_code":0 if pilot.get("valid") else 1})
  if independent.get("valid") is not True or pilot.get("valid") is not True: return _fail(output_dir,f"pilot_{scenario}_verifier",checks,round_start=round_start,release_spec=release_spec,extra={"issues":[*(independent.get("issues") or []),*(pilot.get("issues") or [])]})
  pilot_summaries[scenario]=summary
 current_issues=assert_release_spec_current(release_spec)
 if current_issues: return _fail(output_dir,"release_spec_final_binding",checks,round_start=round_start,release_spec=release_spec,extra={"issues":current_issues})
 host_qualification=qualify_host(ROOT,host,sandbox_probe,pilot_summaries["selective"],pilot_summaries["global"]); (output_dir/"HOST_QUALIFICATION.json").write_bytes(_json_bytes(host_qualification)); checks.append({"name":"host_qualification","exit_code":0 if host_qualification.get("status")=="PASS" else 1})
 release_status="LOCAL_QUALIFIED" if host_qualification.get("status")=="PASS" else "PENDING_HOST_QUALIFICATION"
 return _finish(output_dir,{"status":"PASS","release_status":release_status,"first_failure":None,"checks":checks,"round_id":release_spec["round_id"],"release_spec_digest":release_spec_digest(release_spec),"host":host,"host_qualification":host_qualification,"release_scope":"MECHANISM_QUALIFICATION_ONLY_NO_SKILL_PROMOTION"},round_start=round_start,release_spec=release_spec)
def main():
 p=argparse.ArgumentParser(); p.add_argument("--output-dir",required=True,type=Path); a=p.parse_args()
 try: result=qualify(a.output_dir)
 except Exception as exc: result={"schema_version":"SER-B0-RELEASE-VERDICT-1","status":"FAIL","release_status":"NOT_QUALIFIED","first_failure":"UNHANDLED_RELEASE_EXCEPTION","issues":[f"{type(exc).__name__}:{exc}"]}
 print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result.get("status")=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
