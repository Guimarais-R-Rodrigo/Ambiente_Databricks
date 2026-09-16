from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V14_DIR = ROOT / "docs" / "sprints" / "sistema_temas" / "V14"
PLAN = V14_DIR / "PLANO_MESTRE.md"
README_V14 = V14_DIR / "README.md"
CHECKPOINT = V14_DIR / "CHECKPOINT_S0.md"
ROOT_README = ROOT / "README.md"
SPRINTS_README = ROOT / "docs" / "sprints" / "README.md"
TEMAS_README = ROOT / "docs" / "sprints" / "sistema_temas" / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "temas-v14-ci.yml"


ALLOWED_S0_PATHS = {
    ".github/workflows/temas-v14-ci.yml",
    "README.md",
    "docs/sprints/README.md",
    "docs/sprints/sistema_temas/README.md",
    "docs/sprints/sistema_temas/V14/README.md",
    "docs/sprints/sistema_temas/V14/CHECKPOINT_S0.md",
    "tools/tests/test_temas_v14_s0.py",
}


class V14S0FreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.readme = README_V14.read_text(encoding="utf-8")
        cls.checkpoint = CHECKPOINT.read_text(encoding="utf-8")
        cls.root_readme = ROOT_README.read_text(encoding="utf-8")
        cls.sprints_readme = SPRINTS_README.read_text(encoding="utf-8")
        cls.temas_readme = TEMAS_README.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_s0_artifacts_exist(self) -> None:
        for path in (PLAN, README_V14, CHECKPOINT, WORKFLOW):
            self.assertTrue(path.is_file(), path)

    def test_plan_keeps_exact_s0_contract(self) -> None:
        required = (
            "### S0 — Reconciliação pós-V13 e freeze de readiness",
            "confirmar o fechamento real da V13",
            "classificar documentação viva versus evidência histórica",
            "congelar o escopo V14",
            "inventariar dívidas, bloqueios e concorrência",
            "criar a superfície viva V14",
            "definir CI V14 read-only",
            "confirmar que nenhuma afirmação de production readiness já existe sem evidência",
            "`V14/README.md`",
            "`V14/CHECKPOINT_S0.md`",
            "guarda/CI V14 inicial",
        )
        for fragment in required:
            self.assertIn(fragment, self.plan)

    def test_s0_historical_boundary_remains_recorded_after_s1_starts(self) -> None:
        forbidden = (
            "MATRIZ_READINESS.json",
            "PACOTE_DECISAO_GO_LIVE.md",
            "CATALOGO_INCIDENTES.json",
            "CATALOGO_SLIS.json",
            "LEDGER_CUSTOS.json",
        )
        for name in forbidden:
            self.assertFalse((V14_DIR / name).exists(), name)
        self.assertIn("S1 não foi iniciado", self.checkpoint)
        if (V14_DIR / "MATRIZ_OWNERSHIP.json").exists():
            self.assertIn("S1", self.readme)
            self.assertIn("S2–S8 não foram iniciadas", self.readme)

    def test_inherited_nonpass_states_are_preserved(self) -> None:
        for document in (self.readme, self.checkpoint):
            self.assertIn("A11-01", document)
            self.assertIn("FAIL", document)
            self.assertIn("issue #57", document)
            self.assertIn("V12-LAB-01", document)
            self.assertIn("V12-APP-01", document)
            self.assertIn("V12-AIBI-02", document)
            self.assertIn("BLOQUEADO_AUTORIZACAO", document)

    def test_human_pass_is_not_promoted_to_readiness(self) -> None:
        self.assertIn("`HUMAN-01`", self.readme)
        self.assertIn("evidência formativa", self.readme)
        self.assertIn("sem inferência estatística", self.checkpoint)

    def test_v11_contract_is_frozen_not_reimplemented(self) -> None:
        for document in (self.readme, self.checkpoint):
            self.assertIn("48 tokens", document)
            self.assertIn("3 `translated`", document)
            self.assertIn("23 `approximated`", document)
            self.assertIn("22 `unsupported`", document)
            self.assertIn("três bindings diretos", document)
            self.assertIn('context="aibi"', document)
        self.assertFalse((V14_DIR / "theme.schema.json").exists())
        self.assertFalse((V14_DIR / "binding.json").exists())

    def test_six_surfaces_remain_exact(self) -> None:
        expected = {
            "notebook_visual_core",
            "visual_lab",
            "transition_bundle",
            "databricks_app",
            "aibi_dashboard",
            "workspace_theme",
        }
        observed = {item for item in expected if f"`{item}`" in self.readme}
        self.assertEqual(expected, observed)

    def test_root_readme_tracks_s0_integration_and_v14_continuity(self) -> None:
        self.assertIn("PR #70", self.root_readme)
        self.assertIn("PR #71", self.root_readme)
        self.assertIn("e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493", self.root_readme)
        self.assertIn("S1", self.root_readme)
        self.assertNotIn("candidata de planejamento tecnicamente certificada, pendente de aceite explícito", self.root_readme)

    def test_sprints_index_keeps_s0_historical_entry(self) -> None:
        marker = "## Sistema de Temas do Hub"
        self.assertIn(marker, self.sprints_readme)
        current = self.sprints_readme.split(marker, 1)[1].split("### Continuidade do Sistema de Temas", 1)[0]
        self.assertIn("PR #70", current)
        self.assertIn("S0", current)
        self.assertNotIn("**V14 não foi iniciada.**", current)

    def test_temas_index_keeps_v14_navigation(self) -> None:
        live = self.temas_readme.split("## Estado integrado anterior — V09", 1)[0]
        self.assertIn("V14", live)
        self.assertIn("PR #70", live)
        self.assertNotIn("**V14 não foi iniciada**", live)

    def test_checkpoint_records_baseline_and_concurrency(self) -> None:
        required = (
            "350dcf0b37e730042ef961f12f11b30b2660d2c6",
            "15/15 `success`",
            "PR #69",
            "ahead_by=15",
            "behind_by=6",
            "PR #51",
            "ahead_by=139",
            "behind_by=178",
        )
        for fragment in required:
            self.assertIn(fragment, self.checkpoint)

    def test_checkpoint_records_measured_metrics_and_fail_closed_history(self) -> None:
        required = (
            "42eb2074425e827a7865e4e6a5771818f3881940",
            "35127535148",
            "18465913feab5591e07e780737093294aae6c8bb",
            "35127864758",
            "17/17 PASS",
            "718/718 PASS",
            "12/12 PASS",
            "1485 arquivos",
            "1971 links",
            "2 falhas / 0 avisos",
        )
        for fragment in required:
            self.assertIn(fragment, self.checkpoint)
        self.assertIn("não estima métricas", self.checkpoint)

    def test_workflow_is_read_only(self) -> None:
        self.assertIn("permissions:\n  contents: read", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertNotIn("secrets.", self.workflow.lower())
        self.assertNotIn("DATABRICKS_TOKEN", self.workflow)
        self.assertNotIn("DATABRICKS_HOST", self.workflow)
        self.assertNotIn("databricks configure", self.workflow.lower())

    def test_workflow_keeps_s0_and_canonical_gates(self) -> None:
        expected = (
            "python -B tools/tests/test_temas_v14_s0.py -v",
            "python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v",
            "python -B tools/tests/test_visual_legado_v00.py",
            "python -B tools/validate_assistant.py --conferir-readme",
            "V14_S0_DATABRICKS_MUTATION=0",
        )
        for fragment in expected:
            self.assertIn(fragment, self.workflow)
        self.assertTrue(
            "V14_S1_NOT_STARTED=1" in self.workflow
            or ("tools/tests/test_temas_v14_s1.py" in self.workflow and "V14_S2_NOT_STARTED=1" in self.workflow)
        )

    def test_v14_plan_is_not_rewritten_by_s0_scope(self) -> None:
        self.assertNotIn("PLANO_MESTRE.md", ALLOWED_S0_PATHS)

    def test_ci_diff_stays_inside_s0_allowlist_only_on_s0_branch(self) -> None:
        if os.environ.get("GITHUB_ACTIONS") != "true":
            self.skipTest("escopo Git é verificado no GitHub Actions")

        event_name = os.environ.get("GITHUB_EVENT_NAME", "")
        ref_name = os.environ.get("GITHUB_REF_NAME", "")
        head_ref = os.environ.get("GITHUB_HEAD_REF", "")
        if event_name == "push" and ref_name == "main":
            self.skipTest("push da main já é baseline integrado")
        active_branch = head_ref or ref_name
        if not active_branch.startswith("codex/temas-v14-s0"):
            self.skipTest("allowlist S0 só se aplica à branch S0")

        try:
            merge_base = subprocess.check_output(
                ["git", "merge-base", "HEAD", "origin/main"], cwd=ROOT, text=True
            ).strip()
            changed = subprocess.check_output(
                ["git", "diff", "--name-only", f"{merge_base}...HEAD"], cwd=ROOT, text=True
            ).splitlines()
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            self.fail(f"não foi possível medir o escopo Git: {exc}")

        unexpected = sorted(set(changed) - ALLOWED_S0_PATHS)
        self.assertEqual([], unexpected, f"fora do escopo S0: {unexpected}")

    def test_s0_docs_forbid_databricks_mutation_and_go_live(self) -> None:
        combined = self.readme + "\n" + self.checkpoint
        self.assertIn("mutação Databricks", combined)
        self.assertIn("não executa", combined)
        self.assertIn("go-live", combined)
        self.assertIn("aceite explícito", combined)


if __name__ == "__main__":
    unittest.main()
