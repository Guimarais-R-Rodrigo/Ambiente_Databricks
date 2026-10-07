"""Validação estrutural SER01 em overlay; nunca aplica objetos ao produto original.

Este entrypoint é repo-side, não uma API publicada no Databricks. A policy fica
em L2. O registro emitido não é um Receipt EDA V1, não autentica pessoas e não
prova execução de notebook. Os processos usam o supervisor canônico já integrado.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import platform
import re
import sys
import types
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
VERSION = "SER01-OBJECT-PACKAGE-1"
RECORD_VERSION = "SER01-LOCAL-VALIDATION-1"
MAX_FILES = 4
MAX_BYTES = 2 * 1024 * 1024
TYPES = {"snippet", "script", "prompt", "readme", "notebook", "skill"}
SECTIONS = {"constants", "display", "ml", "spark", "testing", "visual"}
TOOL = "tools/skill_enforcement/ser01_object_validation.py"
PREFLIGHT = "ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/scripts/preflight.py"
POLICY = "ambiente_databricks/.assistant/hub_padroes/skill_enforcement/policy.json"
DOMAIN_RECEIPT = "ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/scripts/object_validation.py"
REQUIRED_COMMANDS = {"identity_before", "status_before", "history", "preflight",
                     "baseline_validator", "clone", "checkout", "stage", "validator",
                     "overlay_head", "overlay_index", "overlay_diff", "overlay_untracked",
                     "identity_after", "status_after"}


class Blocked(ValueError):
    """Pré-condição/escopo ausente: não equivale a erro interno ignorado."""


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _api_stdout_lf(text: str) -> str:
    """Desfaz só o CRLF do stdout textual (Windows); CR isolado e bytes extras ficam."""
    return text.replace("\r\n", "\n")


def loads_strict(text: str) -> Any:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Blocked("DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def constant(_):
        raise Blocked("NONFINITE_JSON_VALUE")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_relative(value: Any) -> PurePosixPath:
    """Subconjunto portátil, sem normalizar silenciosamente nomes ambíguos."""
    if not isinstance(value, str) or not value or value != value.strip():
        raise Blocked("PATH_INVALID")
    parts = value.split("/")
    if (PurePosixPath(value).is_absolute() or PureWindowsPath(value).drive
            or "\\" in value or any(p in ("", ".", "..") for p in parts)):
        raise Blocked("PATH_INVALID")
    for part in parts:
        if (part.startswith(".") or part.endswith((".", " "))
                or not re.fullmatch(r"[A-Za-z0-9_.-]+", part)
                or re.fullmatch(r"(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?", part, re.I)):
            raise Blocked("PATH_INVALID")
    return PurePosixPath(value)


def _no_aliases(path: Path) -> None:
    for item in (path, *path.parents):
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise Blocked("TOPOLOGY_UNSUPPORTED")


def inspect_candidate(candidate: Any) -> dict[str, Any]:
    """Inspeciona somente envelope/bytes. Não chama isso de validação L3."""
    if not isinstance(candidate, dict) or set(candidate) - {
        "candidate_version", "base_sha", "context", "files", "document"
    }:
        raise Blocked("CANDIDATE_FIELDS_INVALID")
    if candidate.get("candidate_version") != VERSION:
        raise Blocked("CANDIDATE_VERSION_UNSUPPORTED")
    if not isinstance(candidate.get("base_sha"), str) or not re.fullmatch(
        r"[0-9a-f]{40}", candidate["base_sha"]
    ):
        raise Blocked("BASE_SHA_INVALID")
    context = candidate.get("context")
    if not isinstance(context, dict):
        raise Blocked("CONTEXT_REQUIRED")
    allowed = {"operation", "object_type", "object_name", "type_confirmed",
               "existing_capability_checked", "existing_capability_status",
               "overlap_resolution", "snippet_section", "readme_scale",
               "destination_relative", "source_relative"}
    if set(context) - allowed:
        raise Blocked("CONTEXT_FIELDS_UNSUPPORTED")
    if not isinstance(context.get("operation"), str) or context["operation"] not in {"create", "convert"}:
        raise Blocked("OPERATION_INVALID")
    if context["operation"] == "convert":
        raise Blocked("CONVERSION_NOT_IMPLEMENTED_IN_A1")
    kind = context.get("object_type")
    if not isinstance(kind, str) or kind not in TYPES:
        raise Blocked("OBJECT_TYPE_INVALID")
    if kind == "skill":
        raise Blocked("SKILL_CREATION_REQUIRES_CATALOG_POLICY_DECISION")
    if context.get("type_confirmed") is not True or context.get("existing_capability_checked") is not True:
        raise Blocked("HUMAN_CONTEXT_REQUIRED")
    capability = context.get("existing_capability_status")
    if not isinstance(capability, str) or capability not in {"not_found", "found"}:
        raise Blocked("CAPABILITY_STATUS_INVALID")
    if capability == "found" and context.get("overlap_resolution") != "create_declared_slice":
        raise Blocked("OVERLAP_DECISION_REQUIRED")
    if "source_relative" in context:
        raise Blocked("SOURCE_NOT_ALLOWED_FOR_CREATE")
    name = context.get("object_name")
    if not isinstance(name, str) or not name or name != name.strip():
        raise Blocked("OBJECT_NAME_INVALID")
    if kind in {"snippet", "script", "prompt"} and not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise Blocked("OBJECT_NAME_INVALID")
    grouped = kind in {"snippet", "script", "prompt"}
    if kind == "snippet":
        section = context.get("snippet_section")
        if not isinstance(section, str) or section not in SECTIONS:
            raise Blocked("SNIPPET_SECTION_UNSUPPORTED")
        destination = f"hub_snippets/{section}/{name}"
    elif kind == "script":
        destination = f"hub_scripts/{name}"
    elif kind == "prompt":
        destination = f"hub_prompts/{name}"
    else:
        destination = str(safe_relative(context.get("destination_relative")))
    if grouped and "destination_relative" in context and context["destination_relative"] != destination:
        raise Blocked("DESTINATION_CONTEXT_MISMATCH")
    if kind == "readme":
        if context.get("readme_scale") != "agregador":
            raise Blocked("STANDALONE_OBJECT_README_NOT_SUPPORTED_IN_A1")
        if PurePosixPath(destination).name != "README.md":
            raise Blocked("README_DESTINATION_INVALID")
        if not isinstance(candidate.get("document"), dict):
            raise Blocked("AGGREGATOR_DOCUMENT_REQUIRED")
    elif "readme_scale" in context or "document" in candidate:
        raise Blocked("README_FIELDS_NOT_APPLICABLE")
    if kind != "snippet" and "snippet_section" in context:
        raise Blocked("SNIPPET_FIELDS_NOT_APPLICABLE")
    if kind == "notebook" and PurePosixPath(destination).suffix != ".py":
        raise Blocked("NOTEBOOK_DESTINATION_INVALID")
    safe_relative(destination)
    if grouped:
        names = {"README.md", f"exemplo_{name}.py", name + (".md" if kind == "prompt" else ".py")}
        if kind != "prompt":
            names.add("__init__.py")
        expected = {destination + "/" + filename for filename in names}
    else:
        expected = {destination}
    files = candidate.get("files")
    if not isinstance(files, dict) or not 1 <= len(files) <= MAX_FILES:
        raise Blocked("FILES_INVALID")
    if set(files) != expected:
        raise Blocked("PACKAGE_FILES_MISMATCH")
    bindings = []
    size = 0
    for path, text in sorted(files.items()):
        safe_relative(path)
        if not isinstance(text, str) or not text.endswith("\n") or "\r" in text or "\x00" in text:
            raise Blocked("CONTENT_REQUIRES_UTF8_LF")
        try:
            raw = text.encode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise Blocked("CONTENT_INVALID_UTF8") from exc
        size += len(raw)
        bindings.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)})
    if size > MAX_BYTES:
        raise Blocked("PACKAGE_TOO_LARGE")
    # Também recusa NaN e tipos Python que não pertencem à interface JSON.
    try:
        candidate_hash = digest(candidate)
    except (ValueError, TypeError, UnicodeError) as exc:
        raise Blocked("CANDIDATE_NOT_FINITE_JSON") from exc
    return {"operation": "create", "object_type": kind, "destination_relative": destination,
            "grouped": grouped, "files": bindings, "candidate_sha256": candidate_hash,
            "base_sha": candidate["base_sha"]}


def _runtime():
    # Reuso explícito do supervisor F-04/A07; não há uma segunda implementação
    # de terminate/wait/cleanup, nem Receipt EDA com numeric_columns inventado.
    if str(ROOT / "tools") not in sys.path:
        sys.path.insert(0, str(ROOT / "tools"))
    from skill_enforcement import validate_create_readme
    return validate_create_readme, validate_create_readme._process_runner()


def _seal(report: dict[str, Any]) -> dict[str, Any]:
    report.pop("record_id", None)
    body = {k: v for k, v in report.items() if k != "object_validation_receipt"}
    report["record_id"] = "ser01v1:" + digest(body)
    return report


def _domain_receipt_module():
    path = ROOT / DOMAIN_RECEIPT
    name = "_ser01_object_validation_receipt_" + uuid.uuid4().hex
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    try:
        exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
        return module
    finally:
        sys.modules.pop(name, None)


def verify_record(report: Any, candidate: Any, *, expected_base_sha: str,
                  expected_run_id: str) -> dict[str, Any]:
    """Integridade/binding, NÃO reverificação de execução nem autenticação."""
    issues = []
    try:
        envelope = inspect_candidate(candidate)
        if not isinstance(report, dict):
            raise Blocked("RECORD_INVALID")
        body = {k: v for k, v in report.items() if k not in {"record_id", "object_validation_receipt"}}
        if report.get("record_id") != "ser01v1:" + digest(body):
            issues.append("RECORD_DIGEST_MISMATCH")
        if report.get("record_version") != RECORD_VERSION:
            issues.append("RECORD_VERSION_UNSUPPORTED")
        if report.get("run_id") != expected_run_id or not expected_run_id:
            issues.append("RUN_BINDING_MISMATCH")
        if report.get("binding") != envelope or envelope["base_sha"] != expected_base_sha:
            issues.append("INPUT_BINDING_MISMATCH")
        if report.get("status") != "PASS" or report.get("issues") != []:
            issues.append("VALIDATION_NOT_PASS")
        if report.get("writes_performed_in_original") is not False or report.get("homologated") is not False:
            issues.append("EFFECT_OR_HOMOLOGATION_CLAIM_INVALID")
        if report.get("runtime_validation") != "NOT_RUN":
            issues.append("RUNTIME_CLAIM_OUTSIDE_SCOPE")
        before = report.get("original_before")
        if not isinstance(before, dict) or before != report.get("original_after") or before.get("status") != "":
            issues.append("ORIGINAL_PRESERVATION_NOT_PROVEN")
        if isinstance(before, dict) and before.get("head") != expected_base_sha:
            issues.append("BASE_BINDING_MISMATCH")
        commands = report.get("commands")
        if not isinstance(commands, list):
            issues.append("COMMAND_EVIDENCE_MISSING")
        else:
            names = [c.get("name") for c in commands if isinstance(c, dict)]
            required = REQUIRED_COMMANDS | ({"api_publica"} if envelope["object_type"] in {"snippet", "script"} else set())
            if len(names) != len(commands) or len(set(names)) != len(names) or not required <= set(names):
                issues.append("COMMAND_COVERAGE_INVALID")
            if any(c.get("exit_code") != 0 or c.get("process_cleanup") != "COMPLETE"
                   or c.get("command_started") is not True or type(c.get("exit_code")) is not int
                   for c in commands if isinstance(c, dict)):
                issues.append("COMMAND_NOT_COMPLETE")
            if required <= set(names):
                order = ["preflight", "baseline_validator", "clone", "checkout", "stage", "validator",
                         "overlay_head", "overlay_index", "overlay_diff", "overlay_untracked",
                         "identity_after", "status_after"]
                if [names.index(x) for x in order] != sorted(names.index(x) for x in order):
                    issues.append("COMMAND_ORDER_INVALID")
        checks = report.get("checks")
        if not isinstance(checks, list) or not checks or any(c.get("status") != "PASS" for c in checks):
            issues.append("CHECKS_NOT_PASS")
        else:
            required_checks = {"destination_matches_preflight", "canonical_validator", "overlay_head_preserved",
                               "overlay_index_exact", "overlay_no_other_changes", "overlay_bytes_exact",
                               "original_preserved"}
            if envelope["object_type"] in {"snippet", "script"}:
                required_checks.add("canonical_public_api")
            if envelope["object_type"] == "readme":
                required_checks.add("canonical_aggregator_check")
            check_names = [c.get("name") for c in checks]
            if len(check_names) != len(set(check_names)) or not required_checks <= set(check_names):
                issues.append("CHECK_COVERAGE_INVALID")
        if (report.get("execution_authenticated") is not False
                or report.get("policy_promotion_authorized") is not False
                or report.get("scope") != "CREATE_PACKAGE_LOCAL_STRUCTURAL_VALIDATION_ONLY"):
            issues.append("AUTHORITY_OR_SCOPE_OVERCLAIM")
        if report.get("status") == "PASS":
            receipt_result = _domain_receipt_module().verify_receipt(
                report.get("object_validation_receipt"), local_record=report,
                expected_run_id=expected_run_id, expected_base_sha=expected_base_sha,
                expected_candidate_sha256=envelope["candidate_sha256"])
            if receipt_result.get("valid") is not True:
                issues.append("OBJECT_VALIDATION_RECEIPT_INVALID")
    except (ValueError, TypeError, KeyError, AttributeError, UnicodeError) as exc:
        issues.append("MALFORMED_RECORD:" + type(exc).__name__)
    return {"valid": not issues, "issues": issues, "verification_scope": "INTEGRITY_ONLY",
            "execution_reverified": False, "human_authority_authenticated": False,
            "policy_promotion_authorized": False}


def validate_package(candidate: Any, *, repo_root: Path, evidence_dir: Path,
                     evidence_authorized: bool = False) -> dict[str, Any]:
    report: dict[str, Any] = {
        "record_version": RECORD_VERSION, "run_id": uuid.uuid4().hex,
        "status": "BLOCKED", "started_at_utc": _utc(), "binding": None,
        "host": {"system": platform.system(), "release": platform.release(), "python": sys.version},
        "issues": [], "commands": [], "checks": [], "homologated": False,
        "runtime_validation": "NOT_RUN", "writes_performed_in_original": False,
        "scope": "CREATE_PACKAGE_LOCAL_STRUCTURAL_VALIDATION_ONLY",
        "execution_authenticated": False, "policy_promotion_authorized": False,
    }
    reserved = None
    runner = None
    repo = None
    original_started = False

    def check(name, ok, details=None):
        report["checks"].append({"name": name, "status": "PASS" if ok else "FAIL", "details": details})
        if not ok:
            raise RuntimeError(name)

    def run(name, argv, cwd, timeout=120):
        runner.REPO_ROOT = cwd
        runner.GIT_TIMEOUT_SECONDS = runner.STEP_TIMEOUT_SECONDS = timeout
        first = len(runner.PROCESS_RECORDS)
        row = {"name": name, "argv": list(map(str, argv)), "cwd": str(cwd), "started": _utc()}
        report["commands"].append(row)
        failure = None
        try:
            row["exit_code"], _, row["seconds"] = runner._run(row["argv"])
        except BaseException as exc:
            failure = exc
            row["exception"] = {"type": type(exc).__name__, "message": str(exc),
                                "winerror": getattr(exc, "winerror", None)}
        records = runner.PROCESS_RECORDS[first:]
        observation = copy.deepcopy(records[0]) if len(records) == 1 else {}
        row["command_started"] = observation.get("command_started")
        row["process_cleanup"] = observation.get("cleanup")
        row["process"] = observation
        row["ended"] = _utc()
        prefix = reserved / f"{len(report['commands']):02d}_{name}"
        for stream in ("stdout", "stderr"):
            raw = observation.get(stream, "").encode("utf-8")
            prefix.with_suffix("." + stream + ".txt").write_bytes(raw)
            row[stream + "_sha256"] = hashlib.sha256(raw).hexdigest()
        prefix.with_suffix(".json").write_bytes(_json_bytes(row) + b"\n")
        if failure is not None:
            raise failure
        if (row["command_started"] is not True or row["process_cleanup"] != "COMPLETE"
                or observation.get("utf8_valid") is not True or observation.get("result") != "EXITED"):
            raise RuntimeError("PROCESS_EVIDENCE_INCOMPLETE:" + name)
        return row["exit_code"], observation.get("stdout", "")

    def git(name, *args, cwd=None):
        code, output = run(name, ["git", "-c", f"core.hooksPath={os.devnull}", "-c",
                                  "core.quotepath=false", *args], cwd or repo)
        if code:
            raise RuntimeError("GIT_FAILED:" + name)
        return output.rstrip("\r\n")

    try:
        candidate = copy.deepcopy(candidate)
        binding = inspect_candidate(candidate)
        report["binding"] = binding
        if evidence_authorized is not True:
            raise Blocked("EVIDENCE_PERSISTENCE_NOT_AUTHORIZED")
        repo = Path(repo_root).absolute()
        evidence = Path(evidence_dir).absolute()
        _no_aliases(repo)
        _no_aliases(evidence)
        repo = repo.resolve(strict=True)
        if repo != ROOT.resolve(strict=True):
            raise Blocked("ENTRYPOINT_MUST_BELONG_TO_VALIDATED_CHECKOUT")
        if evidence.resolve().is_relative_to(repo) or repo.is_relative_to(evidence.resolve()):
            raise Blocked("EVIDENCE_MUST_BE_EXTERNAL")
        if not evidence.parent.is_dir() or os.path.lexists(evidence):
            raise Blocked("EVIDENCE_DIRECTORY_MUST_BE_NEW")
        evidence.mkdir(exist_ok=False)
        reserved = evidence
        legacy, runner = _runtime()
        report["original_before"] = {
            "head": git("identity_before", "rev-parse", "HEAD"),
            "status": git("status_before", "status", "--porcelain=v1", "--untracked-files=all"),
        }
        original_started = True
        if report["original_before"] != {"head": binding["base_sha"], "status": ""}:
            raise Blocked("BASE_MISMATCH_OR_DIRTY")
        if git("history", "rev-parse", "--is-shallow-repository") != "false":
            raise Blocked("COMPLETE_HISTORY_REQUIRED")
        report["base_tree"] = git("base_tree", "rev-parse", "HEAD^{tree}")
        report["source_hashes"] = {p: hashlib.sha256((repo / p).read_bytes()).hexdigest()
                                   for p in (TOOL, PREFLIGHT, POLICY, DOMAIN_RECEIPT, "tools/validate_assistant.py",
                                             "tools/skill_enforcement/validate_create_readme.py",
                                             "tools/skill_enforcement/certify_local.py")}
        code, output = run("preflight", [sys.executable, "-B", str(repo / PREFLIGHT),
                                          "--context-json", _json_bytes(candidate["context"]).decode("utf-8")], repo)
        preflight = loads_strict(output)
        if code or preflight.get("status") != "PASS":
            raise Blocked("CANONICAL_PREFLIGHT_BLOCKED")
        check("destination_matches_preflight", preflight.get("destination_relative") == binding["destination_relative"])
        assistant = repo / "ambiente_databricks/.assistant"
        destination = assistant.joinpath(*safe_relative(binding["destination_relative"]).parts)
        _no_aliases(destination)
        if os.path.lexists(destination) or not destination.parent.is_dir():
            raise Blocked("DESTINATION_MUST_BE_ABSENT_WITH_EXISTING_PARENT")
        template_rel = preflight.get("template", {}).get("path")
        template = assistant.joinpath(*safe_relative(template_rel).parts)
        _no_aliases(template)
        report["template"] = {"path": template_rel, "sha256": hashlib.sha256(template.read_bytes()).hexdigest(),
                              "read_status": "READ_BY_VALIDATOR", "conformance_scope": "CANONICAL_STRUCTURAL_CHECKS_ONLY"}
        code, _ = run("baseline_validator", [sys.executable, "-B", str(repo / "tools/validate_assistant.py")], repo)
        if code:
            raise Blocked("BASELINE_STRUCTURAL_GATE_FAILED")
        overlay = evidence / "overlay"
        git("clone", "clone", "--no-local", "--no-hardlinks", "--no-checkout", "--config", "core.autocrlf=false",
            "--", str(repo), str(overlay))
        git("checkout", "checkout", "--detach", binding["base_sha"], cwd=overlay)
        overlay_assistant = overlay / "ambiente_databricks/.assistant"
        target = overlay_assistant / binding["destination_relative"]
        _no_aliases(target)
        if binding["grouped"]:
            target.mkdir(exist_ok=False)
        for rel, text in candidate["files"].items():
            path = overlay_assistant.joinpath(*safe_relative(rel).parts)
            _no_aliases(path)
            with path.open("xb") as stream:
                stream.write(text.encode("utf-8"))
        repo_paths = ["ambiente_databricks/.assistant/" + p for p in sorted(candidate["files"])]
        git("stage", "add", "--", *repo_paths, cwd=overlay)
        # git add ocorre SOMENTE no clone; o inventário Git do validator vê
        # todos os bytes novos, em vez de certificar acidentalmente a base antiga.
        if binding["object_type"] in {"snippet", "script"}:
            name = candidate["context"]["object_name"]
            code, api = run("api_publica", [sys.executable, "-B", str(overlay / "tools/api_publica.py"),
                                            str(target / (name + ".py"))], overlay)
            check("canonical_public_api", code == 0 and _api_stdout_lf(api).encode("utf-8")
                  == (target / "__init__.py").read_bytes())
        if binding["object_type"] == "readme":
            details = legacy._readme_checks(candidate["files"][binding["destination_relative"]], target,
                                            candidate["document"], template.read_text(encoding="utf-8"))
            check("canonical_aggregator_check", details["status"] == "PASS", details)
        code, _ = run("validator", [sys.executable, "-B", str(overlay / "tools/validate_assistant.py")], overlay)
        check("canonical_validator", code == 0)
        check("overlay_head_preserved", git("overlay_head", "rev-parse", "HEAD", cwd=overlay) == binding["base_sha"])
        indexed = git("overlay_index", "diff", "--cached", "--name-status", "-z", cwd=overlay).split("\x00")
        if indexed and indexed[-1] == "":
            indexed.pop()
        check("overlay_index_exact", indexed == [item for path in sorted(repo_paths) for item in ("A", path)])
        check("overlay_no_other_changes", git("overlay_diff", "diff", "--name-only", cwd=overlay) == ""
              and git("overlay_untracked", "ls-files", "--others", "--exclude-standard", cwd=overlay) == "")
        check("overlay_bytes_exact", all((overlay_assistant / p).read_bytes() == text.encode("utf-8")
                                          for p, text in candidate["files"].items()))
        report["status"] = "PASS"
    except Blocked as exc:
        report["status"] = "BLOCKED"
        report["issues"].append(str(exc))
    except (KeyboardInterrupt, SystemExit) as exc:
        report["status"] = "FAIL"
        report["interrupted"] = True
        report["exit_code"] = 130
        report["issues"].append("INTERRUPTED:" + type(exc).__name__)
    except Exception as exc:
        report["status"] = "FAIL"
        report["issues"].append(type(exc).__name__ + ":" + str(exc))
    finally:
        if original_started:
            try:
                report["original_after"] = {
                    "head": git("identity_after", "rev-parse", "HEAD"),
                    "status": git("status_after", "status", "--porcelain=v1", "--untracked-files=all"),
                }
                check("original_preserved", report["original_before"] == report["original_after"])
            except BaseException as exc:
                report["status"] = "FAIL"
                report["issues"].append("ORIGINAL_POSTCHECK_FAILED:" + type(exc).__name__)
        report["ended_at_utc"] = _utc()
    _seal(report)
    if report["status"] == "PASS":
        try:
            domain_receipt = _domain_receipt_module().build_receipt(report)
            if domain_receipt is None:
                raise RuntimeError("DOMAIN_RECEIPT_BUILD_REJECTED")
            report["object_validation_receipt"] = domain_receipt
        except Exception as exc:
            report["status"] = "FAIL"
            report["issues"].append("DOMAIN_RECEIPT_FAILED:" + type(exc).__name__ + ":" + str(exc))
            report.pop("object_validation_receipt", None)
            _seal(report)
    if reserved is not None:
        try:
            pending = reserved / "validation.pending.json"
            with pending.open("xb") as stream:
                stream.write(_json_bytes(report) + b"\n")
            pending.rename(reserved / "validation.json")
        except BaseException as exc:
            report["status"] = "FAIL"
            report["issues"].append("EVIDENCE_PERSISTENCE_FAILED:" + type(exc).__name__)
            report.pop("object_validation_receipt", None)
            _seal(report)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--evidence-authorized", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.candidate.stat().st_size > 4 * MAX_BYTES:
            raise Blocked("INPUT_FILE_TOO_LARGE")
        candidate = loads_strict(args.candidate.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "issues": [type(exc).__name__ + ":" + str(exc)]}))
        return 2
    report = validate_package(candidate, repo_root=args.repo_root, evidence_dir=args.evidence_dir,
                              evidence_authorized=args.evidence_authorized)
    print(json.dumps(report, ensure_ascii=True, indent=2, allow_nan=False))
    return 0 if report["status"] == "PASS" else report.get("exit_code", 2 if report["status"] == "BLOCKED" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
