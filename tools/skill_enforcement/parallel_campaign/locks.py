from __future__ import annotations
import json, os, time
from pathlib import Path

class LockBusy(RuntimeError): pass
class FileLease:
    def __init__(self,root:Path,key:str,owner:str): self.root=root; self.key=key; self.owner=owner; self.path=root/(key.replace('/','_')+'.lock'); self.fd=None
    def __enter__(self):
        self.root.mkdir(parents=True,exist_ok=True)
        try: self.fd=os.open(self.path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        except FileExistsError as exc: raise LockBusy(self.key) from exc
        os.write(self.fd,json.dumps({"owner":self.owner,"pid":os.getpid(),"created_at":time.time()}).encode()); os.fsync(self.fd); return self
    def __exit__(self,*exc):
        if self.fd is not None: os.close(self.fd); self.fd=None
        try: self.path.unlink()
        except FileNotFoundError: pass

def assert_no_stale_override(lock_path:Path)->None:
    if lock_path.exists(): raise LockBusy("STALE_OR_ACTIVE_LOCK_REQUIRES_RECONCILIATION")
