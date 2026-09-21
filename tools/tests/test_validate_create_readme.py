"""Provas repo-side com Git, clone completo e validate_assistant reais.

O candidato desta suíte é explicitamente sintético; integração com o runner
real é um gate separado. Nenhum README real é removido para criar elegibilidade.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tools/skill_enforcement/validate_create_readme.py"
spec = importlib.util.spec_from_file_location("validate_create_readme_under_test", SOURCE)
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate
spec.loader.exec_module(gate)
sys.path.insert(0, str(ROOT / "tools/tests"))
from test_certify_local import alive, wait_for_file


def git(repo, *args):
    return subprocess.run(["git", "-c", f"core.hooksPath={os.devnull}", *args], cwd=repo,
                          capture_output=True, text=True, check=True, timeout=60).stdout.rstrip("\r\n")


class ValidateCreateReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix="sef-readme-repository-")
        cls.repo = Path(cls.fixture.name) / "repo"
        git(ROOT, "clone", "--no-local", "--no-hardlinks", "--config", "core.autocrlf=false", "--", str(ROOT), str(cls.repo))
        cls.assistant = cls.repo / "ambiente_fonte/.assistant"
        cls.relative = "hub_padroes/piloto_readme_fixture/README.md"
        folder = (cls.assistant / cls.relative).parent
        folder.mkdir()
        (folder / "guia.md").write_text("# Guia sintético\n\nConsulta manual de fixture.\n", encoding="utf8")
        # An additive synthetic release fixture, not a claim about the baseline.
        manifest = cls.assistant / gate.MANIFEST
        if not manifest.exists():
            manifest.write_text(json.dumps({"fixture": "synthetic_release_for_repo_gate"}) + "\n", encoding="utf8")
        git(cls.repo, "add", "ambiente_fonte/.assistant/hub_padroes/piloto_readme_fixture/guia.md", "ambiente_fonte/.assistant/" + gate.MANIFEST)
        git(cls.repo, "-c", "user.name=Synthetic", "-c", "user.email=synthetic@example.invalid", "commit", "-qm", "synthetic absent README fixture")
        cls.sha = git(cls.repo, "rev-parse", "HEAD")

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sef-readme-validation-")
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / "evidence"
        self.document = {"title": "Coleção sintética", "identity": "Guia sintético para testes locais.",
                         "purpose": "Consultar o guia da fixture.", "usage": "Leia [guia](guia.md).",
                         "limitations": "Não executa analytics nem homologa runtime.",
                         "next_steps": "Continue no [guia](guia.md).",
                         "items": [{"path": "guia.md", "description": "Guia de consulta manual."}]}
        content = ("# Coleção sintética\n\nGuia sintético para testes locais.\n\n"
                   "## Para que serve / quando usar\n\nConsultar o guia da fixture.\n\n"
                   "## Como usar\n\nLeia [guia](guia.md).\n\n"
                   "## O que existe aqui\n\n| Item | Descrição |\n| --- | --- |\n"
                   "| [guia.md](guia.md) | Guia de consulta manual. |\n\n"
                   "## Limites e armadilhas\n\nNão executa analytics nem homologa runtime.\n\n"
                   "## Onde continuar\n\nContinue no [guia](guia.md).\n")
        self.candidate = {"content_utf8": content, "document": self.document,
                          "context": {"operation": "create", "object_type": "readme", "object_name": "README",
                                      "readme_scale": "agregador", "destination_relative": self.relative,
                                      "type_confirmed": True, "existing_capability_checked": True,
                                      "existing_capability_status": "not_found"},
                          "binding": {"operation": "create", "object_type": "readme", "readme_scale": "agregador",
                                      "destination_relative": self.relative, "content_sha256": "", "content_size": 0,
                                      "generation_id": "synthetic-fixture-generation", "base_sha": self.sha,
                                      "template_sha256": hashlib.sha256((self.assistant / gate.TEMPLATE).read_bytes()).hexdigest(),
                                      "release_sha256": hashlib.sha256((self.assistant / gate.MANIFEST).read_bytes()).hexdigest()}}
        self.rebind()
        self.result = None

    def rebind(self):
        data = self.candidate["content_utf8"].encode("utf8")
        self.candidate["binding"].update(content_sha256=hashlib.sha256(data).hexdigest(), content_size=len(data))

    def validate(self):
        self.result = gate.validate_candidate(self.candidate, repo_root=self.repo, evidence_dir=self.out)
        return self.result

    def tearDown(self):
        self.assertFalse((self.assistant / self.relative).exists())
        self.assertEqual(self.sha, git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual("", git(self.repo, "status", "--porcelain=v1", "--untracked-files=all"))
        target = os.environ.get("SEF_CREATE_README_TEST_ARTIFACT_DIR")
        if target:
            destination = Path(target) / self._testMethodName
            destination.mkdir(parents=True, exist_ok=False)
            (destination / "candidate.json").write_text(json.dumps(self.candidate, ensure_ascii=False, indent=2), encoding="utf8")
            if self.result:
                (destination / "observed_result.json").write_text(json.dumps(self.result, ensure_ascii=False, indent=2), encoding="utf8")
            if self.out.exists():
                for path in self.out.iterdir():
                    if path.is_file(): shutil.copy2(path, destination / path.name)
                overlay_candidate = self.out / "overlay/ambiente_fonte/.assistant" / self.relative
                if overlay_candidate.exists(): shutil.copy2(overlay_candidate, destination / "overlay_README.md")

    def test_valid_candidate_executes_real_validator_and_preserves_original(self):
        before_template = (self.assistant / gate.TEMPLATE).read_bytes()
        result = self.validate()
        self.assertEqual("PASS", result["status"], result)
        check = next(c for c in result["checks"] if c["name"] == "validate_assistant")
        self.assertEqual(0, check["exit_code"])
        commands = [c for c in result["commands"] if c["argv"][-1].endswith("validate_assistant.py")]
        self.assertEqual(1, len(commands))
        self.assertGreater(commands[0]["pid"], 0)
        self.assertEqual(before_template, (self.assistant / gate.TEMPLATE).read_bytes())
        self.assertEqual(self.candidate["binding"], result["binding"])
        payload = copy.deepcopy(result); identifier = payload.pop("validation_id")
        self.assertEqual(gate.sha256_digest(payload), identifier)
        self.assertEqual("NOT_RUN", result["runtime_validation"])
        self.assertFalse(result["writes_performed_in_original"])
        self.assertTrue(result["generate_not_executed_by_validator"])
        seal = next(c for c in result["checks"] if c["name"] == "candidate_generation_seal")
        self.assertEqual("NOT_PROVIDED", seal["status"])

    def test_bad_link_fails_real_validator(self):
        self.candidate["content_utf8"] += "\n[Link inexistente](nao_existe.md)\n"
        self.rebind()
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        check = next(c for c in result["checks"] if c["name"] == "validate_assistant")
        self.assertNotEqual(0, check["exit_code"])
        self.assertTrue(any("link relativo quebrado" in p.read_text(encoding="utf8") for p in self.out.glob("*.stdout.txt")))

    def test_bad_anchor_fails_specific_link_check(self):
        self.candidate["content_utf8"] += "\n[Âncora ausente](guia.md#inexistente)\n"; self.rebind()
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("LOCAL_LINK_ANCHOR_MISSING" in issue for check in result["checks"] for issue in check.get("issues", [])))

    def test_content_changed_without_rebinding_is_blocked(self):
        self.candidate["content_utf8"] += "alterado\n"
        self.assertIn("CONTENT_BINDING_MISMATCH", self.validate()["issues"])

    def test_path_changed_without_context_is_blocked(self):
        self.candidate["binding"]["destination_relative"] = "hub_padroes/outro/README.md"
        self.assertIn("CONTEXT_BINDING_MISMATCH", self.validate()["issues"])

    def test_wrong_base_is_blocked(self):
        self.candidate["binding"]["base_sha"] = "0" * 40
        self.assertIn("BASE_MISMATCH_OR_DIRTY", self.validate()["issues"])

    def test_wrong_template_is_blocked(self):
        self.candidate["binding"]["template_sha256"] = "0" * 64
        self.assertTrue(any("RELEASE_OR_TEMPLATE_MISMATCH" in i for i in self.validate()["issues"]))

    def test_wrong_release_is_blocked(self):
        self.candidate["binding"]["release_sha256"] = "0" * 64
        self.assertTrue(any("RELEASE_OR_TEMPLATE_MISMATCH" in i for i in self.validate()["issues"]))

    def test_existing_destination_is_blocked_without_modification(self):
        self.candidate["binding"]["destination_relative"] = "hub_padroes/README.md"
        self.candidate["context"]["destination_relative"] = "hub_padroes/README.md"
        path = self.assistant / "hub_padroes/README.md"; original = path.read_bytes()
        self.assertIn("DESTINATION_MUST_BE_ABSENT_IN_EXISTING_DIRECTORY", self.validate()["issues"])
        self.assertEqual(original, path.read_bytes())

    def test_escape_is_blocked(self):
        self.candidate["binding"]["destination_relative"] = "../README.md"
        self.candidate["context"]["destination_relative"] = "../README.md"
        self.assertIn("DESTINATION_INVALID", self.validate()["issues"])

    def test_preflight_blocked_is_not_promoted(self):
        self.candidate["context"]["type_confirmed"] = False
        result = self.validate()
        self.assertIn("PREFLIGHT_BLOCKED", result["issues"])
        self.assertFalse((self.out / "overlay/ambiente_fonte/.assistant" / self.relative).exists())

    def test_object_readme_marker_is_not_an_aggregator(self):
        self.candidate["content_utf8"] += "\n<!-- readme-objeto: 1.0.0 -->\n"; self.rebind()
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("OBJECT_TEMPLATE_NOT_AGGREGATOR" in c.get("issues", []) for c in result["checks"]))

    def test_existing_evidence_namespace_is_preserved(self):
        self.out.mkdir(); marker = self.out / "sealed"; marker.write_bytes(b"SEALED")
        self.assertNotEqual("PASS", self.validate()["status"])
        self.assertEqual([marker], list(self.out.iterdir()))
        self.assertEqual(b"SEALED", marker.read_bytes())

    def test_dirty_source_is_blocked(self):
        marker = self.repo / "synthetic-dirty-probe.txt"
        marker.write_text("fixture only", encoding="utf8")
        try:
            self.assertIn("BASE_MISMATCH_OR_DIRTY", self.validate()["issues"])
        finally:
            marker.unlink()

    def test_evidence_inside_original_is_blocked(self):
        self.out = self.repo / "not-created-evidence"
        result = self.validate()
        self.assertIn("EVIDENCE_MUST_BE_EXTERNAL", result["issues"])
        self.assertFalse(self.out.exists())

    def test_generation_seal_when_present_must_match(self):
        self.candidate["integrity_sha256"] = "0" * 64
        self.assertIn("CANDIDATE_INTEGRITY_MISMATCH", self.validate()["issues"])

    def test_missing_aggregator_section_is_rejected(self):
        self.candidate["content_utf8"] = self.candidate["content_utf8"].replace("## Limites e armadilhas", "## Outra seção")
        self.rebind()
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("AGGREGATOR_SECTION_ORDER" in c.get("issues", []) for c in result["checks"]))

    def test_incomplete_inventory_is_rejected(self):
        self.candidate["document"]["items"] = []
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("DOCUMENT_INVENTORY_MISMATCH" in c.get("issues", []) for c in result["checks"]))

    def test_empty_items_match_a_real_empty_directory(self):
        folder = Path(self.tmp.name) / "empty-directory"
        folder.mkdir()
        document = copy.deepcopy(self.document)
        document.update(items=[], usage="Leia a orientação desta pasta.", next_steps="Solicite revisão editorial.")
        content = self.candidate["content_utf8"].replace("| [guia.md](guia.md) | Guia de consulta manual. |\n", "")
        content = content.replace(self.document["usage"], document["usage"]).replace(self.document["next_steps"], document["next_steps"])
        target = folder / "README.md"
        target.write_text(content, encoding="utf8")
        check = gate._readme_checks(content, target, document, (self.assistant / gate.TEMPLATE).read_text(encoding="utf8"))
        self.assertEqual("PASS", check["status"], check)
        self.assertEqual(0, check["relative_links_checked"])
        # Structural unit check only; Git does not represent empty directories.
        self.out.mkdir()
        (self.out / "empty-directory-structural-only.json").write_text(json.dumps(check, indent=2), encoding="utf8")

    def test_validation_id_binds_all_provenance_fields(self):
        result = self.validate()
        self.assertEqual("PASS", result["status"], result)
        changed = copy.deepcopy(result)
        changed["original_before"]["head"] = "0" * 40
        identifier = changed.pop("validation_id")
        self.assertNotEqual(identifier, gate.sha256_digest(changed))

    def test_item_link_elsewhere_does_not_replace_inventory_row(self):
        self.candidate["content_utf8"] = self.candidate["content_utf8"].replace("| [guia.md](guia.md) | Guia de consulta manual. |\n", "")
        self.rebind()
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("AGGREGATOR_TABLE_INVENTORY_MISMATCH" in c.get("issues", []) for c in result["checks"]))

    def test_human_h2_cannot_spoof_template_sections(self):
        self.candidate["document"]["purpose"] += "\n\n## Título humano extra\n\nProsa."
        self.candidate["content_utf8"] = self.candidate["content_utf8"].replace("Consultar o guia da fixture.", self.candidate["document"]["purpose"])
        self.rebind()
        result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("AGGREGATOR_UNEXPECTED_OR_DUPLICATE_SECTION" in c.get("issues", []) for c in result["checks"]))

    def test_spawn_failure_preserves_command_without_pid(self):
        with mock.patch.object(subprocess, "Popen", side_effect=OSError("SYNTHETIC_SPAWN_FAILURE")):
            result = self.validate()
        self.assertNotEqual("PASS", result["status"])
        process = result["commands"][0]["process"]
        self.assertIsNone(process["pid"])
        self.assertIsNone(process["observed_exit_code"])
        self.assertIn("SYNTHETIC_SPAWN_FAILURE", process["error"])
        self.assertTrue((self.out / "01.result.json").exists())

    def process_boundary(self, cancellation=None, cleanup_error=False):
        runner = gate._process_runner()
        original_run = runner._run
        pidfile = Path(self.tmp.name) / "owned-pids.json"
        ready = Path(self.tmp.name) / "ready"
        command = [sys.executable, "-B", "-c",
                   "import json,os,subprocess,sys,time;from pathlib import Path;"
                   "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);"
                   f"Path({str(pidfile)!r}).write_text(json.dumps([os.getpid(),p.pid]));"
                   "print('BOUNDARY_OUTPUT',flush=True);"
                   f"Path({str(ready)!r}).write_text('ready');time.sleep(30)"]
        def boundary(_requested):
            runner.STEP_TIMEOUT_SECONDS = 1.5
            return original_run(command)
        runner._run = boundary
        original_wait = subprocess.Popen.wait
        fired = []
        def wait(process, *args, **kwargs):
            if cancellation is not None and not fired:
                fired.append(process.pid)
                wait_for_file(ready)
                if cancellation == "keyboard": raise KeyboardInterrupt()
                raise SystemExit(0)
            return original_wait(process, *args, **kwargs)
        original_exit = tempfile.TemporaryDirectory.__exit__
        injected = []
        def cleanup(temp, *args):
            process_record = sys._getframe(1).f_locals.get("record", {})
            original_exit(temp, *args)
            if cleanup_error and Path(temp.name).name.startswith("sef-process-") and process_record.get("result") == "INTERRUPTED":
                injected.append(temp.name)
                error = PermissionError(13, "SYNTHETIC_CLEANUP_AFTER_INTERRUPT", str(Path(temp.name) / "stderr"))
                error.winerror = 32
                raise error
        with mock.patch.object(gate, "_process_runner", return_value=runner), mock.patch.object(subprocess.Popen, "wait", wait), mock.patch.object(tempfile.TemporaryDirectory, "__exit__", cleanup):
            result = self.validate()
        if cleanup_error:
            self.assertEqual(1, len(injected))
            command_record = result["commands"][0]
            details = command_record["execution_exception"]
            self.assertEqual(32, details["winerror"])
            self.assertEqual(str(Path(injected[0]) / "stderr"), details["filename"])
            self.assertIn("SYNTHETIC_CLEANUP_AFTER_INTERRUPT", details["traceback"])
            self.assertIn("certify_local.py", details["traceback"])
            self.assertTrue(any("SYNTHETIC_CLEANUP_AFTER_INTERRUPT" in issue for issue in result["issues"]))
        self.assertEqual("FAIL", result["status"])
        pids = json.loads(pidfile.read_text())
        observation = result["commands"][0]["process"]
        if observation.get("launcher_pid"): pids.append(observation["launcher_pid"])
        oracle = {"pids": pids, "alive_after": [alive(pid) for pid in pids], "fault_injection": "replace first Git observation command with owned parent/child fixture"}
        (self.out / "external-process-oracle.json").write_text(json.dumps(oracle, indent=2), encoding="utf8")
        self.assertFalse(any(oracle["alive_after"]), oracle)
        self.assertEqual("COMPLETE", observation["process_cleanup"])
        self.assertEqual("FAILED" if cleanup_error else "COMPLETE", observation["temporary_cleanup"])
        self.assertEqual("FAILED" if cleanup_error else "COMPLETE", observation["cleanup"])
        if cleanup_error:
            self.assertEqual(32, observation["temporary_cleanup_exception"]["winerror"])
        self.assertIn("BOUNDARY_OUTPUT", observation["stdout"])
        self.assertEqual("INTERRUPTED" if cancellation else "TIMEOUT", observation["result"])
        if cancellation:
            self.assertEqual(130, result["exit_code"])
            self.assertTrue(result["interrupted"])
        self.assertEqual("FAIL", json.loads((self.out / "validation.json").read_text())["status"])

    def test_timeout_cleans_owned_parent_and_child(self):
        self.process_boundary()

    def test_keyboard_interrupt_preserves_observation_and_cleanup(self):
        self.process_boundary("keyboard")

    def test_systemexit_zero_cannot_approve_validation(self):
        self.process_boundary("zero")

    def test_cleanup_error_preserves_real_interruption_and_failure(self):
        self.process_boundary("zero", cleanup_error=True)

    def test_final_evidence_cancellation_cannot_approve(self):
        original = Path.open
        def interrupt(path, *args, **kwargs):
            if path.name == "validation.pending.json": raise SystemExit(0)
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, "open", interrupt):
            result = self.validate()
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(130, result["exit_code"])
        self.assertFalse((self.out / "validation.json").exists())
        self.assertTrue(any(c["name"] == "validate_assistant" and c["status"] == "PASS" for c in result["checks"]))
        unsealed = copy.deepcopy(result); identifier = unsealed.pop("validation_id")
        self.assertEqual(identifier, gate.sha256_digest(unsealed))


if __name__ == "__main__":
    unittest.main()
