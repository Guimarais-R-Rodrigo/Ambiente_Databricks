"""Inventário B0 por identidade e coleta real; não executa nem qualifica testes.

Rejeita etapas omitidas, extras ou duplicadas e declarações AST sem teste
coletável. Contratos históricos permanecem ligados a seus SHAs de origem.
"""
from __future__ import annotations
import ast, fnmatch, importlib.util, json, re, sys, unittest
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[3]; REGISTRY=ROOT/"tools/skill_enforcement/parallel/coverage_registry.json"; _SHA_RE=re.compile(r"^[0-9a-f]{40}$")
REGISTRY_SCHEMA = "SER-PARALLEL-COVERAGE-4"
INVENTORY_SCHEMA = "SER-PARALLEL-COVERAGE-INVENTORY-4"
# O registro resolve paths; esta fronteira conserva a identidade dos grupos SER01.
SER01_GROUP_IDS = frozenset({
 "ser01_object_validation", "ser01_certifier", "ser01_promotion_certifier",
 "ser01_legacy_create_l3", "ser01_free_probe",
})

def _load(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 if spec is None or spec.loader is None: raise RuntimeError(f"MODULE_LOAD_FAILED:{path}")
 module=importlib.util.module_from_spec(spec); sys.modules[name]=module
 try: spec.loader.exec_module(module); return module
 finally: sys.modules.pop(name,None)
@contextmanager
def _root_on_path():
 value=str(ROOT); inserted=value not in sys.path
 if inserted: sys.path.insert(0,value)
 try: yield
 finally:
  if inserted:
   try: sys.path.remove(value)
   except ValueError: pass
def ast_test_methods(path):
 if not path.is_file() or path.suffix!=".py": return []
 tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path)); out=[]; rel=path.relative_to(ROOT).as_posix()
 for node in tree.body:
  if isinstance(node,ast.ClassDef):
   for item in node.body:
    if isinstance(item,(ast.FunctionDef,ast.AsyncFunctionDef)) and item.name.startswith("test_"): out.append(f"{rel}::{node.name}.{item.name}")
  elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name.startswith("test_"): out.append(f"{rel}::{node.name}")
 return sorted(out)
def test_methods(path): return ast_test_methods(path)
def _flatten(suite):
 out=[]
 for item in suite:
  if isinstance(item,unittest.TestSuite): out.extend(_flatten(item))
  else: out.append(item)
 return out
def _normalize_unittest_id(raw):
 parts=raw.split(".")
 for idx in range(len(parts)-2,0,-1):
  candidate=ROOT.joinpath(*parts[:idx]).with_suffix(".py")
  if candidate.is_file(): return f"{candidate.relative_to(ROOT).as_posix()}::{'.'.join(parts[idx:])}"
 return None
def _normalize_loaded_test(test):
 raw=test.id(); module_name=getattr(test.__class__,"__module__",""); module=sys.modules.get(module_name)
 source=getattr(module,"__file__",None) if module is not None else None
 if source:
  try:
   path=Path(source).resolve(); rel=path.relative_to(ROOT.resolve()).as_posix()
  except (OSError,ValueError): pass
  else:
   prefix=module_name+"."
   suffix=raw[len(prefix):] if module_name and raw.startswith(prefix) else raw
   return f"{rel}::{suffix}"
 return _normalize_unittest_id(raw)
def _collect_from_suite(suite):
 ids=[]; errors=[]
 for test in _flatten(suite):
  raw=test.id()
  if "_FailedTest" in raw: errors.append("FAILED_TEST:"+raw); continue
  normalized=_normalize_loaded_test(test)
  if normalized is None: errors.append("UNRESOLVED_TEST_ID:"+raw)
  else: ids.append(normalized)
 return ids,errors
def _discover(start,pattern):
 loader=unittest.TestLoader()
 try:
  with _root_on_path(): suite=loader.discover(start_dir=str(start),pattern=pattern)
 except Exception as exc: return [],[f"DISCOVER_EXCEPTION:{type(exc).__name__}:{exc}"]
 ids,errors=_collect_from_suite(suite); errors.extend(f"LOADER_ERROR:{msg}" for msg in loader.errors); return ids,errors
def _module_target_path(target):
 parts=target.split(".")
 for idx in range(len(parts),0,-1):
  path=ROOT.joinpath(*parts[:idx]).with_suffix(".py")
  if path.is_file(): return path, ".".join(parts[idx:]) or None
 return None,None
def _collect_file(path,selector=None):
 if not path.is_file(): return [],["TARGET_MISSING:"+path.as_posix()]
 rel=path.relative_to(ROOT).with_suffix(""); module_name=".".join(rel.parts); spec=importlib.util.spec_from_file_location(module_name,path)
 if spec is None or spec.loader is None: return [],["MODULE_SPEC_FAILED:"+path.as_posix()]
 module=importlib.util.module_from_spec(spec); previous=sys.modules.get(module_name); sys.modules[module_name]=module
 try:
  with _root_on_path():
   spec.loader.exec_module(module); loader=unittest.TestLoader(); suite=loader.loadTestsFromName(selector,module) if selector else loader.loadTestsFromModule(module); ids,errors=_collect_from_suite(suite); errors.extend(f"LOADER_ERROR:{msg}" for msg in loader.errors); return ids,errors
 except Exception as exc: return [],[f"IMPORT_EXCEPTION:{path.relative_to(ROOT).as_posix()}:{type(exc).__name__}:{exc}"]
 finally:
  if previous is None: sys.modules.pop(module_name,None)
  else: sys.modules[module_name]=previous
def _command_test_paths(argv):
 tokens=list(argv); paths=[]
 if "discover" in tokens and "-s" in tokens and "-p" in tokens:
  start=ROOT/tokens[tokens.index("-s")+1]; pattern=tokens[tokens.index("-p")+1]
  if start.is_dir(): paths.extend(sorted(p for p in start.rglob("*.py") if fnmatch.fnmatch(p.name,pattern)))
 if "-m" in tokens:
  idx=tokens.index("-m")
  if idx+2<len(tokens) and tokens[idx+1]=="unittest":
   for candidate in tokens[idx+2:]:
    if candidate.startswith("-") or candidate=="discover": continue
    path,_=_module_target_path(candidate)
    if path is not None: paths.append(path)
 for token in tokens:
  if token.endswith(".py"):
   p=ROOT/token
   if p.is_file() and ("test" in p.name or "tests" in p.parts): paths.append(p)
 dedup=[]; seen=set()
 for p in paths:
  rp=p.resolve()
  if rp not in seen: seen.add(rp); dedup.append(p)
 return dedup
def _collect_command(argv):
 tokens=list(argv); paths=_command_test_paths(argv)
 if "-m" in tokens:
  idx=tokens.index("-m")
  if idx+1<len(tokens) and tokens[idx+1]=="unittest":
   if "discover" in tokens:
    if "-s" not in tokens or "-p" not in tokens: return [],["DISCOVER_ARGS_INCOMPLETE"],paths
    start=ROOT/tokens[tokens.index("-s")+1]; pattern=tokens[tokens.index("-p")+1]
    if not start.is_dir(): return [],["DISCOVER_START_MISSING:"+start.as_posix()],paths
    ids,errors=_discover(start,pattern); return ids,errors,paths
   targets=[x for x in tokens[idx+2:] if not x.startswith("-")]
   if not targets: return [],["UNITTEST_TARGET_MISSING"],paths
   all_ids=[]; errors=[]
   for target in targets:
    path,selector=_module_target_path(target)
    if path is None: errors.append("UNITTEST_TARGET_MISSING:"+target); continue
    ids,item_errors=_collect_file(path,selector); all_ids.extend(ids); errors.extend(item_errors)
   return all_ids,errors,paths
 direct=[ROOT/token for token in tokens if token.endswith(".py") and ("test" in Path(token).name or "tests" in Path(token).parts)]
 if direct:
  all_ids=[]; errors=[]
  for path in direct:
   ids,item_errors=_collect_file(path); all_ids.extend(ids); errors.extend(item_errors)
  return all_ids,errors,paths
 return [],["NOT_UNITTEST_COMMAND"],paths
def _command_only_errors(argv):
 tokens=list(argv)
 if not tokens: return ["COMMAND_ONLY_ARGV_EMPTY"]
 issues=[]; first=Path(tokens[0]).name.lower()
 is_python=tokens[0]==sys.executable or first.startswith("python")
 if is_python:
  if "-m" in tokens:
   idx=tokens.index("-m")
   if idx+1>=len(tokens): issues.append("COMMAND_ONLY_MODULE_MISSING")
   else:
    module=tokens[idx+1]; path,selector=_module_target_path(module)
    if path is None: issues.append("COMMAND_ONLY_MODULE_TARGET_MISSING:"+module)
    elif selector is not None: issues.append("COMMAND_ONLY_MODULE_SELECTOR_UNSUPPORTED:"+module)
  scripts=[token for token in tokens[1:] if token.endswith(".py")]
  for token in scripts:
   target=ROOT/token
   if not target.is_file(): issues.append("COMMAND_ONLY_SCRIPT_MISSING:"+token)
  if "-m" not in tokens and not scripts: issues.append("COMMAND_ONLY_PYTHON_ENTRYPOINT_MISSING")
 elif first=="git":
  if len(tokens)<2 or tokens[1]!="status": issues.append("COMMAND_ONLY_GIT_OPERATION_UNSUPPORTED")
 else:
  issues.append("COMMAND_ONLY_EXECUTABLE_UNSUPPORTED:"+tokens[0])
 return issues
def _validate_override(test_id,override):
 if not isinstance(override,dict): return ["OVERRIDE_NOT_OBJECT:"+test_id]
 expected={"classification","historical_sha","reason","successor_ids"}
 if set(override)!=expected: return ["OVERRIDE_SCHEMA_INVALID:"+test_id]
 issues=[]
 if override.get("classification")!="HISTORICAL_TEMPORAL": issues.append("OVERRIDE_CLASSIFICATION_INVALID:"+test_id)
 if not isinstance(override.get("historical_sha"),str) or _SHA_RE.fullmatch(override["historical_sha"]) is None: issues.append("OVERRIDE_SHA_INVALID:"+test_id)
 if not isinstance(override.get("reason"),str) or not override["reason"].strip(): issues.append("OVERRIDE_REASON_INVALID:"+test_id)
 successors=override.get("successor_ids")
 if not isinstance(successors,list) or not successors or any(not isinstance(x,str) or not x for x in successors): issues.append("OVERRIDE_SUCCESSORS_INVALID:"+test_id)
 return issues
def _classify(method,default,overrides):
 override=overrides.get(method); return {"test_id":method,**override} if override else {"test_id":method,"classification":default}
def _expected_ast_methods(argv, paths):
 """A named unittest selector promises only that class/method, not its siblings."""
 tokens = list(argv)
 selected = {}
 if "-m" in tokens:
  index = tokens.index("-m")
  if index + 1 < len(tokens) and tokens[index + 1] == "unittest" and "discover" not in tokens:
   for target in tokens[index + 2:]:
    if target.startswith("-"): continue
    path, selector = _module_target_path(target)
    if path is not None: selected.setdefault(path, []).append(selector)
 methods = []
 for path in paths:
  for method in ast_test_methods(path):
   selectors = selected.get(path, [None])
   suffix = method.split("::", 1)[1]
   if any(selector is None or suffix == selector or suffix.startswith(selector + ".") for selector in selectors):
    methods.append(method)
 return methods

def _row(step_id,classification,argv,command_only,overrides,description=None):
 paths=_command_test_paths(argv)
 try: ast_methods=_expected_ast_methods(argv, paths); ast_errors=[]
 except (OSError, UnicodeDecodeError, SyntaxError) as exc:
  ast_methods=[]; ast_errors=["AST_COLLECTION_ERROR:" + type(exc).__name__]
 if step_id in command_only:
  collection_errors=_command_only_errors(argv); test_ids=[]
  status="COMMAND_ONLY" if not collection_errors else ("MISSING" if any("MISSING" in item for item in collection_errors) else "COLLECTION_ERROR")
 else:
  test_ids,collection_errors,paths=_collect_command(argv)
  if collection_errors: status="MISSING" if any("MISSING" in item for item in collection_errors) else "COLLECTION_ERROR"
  elif test_ids: status="MAPPED"
  else: status="EMPTY_METHOD_MAP"
  uncollected = sorted(set(ast_methods) - set(test_ids))
  if uncollected:
   collection_errors.extend("AST_TEST_NOT_COLLECTED:" + method for method in uncollected)
   if status == "MAPPED": status = "COLLECTION_ERROR"
 if ast_errors:
  collection_errors.extend(ast_errors)
  status = "COLLECTION_ERROR"
 default="CURRENT_INVARIANT" if classification=="MIXED_METHOD_CLASSIFICATION" else classification
 row={"step_id":step_id,"classification":classification,"argv":list(argv),"test_paths":[p.relative_to(ROOT).as_posix() for p in paths],"ast_methods":sorted(set(ast_methods)),"test_methods":[_classify(x,default,overrides) for x in test_ids],"mapping_status":status,"collection_errors":collection_errors,"duplicate_test_ids":sorted(x for x,count in Counter(test_ids).items() if count>1)}
 if description is not None: row["description"]=description
 return row
def _step_identity_issues(source, actual, expected):
 """Compare identities from the executable owner, never only cardinality."""
 issues = []
 if not actual: issues.append(source + "_DISCOVERY_EMPTY")
 counts = Counter(actual)
 for step_id, count in counts.items():
  if count > 1: issues.append(source + "_STEP_DUPLICATE:" + step_id)
 for step_id in sorted(set(expected) - set(actual)):
  issues.append(source + "_STEP_MISSING:" + step_id)
 for step_id in sorted(set(actual) - set(expected)):
  issues.append(source + "_STEP_UNEXPECTED:" + step_id)
 return issues

def registry_issues(cfg):
 """Versioned live contract; frozen v3 campaign inventories remain historical."""
 if not isinstance(cfg, dict) or cfg.get("schema_version") != REGISTRY_SCHEMA:
  return ["COVERAGE_REGISTRY_SCHEMA_INVALID"]
 issues = []
 step_policy = cfg.get("step_policy")
 if not isinstance(step_policy, dict) or not step_policy:
  issues.append("STEP_POLICY_EMPTY_OR_INVALID")
 elif any(not isinstance(key, str) or not isinstance(value, str) or value not in {"CURRENT_INVARIANT", "MIXED_METHOD_CLASSIFICATION"} for key, value in step_policy.items()):
  issues.append("STEP_POLICY_CLASSIFICATION_INVALID")
 ci_policy = cfg.get("ci_step_policy")
 if not isinstance(ci_policy, dict) or not ci_policy:
  issues.append("CI_STEP_POLICY_EMPTY_OR_INVALID")
 else:
  for step_id, policy in ci_policy.items():
   if not isinstance(step_id, str) or not step_id.startswith("ci:") or step_id == "ci:sef":
    issues.append("CI_STEP_POLICY_ID_INVALID:" + str(step_id))
   if not isinstance(policy, dict) or set(policy) != {"classification", "mapping_mode"}:
    issues.append("CI_STEP_POLICY_SCHEMA_INVALID:" + str(step_id))
   elif policy["classification"] != "CURRENT_INVARIANT" or not isinstance(policy["mapping_mode"], str) or policy["mapping_mode"] not in {"command", "unittest"}:
    issues.append("CI_STEP_POLICY_CLASSIFICATION_INVALID:" + str(step_id))
 command_only = cfg.get("command_only_steps")
 if not isinstance(command_only, list) or any(not isinstance(item, str) for item in command_only):
  issues.append("COMMAND_ONLY_STEPS_INVALID")
 else:
  if len(command_only) != len(set(command_only)): issues.append("COMMAND_ONLY_STEP_DUPLICATE")
  if isinstance(ci_policy, dict):
   declared = {step_id for step_id, policy in ci_policy.items() if isinstance(policy, dict) and policy.get("mapping_mode") == "command"}
   actual = {step_id for step_id in command_only if step_id.startswith("ci:")}
   if declared != actual: issues.append("CI_COMMAND_ONLY_POLICY_MISMATCH")
 overrides = cfg.get("method_overrides")
 if not isinstance(overrides, dict): issues.append("OVERRIDES_NOT_OBJECT")
 else:
  for test_id, override in overrides.items(): issues.extend(_validate_override(test_id, override))
 retired = cfg.get("retired_method_overrides", {})
 if not isinstance(retired, dict): issues.append("RETIRED_OVERRIDES_NOT_OBJECT")
 else:
  for test_id, record in retired.items():
   if not isinstance(record, dict) or set(record) != {"override", "retirement_sha", "reason", "successor_ids"}:
    issues.append("RETIRED_OVERRIDE_SCHEMA_INVALID:" + test_id); continue
   issues.extend(_validate_override(test_id, record["override"]))
   if not isinstance(record["retirement_sha"], str) or _SHA_RE.fullmatch(record["retirement_sha"]) is None:
    issues.append("RETIRED_OVERRIDE_SHA_INVALID:" + test_id)
   if not isinstance(record["reason"], str) or not record["reason"].strip():
    issues.append("RETIRED_OVERRIDE_REASON_INVALID:" + test_id)
   successors = record["successor_ids"]
   if not isinstance(successors, list) or not successors or any(not isinstance(item, str) or not item for item in successors):
    issues.append("RETIRED_OVERRIDE_SUCCESSORS_INVALID:" + test_id)
   if isinstance(overrides, dict) and test_id in overrides: issues.append("RETIRED_OVERRIDE_STILL_ACTIVE:" + test_id)
 groups = cfg.get("ser01_groups")
 if not isinstance(groups, list) or not groups:
  issues.append("SER01_GROUPS_EMPTY_OR_INVALID")
 else:
  for group in groups:
   if not isinstance(group, dict) or not isinstance(group.get("group_id"), str) or not isinstance(group.get("path"), str):
    issues.append("SER01_GROUP_SCHEMA_INVALID")
   elif not isinstance(group.get("mapping_mode", "unittest"), str) or group.get("mapping_mode", "unittest") not in {"command", "unittest"}:
    issues.append("SER01_GROUP_MAPPING_MODE_INVALID:" + group["group_id"])
 return issues

def _unique_object(pairs):
 result = {}
 for key, value in pairs:
  if key in result: raise ValueError("DUPLICATE_REGISTRY_KEY:" + key)
  result[key] = value
 return result

def inventory():
 try:
  cfg = json.loads(REGISTRY.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
 except (OSError, UnicodeDecodeError, ValueError) as exc:
  return {"schema_version": INVENTORY_SCHEMA, "status": "FAIL", "issues": ["COVERAGE_REGISTRY_UNREADABLE:" + type(exc).__name__]}
 issues = registry_issues(cfg)
 if issues: return {"schema_version": INVENTORY_SCHEMA, "status": "FAIL", "issues": sorted(set(issues))}
 overrides=cfg["method_overrides"]; command_only=set(cfg["command_only_steps"])
 certify=_load("_parallel_coverage_certify",ROOT/"tools/skill_enforcement/certify_local.py"); ci=_load("_parallel_coverage_ci",ROOT/"tools/ci_local.py")
 se08=[]
 se08_steps = certify.PROFILE_STEPS["se08"]
 issues.extend(_step_identity_issues("SE08", [name for name, _ in se08_steps], cfg["step_policy"]))
 for name,argv in se08_steps:
  classification=cfg["step_policy"].get(name,"UNCLASSIFIED")
  if classification=="UNCLASSIFIED": issues.append("STEP_POLICY_UNCLASSIFIED:"+name)
  se08.append(_row(name,classification,list(argv),command_only,overrides))
 ci_rows=[]
 ci_ids = ["ci:" + name for name, _, _ in ci.ETAPAS if name != "sef"]
 issues.extend(_step_identity_issues("CI_NON_SEF", ci_ids, cfg["ci_step_policy"]))
 if sum(name == "sef" for name, _, _ in ci.ETAPAS) != 1: issues.append("CI_SEF_STEP_NOT_UNIQUE")
 for name,description,argv in ci.ETAPAS:
  if name=="sef": continue
  step_id = "ci:" + name
  classification = cfg["ci_step_policy"].get(step_id, {}).get("classification", "UNCLASSIFIED")
  ci_rows.append(_row(step_id,classification,list(argv),command_only,overrides,description))
 ser01=[]
 for config in cfg["ser01_groups"]:
  path=ROOT/config["path"]; step_id=config["group_id"]
  if config.get("mapping_mode")=="command":
   row={**config,"classification":"CURRENT_INVARIANT","exists":path.is_file(),"test_methods":[],"ast_methods":ast_test_methods(path) if path.is_file() else [],"mapping_status":"COMMAND_ONLY" if path.is_file() else "MISSING","collection_errors":[],"duplicate_test_ids":[]}
  else:
   row=_row(step_id,"MIXED_CURRENT_AND_TEMPORAL" if step_id=="ser01_certifier" else "CURRENT_INVARIANT",[sys.executable,str(path.relative_to(ROOT)),"-v"],command_only,overrides); row={**config,"exists":path.is_file(),**row}
  row.setdefault("step_id", step_id)
  ser01.append(row)
 issues.extend(_step_identity_issues("SER01", [row["step_id"] for row in ser01], SER01_GROUP_IDS))
 rows=[*se08,*ci_rows,*ser01]
 known_ids = {row["step_id"] for row in rows}
 for step_id in sorted(command_only - known_ids): issues.append("COMMAND_ONLY_STEP_NOT_OBSERVED:" + step_id)
 for row in rows:
  if row["mapping_status"] in {"UNCLASSIFIED","MISSING","EMPTY_METHOD_MAP","COLLECTION_ERROR"}: issues.append(f"METHOD_MAP_INCOMPLETE:{row['step_id']}:{row['mapping_status']}")
  if row.get("duplicate_test_ids"): issues.append(f"DUPLICATE_TEST_ID:{row['step_id']}:{','.join(row['duplicate_test_ids'])}")
 observed_occurrences=[item["test_id"] for group in rows for item in group.get("test_methods",[])]; observed=set(observed_occurrences)
 for test_id,override in overrides.items():
  if test_id not in observed: issues.append("TEMPORAL_OVERRIDE_NOT_OBSERVED:"+test_id); continue
  for successor in override["successor_ids"]:
   if successor not in observed: issues.append(f"TEMPORAL_SUCCESSOR_NOT_OBSERVED:{test_id}:{successor}")
 for test_id, record in cfg.get("retired_method_overrides", {}).items():
  if test_id in observed: issues.append("RETIRED_OVERRIDE_OBSERVED:" + test_id)
  for successor in [*record["successor_ids"], *record["override"]["successor_ids"]]:
   if successor not in observed: issues.append(f"RETIRED_SUCCESSOR_NOT_OBSERVED:{test_id}:{successor}")
 counts=Counter(observed_occurrences)
 return {"schema_version":INVENTORY_SCHEMA,"status":"PASS" if not issues else "FAIL","issues":sorted(set(issues)),"se08":se08,"ci_non_sef":ci_rows,"ser01":ser01,"counts":{"se08":len(se08),"ci_non_sef":len(ci_rows),"ser01":len(ser01),"method_occurrences":len(observed_occurrences),"unique_methods":len(counts)},"test_id_occurrences":dict(sorted(counts.items())),"temporal_overrides":overrides,"retired_temporal_overrides":cfg.get("retired_method_overrides", {})}
def _json_cli(payload):
 return json.dumps(payload,ensure_ascii=True,indent=2,sort_keys=True)+"\n"
def main():
 payload=inventory(); sys.stdout.write(_json_cli(payload)); return 0 if payload["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
