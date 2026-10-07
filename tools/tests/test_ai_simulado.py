"""Ignored-output parity mutants; no Git index or symlink compatibility shim."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from simulado import inventory, parity_errors
from project_policy import simulated_root


class SimuladoParityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="simulado output with spaces ")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        (self.repo / "tools").mkdir()
        for name in ("render_simulado.py", "project_policy.py", "simulado.py", "notebook_marker.py"):
            shutil.copyfile(TOOLS / name, self.repo / "tools" / name)
        self.source = self.repo / "ambiente_databricks"
        (self.source / ".assistant/empty").mkdir(parents=True)
        (self.source / ".assistant_instructions.md").write_bytes(b"instructions\r\n")
        (self.source / ".assistant/module.py").write_bytes(b"value = 1\r\n")
        (self.source / ".assistant/notebook.py").write_bytes(b"# Databricks notebook source\nvalue = 2\n")
        self.assertEqual(0, self.render("--write").returncode)
        self.target = simulated_root(self.repo)
        self.user = self.target / "Users/usuario-free"

    def render(self, *args):
        return subprocess.run([sys.executable, "-B", "tools/render_simulado.py", *args],
                              cwd=self.repo, capture_output=True, text=True, timeout=15)

    def test_clean_generation_and_second_generation_match_without_git(self):
        self.assertFalse((self.repo / ".git").exists())
        self.assertFalse((self.repo / "Novo_Ambiente_Simulado").exists())
        self.assertEqual([], parity_errors(self.repo))
        first = inventory(self.user)
        self.assertEqual("FILE", first[".assistant/module.py"]["object_type"])
        self.assertEqual("NOTEBOOK", first[".assistant/notebook.py"]["object_type"])
        self.assertEqual(0, self.render("--write").returncode)
        self.assertEqual(first, inventory(self.user))

    def test_missing_extra_byte_and_type_mutants_fail(self):
        for variant in ("missing", "extra", "bytes", "type", "empty-dir", "outer"):
            with self.subTest(variant=variant):
                self.assertEqual(0, self.render("--write").returncode)
                file = self.user / ".assistant/module.py"
                if variant == "missing": file.unlink()
                elif variant == "extra": (self.user / ".assistant/extra.py").write_text("extra")
                elif variant == "bytes": file.write_bytes(file.read_bytes().replace(b"\r\n", b"\n"))
                elif variant == "type": file.unlink(); file.mkdir()
                elif variant == "empty-dir": (self.user / ".assistant/alien-empty").mkdir()
                elif variant == "outer": (self.target / "outside.txt").write_text("extra")
                self.assertNotEqual(0, self.render("--check").returncode)

    def test_source_cache_ignored_but_output_cache_rejected(self):
        cache = self.source / ".assistant/__pycache__"
        cache.mkdir(); (cache / "module.pyc").write_bytes(b"cache")
        self.assertEqual(0, self.render("--write").returncode)
        self.assertEqual([], parity_errors(self.repo))
        (self.user / ".assistant/module.pyc").write_bytes(b"cache")
        self.assertTrue(parity_errors(self.repo))

    def test_explicit_root_shared_and_default_unchanged(self):
        alternate = ".artifacts/release proof/simulado"
        self.assertEqual(0, self.render("--write", "--output-root", alternate).returncode)
        self.assertEqual([], parity_errors(self.repo, alternate))
        self.assertEqual([], parity_errors(self.repo))
        for bad in (".", ".artifacts", "ambiente_databricks", "../escape", ".artifacts/../escape"):
            with self.subTest(bad=bad):
                self.assertNotEqual(0, self.render("--write", "--output-root", bad).returncode)
        self.assertTrue((self.source / ".assistant/module.py").is_file())

    def test_empty_assistant_and_missing_instruction_fail(self):
        for file in (self.source / ".assistant").glob("*.py"): file.unlink()
        self.assertNotEqual(0, self.render("--write").returncode)
        (self.source / ".assistant/module.py").write_text("x=1")
        (self.source / ".assistant_instructions.md").unlink()
        self.assertNotEqual(0, self.render("--write").returncode)

    @unittest.skipIf(os.name == "nt", "symlink privileges are runner-specific")
    def test_symlinks_source_target_and_ancestor_rejected(self):
        original = self.user / ".assistant/module.py"
        for variant in ("source", "target", "ancestor"):
            with self.subTest(variant=variant):
                link = ((self.source / ".assistant/alias") if variant == "source" else
                        (self.target / "alias") if variant == "target" else self.repo / ".artifacts/alias")
                link.symlink_to(self.source, target_is_directory=True)
                try:
                    result = (self.render("--write", "--output-root", ".artifacts/alias/nested")
                              if variant == "ancestor" else self.render("--write"))
                    self.assertNotEqual(0, result.returncode)
                    self.assertTrue(original.is_file())
                finally:
                    link.unlink()

    @unittest.skipIf(os.name == "nt", "symlink privileges are runner-specific")
    def test_source_root_link_rejected_before_any_output_mutation(self):
        # Both directories belong to this disposable fixture. The sentinel is
        # deliberately outside the repository, never a user file.
        with tempfile.TemporaryDirectory(prefix="external synthetic source ") as raw:
            external = Path(raw)
            shutil.copytree(self.source, external / "source")
            external_source = external / "source"
            (external_source / ".assistant/module.py").write_bytes(b"synthetic external only\n")
            before_source = inventory(external_source, source=True)
            before_target = inventory(self.target)
            shutil.rmtree(self.source)
            self.source.symlink_to(external_source, target_is_directory=True)
            for args in ((), ("--write",), ("--check",)):
                with self.subTest(args=args):
                    result = self.render(*args)
                    self.assertNotEqual(0, result.returncode, result.stdout)
                    self.assertIn("link simbólico", result.stdout)
                    self.assertEqual(before_target, inventory(self.target))
                    self.assertEqual(before_source, inventory(external_source, source=True))
            self.assertTrue(parity_errors(self.repo))

    @unittest.skipIf(os.name == "nt", "symlink privileges are runner-specific")
    def test_inventory_and_renderer_refuse_lexical_repository_ancestor(self):
        before = inventory(self.target)
        with tempfile.TemporaryDirectory(prefix="lexical ancestor fixture ") as raw:
            alias = Path(raw) / "repository-link"
            alias.symlink_to(self.repo, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "link simbólico"):
                inventory(alias / "ambiente_databricks", source=True)
            self.assertTrue(parity_errors(alias))
            result = subprocess.run(
                [sys.executable, "-B", str(alias / "tools/render_simulado.py"), "--write"],
                cwd=self.repo, capture_output=True, text=True, timeout=15,
            )
            self.assertNotEqual(0, result.returncode, result.stdout)
            self.assertEqual(before, inventory(self.target))

    def test_inventory_rejects_junction_ancestor_before_reading(self):
        # This exercises the portable guard only; native Windows remains untested.
        with mock.patch.object(Path, "is_junction", create=True,
                               side_effect=lambda: True), \
             mock.patch.object(Path, "read_bytes", side_effect=AssertionError("must not read")):
            with self.assertRaisesRegex(ValueError, "junction"):
                inventory(self.source, source=True)

    def test_publisher_preserves_custom_neutral_username_without_remote_calls(self):
        import publicar_free as publisher
        self.assertEqual(0, self.render("--write", "--username", "fixture-user").returncode)
        with mock.patch.object(publisher, "REPO_ROOT", self.repo), \
             mock.patch.object(publisher, "FONTE", self.source), \
             mock.patch.object(publisher, "SIMULADO", self.target), \
             mock.patch.object(publisher, "resolve_home", return_value=("/Users/synthetic", "synthetic", "https://example.invalid", None)), \
             mock.patch.object(publisher, "cmd_plan", return_value=0) as plan, \
             mock.patch.object(sys, "argv", ["publicar_free.py"]):
            self.assertEqual(0, publisher.main())
            self.assertEqual("fixture-user", plan.call_args.args[0].name)

    def test_check_read_only_and_cli_modes_exclusive(self):
        before = inventory(self.user)
        self.assertEqual(0, self.render("--check").returncode)
        self.assertEqual(before, inventory(self.user))
        self.assertNotEqual(0, self.render("--write", "--check").returncode)


if __name__ == "__main__":
    unittest.main()
