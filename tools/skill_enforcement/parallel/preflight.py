from __future__ import annotations
import json
from .contract import validate_campaign
from .process import ROOT
from .registry import load_registry
PARALLEL=ROOT/"tools/skill_enforcement/parallel"; PLAN=ROOT/"docs/sprints/skill_enforcement_rollout/PARALELO"
def run():
 issues=[]; json_paths=sorted({*PARALLEL.rglob("*.json"),*PLAN.rglob("*.json")}); parsed={}
 for path in json_paths:
  try: parsed[path]=json.loads(path.read_text(encoding="utf-8"))
  except (OSError,UnicodeDecodeError,json.JSONDecodeError) as exc: issues.append(f"JSON_INVALID:{path.relative_to(ROOT).as_posix()}:{type(exc).__name__}:{exc}")
 python_paths=sorted({*PARALLEL.glob("*.py"),ROOT/"tools/tests/test_ser_parallel_b0.py"})
 for path in python_paths:
  try: compile(path.read_text(encoding="utf-8"),str(path),"exec")
  except (OSError,UnicodeDecodeError,SyntaxError) as exc: issues.append(f"PYTHON_COMPILE_INVALID:{path.relative_to(ROOT).as_posix()}:{type(exc).__name__}:{exc}")
 try: load_registry()
 except Exception as exc: issues.append(f"COMMAND_REGISTRY_INVALID:{type(exc).__name__}:{exc}")
 cfg=parsed.get(PARALLEL/"coverage_registry.json")
 if not isinstance(cfg,dict) or cfg.get("schema_version")!="SER-PARALLEL-COVERAGE-3": issues.append("COVERAGE_REGISTRY_SCHEMA_INVALID")
 for name in ("pilot_campaign.json","pilot_global_stop_campaign.json"):
  payload=parsed.get(PARALLEL/name)
  if payload is not None: issues.extend(f"{name}:{x}" for x in validate_campaign(payload))
 return {"schema_version":"SER-B0-AUTHORING-PREFLIGHT-1","status":"PASS" if not issues else "FAIL","issues":issues,"json_files_parsed":len(parsed),"python_files_compiled":len(python_paths)}
def main():
 result=run(); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
