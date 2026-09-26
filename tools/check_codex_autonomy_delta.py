#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENVELOPE = ROOT / "docs" / "operations" / "autonomy" / "B1_AUTONOMY_ENVELOPE.json"


def _patterns() -> tuple[list[str], list[str], list[str]]:
    payload = json.loads(ENVELOPE.read_text(encoding="utf-8"))
    scope = payload["repo_scope"]
    return (
        list(scope["write_roots"]),
        list(scope["protected_roots"]),
        list(scope["shared_roots_requiring_human_gate"]),
    )


def _matches(path: str, patterns: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in patterns)


def classify_path(path: str) -> str:
    write_roots, protected, shared = _patterns()
    if _matches(path, protected):
        return "PROTECTED"
    if _matches(path, shared):
        return "HUMAN_GATE_REQUIRED"
    if _matches(path, write_roots):
        return "ALLOWED_A1"
    return "OUTSIDE_A1"


def _changed_paths(base: str, head: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..{head}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("GIT_DIFF_FAILED:" + (proc.stderr.strip() or proc.stdout.strip()))
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def check_delta(base: str, head: str) -> dict:
    rows = [{"path": path, "classification": classify_path(path)} for path in _changed_paths(base, head)]
    violations = [row for row in rows if row["classification"] != "ALLOWED_A1"]
    return {
        "schema_version": "SER-CODEX-AUTONOMY-DELTA-1",
        "base": base,
        "head": head,
        "status": "PASS" if not violations else "FAIL",
        "files": rows,
        "violations": violations,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    result = check_delta(args.base, args.head)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
