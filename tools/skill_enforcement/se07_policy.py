#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping
import sys

REPO_ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))
ASSISTANT_ROOT=REPO_ROOT/"ambiente_databricks"/".assistant"
SKILLS_ROOT=ASSISTANT_ROOT/"skills"
DEFAULT_POLICY=ASSISTANT_ROOT/"hub_padroes"/"skill_enforcement"/"policy.json"
LEVELS=("L0","L1","L2","L3","L4")
RISK_CLASSES={"low","medium","high","critical"}
ROLLOUT_MODES={"guidance","audit","warn","enforce"}
POLICY_STATUSES={"defined","implemented"}
EVIDENCE_KINDS={"static","preflight","receipt","postflight","authorization"}

@dataclass(frozen=True)
class PolicyIssue:
    code:str; message:str; location:str
    def to_dict(self)->dict[str,str]: return asdict(self)

def _issue(c,m,l): return PolicyIssue(c,m,l)
def _li(level): return LEVELS.index(level) if level in LEVELS else None
def discover_skills(assistant_root:Path|str=ASSISTANT_ROOT)->set[str]:
    skills_root=Path(assistant_root)/"skills"
    if not skills_root.is_dir(): return set()
    return {p.name for p in skills_root.iterdir() if p.is_dir() and (p/"SKILL.md").is_file() and p.name.startswith("hub-ml-")}

def _required(skill,level):
    out=[f"skills/{skill}/SKILL.md"]; i=_li(level)
    if i is None: return out
    if i>=1: out.append(f"skills/{skill}/execution_contract.json")
    if i>=2: out.append(f"skills/{skill}/scripts/preflight.py")
    if i>=3: out.append(f"skills/{skill}/scripts/run.py")
    if i>=4: out.extend([f"skills/{skill}/scripts/run_enforced.py",f"skills/{skill}/scripts/postflight.py"])
    return out

def _read_policy(path:Path)->tuple[Any,list[PolicyIssue]]:
    try: return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError,UnicodeDecodeError,json.JSONDecodeError) as exc:
        return None, [_issue("POLICY_UNREADABLE",str(exc),"$")]

def validate_policy_registry(policy_path:Path|str=DEFAULT_POLICY, *, assistant_root:Path|str=ASSISTANT_ROOT)->list[PolicyIssue]:
    raw, issues=_read_policy(Path(policy_path))
    return issues or _validate_policy_data(raw, Path(assistant_root))

def _validate_policy_data(raw:Any, assistant_root:Path)->list[PolicyIssue]:
    issues=[]
    if not isinstance(raw,Mapping): return [_issue("POLICY_ROOT","policy registry deve ser objeto","$")]
    if raw.get("schema_version")!="1.0": issues.append(_issue("POLICY_SCHEMA","schema_version deve ser 1.0","schema_version"))
    if raw.get("policy_id")!="SE07-skill-enforcement-policy": issues.append(_issue("POLICY_ID","policy_id inesperado","policy_id"))
    skills=raw.get("skills")
    if not isinstance(skills,list): return issues+[_issue("POLICY_SKILLS","skills deve ser lista","skills")]
    discovered=discover_skills(assistant_root); seen=set()
    for idx,item in enumerate(skills):
        loc=f"skills[{idx}]"
        if not isinstance(item,Mapping): issues.append(_issue("POLICY_SKILL_OBJECT","entrada deve ser objeto",loc)); continue
        skill=item.get("skill")
        if not isinstance(skill,str) or not skill.startswith("hub-ml-"): issues.append(_issue("POLICY_SKILL_NAME",f"skill inválida: {skill!r}",f"{loc}.skill")); continue
        if skill in seen: issues.append(_issue("POLICY_DUPLICATE",f"skill duplicada: {skill}",f"{loc}.skill"))
        seen.add(skill)
        risk,current,target,rollout,status,scope=(item.get(k) for k in ("risk_class","current_level","target_level","rollout_mode","policy_status","scope_mode"))
        ci,ti=_li(current),_li(target)
        if risk not in RISK_CLASSES: issues.append(_issue("POLICY_RISK",f"risk_class inválida: {risk!r}",f"{loc}.risk_class"))
        if ci is None: issues.append(_issue("POLICY_CURRENT_LEVEL",f"current_level inválido: {current!r}",f"{loc}.current_level"))
        if ti is None: issues.append(_issue("POLICY_TARGET_LEVEL",f"target_level inválido: {target!r}",f"{loc}.target_level"))
        if ci is not None and ti is not None and ti<ci: issues.append(_issue("POLICY_LEVEL_ORDER","target_level < current_level",loc))
        if rollout not in ROLLOUT_MODES: issues.append(_issue("POLICY_ROLLOUT",f"rollout_mode inválido: {rollout!r}",f"{loc}.rollout_mode"))
        if status not in POLICY_STATUSES: issues.append(_issue("POLICY_STATUS",f"policy_status inválido: {status!r}",f"{loc}.policy_status"))
        if scope not in {"whole_skill","stage_specific"}: issues.append(_issue("POLICY_SCOPE",f"scope_mode inválido: {scope!r}",f"{loc}.scope_mode"))
        if status=="implemented" and current!=target: issues.append(_issue("POLICY_IMPLEMENTED_LEVEL","implemented exige current_level == target_level",loc))
        if rollout=="enforce" and current!="L4": issues.append(_issue("POLICY_ENFORCE_WITHOUT_L4","enforce exige L4 implementado",loc))
        if risk=="critical" and ti is not None and ti<3: issues.append(_issue("POLICY_CRITICAL_TOO_WEAK","risco critical exige target >= L3",loc))
        artifacts=item.get("implemented_artifacts")
        if not isinstance(artifacts,list) or any(not isinstance(x,str) or not x for x in artifacts): issues.append(_issue("POLICY_ARTIFACTS","implemented_artifacts inválido",f"{loc}.implemented_artifacts")); artifacts=[]
        for rel in artifacts:
            if not (assistant_root/rel).is_file(): issues.append(_issue("POLICY_ARTIFACT_MISSING",f"artefato ausente: {rel}",f"{loc}.implemented_artifacts"))
        if isinstance(current,str) and current in LEVELS:
            for rel in _required(skill,current):
                if not (assistant_root/rel).is_file(): issues.append(_issue("POLICY_CURRENT_LEVEL_UNPROVEN",f"{current} declarado sem {rel}",loc))
        surfaces=item.get("protected_surfaces")
        if not isinstance(surfaces,list) or not surfaces: issues.append(_issue("POLICY_SURFACES","protected_surfaces deve ser lista não vazia",f"{loc}.protected_surfaces")); surfaces=[]
        ids=set()
        for sidx,s in enumerate(surfaces):
            sloc=f"{loc}.protected_surfaces[{sidx}]"
            if not isinstance(s,Mapping): issues.append(_issue("POLICY_SURFACE_OBJECT","surface deve ser objeto",sloc)); continue
            sid,sl,ev,ra=s.get("id"),s.get("level"),s.get("evidence"),s.get("rationale")
            if not isinstance(sid,str) or not sid: issues.append(_issue("POLICY_SURFACE_ID","id inválido",f"{sloc}.id"))
            elif sid in ids: issues.append(_issue("POLICY_SURFACE_DUPLICATE",f"id duplicado: {sid}",f"{sloc}.id"))
            else: ids.add(sid)
            si=_li(sl)
            if si is None: issues.append(_issue("POLICY_SURFACE_LEVEL",f"level inválido: {sl!r}",f"{sloc}.level"))
            elif ti is not None and si>ti: issues.append(_issue("POLICY_SURFACE_ABOVE_TARGET","surface excede target_level",sloc))
            if ev not in EVIDENCE_KINDS: issues.append(_issue("POLICY_SURFACE_EVIDENCE",f"evidence inválida: {ev!r}",f"{sloc}.evidence"))
            if not isinstance(ra,str) or not ra.strip(): issues.append(_issue("POLICY_SURFACE_RATIONALE","rationale ausente",f"{sloc}.rationale"))
        debt=item.get("known_debt")
        if not isinstance(debt,list) or any(not isinstance(x,str) or not x for x in debt): issues.append(_issue("POLICY_DEBT","known_debt inválido",f"{loc}.known_debt"))
    missing,extra=sorted(discovered-seen),sorted(seen-discovered)
    if missing: issues.append(_issue("POLICY_SKILLS_MISSING",", ".join(missing),"skills"))
    if extra: issues.append(_issue("POLICY_SKILLS_EXTRA",", ".join(extra),"skills"))
    # A igualdade de conjuntos acima é o contrato: o catálogo cresce por skills reais.
    if not discovered: issues.append(_issue("POLICY_CATALOG_COUNT","nenhuma skill real descoberta","skills"))
    if not seen: issues.append(_issue("POLICY_ENTRY_COUNT","nenhuma política registrada","skills"))
    by={i.get("skill"):i for i in skills if isinstance(i,Mapping)}
    audit=by.get("hub-ml-auditoria-skills")
    if isinstance(audit,Mapping):
        missing_debt=sorted({"AUDIT_FALSE_REASSURANCE","AUDIT_STATE_LADDER","AUDIT_CONDITIONAL_APPLICABILITY"}-set(audit.get("known_debt") or []))
        if missing_debt: issues.append(_issue("POLICY_AUDIT_DEBT_MISSING",", ".join(missing_debt),"hub-ml-auditoria-skills"))
    pipeline=by.get("hub-ml-pipeline-builder")
    if isinstance(pipeline,Mapping):
        ev={s.get("evidence") for s in pipeline.get("protected_surfaces",[]) if isinstance(s,Mapping)}
        if "authorization" not in ev: issues.append(_issue("POLICY_PIPELINE_AUTHORIZATION","pipeline-builder precisa de surface authorization","hub-ml-pipeline-builder"))
    return issues

def summarize(policy_path:Path|str=DEFAULT_POLICY, *, assistant_root:Path|str=ASSISTANT_ROOT)->dict[str,Any]:
    assistant_root=Path(assistant_root)
    raw, issues=_read_policy(Path(policy_path))
    if not issues: issues=_validate_policy_data(raw, assistant_root)
    entries=raw.get("skills",[]) if isinstance(raw,Mapping) else []
    return {"schema_version":"1.0","sprint":"SE07","status":"PASS" if not issues else "FAIL","catalog_skills":len(discover_skills(assistant_root)),"policy_entries":len(entries) if isinstance(entries,list) else 0,"issues":[x.to_dict() for x in issues]}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--policy",default=str(DEFAULT_POLICY)); p.add_argument("--assistant-root",default=str(ASSISTANT_ROOT)); p.add_argument("--json",action="store_true"); a=p.parse_args()
    s=summarize(Path(a.policy), assistant_root=Path(a.assistant_root))
    if a.json: print(json.dumps(s,ensure_ascii=False,indent=2,sort_keys=True))
    else:
        print(f"SE07_POLICY = {s['status']} | catalog={s['catalog_skills']} | policies={s['policy_entries']}")
        for i in s["issues"]: print(f"FAIL {i['code']} {i['location']}: {i['message']}")
    return 0 if s["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
