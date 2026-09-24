from __future__ import annotations
import locale, os, platform, shutil, sys
from pathlib import Path

def observe(repo:Path,scratch:Path)->dict:
    scratch.mkdir(parents=True,exist_ok=True)
    probe=scratch/'write_probe.tmp'; probe.write_text('probe',encoding='utf-8'); probe.unlink()
    return {"qualification_version":"SER-PARALLEL-HOST-1","platform":platform.platform(),"system":platform.system(),"python":sys.version.split()[0],"executable":sys.executable,"locale":locale.getpreferredencoding(False),"git":shutil.which('git'),"repo":str(repo.resolve()),"scratch":str(scratch.resolve()),"scratch_write":True,"codex_permission_probe":"NOT_RUN_REQUIRES_CLIENT_SANDBOX","model_alias_resolution":"NOT_RUN_REQUIRES_CLIENT"}
