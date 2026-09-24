from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "tools/skill_enforcement/parallel/coverage_registry.json"

def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAILED:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        sys.modules.pop(name, None)

def test_methods(path: Path) -> list[str]:
    if not path.is_file() or path.suffix != ".py":
        return []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("test_"):
                    out.append(f"{node.name}.{item.name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            out.append(node.name)
    return sorted(out)

def _command_test_path(argv: list[str]) -> Path | None:
    tokens = list(argv)
    for token in tokens:
        if token.endswith(".py") and ("test" in token or token.startswith("tools/tests/")):
            p = ROOT / token
            return p if p.is_file() else None
    if "-m" in tokens:
        idx = tokens.index("-m")
        if idx + 2 < len(tokens) and tokens[idx + 1] == "unittest":
            candidate = tokens[idx + 2]
            if candidate.startswith("tools.tests."):
                p = ROOT / (candidate.replace(".", "/") + ".py")
                return p if p.is_file() else None
    return None

def inventory() -> dict[str, Any]:
    cfg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    certify = _load("_parallel_coverage_certify", ROOT / "tools/skill_enforcement/certify_local.py")
    ci = _load("_parallel_coverage_ci", ROOT / "tools/ci_local.py")
    se08 = []
    for name, argv in certify.PROFILE_STEPS["se08"]:
        path = _command_test_path(argv)
        se08.append({
            "step_id": name,
            "classification": cfg["step_policy"].get(name, "UNCLASSIFIED"),
            "argv": list(argv),
            "test_path": path.relative_to(ROOT).as_posix() if path else None,
            "test_methods": test_methods(path) if path else [],
        })
    ci_rows = []
    for name, description, argv in ci.ETAPAS:
        if name == "sef":
            continue
        path = _command_test_path(argv)
        ci_rows.append({
            "step_id": "ci:" + name,
            "classification": "CURRENT_INVARIANT",
            "description": description,
            "argv": list(argv),
            "test_path": path.relative_to(ROOT).as_posix() if path else None,
            "test_methods": test_methods(path) if path else [],
        })
    ser01 = []
    for row in cfg["ser01_groups"]:
        path = ROOT / row["path"]
        ser01.append({**row, "classification": "CURRENT_INVARIANT", "exists": path.is_file(), "test_methods": test_methods(path)})
    issues = []
    if len(se08) != 21:
        issues.append(f"SE08_STEP_COUNT:{len(se08)}")
    if len(ci_rows) != 9:
        issues.append(f"CI_NON_SEF_COUNT:{len(ci_rows)}")
    if len(ser01) != 5:
        issues.append(f"SER01_GROUP_COUNT:{len(ser01)}")
    if any(row["classification"] == "UNCLASSIFIED" for row in se08):
        issues.append("SE08_UNCLASSIFIED_STEP")
    if any(not row["exists"] for row in ser01):
        issues.append("SER01_GROUP_MISSING")
    return {
        "schema_version": "SER-PARALLEL-COVERAGE-INVENTORY-1",
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "se08": se08,
        "ci_non_sef": ci_rows,
        "ser01": ser01,
        "counts": {"se08": len(se08), "ci_non_sef": len(ci_rows), "ser01": len(ser01)},
    }

def main() -> int:
    payload = inventory()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
