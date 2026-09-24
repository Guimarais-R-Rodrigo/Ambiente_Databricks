from __future__ import annotations
import hashlib, platform, subprocess, sys, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from .contract import digest_json
from .process import ROOT
from .registry import DEFAULT_REGISTRY, load_registry
POLICY=ROOT/"ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json"
ROUND_START_SCHEMA="SER-B0-ROUND-START-1"; RELEASE_SPEC_SCHEMA="SER-B0-RELEASE-SPEC-1"
def _utc(): return datetime.now(timezone.utc).isoformat()
def _git(*args):
 p=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,text=True,timeout=30)
 if p.returncode!=0: raise RuntimeError("GIT_FAILED:"+" ".join(args)+":"+(p.stderr or "").strip())
 return p.stdout.strip()
def capture_round_start():
 if _git("status","--porcelain=v1","--untracked-files=all"): raise RuntimeError("WORKTREE_NOT_CLEAN")
 if _git("rev-parse","--is-shallow-repository")!="false": raise RuntimeError("SHALLOW_REPOSITORY")
 candidate=_git("rev-parse","HEAD")
 return {"schema_version":ROUND_START_SCHEMA,"round_id":"B0ROUND-"+uuid.uuid4().hex,"candidate_sha":candidate,"candidate_tree_sha":_git("rev-parse","HEAD^{tree}"),"baseline_sha":_git("merge-base","HEAD","origin/main"),"branch":_git("rev-parse","--abbrev-ref","HEAD"),"started_at_utc":_utc()}
def assert_round_start_current(row:Mapping[str,Any]):
 issues=[]
 try:
  if _git("rev-parse","HEAD")!=row.get("candidate_sha"): issues.append("ROUND_HEAD_CHANGED")
  if _git("rev-parse","HEAD^{tree}")!=row.get("candidate_tree_sha"): issues.append("ROUND_TREE_CHANGED")
  if _git("merge-base","HEAD","origin/main")!=row.get("baseline_sha"): issues.append("ROUND_MERGE_BASE_CHANGED")
  if _git("status","--porcelain=v1","--untracked-files=all"): issues.append("ROUND_WORKTREE_DIRTY")
 except RuntimeError as exc: issues.append(str(exc))
 return issues
def build_release_spec(round_start,coverage_payload,host_payload):
 if coverage_payload.get("status")!="PASS": raise ValueError("COVERAGE_NOT_PASS")
 return {"schema_version":RELEASE_SPEC_SCHEMA,"round_id":round_start["round_id"],"candidate_sha":round_start["candidate_sha"],"candidate_tree_sha":round_start["candidate_tree_sha"],"baseline_sha":round_start["baseline_sha"],"branch":round_start["branch"],"command_registry_digest":digest_json(load_registry(DEFAULT_REGISTRY)),"coverage_digest":digest_json(coverage_payload),"policy_before_digest":hashlib.sha256(POLICY.read_bytes()).hexdigest(),"host_digest":digest_json(host_payload),"python_executable":str(Path(sys.executable).resolve()),"python_version":platform.python_version(),"platform":platform.platform(),"created_at_utc":_utc()}
def release_spec_digest(spec): return digest_json(dict(spec))
def validate_release_spec(spec):
 if not isinstance(spec,Mapping): return ["RELEASE_SPEC_NOT_OBJECT"]
 required={"schema_version","round_id","candidate_sha","candidate_tree_sha","baseline_sha","branch","command_registry_digest","coverage_digest","policy_before_digest","host_digest","python_executable","python_version","platform","created_at_utc"}
 issues=[]
 if set(spec)!=required: issues.append("RELEASE_SPEC_KEYS_INVALID")
 if spec.get("schema_version")!=RELEASE_SPEC_SCHEMA: issues.append("RELEASE_SPEC_SCHEMA_INVALID")
 for key in ("round_id","branch","python_executable","python_version","platform","created_at_utc"):
  if not isinstance(spec.get(key),str) or not spec.get(key): issues.append("RELEASE_SPEC_FIELD_INVALID:"+key)
 for key in ("candidate_sha","candidate_tree_sha","baseline_sha"):
  value=spec.get(key)
  if not isinstance(value,str) or len(value)!=40 or any(c not in "0123456789abcdef" for c in value): issues.append("RELEASE_SPEC_SHA_INVALID:"+key)
 for key in ("command_registry_digest","coverage_digest","policy_before_digest","host_digest"):
  value=spec.get(key)
  if not isinstance(value,str) or len(value)!=64 or any(c not in "0123456789abcdef" for c in value): issues.append("RELEASE_SPEC_DIGEST_INVALID:"+key)
 return issues
def assert_release_spec_current(spec):
 issues=validate_release_spec(spec)
 try:
  if _git("rev-parse","HEAD")!=spec.get("candidate_sha"): issues.append("RELEASE_HEAD_CHANGED")
  if _git("rev-parse","HEAD^{tree}")!=spec.get("candidate_tree_sha"): issues.append("RELEASE_TREE_CHANGED")
  if _git("merge-base","HEAD","origin/main")!=spec.get("baseline_sha"): issues.append("RELEASE_MERGE_BASE_CHANGED")
  if _git("status","--porcelain=v1","--untracked-files=all"): issues.append("RELEASE_WORKTREE_DIRTY")
 except RuntimeError as exc: issues.append(str(exc))
 try:
  if digest_json(load_registry(DEFAULT_REGISTRY))!=spec.get("command_registry_digest"): issues.append("RELEASE_REGISTRY_CHANGED")
 except Exception as exc: issues.append("RELEASE_REGISTRY_UNREADABLE:"+type(exc).__name__)
 try:
  if hashlib.sha256(POLICY.read_bytes()).hexdigest()!=spec.get("policy_before_digest"): issues.append("RELEASE_POLICY_CHANGED")
 except OSError as exc: issues.append("RELEASE_POLICY_UNREADABLE:"+type(exc).__name__)
 if str(Path(sys.executable).resolve())!=spec.get("python_executable"): issues.append("RELEASE_INTERPRETER_CHANGED")
 if platform.python_version()!=spec.get("python_version"): issues.append("RELEASE_PYTHON_VERSION_CHANGED")
 return issues
