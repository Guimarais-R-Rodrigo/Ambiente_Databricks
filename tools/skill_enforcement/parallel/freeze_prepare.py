from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
README = ROOT / "README.md"

_ID_RE = re.compile(r"(?m)^(repo \(identidade\)\s*:\s*)\d+(\s+arquivos varridos no repositório editável/derivado\s*)$")
_LINK_RE = re.compile(r"(?m)^(repo \(links\)\s*:\s*)\d+(\s+links fora da raiz analisada\s*)$")
_OUT_ID_RE = re.compile(r"(?m)^repo \(identidade\)\s*:\s*(\d+)\b")
_OUT_LINK_RE = re.compile(r"(?m)^repo \(links\)\s*:\s*(\d+)\b")


def parse_snapshot(output: str) -> tuple[int, int]:
    ids = _OUT_ID_RE.findall(output)
    links = _OUT_LINK_RE.findall(output)
    if len(ids) != 1 or len(links) != 1:
        raise ValueError("SNAPSHOT_OUTPUT_AMBIGUOUS")
    return int(ids[0]), int(links[0])


def rewrite_readme(text: str, identity: int, links: int) -> str:
    if len(_ID_RE.findall(text)) != 1 or len(_LINK_RE.findall(text)) != 1:
        raise ValueError("README_SNAPSHOT_LINES_AMBIGUOUS")
    text = _ID_RE.sub(lambda m: f"{m.group(1)}{identity}{m.group(2)}", text, count=1)
    text = _LINK_RE.sub(lambda m: f"{m.group(1)}{links}{m.group(2)}", text, count=1)
    return text


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
        env={**__import__("os").environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
    )


def prepare(*, apply: bool) -> dict:
    status = _run(["git", "status", "--porcelain=v1", "--untracked-files=all"])
    if status.returncode != 0 or status.stdout.strip():
        return {"status": "FAIL", "issue": "WORKTREE_MUST_START_CLEAN"}

    validation = _run([sys.executable, "-B", "tools/validate_assistant.py"])
    if validation.returncode != 0:
        return {
            "status": "FAIL",
            "issue": "VALIDATOR_BASELINE_FAILED",
            "exit_code": validation.returncode,
            "stdout": validation.stdout,
            "stderr": validation.stderr,
        }
    try:
        identity, links = parse_snapshot(validation.stdout + "\n" + validation.stderr)
        original = README.read_text(encoding="utf-8")
        proposed = rewrite_readme(original, identity, links)
    except (OSError, UnicodeError, ValueError) as exc:
        return {"status": "FAIL", "issue": f"SNAPSHOT_PREPARATION:{type(exc).__name__}:{exc}"}

    changed = proposed != original
    result = {
        "status": "PASS",
        "apply": apply,
        "changed": changed,
        "snapshot": {"repo_identity": identity, "repo_links": links},
        "allowed_paths": ["README.md"],
    }
    if not apply or not changed:
        return result

    README.write_text(proposed, encoding="utf-8")
    after = _run(["git", "status", "--porcelain=v1", "--untracked-files=all"])
    changed_paths = []
    for line in after.stdout.splitlines():
        if len(line) >= 4:
            changed_paths.append(line[3:].strip().strip('"'))
    if after.returncode != 0 or set(changed_paths) != {"README.md"}:
        return {**result, "status": "FAIL", "issue": "UNEXPECTED_PREPARATION_DELTA", "changed_paths": changed_paths}

    checked = _run([sys.executable, "-B", "tools/validate_assistant.py", "--conferir-readme"])
    if checked.returncode != 0:
        return {
            **result,
            "status": "FAIL",
            "issue": "README_SNAPSHOT_RECHECK_FAILED",
            "exit_code": checked.returncode,
            "stdout": checked.stdout,
            "stderr": checked.stderr,
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcilia mecanicamente apenas o snapshot medido do README antes do freeze B0.")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    payload = prepare(apply=args.apply)
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
