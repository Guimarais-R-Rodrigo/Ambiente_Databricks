from __future__ import annotations
import hashlib, os
from pathlib import Path

def _h(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def fingerprint_one(root: Path, rel: str) -> dict[str,str]:
    path=root/rel; out={}
    if not path.exists() and not path.is_symlink(): return {rel:"MISSING"}
    if path.is_symlink(): return {rel:"SYMLINK:"+os.readlink(path)}
    if path.is_file(): return {rel:"FILE:"+_h(path.read_bytes())}
    for base,dirs,files in os.walk(path,followlinks=False):
        b=Path(base)
        for name in sorted(list(dirs)):
            p=b/name; rr=p.relative_to(root).as_posix()
            if p.is_symlink() or getattr(p,"is_junction",lambda:False)():
                dirs.remove(name); out[rr]="LINK:"+os.readlink(p)
            else: out[rr]="DIR"
        for name in sorted(files):
            p=b/name; rr=p.relative_to(root).as_posix()
            out[rr]="SYMLINK:"+os.readlink(p) if p.is_symlink() else "FILE:"+_h(p.read_bytes())
    return out

def fingerprint_paths(root: Path, paths: tuple[str,...]|list[str]) -> dict[str,str]:
    out={}
    for rel in paths:
        out.update(fingerprint_one(root,rel))
    return out
