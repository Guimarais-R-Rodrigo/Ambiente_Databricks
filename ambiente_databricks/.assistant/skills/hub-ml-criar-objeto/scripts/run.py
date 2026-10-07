"""Piloto L3 estreito create/readme/agregador; policy da skill permanece L2.

Generate não escreve produto nem staging. Apply exige registros locais exatos
de validação e autorização: integridade verificável não autentica seus emissores.
O único writer suportado é Windows/local NTFS, com ancestrais fixados por handles.
Não há homologação, execução de tools, rollback, conversão ou overwrite aqui.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import types
import uuid
from pathlib import Path
from urllib.parse import quote

SKILL = "hub-ml-criar-objeto"
SCOPE = "create_readme_aggregator"
SCHEMA = "SE07-CREATE-README-EVIDENCE-1"
SKILL_REL = f"skills/{SKILL}"
TEMPLATE = "hub_padroes/readme/template.md"
RECEIPT = "hub_scripts/skill_execution/receipt/__init__.py"
REQUIRED_ARTIFACTS = {
    f"{SKILL_REL}/SKILL.md", f"{SKILL_REL}/execution_contract.json",
    f"{SKILL_REL}/scripts/preflight.py", f"{SKILL_REL}/scripts/run.py",
    f"{SKILL_REL}/scripts/_windows_writer.py",
    f"{SKILL_REL}/templates/checklist-objeto-novo.md", TEMPLATE, RECEIPT,
}
BINDING_FIELDS = {"operation", "object_type", "readme_scale", "destination_relative",
                  "content_sha256", "content_size", "generation_id", "base_sha",
                  "release_sha256", "template_sha256"}


def _own_root():
    return Path(__file__).absolute().parents[3]


def _module(path):
    # Carregamento sem __pycache__: generate não cria arquivos implicitamente.
    name = "_sef_create_" + uuid.uuid4().hex
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    try:
        exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
        return module
    finally:
        sys.modules.pop(name, None)


_receipt = _module(_own_root() / RECEIPT)
canonical_json_bytes = _receipt.canonical_json_bytes
sha256_digest = _receipt.sha256_digest
_writer = _module(Path(__file__).with_name("_windows_writer.py"))


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _relative(raw):
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ValueError("PATH_INVALID: use caminho relativo canônico com /")
    parts = raw.split("/")
    reserved = re.compile(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$", re.I)
    if any(not p or p in {".", ".."} or p.endswith((".", " "))
           or re.search(r'[<>:"|?*\x00-\x1f]', p) or reserved.fullmatch(p) for p in parts):
        raise ValueError("PATH_INVALID: componente ambíguo, reservado ou escape")
    return Path(*parts)


def _root(assistant_root):
    raw = _own_root() if assistant_root is None else Path(assistant_root)
    if not raw.is_absolute() or ".." in raw.parts:
        raise ValueError("ROOT_INVALID: raiz absoluta explícita exigida")
    return Path(os.path.abspath(raw))


def _release(root):
    data = (root / SKILL_REL / "release_manifest.json").read_bytes()
    manifest = json.loads(data)
    if (manifest.get("manifest_version") != "0.1" or manifest.get("skill") != SKILL
            or manifest.get("algorithm") != "git_blob_sha1"):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    seen = set()
    template = None
    for item in manifest["artifacts"]:
        rel = item["path"]
        safe = _relative(rel)
        if rel in seen:
            raise ValueError("RELEASE_MANIFEST_DUPLICATE")
        seen.add(rel)
        target = root / safe
        if not target.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
            raise ValueError("RELEASE_PATH_ESCAPE")
        content = target.read_bytes()
        digest = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
        if digest != item["git_blob_sha1"]:
            raise ValueError(f"RELEASE_INTEGRITY_MISMATCH: {rel}")
        if rel == TEMPLATE:
            template = content
        if rel in {f"{SKILL_REL}/scripts/run.py", f"{SKILL_REL}/scripts/_windows_writer.py",
                   f"{SKILL_REL}/scripts/preflight.py", RECEIPT}:
            if content != (_own_root() / safe).read_bytes():
                raise ValueError(f"RUNTIME_RELEASE_MISMATCH: {rel}")
    if not REQUIRED_ARTIFACTS.issubset(seen):
        raise ValueError("RELEASE_ARTIFACTS_MISSING")
    template.decode("utf-8")
    return _sha(data), _sha(template)


def _context(context):
    if not isinstance(context, dict):
        raise ValueError("CONTEXT_INVALID")
    if any(context.get(k) != v for k, v in {
            "operation": "create", "object_type": "readme", "readme_scale": "agregador"}.items()):
        raise ValueError("SCOPE_UNSUPPORTED")
    allowed = {"operation", "object_type", "object_name", "readme_scale", "destination_relative",
               "type_confirmed", "existing_capability_checked", "existing_capability_status",
               "overlap_resolution"}
    if set(context) - allowed:
        raise ValueError("CONTEXT_FIELDS_UNSUPPORTED")
    relative = _relative(context.get("destination_relative"))
    if relative.name != "README.md":
        raise ValueError("DESTINATION_MUST_BE_README")
    return relative


def _preflight(context, root, trace):
    trace["preflight_called"] = True
    module = _module(Path(__file__).with_name("preflight.py"))
    module._resolve_assistant_root = lambda: root
    result = module.preflight(context)
    trace["preflight_completed"] = True
    trace["preflight_status"] = result.get("status")
    if result.get("status") != "PASS":
        raise ValueError("PREFLIGHT_BLOCKED: " + json.dumps(result.get("blocking_issues"), ensure_ascii=False))


def _document(document, parent):
    fields = {"title", "identity", "purpose", "usage", "limitations", "next_steps", "items"}
    if not isinstance(document, dict) or set(document) != fields:
        raise ValueError("DOCUMENT_FIELDS_INVALID")
    for key in fields - {"items"}:
        if not isinstance(document[key], str) or not document[key].strip() or "\r" in document[key] or "\x00" in document[key]:
            raise ValueError(f"DOCUMENT_TEXT_INVALID: {key}")
    if "\n" in document["title"]:
        raise ValueError("DOCUMENT_TITLE_MULTILINE")
    if not isinstance(document["items"], list):
        raise ValueError("DOCUMENT_ITEMS_INVALID")
    names = []
    for item in document["items"]:
        if not isinstance(item, dict) or set(item) != {"path", "description"}:
            raise ValueError("DOCUMENT_ITEM_INVALID")
        path = _relative(item["path"])
        if len(path.parts) != 1 or path.name == "README.md":
            raise ValueError("DOCUMENT_ITEM_NOT_CHILD")
        description = item["description"]
        if not isinstance(description, str) or not description.strip() or any(c in description for c in "\r\n\x00"):
            raise ValueError("DOCUMENT_ITEM_DESCRIPTION_INVALID")
        child = parent / path
        info = child.lstat()
        if child.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400 or info.st_nlink > 1 and child.is_file():
            raise ValueError("DOCUMENT_ITEM_LINK_UNSUPPORTED")
        names.append(path.name)
    actual = sorted(p.name for p in parent.iterdir() if p.name != "README.md")
    if len(set(names)) != len(names) or sorted(names) != actual:
        raise ValueError("DOCUMENT_INVENTORY_MISMATCH")


def _render(document, parent):
    _document(document, parent)
    lines = [f"# {document['title'].strip()}", "", document["identity"].strip(), "",
             "## Para que serve / quando usar", "", document["purpose"].strip(), ""]
    items = sorted(document["items"], key=lambda i: i["path"])
    if sum((parent / i["path"]).is_dir() for i in items) > 5:
        lines += ["## Visão estrutural", "", "```text"]
        lines += [i["path"] for i in items]
        lines += ["```", ""]
    lines += ["## Como usar", "", document["usage"].strip(), "", "## O que existe aqui", "",
              "| Item | Descrição |", "|---|---|"]
    for item in items:
        label = item["path"].replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;")
        description = item["description"].replace("|", "&#124;")
        lines.append(f"| [{label}]({quote(item['path'])}) | {description} |")
    lines += ["", "## Limites e armadilhas", "", document["limitations"].strip(), "",
              "## Onde continuar", "", document["next_steps"].strip(), ""]
    return "\n".join(lines)


def _trace(phase):
    return {"phase": phase, "entrypoint": f"{SKILL_REL}/scripts/run.py::{phase}",
            "preflight_called": False, "preflight_completed": False, "preflight_status": "NOT_RUN",
            "generation_completed": False, "template_read": False,
            "repository_validator_executed": False, "authorization_presented": False,
            "create_attempted": False, "create_completed": False, "reread_completed": False}


def _seal(payload):
    return {**payload, "integrity_sha256": sha256_digest(payload)}


def _intact(payload):
    return isinstance(payload, dict) and payload.get("integrity_sha256") == sha256_digest({k: v for k, v in payload.items() if k != "integrity_sha256"})


def _result(status, trace, issues, *, writes=False, binding=None, observed=None):
    evidence = _seal({"schema_version": SCHEMA, "skill": SKILL, "scope": SCOPE,
                      "status": status, "trace": copy.deepcopy(trace), "issues": list(issues),
                      "binding": binding, "writes_performed": writes, "observed": observed,
                      "homologated": False, "authentication": "local_integrity_only"})
    return {"status": status, "writes_performed": writes, "trace": trace,
            "issues": issues, "homologated": False, "evidence": evidence,
            "observed": observed}


def generate(context, document, *, base_sha, assistant_root=None):
    trace = _trace("generate")
    try:
        root = _root(assistant_root)
        relative = _context(context)
        if not isinstance(base_sha, str) or not re.fullmatch("[0-9a-f]{40}", base_sha):
            raise ValueError("BASE_SHA_INVALID")
        _preflight(context, root, trace)
        with _writer.PinnedParent(root, relative) as pinned:
            release, template = _release(root)
            trace["template_read"] = True
            content = _render(document, pinned.destination.parent)
            raw = content.encode("utf-8")
            binding = {"operation": "create", "object_type": "readme", "readme_scale": "agregador",
                       "destination_relative": relative.as_posix(), "content_sha256": _sha(raw),
                       "content_size": len(raw), "generation_id": uuid.uuid4().hex,
                       "base_sha": base_sha, "release_sha256": release, "template_sha256": template}
            trace["generation_completed"] = True
            candidate = _seal({"binding": binding, "content_utf8": content,
                               "context": copy.deepcopy(context), "document": copy.deepcopy(document),
                               "root": str(root), "ancestors": pinned.identities,
                               "generation_trace": copy.deepcopy(trace)})
        result = _result("GERADO", trace, [], binding=binding)
        result["candidate"] = candidate
        return result
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return _result("BLOCKED", trace, [str(exc)])


def _check_candidate(candidate, root):
    if not _intact(candidate):
        raise ValueError("CANDIDATE_INTEGRITY_MISMATCH")
    binding = candidate["binding"]
    if not isinstance(binding, dict) or set(binding) != BINDING_FIELDS:
        raise ValueError("BINDING_FIELDS_INVALID")
    relative = _context(candidate["context"])
    if (binding["operation"] != "create" or binding["object_type"] != "readme"
            or binding["readme_scale"] != "agregador"
            or binding["destination_relative"] != relative.as_posix()
            or str(root) != candidate["root"]):
        raise ValueError("CANDIDATE_PATH_BINDING_MISMATCH")
    if not re.fullmatch("[0-9a-f]{40}", binding["base_sha"]) or not re.fullmatch("[0-9a-f]{32}", binding["generation_id"]):
        raise ValueError("CANDIDATE_ID_INVALID")
    raw = candidate["content_utf8"].encode("utf-8")
    if type(binding["content_size"]) is not int or binding["content_size"] != len(raw) or binding["content_sha256"] != _sha(raw):
        raise ValueError("CANDIDATE_CONTENT_BINDING_MISMATCH")
    if not raw.endswith(b"\n") or b"\r" in raw:
        raise ValueError("CANDIDATE_ENCODING_INVALID")
    gen = candidate["generation_trace"]
    if gen.get("preflight_status") != "PASS" or gen.get("generation_completed") is not True or gen.get("template_read") is not True:
        raise ValueError("GENERATION_EVIDENCE_INVALID")
    return binding, relative, raw


def _records(binding, authorization, validation):
    if (not isinstance(authorization, dict) or authorization.get("decision") != "AUTHORIZE_CREATE"
            or authorization.get("authority") != "external_confirmation_record"
            or not isinstance(authorization.get("authorization_id"), str)
            or not authorization["authorization_id"].strip()
            or sha256_digest(authorization.get("binding")) != sha256_digest(binding)):
        raise ValueError("AUTHORIZATION_MISSING_OR_MISMATCH")
    if (not isinstance(validation, dict) or validation.get("status") != "PASS"
            or validation.get("validator") != "repo_side_create_readme_v1"
            or sha256_digest(validation.get("binding")) != sha256_digest(binding)
            or not isinstance(validation.get("checks"), (dict, list)) or not validation["checks"]
            or validation.get("validation_id") != sha256_digest({k: v for k, v in validation.items() if k != "validation_id"})):
        raise ValueError("VALIDATION_MISSING_OR_MISMATCH")


def _persist(path, payload):
    with path.open("xb") as stream:
        stream.write(canonical_json_bytes(payload) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def _reserve_evidence(root, evidence_dir, authorized):
    if authorized is not True or evidence_dir is None:
        raise ValueError("EVIDENCE_STAGING_NOT_AUTHORIZED")
    path = Path(evidence_dir)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("EVIDENCE_PATH_INVALID")
    parent = path.parent.resolve(strict=True)
    canonical_root = root.resolve(strict=True)
    if parent.is_relative_to(canonical_root) or canonical_root.is_relative_to(parent / path.name):
        raise ValueError("EVIDENCE_MUST_BE_EXTERNAL")
    # Fixar ancestrais do staging também impede redirecionamento para o produto.
    guard = _writer.PinnedParent(Path(path.anchor), str(path.relative_to(path.anchor)).replace("\\", "/"))
    guard.__enter__()
    try:
        path.mkdir()
        child_guard = _writer.PinnedParent(path, "evidence-placeholder")
        child_guard.__enter__()
    except BaseException:
        guard.__exit__(None, None, None)
        raise
    guard.__exit__(None, None, None)
    return path, child_guard


def apply(candidate, authorization, validation, *, assistant_root=None,
          evidence_dir=None, evidence_authorized=False):
    trace = _trace("apply")
    writes = False
    binding = None
    observed = None
    staging = None
    staging_guard = None
    fd = None
    pinned = None
    result = None
    try:
        root = _root(assistant_root)
        binding, relative, raw = _check_candidate(candidate, root)
        _records(binding, authorization, validation)
        trace["authorization_presented"] = True
        trace["validation_record_presented"] = True
        _preflight(candidate["context"], root, trace)
        with _writer.PinnedParent(root, relative) as pinned:
            if pinned.identities != candidate["ancestors"]:
                raise ValueError("ANCESTOR_IDENTITY_MISMATCH")
            trace["destination_absence_revalidated"] = True
            trace["writer_support"] = "Windows_local_NTFS"
            release, template = _release(root)
            trace["template_read"] = True
            if release != binding["release_sha256"] or template != binding["template_sha256"]:
                raise ValueError("RELEASE_TEMPLATE_BINDING_MISMATCH")
            _document(candidate["document"], pinned.destination.parent)
            staging, staging_guard = _reserve_evidence(root, evidence_dir, evidence_authorized)
            _persist(staging / "01-before.json", _result("PREPARED", trace, [], binding=binding))
            trace["create_attempted"] = True
            fd = pinned.create()
            writes = True
            trace["create_completed"] = True
            trace["created_identity"] = pinned.created_identity
            _persist(staging / "02-created.json", _result("INCONCLUSIVE", trace, [], writes=True, binding=binding))
            offset = 0
            while offset < len(raw):
                count = os.write(fd, raw[offset:])
                if count <= 0:
                    raise OSError("WRITE_NO_PROGRESS")
                offset += count
            os.fsync(fd)
            os.lseek(fd, 0, os.SEEK_SET)
            chunks = []
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
            final = b"".join(chunks)
            observed = {"content_sha256": _sha(final), "content_size": len(final)}
            trace["reread_completed"] = True
            if final != raw:
                raise ValueError("FINAL_BYTES_MISMATCH")
            closing_fd, fd = fd, None
            os.close(closing_fd)
            trace["file_close_completed"] = True
            result = _result("ESCRITO", trace, [], writes=True, binding=binding, observed=observed)
            _persist(staging / "03-final.json", result)
    except BaseException as exc:
        writes = writes or bool(pinned is not None and pinned.created)
        if writes:
            trace["create_completed"] = True
            trace["created_identity"] = pinned.created_identity
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            status = "INTERRUPTED"
        else:
            status = "INCONCLUSIVE" if writes else "BLOCKED"
        result = _result(status, trace, [f"{type(exc).__name__}: {exc}"], writes=writes, binding=binding, observed=observed)
        if staging is not None:
            try:
                _persist(staging / "04-failure.json", result)
            except BaseException as persistence:
                result = _result(status, trace, result["issues"] + [f"EVIDENCE_PERSISTENCE_FAILED: {persistence}"],
                                 writes=writes, binding=binding, observed=observed)
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except BaseException as close_error:
                result = _result("INCONCLUSIVE" if writes else "BLOCKED", trace,
                                 (result or {}).get("issues", []) + [f"FILE_CLOSE_FAILED: {close_error}"],
                                 writes=writes, binding=binding, observed=observed)
                if staging is not None:
                    try:
                        _persist(staging / "05-close-failure.json", result)
                    except BaseException:
                        pass  # Falha já não é sucesso; retorno conserva diagnóstico.
        if staging_guard is not None:
            staging_guard.__exit__(None, None, None)
    return result


def verify_evidence(payload, *, assistant_root=None):
    issues = []
    try:
        evidence = payload.get("evidence", payload)
        if not _intact(evidence):
            raise ValueError("EVIDENCE_INTEGRITY_MISMATCH")
        if "evidence" in payload:
            for key in ("status", "writes_performed", "trace", "issues", "observed", "homologated"):
                if key not in payload or payload[key] != evidence.get(key):
                    raise ValueError(f"EVIDENCE_ENVELOPE_MISMATCH: {key}")
        if (evidence.get("schema_version") != SCHEMA or evidence.get("skill") != SKILL
                or evidence.get("scope") != SCOPE or evidence.get("homologated") is not False
                or evidence.get("authentication") != "local_integrity_only"):
            raise ValueError("EVIDENCE_SCHEMA_INVALID")
        trace = evidence["trace"]
        if trace.get("repository_validator_executed") is not False:
            raise ValueError("RUNTIME_VALIDATOR_OVERCLAIM")
        status = evidence["status"]
        if status == "ESCRITO":
            binding = evidence["binding"]
            if (evidence["writes_performed"] is not True or evidence["issues"]
                    or trace.get("preflight_status") != "PASS"
                    or any(trace.get(k) is not True for k in ("authorization_presented", "validation_record_presented", "create_completed", "reread_completed", "file_close_completed"))
                    or evidence["observed"] != {"content_sha256": binding["content_sha256"], "content_size": binding["content_size"]}):
                raise ValueError("WRITTEN_EVIDENCE_INVALID")
        elif status == "GERADO":
            if evidence["writes_performed"] is not False or not trace.get("generation_completed") or trace.get("preflight_status") != "PASS":
                raise ValueError("GENERATED_EVIDENCE_INVALID")
            if "candidate" in payload:
                binding, _, _ = _check_candidate(payload["candidate"], Path(payload["candidate"]["root"]))
                if binding != evidence["binding"]:
                    raise ValueError("EVIDENCE_CANDIDATE_MISMATCH")
        elif status not in {"BLOCKED", "FAIL", "INCONCLUSIVE", "INTERRUPTED", "PREPARED"}:
            raise ValueError("EVIDENCE_STATUS_INVALID")
        if assistant_root is not None and evidence.get("binding"):
            release, template = _release(_root(assistant_root))
            if release != evidence["binding"]["release_sha256"] or template != evidence["binding"]["template_sha256"]:
                raise ValueError("EVIDENCE_RELEASE_MISMATCH")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        issues.append(str(exc))
    return {"valid": not issues, "issues": issues, "authentication": "local_integrity_only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="phase", required=True)
    g = commands.add_parser("generate")
    g.add_argument("--context-json", required=True, help="arquivo JSON")
    g.add_argument("--document-json", required=True, help="arquivo JSON")
    g.add_argument("--base-sha", required=True)
    a = commands.add_parser("apply")
    a.add_argument("--candidate-json", required=True)
    a.add_argument("--authorization-json", required=True)
    a.add_argument("--validation-json", required=True)
    a.add_argument("--evidence-dir", required=True)
    a.add_argument("--evidence-authorized", action="store_true")
    for sub in (g, a):
        sub.add_argument("--assistant-root")
    args = parser.parse_args()
    def read(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    try:
        if args.phase == "generate":
            result = generate(read(args.context_json), read(args.document_json), base_sha=args.base_sha, assistant_root=args.assistant_root)
        else:
            result = apply(read(args.candidate_json), read(args.authorization_json), read(args.validation_json),
                           assistant_root=args.assistant_root, evidence_dir=args.evidence_dir, evidence_authorized=args.evidence_authorized)
    except (OSError, ValueError) as exc:
        result = _result("BLOCKED", _trace(args.phase), [str(exc)])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result["status"] in {"GERADO", "ESCRITO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
