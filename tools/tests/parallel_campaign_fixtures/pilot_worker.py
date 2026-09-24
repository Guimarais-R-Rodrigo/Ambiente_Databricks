from __future__ import annotations
import json,sys,time
from pathlib import Path
mode=sys.argv[1]; evidence=Path(sys.argv[2]); task_id=sys.argv[3]
evidence.mkdir(parents=True,exist_ok=True)
(evidence/'worker.json').write_text(json.dumps({'task_id':task_id,'mode':mode}),encoding='utf-8')
if mode=='pass': print('PILOT_PASS'); raise SystemExit(0)
if mode=='fail': print('PILOT_FAIL',file=sys.stderr); raise SystemExit(7)
if mode=='sleep': time.sleep(.2); print('PILOT_SLEEP_PASS'); raise SystemExit(0)
raise SystemExit(9)
