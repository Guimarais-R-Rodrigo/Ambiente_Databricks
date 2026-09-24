from __future__ import annotations

import ast
import fnmatch
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "tools/skill_enforcement/parallel/coverage_registry.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None: raise RuntimeError(f"MODULE_LOAD_FAILED:{path}")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    try: spec.loader.exec_module(module); return module
    finally: sys.modules.pop(name, None)


def test_methods(path: Path) -> list[str]:
    if not path.is_file() or path.suffix != ".py": return []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path)); out=[]
    rel = path.relative_to(ROOT).as_posix()
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("test_"):
                    out.append(f"{rel}::{node.name}.{item.name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            out.append(f"{rel}::{node.name}")
    return sorted(out)


def _command_test_paths(argv: list[str]) -> list[Path]:
    tokens=list(argv); paths=[]
    if "discover" in tokens and "-s" in tokens and "-p" in tokens:
        start=ROOT/tokens[tokens.index("-s")+1]; pattern=tokens[tokens.index("-p")+1]
        if start.is_dir(): paths.extend(sorted(p for p in start.rglob("*.py") if fnmatch.fnmatch(p.name, pattern)))
    if "-m" in tokens:
        idx=tokens.index("-m")
        if idx+2 < len(tokens) and tokens[idx+1]=="unittest":
            for candidate in tokens[idx+2:]:
                if candidate.startswith("-"): continue
                if candidate.startswith("tools.tests."):
                    p=ROOT/(candidate.replace(".","/")+".py")
                    if p.is_file(): paths.append(p)
    for token in tokens:
        if token.endswith(".py"):
            p=ROOT/token
            if p.is_file() and ("test" in p.name or "tests" in p.parts): paths.append(p)
    dedup=[]; seen=set()
    for p in paths:
        rp=p.resolve()
        if rp not in seen: seen.add(rp); dedup.append(p)
    return dedup


def _classify(method: str, default: str, overrides: dict[str, Any]) -> dict[str, Any]:
    override=overrides.get(method)
    if override: return {"test_id":method, **override}
    return {"test_id":method,"classification":default}


def inventory() -> dict[str, Any]:
    cfg=json.loads(REGISTRY.read_text(encoding="utf-8")); overrides=cfg.get("method_overrides",{})
    certify=_load("_parallel_coverage_certify",ROOT/"tools/skill_enforcement/certify_local.py")
    ci=_load("_parallel_coverage_ci",ROOT/"tools/ci_local.py")
    se08=[]
    for name,argv in certify.PROFILE_STEPS["se08"]:
        paths=_command_test_paths(list(argv)); default=cfg["step_policy"].get(name,"UNCLASSIFIED")
        methods=[m for path in paths for m in test_methods(path)]
        classified=[_classify(m,"CURRENT_INVARIANT" if default=="MIXED_METHOD_CLASSIFICATION" else default,overrides) for m in methods]
        mapping_status="UNCLASSIFIED" if default=="UNCLASSIFIED" else ("MAPPED" if methods else ("EMPTY_METHOD_MAP" if paths else "COMMAND_ONLY"))
        se08.append({"step_id":name,"classification":default,"argv":list(argv),"test_paths":[p.relative_to(ROOT).as_posix() for p in paths],"test_methods":classified,"mapping_status":mapping_status})
    ci_rows=[]
    for name,description,argv in ci.ETAPAS:
        if name=="sef": continue
        paths=_command_test_paths(list(argv)); methods=[m for path in paths for m in test_methods(path)]
        step_id="ci:"+name
        mapping_status="COMMAND_ONLY" if step_id in set(cfg.get("command_only_steps",[])) else ("MAPPED" if methods else ("EMPTY_METHOD_MAP" if paths else "COMMAND_ONLY"))
        ci_rows.append({"step_id":step_id,"classification":"CURRENT_INVARIANT","description":description,"argv":list(argv),"test_paths":[p.relative_to(ROOT).as_posix() for p in paths],"test_methods":[_classify(m,"CURRENT_INVARIANT",overrides) for m in methods],"mapping_status":mapping_status})
    ser01=[]
    for row in cfg["ser01_groups"]:
        path=ROOT/row["path"]; methods=test_methods(path)
        mapping_status="MISSING" if not path.is_file() else ("MAPPED" if methods else ("COMMAND_ONLY" if row.get("mapping_mode")=="command" else "EMPTY_METHOD_MAP"))
        ser01.append({**row,"classification":"MIXED_CURRENT_AND_TEMPORAL" if row["group_id"]=="ser01_certifier" else "CURRENT_INVARIANT","exists":path.is_file(),"test_methods":[_classify(m,"CURRENT_INVARIANT",overrides) for m in methods],"mapping_status":mapping_status})
    issues=[]
    if len(se08)!=21: issues.append(f"SE08_STEP_COUNT:{len(se08)}")
    if len(ci_rows)!=9: issues.append(f"CI_NON_SEF_COUNT:{len(ci_rows)}")
    if len(ser01)!=5: issues.append(f"SER01_GROUP_COUNT:{len(ser01)}")
    if any(row["mapping_status"] in {"UNCLASSIFIED","MISSING","EMPTY_METHOD_MAP"} for row in [*se08,*ci_rows,*ser01]): issues.append("METHOD_MAP_INCOMPLETE")
    observed={item["test_id"] for group in [*se08,*ci_rows,*ser01] for item in group["test_methods"]}
    missing_overrides=sorted(set(overrides)-observed)
    if missing_overrides: issues.append("TEMPORAL_OVERRIDE_NOT_OBSERVED:"+",".join(missing_overrides))
    return {"schema_version":"SER-PARALLEL-COVERAGE-INVENTORY-2","status":"PASS" if not issues else "FAIL","issues":issues,"se08":se08,"ci_non_sef":ci_rows,"ser01":ser01,"counts":{"se08":len(se08),"ci_non_sef":len(ci_rows),"ser01":len(ser01),"methods":sum(len(r["test_methods"]) for r in [*se08,*ci_rows,*ser01])},"temporal_overrides":overrides}


def main() -> int:
    payload=inventory(); print(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if payload["status"]=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
