#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Certificação prospectiva da promoção SER01 L2→L3.

Executa somente após a policy declarar L3. Preserva SE07/SE08 como canais
históricos: seus assertions temporais L2 são observados, não reescritos.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = ROOT / "ambiente_fonte" / ".assistant"
POLICY = ASSISTANT / "hub_padroes/skill_enforcement/policy.json"
SKILL = "hub-ml-criar-objeto"
SURFACE = "object_validation"
PROFILE = "ser01-object-validation-post-promotion"
VERSION = "SER-PROMOTION-CERT-1"
ID_PREFIX = "serprom1:"
BRANCH = "ser/SER01-criar-objeto-l3"

def _load(name: str, path: Path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError("MODULE_LOAD_FAILED")
    mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod
    try: spec.loader.exec_module(mod); return mod
    finally: sys.modules.pop(name,None)

ser=_load("_ser_promotion_base", ROOT/"tools/skill_enforcement/ser_certify.py")

def _json_bytes(v:Any)->bytes:
    return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")
def _digest(v:Any)->str: return hashlib.sha256(_json_bytes(v)).hexdigest()
def _write(path:Path,v:Any): path.write_bytes(_json_bytes(v)+b"\n")
def _seal(v:dict[str,Any])->dict[str,Any]:
    v.pop("certification_id",None); v["certification_id"]=ID_PREFIX+_digest(v); return v

def _policy_entry()->Mapping[str,Any]:
    raw=json.loads(POLICY.read_text(encoding="utf-8"))
    return next(x for x in raw["skills"] if x["skill"]==SKILL)

def _promotion_gate()->dict[str,Any]:
    p=_policy_entry(); issues=[]
    required={
      f"skills/{SKILL}/SKILL.md",
      f"skills/{SKILL}/execution_contract.json",
      f"skills/{SKILL}/scripts/preflight.py",
      f"skills/{SKILL}/scripts/run.py",
      f"skills/{SKILL}/scripts/object_validation.py",
      f"skills/{SKILL}/release_manifest.json",
    }
    if p.get("current_level")!="L3" or p.get("target_level")!="L3":
        issues.append("POLICY_LEVEL_NOT_L3")
    if p.get("policy_status")!="implemented": issues.append("POLICY_STATUS_NOT_IMPLEMENTED")
    if p.get("rollout_mode")!="audit" or p.get("scope_mode")!="stage_specific":
        issues.append("POLICY_MODE_OR_SCOPE_CHANGED")
    if not required <= set(p.get("implemented_artifacts") or []):
        issues.append("IMPLEMENTED_ARTIFACTS_INCOMPLETE")
    surfaces={x.get("id"):x for x in p.get("protected_surfaces",[]) if isinstance(x,Mapping)}
    ov=surfaces.get(SURFACE)
    if not isinstance(ov,Mapping) or ov.get("level")!="L3" or ov.get("evidence")!="receipt":
        issues.append("OBJECT_VALIDATION_SURFACE_INVALID")
    for rel in required:
        if not (ASSISTANT/rel).is_file(): issues.append("REQUIRED_ARTIFACT_MISSING:"+rel)
    return {"status":"PASS" if not issues else "FAIL","issues":issues,
            "current_level":p.get("current_level"),"target_level":p.get("target_level"),
            "policy_status":p.get("policy_status"),"rollout_mode":p.get("rollout_mode")}

def _historical_result(name:str, code:int, output:str, expected:set[str])->dict[str,Any]:
    observed=set(re.findall(r"FAIL: (test_[A-Za-z0-9_]+)",output))
    unexpected=sorted(observed-expected); missing=sorted(expected-observed)
    ok=code==1 and not unexpected and not missing
    return {"name":name,"status":"EXPECTED_TEMPORAL_FAIL" if ok else "UNEXPECTED_RESULT",
            "exit_code":code,"expected_failures":sorted(expected),
            "observed_failures":sorted(observed),"unexpected":unexpected,"missing":missing}

def verify_certification(payload:Any,*,expected_head:str|None=None)->dict[str,Any]:
    issues=[]
    if not isinstance(payload,Mapping): return {"valid":False,"issues":["NOT_MAPPING"]}
    body={k:copy.deepcopy(v) for k,v in payload.items() if k!="certification_id"}
    if payload.get("certification_id")!=ID_PREFIX+_digest(body): issues.append("ID_MISMATCH")
    if payload.get("version")!=VERSION or payload.get("profile")!=PROFILE: issues.append("IDENTITY_MISMATCH")
    if payload.get("status")!="PASS" or payload.get("issues")!=[]: issues.append("NOT_CLEAN_PASS")
    if (payload.get("promotion_gate") or {}).get("status")!="PASS": issues.append("PROMOTION_GATE")
    if (payload.get("evidence_gate") or {}).get("status")!="PASS": issues.append("EVIDENCE_GATE")
    before,after=payload.get("git_before"),payload.get("git_after")
    if not isinstance(before,Mapping) or before!=after: issues.append("GIT_DRIFT")
    elif expected_head and before.get("head")!=expected_head: issues.append("HEAD_MISMATCH")
    claims=payload.get("claims")
    if claims!={"skill":SKILL,"current_level":"L3","target_level":"L3",
               "rollout_mode":"audit","merge_authorized":False,
               "human_authority_authenticated":False}:
        issues.append("CLAIMS_INVALID")
    hist=payload.get("historical_channels")
    if not isinstance(hist,list) or len(hist)!=2 or any(x.get("status")!="EXPECTED_TEMPORAL_FAIL" for x in hist if isinstance(x,Mapping)):
        issues.append("HISTORICAL_CHANNEL_INVALID")
    required={"ser01_object_validation","contracts","policy","assistant","renderer","render_diff","readme_snapshot",
              *(f"git_{phase}_{component}" for phase in ("before","after") for component in ser.GIT_STATE_COMPONENTS)}
    steps=payload.get("steps")
    if not isinstance(steps,list) or any(not isinstance(x,Mapping) for x in steps):
        issues.append("STEPS_INVALID")
    else:
        names=[x.get("name") for x in steps]
        material=[x for x in steps if x.get("name") in required]
        if len(names)!=len(set(names)) or not required<=set(names) or any(x.get("exit_code")!=0 for x in material):
            issues.append("STEPS_INVALID")
    return {"valid":not issues,"issues":issues,"verification_scope":"SER_POLICY_PROMOTION_CERTIFICATION"}

def main(argv=None)->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--profile",required=True,choices=[PROFILE])
    ap.add_argument("--evidence-dir",required=True,type=Path); ap.add_argument("--evidence-authorized",action="store_true")
    a=ap.parse_args(argv)
    evidence=ser._reserve_evidence(a.evidence_dir,a.evidence_authorized)
    runner=ser._process_runner(); runner.REPO_ROOT=ROOT; steps=[]
    summary={"version":VERSION,"profile":PROFILE,"run_id":uuid.uuid4().hex,
             "started_at_utc":datetime.now(timezone.utc).isoformat(),"status":"BLOCKED","issues":[],
             "steps":steps,"promotion_gate":None,"evidence_gate":None,"historical_channels":[],
             "git_before":None,"git_after":None,
             "claims":{"skill":SKILL,"current_level":"L3","target_level":"L3","rollout_mode":"audit",
                       "merge_authorized":False,"human_authority_authenticated":False}}
    try:
        summary["git_before"]=ser._git_state(runner,evidence,steps,phase="before")
        st=summary["git_before"]
        if st["branch"]!=BRANCH or st["status"]!="" or st["shallow"]!="false" or st["behind"]!=0 or st["merge_base"]!=st["origin_main"]:
            raise ValueError("GIT_PRECONDITION_FAILED")
        pg=_promotion_gate(); summary["promotion_gate"]=pg
        if pg["status"]!="PASS": raise ValueError("PROMOTION_GATE_FAILED")
        integ=evidence/"integration"
        ser._run_step(runner,evidence,steps,"ser01_object_validation",
            [sys.executable,"-B","-m","unittest","tools.tests.test_ser01_object_validation","-v","-f"],
            env={"SER01_RUN_REPO_INTEGRATION":"1","SER01_EVIDENCE_ROOT":str(integ)})
        eg=ser._evidence_gate(integ,st["head"]); summary["evidence_gate"]=eg; _write(evidence/"route_evidence.json",eg)
        if eg["status"]!="PASS": raise ser.GateFailed("EVIDENCE_GATE_FAILED")
        ser._run_step(runner,evidence,steps,"contracts",[sys.executable,"-B","tools/skill_enforcement/validate_contracts.py"])
        ser._run_step(runner,evidence,steps,"policy",[sys.executable,"-B","tools/skill_enforcement/se07_policy.py"])
        ser._run_step(runner,evidence,steps,"assistant",[sys.executable,"-B","tools/validate_assistant.py"])
        ser._run_step(runner,evidence,steps,"renderer",[sys.executable,"-B","tools/render_simulado.py","--write"])
        _,drift=ser._run_step(runner,evidence,steps,"render_diff",["git","status","--porcelain","--untracked-files=all","--","Novo_Ambiente_Simulado"])
        if drift.strip(): raise ser.GateFailed("DERIVED_STALE")
        ser._run_step(runner,evidence,steps,"readme_snapshot",[sys.executable,"-B","tools/validate_assistant.py","--conferir-readme"])
        for name,module,expected in (
            ("historical_se07","tools.tests.test_skill_enforcement_se07",
             {"test_current_level_is_evidence_based","test_runtime_resolver"}),
            ("historical_se08","tools.tests.test_skill_enforcement_se08",
             {"test_create_object_global_level_is_not_promoted_by_se08"}),
        ):
            code,out=ser._run_step(runner,evidence,steps,name,[sys.executable,"-B","-m","unittest",module,"-v"],require_zero=False)
            hr=_historical_result(name,code,out,expected); summary["historical_channels"].append(hr)
            if hr["status"]!="EXPECTED_TEMPORAL_FAIL": raise ser.GateFailed(name+":UNEXPECTED_HISTORICAL_RESULT")
        summary["git_after"]=ser._git_state(runner,evidence,steps,phase="after")
        if summary["git_after"]!=summary["git_before"]: raise ser.GateFailed("GIT_DRIFT")
        summary["status"]="PASS"
    except (ValueError,OSError,ser.GateFailed,KeyboardInterrupt,SystemExit) as exc:
        summary["status"]="FAIL"; summary["issues"].append(type(exc).__name__+":"+str(exc))
    summary["ended_at_utc"]=datetime.now(timezone.utc).isoformat(); _seal(summary)
    if summary["status"]=="PASS":
        checked=verify_certification(summary,expected_head=(summary["git_before"] or {}).get("head"))
        if not checked["valid"]:
            summary["status"]="FAIL"; summary["issues"].append("SELF_VERIFY:"+",".join(checked["issues"])); _seal(summary)
    _write(evidence/"summary.json",summary); print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
    return 0 if summary["status"]=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
