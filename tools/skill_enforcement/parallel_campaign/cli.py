from __future__ import annotations
import argparse,json,sys
from pathlib import Path

# Suporta tanto `python -m tools.skill_enforcement.parallel_campaign.cli` quanto
# a invocação direta pelo path usada nos runbooks locais.
if __package__ in {None, ''}:
    ROOT = Path(__file__).resolve().parents[3]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    __package__ = 'tools.skill_enforcement.parallel_campaign'

from .engine import execute
from .host_qualification import observe
from .inventory import expand_patterns
from .manifest import validate_campaign,validate_registry
from .packaging import make_share,zip_share,validate_zip_members
from .util import read_json,write_json_atomic
from .verify import verify_manifest,verify_run

def main(argv=None)->int:
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
    lint=sub.add_parser('lint'); lint.add_argument('--campaign',type=Path,required=True); lint.add_argument('--registry',type=Path,required=True)
    for name in ('diagnose','certify','pilot'):
        q=sub.add_parser(name); q.add_argument('--repo',type=Path,default=Path('.')); q.add_argument('--campaign',type=Path,required=True); q.add_argument('--registry',type=Path,required=True); q.add_argument('--evidence-dir',type=Path,required=True); q.add_argument('--evidence-authorized',action='store_true'); q.add_argument('--authorization',type=Path)
    inv=sub.add_parser('inventory'); inv.add_argument('--repo',type=Path,default=Path('.')); inv.add_argument('--patterns-json',type=Path,required=True); inv.add_argument('--output',type=Path,required=True)
    qual=sub.add_parser('qualify-host'); qual.add_argument('--repo',type=Path,default=Path('.')); qual.add_argument('--scratch',type=Path,required=True); qual.add_argument('--output',type=Path,required=True)
    ver=sub.add_parser('verify'); ver.add_argument('--campaign',type=Path,required=True); ver.add_argument('--evidence-dir',type=Path,required=True)
    pack=sub.add_parser('package'); pack.add_argument('--raw',type=Path,required=True); pack.add_argument('--share',type=Path,required=True); pack.add_argument('--redactions',type=Path,required=True); pack.add_argument('--zip',type=Path,required=True)
    zv=sub.add_parser('verify-zip'); zv.add_argument('zip_path',type=Path)
    a=p.parse_args(argv)
    if a.cmd=='lint':
        reg=read_json(a.registry); camp=read_json(a.campaign); issues=validate_campaign(camp,reg); print(json.dumps({"status":"PASS" if not issues else "FAIL","issues":issues},ensure_ascii=False,indent=2)); return 0 if not issues else 1
    if a.cmd in {'diagnose','certify','pilot'}:
        camp=read_json(a.campaign)
        if camp.get('mode')!=a.cmd: print('MODE_MISMATCH',file=sys.stderr); return 2
        try: s=execute(a.repo.resolve(),a.campaign,a.registry,a.evidence_dir,a.evidence_authorized,a.authorization)
        except Exception as exc: print(f"ENGINE_ERROR:{type(exc).__name__}:{exc}",file=sys.stderr); return 2
        print(json.dumps(s,ensure_ascii=False,indent=2)); return 0 if s['status']=='PASS' else 1
    if a.cmd=='inventory':
        patterns=read_json(a.patterns_json)['patterns']; out={"inventory_version":"SER-PARALLEL-INVENTORY-1","patterns":expand_patterns(a.repo,patterns)}; write_json_atomic(a.output,out); print(json.dumps(out,indent=2)); return 0
    if a.cmd=='qualify-host': out=observe(a.repo,a.scratch); write_json_atomic(a.output,out); print(json.dumps(out,indent=2)); return 0
    if a.cmd=='verify':
        camp=read_json(a.campaign); out={"run":verify_run(camp,a.evidence_dir),"manifest":verify_manifest(a.evidence_dir)}; print(json.dumps(out,indent=2)); return 0 if out['run']['valid'] and out['manifest']['valid'] else 1
    if a.cmd=='package': red=read_json(a.redactions); make_share(a.raw,a.share,red); zip_share(a.share,a.zip); issues=validate_zip_members(a.zip); print(json.dumps({"status":"PASS" if not issues else "FAIL","issues":issues},indent=2)); return 0 if not issues else 1
    if a.cmd=='verify-zip': issues=validate_zip_members(a.zip_path); print(json.dumps({"status":"PASS" if not issues else "FAIL","issues":issues},indent=2)); return 0 if not issues else 1
    return 2

if __name__=='__main__': raise SystemExit(main())
