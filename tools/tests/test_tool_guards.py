"""Mutation-style regression tests for the local gates."""

from __future__ import annotations

import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import validate_assistant as validator  # noqa: E402
import bundle_para_auditoria as audit_bundle  # noqa: E402
import publicar_free as publisher  # noqa: E402
from project_policy import EXPECTED_SKILL_NAMES, validate_username_component  # noqa: E402


class TemporaryObject(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def object(self, name: str, module: str, notebook: str) -> Path:
        folder = self.root / ".assistant" / "hub_snippets" / "ml" / name
        folder.mkdir(parents=True)
        (folder / "__init__.py").write_text("", encoding="utf-8")
        (folder / f"{name}.py").write_text(module, encoding="utf-8")
        (folder / f"exemplo_{name}.py").write_text(notebook, encoding="utf-8")
        return folder


class ContractGuardTests(TemporaryObject):
    def test_qualified_call_is_checked(self) -> None:
        self.object(
            "sample",
            "def f(ok=1):\n    return ok\n",
            "import sample as mod\nmod.f(bad=1)\n",
        )
        problems: list[str] = []
        validator.check_contrato_de_entrada(self.root, problems)
        self.assertTrue(any("bad=" in problem for problem in problems), problems)

    def test_select_is_not_masked_by_incidental_literal(self) -> None:
        self.object(
            "sample",
            "def f():\n    raise ValueError('ghost')\n",
            "def use(df):\n    return df.select('ghost')\n",
        )
        problems: list[str] = []
        validator.check_contrato_de_dados(self.root, problems)
        self.assertTrue(any("ghost" in problem for problem in problems), problems)


class NormGuardTests(TemporaryObject):
    def run_norm(self, source: str) -> list[str]:
        self.object("sample", source, "# Databricks notebook source\n")
        problems: list[str] = []
        validator.check_normas_do_molde(self.root, problems)
        return problems

    def test_cache_in_finally_is_not_considered_protected(self) -> None:
        problems = self.run_norm(
            "def f(df: DataFrame):\n    try:\n        pass\n    finally:\n        df.cache()\n"
        )
        self.assertTrue(any("cache" in problem for problem in problems), problems)

    def test_limit_word_in_comment_does_not_protect_to_pandas(self) -> None:
        problems = self.run_norm(
            "def f(df: DataFrame):\n    # no limit is needed\n    return df.toPandas()\n"
        )
        self.assertTrue(any("toPandas" in problem for problem in problems), problems)

    def test_spark_binding_in_other_scope_does_not_mask_global(self) -> None:
        problems = self.run_norm(
            "def a():\n    spark = object()\n    return spark\n\ndef b():\n    return spark.table('x')\n"
        )
        self.assertTrue(any("global `spark`" in problem for problem in problems), problems)

    def test_unrelated_cache_method_is_not_a_dataframe_violation(self) -> None:
        problems = self.run_norm(
            "class Memo:\n    def cache(self):\n        return 1\n\ndef f(memo):\n    return memo.cache()\n"
        )
        self.assertFalse(any("cache()` fora" in problem for problem in problems), problems)


class StructuralGuardTests(unittest.TestCase):
    def test_renderer_rejects_path_traversal(self) -> None:
        for value in ("..", "..\\..\\escape", "a/b", "pessoa@example.com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_username_component(value)

    def test_frontmatter_rejects_invalid_and_empty_values(self) -> None:
        cases = (
            "---\nname: x\ndescription:\n---\n",
            "---\nname: [x\ndescription: y\n---\n",
            "---\nname: x\ndescription: y\n",
        )
        for text in cases:
            with self.subTest(text=text):
                _values, error = validator._parse_frontmatter_subset(text, Path("SKILL.md"))
                self.assertIsNotNone(error)

    def test_unexpected_skill_folder_fails_exact_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skills = root / ".assistant" / "skills"
            for name in EXPECTED_SKILL_NAMES | {"pasta-lixo"}:
                folder = skills / name
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: teste\n---\n",
                    encoding="utf-8",
                )
            problems: list[str] = []
            validator.check_skill_frontmatter(root, problems)
            self.assertTrue(any("pasta inesperada" in p for p in problems), problems)

    def test_publisher_requires_explicit_profile_and_exact_host_for_write(self) -> None:
        identity = {"userName": "usuario@example.com"}
        auth = {
            "details": {
                "configuration": {
                    "host": {"value": "https://free.example.com"},
                    "profile": {"value": "free"},
                }
            }
        }
        with mock.patch.object(publisher, "databricks_json", side_effect=[identity, auth]):
            with mock.patch.object(publisher, "CLI_PROFILE", None):
                with self.assertRaises(SystemExit):
                    publisher.resolve_home(
                        expected_host="https://free.example.com",
                        require_explicit_target=True,
                    )
        with mock.patch.object(publisher, "databricks_json", side_effect=[identity, auth]):
            with mock.patch.object(publisher, "CLI_PROFILE", "free"):
                with self.assertRaises(SystemExit):
                    publisher.resolve_home(
                        expected_host="https://outro.example.com",
                        require_explicit_target=True,
                    )

    def test_publisher_verify_rejects_unexpected_skill_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local = root / ".assistant" / "marker.txt"
            local.parent.mkdir(parents=True)
            local.write_text("ok", encoding="utf-8")

            def remote_list(path: str) -> list[dict[str, str]]:
                if path.endswith("/.assistant/skills"):
                    names = sorted(EXPECTED_SKILL_NAMES | {"skill-fantasma"})
                    return [
                        {"path": f"{path}/{name}", "object_type": "DIRECTORY"}
                        for name in names
                    ]
                if path.endswith("/.assistant"):
                    return [
                        {"path": f"{path}/{name}", "object_type": "DIRECTORY"}
                        for name in publisher.EXPECTED_HUB_DIRS
                    ]
                return []

            remote_file = {
                "path": "/Users/u/.assistant/marker.txt",
                "object_type": "FILE",
            }
            with mock.patch.object(publisher, "remote_walk", return_value=[remote_file]):
                with mock.patch.object(publisher, "remote_list", side_effect=remote_list):
                    with mock.patch.object(publisher, "databricks_json", return_value=None):
                        output = StringIO()
                        with redirect_stdout(output):
                            result = publisher.cmd_verify(root, [local], "/Users/u")
            self.assertEqual(result, 1)
            self.assertIn("skill inesperada: skill-fantasma", output.getvalue())

    def test_audit_bundle_rejects_git_failure_instead_of_empty_success(self) -> None:
        failed = mock.Mock(returncode=128, stdout="", stderr="not a repository")
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(audit_bundle, "REPO_ROOT", Path(directory)):
                with mock.patch.object(audit_bundle.subprocess, "run", return_value=failed):
                    with mock.patch.object(sys, "argv", ["bundle_para_auditoria.py"]):
                        with redirect_stdout(StringIO()):
                            self.assertEqual(audit_bundle.main(), 1)
            self.assertFalse((Path(directory) / "bundle_auditoria.txt").exists())

    def test_smoke_marker_uses_behavior_not_only_constants(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tools = root / "tools"
            tools.mkdir()
            (tools / "notebook_marker.py").write_text("# present\n", encoding="utf-8")
            (tools / "spark_smoke_test.py").write_text(
                "MARCADOR_NOTEBOOK = '# Databricks notebook source'\n"
                "_PREFIXOS_TOLERADOS = ('#!', '# -*-', '# coding', '# vim:')\n"
                "def modulo_e_notebook(module_finder, nome, ispkg):\n"
                "    return False\n",
                encoding="utf-8",
            )
            problems: list[str] = []
            with mock.patch.object(validator, "REPO_ROOT", root):
                validator.check_smoke_test_sincronizado(problems)
            self.assertTrue(any("diverge" in problem for problem in problems), problems)

    def test_prompt_field_without_four_column_guide_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".assistant" / "hub_prompts" / "demo"
            folder.mkdir(parents=True)
            (folder / "demo.md").write_text(
                "## Como preencher cada campo\n"
                "Campo {{RECURSO}} importa.\n\n"
                "## Prompt pronto para colar\n{{RECURSO}}\n\n"
                "## O que conferir na resposta\n- recurso\n\n"
                "## Limites\n- sem escrita\n",
                encoding="utf-8",
            )
            problems: list[str] = []
            validator.check_prompt_contract(root, problems)
            self.assertTrue(any("campo/como" in p for p in problems), problems)



class PublishContentGuardTests(unittest.TestCase):
    """T5 — o verify precisa provar conteúdo, não só nome e tipo."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.fonte = base / "ambiente_fonte"
        self.espelho = base / "espelho"
        for raiz in (self.fonte, self.espelho):
            (raiz / ".assistant" / "hub_snippets").mkdir(parents=True)
            (raiz / ".assistant_instructions.md").write_text("instrucoes\n", encoding="utf-8")
            (raiz / ".assistant" / "hub_snippets" / "modulo.py").write_text(
                "def f():\n    return 1\n", encoding="utf-8"
            )
            (raiz / ".assistant" / "hub_snippets" / "exemplo_modulo.py").write_text(
                "# Databricks notebook source\nprint(1)\n", encoding="utf-8"
            )
        self.arquivos = sorted(p for p in self.espelho.rglob("*") if p.is_file())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_mirror_in_sync_reports_no_problem(self) -> None:
        with mock.patch.object(publisher, "FONTE", self.fonte):
            self.assertEqual(publisher.conferir_fonte_espelho(self.espelho), [])

    def test_stale_mirror_is_rejected_before_writing(self) -> None:
        (self.espelho / ".assistant" / "hub_snippets" / "modulo.py").write_text(
            "def f():\n    return 2\n", encoding="utf-8"
        )
        with mock.patch.object(publisher, "FONTE", self.fonte):
            problemas = publisher.conferir_fonte_espelho(self.espelho)
        self.assertTrue(any("conteúdo difere" in p for p in problemas), problemas)

    def test_file_only_in_source_or_only_in_mirror_is_rejected(self) -> None:
        (self.fonte / ".assistant" / "novo.md").write_text("x\n", encoding="utf-8")
        (self.espelho / ".assistant" / "sobra.md").write_text("y\n", encoding="utf-8")
        with mock.patch.object(publisher, "FONTE", self.fonte):
            problemas = publisher.conferir_fonte_espelho(self.espelho)
        self.assertTrue(any("ausente no espelho" in p for p in problemas), problemas)
        self.assertTrue(any("não existe na fonte" in p for p in problemas), problemas)

    def test_pycache_in_source_does_not_count_as_divergence(self) -> None:
        lixo = self.fonte / ".assistant" / "hub_snippets" / "__pycache__"
        lixo.mkdir()
        (lixo / "modulo.cpython-312.pyc").write_bytes(b"\x00binario")
        with mock.patch.object(publisher, "FONTE", self.fonte):
            self.assertEqual(publisher.conferir_fonte_espelho(self.espelho), [])

    def test_remote_content_change_with_correct_name_and_type_fails(self) -> None:
        def exportar(caminho: str, notebook: bool):
            if caminho.endswith("modulo"):  # notebook, sem .py
                return b"# Databricks notebook source\nprint(1)\n", ""
            if caminho.endswith("modulo.py"):
                return b"def f():\n    return 999\n", ""   # mesmo nome, mesmo tipo
            return b"instrucoes\n", ""

        with mock.patch.object(publisher, "_exportar_remoto", side_effect=exportar):
            problemas, conferidos = publisher.comparar_conteudo(
                self.espelho, self.arquivos, "/Users/x"
            )
        self.assertEqual(conferidos, len(self.arquivos))
        self.assertTrue(any("conteúdo divergente" in p for p in problemas), problemas)

    def test_incomplete_remote_read_is_not_treated_as_valid(self) -> None:
        with mock.patch.object(
            publisher, "_exportar_remoto", return_value=(None, "RESOURCE_DOES_NOT_EXIST")
        ):
            problemas, conferidos = publisher.comparar_conteudo(
                self.espelho, self.arquivos, "/Users/x"
            )
        self.assertEqual(conferidos, 0)
        self.assertEqual(len(problemas), len(self.arquivos))
        self.assertTrue(all("leitura remota incompleta" in p for p in problemas))

    def test_documented_equivalent_representations_pass(self) -> None:
        """CRLF e quebra final de notebook são transformação da plataforma."""

        def exportar(caminho: str, notebook: bool):
            local = next(
                a for a in self.arquivos
                if caminho.endswith(a.name) or caminho.endswith(a.name[:-3])
            )
            dados = local.read_bytes().replace(b"\n", b"\r\n")
            if notebook:
                dados += b"\r\n\r\n"
            return dados, ""

        with mock.patch.object(publisher, "_exportar_remoto", side_effect=exportar):
            problemas, conferidos = publisher.comparar_conteudo(
                self.espelho, self.arquivos, "/Users/x"
            )
        self.assertEqual(problemas, [])
        self.assertEqual(conferidos, len(self.arquivos))

    def test_trailing_newline_moves_raw_hash_but_not_normalized_hash(self) -> None:
        bruto1, norm1 = publisher._hashes_do_pacote(self.espelho, self.arquivos)
        caderno = self.espelho / ".assistant" / "hub_snippets" / "exemplo_modulo.py"
        caderno.write_bytes(caderno.read_bytes() + b"\n\n")
        bruto2, norm2 = publisher._hashes_do_pacote(self.espelho, self.arquivos)
        self.assertNotEqual(bruto1, bruto2, "hash bruto deveria acompanhar os bytes")
        self.assertEqual(norm1, norm2, "hash normalizado não deveria mudar")

    def test_normalization_does_not_erase_blank_lines_or_comments(self) -> None:
        """Normalizar demais mascararia diferença real de conteúdo."""
        com_comentario = b"a = 1\n# nota\n\nb = 2\n"
        sem_comentario = b"a = 1\nb = 2\n"
        self.assertNotEqual(
            publisher._normalizar_para_comparacao(com_comentario, notebook=False),
            publisher._normalizar_para_comparacao(sem_comentario, notebook=False),
        )


if __name__ == "__main__":
    unittest.main()
