from __future__ import annotations
import json, shutil, zipfile
from pathlib import Path, PurePosixPath
from .util import sha256_file, write_json_atomic

def validate_zip_members(path:Path)->list[str]:
    issues=[]
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts: issues.append('ZIP_PATH_UNSAFE:'+info.filename)
            mode=(info.external_attr>>16)&0o170000
            if mode==0o120000: issues.append('ZIP_SYMLINK_FORBIDDEN:'+info.filename)
    return issues

def make_share(raw:Path,share:Path,redactions:dict[str,str])->dict:
    if share.exists(): raise ValueError('SHARE_MUST_BE_NEW')
    share.mkdir(parents=True)
    bindings=[]
    for src in sorted(raw.rglob('*')):
        if not src.is_file() or src.is_symlink(): continue
        rel=src.relative_to(raw); dst=share/rel; dst.parent.mkdir(parents=True,exist_ok=True)
        data=src.read_bytes(); changed=False
        try:
            text=data.decode('utf-8')
            for old,new in redactions.items():
                if old in text: text=text.replace(old,new); changed=True
            out=text.encode('utf-8')
        except UnicodeDecodeError: out=data
        dst.write_bytes(out)
        bindings.append({"path":rel.as_posix(),"raw_sha256":__import__('hashlib').sha256(data).hexdigest(),"share_sha256":__import__('hashlib').sha256(out).hexdigest(),"sanitized":changed})
    payload={"binding_version":"SER-PARALLEL-RAW-SHARE-1","files":bindings}
    write_json_atomic(share/'raw_bindings.json',payload)
    return payload

def zip_share(share:Path,target:Path)->None:
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(share.rglob('*')):
            if p.is_file() and not p.is_symlink(): z.write(p,p.relative_to(share).as_posix())
