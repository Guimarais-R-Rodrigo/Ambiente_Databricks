"""Valida um candidato README em clone descartável; não escreve no produto original.

O PASS vincula bytes/base/destino a checks locais executados. Não autentica o
emissor, autoriza apply, certifica runtime Databricks ou executa renderer/FULL.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import traceback
import uuid
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ambiente_fonte/.assistant"))
sys.path.insert(0, str(ROOT / "tools"))
from hub_scripts.skill_execution.receipt import sha256_digest
from markdown_contract import anchors, markdown_links, mask_fences

VALIDATOR = "repo_side_create_readme_v1"
TEMPLATE = "hub_padroes/readme/template.md"
MANIFEST = "skills/hub-ml-criar-objeto/release_manifest.json"
BINDING_FIELDS = {"operation", "object_type", "readme_scale", "destination_relative",
                  "content_sha256", "content_size", "generation_id", "base_sha",
                  "release_sha256", "template_sha256"}


def _process_runner():
    """Reusa cleanup F-04 aceito, com globals privados desta validação."""
    name = "_create_readme_process_" + uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools/skill_enforcement/certify_local.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    return module


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _no_aliases(path):
    for item in [path, *path.parents]:
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError("TOPOLOGY_UNSUPPORTED:" + str(item))


def _relative(raw):
    if not isinstance(raw, str) or not raw or raw != raw.strip():
        raise ValueError("DESTINATION_INVALID")
    parts = raw.split("/")
    if (PurePosixPath(raw).is_absolute() or PureWindowsPath(raw).drive or "\\" in raw
            or any(p in ("", ".", "..") for p in parts) or any(c in raw for c in ":\x00\r\n")
            or any(p.endswith((".", " ")) or re.search(r'[<>"|?*\x00-\x1f]', p)
                   or re.fullmatch(r"(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?", p, re.I) for p in parts)
            or parts[-1] != "README.md"):
        raise ValueError("DESTINATION_INVALID")
    return PurePosixPath(raw)


def _destination(assistant, relative):
    target = assistant.joinpath(*relative.parts)
    _no_aliases(target)
    if not target.parent.is_dir() or target.exists():
        raise ValueError("DESTINATION_MUST_BE_ABSENT_IN_EXISTING_DIRECTORY")
    if not target.parent.resolve(strict=True).is_relative_to(assistant.resolve(strict=True)):
        raise ValueError("DESTINATION_ESCAPE")
    return target


def _readme_checks(content, target, document, template):
    """Forma/links/inventário do piloto, sem executar exemplos ou julgar a prosa.

    Até cinco diretórios filhos usa forma curta; acima disso exige a visão
    estrutural. Conteúdo humano pode incluir subtítulos, não novos títulos H2
    que se confundam com as seções determinísticas. Links seguem o parser
    conservador canônico, não uma promessa de cobertura CommonMark universal.
    """
    issues = []
    if "\r" in content or not content.endswith("\n") or "\x00" in content:
        issues.append("CONTENT_REQUIRES_UTF8_LF_FINAL_NEWLINE")
    visible = mask_fences(content)
    if len(re.findall(r"(?m)^# [^\n]+$", visible)) != 1:
        issues.append("AGGREGATOR_TITLE_REQUIRED")
    if "readme-objeto:" in content:
        issues.append("OBJECT_TEMPLATE_NOT_AGGREGATOR")
    # The selected short aggregator has the always-applicable template sections.
    headings = ["Para que serve / quando usar", "Como usar", "O que existe aqui",
                "Limites e armadilhas", "Onde continuar"]
    actual = re.findall(r"(?m)^## (.+?)\s*$", visible)
    positions = [next((i for i, title in enumerate(actual) if title.startswith(h)), -1) for h in headings]
    if -1 in positions or positions != sorted(set(positions)):
        issues.append("AGGREGATOR_SECTION_ORDER")
    if any(h not in template for h in headings):
        issues.append("AGGREGATOR_TEMPLATE_UNRECOGNIZED")
    if not re.search(r"(?m)^\|.*\|\s*\n\|[ :|\-]+\|", visible):
        issues.append("AGGREGATOR_INVENTORY_TABLE_REQUIRED")
    items = document.get("items") if isinstance(document, dict) else None
    item_names = []
    linked_paths = {unquote(urlsplit(m[1].strip("<>")).path) for m in markdown_links(content)}
    if not isinstance(document, dict) or any(not isinstance(document.get(k), str) or not document[k].strip()
            for k in ("title", "identity", "purpose", "usage", "limitations", "next_steps")):
        issues.append("DOCUMENT_EDITORIAL_FIELDS_REQUIRED")
    else:
        if not content.startswith(f"# {document['title'].strip()}\n\n{document['identity'].strip()}\n\n"):
            issues.append("DOCUMENT_IDENTITY_MISMATCH")
        for heading, field in ((headings[0], "purpose"), (headings[1], "usage"),
                               (headings[3], "limitations"), (headings[4], "next_steps")):
            match = re.search(r"(?ms)^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", content)
            if not match or match[1].strip() != document[field].strip():
                issues.append("DOCUMENT_SECTION_MISMATCH:" + field)
    if not isinstance(items, list):
        issues.append("DOCUMENT_ITEMS_LIST_REQUIRED")
    else:
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                issues.append("DOCUMENT_ITEM_INVALID"); continue
            path = item["path"]
            if "/" in path or "\\" in path or path in ("", ".", ".."):
                issues.append("DOCUMENT_ITEM_MUST_BE_DIRECT_CHILD"); continue
            item_names.append(path)
            if not (target.parent / path).exists() or path == "README.md":
                issues.append("DOCUMENT_ITEM_NOT_FOUND:" + path)
            if path not in linked_paths and path + "/" not in linked_paths:
                issues.append("DOCUMENT_ITEM_LINK_MISSING:" + path)
        actual_children = sorted(p.name for p in target.parent.iterdir() if p.name != "README.md")
        if sorted(item_names) != actual_children:
            issues.append("DOCUMENT_INVENTORY_MISMATCH")
        standard = sum((target.parent / name).is_dir() for name in item_names) > 5
        expected_headings = [headings[0], "Visão estrutural", *headings[1:]] if standard else headings
        if actual != expected_headings:
            issues.append("AGGREGATOR_UNEXPECTED_OR_DUPLICATE_SECTION")
        if standard:
            if "Visão estrutural" not in actual or not positions[0] < actual.index("Visão estrutural") < positions[1]:
                issues.append("AGGREGATOR_STANDARD_STRUCTURE_REQUIRED")
        inventory = re.search(r"(?ms)^## O que existe aqui\n(.*?)(?=^## |\Z)", content)
        rows = inventory[1].splitlines() if inventory else []
        table_links = []
        for row in rows:
            if row.startswith("|"):
                table_links += [unquote(urlsplit(m[1]).path) for m in markdown_links(row)]
        if sorted(table_links) != sorted(item_names):
            issues.append("AGGREGATOR_TABLE_INVENTORY_MISMATCH")
    checked = 0
    for link in markdown_links(content):
        raw = link[1].strip("<>")
        parsed = urlsplit(raw)
        if parsed.scheme in ("http", "https", "mailto"):
            continue
        checked += 1
        if parsed.scheme or parsed.netloc or parsed.path.startswith(("/", "\\")):
            issues.append("LOCAL_LINK_INVALID:" + raw); continue
        linked = target.parent / unquote(parsed.path) if parsed.path else target
        if not linked.exists():
            issues.append("LOCAL_LINK_MISSING:" + raw); continue
        # Preserve case correctness across Windows and Linux.
        cursor = target.parent
        for component in unquote(parsed.path).replace("\\", "/").split("/"):
            if component in ("", "."): continue
            if component == "..": cursor = cursor.parent; continue
            if component not in {p.name for p in cursor.iterdir()}:
                issues.append("LOCAL_LINK_CASE_MISMATCH:" + raw); break
            cursor = cursor / component
        if parsed.fragment and linked.suffix.lower() == ".md":
            if unquote(parsed.fragment) not in anchors(linked.read_text(encoding="utf8")):
                issues.append("LOCAL_LINK_ANCHOR_MISSING:" + raw)
    return {"name": "aggregator_template_and_links", "status": "FAIL" if issues else "PASS",
            "relative_links_checked": checked, "issues": issues}


def validate_candidate(candidate, *, repo_root, evidence_dir):
    """Executa validator real sobre overlay único, retornando binding verificável."""
    candidate = copy.deepcopy(candidate)
    binding = copy.deepcopy(candidate.get("binding", {})) if isinstance(candidate, dict) else {}
    result = {"status": "BLOCKED", "binding": binding, "validator": VALIDATOR,
              "checks": [], "issues": [], "writes_performed_in_original": False,
              "runtime_validation": "NOT_RUN", "homologated": False,
              "generate_not_executed_by_validator": True,
              "started_at_utc": _utc(), "commands": []}
    reserved = None
    repo = None
    runner = _process_runner()

    def run(argv, cwd, timeout=30):
        number = len(result["commands"]) + 1
        record = {"argv": [str(v) for v in argv], "cwd": str(cwd), "start": _utc(),
                  "python": sys.version, "timeout_seconds": timeout}
        result["commands"].append(record)
        prefix = reserved / f"{number:02d}"
        (prefix.with_suffix(".ledger.json")).write_text(json.dumps(record, indent=2), encoding="utf8")
        runner.REPO_ROOT = cwd
        runner.GIT_TIMEOUT_SECONDS = runner.STEP_TIMEOUT_SECONDS = timeout
        previous = len(runner.PROCESS_RECORDS)
        failure = None
        try:
            record["exit_code"], _, record["duration_seconds"] = runner._run(record["argv"])
        except BaseException as exc:
            failure = exc
            record["execution_error"] = repr(exc)
            record["execution_exception"] = {"type": type(exc).__name__,
                "traceback": traceback.format_exc(), "filename": getattr(exc, "filename", None),
                "errno": getattr(exc, "errno", None), "winerror": getattr(exc, "winerror", None)}
        records = runner.PROCESS_RECORDS[previous:]
        observation = dict(records[0]) if len(records) == 1 else {}
        record["process"] = observation
        record["pid"] = observation.get("pid")
        record["end"] = _utc()
        try:
            prefix.with_suffix(".stdout.txt").write_text(observation.get("stdout", ""), encoding="utf8")
            prefix.with_suffix(".stderr.txt").write_text(observation.get("stderr", ""), encoding="utf8")
            prefix.with_suffix(".result.json").write_text(json.dumps(record, indent=2), encoding="utf8")
        except OSError as exc:
            record["persistence_error"] = repr(exc)
            if failure is None: failure = exc
        # An error during helper cleanup must not erase an observed interruption.
        conventional = observation.get("conventional_exit_code")
        if observation.get("result") == "INTERRUPTED" and type(conventional) is int and conventional != 0:
            result["interrupted"] = True
            result["exit_code"] = conventional
        if failure is not None: raise failure
        if observation.get("result") == "INTERRUPTED": raise KeyboardInterrupt()
        if observation.get("result") == "TIMEOUT": raise OSError("SUBPROCESS_TIMEOUT")
        if observation.get("cleanup") != "COMPLETE" or not observation.get("utf8_valid"):
            raise OSError("SUBPROCESS_OBSERVATION_INCOMPLETE")
        return record["exit_code"], observation.get("stdout", "")

    def git(*args, cwd=None):
        code, output = run(["git", "-c", f"core.hooksPath={os.devnull}", "-c", "core.longpaths=true", *args], cwd or repo)
        if code: raise ValueError("GIT_COMMAND_FAILED:" + " ".join(args))
        return output.rstrip("\r\n")

    try:
        repo = Path(repo_root).absolute()
        evidence = Path(evidence_dir).absolute()
        _no_aliases(repo); _no_aliases(evidence)
        repo = repo.resolve(strict=True)
        if evidence.resolve().is_relative_to(repo) or repo.is_relative_to(evidence.resolve()):
            raise ValueError("EVIDENCE_MUST_BE_EXTERNAL")
        evidence.mkdir(parents=False, exist_ok=False)
        reserved = evidence
        if not isinstance(candidate, dict) or not isinstance(binding, dict) or set(binding) != BINDING_FIELDS:
            raise ValueError("CANDIDATE_BINDING_INVALID")
        if "integrity_sha256" in candidate and candidate["integrity_sha256"] != sha256_digest({k: v for k, v in candidate.items() if k != "integrity_sha256"}):
            raise ValueError("CANDIDATE_INTEGRITY_MISMATCH")
        result["checks"].append({"name": "candidate_generation_seal", "required": False,
                                 "status": "PASS" if "integrity_sha256" in candidate else "NOT_PROVIDED",
                                 "authenticates_generation": False})
        if any(binding[k] != v for k, v in (("operation", "create"), ("object_type", "readme"), ("readme_scale", "agregador"))):
            raise ValueError("OPERATION_OUTSIDE_PILOT")
        if not isinstance(binding["generation_id"], str) or not binding["generation_id"].strip():
            raise ValueError("GENERATION_ID_REQUIRED")
        for key, length in (("base_sha", 40), ("content_sha256", 64), ("release_sha256", 64), ("template_sha256", 64)):
            if not isinstance(binding[key], str) or not re.fullmatch(f"[0-9a-f]{{{length}}}", binding[key]):
                raise ValueError("BINDING_HASH_INVALID:" + key)
        content = candidate.get("content_utf8")
        if not isinstance(content, str): raise ValueError("CONTENT_UTF8_REQUIRED")
        data = content.encode("utf8")
        if type(binding["content_size"]) is not int or binding["content_size"] != len(data) or binding["content_sha256"] != hashlib.sha256(data).hexdigest():
            raise ValueError("CONTENT_BINDING_MISMATCH")
        relative = _relative(binding["destination_relative"])
        context = candidate.get("context")
        if not isinstance(context, dict) or any(context.get(k) != binding[k] for k in ("operation", "object_type", "readme_scale", "destination_relative")) or "source_relative" in context:
            raise ValueError("CONTEXT_BINDING_MISMATCH")
        before = {"head": git("rev-parse", "HEAD"), "status": git("status", "--porcelain=v1", "--untracked-files=all")}
        result["original_before"] = before
        if before["head"] != binding["base_sha"] or before["status"]:
            raise ValueError("BASE_MISMATCH_OR_DIRTY")
        if git("rev-parse", "--is-shallow-repository") != "false":
            raise ValueError("COMPLETE_HISTORY_REQUIRED")
        assistant = repo / "ambiente_fonte/.assistant"
        _destination(assistant, relative)
        for key, path in (("template_sha256", TEMPLATE), ("release_sha256", MANIFEST)):
            target = assistant / path
            _no_aliases(target)
            if hashlib.sha256(target.read_bytes()).hexdigest() != binding[key]:
                raise ValueError("RELEASE_OR_TEMPLATE_MISMATCH:" + key)
        result["checks"].append({"name": "candidate_base_binding", "status": "PASS"})
        overlay = reserved / "overlay"
        git("clone", "--no-local", "--no-hardlinks", "--no-checkout", "--config", "core.autocrlf=false", "--", str(repo), str(overlay))
        git("checkout", "--detach", binding["base_sha"], cwd=overlay)
        if git("rev-parse", "--is-shallow-repository", cwd=overlay) != "false" or git("status", "--porcelain=v1", "--untracked-files=all", cwd=overlay):
            raise ValueError("OVERLAY_BASE_NOT_CLEAN_AND_COMPLETE")
        overlay_assistant = overlay / "ambiente_fonte/.assistant"
        target = _destination(overlay_assistant, relative)
        preflight_path = overlay_assistant / "skills/hub-ml-criar-objeto/scripts/preflight.py"
        preflight_code, preflight_output = run([sys.executable, "-B", str(preflight_path), "--context-json", json.dumps(context, ensure_ascii=False)], overlay)
        preflight_result = json.loads(preflight_output)
        if preflight_code or preflight_result.get("status") != "PASS":
            result["checks"].append({"name": "preflight_l2", "status": "FAIL", "exit_code": preflight_code})
            raise ValueError("PREFLIGHT_BLOCKED")
        result["checks"].append({"name": "preflight_l2", "status": "PASS", "exit_code": 0})
        with target.open("xb") as stream: stream.write(data)
        if target.read_bytes() != data: raise OSError("OVERLAY_BYTES_DIVERGED")
        result["overlay"] = {"path": str(overlay), "base_sha": binding["base_sha"],
                             "destination": str(target.relative_to(overlay).as_posix()),
                             "content_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
        result["checks"].append(_readme_checks(content, target, candidate.get("document"), (overlay_assistant / TEMPLATE).read_text(encoding="utf8")))
        validator = overlay / "tools/validate_assistant.py"
        result["validator_source_sha256"] = hashlib.sha256(validator.read_bytes()).hexdigest()
        code, _ = run([sys.executable, "-B", str(validator)], overlay, timeout=120)
        result["checks"].append({"name": "validate_assistant", "status": "PASS" if code == 0 else "FAIL", "exit_code": code})
        expected = "?? " + target.relative_to(overlay).as_posix()
        status = git("-c", "core.quotepath=false", "status", "--porcelain=v1", "--untracked-files=all", cwd=overlay)
        intact = (git("rev-parse", "HEAD", cwd=overlay) == binding["base_sha"] and status == expected and target.read_bytes() == data)
        result["checks"].append({"name": "single_overlay_preserved", "status": "PASS" if intact else "FAIL", "status_porcelain": status})
        after = {"head": git("rev-parse", "HEAD"), "status": git("status", "--porcelain=v1", "--untracked-files=all")}
        result["original_after"] = after
        result["checks"].append({"name": "original_preserved", "status": "PASS" if before == after and not (assistant / relative).exists() else "FAIL"})
        result["status"] = "PASS" if all(c["status"] == "PASS" or (c.get("required") is False and c["status"] == "NOT_PROVIDED") for c in result["checks"]) else "FAIL"
    except (ValueError, TypeError, UnicodeError) as exc:
        result["issues"].append(str(exc))
    except OSError as exc:
        result["status"] = "FAIL"; result["issues"].append(repr(exc))
    except (KeyboardInterrupt, SystemExit) as exc:
        result["status"] = "FAIL"; result["issues"].append("INTERRUPTED:" + repr(exc))
        result["interrupted"] = True
        result["exit_code"] = exc.code if isinstance(exc, SystemExit) and type(exc.code) is int and exc.code != 0 else 130
    result["ended_at_utc"] = _utc()
    result["validation_id"] = sha256_digest(result)
    if reserved is not None:
        try:
            pending = reserved / "validation.pending.json"
            with pending.open("x", encoding="utf8") as stream:
                json.dump(result, stream, ensure_ascii=False, indent=2)
            pending.rename(reserved / "validation.json")
        except (OSError, KeyboardInterrupt, SystemExit) as exc:
            result["status"] = "FAIL"; result["issues"].append("EVIDENCE_PERSISTENCE_FAILED:" + repr(exc))
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                result["interrupted"] = True
                result["exit_code"] = exc.code if isinstance(exc, SystemExit) and type(exc.code) is int and exc.code != 0 else 130
            result.pop("validation_id", None); result["validation_id"] = sha256_digest(result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    result = validate_candidate(json.loads(args.candidate.read_text(encoding="utf8")), repo_root=args.repo_root, evidence_dir=args.evidence_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else result.get("exit_code", 2)


if __name__ == "__main__":
    raise SystemExit(main())
