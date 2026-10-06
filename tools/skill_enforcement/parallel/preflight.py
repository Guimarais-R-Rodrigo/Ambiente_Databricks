from __future__ import annotations
import json
from .contract import (CAMPAIGN_SCHEMA_VERSION, COMMAND_RECORD_SCHEMA_VERSION, RESULT_SCHEMA_VERSION, TASK_SCHEMA_VERSION, validate_campaign)
from .process import ROOT
from .registry import load_registry
from .coverage import registry_issues
from tools.project_policy import CORPORATE_RE, PERSONAL_RE
PARALLEL=ROOT/"tools/skill_enforcement/parallel"; PLAN=ROOT/"docs/sprints/skill_enforcement_rollout/PARALELO"

def _hygiene_issues(paths):
 issues=[]
 for path in paths:
  try: text=path.read_text(encoding="utf-8")
  except (OSError,UnicodeDecodeError) as exc: issues.append(f"HYGIENE_READ_ERROR:{path}:{type(exc).__name__}"); continue
  if CORPORATE_RE.search(text) or PERSONAL_RE.search(text):
   try: rel=path.relative_to(ROOT).as_posix()
   except ValueError: rel=str(path)
   issues.append("REPO_HYGIENE_IDENTIFIER:"+rel)
 return issues

def run():
 issues=[]; json_paths=sorted({*PARALLEL.rglob("*.json"),*PLAN.rglob("*.json")}); parsed={}
 for path in json_paths:
  try: parsed[path]=json.loads(path.read_text(encoding="utf-8"))
  except (OSError,UnicodeDecodeError,json.JSONDecodeError) as exc: issues.append(f"JSON_INVALID:{path.relative_to(ROOT).as_posix()}:{type(exc).__name__}:{exc}")
 hygiene_paths=sorted({
  ROOT/"CHANGELOG.md",
  ROOT/"tools/tests/test_ser_parallel_b0.py",
  *PARALLEL.glob("*.py"),
  *PLAN.rglob("*.md"),
  *PLAN.rglob("*.json"),
 })
 issues.extend(_hygiene_issues(hygiene_paths))
 python_paths=sorted({*PARALLEL.glob("*.py"),ROOT/"tools/tests/test_ser_parallel_b0.py"})
 for path in python_paths:
  try: compile(path.read_text(encoding="utf-8"),str(path),"exec")
  except (OSError,UnicodeDecodeError,SyntaxError) as exc: issues.append(f"PYTHON_COMPILE_INVALID:{path.relative_to(ROOT).as_posix()}:{type(exc).__name__}:{exc}")
 try: load_registry()
 except Exception as exc: issues.append(f"COMMAND_REGISTRY_INVALID:{type(exc).__name__}:{exc}")
 cfg=parsed.get(PARALLEL/"coverage_registry.json")
 issues.extend(registry_issues(cfg))
 schema_contracts=[
  (PARALLEL/"schemas/campaign.schema.json","schema_version",CAMPAIGN_SCHEMA_VERSION),
  (PARALLEL/"schemas/task.schema.json","task_schema",TASK_SCHEMA_VERSION),
  (PARALLEL/"schemas/result.schema.json","result_schema",RESULT_SCHEMA_VERSION),
  (PARALLEL/"schemas/command_record.schema.json","record_schema",COMMAND_RECORD_SCHEMA_VERSION),
 ]
 for path,field,expected in schema_contracts:
  schema=parsed.get(path)
  if not isinstance(schema,dict): issues.append("CONTRACT_SCHEMA_INVALID:"+path.name); continue
  if schema.get("$id")!=expected: issues.append("CONTRACT_SCHEMA_ID_DRIFT:"+path.name)
  if schema.get("additionalProperties") is not False: issues.append("CONTRACT_SCHEMA_NOT_CLOSED:"+path.name)
  prop=(schema.get("properties") or {}).get(field)
  if not isinstance(prop,dict) or prop.get("const")!=expected: issues.append("CONTRACT_SCHEMA_VERSION_DRIFT:"+path.name)
 planning_campaign=parsed.get(PLAN/"templates/CAMPANHA_PLANEJADA.json")
 planning_task=parsed.get(PLAN/"templates/TAREFA_LOCAL.json")
 if not isinstance(planning_campaign,dict) or planning_campaign.get("contract_version")!=CAMPAIGN_SCHEMA_VERSION: issues.append("PLANNING_CAMPAIGN_CONTRACT_DRIFT")
 if not isinstance(planning_task,dict) or planning_task.get("contract_version")!=TASK_SCHEMA_VERSION: issues.append("PLANNING_TASK_CONTRACT_DRIFT")
 for name in ("pilot_campaign.json","pilot_global_stop_campaign.json"):
  payload=parsed.get(PARALLEL/name)
  if payload is not None: issues.extend(f"{name}:{x}" for x in validate_campaign(payload))
 return {"schema_version":"SER-B0-AUTHORING-PREFLIGHT-1","status":"PASS" if not issues else "FAIL","issues":issues,"json_files_parsed":len(parsed),"python_files_compiled":len(python_paths),"schema_contracts_checked":len(schema_contracts),"hygiene_files_checked":len(hygiene_paths)}
def main():
 result=run(); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
