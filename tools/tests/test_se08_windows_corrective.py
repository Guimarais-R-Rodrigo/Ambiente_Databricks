"""Guardrails da corretiva SE08 Windows/CI.

Estes testes são estáticos/portáveis. Não afirmam reproduzir WinError32, NTFS ou
privilégio de symlink; protegem apenas a instrumentação e os reparos de teste.
"""
from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class SE08WindowsCorrectiveStaticTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_certifier_cleanup_diagnostic_is_observational(self):
        text = self.read("tools/skill_enforcement/certify_local.py")
        self.assertIn("def _temporary_cleanup_observation(", text)
        self.assertIn('"temporary_cleanup_pre_remove"', text)
        helper = ast.parse(text)
        fn = next(n for n in helper.body if isinstance(n, ast.FunctionDef)
                  and n.name == "_temporary_cleanup_observation")
        calls = {getattr(n.func, "attr", getattr(n.func, "id", ""))
                 for n in ast.walk(fn) if isinstance(n, ast.Call)}
        for forbidden in ("sleep", "rmtree", "unlink", "remove", "kill", "terminate"):
            self.assertNotIn(forbidden, calls)

    def test_se08_operational_module_is_valid_python(self):
        text = self.read("tools/tests/test_skill_enforcement_se08.py")
        ast.parse(text)

    def test_validator_disables_bytecode_before_local_imports(self):
        text = self.read("tools/validate_assistant.py")
        lines = text.splitlines()
        guard = next(i for i, line in enumerate(lines)
                     if "sys.dont_write_bytecode = True" in line)
        local_import = next(i for i, line in enumerate(lines)
                            if line.startswith("from readme_objeto_contract import"))
        self.assertLess(guard, local_import)

    def test_native_winerror32_observer_is_post_failure_only(self):
        text = self.read("tools/skill_enforcement/certify_local.py")
        tree = ast.parse(text)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "_windows_cleanup_failure_observation")
        calls = {getattr(n.func, "attr", getattr(n.func, "id", ""))
                 for n in ast.walk(fn) if isinstance(n, ast.Call)}
        for forbidden in ("sleep", "rmtree", "unlink", "remove", "kill", "terminate"):
            self.assertNotIn(forbidden, calls)
        self.assertIn("windows_cleanup_failure_observation", text)
        self.assertIn('record["windows_job_after_terminate"]', text)
        self.assertIn('record["windows_job_before_close"]', text)

    def test_ci_failure_output_is_not_truncated(self):
        text = self.read("tools/ci_local.py")
        self.assertNotIn('[:4000]', text)
        self.assertIn('saida.strip().replace("\\n", "\\n   ")', text)

    def test_file_owner_pid_query_is_diagnostic_only(self):
        text = self.read("tools/skill_enforcement/cleanup_diagnostics.py")
        tree = ast.parse(text)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "file_process_ids_using_file")
        calls = {getattr(n.func, "attr", getattr(n.func, "id", ""))
                 for n in ast.walk(fn) if isinstance(n, ast.Call)}
        for forbidden in ("sleep", "rmtree", "unlink", "remove", "kill", "terminate"):
            self.assertNotIn(forbidden, calls)
        self.assertIn("FileProcessIdsUsingFileInformation", text)
        self.assertIn("observer_pid_may_be_query_handle", text)

    def test_process_stream_uses_share_delete_without_retry(self):
        text = self.read("tools/skill_enforcement/certify_local.py")
        tree = ast.parse(text)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "_open_process_stream")
        calls = {getattr(n.func, "attr", getattr(n.func, "id", ""))
                 for n in ast.walk(fn) if isinstance(n, ast.Call)}
        self.assertIn("CreateFileW", text)
        self.assertIn("FILE_SHARE_DELETE", text)
        self.assertIn("_open_process_stream(path / \"stdout\")", text)
        self.assertIn("_open_process_stream(path / \"stderr\")", text)
        for forbidden in ("sleep", "rmtree", "unlink", "remove", "kill", "terminate"):
            self.assertNotIn(forbidden, calls)

    def test_theme_dependency_probe_ignores_python_environment(self):
        text = self.read("tools/tests/test_temas_v02.py")
        self.assertGreaterEqual(text.count("'PYTHONPATH'"), 2)
        self.assertGreaterEqual(text.count("'-B','-E','-S','-c'"), 2)

    def test_theme_layout_mocks_do_not_depend_on_posix_separator(self):
        text = self.read("tools/tests/test_temas_v02.py")
        self.assertIn("def _path_endswith(", text)
        for legacy in (
            "endswith('V01/theme.schema.json')",
            "endswith('exemplos/legado_notebook.json')",
            "endswith('identidade_visual/TOKENS.md')",
            "endswith('tema/__init__.py')",
            "endswith('identidade_visual/theme.schema.json')",
        ):
            self.assertNotIn(legacy, text)
        self.assertIn("PureWindowsPath", text)

    def test_restricted_symlink_environment_is_explicit_not_pass(self):
        for path in (
            "tools/tests/test_temas_v01.py",
            "tools/tests/test_temas_v02.py",
            "tools/tests/test_temas_v05_integracao.py",
            "tools/tests/test_transicao_trabalho.py",
            "tools/tests/test_readme_objeto_contract.py",
        ):
            text = self.read(path)
            self.assertIn("skipTest", text, path)
        # Não substituir a propriedade original por junction nesses testes.
        for path in (
            "tools/tests/test_temas_v01.py",
            "tools/tests/test_temas_v02.py",
            "tools/tests/test_transicao_trabalho.py",
            "tools/tests/test_readme_objeto_contract.py",
        ):
            self.assertNotIn("CreateJunction", self.read(path), path)


if __name__ == "__main__":
    unittest.main()
