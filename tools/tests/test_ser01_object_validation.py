"""SER01: envelope/adversariais; integração real é opt-in e deixa evidência externa.

Os records sintéticos abaixo testam somente integridade. Não representam Receipt
real, prova Windows/Databricks, certificação ou autorização humana.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ser01_validation_under_test", ROOT / "tools/skill_enforcement/ser01_object_validation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def candidate(kind="notebook"):
    context = {"operation": "create", "object_type": kind, "object_name": "ensaio_ser01",
               "type_confirmed": True, "existing_capability_checked": True,
               "existing_capability_status": "not_found"}
    if kind == "snippet":
        context["snippet_section"] = "testing"
        folder = "hub_snippets/testing/ensaio_ser01"
    elif kind in {"script", "prompt"}:
        folder = {"script": "hub_scripts", "prompt": "hub_prompts"}[kind] + "/ensaio_ser01"
    else:
        context["destination_relative"] = "hub_lab/exemplo_ser01.py"
        folder = None
    if folder:
        names = ["README.md", "exemplo_ensaio_ser01.py", "ensaio_ser01.md" if kind == "prompt" else "ensaio_ser01.py"]
        if kind != "prompt":
            names.append("__init__.py")
        files = {folder + "/" + name: "conteúdo sintético\n" for name in names}
    else:
        files = {context["destination_relative"]: "# Databricks notebook source\n# Ensaio sintético.\n"}
    return {"candidate_version": module.VERSION, "base_sha": "a" * 40,
            "context": context, "files": files}


def synthetic_record(data):
    """Record propositalmente sintético; nunca é apresentado como execução."""
    envelope = module.inspect_candidate(data)
    names = ["identity_before", "status_before", "history", "preflight", "baseline_validator", "clone",
             "checkout", "stage", "validator", "overlay_head", "overlay_index", "overlay_diff",
             "overlay_untracked", "identity_after", "status_after"]
    checks = ["destination_matches_preflight", "canonical_validator", "overlay_head_preserved", "overlay_index_exact",
              "overlay_no_other_changes", "overlay_bytes_exact", "original_preserved"]
    report = {"record_version": module.RECORD_VERSION, "run_id": "synthetic-run",
              "status": "PASS", "issues": [], "binding": envelope,
              "writes_performed_in_original": False, "homologated": False,
              "runtime_validation": "NOT_RUN", "execution_authenticated": False,
              "policy_promotion_authorized": False,
              "scope": "CREATE_PACKAGE_LOCAL_STRUCTURAL_VALIDATION_ONLY",
              "original_before": {"head": "a" * 40, "status": ""},
              "original_after": {"head": "a" * 40, "status": ""},
              "commands": [{"name": n, "exit_code": 0, "process_cleanup": "COMPLETE", "command_started": True} for n in names],
              "checks": [{"name": n, "status": "PASS"} for n in checks]}
    return module._seal(report)


class EnvelopeTests(unittest.TestCase):
    def test_four_package_shapes_are_explicit(self):
        expected_counts = {"snippet": 4, "script": 4, "prompt": 3, "notebook": 1}
        for kind, count in expected_counts.items():
            with self.subTest(kind=kind):
                plan = module.inspect_candidate(candidate(kind))
                self.assertEqual(count, len(plan["files"]))
                self.assertEqual(kind, plan["object_type"])

    def test_conversion_is_blocked_before_io(self):
        data = candidate()
        data["context"]["operation"] = "convert"
        with self.assertRaisesRegex(module.Blocked, "CONVERSION_NOT_IMPLEMENTED"):
            module.inspect_candidate(data)

    def test_seventh_type_is_rejected(self):
        data = candidate()
        data["context"]["object_type"] = "micromodelo"
        with self.assertRaisesRegex(module.Blocked, "OBJECT_TYPE_INVALID"):
            module.inspect_candidate(data)

    def test_skill_creation_does_not_fake_registry_entry(self):
        data = candidate()
        data["context"]["object_type"] = "skill"
        with self.assertRaisesRegex(module.Blocked, "CATALOG_POLICY_DECISION"):
            module.inspect_candidate(data)

    def test_aggregator_and_standalone_readme_object_are_distinct(self):
        data = candidate()
        data["context"].update(object_type="readme", readme_scale="agregador",
                               destination_relative="hub_lab/README.md")
        data["files"] = {"hub_lab/README.md": "# Fixture\n"}
        with self.assertRaisesRegex(module.Blocked, "DOCUMENT_REQUIRED"):
            module.inspect_candidate(data)
        data["document"] = {"title": "Fixture"}
        self.assertEqual("readme", module.inspect_candidate(data)["object_type"])
        data["context"]["readme_scale"] = "objeto"
        with self.assertRaisesRegex(module.Blocked, "STANDALONE_OBJECT_README"):
            module.inspect_candidate(data)

    def test_wrong_types_are_structured(self):
        for field in ("operation", "object_type", "existing_capability_status", "object_name"):
            for value in (None, [], {}, 12, True):
                data = candidate()
                data["context"][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(module.Blocked):
                    module.inspect_candidate(data)

    def test_human_context_requires_booleans_not_truthy_values(self):
        for field in ("type_confirmed", "existing_capability_checked"):
            for value in (False, 1, "true", None):
                data = candidate()
                data["context"][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(module.Blocked):
                    module.inspect_candidate(data)

    def test_existing_capability_requires_explicit_slice(self):
        data = candidate()
        data["context"]["existing_capability_status"] = "found"
        with self.assertRaisesRegex(module.Blocked, "OVERLAP_DECISION"):
            module.inspect_candidate(data)
        data["context"]["overlap_resolution"] = "create_declared_slice"
        module.inspect_candidate(data)

    def test_missing_or_extra_file_cannot_escape_validator_coverage(self):
        for change in ("missing", "tools", "extra"):
            data = candidate("snippet")
            if change == "missing":
                data["files"].pop(next(p for p in data["files"] if p.endswith("__init__.py")))
            else:
                # Mantém quatro arquivos: discrimina a allowlist, não apenas o limite.
                data["files"].pop(next(p for p in data["files"] if p.endswith("__init__.py")))
                data["files"]["tools/validate_assistant.py" if change == "tools" else "hub_snippets/testing/ensaio_ser01/extra.py"] = "pass\n"
            with self.subTest(change=change), self.assertRaisesRegex(module.Blocked, "PACKAGE_FILES_MISMATCH"):
                module.inspect_candidate(data)

    def test_unsafe_paths_rejected_portably(self):
        paths = ["../x.py", "/x.py", "C:x.py", "C:/x.py", "//server/share/x.py", "a\\x.py", "a/./x.py",
                 "a//x.py", "a/x.py:ads", "a/NUL.py", "a/README.md.", "a/x.py ", "a/\x00.py", ".git/a.py"]
        for name in paths:
            with self.subTest(name=name), self.assertRaises(module.Blocked):
                module.safe_relative(name)

    def test_case_or_destination_mismatch_is_not_normalized(self):
        data = candidate("prompt")
        path = next(p for p in data["files"] if p.endswith("README.md"))
        data["files"][path.replace("README", "readme")] = data["files"].pop(path)
        with self.assertRaises(module.Blocked):
            module.inspect_candidate(data)
        data = candidate("script")
        data["context"]["destination_relative"] = "hub_scripts/outro"
        with self.assertRaises(module.Blocked):
            module.inspect_candidate(data)

    def test_encoding_and_size_restrictions(self):
        for text in ("sem newline", "CRLF\r\n", "nul\x00\n", "\ud800\n"):
            data = candidate()
            data["files"][next(iter(data["files"]))] = text
            with self.subTest(text=repr(text)), self.assertRaises(module.Blocked):
                module.inspect_candidate(data)
        with patch.object(module, "MAX_BYTES", 3), self.assertRaisesRegex(module.Blocked, "TOO_LARGE"):
            module.inspect_candidate(candidate())

    def test_json_duplicates_and_nonfinite_are_rejected(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}'):
            with self.subTest(text=text), self.assertRaises(module.Blocked):
                module.loads_strict(text)

    def test_unknown_fields_and_sections_fail_closed(self):
        for change in ("extra", "context", "section"):
            data = candidate("snippet")
            if change == "extra":
                data["authorize_everything"] = True
            elif change == "context":
                data["context"]["new_snippet_section_authorized"] = True
            else:
                data["context"]["snippet_section"] = "new_section"
            with self.subTest(change=change), self.assertRaises(module.Blocked):
                module.inspect_candidate(data)

    def test_input_and_file_bindings_change_with_one_byte(self):
        left = candidate()
        right = copy.deepcopy(left)
        right["files"][next(iter(right["files"]))] += "# diferença\n"
        a, b = module.inspect_candidate(left), module.inspect_candidate(right)
        self.assertNotEqual(a["candidate_sha256"], b["candidate_sha256"])
        self.assertNotEqual(a["files"][0]["sha256"], b["files"][0]["sha256"])

    def test_api_stdout_canonicalizes_only_crlf_transport(self):
        lf = 'from .x import a\n\n__all__ = [\n    "a",\n]\n\n'
        self.assertEqual(lf, module._api_stdout_lf(lf))
        self.assertEqual(lf.encode("utf-8"), module._api_stdout_lf(lf.replace("\n", "\r\n")).encode("utf-8"))
        for changed in (lf.replace("__all__", "\r__all__"),          # CR isolado permanece
                        lf.replace("\n", "\r"),                       # só CR não vira LF
                        lf + "\r\n",                                  # bytes extras não somem
                        lf.replace('"a"', '"b"').replace("\n", "\r\n")):  # conteúdo diferente
            with self.subTest(changed=repr(changed)):
                self.assertNotEqual(lf, module._api_stdout_lf(changed))

    def test_unapproved_evidence_persistence_does_not_touch_disk(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "must-not-exist"
            report = module.validate_package(candidate(), repo_root=ROOT, evidence_dir=target)
            self.assertEqual("BLOCKED", report["status"])
            self.assertIn("EVIDENCE_PERSISTENCE_NOT_AUTHORIZED", report["issues"])
            self.assertEqual([], report["commands"])
            self.assertFalse(target.exists())

    def test_unsupported_operations_never_start_processes(self):
        data = candidate()
        data["context"]["operation"] = "convert"
        with patch.object(module, "_runtime", side_effect=AssertionError("must not start")):
            result = module.validate_package(data, repo_root=ROOT, evidence_dir=ROOT / "unused", evidence_authorized=True)
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual([], result["commands"])


class IntegrityTests(unittest.TestCase):
    def verify(self, report, data=None, **kwargs):
        return module.verify_record(report, data or candidate(), expected_base_sha=kwargs.get("base", "a" * 40),
                                    expected_run_id=kwargs.get("run", "synthetic-run"))

    def test_synthetic_record_verifies_integrity_not_execution(self):
        checked = self.verify(synthetic_record(candidate()))
        self.assertTrue(checked["valid"], checked)
        self.assertFalse(checked["execution_reverified"])
        self.assertFalse(checked["human_authority_authenticated"])
        self.assertFalse(checked["policy_promotion_authorized"])

    def test_single_byte_tamper_is_rejected(self):
        record = synthetic_record(candidate())
        record["binding"]["files"][0]["size"] += 1
        self.assertFalse(self.verify(record)["valid"])

    def test_replay_other_candidate_run_or_base_is_rejected(self):
        record = synthetic_record(candidate())
        other = candidate()
        other["files"][next(iter(other["files"]))] += "# mudou\n"
        self.assertFalse(self.verify(record, other)["valid"])
        self.assertFalse(self.verify(record, run="another-run")["valid"])
        self.assertFalse(self.verify(record, base="b" * 40)["valid"])

    def test_resealed_overclaims_do_not_become_valid(self):
        for field, value in (("homologated", True), ("writes_performed_in_original", True),
                             ("runtime_validation", "PASS"), ("execution_authenticated", True),
                             ("policy_promotion_authorized", True), ("status", "BLOCKED")):
            record = synthetic_record(candidate())
            record[field] = value
            module._seal(record)
            with self.subTest(field=field):
                self.assertFalse(self.verify(record)["valid"])

    def test_missing_duplicate_reordered_commands_are_rejected(self):
        for change in ("missing", "duplicate", "reorder", "bool_exit", "cleanup", "not_started"):
            record = synthetic_record(candidate())
            if change == "missing":
                record["commands"] = [x for x in record["commands"] if x["name"] != "validator"]
            elif change == "duplicate":
                record["commands"].append(dict(record["commands"][0]))
            elif change == "reorder":
                record["commands"].reverse()
            elif change == "bool_exit":
                record["commands"][0]["exit_code"] = False
            elif change == "cleanup":
                record["commands"][0]["process_cleanup"] = "FAILED"
            else:
                record["commands"][0]["command_started"] = False
            module._seal(record)
            with self.subTest(change=change):
                self.assertFalse(self.verify(record)["valid"])

    def test_original_changed_or_missing_check_is_rejected(self):
        for change in ("dirty", "check"):
            record = synthetic_record(candidate())
            if change == "dirty":
                record["original_after"]["status"] = " M README.md"
            else:
                record["checks"] = [x for x in record["checks"] if x["name"] != "overlay_bytes_exact"]
            module._seal(record)
            with self.subTest(change=change):
                self.assertFalse(self.verify(record)["valid"])

    def test_malformed_report_does_not_raise(self):
        for item in (None, [], {}, {"commands": [None]}, {"checks": [True]}):
            self.assertFalse(self.verify(item)["valid"])


@unittest.skipUnless(os.environ.get("SER01_RUN_REPO_INTEGRATION") == "1", "integração em clone integral requer opt-in e evidência externa")
class RepositoryIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                                   capture_output=True, text=True, encoding="utf-8").stdout.strip()
        raw = os.environ.get("SER01_EVIDENCE_ROOT")
        self.assertTrue(raw, "SER01_EVIDENCE_ROOT externo é obrigatório")
        self.evidence = Path(raw).resolve()
        self.evidence.mkdir(parents=True, exist_ok=True)
        self.assertFalse(self.evidence.is_relative_to(ROOT.resolve()))
        self.assistant = ROOT / "ambiente_fonte/.assistant"

    def execute(self, data):
        data["base_sha"] = self.base
        label = self._testMethodName + "_" + uuid.uuid4().hex
        (self.evidence / (label + ".candidate.json")).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        destination = self.evidence / label
        report = module.validate_package(data, repo_root=ROOT, evidence_dir=destination, evidence_authorized=True)
        self.assertEqual("PASS", report["status"], f"{report['issues']}; evidência={destination}")
        checked = module.verify_record(report, data, expected_base_sha=self.base, expected_run_id=report["run_id"])
        self.assertTrue(checked["valid"], checked)
        self.assertFalse((self.assistant / report["binding"]["destination_relative"]).exists())

    def replica(self, kind, source_relative):
        source = self.assistant / source_relative
        old = source.name
        new = "ser01_fixture_" + kind
        data = candidate(kind)
        data["context"]["object_name"] = new
        data["context"]["existing_capability_status"] = "found"
        data["context"]["overlap_resolution"] = "create_declared_slice"
        if kind == "snippet":
            data["context"]["snippet_section"] = source.parent.name
        folder = source.parent.relative_to(self.assistant).as_posix() + "/" + new
        data["files"] = {}
        for name in ("README.md", old + (".md" if kind == "prompt" else ".py"), "exemplo_" + old + ".py") + (() if kind == "prompt" else ("__init__.py",)):
            text = (source / name).read_text(encoding="utf-8").replace(old, new)
            # Fixture positiva é candidato novo: canoniza LF terminal só aqui. O
            # fonte legado não muda e a primitive segue fail-closed sem LF.
            if not text.endswith("\n"):
                text += "\n"
            data["files"][folder + "/" + name.replace(old, new)] = text
        return data

    def test_real_snippet_validation(self):
        self.execute(self.replica("snippet", "hub_snippets/constants/format_br"))

    def test_real_script_validation(self):
        self.execute(self.replica("script", "hub_scripts/data_quality_check"))

    def test_real_prompt_validation(self):
        self.execute(self.replica("prompt", "hub_prompts/eda_rapida"))

    def test_real_notebook_validation(self):
        data = candidate()
        path = "hub_prompts/eda_rapida/exemplo_ser01_fixture.py"
        data["context"]["destination_relative"] = path
        data["files"] = {path: (self.assistant / "hub_prompts/eda_rapida/exemplo_eda_rapida.py").read_text(encoding="utf-8")}
        self.execute(data)

    def test_invalid_notebook_is_not_certified_by_green_baseline(self):
        data = candidate()
        data["base_sha"] = self.base
        path = "hub_prompts/eda_rapida/exemplo_ser01_invalid.py"
        data["context"]["destination_relative"] = path
        data["files"] = {path: "# Databricks notebook source\nthis is not valid Python !!!\n"}
        label = self._testMethodName + "_" + uuid.uuid4().hex
        (self.evidence / (label + ".candidate.json")).write_text(json.dumps(data), encoding="utf-8")
        report = module.validate_package(data, repo_root=ROOT, evidence_dir=self.evidence / label, evidence_authorized=True)
        self.assertEqual("FAIL", report["status"], report["issues"])
        rows = {x["name"]: x for x in report["commands"]}
        self.assertEqual(0, rows["baseline_validator"]["exit_code"])
        self.assertNotEqual(0, rows["validator"]["exit_code"])
        self.assertEqual(report["original_before"], report["original_after"])
        self.assertFalse((self.assistant / path).exists())

    def test_incorrect_public_api_is_rejected_without_repairing_candidate(self):
        data = self.replica("snippet", "hub_snippets/constants/format_br")
        data["base_sha"] = self.base
        rel = next(p for p in data["files"] if p.endswith("__init__.py"))
        data["files"][rel] = "# API deliberadamente ausente.\n"
        label = self._testMethodName + "_" + uuid.uuid4().hex
        (self.evidence / (label + ".candidate.json")).write_text(json.dumps(data), encoding="utf-8")
        report = module.validate_package(data, repo_root=ROOT, evidence_dir=self.evidence / label, evidence_authorized=True)
        self.assertEqual("FAIL", report["status"], report["issues"])
        self.assertTrue(any(c["name"] == "canonical_public_api" and c["status"] == "FAIL" for c in report["checks"]))
        self.assertEqual(report["original_before"], report["original_after"])
        overlay = self.evidence / label / "overlay/ambiente_fonte/.assistant" / rel
        self.assertEqual(data["files"][rel].encode("utf-8"), overlay.read_bytes())

    def test_real_aggregator_validation(self):
        folder = "skills/hub-ml-criar-objeto/scripts"
        names = sorted(p.name for p in (self.assistant / folder).iterdir())
        self.assertNotIn("README.md", names)
        self.assertTrue(all((self.assistant / folder / name).is_file() for name in names))
        doc = {"title": "Ensaio estrutural SER01", "identity": "Fixture sintética; não é publicação.",
               "purpose": "Verificar a rota canônica em clone isolado.", "usage": "Executar somente neste ensaio.",
               "limitations": "Não comprova execução Databricks.", "next_steps": "Revisar o registro da validação.",
               "items": [{"path": n, "description": "Recurso existente do piloto."} for n in names]}
        text = f"# {doc['title']}\n\n{doc['identity']}\n\n"
        text += "## Para que serve / quando usar\n\n" + doc["purpose"] + "\n\n## Como usar\n\n" + doc["usage"]
        text += "\n\n## O que existe aqui\n\n| Item | Descrição |\n|---|---|\n"
        text += "".join(f"| [{n}]({n}) | Recurso existente do piloto. |\n" for n in names)
        text += "\n## Limites e armadilhas\n\n" + doc["limitations"] + "\n\n## Onde continuar\n\n" + doc["next_steps"] + "\n"
        data = candidate()
        data["context"].update(object_type="readme", readme_scale="agregador", destination_relative=folder + "/README.md")
        data["document"] = doc
        data["files"] = {folder + "/README.md": text}
        self.execute(data)


if __name__ == "__main__":
    unittest.main()
