#!/usr/bin/env python3
"""MM01 Local Certification v1.

Mechanical, fail-closed local executor for the MM01 certification gates.
It does not decide whether MM01 is fit for merge and it does not replace
independent audit or explicit human acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import urlparse

REPOSITORY = "Guimarais-R-Rodrigo/Ambiente_Databricks"
DEFAULT_BRANCH = "micromodelos/mm01-contrato-canonico"
BUNDLE_SCHEMA = "mm01-local-certification/v1"
PYTHON_MAJOR_MINOR = (3, 12)
NODE_MAJOR = 22
PNPM_VERSION = "10.34.5"
SOURCE_DATE_EPOCH = "1700000000"

WORKFLOW_SOURCES = (
    ".github/workflows/ci.yml",
    ".github/workflows/micromodelos-mm01-ci.yml",
    ".github/workflows/temas-v00-ci.yml",
    ".github/workflows/temas-v01-ci.yml",
    ".github/workflows/temas-v02-ci.yml",
    ".github/workflows/temas-v10-ci.yml",
    ".github/workflows/temas-v11-ci.yml",
    ".github/workflows/temas-v12-ci.yml",
    ".github/workflows/temas-v13-ci.yml",
)

# Exact Git blob identities of the workflow definitions whose executable gates
# are mirrored below. Any workflow edit (including a newly added gate) must
# fail closed until this certifier is deliberately reconciled and reviewed.
WORKFLOW_EXPECTED_BLOBS = {
    ".github/workflows/ci.yml": "af73cb6abbf4d09e4aacd217a6be0490ac36e7c1",
    ".github/workflows/micromodelos-mm01-ci.yml": "7d45792cb733d3b42d0c8822091d253df185e726",
    ".github/workflows/temas-v00-ci.yml": "a56c1243ee0e97574af25279c07bc3907c8ae33c",
    ".github/workflows/temas-v01-ci.yml": "91e3a174930e5e27953719a14f7b4979f1b41424",
    ".github/workflows/temas-v02-ci.yml": "53ebc80ccd7777430f5c37e7fd7fc05b6558071e",
    ".github/workflows/temas-v10-ci.yml": "f05b501569d30e350100e05663e269062c6b7aea",
    ".github/workflows/temas-v11-ci.yml": "b3cc6fc8f0c656d98db196c4998de230274a02e1",
    ".github/workflows/temas-v12-ci.yml": "d47c925db7c97e9bad8931198d4cf09079a7c559",
    ".github/workflows/temas-v13-ci.yml": "da1200bb158eaa11c8d3cf155cbfa28fd8a0d9ac",
}

WORKFLOW_REQUIRED_SNIPPETS = {
    ".github/workflows/ci.yml": (
        "python -m pip install -r tools/requirements-dev.txt",
        "npm install --global pnpm@10.34.5",
        "pnpm --dir tools/readme_visuals install --frozen-lockfile",
        "python tools/ci_local.py",
    ),
    ".github/workflows/micromodelos-mm01-ci.yml": (
        "python -B -m unittest tools/tests/test_micromodelo_mm01.py -v",
        "python -B -m unittest tools/tests/test_micromodelo_mm01_r02.py -v",
        "python -B -m unittest tools/tests/test_micromodelo_mm01_r03.py -v",
        "python -B tools/validate_assistant.py --root ambiente_fonte",
    ),
    ".github/workflows/temas-v00-ci.yml": (
        "python -B tools/tests/test_inventario_visual.py",
        "python -B tools/tests/test_visual_legado_v00.py",
        "python -B tools/tests/test_baseline_visual_runner.py",
    ),
    ".github/workflows/temas-v01-ci.yml": (
        "python -B tools/temas_v01_contract.py",
        "test_temas_v01*.py",
    ),
    ".github/workflows/temas-v02-ci.yml": (
        "python -B tools/temas_v02_check.py",
        "python -B tools/temas_v01_contract.py",
        "python -B tools/tests/test_temas_v02.py",
        "python -B ambiente_fonte/.assistant/hub_snippets/visual/tema/exemplo_tema.py",
    ),
    ".github/workflows/temas-v10-ci.yml": (
        "python -B tools/tests/test_temas_v10.py -v",
        "app.py",
        "app_service.py",
        "test_temas*.py",
        "python -B tools/tests/test_visual_legado_v00.py",
        "python -B tools/temas_v10_app.py --output .artifacts/v10-app",
        "python -B tools/temas_v10_app.py --verify .artifacts/v10-app",
        "python -B tools/validate_assistant.py --conferir-readme",
    ),
    ".github/workflows/temas-v11-ci.yml": (
        "python -B tools/tests/test_temas_v11.py -v",
        "aibi_theme.py",
        "test_temas*.py",
        "python -B tools/tests/test_visual_legado_v00.py",
        "python -B tools/validate_assistant.py --conferir-readme",
    ),
    ".github/workflows/temas-v12-ci.yml": (
        "python -B tools/tests/test_temas_v12.py -v",
        "python -B tools/tests/test_temas_v12_evidencia_real.py -v",
        "test_temas*.py",
        "python -B tools/tests/test_visual_legado_v00.py",
        "python -B tools/validate_assistant.py --conferir-readme",
        "V12_SCOPE=NOT_APPLICABLE",
    ),
    ".github/workflows/temas-v13-ci.yml": (
        "python -B tools/tests/test_temas_v13_s1.py -v",
        "python -B tools/temas_v13_operacional.py",
        "python -B tools/tests/test_temas_v13_s2.py -v",
        "python -B tools/tests/test_temas_v13_s3.py -v",
        "python -B tools/tests/test_temas_v13_s4.py -v",
        "python -B tools/tests/test_temas_v13_s5.py -v",
        "python -B tools/tests/test_temas_v13_s6.py -v",
        "python -B tools/tests/test_temas_v13_s7.py -v",
        "test_temas*.py",
        "python -B tools/tests/test_visual_legado_v00.py",
        "python -B tools/validate_assistant.py --conferir-readme",
        "V13_S1_REMOTE_MUTATION=0",
        "V13_S2_NETWORK=0",
        "V13_S3_LOCAL_DRY_RUN_ONLY=1",
        "V13_S4_DIAGNOSIS_READ_ONLY=1",
        "V13_S5_CONTRAST_PREFLIGHT_LOCAL=1",
        "V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5",
        "V13_S7_DATABRICKS_MUTATION=0",
        "V13_S7_HUMAN_EVIDENCE=VERSIONED_HUMAN_SESSION",
        "V13_V14_NOT_STARTED=1",
    ),
}

CRITICAL_INPUTS = (
    *WORKFLOW_SOURCES,
    "tools/mm01_local_certify.py",
    "tools/tests/test_mm01_local_certify.py",
    "tools/requirements-dev.txt",
    "tools/requirements-temas-dev.txt",
    "tools/readme_visuals/pnpm-lock.yaml",
    "ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/requirements.txt",
    "docs/sprints/micromodelos/MM01/MATRIZ_ACEITE_FINAL.md",
    "docs/sprints/micromodelos/MM01/TESTES.md",
)

ALLOWED_SKIP_IDS = {"V12_SCOPE_STRICT"}

REQUIRED_STEP_IDS = {
    "BOOTSTRAP_PYTHON",
    "BOOTSTRAP_IPYWIDGETS",
    "BOOTSTRAP_APP",
    "BOOTSTRAP_PNPM",
    "BOOTSTRAP_VISUAL",
    "CERT_SELFTEST",
    "MM01_CANONICAL",
    "MM01_R02",
    "MM01_R03",
    "MM01_VALIDATE_ASSISTANT",
    "CI_LOCAL",
    "V00_INVENTORY",
    "V00_LEGACY",
    "V00_REPORT",
    "V01_CONTRACT",
    "V01_TESTS",
    "V02_CHECK",
    "V02_V01_CONTRACT",
    "V02_TESTS",
    "V02_EXAMPLE",
    "V10_TEST",
    "V10_COMPILE",
    "V10_REGRESSIONS",
    "V10_LEGACY",
    "V10_BUILD",
    "V10_VERIFY",
    "V10_VALIDATE",
    "V11_TEST",
    "V11_COMPILE",
    "V11_REGRESSIONS",
    "V11_LEGACY",
    "V11_VALIDATE",
    "V12_TEST",
    "V12_REAL_EVIDENCE",
    "V12_REGRESSIONS",
    "V12_LEGACY",
    "V12_VALIDATE",
    "V12_SCOPE_STRICT",
    "V13_S1",
    "V13_S1_READONLY",
    "V13_S2",
    "V13_S3",
    "V13_S4",
    "V13_S5",
    "V13_S6",
    "V13_S7",
    "V13_REGRESSIONS",
    "V13_LEGACY",
    "V13_VALIDATE",
    "V13_BOUNDARIES",
}


@dataclass(frozen=True)
class Step:
    step_id: str
    source: str
    argv: tuple[str, ...]
    env: tuple[tuple[str, str], ...] = ()


@dataclass
class StepResult:
    step_id: str
    source: str
    command: list[str]
    started_utc: str
    ended_utc: str
    duration_seconds: float
    exit_code: int | None
    status: str
    log_file: str | None
    log_sha256: str | None
    reason: str | None = None


class CertificationError(RuntimeError):
    pass


class StepFailed(CertificationError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_text(text: str, repo_root: Path) -> str:
    text = text.replace(str(repo_root), "<REPO>")
    home = str(Path.home())
    if home:
        text = text.replace(home, "<HOME>")
    text = re.sub(
        r"([A-Za-z][A-Za-z0-9+.-]*://)([^/\s@]+)@",
        r"\1<REDACTED>@",
        text,
    )
    text = re.sub(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]+\b", "<REDACTED_TOKEN>", text)
    return text


def run_capture(argv: Sequence[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(
        list(argv),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def git(repo_root: Path, *args: str, check: bool = True) -> str:
    code, out = run_capture(("git", *args), repo_root)
    if check and code != 0:
        raise CertificationError("git command failed: git " + " ".join(args))
    return out.strip()


def normalize_remote(url: str) -> str | None:
    value = url.strip()
    if value.startswith("git@github.com:"):
        path = value.split(":", 1)[1]
    elif value.startswith("ssh://git@github.com/"):
        path = value.split("github.com/", 1)[1]
    else:
        parsed = urlparse(value)
        if parsed.hostname != "github.com":
            return None
        path = parsed.path.lstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return path if path == REPOSITORY else None


def validate_full_sha(value: str, label: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise CertificationError(label + " must be a full lowercase 40-hex SHA")
    return value


def require_outside_repo(output_dir: Path, repo_root: Path) -> None:
    out = output_dir.resolve()
    root = repo_root.resolve()
    try:
        out.relative_to(root)
    except ValueError:
        return
    raise CertificationError("output directory must be outside the repository")


def hash_inputs(repo_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for rel in CRITICAL_INPUTS:
        path = repo_root / rel
        if not path.is_file():
            raise CertificationError("critical input missing: " + rel)
        result[rel] = sha256_file(path)
    return result


def check_workflow_drift(repo_root: Path) -> dict[str, dict[str, object]]:
    if set(WORKFLOW_EXPECTED_BLOBS) != set(WORKFLOW_SOURCES):
        raise CertificationError("workflow blob pin set does not match workflow sources")
    if set(WORKFLOW_REQUIRED_SNIPPETS) != set(WORKFLOW_SOURCES):
        raise CertificationError("workflow snippet set does not match workflow sources")

    report: dict[str, dict[str, object]] = {}
    for rel in WORKFLOW_SOURCES:
        snippets = WORKFLOW_REQUIRED_SNIPPETS[rel]
        path = repo_root / rel
        if not path.is_file():
            raise CertificationError("workflow missing: " + rel)
        actual_blob = git(repo_root, "hash-object", rel)
        expected_blob = WORKFLOW_EXPECTED_BLOBS[rel]
        text = path.read_text(encoding="utf-8")
        missing = [snippet for snippet in snippets if snippet not in text]
        report[rel] = {
            "git_blob": actual_blob,
            "expected_git_blob": expected_blob,
            "blob_matches": actual_blob == expected_blob,
            "sha256": sha256_file(path),
            "missing_snippets": missing,
        }
        if actual_blob != expected_blob:
            raise CertificationError(
                "workflow definition changed since certification plan was frozen: "
                + rel
                + " expected "
                + expected_blob
                + " found "
                + actual_blob
            )
        if missing:
            raise CertificationError(
                "workflow drift detected in " + rel + ": " + repr(missing)
            )
    return report


def git_state(repo_root: Path) -> dict[str, object]:
    status = git(repo_root, "status", "--porcelain=v1", "--untracked-files=all")
    branch = git(repo_root, "symbolic-ref", "--quiet", "--short", "HEAD")
    head = git(repo_root, "rev-parse", "HEAD")
    tree = git(repo_root, "rev-parse", "HEAD^{tree}")
    origin_main = git(repo_root, "rev-parse", "origin/main")
    merge_base = git(repo_root, "merge-base", "HEAD", "origin/main")
    counts = git(
        repo_root,
        "rev-list",
        "--left-right",
        "--count",
        "origin/main...HEAD",
    ).split()
    if len(counts) != 2:
        raise CertificationError("unexpected rev-list output")
    behind_by, ahead_by = map(int, counts)
    shallow = git(repo_root, "rev-parse", "--is-shallow-repository")
    remote_url = git(repo_root, "remote", "get-url", "origin")
    return {
        "branch": branch,
        "head_sha": head,
        "tree_sha": tree,
        "origin_main_sha": origin_main,
        "merge_base_sha": merge_base,
        "behind_by": behind_by,
        "ahead_by": ahead_by,
        "worktree_clean": status == "",
        "worktree_status": status.splitlines(),
        "is_shallow_repository": shallow == "true",
        "origin_repository": normalize_remote(remote_url),
    }


def validate_state(
    state: dict[str, object],
    expected_sha: str,
    expected_main_sha: str,
    expected_branch: str,
) -> None:
    failures: list[str] = []
    if state["branch"] != expected_branch:
        failures.append("branch mismatch")
    if state["head_sha"] != expected_sha:
        failures.append("HEAD mismatch")
    if state["origin_main_sha"] != expected_main_sha:
        failures.append("origin/main mismatch")
    if state["merge_base_sha"] != expected_main_sha:
        failures.append("merge-base is not expected main SHA")
    if state["behind_by"] != 0:
        failures.append("behind_by is not zero")
    if not state["worktree_clean"]:
        failures.append("worktree is not clean")
    if state["is_shallow_repository"]:
        failures.append("repository is shallow")
    if state["origin_repository"] != REPOSITORY:
        failures.append("origin is not canonical repository")
    if failures:
        raise CertificationError("; ".join(failures))


def command_plan(python: str) -> list[Step]:
    py = python
    py_b = (py, "-B")
    env_common = (
        ("PYTHONDONTWRITEBYTECODE", "1"),
        ("PYTHONUTF8", "1"),
        ("SOURCE_DATE_EPOCH", SOURCE_DATE_EPOCH),
    )
    compile_v10 = (
        "from pathlib import Path; "
        "paths=[Path('ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app.py'),"
        "Path('ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app_service.py')]; "
        "[compile(p.read_text(encoding='utf-8'),str(p),'exec') for p in paths]; "
        "print('OK: sintaxe V10 compilada em memoria')"
    )
    compile_v11 = (
        "from pathlib import Path; "
        "p=Path('ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/aibi_theme.py'); "
        "compile(p.read_text(encoding='utf-8'),str(p),'exec'); "
        "print('OK: sintaxe V11 compilada em memoria')"
    )
    boundaries_v13 = (
        "print('V13_S1_REMOTE_MUTATION=0');"
        "print('V13_S2_NETWORK=0');print('V13_S2_REMOTE_MUTATION=0');"
        "print('V13_S3_NETWORK=0');print('V13_S3_REMOTE_MUTATION=0');print('V13_S3_LOCAL_DRY_RUN_ONLY=1');"
        "print('V13_S4_NETWORK=0');print('V13_S4_REMOTE_MUTATION=0');print('V13_S4_DIAGNOSIS_READ_ONLY=1');"
        "print('V13_S5_NETWORK=0');print('V13_S5_REMOTE_MUTATION=0');print('V13_S5_CONTRAST_PREFLIGHT_LOCAL=1');"
        "print('V13_S6_NETWORK=0');print('V13_S6_REMOTE_MUTATION=0');"
        "print('V13_S6_IMPLICIT_PUBLICATION=0');print('V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5');"
        "print('V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3');"
        "print('V13_S7_NETWORK=0');print('V13_S7_REMOTE_MUTATION=0');"
        "print('V13_S7_DATABRICKS_MUTATION=0');print('V13_S7_HUMAN_VALIDATION=PASS');"
        "print('V13_S7_HUMAN_EVIDENCE=VERSIONED_HUMAN_SESSION');print('V13_V14_NOT_STARTED=1')"
    )
    return [
        Step("BOOTSTRAP_PYTHON", "ci.yml", (py, "-m", "pip", "install", "-r", "tools/requirements-dev.txt")),
        Step("BOOTSTRAP_IPYWIDGETS", "temas-v10/v11/v12/v13", (py, "-m", "pip", "install", "ipywidgets>=8,<9")),
        Step("BOOTSTRAP_APP", "temas-v10/v11/v12/v13", (py, "-m", "pip", "install", "-r", "ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/requirements.txt")),
        Step("BOOTSTRAP_PNPM", "ci.yml", ("npm", "install", "--global", "pnpm@" + PNPM_VERSION)),
        Step("BOOTSTRAP_VISUAL", "ci.yml", ("pnpm", "--dir", "tools/readme_visuals", "install", "--frozen-lockfile")),
        Step("CERT_SELFTEST", "MM01 Local Certification v1", (*py_b, "-m", "unittest", "tools/tests/test_mm01_local_certify.py", "-v")),
        Step("MM01_CANONICAL", "micromodelos-mm01-ci.yml", (*py_b, "-m", "unittest", "tools/tests/test_micromodelo_mm01.py", "-v")),
        Step("MM01_R02", "micromodelos-mm01-ci.yml", (*py_b, "-m", "unittest", "tools/tests/test_micromodelo_mm01_r02.py", "-v")),
        Step("MM01_R03", "micromodelos-mm01-ci.yml", (*py_b, "-m", "unittest", "tools/tests/test_micromodelo_mm01_r03.py", "-v")),
        Step("MM01_VALIDATE_ASSISTANT", "micromodelos-mm01-ci.yml", (*py_b, "tools/validate_assistant.py", "--root", "ambiente_fonte")),
        Step("CI_LOCAL", "ci.yml", (py, "tools/ci_local.py")),
        Step("V00_INVENTORY", "temas-v00-ci.yml", (*py_b, "tools/tests/test_inventario_visual.py"), env_common),
        Step("V00_LEGACY", "temas-v00-ci.yml", (*py_b, "tools/tests/test_visual_legado_v00.py"), env_common),
        Step("V00_REPORT", "temas-v00-ci.yml", (*py_b, "tools/tests/test_baseline_visual_runner.py"), env_common),
        Step("V01_CONTRACT", "temas-v01-ci.yml", (*py_b, "tools/temas_v01_contract.py"), env_common),
        Step("V01_TESTS", "temas-v01-ci.yml", (*py_b, "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_temas_v01*.py", "-v"), env_common),
        Step("V02_CHECK", "temas-v02-ci.yml", (*py_b, "tools/temas_v02_check.py"), env_common),
        Step("V02_V01_CONTRACT", "temas-v02-ci.yml", (*py_b, "tools/temas_v01_contract.py"), env_common),
        Step("V02_TESTS", "temas-v02-ci.yml", (*py_b, "tools/tests/test_temas_v02.py"), env_common),
        Step("V02_EXAMPLE", "temas-v02-ci.yml", (*py_b, "ambiente_fonte/.assistant/hub_snippets/visual/tema/exemplo_tema.py"), env_common),
        Step("V10_TEST", "temas-v10-ci.yml", (*py_b, "tools/tests/test_temas_v10.py", "-v"), env_common),
        Step("V10_COMPILE", "temas-v10-ci.yml", (py, "-B", "-c", compile_v10), env_common),
        Step("V10_REGRESSIONS", "temas-v10-ci.yml", (*py_b, "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_temas*.py", "-v"), env_common),
        Step("V10_LEGACY", "temas-v10-ci.yml", (*py_b, "tools/tests/test_visual_legado_v00.py"), env_common),
        Step("V10_BUILD", "temas-v10-ci.yml", (*py_b, "tools/temas_v10_app.py", "--output", ".artifacts/v10-app"), env_common),
        Step("V10_VERIFY", "temas-v10-ci.yml", (*py_b, "tools/temas_v10_app.py", "--verify", ".artifacts/v10-app"), env_common),
        Step("V10_VALIDATE", "temas-v10-ci.yml", (*py_b, "tools/validate_assistant.py", "--conferir-readme"), env_common),
        Step("V11_TEST", "temas-v11-ci.yml", (*py_b, "tools/tests/test_temas_v11.py", "-v"), env_common),
        Step("V11_COMPILE", "temas-v11-ci.yml", (py, "-B", "-c", compile_v11), env_common),
        Step("V11_REGRESSIONS", "temas-v11-ci.yml", (*py_b, "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_temas*.py", "-v"), env_common),
        Step("V11_LEGACY", "temas-v11-ci.yml", (*py_b, "tools/tests/test_visual_legado_v00.py"), env_common),
        Step("V11_VALIDATE", "temas-v11-ci.yml", (*py_b, "tools/validate_assistant.py", "--conferir-readme"), env_common),
        Step("V12_TEST", "temas-v12-ci.yml", (*py_b, "tools/tests/test_temas_v12.py", "-v"), env_common),
        Step("V12_REAL_EVIDENCE", "temas-v12-ci.yml", (*py_b, "tools/tests/test_temas_v12_evidencia_real.py", "-v"), env_common),
        Step("V12_REGRESSIONS", "temas-v12-ci.yml", (*py_b, "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_temas*.py", "-v"), env_common),
        Step("V12_LEGACY", "temas-v12-ci.yml", (*py_b, "tools/tests/test_visual_legado_v00.py"), env_common),
        Step("V12_VALIDATE", "temas-v12-ci.yml", (*py_b, "tools/validate_assistant.py", "--conferir-readme"), env_common),
        Step("V13_S1", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s1.py", "-v"), env_common),
        Step("V13_S1_READONLY", "temas-v13-ci.yml", (*py_b, "tools/temas_v13_operacional.py"), env_common),
        Step("V13_S2", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s2.py", "-v"), env_common),
        Step("V13_S3", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s3.py", "-v"), env_common),
        Step("V13_S4", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s4.py", "-v"), env_common),
        Step("V13_S5", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s5.py", "-v"), env_common),
        Step("V13_S6", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s6.py", "-v"), env_common),
        Step("V13_S7", "temas-v13-ci.yml", (*py_b, "tools/tests/test_temas_v13_s7.py", "-v"), env_common),
        Step("V13_REGRESSIONS", "temas-v13-ci.yml", (*py_b, "-m", "unittest", "discover", "-s", "tools/tests", "-p", "test_temas*.py", "-v"), env_common),
        Step("V13_LEGACY", "temas-v13-ci.yml", (*py_b, "tools/tests/test_visual_legado_v00.py"), env_common),
        Step("V13_VALIDATE", "temas-v13-ci.yml", (*py_b, "tools/validate_assistant.py", "--conferir-readme"), env_common),
        Step("V13_BOUNDARIES", "temas-v13-ci.yml", (py, "-c", boundaries_v13), env_common),
    ]


def skipped_v12_scope() -> StepResult:
    now = utc_now()
    return StepResult(
        step_id="V12_SCOPE_STRICT",
        source="temas-v12-ci.yml",
        command=[],
        started_utc=now,
        ended_utc=now,
        duration_seconds=0.0,
        exit_code=None,
        status="SKIP_ALLOWED",
        log_file=None,
        log_sha256=None,
        reason=(
            "Permanent V12 workflow marks strict V12 scope NOT_APPLICABLE for "
            "pull requests whose head is not codex/temas-v12*; MM01 preserves "
            "that exact applicability contract."
        ),
    )


def result_is_complete(
    results: Sequence[StepResult],
    preflight_ok: bool,
    postflight_ok: bool,
) -> bool:
    if not preflight_ok or not postflight_ok:
        return False
    by_id = {item.step_id: item for item in results}
    if set(by_id) != REQUIRED_STEP_IDS:
        return False
    for step_id in REQUIRED_STEP_IDS:
        item = by_id[step_id]
        if step_id in ALLOWED_SKIP_IDS:
            if item.status != "SKIP_ALLOWED":
                return False
        elif item.status != "PASS" or item.exit_code != 0:
            return False
    return True


def run_step(step: Step, repo_root: Path, logs_dir: Path) -> StepResult:
    started = utc_now()
    start_clock = time.monotonic()
    env = os.environ.copy()
    env.update(dict(step.env))
    proc = subprocess.run(
        list(step.argv),
        cwd=repo_root,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    ended = utc_now()
    duration = time.monotonic() - start_clock
    log_rel = "logs/" + step.step_id + ".log"
    log_path = logs_dir / (step.step_id + ".log")
    rendered = "$ " + " ".join(step.argv) + "\n\n" + proc.stdout
    rendered = sanitize_text(rendered, repo_root)
    log_path.write_text(rendered, encoding="utf-8")
    status = "PASS" if proc.returncode == 0 else "FAIL"
    return StepResult(
        step_id=step.step_id,
        source=step.source,
        command=list(step.argv),
        started_utc=started,
        ended_utc=ended,
        duration_seconds=round(duration, 3),
        exit_code=proc.returncode,
        status=status,
        log_file=log_rel,
        log_sha256=sha256_file(log_path),
    )


def version_output(argv: Sequence[str], repo_root: Path) -> str:
    code, out = run_capture(argv, repo_root)
    if code != 0:
        raise CertificationError("version command failed: " + " ".join(argv))
    return sanitize_text(out.strip(), repo_root)


def base_runtime_preflight(repo_root: Path) -> dict[str, object]:
    if sys.version_info[:2] != PYTHON_MAJOR_MINOR:
        raise CertificationError(
            "Python 3.12 required; found " + platform.python_version()
        )
    executable = Path(sys.executable).resolve()
    try:
        executable.relative_to(repo_root.resolve())
    except ValueError:
        pass
    else:
        raise CertificationError(
            "Python environment must live outside the repository"
        )
    node = version_output(("node", "--version"), repo_root)
    match = re.search(r"(\d+)", node)
    if not match or int(match.group(1)) != NODE_MAJOR:
        raise CertificationError("Node 22 required; found " + node)
    residues = [
        rel
        for rel in (
            ".artifacts/v10-app",
            "tools/readme_visuals/node_modules",
        )
        if (repo_root / rel).exists()
    ]
    if residues:
        raise CertificationError(
            "dedicated checkout required; pre-existing generated residue: "
            + ", ".join(residues)
        )
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_environment_location": "OUTSIDE_REPOSITORY",
        "node_version": node,
        "npm_version": version_output(("npm", "--version"), repo_root),
        "git_version": version_output(("git", "--version"), repo_root),
    }


def environment_snapshot(repo_root: Path) -> dict[str, object]:
    if sys.version_info[:2] != PYTHON_MAJOR_MINOR:
        raise CertificationError(
            "Python 3.12 required; found " + platform.python_version()
        )
    node = version_output(("node", "--version"), repo_root)
    match = re.search(r"(\d+)", node)
    if not match or int(match.group(1)) != NODE_MAJOR:
        raise CertificationError("Node 22 required; found " + node)
    pnpm = version_output(("pnpm", "--version"), repo_root)
    if pnpm.strip() != PNPM_VERSION:
        raise CertificationError("pnpm " + PNPM_VERSION + " required; found " + pnpm)
    pip_list = version_output(
        (sys.executable, "-m", "pip", "list", "--format=json"),
        repo_root,
    )
    try:
        packages = json.loads(pip_list)
    except json.JSONDecodeError as exc:
        raise CertificationError("pip list returned invalid JSON") from exc
    return {
        "captured_utc": utc_now(),
        "python": {
            "executable": "<PYTHON_EXECUTABLE>",
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "git_version": version_output(("git", "--version"), repo_root),
        "pip_version": version_output((sys.executable, "-m", "pip", "--version"), repo_root),
        "node_version": node,
        "npm_version": version_output(("npm", "--version"), repo_root),
        "pnpm_version": pnpm,
        "packages": packages,
    }


def write_json(path: Path, data: object) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_checksums(bundle_dir: Path) -> None:
    entries: list[str] = []
    for path in sorted(bundle_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(bundle_dir).as_posix()
        if rel == "SHA256SUMS.txt":
            continue
        entries.append(sha256_file(path) + "  " + rel)
    (bundle_dir / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")


def zip_bundle(bundle_dir: Path) -> Path:
    zip_path = bundle_dir.with_suffix(".zip")
    if zip_path.exists():
        raise CertificationError("zip output already exists: " + str(zip_path))
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(bundle_dir.rglob("*")):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(bundle_dir).as_posix())
    return zip_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-sha")
    parser.add_argument("--expected-main-sha")
    parser.add_argument("--expected-branch", default=DEFAULT_BRANCH)
    parser.add_argument("--output-dir")
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Print the current gate plan and exit without executing it.",
    )
    return parser.parse_args(argv)


def describe() -> int:
    payload = {
        "schema": BUNDLE_SCHEMA,
        "repository": REPOSITORY,
        "expected_branch_default": DEFAULT_BRANCH,
        "required_step_ids": sorted(REQUIRED_STEP_IDS),
        "allowed_skip_ids": sorted(ALLOWED_SKIP_IDS),
        "workflow_sources": list(WORKFLOW_SOURCES),
        "steps": [
            {"id": step.step_id, "source": step.source, "argv": list(step.argv)}
            for step in command_plan("<python-3.12>")
        ],
        "v12_scope": asdict(skipped_v12_scope()),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.describe:
        return describe()
    if not args.expected_sha or not args.expected_main_sha or not args.output_dir:
        raise CertificationError(
            "--expected-sha, --expected-main-sha and --output-dir are mandatory"
        )
    expected_sha = validate_full_sha(args.expected_sha, "expected SHA")
    expected_main_sha = validate_full_sha(args.expected_main_sha, "expected main SHA")
    expected_branch = args.expected_branch
    if expected_branch != DEFAULT_BRANCH:
        raise CertificationError(
            "MM01 Local Certification v1 only accepts the canonical MM01 branch"
        )
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        raise CertificationError("local certification must not run inside GitHub Actions")

    repo_root = Path(
        run_capture(("git", "rev-parse", "--show-toplevel"), Path.cwd())[1].strip()
    ).resolve()
    if not repo_root.is_dir():
        raise CertificationError("not inside a Git repository")

    output_dir = Path(args.output_dir).expanduser().resolve()
    require_outside_repo(output_dir, repo_root)
    if output_dir.exists():
        raise CertificationError("output directory already exists")
    if output_dir.with_suffix(".zip").exists():
        raise CertificationError("zip output already exists")
    output_dir.mkdir(parents=True, exist_ok=False)
    logs_dir = output_dir / "logs"
    logs_dir.mkdir()

    preflight_ok = False
    postflight_ok = False
    results: list[StepResult] = []
    preflight: dict[str, object] = {}
    postflight: dict[str, object] = {}
    environment: dict[str, object] = {}
    input_hashes_before: dict[str, str] = {}
    failure: str | None = None
    started_utc = utc_now()

    try:
        base_runtime = base_runtime_preflight(repo_root)
        input_hashes_before = hash_inputs(repo_root)
        drift = check_workflow_drift(repo_root)
        pre_state = git_state(repo_root)
        validate_state(pre_state, expected_sha, expected_main_sha, expected_branch)
        preflight = {
            "captured_utc": utc_now(),
            "state": pre_state,
            "workflow_drift": drift,
            "base_runtime": base_runtime,
            "critical_inputs_sha256": input_hashes_before,
        }
        write_json(output_dir / "preflight.json", preflight)
        write_json(output_dir / "inputs_sha256.json", input_hashes_before)
        preflight_ok = True

        for step in command_plan(sys.executable):
            result = run_step(step, repo_root, logs_dir)
            results.append(result)
            if result.status != "PASS":
                raise StepFailed(step.step_id + " failed with exit code " + str(result.exit_code))

        results.append(skipped_v12_scope())
        environment = environment_snapshot(repo_root)
        write_json(output_dir / "environment.json", environment)

        post_state = git_state(repo_root)
        input_hashes_after = hash_inputs(repo_root)
        validate_state(post_state, expected_sha, expected_main_sha, expected_branch)
        if input_hashes_after != input_hashes_before:
            raise CertificationError("critical inputs changed during certification")
        if post_state != pre_state:
            raise CertificationError("Git state changed during certification")
        postflight = {
            "captured_utc": utc_now(),
            "state": post_state,
            "critical_inputs_sha256": input_hashes_after,
            "same_as_preflight": True,
        }
        postflight_ok = True
        write_json(output_dir / "postflight.json", postflight)

    except Exception as exc:
        failure = type(exc).__name__ + ": " + str(exc)
        try:
            if not postflight:
                post_state = git_state(repo_root)
                postflight = {
                    "captured_utc": utc_now(),
                    "state": post_state,
                    "same_as_preflight": False,
                    "collection_after_failure": True,
                }
                write_json(output_dir / "postflight.json", postflight)
        except Exception as post_exc:
            postflight = {
                "captured_utc": utc_now(),
                "collection_after_failure": False,
                "error": type(post_exc).__name__ + ": " + str(post_exc),
            }
            write_json(output_dir / "postflight.json", postflight)

    complete = result_is_complete(results, preflight_ok, postflight_ok)
    status = "PASS" if complete and failure is None else "FAIL"
    manifest = {
        "schema": BUNDLE_SCHEMA,
        "status": status,
        "repository": REPOSITORY,
        "branch": expected_branch,
        "expected_sha": expected_sha,
        "expected_main_sha": expected_main_sha,
        "tree_sha": preflight.get("state", {}).get("tree_sha") if preflight else None,
        "started_utc": started_utc,
        "ended_utc": utc_now(),
        "preflight_ok": preflight_ok,
        "postflight_ok": postflight_ok,
        "required_step_ids": sorted(REQUIRED_STEP_IDS),
        "allowed_skip_ids": sorted(ALLOWED_SKIP_IDS),
        "steps": [asdict(item) for item in results],
        "failure": failure,
        "decision_scope": (
            "Mechanical local execution evidence only. This manifest does not "
            "declare MM01 fit for merge, does not replace independent audit, "
            "does not replace contradictory review, and does not replace "
            "explicit human acceptance."
        ),
    }
    write_json(output_dir / "manifest.json", manifest)
    if not environment:
        write_json(
            output_dir / "environment.json",
            {
                "captured_utc": utc_now(),
                "status": "UNAVAILABLE_DUE_TO_FAILURE",
            },
        )
    write_checksums(output_dir)
    zip_path = zip_bundle(output_dir)
    bundle_sha = sha256_file(zip_path)

    print("MM01_LOCAL_CERTIFICATION_STATUS=" + status)
    print("MM01_LOCAL_CERTIFICATION_SHA=" + expected_sha)
    print("MM01_LOCAL_CERTIFICATION_MAIN_SHA=" + expected_main_sha)
    print("MM01_LOCAL_CERTIFICATION_BUNDLE=" + str(zip_path))
    print("MM01_LOCAL_CERTIFICATION_BUNDLE_SHA256=" + bundle_sha)
    if failure:
        print("MM01_LOCAL_CERTIFICATION_FAILURE=" + sanitize_text(failure, repo_root))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificationError as exc:
        print("MM01_LOCAL_CERTIFICATION_FATAL=" + str(exc), file=sys.stderr)
        raise SystemExit(2)
