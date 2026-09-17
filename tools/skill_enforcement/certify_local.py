#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Certificação local reproduzível do Skill Enforcement Framework.

Uso principal:

    python -B tools/skill_enforcement/certify_local.py --profile se02

O certifier é o gate determinístico de desenvolvimento do SEF. Ele não usa
credenciais Databricks nem rede por conta própria. GitHub Actions deve chamar o
mesmo entrypoint somente na release candidate/Ready-for-review e pós-merge.

Por padrão a execução exige worktree limpo, materializa o simulado pelo renderer
canônico e falha se o renderer deixar diff. Isso transforma drift do derivado em
evidência explícita (`DERIVED_STALE`) em vez de permitir uma cópia manual.

A precondição de worktree limpo é uma barreira de segurança: se ela falhar, o
certifier encerra antes de qualquer step mutável, especialmente antes do renderer.
"""

from __future__ import annotations

import argparse
import json
import locale
import os
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = Path.home() / ".ambiente_databricks" / "sef_certifications"


@dataclass(frozen=True)
class StepResult:
    name: str
    command: list[str]
    exit_code: int
    duration_seconds: float
    status: str
    last_line: str
    log_file: str | None = None


@dataclass(frozen=True)
class GitState:
    head_sha: str | None
    branch: str | None
    origin_main_sha: str | None
    merge_base_sha: str | None
    status_short: str

    @property
    def clean(self) -> bool:
        return not self.status_short.strip()


PROFILE_STEPS: dict[str, list[tuple[str, list[str]]]] = {
    "se02": [
        (
            "contract_v0_1",
            [sys.executable, "-B", "tools/skill_enforcement/validate_contracts.py"],
        ),
        (
            "se01_regression",
            [sys.executable, "-B", "tools/tests/test_skill_enforcement_se01.py"],
        ),
        (
            "se02_tests",
            [sys.executable, "-B", "tools/tests/test_skill_enforcement_se02.py", "-v"],
        ),
        (
            "assistant_structure",
            [sys.executable, "tools/validate_assistant.py"],
        ),
        (
            "render_simulado",
            [sys.executable, "tools/render_simulado.py", "--write"],
        ),
        (
            "render_diff",
            ["git", "diff", "--exit-code", "--", "Novo_Ambiente_Simulado"],
        ),
        (
            "readme_snapshot",
            [sys.executable, "tools/validate_assistant.py", "--conferir-readme"],
        ),
    ]
}


def _decode(data: bytes) -> str:
    for encoding in ("utf-8", locale.getpreferredencoding(False)):
        try:
            return data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="replace")


def _run(command: Sequence[str]) -> tuple[int, str, float]:
    env = dict(
        os.environ,
        PYTHONIOENCODING="utf-8",
        PYTHONUTF8="1",
        PYTHONDONTWRITEBYTECODE="1",
    )
    start = time.monotonic()
    proc = subprocess.run(
        list(command),
        cwd=REPO_ROOT,
        capture_output=True,
        env=env,
    )
    duration = time.monotonic() - start
    output = _decode((proc.stdout or b"") + (proc.stderr or b""))
    return proc.returncode, output, duration


def _git_output(*args: str) -> str | None:
    code, output, _ = _run(["git", *args])
    if code != 0:
        return None
    return output.strip()


def _git_state() -> GitState:
    head = _git_output("rev-parse", "HEAD")
    branch = _git_output("branch", "--show-current")
    origin_main = _git_output("rev-parse", "origin/main")
    merge_base = None
    if head and origin_main:
        merge_base = _git_output("merge-base", head, origin_main)
    status = _git_output("status", "--short", "--untracked-files=all")
    return GitState(
        head_sha=head,
        branch=branch or None,
        origin_main_sha=origin_main,
        merge_base_sha=merge_base,
        status_short=status or "",
    )


def _last_nonempty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()[:240]
    return ""


def _resolve_evidence_dir(raw: str | None, head_sha: str | None) -> Path:
    if raw:
        target = Path(raw).expanduser().resolve()
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        suffix = (head_sha or "unknown")[:12]
        target = (DEFAULT_EVIDENCE_ROOT / f"{timestamp}_{suffix}").resolve()
    if target == REPO_ROOT or target.is_relative_to(REPO_ROOT):
        raise ValueError("evidence-dir deve ficar fora da árvore do repositório")
    return target


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _filtered_steps(profile: str, skip_render: bool) -> list[tuple[str, list[str]]]:
    steps = list(PROFILE_STEPS[profile])
    if not skip_render:
        return steps
    return [
        item
        for item in steps
        if item[0] not in {"render_simulado", "render_diff"}
    ]


def _persist_bundle(
    evidence_dir: Path | None,
    summary: dict[str, object],
    results: list[StepResult],
) -> None:
    if evidence_dir is None:
        return
    evidence_dir.mkdir(parents=True, exist_ok=True)
    _write_json(evidence_dir / "summary.json", summary)
    _write_json(
        evidence_dir / "environment.json",
        {
            "python": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
            "cwd": str(REPO_ROOT),
        },
    )
    _write_json(
        evidence_dir / "commands.json",
        [{"name": result.name, "command": result.command} for result in results],
    )


def _build_summary(
    *,
    profile: str,
    scope: str,
    before: GitState,
    after: GitState,
    results: list[StepResult],
) -> dict[str, object]:
    failures = [result for result in results if result.exit_code != 0]
    derived_stale = any(
        result.name == "render_diff" and result.exit_code != 0 for result in results
    )
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "certification_scope": scope,
        "LOCAL_CERTIFICATION": "PASS" if not failures else "FAIL",
        "DERIVED_STALE": derived_stale,
        "GITHUB_ACTIONS": "NOT_EVALUATED_BY_LOCAL_CERTIFIER",
        "databricks_free": "NOT_EVALUATED_BY_LOCAL_CERTIFIER",
        "synthetic_agent_screening": "NOT_EVALUATED_BY_LOCAL_CERTIFIER",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "git_before": asdict(before),
        "git_after": asdict(after),
        "steps": [asdict(result) for result in results],
        "failure_count": len(failures),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILE_STEPS), default="se02")
    parser.add_argument(
        "--evidence-dir",
        help="Diretório explícito para evidence bundle; por padrão usa ~/.ambiente_databricks/sef_certifications.",
    )
    parser.add_argument(
        "--no-evidence",
        action="store_true",
        help="Não grava evidence bundle; útil quando chamado como subgate do ci_local.py.",
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="Pula renderer/diff; não equivale a certificação SE02 completa.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Permite worktree já sujo; o padrão fail-closed exige worktree limpo.",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    before = _git_state()
    evidence_dir: Path | None = None
    if not args.no_evidence:
        try:
            evidence_dir = _resolve_evidence_dir(args.evidence_dir, before.head_sha)
        except ValueError as exc:
            print(f"FAIL evidence_dir: {exc}")
            return 2
        evidence_dir.mkdir(parents=True, exist_ok=True)

    print("== SKILL ENFORCEMENT LOCAL CERTIFICATION ==")
    print(f"profile : {args.profile}")
    print(f"root    : {REPO_ROOT}")
    print(f"branch  : {before.branch or '<unknown>'}")
    print(f"HEAD    : {before.head_sha or '<unknown>'}")
    print(f"python  : {sys.version.split()[0]}")
    print(f"platform: {platform.platform()}")

    results: list[StepResult] = []

    if not before.clean and not args.allow_dirty:
        print("\nFAIL precheck_git_clean: worktree deve estar limpo para certificação.")
        if before.status_short.strip():
            print(before.status_short.strip())
        results.append(
            StepResult(
                name="precheck_git_clean",
                command=["git", "status", "--short", "--untracked-files=all"],
                exit_code=1,
                duration_seconds=0.0,
                status="FAIL",
                last_line="worktree sujo; nenhum step mutável foi executado",
            )
        )
        after = _git_state()
        summary = _build_summary(
            profile=args.profile,
            scope="PRECHECK_ONLY",
            before=before,
            after=after,
            results=results,
        )
        _persist_bundle(evidence_dir, summary, results)
        if evidence_dir is not None:
            print(f"evidence: {evidence_dir}")
        print("LOCAL_CERTIFICATION = FAIL")
        print("failed_steps        = precheck_git_clean")
        return 2

    logs_dir: Path | None = None
    if evidence_dir is not None:
        logs_dir = evidence_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

    for index, (name, command) in enumerate(_filtered_steps(args.profile, args.skip_render), 1):
        print(f"\n-- {index:02d} {name}")
        code, output, duration = _run(command)
        status = "PASS" if code == 0 else "FAIL"
        log_file = None
        if logs_dir is not None:
            target = logs_dir / f"{index:02d}_{name}.log"
            target.write_text(output, encoding="utf-8")
            log_file = str(target)
        if args.verbose or code != 0:
            print(output.rstrip())
        print(f"   {status} ({duration:.2f}s) {_last_nonempty_line(output)}")
        results.append(
            StepResult(
                name=name,
                command=list(command),
                exit_code=code,
                duration_seconds=round(duration, 4),
                status=status,
                last_line=_last_nonempty_line(output),
                log_file=log_file,
            )
        )

    after = _git_state()
    scope = "PARTIAL_NO_RENDER" if args.skip_render else "FULL_SE02_LOCAL"
    summary = _build_summary(
        profile=args.profile,
        scope=scope,
        before=before,
        after=after,
        results=results,
    )
    _persist_bundle(evidence_dir, summary, results)

    failures = [result for result in results if result.exit_code != 0]
    derived_stale = bool(summary["DERIVED_STALE"])

    if evidence_dir is not None:
        print(f"\nevidence: {evidence_dir}")

    print("\n== CERTIFICATION SUMMARY ==")
    print(f"LOCAL_CERTIFICATION = {summary['LOCAL_CERTIFICATION']}")
    print(f"scope               = {scope}")
    print(f"DERIVED_STALE       = {str(derived_stale).lower()}")
    print(f"failures            = {len(failures)}")
    if args.skip_render:
        print("note                = renderer/diff não foram avaliados")

    if failures:
        print("failed_steps        = " + ", ".join(result.name for result in failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
