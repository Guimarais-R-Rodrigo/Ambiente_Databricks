from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from tools.skill_enforcement.parallel.contract import digest_json
from tools.skill_enforcement.parallel.host_probe import probe
from tools.skill_enforcement.parallel.process import ROOT
from tools.skill_enforcement.real_campaigns.b1.coverage import build_report
from tools.skill_enforcement.real_campaigns.b1.registry import load_registry

POLICY = ROOT / "ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json"
PARALLEL_ROOT = ROOT / "tools/skill_enforcement/parallel"
B0_BINDINGS = Path(__file__).with_name("b0_qualified_bindings.json")
ROUND_START_SCHEMA = "SER-B1-ROUND-START-1"
RELEASE_SPEC_SCHEMA = "SER-B1-RELEASE-SPEC-2"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=30)
    if p.returncode != 0:
        raise RuntimeError("GIT_FAILED:" + " ".join(args) + ":" + (p.stderr or "").strip())
    return p.stdout.strip()


def _git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _runtime_path_key(value: str) -> str:
    return os.path.normcase(os.path.normpath(value))


def _probe_python_launcher(python_launcher: str) -> dict[str, Any]:
    code = (
        "import json,platform,sys;"
        "print(json.dumps({"
        "'executable':sys.executable,"
        "'version':platform.python_version(),"
        "'implementation':platform.python_implementation(),"
        "'prefix':sys.prefix,"
        "'base_prefix':sys.base_prefix,"
        "'isolated':sys.prefix != sys.base_prefix"
        "},sort_keys=True))"
    )
    p = subprocess.run(
        [python_launcher, "-B", "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if p.returncode != 0:
        raise RuntimeError("B1_PYTHON_LAUNCHER_PROBE_FAILED:" + str(p.returncode))
    lines = [line.strip() for line in p.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("B1_PYTHON_LAUNCHER_PROBE_EMPTY")
    try:
        payload = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError("B1_PYTHON_LAUNCHER_PROBE_JSON_INVALID") from exc
    required = {"executable", "version", "implementation", "prefix", "base_prefix", "isolated"}
    if not isinstance(payload, dict) or set(payload) != required:
        raise RuntimeError("B1_PYTHON_LAUNCHER_PROBE_SHAPE_INVALID")
    if not all(isinstance(payload.get(k), str) and payload.get(k) for k in ("executable", "version", "implementation", "prefix", "base_prefix")):
        raise RuntimeError("B1_PYTHON_LAUNCHER_PROBE_FIELD_INVALID")
    if not isinstance(payload.get("isolated"), bool):
        raise RuntimeError("B1_PYTHON_LAUNCHER_PROBE_ISOLATION_INVALID")
    return payload


def _capture_python_binding(python_launcher: str) -> dict[str, Any]:
    if not isinstance(python_launcher, str) or not python_launcher:
        raise ValueError("B1_PYTHON_LAUNCHER_REQUIRED")
    launcher_path = Path(python_launcher)
    if not launcher_path.is_absolute():
        raise ValueError("B1_PYTHON_LAUNCHER_MUST_BE_ABSOLUTE")
    if not launcher_path.is_file():
        raise ValueError("B1_PYTHON_LAUNCHER_NOT_FILE")

    probe_payload = _probe_python_launcher(python_launcher)
    runtime_observed = str(Path(sys.executable).resolve())
    if probe_payload["version"] != platform.python_version():
        raise ValueError("B1_PYTHON_LAUNCHER_VERSION_MISMATCH")
    if probe_payload["implementation"] != platform.python_implementation():
        raise ValueError("B1_PYTHON_LAUNCHER_IMPLEMENTATION_MISMATCH")
    isolated = sys.prefix != sys.base_prefix
    if probe_payload["isolated"] is not isolated:
        raise ValueError("B1_PYTHON_LAUNCHER_ISOLATION_MISMATCH")

    launcher_sha = _sha256_file(launcher_path)
    probe_runtime_sha = _sha256_file(Path(probe_payload["executable"]))
    runtime_sha = _sha256_file(Path(runtime_observed))
    if len({launcher_sha, probe_runtime_sha, runtime_sha}) != 1:
        raise ValueError("B1_PYTHON_LAUNCHER_BINARY_MISMATCH")

    return {
        "python_executable": python_launcher,
        "python_runtime_executable_observed": runtime_observed,
        "python_executable_sha256": launcher_sha,
        "python_runtime_executable_sha256": runtime_sha,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_isolated": isolated,
    }


def _runtime_binding_issues(
    spec: Mapping[str, Any],
    *,
    current_executable: str | None = None,
    current_version: str | None = None,
    current_implementation: str | None = None,
    current_isolated: bool | None = None,
) -> list[str]:
    issues: list[str] = []
    observed = current_executable if current_executable is not None else str(Path(sys.executable).resolve())
    version = current_version if current_version is not None else platform.python_version()
    implementation = current_implementation if current_implementation is not None else platform.python_implementation()
    isolated = current_isolated if current_isolated is not None else (sys.prefix != sys.base_prefix)

    if version != spec.get("python_version"):
        issues.append("B1_RELEASE_PYTHON_VERSION_CHANGED")
    if implementation != spec.get("python_implementation"):
        issues.append("B1_RELEASE_PYTHON_IMPLEMENTATION_CHANGED")
    if isolated is not spec.get("python_isolated"):
        issues.append("B1_RELEASE_PYTHON_ISOLATION_CHANGED")

    try:
        runtime_sha = _sha256_file(Path(observed))
        if runtime_sha != spec.get("python_runtime_executable_sha256"):
            issues.append("B1_RELEASE_RUNTIME_BINARY_CHANGED")
    except OSError as exc:
        issues.append("B1_RELEASE_RUNTIME_BINARY_UNREADABLE:" + type(exc).__name__)

    launcher = spec.get("python_executable")
    try:
        if not isinstance(launcher, str) or not launcher:
            issues.append("B1_RELEASE_PYTHON_LAUNCHER_INVALID")
        else:
            launcher_sha = _sha256_file(Path(launcher))
            if launcher_sha != spec.get("python_executable_sha256"):
                issues.append("B1_RELEASE_PYTHON_LAUNCHER_CHANGED")
            if launcher_sha != spec.get("python_runtime_executable_sha256"):
                issues.append("B1_RELEASE_PYTHON_LAUNCHER_RUNTIME_DIGEST_MISMATCH")
    except OSError as exc:
        issues.append("B1_RELEASE_PYTHON_LAUNCHER_UNREADABLE:" + type(exc).__name__)
    return sorted(set(issues))


def _load_b0_bindings() -> dict[str, Any]:
    raw = json.loads(B0_BINDINGS.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "qualified_pr", "qualified_main", "files"}:
        raise ValueError("B0_BINDINGS_SHAPE_INVALID")
    if raw.get("schema_version") != "SER-B1-B0-QUALIFIED-BINDINGS-1":
        raise ValueError("B0_BINDINGS_SCHEMA_INVALID")
    if raw.get("qualified_pr") != 113 or raw.get("qualified_main") != "4ba7f551767d847381df1556ed937116258fa77d":
        raise ValueError("B0_BINDINGS_AUTHORITY_INVALID")
    files = raw.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("B0_BINDINGS_FILES_INVALID")
    for rel, sha in files.items():
        if not isinstance(rel, str) or not rel.startswith("tools/skill_enforcement/parallel/"):
            raise ValueError("B0_BINDINGS_PATH_INVALID")
        if not isinstance(sha, str) or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError("B0_BINDINGS_SHA_INVALID:" + rel)
    return raw


def qualified_b0_issues() -> list[str]:
    issues: list[str] = []
    try:
        bindings = _load_b0_bindings()
    except Exception as exc:
        return ["B0_QUALIFIED_BINDINGS_UNREADABLE:" + type(exc).__name__ + ":" + str(exc)]
    expected = bindings["files"]
    observed: set[str] = set()
    try:
        for path in PARALLEL_ROOT.rglob("*"):
            if path.is_symlink():
                issues.append("B0_QUALIFIED_SYMLINK_PRESENT:" + path.relative_to(ROOT).as_posix())
            elif path.is_file():
                observed.add(path.relative_to(ROOT).as_posix())
    except OSError as exc:
        issues.append("B0_QUALIFIED_TREE_UNREADABLE:" + type(exc).__name__)
        return sorted(set(issues))
    if observed != set(expected):
        missing = sorted(set(expected) - observed)
        extra = sorted(observed - set(expected))
        if missing:
            issues.append("B0_QUALIFIED_FILES_MISSING:" + ",".join(missing))
        if extra:
            issues.append("B0_QUALIFIED_FILES_EXTRA:" + ",".join(extra))
    for rel, expected_sha in expected.items():
        path = ROOT / rel
        try:
            if not path.is_file() or path.is_symlink():
                issues.append("B0_QUALIFIED_FILE_INVALID:" + rel)
            elif _git_blob(path) != expected_sha:
                issues.append("B0_QUALIFIED_BLOB_MISMATCH:" + rel)
        except OSError as exc:
            issues.append("B0_QUALIFIED_FILE_UNREADABLE:" + rel + ":" + type(exc).__name__)
    return sorted(set(issues))


def _b0_digest() -> str:
    issues = qualified_b0_issues()
    if issues:
        raise ValueError("B0_NOT_QUALIFIED:" + ",".join(issues))
    bindings = _load_b0_bindings()
    rows = [{"path": rel, "git_blob_sha1": sha} for rel, sha in sorted(bindings["files"].items())]
    return digest_json({
        "qualified_pr": bindings["qualified_pr"],
        "qualified_main": bindings["qualified_main"],
        "files": rows,
    })


def capture_round_start() -> dict[str, Any]:
    if _git("status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError("WORKTREE_NOT_CLEAN")
    if _git("rev-parse", "--is-shallow-repository") != "false":
        raise RuntimeError("SHALLOW_REPOSITORY")
    behind = int(_git("rev-list", "--count", "HEAD..origin/main") or "0")
    if behind:
        raise RuntimeError("CANDIDATE_BEHIND_ORIGIN_MAIN:" + str(behind))
    candidate = _git("rev-parse", "HEAD")
    return {
        "schema_version": ROUND_START_SCHEMA,
        "round_id": "B1ROUND-" + uuid.uuid4().hex,
        "candidate_sha": candidate,
        "candidate_tree_sha": _git("rev-parse", "HEAD^{tree}"),
        "baseline_sha": _git("merge-base", "HEAD", "origin/main"),
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "started_at_utc": _utc(),
    }


def build_release_spec(round_start: Mapping[str, Any], *, python_launcher: str) -> dict[str, Any]:
    coverage = build_report()
    if coverage.get("status") != "PASS":
        raise ValueError("B1_COVERAGE_NOT_PASS")
    host = probe()
    return {
        "schema_version": RELEASE_SPEC_SCHEMA,
        "round_id": round_start["round_id"],
        "candidate_sha": round_start["candidate_sha"],
        "candidate_tree_sha": round_start["candidate_tree_sha"],
        "baseline_sha": round_start["baseline_sha"],
        "branch": round_start["branch"],
        "command_registry_digest": digest_json(load_registry()),
        "coverage_digest": digest_json(coverage),
        "policy_before_digest": hashlib.sha256(POLICY.read_bytes()).hexdigest(),
        "host_digest": digest_json(host),
        "b0_mechanism_digest": _b0_digest(),
        "adapter_id": "SER-B1-ADAPTER-1",
        **_capture_python_binding(python_launcher),
        "platform": platform.platform(),
        "created_at_utc": _utc(),
    }


def validate_release_spec(spec: Any) -> list[str]:
    if not isinstance(spec, Mapping):
        return ["B1_RELEASE_SPEC_NOT_OBJECT"]
    required = {
        "schema_version", "round_id", "candidate_sha", "candidate_tree_sha", "baseline_sha",
        "branch", "command_registry_digest", "coverage_digest", "policy_before_digest",
        "host_digest", "b0_mechanism_digest", "adapter_id", "python_executable",
        "python_runtime_executable_observed", "python_executable_sha256",
        "python_runtime_executable_sha256", "python_version", "python_implementation",
        "python_isolated", "platform", "created_at_utc",
    }
    issues: list[str] = []
    if set(spec) != required:
        issues.append("B1_RELEASE_SPEC_KEYS_INVALID")
    if spec.get("schema_version") != RELEASE_SPEC_SCHEMA:
        issues.append("B1_RELEASE_SPEC_SCHEMA_INVALID")
    if spec.get("adapter_id") != "SER-B1-ADAPTER-1":
        issues.append("B1_RELEASE_ADAPTER_INVALID")
    for key in (
        "round_id", "branch", "python_executable", "python_runtime_executable_observed",
        "python_version", "python_implementation", "platform", "created_at_utc",
    ):
        if not isinstance(spec.get(key), str) or not spec.get(key):
            issues.append("B1_RELEASE_FIELD_INVALID:" + key)
    if not isinstance(spec.get("python_isolated"), bool):
        issues.append("B1_RELEASE_FIELD_INVALID:python_isolated")
    for key in ("candidate_sha", "candidate_tree_sha", "baseline_sha"):
        value = spec.get(key)
        if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
            issues.append("B1_RELEASE_SHA_INVALID:" + key)
    for key in (
        "command_registry_digest", "coverage_digest", "policy_before_digest",
        "host_digest", "b0_mechanism_digest", "python_executable_sha256",
        "python_runtime_executable_sha256",
    ):
        value = spec.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            issues.append("B1_RELEASE_DIGEST_INVALID:" + key)
    if (
        isinstance(spec.get("python_executable_sha256"), str)
        and isinstance(spec.get("python_runtime_executable_sha256"), str)
        and spec.get("python_executable_sha256") != spec.get("python_runtime_executable_sha256")
    ):
        issues.append("B1_RELEASE_PYTHON_BINDING_DIGEST_MISMATCH")
    return sorted(set(issues))


def assert_release_spec_current(spec: Mapping[str, Any]) -> list[str]:
    issues = validate_release_spec(spec)
    try:
        if _git("rev-parse", "HEAD") != spec.get("candidate_sha"):
            issues.append("B1_RELEASE_HEAD_CHANGED")
        if _git("rev-parse", "HEAD^{tree}") != spec.get("candidate_tree_sha"):
            issues.append("B1_RELEASE_TREE_CHANGED")
        if _git("merge-base", "HEAD", "origin/main") != spec.get("baseline_sha"):
            issues.append("B1_RELEASE_MERGE_BASE_CHANGED")
        if _git("status", "--porcelain=v1", "--untracked-files=all"):
            issues.append("B1_RELEASE_WORKTREE_DIRTY")
        if int(_git("rev-list", "--count", "HEAD..origin/main") or "0"):
            issues.append("B1_RELEASE_BEHIND_ORIGIN_MAIN")
    except Exception as exc:
        issues.append("B1_RELEASE_GIT_UNREADABLE:" + type(exc).__name__)
    try:
        if digest_json(load_registry()) != spec.get("command_registry_digest"):
            issues.append("B1_RELEASE_REGISTRY_CHANGED")
    except Exception as exc:
        issues.append("B1_RELEASE_REGISTRY_UNREADABLE:" + type(exc).__name__)
    try:
        coverage = build_report()
        if coverage.get("status") != "PASS" or digest_json(coverage) != spec.get("coverage_digest"):
            issues.append("B1_RELEASE_COVERAGE_CHANGED")
    except Exception as exc:
        issues.append("B1_RELEASE_COVERAGE_UNREADABLE:" + type(exc).__name__)
    try:
        if hashlib.sha256(POLICY.read_bytes()).hexdigest() != spec.get("policy_before_digest"):
            issues.append("B1_RELEASE_POLICY_CHANGED")
        issues.extend("B1_RELEASE_" + item for item in qualified_b0_issues())
        if not qualified_b0_issues() and _b0_digest() != spec.get("b0_mechanism_digest"):
            issues.append("B1_RELEASE_B0_MECHANISM_CHANGED")
        if digest_json(probe()) != spec.get("host_digest"):
            issues.append("B1_RELEASE_HOST_CHANGED")
    except Exception as exc:
        issues.append("B1_RELEASE_BINDING_UNREADABLE:" + type(exc).__name__)
    issues.extend(_runtime_binding_issues(spec))
    return sorted(set(issues))
