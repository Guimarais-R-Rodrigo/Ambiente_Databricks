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
from project_policy import (  # noqa: E402
    EXPECTED_SKILL_NAMES,
    PERSONAL_RE,
    validate_username_component,
)


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
    def test_personal_identifier_token_has_alphanumeric_boundaries(self) -> None:
        token = "c" + "123456"
        positives = (
            token,
            f"{token}@example.com",
            f"usuario+{token}@example.com",
            f"/Users/{token}/projeto",
            f"C:\\prefixo\\{token}\\projeto",
            f"prefixo:{token}",
        )
        for text in positives:
            with self.subTest(text=text):
                self.assertIsNotNone(PERSONAL_RE.search(text))

        hashes_or_larger_tokens = (
            "a" * 20 + token + "b" * 37,
            token + "a" * 57,
            "a" * 57 + token,
            "x" + token,
            token + "7",
        )
        for text in hashes_or_larger_tokens:
            with self.subTest(text=text):
                self.assertIsNone(PERSONAL_RE.search(text))

        legacy_patterns = (
            "corp" + ".caixa",
            "caixa" + ".gov" + ".br",
            "guimarais" + ".r.rodrigo@",
            "C:\\Users\\" + "Rodrigo",
            "/Users/" + "rodri",
        )
        for text in legacy_patterns:
            with self.subTest(text=text):
                self.assertIsNotNone(PERSONAL_RE.search(text))

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
        # write_bytes, e não write_text: no Windows o modo texto traduz \\n para
        # \\r\\n, e o teste passaria a medir a tradução do sistema operacional em
        # vez do contrato da comparação.
        for raiz in (self.fonte, self.espelho):
            (raiz / ".assistant" / "hub_snippets").mkdir(parents=True)
            (raiz / ".assistant_instructions.md").write_bytes(b"instrucoes\n")
            (raiz / ".assistant" / "hub_snippets" / "modulo.py").write_bytes(
                b"def f():\n    return 1\n"
            )
            (raiz / ".assistant" / "hub_snippets" / "exemplo_modulo.py").write_bytes(
                b"# Databricks notebook source\nprint(1)\n"
            )
        self.arquivos = sorted(p for p in self.espelho.rglob("*") if p.is_file())

    def _mapa_remoto(self, home: str = "/Users/x") -> dict:
        """Caminho remoto -> arquivo local, montado como o publicador monta.

        Casar por ``endswith`` dependia da ordem de iteração e do separador de
        path do sistema: '.../exemplo_modulo' termina em 'modulo'.
        """
        mapa = {}
        for arquivo in self.arquivos:
            relativo = str(arquivo.relative_to(self.espelho)).replace("\\", "/")
            if publisher.eh_notebook(arquivo):
                mapa[f"{home}/{relativo[:-3]}"] = arquivo
            else:
                mapa[f"{home}/{relativo}"] = arquivo
        return mapa

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

        mapa = self._mapa_remoto()

        def exportar(caminho: str, notebook: bool):
            local = mapa[caminho]
            # Normaliza para LF antes de simular o CRLF do remoto: sem isso, um
            # arquivo já em CRLF no disco viraria \\r\\r\\n e o teste mediria o
            # próprio defeito em vez do contrato.
            dados = local.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
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


class ReviewRegressionTests(unittest.TestCase):
    def test_ignored_mirror_extra_blocks_upload_before_any_call(self):
        with tempfile.TemporaryDirectory() as td:
            source, mirror = Path(td) / "source", Path(td) / "mirror"
            for root in (source, mirror):
                (root / ".assistant").mkdir(parents=True)
                (root / ".assistant_instructions.md").write_bytes(b"instructions")
            (mirror / ".assistant" / "__pycache__").mkdir()
            extra = mirror / ".assistant" / "__pycache__" / "extra.pyc"
            extra.write_bytes(b"not-product")
            files = [p for p in mirror.rglob("*") if p.is_file()]
            with mock.patch.object(publisher, "FONTE", source), mock.patch.object(publisher, "databricks") as cli:
                with redirect_stdout(StringIO()):
                    code = publisher.cmd_plan(mirror, files, "/Users/test", True)
                self.assertEqual(code, 1)
                cli.assert_not_called()

    def test_export_protocol_errors_and_empty_file(self):
        import json
        cases = [(1, "", "denied"), (0, "not-json", ""),
                 (0, "{}", ""), (0, json.dumps({"content": "%%%"}), "")]
        for result in cases:
            with self.subTest(result=result), mock.patch.object(publisher, "databricks", return_value=result):
                data, error = publisher._exportar_remoto("/Users/test/a", False)
                self.assertIsNone(data)
                self.assertTrue(error)
        with mock.patch.object(publisher, "databricks", return_value=(0, '{"content":""}', "")):
            self.assertEqual(publisher._exportar_remoto("/Users/test/a", False), (b"", ""))

    def test_git_status_failure_is_not_clean_provenance(self):
        ok = mock.Mock(returncode=0, stdout="a" * 40 + "\n")
        fail = mock.Mock(returncode=128, stdout="")
        with mock.patch.object(publisher.subprocess, "run", side_effect=[ok, fail]):
            with self.assertRaisesRegex(ValueError, "Git falhou"):
                publisher._commit_atual()

    def test_git_provenance_is_scoped_to_the_published_product(self):
        head = mock.Mock(returncode=0, stdout="a" * 40 + "\n")
        clean = mock.Mock(returncode=0, stdout="")
        with mock.patch.object(publisher.subprocess, "run", side_effect=[head, clean]) as run:
            self.assertEqual(publisher._commit_atual(), "a" * 40)
        status_command = run.call_args_list[1].args[0]
        separator = status_command.index("--")
        scopes = set(status_command[separator + 1 :])
        self.assertEqual(
            scopes,
            {
                str(publisher.FONTE.relative_to(publisher.REPO_ROOT)),
                str(
                    publisher.SIMULADO.relative_to(publisher.REPO_ROOT)
                    / "Users"
                    / "usuario-free"
                ),
            },
        )

    def test_verify_persists_full_hashes_and_scope(self):
        import json
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "mirror"
            f = root / ".assistant" / "a.py"
            f.parent.mkdir(parents=True)
            f.write_bytes(b"x=1\n")
            target = Path(td) / "evidence.json"
            home = "/Users/test"
            def list_remote(path):
                names = EXPECTED_SKILL_NAMES if path.endswith("/skills") else publisher.EXPECTED_HUB_DIRS
                return [{"path": path + "/" + n, "object_type": "DIRECTORY"} for n in names]
            with mock.patch.object(publisher, "remote_walk", return_value=[{"path": home + "/.assistant/a.py", "object_type": "FILE"}]), mock.patch.object(publisher, "remote_list", side_effect=list_remote), mock.patch.object(publisher, "databricks_json", return_value=None), mock.patch.object(publisher, "conferir_fonte_espelho", return_value=[]), mock.patch.object(publisher, "_exportar_remoto", return_value=(f.read_bytes(), "")), mock.patch.object(publisher, "_commit_atual", return_value="a" * 40):
                with redirect_stdout(StringIO()):
                    code = publisher.cmd_verify(root, [f], home, conteudo=True, relatorio=target)
            self.assertEqual(code, 0)
            evidence = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(evidence["status"], "PASS")
            self.assertEqual(evidence["source_commit"], "a" * 40)
            self.assertEqual(len(evidence["package_raw_sha256"]), 64)
            self.assertEqual(evidence["files_compared"], 1)
            self.assertEqual(evidence["files"][0]["path"], ".assistant/a.py")

    def _load_function(self, path, name, namespace=None):
        import ast
        tree = ast.parse(path.read_text(encoding="utf-8"))
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
        ns = namespace or {}
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), "exec"), ns)
        return ns[name]

    def test_pit_multiset_rejects_loss_outside_c1_and_date_change(self):
        from datetime import date
        check = self._load_function(TOOLS / "spark_smoke_test.py", "_conferir_linhas_pit")
        d = date(2026, 3, 10)
        rows = [("C1", d, 20), ("C1", d, 20), ("C2", d, None),
                ("C3", d, None), (None, d, None), ("C4", None, None)]
        check(list(reversed(rows)))
        for i in range(len(rows)):
            mutant = rows.copy()
            mutant[i] = ("wrong", d, None)
            with self.subTest(i=i), self.assertRaises(AssertionError):
                check(mutant)
        mutant = rows.copy()
        mutant[2] = rows[3]
        with self.assertRaises(AssertionError):
            check(mutant)
        mutant = rows.copy()
        mutant[2] = ("C2", date(2026, 3, 11), None)
        with self.assertRaises(AssertionError):
            check(mutant)

    def test_csi_invalid_limit_fails_before_spark_access(self):
        from numbers import Integral
        from typing import Dict, List
        path = TOOLS.parent / "ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/psi_calculator.py"
        ns = {"Integral": Integral, "DataFrame": object, "List": List, "Dict": Dict,
              "LIMITE_CATEGORIAS_CSI": 1000}
        check = self._load_function(path, "_validar_max_categorias", ns)
        public = self._load_function(path, "calcular_csi", ns)
        for value in (float("nan"), float("inf"), True, 0, -1, 1.5, "100"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "inteiro positivo"):
                public(None, None, ["x"], max_categorias=value)
        check(1)
        check(1000)


class RepoInventoryTests(unittest.TestCase):
    def test_node_modules_is_ignored_only_when_it_is_an_extra(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(["git", "init", "-q", td], check=True)
            (root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")

            tracked = root / "vendor" / "node_modules" / "tracked.md"
            tracked.parent.mkdir(parents=True)
            tracked.write_text("identificador " + "c" + "123456", encoding="utf-8")
            subprocess.run(["git", "add", ".gitignore"], cwd=root, check=True)
            subprocess.run(
                ["git", "add", "-f", tracked.relative_to(root).as_posix()],
                cwd=root,
                check=True,
            )

            ignored = root / "node_modules" / "ignored.md"
            ignored.parent.mkdir()
            ignored.write_text("[bad](missing.md)", encoding="utf-8")
            (root / "guide.md").write_text("ok", encoding="utf-8")

            with mock.patch.object(validator, "REPO_ROOT", root):
                extra_problems: list[str] = []
                self.assertEqual(validator.check_worktree_hygiene(extra_problems), 1)
                self.assertEqual(extra_problems, [])

                tracked_problems: list[str] = []
                self.assertGreater(validator.check_repo_corporate(tracked_problems), 0)
                self.assertTrue(
                    any("tracked.md" in problem for problem in tracked_problems),
                    tracked_problems,
                )

    def test_ignored_guide_does_not_change_versioned_count_but_is_checked(self):
        import subprocess
        import repo_inventory
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(["git", "init", "-q", td], check=True)
            (root / ".gitignore").write_text("guide.md\n", encoding="utf-8")
            (root / "README.md").write_text("hello", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            before = repo_inventory.git_paths(root)
            (root / "guide.md").write_text("[bad](missing.md)", encoding="utf-8")
            self.assertEqual(before, repo_inventory.git_paths(root))
            with mock.patch.object(validator, "REPO_ROOT", root):
                problems = []
                self.assertEqual(validator.check_worktree_hygiene(problems), 1)
                self.assertTrue(any("link quebrado" in p for p in problems))

    def test_git_failure_and_empty_output_are_not_certified(self):
        import repo_inventory
        for rc, output in ((128, b""), (0, b"")):
            with mock.patch.object(repo_inventory.subprocess, "run", return_value=mock.Mock(returncode=rc, stdout=output)):
                with self.assertRaises(ValueError):
                    repo_inventory.git_paths(Path.cwd())

    def test_readme_local_check_never_invokes_remote_cli(self):
        import subprocess
        calls = []
        def run(cmd, **kwargs):
            calls.append(cmd)
            return mock.Mock(returncode=0, stdout="")
        with mock.patch.object(subprocess, "run", side_effect=run):
            validator.check_saida_de_comando_no_readme([])
        self.assertEqual(len(calls), 1)
        self.assertIn("validate_assistant.py", calls[0][1])


class ManualTecnicoTests(unittest.TestCase):
    """Guarda a redação unificada sem alterar regras analíticas do produto."""

    @classmethod
    def setUpClass(cls):
        cls.repo = TOOLS.parent
        cls.source = cls.repo / "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
        cls.text = cls.source.read_text(encoding="utf-8")

    def test_manual_copies_are_identical(self):
        from project_policy import SAFE_SIMULATED_USERNAME
        derived = self.repo / ".artifacts/simulado/Users" / SAFE_SIMULATED_USERNAME / ".assistant/MANUAL_TECNICO.md"
        self.assertEqual(self.source.read_bytes(), (self.repo / "MANUAL_TECNICO.md").read_bytes())
        self.assertEqual(self.source.read_bytes(), derived.read_bytes())
        for root in (self.source.parent, derived.parent):
            self.assertFalse((root / "CATALOGO_HELPERS.md").exists())
            self.assertFalse((root / "GLOSSARIO.md").exists())

    def test_manual_inventory_covers_current_objects(self):
        base = self.source.parent
        for collection in ("hub_snippets", "hub_scripts"):
            for module in (base / collection).rglob("*.py"):
                if module.stem != module.parent.name:
                    continue
                dotted = ".".join(module.parent.relative_to(base).parts)
                self.assertIn(f"#### `{dotted}`", self.text, dotted)

    def test_manual_python_blocks_and_internal_links(self):
        import ast
        import re
        anchors = set(re.findall(r'<a id="([^"]+)"', self.text))
        self.assertGreaterEqual(len(anchors), 31)
        for target in re.findall(r'\]\(#([^\s)]+)\)', self.text):
            self.assertIn(target, anchors)
        for number, code in enumerate(re.findall(r'```python\n(.*?)```', self.text, re.S), 1):
            ast.parse(code, filename=f"MANUAL_TECNICO.md:bloco-{number}")

    def test_manual_portable_examples_as_written(self):
        import re
        labels = {"funcao_didatica", "introspeccao", "split_temporal", "metricas_binarias"}
        found = set()
        blocks = re.findall(r'```python\n(.*?)```', self.text, re.S)
        with mock.patch.object(sys, "path", [str(self.source.parent)] + sys.path):
            for code in blocks:
                tag = re.search(r"^# EXEMPLO: (\w+)$", code, re.M)
                if tag and tag[1] in labels:
                    with self.subTest(example=tag[1]), redirect_stdout(StringIO()):
                        exec(compile(code, f"MANUAL_TECNICO.md:{tag[1]}", "exec"), {})
                    found.add(tag[1])
        self.assertEqual(found, labels)

if __name__ == "__main__":
    unittest.main()
