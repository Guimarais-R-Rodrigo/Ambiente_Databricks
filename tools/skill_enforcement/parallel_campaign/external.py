from __future__ import annotations
from pathlib import Path
from .util import read_json,write_json_atomic

def collect_literal(record_path:Path,output:Path)->dict:
    record=read_json(record_path)
    required={'case_id','deployment_id','environment','payload_literal','evidence_grade'}
    missing=sorted(required-set(record))
    if missing: raise ValueError('EXTERNAL_RECORD_MISSING:'+','.join(missing))
    write_json_atomic(output,record); return record
