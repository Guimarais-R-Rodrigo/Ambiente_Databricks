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
        self.source = self.repo / "ambiente_fonte"
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
        for bad in (".", ".artifacts", "ambiente_fonte", "../escape", ".artifacts/../escape"):
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

    def test_check_read_only_and_cli_modes_exclusive(self):
        before = inventory(self.user)
        self.assertEqual(0, self.render("--check").returncode)
        self.assertEqual(before, inventory(self.user))
        self.assertNotEqual(0, self.render("--write", "--check").returncode)


if __name__ == "__main__":
    unittest.main()
