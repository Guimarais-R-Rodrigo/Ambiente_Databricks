from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from typing import Any

def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data=canonical_json_bytes(value)+b"\n"
    tmp=path.with_name(path.name+f".tmp-{os.getpid()}")
    with tmp.open("xb") as fh:
        fh.write(data); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp,path)

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
