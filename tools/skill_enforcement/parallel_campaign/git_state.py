from __future__ import annotations
import os, subprocess
from pathlib import Path

def _run(repo: Path,*args:str)->str:
    p=subprocess.run(["git","-c",f"core.hooksPath={os.devnull}","-c","core.quotepath=false",*args],cwd=repo,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=30)
    if p.returncode: raise RuntimeError(f"GIT_FAILED:{args}:{p.stderr.strip()}")
    return p.stdout.rstrip("\r\n")

def status_paths(repo: Path)->list[str]:
    out=_run(repo,"status","--porcelain=v1","--untracked-files=all")
    paths=[]
    for line in out.splitlines():
        if not line: continue
        raw=line[3:]
        if " -> " in raw: raw=raw.split(" -> ",1)[1]
        if raw.startswith('"') and raw.endswith('"'): raw=raw[1:-1]
        paths.append(raw.replace("\\","/"))
    return sorted(paths)

def git_state(repo: Path)->dict:
    counts=_run(repo,"rev-list","--left-right","--count","origin/main...HEAD").split()
    return {"head":_run(repo,"rev-parse","HEAD"),"tree":_run(repo,"rev-parse","HEAD^{tree}"),"branch":_run(repo,"rev-parse","--abbrev-ref","HEAD"),"origin_main":_run(repo,"rev-parse","origin/main"),"merge_base":_run(repo,"merge-base","HEAD","origin/main"),"shallow":_run(repo,"rev-parse","--is-shallow-repository"),"status":status_paths(repo),"behind":int(counts[0]),"ahead":int(counts[1])}
