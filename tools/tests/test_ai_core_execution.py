"""Execution-coverage mutants for core; the frozen method AST stays untouched."""
from __future__ import annotations

import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TOOLS))
import ci_local
import package_boundary as boundary
import run_core_tests as core
from tools.skill_enforcement.parallel import coverage


class CoreExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original_path = sys.path[:]
        original_modules = {name: module for name, module in sys.modules.items()
                            if name == "hub_snippets" or name.startswith("hub_snippets.")}

        def restore_fixture_imports():
            # The fixture is deleted after this class. Do not leave its package
            # __path__ in the process and break later real B0/Temas discovery.
            for name in list(sys.modules):
                if name == "hub_snippets" or name.startswith("hub_snippets."):
                    sys.modules.pop(name)
            sys.modules.update(original_modules)
            sys.path[:] = original_path

        cls.temp = tempfile.TemporaryDirectory(prefix="core execution with spaces ")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.addClassCleanup(restore_fixture_imports)
        cls.root = Path(cls.temp.name)
        for relative in ("tools/tests/runtime", "ambiente_databricks/.assistant"):
            shutil.copytree(ROOT / relative, cls.root / relative,
                            ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(TOOLS / "run_core_tests.py", cls.root / "tools/run_core_tests.py")
        cls.path = cls.root / boundary.CORE_PATH
        cls.original = cls.path.read_text(encoding="utf-8")
        cls.signature = boundary.core_signature(cls.path)

    def setUp(self):
        self.path.write_text(self.original, encoding="utf-8")

    def check_mutant(self, source):
        self.assertNotEqual(self.original, source)
        self.path.write_text(source, encoding="utf-8")
        self.assertEqual(self.signature, boundary.core_signature(self.path))
        report = core.run_core(self.root, stream=io.StringIO())
        self.assertEqual("FAIL", report["status"], report)
        return report

    def test_current_core_executes_all_expected_ids_once_without_skips(self):
        report = core.run_core(self.root, stream=io.StringIO())
        self.assertEqual("PASS", report["status"])
        self.assertEqual(45, report["tests_run"])
        self.assertEqual(report["expected_ids"], sorted(report["successful_ids"]))
        for key in ("skipped", "missing_ids", "unexpected_ids", "duplicate_ids"):
            self.assertEqual([], report[key])

    def test_original_all_class_skip_mutant_fails_execution_guard(self):
        report = self.check_mutant(self.original.replace(
            "class ", '@unittest.skip("audit synthetic")\nclass '))
        self.assertEqual(45, len(report["skipped"]))
        self.assertEqual(45, len(report["missing_ids"]))

    def test_original_no_testcase_bases_mutant_fails_empty_discovery(self):
        report = self.check_mutant(self.original.replace("(unittest.TestCase)", "(object)"))
        self.assertEqual(0, report["tests_run"])
        self.assertEqual(45, len(report["missing_ids"]))

    def test_one_class_and_class_setup_skips_cannot_pass(self):
        for prefix in ('@unittest.skip("one class")\nclass FormatTests(unittest.TestCase):',
                       'class FormatTests(unittest.TestCase):\n'
                       '    @classmethod\n'
                       '    def setUpClass(cls):\n'
                       '        raise unittest.SkipTest("class setup")'):
            with self.subTest(prefix=prefix):
                report = self.check_mutant(self.original.replace(
                    "class FormatTests(unittest.TestCase):", prefix))
                self.assertEqual(2, len(report["missing_ids"]))
                self.assertTrue(report["skipped"])

    def test_module_setup_skip_cannot_pass(self):
        report = self.check_mutant(self.original + '\ndef setUpModule():\n'
                                  '    raise unittest.SkipTest("module setup")\n')
        self.assertEqual(0, report["tests_run"])
        self.assertEqual(45, len(report["missing_ids"]))
        self.assertTrue(report["skipped"])

    def test_load_tests_empty_filtered_and_duplicate_suites_cannot_pass(self):
        hooks = {
            "empty": "return unittest.TestSuite()",
            "filtered": "return loader.loadTestsFromTestCase(FormatTests)",
            "duplicate": "return unittest.TestSuite([tests, loader.loadTestsFromTestCase(FormatTests)])",
        }
        for name, body in hooks.items():
            with self.subTest(name=name):
                report = self.check_mutant(self.original + '\ndef load_tests(loader, tests, pattern):\n    ' + body + '\n')
                if name == "duplicate":
                    self.assertEqual(2, len(report["duplicate_ids"]))
                else:
                    self.assertTrue(report["missing_ids"])

    def test_unexpected_runtime_test_ids_cannot_pass(self):
        report = self.check_mutant(self.original + '\nUnexpected = type("Unexpected", (unittest.TestCase,), '
                                  '{"test_added": lambda self: None, "__module__": __name__})\n')
        self.assertEqual([core.MODULE_NAME + ".Unexpected.test_added"], report["unexpected_ids"])

    def test_normal_failures_errors_and_expected_failures_still_fail(self):
        for raised in ('AssertionError("failure")', 'RuntimeError("error")'):
            with self.subTest(raised=raised):
                report = self.check_mutant(self.original.replace(
                    'class FormatTests(unittest.TestCase):',
                    'class FormatTests(unittest.TestCase):\n    def setUp(self):\n        raise ' + raised))
                self.assertEqual(2, report["failures"] + report["errors"])
        expected_failure = (self.original + '\nFormatTests.test_percent_scale_is_explicit = '
                            'unittest.expectedFailure(lambda self: self.fail("expected"))\n')
        report = self.check_mutant(expected_failure)
        self.assertEqual(1, report["expected_failures"])
        self.assertEqual(1, len(report["missing_ids"]))

    def test_fingerprint_failure_stops_before_loading_the_module(self):
        self.path.write_text(self.original.replace('fmt_brl(1.999)', 'fmt_brl(2.999)') +
                             '\nraise RuntimeError("must never import")\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "CORE_CASES_OR_ASSERTIONS_CHANGED"):
            core.run_core(self.root, stream=io.StringIO())

    def test_cli_fails_closed_for_skips_filtered_discovery_and_system_exit(self):
        variants = [self.original.replace("class ", '@unittest.skip("audit synthetic")\nclass '),
                    self.original + '\ndef load_tests(loader, tests, pattern):\n    return unittest.TestSuite()\n',
                    self.original + '\nraise SystemExit(0)\n']
        for source in variants:
            with self.subTest(source=source[-100:]):
                self.path.write_text(source, encoding="utf-8")
                proc = subprocess.run([sys.executable, "-B", str(TOOLS / "run_core_tests.py"),
                                       "--root", str(self.root)], cwd=self.root,
                                      text=True, capture_output=True)
                self.assertEqual(1, proc.returncode, proc.stderr)
                self.assertEqual("FAIL", json.loads(proc.stdout)["status"])

    def test_success_callbacks_cannot_hide_missing_start_or_stop(self):
        class Incomplete(unittest.TestCase):
            def run(self, result):
                result.addSuccess(self)
        test = Incomplete()
        report = core.run_suite(unittest.TestSuite([test]), {test.id()}, stream=io.StringIO())
        self.assertEqual("FAIL", report["status"])

    def test_local_gate_uses_guarded_runner(self):
        stage = next(stage for stage in ci_local.ETAPAS if stage[0] == "biblioteca")
        self.assertEqual([sys.executable, "-B", "tools/run_core_tests.py"], stage[2])

    def test_b0_maps_runner_to_actual_core_ids_without_execution(self):
        recipes = [[sys.executable, "-B", "tools/run_core_tests.py"],
                   [sys.executable, "-B", "-m", "tools.run_core_tests", "-v"]]
        expected = {boundary.CORE_PATH + "::" + name.removeprefix(core.MODULE_NAME + ".")
                    for name in core.expected_ids(self.root)}
        for argv in recipes:
            with self.subTest(argv=argv), mock.patch.object(coverage, "ROOT", self.root):
                with mock.patch.object(unittest.TestCase, "run", side_effect=AssertionError("must not execute")):
                    ids, errors, paths = coverage._collect_command(argv)
                self.assertEqual([], errors)
                self.assertEqual(expected, set(ids))
                self.assertEqual(45, len(ids))
                self.assertEqual([self.root / boundary.CORE_PATH], paths)

    def test_b0_mapping_still_rejects_omitted_discovery_and_missing_inputs(self):
        argv = [sys.executable, "-B", "tools/run_core_tests.py"]
        with mock.patch.object(coverage, "ROOT", self.root):
            self.path.write_text(self.original.replace("(unittest.TestCase)", "(object)"), encoding="utf-8")
            row = coverage._row("ci:biblioteca", "CURRENT_INVARIANT", argv, set(), {})
            self.assertNotEqual("MAPPED", row["mapping_status"])
            self.assertEqual(45, len(row["ast_methods"]))
            self.assertTrue(any(e.startswith("AST_TEST_NOT_COLLECTED:") for e in row["collection_errors"]))
            self.path.unlink()
            ids, errors, _ = coverage._collect_command(argv)
            self.assertFalse(ids)
            self.assertTrue(any(e.startswith("TARGET_MISSING:") for e in errors))
            self.path.write_text(self.original, encoding="utf-8")
            runner = self.root / "tools/run_core_tests.py"
            source = runner.read_bytes()
            runner.unlink()
            try:
                ids, errors, _ = coverage._collect_command(argv)
                self.assertFalse(ids)
                self.assertIn("CORE_RUNNER_MISSING:tools/run_core_tests.py", errors)
            finally:
                runner.write_bytes(source)

    def test_b0_mapping_rejects_unknown_runner_flags_and_root_overrides(self):
        for argv in ([sys.executable, "tools/run_core_tests.py", "--root", "elsewhere"],
                     [sys.executable, "tools/run_core_tests.py", "--filter", "one"],
                     ["bash", "tools/run_core_tests.py"],
                     [sys.executable, "-m", "unittest", "tools.run_core_tests"]):
            with self.subTest(argv=argv), mock.patch.object(coverage, "ROOT", self.root):
                ids, errors, _ = coverage._collect_command(argv)
                self.assertFalse(ids)
                self.assertIn("CORE_RUNNER_ARGS_UNSUPPORTED", errors)


class LocalHelpTests(unittest.TestCase):
    def test_help_enumerates_current_stage_ids_descriptions_and_commands(self):
        proc = subprocess.run([sys.executable, "-B", str(TOOLS / "ci_local.py"), "--help"],
                              cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn(ci_local.ajuda_etapas(), proc.stdout)
        self.assertNotIn("hub_snippets/tests/test_core.py", proc.stdout)
        for index, (name, description, command) in enumerate(ci_local.ETAPAS, 1):
            self.assertIn(f"{index}. {name}: {description}", proc.stdout)
        self.assertIn("parcial sem renderer", proc.stdout)
        self.assertIn("tools/run_core_tests.py", proc.stdout)

    def test_help_tracks_stage_changes_without_a_second_list(self):
        stage = ("synthetic", "Descrição sintética", [sys.executable, "tools/synthetic.py"])
        with mock.patch.object(ci_local, "ETAPAS", [stage]):
            self.assertEqual("Etapas executadas, em ordem:\n1. synthetic: Descrição sintética\n"
                             "   python tools/synthetic.py", ci_local.ajuda_etapas())


if __name__ == "__main__":
    unittest.main()
