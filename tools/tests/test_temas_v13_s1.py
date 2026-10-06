from __future__ import annotations

import ast
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import temas_v13_operacional as contract  # noqa: E402


class V13S1ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = contract.load_matrix()

    def surface(self, surface_id: str):
        return next(item for item in self.data["surfaces"] if item["surface_id"] == surface_id)

    @staticmethod
    def action(surface: dict, action_id: str):
        return next(item for item in surface["actions"] if item["action_id"] == action_id)

    def assert_invalid(self, data: dict):
        with self.assertRaises(contract.OperationalContractError):
            contract.validate_matrix(data)

    def test_package_imports_in_fresh_process_without_pythonpath(self):
        # A descoberta agregada altera sys.path; não pode preparar o import da S2.
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        result = subprocess.run(
            [sys.executable, "-B", "-c", (
                "from tools import temas_v13_operacional as contract; "
                "from tools import temas_v13_preflight as preflight; "
                "from tools.project_policy import SIMULATED_ROOT; "
                "assert contract.SIMULATED_ROOT == SIMULATED_ROOT; "
                "assert preflight.s1_contract is contract; "
                "contract.validate_matrix(contract.load_matrix())"
            )],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_script_and_module_entrypoints_without_pythonpath(self):
        # Preserva a CLI direta, inclusive fora da raiz, e a execução como pacote.
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        with tempfile.TemporaryDirectory(prefix="v13 entrypoint ") as outside:
            routes = (
                (outside, [str(TOOLS / "temas_v13_operacional.py")]),
                (ROOT, ["-m", "tools.temas_v13_operacional"]),
            )
            for cwd, arguments in routes:
                with self.subTest(arguments=arguments):
                    result = subprocess.run(
                        [sys.executable, "-B", *arguments], cwd=cwd, env=env,
                        capture_output=True, text=True, timeout=60,
                    )
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertIn("PASS", result.stdout)

    def test_current_derived_root_and_legacy_owner_alias_fail_closed(self):
        self.assertEqual(".artifacts/simulado/", self.data["rules"]["derived_root"])
        mutant = copy.deepcopy(self.data)
        mutant["rules"]["derived_root"] = "Novo_Ambiente_Simulado/"
        self.assert_invalid(mutant)
        for ref in (".artifacts/simulado/Users/usuario-free/x", "Novo_Ambiente_Simulado/x"):
            with self.assertRaises(contract.OperationalContractError):
                contract._check_repo_ref(ref, "synthetic")

    def test_real_matrix_validates(self):
        contract.validate_matrix(self.data)

    def test_surface_set_is_exactly_the_plan_inventory(self):
        self.assertEqual(
            {item["surface_id"] for item in self.data["surfaces"]},
            contract.EXPECTED_SURFACES,
        )

    def test_every_owner_and_artifact_is_a_real_reference(self):
        # A validação real percorre owners, dependências, artefatos, checks, smoke,
        # rollback e evidências. Se qualquer caminho sumir, o contrato falha.
        contract.validate_matrix(self.data)

    def test_s1_does_not_copy_canonical_contracts(self):
        serialized = json.dumps(self.data, ensure_ascii=False)
        self.assertNotIn("widget.background", serialized)
        self.assertNotIn("widget.corner_radius", serialized)
        self.assertNotIn("visualization.categorical_palette", serialized)
        self.assertFalse(set(contract._walk_keys(self.data)) & contract.FORBIDDEN_DUPLICATE_KEYS)

    def test_relationships_cover_v05_v09_v10_v11_boundaries(self):
        rels = {item["relationship_id"] for item in self.data["relationships"]}
        self.assertTrue(
            {
                "visual_lab_reuses_core",
                "app_reuses_visual_lab",
                "transition_bundle_transports_core_without_activation",
                "transition_bundle_does_not_replace_app_bundle",
                "aibi_projects_from_resolved_theme",
                "workspace_theme_is_separate_from_dashboard_theme",
            }
            <= rels
        )

    def test_mutant_without_owner_fails(self):
        mutant = copy.deepcopy(self.data)
        del mutant["surfaces"][0]["primary_owner"]
        self.assert_invalid(mutant)

    def test_mutant_with_missing_owner_artifact_fails(self):
        mutant = copy.deepcopy(self.data)
        mutant["surfaces"][0]["primary_owner"]["contract_ref"] = "docs/nao-existe.md"
        self.assert_invalid(mutant)

    def test_mutant_without_authorization_on_mutable_action_fails(self):
        mutant = copy.deepcopy(self.data)
        app = next(item for item in mutant["surfaces"] if item["surface_id"] == "databricks_app")
        deploy = next(item for item in app["actions"] if item["action_id"] == "deploy_app")
        del deploy["authorization"]
        self.assert_invalid(mutant)

    def test_mutant_without_rollback_on_mutable_action_fails(self):
        mutant = copy.deepcopy(self.data)
        app = next(item for item in mutant["surfaces"] if item["surface_id"] == "databricks_app")
        deploy = next(item for item in app["actions"] if item["action_id"] == "deploy_app")
        del deploy["rollback"]
        self.assert_invalid(mutant)

    def test_mutant_that_marks_mutation_authorization_optional_fails(self):
        mutant = copy.deepcopy(self.data)
        app = next(item for item in mutant["surfaces"] if item["surface_id"] == "databricks_app")
        deploy = next(item for item in app["actions"] if item["action_id"] == "deploy_app")
        deploy["authorization"]["required"] = False
        self.assert_invalid(mutant)

    def test_mutant_that_marks_mutation_rollback_optional_fails(self):
        mutant = copy.deepcopy(self.data)
        workspace = next(item for item in mutant["surfaces"] if item["surface_id"] == "workspace_theme")
        action = workspace["actions"][0]
        action["rollback"]["required"] = False
        self.assert_invalid(mutant)

    def test_mutant_that_anticipates_s2_preflight_fails(self):
        mutant = copy.deepcopy(self.data)
        mutant["surfaces"][0]["preflight"]["stage"] = "IMPLEMENTED"
        self.assert_invalid(mutant)

    def test_mutant_that_claims_s1_remote_mutation_fails(self):
        mutant = copy.deepcopy(self.data)
        workspace = next(item for item in mutant["surfaces"] if item["surface_id"] == "workspace_theme")
        workspace["actions"][0]["performed_by_s1"] = True
        self.assert_invalid(mutant)

    def test_mutant_that_embeds_second_token_contract_fails(self):
        mutant = copy.deepcopy(self.data)
        mutant["surfaces"][0]["tokens"] = {"brand.primary": "#000000"}
        self.assert_invalid(mutant)

    def test_inherited_non_pass_states_are_preserved(self):
        states = {
            state["case_id"]: state["state"]
            for surface in self.data["surfaces"]
            for state in surface["known_homologation_states"]
        }
        self.assertEqual(states["A11-01"], "FAIL")
        self.assertEqual(states["V12-LAB-01"], "BLOQUEADO_AUTORIZACAO")
        self.assertEqual(states["V12-APP-01"], "BLOQUEADO_AUTORIZACAO")
        self.assertEqual(states["V12-AIBI-02"], "BLOQUEADO_AUTORIZACAO")

    def test_aibi_pass_scope_does_not_hide_a11_fail(self):
        states = {
            state["case_id"]: state
            for state in self.surface("aibi_dashboard")["known_homologation_states"]
        }
        self.assertEqual(states["V12-AIBI-01"]["state"], "PASS")
        self.assertIn("draft", states["V12-AIBI-01"]["scope"])
        self.assertEqual(states["A11-01"]["state"], "FAIL")
        self.assertEqual(states["A11-01"]["issue_ref"], "#57")

    def test_workspace_and_dashboard_are_distinct_surfaces(self):
        ids = {item["surface_id"] for item in self.data["surfaces"]}
        self.assertIn("aibi_dashboard", ids)
        self.assertIn("workspace_theme", ids)
        self.assertNotEqual(self.surface("aibi_dashboard"), self.surface("workspace_theme"))

    def test_validator_has_no_network_or_databricks_client_import(self):
        source = (ROOT / "tools/temas_v13_operacional.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertTrue(imports.isdisjoint({"requests", "socket", "urllib", "httpx", "databricks", "subprocess"}))

    def test_s1_documentation_keeps_s2_and_databricks_out_of_scope(self):
        doc = (ROOT / "docs/sprints/sistema_temas/V13/S1_INVENTARIO_OPERACIONAL.md").read_text(encoding="utf-8")
        self.assertIn("S2 não foi implementada", doc)
        self.assertIn("nenhuma mutação Databricks", doc)
        self.assertIn("Para quem nunca entrou no Hub", doc)

    def test_v13_workflow_is_read_only(self):
        workflow = (ROOT / ".github/workflows/temas-v13-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("DATABRICKS_HOST", workflow)
        self.assertNotIn("DATABRICKS_TOKEN", workflow)
        self.assertNotIn("secrets.", workflow)


if __name__ == "__main__":
    unittest.main()
