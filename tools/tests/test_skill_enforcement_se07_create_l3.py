"""Independent adversarial oracles for the narrow SE07 create/readme pilot.

All writes use synthetic, external fixtures. Authorization/validation records in
this suite are labelled test records: they do not claim a human identity or a
repo-side validator run. The actual gate is exercised by its separate suite.
SE07_L3_EVIDENCE_DIR preserves ledgers, outputs, PIDs and filesystem snapshots.
SE07_L3_RUNNER_PATH optionally selects an immutable integration snapshot.
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
import time
import unittest
from unittest.mock import patch
import uuid

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = ROOT / "ambiente_databricks/.assistant"
SKILL = "skills/hub-ml-criar-objeto"
RUNNER = f"{SKILL}/scripts/run.py"
BASE = "d49c8728f0e47adc15f7f78293c9fcc58c809a15"
BINDING_KEYS = {"operation", "object_type", "readme_scale", "destination_relative",
                "content_sha256", "content_size", "generation_id", "base_sha",
                "release_sha256", "template_sha256"}

WORKER = r'''
import importlib.util, json, os, pathlib, sys, time
sys.dont_write_bytecode = True
root, request, barrier, evidence, result, ready = map(pathlib.Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location("independent_process_runner", root / "skills/hub-ml-criar-objeto/scripts/run.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
data = json.loads(request.read_text(encoding="utf-8"))
if data.get("fault") == "partial_pause":
    original_write = os.write
    def interrupted_write(fd, content):
        written = original_write(fd, content[:17])
        os.fsync(fd)
        ready.write_text(json.dumps({"pid": os.getpid(), "phase": "PARTIAL_WRITE", "bytes": written}), encoding="utf-8")
        while True:
            time.sleep(.05)
    module.os.write = interrupted_write
ready.write_text(json.dumps({"pid": os.getpid(), "phase": "BEFORE_APPLY"}), encoding="utf-8")
deadline = time.monotonic() + 30
while not barrier.exists():
    if time.monotonic() > deadline:
        raise TimeoutError("barrier not released")
    time.sleep(.01)
payload = module.apply(data["candidate"], data["authorization"], data["validation"],
                       assistant_root=root, evidence_dir=evidence, evidence_authorized=True)
result.write_text(json.dumps({"pid": os.getpid(), "payload": payload}), encoding="utf-8")
print(json.dumps(payload), flush=True)
raise SystemExit(0 if payload["status"] == "ESCRITO" else 2)
'''


def load_module(path):
    name = "se07_b_" + uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")


def tree_bytes(root):
    """Independent byte inventory; never follow adversarial links/junctions."""
    result = {}
    for folder, dirs, files in os.walk(root, followlinks=False):
        base = Path(folder)
        for name in list(dirs):
            p = base / name
            if p.is_symlink() or getattr(p, "is_junction", lambda: False)():
                dirs.remove(name)
                result[p.relative_to(root).as_posix()] = "LINK:" + os.readlink(p)
            else:
                result[p.relative_to(root).as_posix() + "/"] = "DIRECTORY"
        for name in files:
            p = base / name
            result[p.relative_to(root).as_posix()] = (
                "LINK:" + os.readlink(p) if p.is_symlink()
                else hashlib.sha256(p.read_bytes()).hexdigest())
    return result


class CreateReadmeL3AdversarialTests(unittest.TestCase):
    def setUp(self):
        sys.dont_write_bytecode = True
        evidence = os.environ.get("SE07_L3_EVIDENCE_DIR")
        if evidence:
            parent = Path(evidence)
            parent.mkdir(parents=True, exist_ok=True)
            self.workspace = parent / (self._testMethodName + "_" + uuid.uuid4().hex)
            self.workspace.mkdir()
        else:
            temp = tempfile.TemporaryDirectory(prefix="sef_l3_independent_")
            self.addCleanup(temp.cleanup)
            self.workspace = Path(temp.name)
        dump(self.workspace / "ledger.json", {"status": "STARTED", "test": self.id(),
             "pid": os.getpid(), "runtime": sys.version, "time_ns": time.time_ns()})
        self.root = self.workspace / ".assistant"
        shutil.copytree(ASSISTANT, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        snapshot = os.environ.get("SE07_L3_RUNNER_PATH")
        if snapshot:
            shutil.copyfile(snapshot, self.root / RUNNER)
            sibling = Path(snapshot).parent / "_windows_writer.py"
            if sibling.exists():
                shutil.copyfile(sibling, self.root / SKILL / "scripts/_windows_writer.py")
        self.assertTrue((self.root / RUNNER).is_file(), "NOT_IMPLEMENTED_BASELINE: runner missing")
        self._fixture_manifest()
        self.runner = load_module(self.root / RUNNER)
        self.receipt = load_module(self.root / "hub_scripts/skill_execution/receipt/__init__.py")
        self.folder = self.root / "synthetic_collection"
        self.folder.mkdir()
        (self.folder / "guide.md").write_bytes(b"# Synthetic guide\n")
        self.destination = self.folder / "README.md"
        self.context = {"operation": "create", "object_type": "readme", "object_name": "Synthetic collection",
                        "type_confirmed": True, "existing_capability_checked": True,
                        "existing_capability_status": "not_found", "readme_scale": "agregador",
                        "destination_relative": "synthetic_collection/README.md"}
        self.document = {"title": "Coleção sintética", "identity": "Guias sintéticos para testes locais.",
                         "purpose": "Consultar o guia desta coleção.", "usage": "Leia [o guia](guide.md).",
                         "limitations": "Não executa analytics nem comprova homologação.",
                         "next_steps": "Continue no [guia](guide.md).",
                         "items": [{"path": "guide.md", "description": "Guia sintético."}]}
        self.sequence = 0

    def tearDown(self):
        result = self._outcome.result
        failures = [text for test, text in result.failures if test.id().startswith(self.id())]
        errors = [text for test, text in result.errors if test.id().startswith(self.id())]
        skips = [reason for test, reason in result.skipped if test.id().startswith(self.id())]
        dump(self.workspace / "test_finished.json", {"test": self.id(), "pid": os.getpid(),
             "status": "ERROR" if errors else "FAIL" if failures else "NOT_RUN" if skips else "PASS",
             "errors": errors, "failures": failures, "skips": skips, "time_ns": time.time_ns()})

    def _fixture_manifest(self):
        """Real hashes of real fixture files; no bypass of release verification."""
        path = self.root / SKILL / "release_manifest.json"
        if path.exists():
            manifest = json.loads(path.read_text(encoding="utf-8"))
        else:
            artifacts = [(f"{SKILL}/SKILL.md", "skill_guidance"),
                         (f"{SKILL}/execution_contract.json", "contract"),
                         (f"{SKILL}/scripts/preflight.py", "preflight"), (RUNNER, "runner"),
                         (f"{SKILL}/scripts/_windows_writer.py", "protected_primitive"),
                         (f"{SKILL}/templates/checklist-objeto-novo.md", "checklist"),
                         ("hub_padroes/readme/template.md", "template"),
                         ("hub_scripts/skill_execution/receipt/__init__.py", "receipt_engine")]
            manifest = {"manifest_version": "0.1", "skill": "hub-ml-criar-objeto",
                        "algorithm": "git_blob_sha1", "artifacts":
                        [{"path": p, "role": r} for p, r in artifacts]}
        for item in manifest["artifacts"]:
            data = (self.root / item["path"]).read_bytes()
            item["git_blob_sha1"] = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        dump(path, manifest)

    def invoke(self, phase, *args, **kwargs):
        self.sequence += 1
        prefix = self.workspace / f"{self.sequence:02d}_{phase}"
        dump(prefix.with_suffix(".ledger.json"), {"status": "STARTED", "pid": os.getpid(), "phase": phase})
        dump(prefix.with_suffix(".before.json"), tree_bytes(self.root))
        try:
            result = getattr(self.runner, phase)(*args, assistant_root=self.root, **kwargs)
        except BaseException as exc:
            dump(prefix.with_suffix(".error.json"), {"type": type(exc).__name__, "message": str(exc)})
            raise
        finally:
            dump(prefix.with_suffix(".after.json"), tree_bytes(self.root))
        dump(prefix.with_suffix(".result.json"), result)
        return result

    def candidate(self):
        before = tree_bytes(self.root)
        result = self.invoke("generate", self.context, self.document, base_sha=BASE)
        self.assertEqual("GERADO", result["status"], result)
        self.assertIs(result["writes_performed"], False)
        self.assertEqual(before, tree_bytes(self.root))
        candidate = result["candidate"]
        self.assertEqual(BINDING_KEYS, set(candidate["binding"]))
        return candidate

    def records(self, candidate):
        auth = {"decision": "AUTHORIZE_CREATE", "binding": copy.deepcopy(candidate["binding"]),
                "authorization_id": "SYNTHETIC_TEST_RECORD", "authority": "external_confirmation_record"}
        validation = {"status": "PASS", "binding": copy.deepcopy(candidate["binding"]),
                      "validator": "repo_side_create_readme_v1", "checks": ["SYNTHETIC_BINDING_TEST_ONLY"]}
        validation["validation_id"] = self.receipt.sha256_digest(validation)
        return auth, validation

    def apply(self, candidate, auth=None, validation=None, **kwargs):
        if auth is None and validation is None:
            auth, validation = self.records(candidate)
        kwargs.setdefault("evidence_dir", self.workspace / ("apply_" + uuid.uuid4().hex))
        kwargs.setdefault("evidence_authorized", True)
        return self.invoke("apply", candidate, auth, validation, **kwargs)

    def assert_blocked_unchanged(self, callback):
        before = tree_bytes(self.root)
        result = callback()
        self.assertIn(result["status"], {"BLOCKED", "FAIL", "INCONCLUSIVE", "INTERRUPTED"}, result)
        self.assertIs(result["writes_performed"], False)
        self.assertEqual(before, tree_bytes(self.root))
        return result

    def test_deterministic_bytes_and_exact_single_create(self):
        candidate = self.candidate()
        again = self.candidate()
        data = candidate["content_utf8"].encode("utf-8")
        self.assertEqual(data, again["content_utf8"].encode("utf-8"))
        self.assertNotIn(b"\r", data)
        self.assertTrue(data.endswith(b"\n"))
        self.assertEqual(len(data), candidate["binding"]["content_size"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), candidate["binding"]["content_sha256"])
        before = tree_bytes(self.root)
        result = self.apply(candidate)
        self.assertEqual("ESCRITO", result["status"], result)
        self.assertIs(result["writes_performed"], True)
        self.assertIs(result["homologated"], False)
        self.assertEqual(data, self.destination.read_bytes())
        self.assertEqual(data, self.destination.read_bytes())
        before["synthetic_collection/README.md"] = hashlib.sha256(data).hexdigest()
        self.assertEqual(before, tree_bytes(self.root))
        self.assertTrue(self.runner.verify_evidence(result, assistant_root=self.root)["valid"])

    def test_no_authorization_or_boolean_is_not_authorization(self):
        candidate = self.candidate()
        _, validation = self.records(candidate)
        for auth in (None, {}, {"approved": True}, True):
            with self.subTest(auth=auth):
                self.assert_blocked_unchanged(lambda: self.apply(candidate, auth, validation))

    def test_each_authorization_binding_field_is_required_and_exact(self):
        candidate = self.candidate()
        for key in sorted(BINDING_KEYS):
            for mode in ("missing", "different"):
                with self.subTest(field=key, mode=mode):
                    auth, validation = self.records(candidate)
                    if mode == "missing":
                        del auth["binding"][key]
                    else:
                        value = auth["binding"][key]
                        auth["binding"][key] = value + 1 if isinstance(value, int) else value + "tamper"
                    self.assert_blocked_unchanged(lambda: self.apply(candidate, auth, validation))

    def test_authorization_record_shape_and_decision(self):
        candidate = self.candidate()
        for field, value in (("decision", "APPROVED"), ("authority", "claimed_human_identity"),
                             ("authorization_id", ""), ("binding", None)):
            with self.subTest(field=field):
                auth, validation = self.records(candidate)
                auth[field] = value
                self.assert_blocked_unchanged(lambda: self.apply(candidate, auth, validation))

    def test_validation_missing_or_nonpass_record(self):
        candidate = self.candidate()
        auth, valid = self.records(candidate)
        for validation in (None, {}, {**valid, "status": "FAIL"}, {**valid, "checks": []},
                           {**valid, "validator": "runtime_claims_repo_validator"}):
            with self.subTest(validation=validation):
                self.assert_blocked_unchanged(lambda: self.apply(candidate, auth, validation))

    def test_generated_evidence_cannot_be_tampered_into_written(self):
        result = self.invoke("generate", self.context, self.document, base_sha=BASE)
        self.assertEqual("GERADO", result["status"])
        self.assertTrue(self.runner.verify_evidence(result, assistant_root=self.root)["valid"])
        result["status"] = "ESCRITO"
        result["writes_performed"] = True
        self.assertFalse(self.runner.verify_evidence(result, assistant_root=self.root)["valid"])
        self.assertFalse(self.destination.exists())

    def test_validation_binding_or_id_mismatch(self):
        candidate = self.candidate()
        for field in ("content_sha256", "destination_relative", "base_sha", "generation_id", "validation_id"):
            with self.subTest(field=field):
                auth, validation = self.records(candidate)
                target = validation if field == "validation_id" else validation["binding"]
                target[field] = "f" * 64
                if field != "validation_id":
                    validation.pop("validation_id")
                    validation["validation_id"] = self.receipt.sha256_digest(validation)
                self.assert_blocked_unchanged(lambda: self.apply(candidate, auth, validation))

    def test_changed_candidate_bytes_or_path(self):
        candidate = self.candidate()
        auth, validation = self.records(candidate)
        for field in ("bytes", "path"):
            altered = copy.deepcopy(candidate)
            if field == "bytes":
                altered["content_utf8"] += "unauthorized\n"
            else:
                altered["binding"]["destination_relative"] = "README.md"
            self.assert_blocked_unchanged(lambda: self.apply(altered, auth, validation))

    def test_existing_destination_before_generate(self):
        self.destination.write_bytes(b"owner sentinel\n")
        self.assert_blocked_unchanged(lambda: self.invoke("generate", self.context, self.document, base_sha=BASE))

    def test_created_between_generate_and_apply_and_retry(self):
        candidate = self.candidate()
        self.destination.write_bytes(b"concurrent owner\n")
        self.assert_blocked_unchanged(lambda: self.apply(candidate))
        self.assertEqual(b"concurrent owner\n", self.destination.read_bytes())

    def test_retry_same_bytes_is_blocked(self):
        candidate = self.candidate()
        self.assertEqual("ESCRITO", self.apply(candidate)["status"])
        self.assert_blocked_unchanged(lambda: self.apply(candidate))

    def test_preflight_blocked_and_nonpilot_operations(self):
        changes = [{"type_confirmed": False}, {"operation": "convert"},
                   {"readme_scale": "objeto"}, {"object_type": "script"},
                   {"source_relative": "."}, {"overwrite": True}]
        for change in changes:
            with self.subTest(change=change):
                context = {**self.context, **change}
                self.assert_blocked_unchanged(lambda: self.invoke("generate", context, self.document, base_sha=BASE))

    def test_missing_parent_file_ancestor_and_escape(self):
        (self.root / "file_ancestor").write_bytes(b"file\n")
        for destination in ("missing/README.md", "file_ancestor/README.md", "../README.md", "C:README.md", "synthetic_collection/../README.md"):
            with self.subTest(destination=destination):
                context = {**self.context, "destination_relative": destination}
                self.assert_blocked_unchanged(lambda: self.invoke("generate", context, self.document, base_sha=BASE))

    def test_missing_and_tampered_template(self):
        template = self.root / "hub_padroes/readme/template.md"
        original = template.read_bytes()
        template.unlink()
        self.assert_blocked_unchanged(lambda: self.invoke("generate", self.context, self.document, base_sha=BASE))
        template.write_bytes(original + b"\nTAMPER\n")
        self.assert_blocked_unchanged(lambda: self.invoke("generate", self.context, self.document, base_sha=BASE))

    def test_template_changed_after_generation(self):
        candidate = self.candidate()
        template = self.root / "hub_padroes/readme/template.md"
        template.write_bytes(template.read_bytes() + b"\nTAMPER\n")
        self.assert_blocked_unchanged(lambda: self.apply(candidate))

    def test_parent_identity_replaced_after_generation(self):
        candidate = self.candidate()
        original = self.root / "original_collection"
        self.folder.rename(original)
        shutil.copytree(original, self.folder)
        self.assert_blocked_unchanged(lambda: self.apply(candidate))

    @unittest.skipUnless(os.name == "nt", "NOT_RUN: Windows pinned ancestor handle demonstration")
    def test_parent_rename_during_exclusive_create_is_prevented(self):
        candidate = self.candidate()
        original = self.runner._writer.PinnedParent.create
        attempts = []
        moved = self.root / "concurrent_moved_parent"
        def adversarial_create(pinned):
            try:
                self.folder.rename(moved)
            except OSError as exc:
                attempts.append({"renamed": False, "error": str(exc)})
            else:
                attempts.append({"renamed": True})
            return original(pinned)
        with patch.object(self.runner._writer.PinnedParent, "create", adversarial_create):
            result = self.apply(candidate)
        dump(self.workspace / "ancestor_race_observed.json", attempts)
        self.assertEqual(1, len(attempts))
        self.assertFalse(attempts[0]["renamed"], "ancestor moved while writer claims it is pinned")
        self.assertEqual("ESCRITO", result["status"], result)
        self.assertFalse(moved.exists())
        self.assertEqual(candidate["content_utf8"].encode("utf-8"), self.destination.read_bytes())

    def test_other_root_is_not_original_generation(self):
        candidate = self.candidate()
        other = self.workspace / "other_root"
        shutil.copytree(self.root, other)
        auth, validation = self.records(candidate)
        before = tree_bytes(other)
        dump(self.workspace / "other_root_before.json", before)
        result = self.runner.apply(candidate, auth, validation, assistant_root=other,
                                   evidence_dir=self.workspace / "other_evidence", evidence_authorized=True)
        self.assertNotEqual("ESCRITO", result["status"])
        self.assertFalse(result["writes_performed"])
        dump(self.workspace / "other_root_result.json", result)
        dump(self.workspace / "other_root_after.json", tree_bytes(other))
        self.assertEqual(before, tree_bytes(other))

    def test_existing_hardlink_preserves_both_names(self):
        candidate = self.candidate()
        owner = self.workspace / "hardlink_owner"
        owner.write_bytes(b"hardlink owner\n")
        try:
            os.link(owner, self.destination)
        except OSError as exc:
            self.skipTest("NOT_RUN: hardlink unavailable: " + str(exc))
        self.assert_blocked_unchanged(lambda: self.apply(candidate))
        self.assertEqual(b"hardlink owner\n", owner.read_bytes())
        self.assertTrue(owner.samefile(self.destination))

    def test_evidence_requires_explicit_external_new_directory(self):
        candidate = self.candidate()
        self.assert_blocked_unchanged(lambda: self.apply(candidate, evidence_authorized=False))
        self.assert_blocked_unchanged(lambda: self.apply(candidate, evidence_dir=self.root / "evidence"))
        existing = self.workspace / "existing_evidence"
        existing.mkdir()
        (existing / "sentinel").write_bytes(b"evidence owner")
        self.assert_blocked_unchanged(lambda: self.apply(candidate, evidence_dir=existing))
        self.assertEqual(b"evidence owner", (existing / "sentinel").read_bytes())

    def test_evidence_parent_file_blocks_before_product_write(self):
        candidate = self.candidate()
        parent = self.workspace / "evidence_parent_file"
        parent.write_bytes(b"owner")
        self.assert_blocked_unchanged(lambda: self.apply(candidate, evidence_dir=parent / "receipt"))

    @unittest.skipUnless(os.name == "nt", "NOT_RUN: Windows volume API fault injection")
    def test_unsupported_filesystem_fails_closed(self):
        api = self.runner._writer._api()
        calls = []
        class UnsupportedVolume:
            def __getattr__(self, name):
                return getattr(api, name)
            def GetVolumeInformationW(self, anchor, label, label_size, serial, maximum, flags, filesystem, size):
                calls.append(anchor)
                filesystem.value = "FAT32"
                return 1
        with patch.object(self.runner._writer, "_api", return_value=UnsupportedVolume()):
            result = self.assert_blocked_unchanged(lambda: self.invoke("generate", self.context, self.document, base_sha=BASE))
        self.assertTrue(calls, "unsupported filesystem injection was not reached")
        self.assertIn("UNSUPPORTED_FILESYSTEM", json.dumps(result))

    def make_link(self, target, link):
        if os.name == "nt":
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
        else:
            link.symlink_to(target, target_is_directory=True)
        self.assertTrue(link.is_junction() if os.name == "nt" else link.is_symlink())
        def cleanup():
            if link.is_symlink() or getattr(link, "is_junction", lambda: False)():
                link.rmdir() if os.name == "nt" else link.unlink()
        self.addCleanup(cleanup)

    def test_junction_or_symlink_ancestor_is_not_supported(self):
        link = self.root / "alias"
        self.make_link(self.folder, link)
        context = {**self.context, "destination_relative": "alias/README.md"}
        self.assert_blocked_unchanged(lambda: self.invoke("generate", context, self.document, base_sha=BASE))
        self.assertFalse(self.destination.exists())

    def test_cycle_is_blocked_without_traversal(self):
        target = self.root / "cycle"
        target.mkdir()
        link = self.root / "cycle_initial"
        self.make_link(target, link)
        target.rmdir()
        link.rename(target)
        def cleanup():
            target.rmdir() if os.name == "nt" else target.unlink()
        self.addCleanup(cleanup)
        context = {**self.context, "destination_relative": "cycle/README.md"}
        self.assert_blocked_unchanged(lambda: self.invoke("generate", context, self.document, base_sha=BASE))

    def test_parent_replaced_by_external_junction_after_generation(self):
        candidate = self.candidate()
        outside = self.workspace / "outside"
        outside.mkdir()
        (outside / "sentinel").write_bytes(b"external owner")
        self.folder.rename(self.root / "saved_collection")
        self.make_link(outside, self.folder)
        outside_before = tree_bytes(outside)
        self.assert_blocked_unchanged(lambda: self.apply(candidate))
        self.assertEqual(outside_before, tree_bytes(outside))

    def spawn_apply(self, candidate, label, barrier, fault=None):
        auth, validation = self.records(candidate)
        request = self.workspace / (label + "_request.json")
        dump(request, {"candidate": candidate, "authorization": auth, "validation": validation, "fault": fault})
        result = self.workspace / (label + "_result.json")
        ready = self.workspace / (label + "_ready.json")
        command = [sys.executable, "-B", "-c", WORKER, str(self.root), str(request), str(barrier),
                   str(self.workspace / (label + "_evidence")), str(result), str(ready)]
        dump(self.workspace / (label + "_ledger.json"), {"status": "STARTED", "argv": command})
        stdout = (self.workspace / (label + "_stdout.txt")).open("wb")
        stderr = (self.workspace / (label + "_stderr.txt")).open("wb")
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
        def cleanup():
            if process.poll() is None:
                process.kill()
            process.wait(timeout=10)
            stdout.close()
            stderr.close()
        self.addCleanup(cleanup)
        return process, result, ready

    def await_ready(self, processes):
        deadline = time.monotonic() + 20
        while not all(ready.exists() for _, _, ready in processes):
            self.assertLess(time.monotonic(), deadline, "process readiness deadline exceeded")
            for process, _, ready in processes:
                if not ready.exists():
                    self.assertIsNone(process.poll(), "worker exited before ready")
            time.sleep(.01)
        for process, _, ready in processes:
            self.assertEqual(process.pid, json.loads(ready.read_text())["pid"])

    def test_two_real_processes_only_one_creates(self):
        candidate = self.candidate()
        before = tree_bytes(self.root)
        barrier = self.workspace / "release_barrier"
        processes = [self.spawn_apply(candidate, f"competitor_{i}", barrier) for i in range(2)]
        self.await_ready(processes)
        self.assertNotEqual(processes[0][0].pid, processes[1][0].pid)
        barrier.write_bytes(b"GO")
        observed = []
        for process, result, _ in processes:
            code = process.wait(timeout=30)
            payload = json.loads(result.read_text(encoding="utf-8"))
            self.assertEqual(process.pid, payload["pid"])
            observed.append({"pid": process.pid, "exit": code, "payload": payload["payload"]})
        dump(self.workspace / "concurrency_observed.json", observed)
        self.assertEqual([0, 2], sorted(item["exit"] for item in observed))
        self.assertEqual(1, sum(item["payload"]["status"] == "ESCRITO" for item in observed))
        self.assertEqual(1, sum(item["payload"]["writes_performed"] is True for item in observed))
        data = candidate["content_utf8"].encode("utf-8")
        self.assertEqual(data, self.destination.read_bytes())
        before["synthetic_collection/README.md"] = hashlib.sha256(data).hexdigest()
        self.assertEqual(before, tree_bytes(self.root))

    def test_real_process_interrupted_before_apply_preserves_tree(self):
        candidate = self.candidate()
        before = tree_bytes(self.root)
        barrier = self.workspace / "never_released"
        worker = self.spawn_apply(candidate, "interrupted", barrier)
        self.await_ready([worker])
        process, result, _ = worker
        process.terminate()
        code = process.wait(timeout=10)
        dump(self.workspace / "interruption_observed.json", {"pid": process.pid, "exit": code,
             "status": "INTERRUPTED", "result_exists": result.exists(), "phase": "BEFORE_APPLY"})
        self.assertNotEqual(0, code)
        self.assertFalse(result.exists())
        self.assertEqual(before, tree_bytes(self.root))

    def test_partial_write_failure_preserves_partial_bytes_and_blocks_retry(self):
        candidate = self.candidate()
        data = candidate["content_utf8"].encode("utf-8")
        original = os.write
        calls = []
        def fail_after_partial(fd, content):
            calls.append(len(content))
            if len(calls) == 1:
                return original(fd, content[:17])
            raise OSError("SYNTHETIC partial write failure")
        with patch.object(self.runner.os, "write", fail_after_partial):
            result = self.apply(candidate)
        self.assertGreaterEqual(len(calls), 2)
        self.assertEqual("INCONCLUSIVE", result["status"], result)
        self.assertIs(result["writes_performed"], True)
        self.assertEqual(data[:17], self.destination.read_bytes())
        self.assert_blocked_unchanged(lambda: self.apply(candidate))

    @unittest.skipUnless(os.name == "nt", "NOT_RUN: Win32 HANDLE-to-fd boundary")
    def test_fd_conversion_failure_reports_real_created_empty_file(self):
        import msvcrt
        candidate = self.candidate()
        with patch.object(msvcrt, "open_osfhandle", side_effect=OSError("SYNTHETIC handle conversion failure")) as fault:
            result = self.apply(candidate)
        self.assertTrue(fault.called)
        self.assertTrue(self.destination.exists(), "CREATE_NEW happened before fd conversion")
        self.assertEqual(b"", self.destination.read_bytes())
        self.assertIs(result["writes_performed"], True, result)
        self.assertEqual("INCONCLUSIVE", result["status"], result)
        self.assert_blocked_unchanged(lambda: self.apply(candidate))

    def test_close_failure_preserves_effect_and_does_not_claim_success(self):
        candidate = self.candidate()
        original = os.close
        calls = []
        def close_then_fail(fd):
            original(fd)
            calls.append(fd)
            raise OSError("SYNTHETIC close failure after actual close")
        with patch.object(self.runner.os, "close", close_then_fail):
            result = self.apply(candidate)
        self.assertTrue(calls)
        self.assertEqual(candidate["content_utf8"].encode("utf-8"), self.destination.read_bytes())
        self.assertIs(result["writes_performed"], True, result)
        self.assertEqual("INCONCLUSIVE", result["status"], result)

    def test_reread_mismatch_is_not_success(self):
        candidate = self.candidate()
        original = os.read
        calls = []
        def mismatching_read(fd, size):
            content = original(fd, size)
            calls.append(len(content))
            return b"X" + content[1:] if content else content
        with patch.object(self.runner.os, "read", mismatching_read):
            result = self.apply(candidate)
        self.assertTrue(calls, "fault must reach reread primitive")
        self.assertEqual("INCONCLUSIVE", result["status"], result)
        self.assertIs(result["writes_performed"], True)
        self.assertEqual(candidate["content_utf8"].encode("utf-8"), self.destination.read_bytes())

    def test_evidence_persistence_failure_before_create_blocks(self):
        candidate = self.candidate()
        with patch.object(self.runner, "_persist", side_effect=OSError("SYNTHETIC evidence failure")) as observed:
            self.assert_blocked_unchanged(lambda: self.apply(candidate))
        self.assertTrue(observed.called)

    def test_evidence_persistence_failure_after_create_preserves_effect(self):
        candidate = self.candidate()
        original = self.runner._persist
        triggered = []
        def fail_after_write(path, payload):
            if self.destination.exists():
                triggered.append(str(path))
                raise OSError("SYNTHETIC final evidence failure")
            return original(path, payload)
        with patch.object(self.runner, "_persist", fail_after_write):
            result = self.apply(candidate)
        self.assertTrue(triggered)
        self.assertEqual("INCONCLUSIVE", result["status"], result)
        self.assertIs(result["writes_performed"], True)
        # The first evidence after CREATE_NEW precedes content writing.
        self.assertEqual(b"", self.destination.read_bytes())

    def test_final_evidence_failure_preserves_complete_bytes(self):
        candidate = self.candidate()
        original = self.runner._persist
        triggered = []
        def fail_final(path, payload):
            if payload.get("status") == "ESCRITO" or triggered:
                triggered.append(str(path))
                raise OSError("SYNTHETIC final evidence failure")
            return original(path, payload)
        with patch.object(self.runner, "_persist", fail_final):
            result = self.apply(candidate)
        self.assertTrue(triggered)
        self.assertEqual("INCONCLUSIVE", result["status"], result)
        self.assertIs(result["writes_performed"], True)
        self.assertEqual(candidate["content_utf8"].encode("utf-8"), self.destination.read_bytes())

    def test_real_process_interrupted_during_write_retains_partial_file(self):
        candidate = self.candidate()
        before = tree_bytes(self.root)
        barrier = self.workspace / "partial_release"
        worker = self.spawn_apply(candidate, "partial_interrupted", barrier, fault="partial_pause")
        self.await_ready([worker])
        process, result, ready = worker
        barrier.write_bytes(b"GO")
        deadline = time.monotonic() + 20
        while True:
            try:
                observed = json.loads(ready.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                observed = {}
            if observed.get("phase") == "PARTIAL_WRITE":
                break
            self.assertLess(time.monotonic(), deadline, "partial write readiness deadline exceeded")
            self.assertIsNone(process.poll(), "worker exited before partial-write marker")
            time.sleep(.01)
        self.assertEqual(process.pid, observed["pid"])
        self.assertEqual(17, observed["bytes"])
        process.terminate()
        code = process.wait(timeout=10)
        dump(self.workspace / "partial_interruption_observed.json", {**observed, "exit": code,
             "status": "INTERRUPTED", "result_exists": result.exists()})
        self.assertNotEqual(0, code)
        self.assertFalse(result.exists())
        partial = candidate["content_utf8"].encode("utf-8")[:17]
        self.assertEqual(partial, self.destination.read_bytes())
        before["synthetic_collection/README.md"] = hashlib.sha256(partial).hexdigest()
        self.assertEqual(before, tree_bytes(self.root))
        evidence = self.workspace / "partial_interrupted_evidence"
        self.assertTrue(list(evidence.glob("*.json")), "pre-write evidence must survive interruption")
        self.assert_blocked_unchanged(lambda: self.apply(candidate))


if __name__ == "__main__":
    unittest.main()
