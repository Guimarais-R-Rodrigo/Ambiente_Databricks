from __future__ import annotations
import json, os
from pathlib import Path
from .util import sha256_file, write_json_atomic

class EvidenceError(ValueError): pass

def reserve_evidence(path:Path,repo:Path,authorized:bool)->Path:
    if authorized is not True: raise EvidenceError("EVIDENCE_PERSISTENCE_NOT_AUTHORIZED")
    if path.exists() or path.is_symlink(): raise EvidenceError("EVIDENCE_DIRECTORY_MUST_BE_NEW")
    parent=path.parent.resolve(strict=True); rr=repo.resolve(strict=True); target=path.absolute()
    try:
        inside_repo=parent.is_relative_to(rr)
        contains_repo=rr.is_relative_to(target)
    except AttributeError:
        inside_repo=str(parent).startswith(str(rr)+os.sep) or parent==rr
        contains_repo=str(rr).startswith(str(target)+os.sep) or rr==target
    if inside_repo or contains_repo: raise EvidenceError("EVIDENCE_MUST_BE_EXTERNAL_TO_REPO")
    path.mkdir(); return path

def manifest_tree(root:Path)->dict:
    files=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and not p.is_symlink():
            files.append({"path":p.relative_to(root).as_posix(),"size":p.stat().st_size,"sha256":sha256_file(p)})
    return {"manifest_version":"SER-PARALLEL-EVIDENCE-MANIFEST-1","files":files}

def write_manifest(root:Path)->dict:
    m=manifest_tree(root); write_json_atomic(root/'manifest.json',m); return m
