from __future__ import annotations
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
class HostLeaseBusy(RuntimeError): pass
class HostCampaignLease:
 def __init__(self,round_id:str,campaign_id:str):
  self.round_id=round_id; self.campaign_id=campaign_id; self.path=Path(tempfile.gettempdir())/"ambiente_databricks_ser"/"campaign.lock"; self._fh=None
 def __enter__(self):
  self.path.parent.mkdir(parents=True,exist_ok=True); fh=self.path.open("a+b"); fh.seek(0,os.SEEK_END)
  if fh.tell()==0: fh.write(b"\0"); fh.flush()
  fh.seek(0)
  try:
   if os.name=="nt":
    import msvcrt
    try: msvcrt.locking(fh.fileno(),msvcrt.LK_NBLCK,1)
    except OSError as exc: raise HostLeaseBusy("HOST_CAMPAIGN_LEASE_BUSY") from exc
   else:
    import fcntl
    try: fcntl.flock(fh.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except OSError as exc: raise HostLeaseBusy("HOST_CAMPAIGN_LEASE_BUSY") from exc
   self._fh=fh; metadata={"schema_version":"SER-PARALLEL-HOST-LEASE-1","round_id":self.round_id,"campaign_id":self.campaign_id,"pid":os.getpid(),"acquired_at_utc":datetime.now(timezone.utc).isoformat()}
   fh.seek(0); fh.truncate(); fh.write((json.dumps(metadata,sort_keys=True)+"\n").encode()); fh.flush(); os.fsync(fh.fileno()); return self
  except Exception:
   if self._fh is None: fh.close()
   raise
 def __exit__(self,exc_type,exc,tb):
  fh=self._fh; self._fh=None
  if fh is None: return False
  try:
   fh.seek(0); fh.truncate(); fh.write(b"\0"); fh.flush()
   if os.name=="nt":
    import msvcrt; fh.seek(0); msvcrt.locking(fh.fileno(),msvcrt.LK_UNLCK,1)
   else:
    import fcntl; fcntl.flock(fh.fileno(),fcntl.LOCK_UN)
  finally: fh.close()
  return False
