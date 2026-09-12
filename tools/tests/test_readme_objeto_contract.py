"""Regressões adversariais: estrutura não é pedagogia e dispensa não pode crescer."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import readme_objeto_contract as rc

REAL = Path(__file__).resolve().parents[2]
TEXT = (REAL / "ambiente_fonte/.assistant" / rc.TEMPLATE).read_text(encoding="utf-8")
VERSION, HEADINGS = rc.template_contract(TEXT)


class ReadmeContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.root = self.repo / "ambiente_fonte"
        self.base = self.root / ".assistant"
        template = self.base / rc.TEMPLATE
        template.parent.mkdir(parents=True)
        template.write_text(TEXT, encoding="utf-8")
        self.spec = self.make_object("hub_snippets/ml/recurso", "snippet")

    def tearDown(self):
        self.temp.cleanup()

    def make_object(self, name, kind, exemplar=False):
        spec = rc.ObjectSpec(Path(name), kind, exemplar)
        folder = self.base / spec.path
        folder.mkdir(parents=True, exist_ok=True)
        for file in [spec.main, spec.example, "__init__.py"]:
            (folder / file).write_text("# Exemplo sintético de teste.\n", encoding="utf-8")
        return spec

    def readme(self, spec=None, transform=lambda text: text):
        spec = spec or self.spec
        folder = self.base / spec.path
        intro = (f"# `{spec.path.name}` — recurso de teste\n\n"
                 f"<!-- readme-objeto: {VERSION} -->\n\n## Visão rápida\n"
                 "Este objeto ilustra o contrato de teste, sem executar dados.\n\n")
        body = "\n\n".join(h + "\n\nExplicação específica de teste." for h in HEADINGS)
        links = (f"\n\n[Implementação]({spec.main}). [Exemplo]({spec.example}). "
                 "[API](__init__.py).\n")
        text = transform(intro + body + links)
        (folder / "README.md").write_text(text, encoding="utf-8")
        return text

    def errors(self, spec=None):
        return rc.validate_readme(self.base, spec or self.spec, VERSION, HEADINGS)

    def control(self, pending=None, phase="migration"):
        data = {"schema_version": 1, "base_commit": "a" * 40,
                "template_version": VERSION, "phase": phase,
                "pending": {p: {"sprint": "R02", "lote": "A"} for p in (pending or [])}}
        path = self.repo / rc.CONTROL
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(text, encoding="utf-8")
        return text

    def coverage(self, pending=None, previous=None):
        self.control(pending)
        errors = []
        counts = rc.check_readme_objects(self.root, errors, repo=self.repo,
                                        previous=previous if previous is not None else set(pending or []))
        return counts, errors

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def init_git(self):
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.commit("base")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)

    def test_unknown_category_is_not_silently_ignored(self):
        self.make_object("hub_snippets/new_category/new", "snippet")
        with self.assertRaisesRegex(ValueError, "categoria"):
            rc.discover(self.base)

    def test_waived_symlink_is_not_silently_accepted(self):
        target = self.repo / "outside"; target.mkdir()
        (self.base / "hub_snippets/ml/link").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "simbólico"):
            rc.discover(self.base)

    def test_short_document_has_no_word_quota(self):
        self.readme(); self.assertEqual([], self.errors())

    def test_missing_readme(self):
        self.assertTrue(any("ausente" in e for e in self.errors()))

    def test_wrong_order(self):
        self.readme(transform=lambda s: s.replace(HEADINGS[0], "@swap@").replace(HEADINGS[1], HEADINGS[0]).replace("@swap@", HEADINGS[1]))
        self.assertTrue(any("ordem" in e for e in self.errors()))

    def test_missing_section(self):
        self.readme(transform=lambda s: s.replace(HEADINGS[2], "### contexto"))
        self.assertTrue(self.errors())

    def test_duplicate_heading(self):
        self.readme(transform=lambda s: s + "\n" + HEADINGS[0] + "\nTexto.")
        self.assertTrue(self.errors())

    def test_fenced_headings_do_not_count(self):
        self.readme(transform=lambda s: s.replace(HEADINGS[0], "```text\n"+HEADINGS[0]+"\n```"))
        self.assertTrue(self.errors())

    def test_comment_headings_do_not_count(self):
        self.readme(transform=lambda s: s.replace(HEADINGS[0], "<!-- " + HEADINGS[0] + " -->"))
        self.assertTrue(self.errors())

    def test_empty_section(self):
        self.readme(transform=lambda s: s.replace("Explicação específica de teste.", "", 1))
        self.assertTrue(any("sem explicação" in e for e in self.errors()))

    def test_code_only_section(self):
        self.readme(transform=lambda s: s.replace("Explicação específica de teste.", "```python\nprint(1)\n```", 1))
        self.assertTrue(any("sem explicação" in e for e in self.errors()))

    def test_missing_version(self):
        self.readme(transform=lambda s: s.replace(f"<!-- readme-objeto: {VERSION} -->", ""))
        self.assertTrue(self.errors())

    def test_wrong_version(self):
        self.readme(transform=lambda s: s.replace(VERSION, "2.0.0"))
        self.assertTrue(self.errors())

    def test_missing_quick_view(self):
        self.readme(transform=lambda s: s.replace("## Visão rápida", "## Outro título"))
        self.assertTrue(self.errors())

    def test_missing_api_link(self):
        self.readme(transform=lambda s: s.replace("[API](__init__.py)", "API"))
        self.assertTrue(any("falta link" in e for e in self.errors()))

    def test_link_inside_code_not_real_link(self):
        self.readme(transform=lambda s: s.replace("[API](__init__.py)", "`[API](__init__.py)`"))
        self.assertTrue(any("falta link" in e for e in self.errors()))

    def test_broken_link(self):
        self.readme(transform=lambda s: s + "\n[Ghost](inexistente.md)")
        self.assertTrue(any("quebrado" in e for e in self.errors()))

    def test_broken_anchor(self):
        self.readme(transform=lambda s: s + "\n[Ghost](README.md#inexistente)")
        self.assertTrue(any("âncora" in e for e in self.errors()))

    def test_existing_anchor(self):
        self.readme(transform=lambda s: s + "\n[Visão](README.md#visão-rápida)")
        self.assertEqual([], self.errors())

    def test_escape_product_tree(self):
        self.readme(transform=lambda s: s + "\n[Outside](../../../../../../outside.md)")
        self.assertTrue(any("sai do produto" in e for e in self.errors()))

    def test_symlink_readme_rejected(self):
        path = self.base / self.spec.path / "README.md"
        target = self.repo / "real.md"; target.write_text("texto")
        path.symlink_to(target)
        self.assertTrue(any("simbólico" in e for e in self.errors()))

    def test_editor_placeholder_rejected(self):
        self.readme(transform=lambda s: s + "\nPREENCHER_AQUI")
        self.assertTrue(self.errors())

    def test_prompt_placeholder_is_legitimate(self):
        spec = self.make_object("hub_prompts/campanha", "prompt")
        self.readme(spec, transform=lambda s: s + "\nO campo `{{TABELA}}` identifica o recurso real.")
        self.assertEqual([], self.errors(spec))

    def test_script_and_exemplar(self):
        for name, kind, exemplar in [("hub_scripts/check", "script", False),
                                     ("hub_padroes/prompt/demo", "prompt", True)]:
            spec = self.make_object(name, kind, exemplar)
            self.readme(spec)
            self.assertEqual([], self.errors(spec))
        self.assertEqual(3, len(rc.discover(self.base)))

    def test_legitimate_pending_legacy(self):
        counts, errors = self.coverage([self.spec.path.as_posix()])
        self.assertEqual([], errors); self.assertEqual(1, counts["pending"])

    def test_new_object_without_readme(self):
        _, errors = self.coverage()
        self.assertTrue(any("obrigatório ausente" in e for e in errors))

    def test_delivered_must_retire_waiver(self):
        self.readme()
        _, errors = self.coverage([self.spec.path.as_posix()])
        self.assertTrue(any("ainda está dispensado" in e for e in errors))

    def test_new_waiver_rejected(self):
        _, errors = self.coverage([self.spec.path.as_posix()], previous=set())
        self.assertTrue(any("dispensa nova" in e for e in errors))

    def test_ghost_waiver_rejected(self):
        _, errors = self.coverage(["hub_scripts/ghost"])
        self.assertTrue(any("sem objeto" in e for e in errors))

    def test_complete_with_pending_rejected(self):
        with self.assertRaises(ValueError):
            rc.read_control(self.control([self.spec.path.as_posix()], "complete"))

    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError):
            rc.read_control('{"schema_version": 1, "schema_version": 1}')

    def test_control_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            rc.read_control(self.control(["../outside"]))

    def test_template_order_is_validated(self):
        with self.assertRaises(ValueError):
            rc.template_contract(TEXT.replace("## 1. O que é?", "## 16. Outro"))

    def test_git_bootstrap_only_preexisting(self):
        self.init_git()
        new = self.make_object("hub_scripts/new", "script")
        current = self.control([new.path.as_posix()])
        allowed = rc.prior_pending(self.repo, current)
        self.assertIn(self.spec.path.as_posix(), allowed)
        self.assertNotIn(new.path.as_posix(), allowed)

    def test_git_reintroduced_waiver_in_worktree(self):
        self.init_git()
        self.control([self.spec.path.as_posix()]); self.commit("introducao")
        self.readme(); self.control([]); self.commit("entrega")
        current = self.control([self.spec.path.as_posix()])
        self.assertEqual(set(), rc.prior_pending(self.repo, current))

    def test_git_reintroduced_waiver_in_commit(self):
        self.init_git()
        self.control([self.spec.path.as_posix()]); self.commit("introducao")
        self.readme(); self.control([]); self.commit("entrega")
        current = self.control([self.spec.path.as_posix()]); self.commit("regressao")
        self.assertEqual(set(), rc.prior_pending(self.repo, current))

    def test_committed_bootstrap(self):
        self.init_git()
        current = self.control([self.spec.path.as_posix()]); self.commit("introducao")
        self.assertEqual({self.spec.path.as_posix()}, rc.prior_pending(self.repo, current))

    def test_history_unavailable_fails_closed(self):
        self.control([self.spec.path.as_posix()])
        errors = []; rc.check_readme_objects(self.root, errors, repo=self.repo)
        self.assertTrue(any("histórico Git indisponível" in e for e in errors))

    def test_shallow_history_fails_closed(self):
        self.init_git()
        (self.repo / ".git/shallow").write_text(self.git("rev-parse", "HEAD") + "\n")
        with self.assertRaisesRegex(ValueError, "raso"):
            rc.prior_pending(self.repo, self.control([self.spec.path.as_posix()]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
