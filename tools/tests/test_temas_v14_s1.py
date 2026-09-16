from __future__ import annotations

import copy
import importlib.util
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V14_DIR = ROOT / "docs" / "sprints" / "sistema_temas" / "V14"
MATRIX = V14_DIR / "MATRIZ_OWNERSHIP.json"
RUNBOOK = V14_DIR / "S1_MODELO_OPERACIONAL.md"
CHECKPOINT = V14_DIR / "CHECKPOINT_S1.md"
README_V14 = V14_DIR / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "temas-v14-ci.yml"
VALIDATOR = ROOT / "tools" / "temas_v14_ownership.py"

spec = importlib.util.spec_from_file_location("temas_v14_ownership", VALIDATOR)
assert spec and spec.loader
ownership = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ownership)

ALLOWED_S1_PATHS = {
    ".github/workflows/temas-v14-ci.yml",
    "README.md",
    "docs/sprints/sistema_temas/V14/README.md",
    "docs/sprints/sistema_temas/V14/MATRIZ_OWNERSHIP.json",
    "docs/sprints/sistema_temas/V14/S1_MODELO_OPERACIONAL.md",
    "docs/sprints/sistema_temas/V14/CHECKPOINT_S1.md",
    "tools/temas_v14_ownership.py",
    "tools/tests/test_temas_v14_s0.py",
    "tools/tests/test_temas_v14_s1.py",
}


class V14S1OwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = ownership.load_matrix(MATRIX)
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.checkpoint = CHECKPOINT.read_text(encoding="utf-8")
        cls.readme = README_V14.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_real_matrix_validates(self) -> None:
        ownership.validate_matrix(self.matrix)

    def test_exact_six_surfaces_and_technical_owners(self) -> None:
        observed = {item["surface_id"]: item["technical_owner"]["owner_ref"] for item in self.matrix["surfaces"]}
        self.assertEqual(ownership.EXPECTED_SURFACES, observed)

    def test_all_operational_slots_are_fail_closed_without_evidence(self) -> None:
        for item in self.matrix["surfaces"]:
            self.assertEqual(ownership.EXPECTED_ROLES, set(item["operational_roles"]))
            for role in item["operational_roles"].values():
                self.assertEqual("BLOCKED", role["status"])
                self.assertIsNone(role["principal_ref"])
                self.assertEqual([], role["evidence_refs"])

    def test_v01_and_v13_remain_canonical_owners(self) -> None:
        self.assertEqual("docs/sprints/sistema_temas/V01/GOVERNANCA.md", self.matrix["role_policy_ref"])
        self.assertEqual("docs/sprints/sistema_temas/V13/MATRIZ_OPERACIONAL.json", self.matrix["operational_inventory_ref"])

    def test_missing_technical_owner_fails(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        mutant["surfaces"][0]["technical_owner"].pop("owner_ref")
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_wrong_technical_owner_fails(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        mutant["surfaces"][0]["technical_owner"]["owner_ref"] = "V11"
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_missing_operational_slot_fails(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        mutant["surfaces"][0]["operational_roles"].pop("backup_operational_owner")
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_blocked_slot_cannot_claim_principal(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        mutant["surfaces"][0]["operational_roles"]["operational_owner"]["principal_ref"] = "role:operator"
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_evidenced_authority_requires_evidence(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        role = mutant["surfaces"][0]["operational_roles"]["go_live_authority"]
        role["status"] = "EVIDENCED"
        role["principal_ref"] = "role:go-live-authority"
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_invented_authority_fails_even_with_existing_file_ref(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        role = mutant["surfaces"][0]["operational_roles"]["go_live_authority"]
        role["status"] = "EVIDENCED"
        role["principal_ref"] = "invented:go-live-board"
        role["evidence_refs"] = ["docs/sprints/sistema_temas/V01/GOVERNANCA.md"]
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_self_approval_fails(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        roles = mutant["surfaces"][0]["operational_roles"]
        for name in ("operational_owner", "change_approver"):
            roles[name]["status"] = "EVIDENCED"
            roles[name]["principal_ref"] = "role:same-principal"
            roles[name]["evidence_refs"] = ["docs/sprints/sistema_temas/V01/GOVERNANCA.md"]
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_nonexistent_evidence_ref_fails(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        mutant["surfaces"][0]["technical_owner"]["evidence_refs"] = [
            "docs/sprints/sistema_temas/V13/MATRIZ_OPERACIONAL.json",
            "docs/sprints/sistema_temas/V99/README.md",
        ]
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_remote_mutation_readiness_and_s2_claims_fail(self) -> None:
        for key, value in (
            ("remote_mutation_performed_by_s1", True),
            ("production_readiness_declared", True),
            ("s2_started", True),
        ):
            mutant = copy.deepcopy(self.matrix)
            mutant[key] = value
            with self.assertRaises(ownership.OwnershipContractError, msg=key):
                ownership.validate_matrix(mutant)

    def test_go_live_decision_remains_not_decided(self) -> None:
        mutant = copy.deepcopy(self.matrix)
        mutant["go_live_decision"] = "GO"
        with self.assertRaises(ownership.OwnershipContractError):
            ownership.validate_matrix(mutant)

    def test_inherited_states_are_not_reclassified(self) -> None:
        self.assertEqual(ownership.EXPECTED_INHERITED, self.matrix["inherited_states"])
        for document in (self.runbook, self.checkpoint, self.readme):
            self.assertIn("A11-01", document)
            self.assertIn("FAIL", document)
            self.assertIn("issue #57", document)
            self.assertIn("V12-LAB-01", document)
            self.assertIn("V12-APP-01", document)
            self.assertIn("V12-AIBI-02", document)
            self.assertIn("BLOQUEADO_AUTORIZACAO", document)

    def test_human_pass_remains_formative(self) -> None:
        self.assertIn("HUMAN-01", self.checkpoint)
        self.assertIn("evidência formativa", self.checkpoint)
        self.assertIn("sem inferência estatística", self.checkpoint)

    def test_runbook_forbids_invented_identity_channel_and_sla(self) -> None:
        required = (
            "Não foram inventados",
            "nomes de pessoas",
            "grupos corporativos",
            "e-mails",
            "canais de Teams/Slack",
            "SLA/SLO",
            "`BLOCKED`",
            "Não faça self-approval",
            "Não derive go-live de owner técnico",
        )
        for fragment in required:
            self.assertIn(fragment, self.runbook)

    def test_s2_artifacts_are_not_started(self) -> None:
        self.assertFalse((V14_DIR / "MATRIZ_READINESS.json").exists())
        self.assertFalse((V14_DIR / "CATALOGO_INCIDENTES.json").exists())
        self.assertFalse((V14_DIR / "CATALOGO_SLIS.json").exists())
        self.assertIn("S2 não iniciada", self.checkpoint)

    def test_validator_has_no_network_databricks_or_mutation_clients(self) -> None:
        source = VALIDATOR.read_text(encoding="utf-8").lower()
        forbidden = ("requests", "urllib", "socket", "databricks", "subprocess", "dbutils", "workspaceclient")
        for token in forbidden:
            self.assertNotIn(token, source)

    def test_workflow_runs_s0_s1_and_canonical_gates_read_only(self) -> None:
        required = (
            "permissions:\n  contents: read",
            "persist-credentials: false",
            "python -B tools/tests/test_temas_v14_s0.py -v",
            "python -B tools/temas_v14_ownership.py --check",
            "python -B tools/tests/test_temas_v14_s1.py -v",
            "python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v",
            "python -B tools/tests/test_visual_legado_v00.py",
            "python -B tools/validate_assistant.py --conferir-readme",
            "V14_S1_DATABRICKS_MUTATION=0",
            "V14_S2_NOT_STARTED=1",
        )
        for fragment in required:
            self.assertIn(fragment, self.workflow)
        self.assertNotIn("secrets.", self.workflow.lower())
        self.assertNotIn("DATABRICKS_TOKEN", self.workflow)
        self.assertNotIn("DATABRICKS_HOST", self.workflow)

    def test_readme_marks_s0_integrated_s1_active_and_s2_not_started(self) -> None:
        self.assertIn("PR #71", self.readme)
        self.assertIn("e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493", self.readme)
        self.assertIn("S1", self.readme)
        self.assertIn("S2–S8 não foram iniciadas", self.readme)

    def test_ci_diff_stays_inside_s1_allowlist(self) -> None:
        if os.environ.get("GITHUB_ACTIONS") != "true":
            self.skipTest("escopo Git é verificado no GitHub Actions")
        if os.environ.get("GITHUB_EVENT_NAME") == "push" and os.environ.get("GITHUB_REF_NAME") == "main":
            self.skipTest("push da main já representa baseline integrado")

        try:
            merge_base = subprocess.check_output(
                ["git", "merge-base", "HEAD", "origin/main"], cwd=ROOT, text=True
            ).strip()
            changed = subprocess.check_output(
                ["git", "diff", "--name-only", f"{merge_base}...HEAD"], cwd=ROOT, text=True
            ).splitlines()
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            self.fail(f"não foi possível medir escopo Git: {exc}")

        unexpected = sorted(set(changed) - ALLOWED_S1_PATHS)
        self.assertEqual([], unexpected, f"fora do escopo S1: {unexpected}")


if __name__ == "__main__":
    unittest.main()
