"""Contratos do corpus amplo e do recorte explícito, em repositórios sintéticos."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import bundle_para_auditoria as bundle  # noqa: E402
import task_context  # noqa: E402


class BundleCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="bundle com espaços ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "cópia limpa"
        self.root.mkdir()
        self.write("tools/bundle_para_auditoria.py", (TOOLS / "bundle_para_auditoria.py").read_bytes())
        self.write("tools/task_context.py", (TOOLS / "task_context.py").read_bytes())
        self.write("tools/project_policy.py", "from pathlib import Path\nSIMULATED_ROOT = Path('.artifacts/simulado')\n")
        self.write(".gitignore", ".artifacts/\nbundle_auditoria*.txt\n__pycache__/\n")
        self.write("AGENTS.md", "Contrato sintético\n")
        self.write("docs/input com espaço.md", "Entrada explícita\r\n")
        self.write("docs/historico/falha.md", "FAIL histórico preservado\n")
        self.write("Novo_Ambiente_Simulado/derivado.md", "Espelho legado\n")
        self.write("Ajustes_Codex/congelado.md", "Referência congelada\n")
        self.write("image.png", b"binary-image")
        self.write("invalid.dat", b"\xff\xfe")
        self.config = {
            "schema_version": 1,
            "common": [{"path": "AGENTS.md", "reason": "Contrato comum"}],
            "tasks": {"revisar": {
                "description": "Revisão sintética",
                "files": [{"path": "docs/input com espaço.md", "reason": "Objeto afetado"}],
                "exclusions": ["Histórico apenas por inclusão explícita"],
                "expand": ["Use --include PATH ou --mode canonical para expandir"],
            }},
        }
        self.write_config()
        self.git("init", "-q")
        self.commit_fixture()

    def write(self, relative: str, content: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def write_config(self) -> None:
        self.write(task_context.CONFIG, json.dumps(self.config, ensure_ascii=False))

    def git(self, *args: str) -> str:
        result = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def commit_fixture(self) -> None:
        # Commits somente neste fixture temporário; nunca no checkout sob teste.
        self.git("add", "-A")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")

    def cli(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(
            [sys.executable, "-B", str(self.root / "tools/bundle_para_auditoria.py"), *args],
            cwd=self.temp.name, capture_output=True, text=True, encoding="utf-8",
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def task(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
        return self.cli("--mode", "task", "--task", "revisar", *args, ok=ok)

    def read_manifest(self, relative: str = ".artifacts/contexto-revisar.txt") -> dict:
        return json.loads((self.root / (relative + ".manifest.json")).read_text(encoding="utf-8"))

    def test_old_default_canonical_retains_all_history(self) -> None:
        result = self.cli()
        data = (self.root / "bundle_auditoria.txt").read_bytes()
        self.assertIn(b"modo: canonical", data)
        self.assertIn(b"===== ARQUIVO: docs/historico/falha.md =====", data)
        self.assertNotIn(b"===== ARQUIVO: Novo_Ambiente_Simulado/", data)
        self.assertNotIn(b"===== ARQUIVO: Ajustes_Codex/", data)
        self.assertNotIn(b"===== ARQUIVO: image.png", data)
        self.assertNotIn(b"===== ARQUIVO: invalid.dat", data)
        self.assertIn("docs/input com espaço.md".encode(), data)
        self.assertIn("Entrada explícita\n".encode(), data)
        self.assertNotIn("Entrada explícita\r\n".encode(), data)
        self.assertNotIn("tokens estimados", result.stdout)
        self.cli()
        self.assertEqual(data, (self.root / "bundle_auditoria.txt").read_bytes())
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_security_hashes_omitted_binary_and_layers(self) -> None:
        self.cli("--mode", "security", "--saida", ".artifacts/security.txt")
        text = (self.root / ".artifacts/security.txt").read_text(encoding="utf-8")
        for path in ("image.png", "invalid.dat", "Novo_Ambiente_Simulado/derivado.md", "Ajustes_Codex/congelado.md"):
            digest = hashlib.sha256((self.root / path).read_bytes()).hexdigest()
            self.assertIn(f"{digest}  {path}", text)
            self.assertNotIn(f"===== ARQUIVO: {path} =====", text)

    def test_old_full_and_alias_override_remain_equivalent(self) -> None:
        self.cli("--mode", "full", "--saida", ".artifacts/full.txt")
        self.cli("--mode", "security", "--incluir-espelho", "--saida", ".artifacts/alias.txt")
        full = (self.root / ".artifacts/full.txt").read_bytes()
        self.assertEqual(full, (self.root / ".artifacts/alias.txt").read_bytes())
        self.assertIn(b"===== ARQUIVO: Novo_Ambiente_Simulado/derivado.md =====", full)
        self.assertIn(b"===== ARQUIVO: Ajustes_Codex/congelado.md =====", full)
        self.assertNotIn(b"===== ARQUIVO: image.png =====", full)

    def test_task_exact_selection_hashes_metrics_and_exclusions(self) -> None:
        result = self.task()
        manifest = self.read_manifest()
        data = (self.root / ".artifacts/contexto-revisar.txt").read_bytes()
        self.assertIn(b"NAO E AUDITORIA INTEGRAL", data)
        self.assertIn("Entrada explícita\r\n".encode(), data)
        self.assertEqual(manifest["git_commit"], self.git("rev-parse", "HEAD").strip())
        self.assertFalse(manifest["worktree_dirty"])
        self.assertFalse(manifest["allow_dirty"])
        self.assertEqual(manifest["dirty_entries"], [])
        self.assertEqual(manifest["kind"], "task-context-not-full-audit")
        self.assertEqual({item["path"] for item in manifest["included"]}, {"AGENTS.md", "docs/input com espaço.md"})
        for item in manifest["included"]:
            original = (self.root / item["path"]).read_bytes()
            self.assertEqual(item["bytes"], len(original))
            self.assertEqual(item["sha256"], hashlib.sha256(original).hexdigest())
            self.assertTrue(item["reasons"])
        self.assertEqual(manifest["metrics"]["included_files"], 2)
        self.assertEqual(manifest["metrics"]["included_content_bytes"], sum(item["bytes"] for item in manifest["included"]))
        self.assertEqual(manifest["bundle"]["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest["bundle"]["bytes"], len(data))
        config_bytes = (self.root / task_context.CONFIG).read_bytes()
        self.assertEqual(manifest["route_config"]["sha256"], hashlib.sha256(config_bytes).hexdigest())
        self.assertIn("docs/historico/falha.md", {item["path"] for item in manifest["excluded"]})
        self.assertTrue(all(item["reason"] for item in manifest["excluded"]))
        self.assertTrue(manifest["exclusion_notes"])
        self.assertTrue(manifest["expand"])
        self.assertIn("2 arquivos", result.stdout)
        self.assertIn("bytes de conteúdo", result.stdout)

    def test_explicit_history_expansion_is_not_silent_global_ignore(self) -> None:
        self.task("--include", "docs/historico/falha.md")
        item = next(row for row in self.read_manifest()["included"] if row["path"] == "docs/historico/falha.md")
        self.assertIn("--include", item["reasons"][0])

    def test_dirty_requires_opt_in_and_untracked_provenance_is_precise(self) -> None:
        self.write("AGENTS.md", "Alterado\n")
        self.write("novo com espaço.md", "Novo sintético\n")
        self.write(".artifacts/simulado/ignored.md", "Ignorado\n")
        self.task(ok=False)
        self.assertFalse((self.root / ".artifacts/contexto-revisar.txt").exists())
        self.task("--allow-dirty", "--include", "novo com espaço.md")
        manifest = self.read_manifest()
        self.assertTrue(manifest["worktree_dirty"])
        statuses = {item["path"]: item["status"] for item in manifest["dirty_entries"]}
        self.assertEqual(statuses["AGENTS.md"], " M")
        self.assertEqual(statuses["novo com espaço.md"], "??")
        new = next(row for row in manifest["included"] if row["path"] == "novo com espaço.md")
        self.assertFalse(new["tracked"])
        self.assertNotIn(".artifacts/simulado/ignored.md", statuses)
        self.assertNotIn(".artifacts/simulado/ignored.md", {row["path"] for row in manifest["excluded"]})

    def test_dirty_rename_records_both_paths(self) -> None:
        self.git("mv", "docs/historico/falha.md", "docs/historico/falha renomeada.md")
        self.task("--allow-dirty")
        renamed = next(row for row in self.read_manifest()["dirty_entries"] if "R" in row["status"])
        self.assertEqual(renamed["path"], "docs/historico/falha renomeada.md")
        self.assertEqual(renamed["original_path"], "docs/historico/falha.md")

    def test_task_and_old_modes_do_not_ingest_their_own_output(self) -> None:
        self.task("--saida", "saída com espaço.txt", "--allow-dirty")
        self.task("--saida", "saída com espaço.txt", "--allow-dirty")
        manifest = self.read_manifest("saída com espaço.txt")
        self.assertEqual(manifest["metrics"]["included_files"], 2)
        omitted = {row["path"]: row["reason"] for row in manifest["excluded"]}
        self.assertIn("próprio comando", omitted["saída com espaço.txt"])
        self.assertIn("próprio comando", omitted["saída com espaço.txt.manifest.json"])
        for mode in ("canonical", "security", "full"):
            relative = f"{mode} saída.txt"
            self.cli("--mode", mode, "--allow-dirty", "--saida", relative)
            self.cli("--mode", mode, "--allow-dirty", "--saida", relative)
            self.assertNotIn(f"===== ARQUIVO: {relative} =====", (self.root / relative).read_text(encoding="utf-8"))

    def test_explicit_self_output_is_rejected(self) -> None:
        self.task("--saida", "review.txt")
        result = self.task("--allow-dirty", "--saida", "review.txt", "--include", "review.txt", ok=False)
        self.assertIn("própria saída", result.stdout)

    def test_invalid_task_or_mode_combination(self) -> None:
        for args in (("--mode", "task"), ("--mode", "task", "--task", "../escape"),
                     ("--task", "revisar"), ("--include", "AGENTS.md"),
                     ("--mode", "task", "--task", "revisar", "--incluir-espelho"),
                     ("--mode", "unknown")):
            with self.subTest(args=args):
                self.cli(*args, ok=False)

    def test_invalid_or_nontext_additional_paths_fail_closed(self) -> None:
        for path in ("../outside.md", "/tmp/outside.md", "docs/../AGENTS.md", "./AGENTS.md",
                     "docs\\input.md", "C:/outside.md", ".git/config", "docs/*.md", "docs/",
                     "missing.md", "docs", "image.png", "invalid.dat", "Novo_Ambiente_Simulado/derivado.md"):
            with self.subTest(path=path):
                self.task("--include", path, ok=False)
        self.write(".artifacts/ignored.md", "Ignorado")
        self.task("--allow-dirty", "--include", ".artifacts/ignored.md", ok=False)

    def test_invalid_empty_duplicate_or_broad_route_is_rejected(self) -> None:
        base = json.loads(json.dumps(self.config))
        mutations = [[], [{"path": "docs/", "reason": "Amplo"}],
                     [{"path": "docs/*.md", "reason": "Glob"}],
                     [{"path": "AGENTS.md", "reason": ""}],
                     [{"path": "AGENTS.md", "reason": "A"}] * 2]
        for files in mutations:
            with self.subTest(files=files):
                self.config = json.loads(json.dumps(base))
                self.config["tasks"]["revisar"]["files"] = files
                self.write_config()
                self.task("--allow-dirty", ok=False)
        self.write(task_context.CONFIG, "{broken")
        self.task("--allow-dirty", ok=False)

    def test_missing_or_deleted_route_file_is_not_silent_reduction(self) -> None:
        (self.root / "docs/input com espaço.md").unlink()
        self.task("--allow-dirty", ok=False)
        self.cli("--allow-dirty", "--saida", ".artifacts/deleted-canonical.txt")

    def test_output_cannot_overwrite_source_or_escape_relative_root(self) -> None:
        original = (self.root / "AGENTS.md").read_bytes()
        for path in ("AGENTS.md", ".git/config", "../escape.txt"):
            with self.subTest(path=path):
                self.task("--saida", path, ok=False)
        self.assertEqual(original, (self.root / "AGENTS.md").read_bytes())
        self.task("--saida", str(Path(self.temp.name) / "externo com espaço.txt"))
        self.assertTrue((Path(self.temp.name) / "externo com espaço.txt.manifest.json").is_file())

    def test_symlink_inputs_and_output_ancestors_are_rejected(self) -> None:
        target = Path(self.temp.name) / "outside.md"
        target.write_text("Fora da raiz", encoding="utf-8")
        try:
            (self.root / "escape.md").symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink indisponível nesta plataforma: {exc}")
        self.task("--allow-dirty", "--include", "escape.md", ok=False)
        for mode in ("canonical", "security", "full"):
            self.cli("--mode", mode, "--allow-dirty", ok=False)
        (self.root / "escape.md").unlink()
        (self.root / "linked-dir").symlink_to(Path(self.temp.name), target_is_directory=True)
        self.task("--allow-dirty", "--saida", "linked-dir/output.txt", ok=False)
        self.assertFalse((Path(self.temp.name) / "output.txt").exists())

    def test_current_generated_mirror_is_excluded_even_if_tracked(self) -> None:
        self.write(".artifacts/simulado/generated.md", "Gerado")
        self.git("add", "-f", ".artifacts/simulado/generated.md")
        self.commit_fixture()
        self.cli("--saida", ".artifacts/canonical.txt")
        self.assertNotIn("===== ARQUIVO: .artifacts/simulado/generated.md", (self.root / ".artifacts/canonical.txt").read_text())
        self.task("--include", ".artifacts/simulado/generated.md", ok=False)
        self.cli("--mode", "full", "--saida", ".artifacts/full.txt")
        self.assertIn("===== ARQUIVO: .artifacts/simulado/generated.md", (self.root / ".artifacts/full.txt").read_text())

    def test_clean_clone_retains_cli_and_route_behavior(self) -> None:
        clone = Path(self.temp.name) / "clone com espaços"
        result = subprocess.run(["git", "clone", "-q", str(self.root), str(clone)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.root = clone
        self.task()
        self.cli("--mode", "security", "--saida", ".artifacts/security.txt")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_module_cli_and_import_in_fresh_processes(self) -> None:
        for args in (
            ["-m", "tools.bundle_para_auditoria", "--mode", "task", "--task", "revisar"],
            ["-m", "tools.bundle_para_auditoria", "--mode", "full", "--saida", ".artifacts/module.txt"],
            ["-c", "import tools.bundle_para_auditoria as bundle; assert callable(bundle.main)"],
        ):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "-B", *args], cwd=self.root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")


class BundleCoreTests(unittest.TestCase):
    def test_binary_only_inventory_rejects_empty_body(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "only.png").write_bytes(b"image")
            with mock.patch.object(bundle, "REPO_ROOT", root), mock.patch.object(
                bundle, "_git", side_effect=["", "only.png\0", "a" * 40]
            ), redirect_stdout(StringIO()) as output:
                self.assertEqual(bundle.main([]), 1)
            self.assertIn("seleção textual vazia", output.getvalue())
            self.assertFalse((root / "bundle_auditoria.txt").exists())

    def test_git_failure_does_not_create_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with mock.patch.object(bundle, "REPO_ROOT", root), mock.patch.object(
                bundle.subprocess, "run", return_value=mock.Mock(returncode=128, stdout="", stderr="not a repository")
            ), redirect_stdout(StringIO()) as output:
                self.assertEqual(bundle.main([]), 1)
            self.assertIn("FAIL git status", output.getvalue())
            self.assertFalse((root / "bundle_auditoria.txt").exists())

    def test_real_reviewed_routes_are_bounded_and_resolve(self) -> None:
        root = TOOLS.parent
        config, _data = task_context.load_routes(root)
        self.assertEqual(set(config["tasks"]), {"alterar-objeto", "preparar-entrega", "instrucoes-ia", "investigar-regressao"})
        for name in config["tasks"]:
            selected, _task = task_context.select_task(config, name, [])
            self.assertLessEqual(len(selected), 2 * task_context.MAX_ROUTE_FILES)
            for path in selected:
                self.assertTrue(task_context.safe_path(root, path).is_file(), (name, path))


if __name__ == "__main__":
    unittest.main()
