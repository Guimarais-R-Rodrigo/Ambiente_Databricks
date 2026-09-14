from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "tools" / "micromodelo_mm01_contract.py"
SCHEMA = REPO / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
TEMPLATE = REPO / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.template.yaml"
FIXTURES = REPO / "tools" / "tests" / "fixtures" / "micromodelos_mm01"

spec = importlib.util.spec_from_file_location("micromodelo_mm01_contract", CONTRACT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def _walk(document: object, path: list[object]) -> tuple[object, object]:
    current = document
    for part in path[:-1]:
        current = current[part]  # type: ignore[index]
    return current, path[-1]


def _apply_operations(document: dict, operations: list[dict]) -> dict:
    result = copy.deepcopy(document)
    for operation in operations:
        parent, leaf = _walk(result, operation["path"])
        if operation["acao"] == "set":
            parent[leaf] = operation.get("value")  # type: ignore[index]
        elif operation["acao"] == "delete":
            del parent[leaf]  # type: ignore[index]
        else:  # pragma: no cover - protege a própria fixture
            raise AssertionError(f"ação de fixture desconhecida: {operation['acao']}")
    return result


class MicromodeloMM01ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = module.load_schema(SCHEMA)
        cls.valid = json.loads((FIXTURES / "valido_validado.json").read_text(encoding="utf-8"))
        cls.invalid_cases = json.loads((FIXTURES / "casos_invalidos.json").read_text(encoding="utf-8"))

    def codes(self, document: dict) -> set[str]:
        return {issue.code for issue in module.validate_spec(document, self.schema)}

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_template_yaml_is_valid(self) -> None:
        document = module.load_document(TEMPLATE)
        self.assertEqual([], module.validate_spec(document, self.schema))
        semantics = document["classificacao"]["semantica"]
        self.assertIn("quando_true", semantics)
        self.assertIn("quando_false", semantics)
        self.assertNotIn(True, semantics)
        self.assertNotIn(False, semantics)

    def test_validated_fixture_is_valid(self) -> None:
        self.assertEqual([], module.validate_spec(self.valid, self.schema))

    def test_negative_fixtures_fail_for_expected_reason(self) -> None:
        self.assertEqual(9, len(self.invalid_cases))
        for case in self.invalid_cases:
            with self.subTest(nome=case["nome"]):
                document = _apply_operations(self.valid, case["operacoes"])
                self.assertIn(case["codigo_esperado"], self.codes(document))

    def test_unknown_source_reference_is_rejected(self) -> None:
        document = copy.deepcopy(self.valid)
        document["evidencias"][0]["fontes_ref"] = ["fonte_inexistente"]
        self.assertIn("UNKNOWN_SOURCE_REF", self.codes(document))

    def test_score_disabled_cannot_leave_score_contract_behind(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["habilitado"] = False
        self.assertIn("SCORE_DISABLED", self.codes(document))


    def test_human_validation_decision_must_match_status(self) -> None:
        document = copy.deepcopy(self.valid)
        document["validacao"]["aprovacao_humana"]["status"] = "REPROVADO"
        self.assertIn("VALIDATION_HUMAN_GATE", self.codes(document))

    def test_valid_transition_table_has_rework_but_no_skips(self) -> None:
        self.assertIn((None, "IDEIA"), module.TRANSICOES_FASE)
        self.assertIn(("EM_VALIDACAO", "EM_ESTUDO"), module.TRANSICOES_FASE)
        self.assertNotIn(("IDEIA", "EM_ESTUDO"), module.TRANSICOES_FASE)
        self.assertNotIn(("VALIDADO", "PUBLICADO"), module.TRANSICOES_FASE)
        self.assertNotIn(("PUBLICADO", "EM_ESTUDO"), module.TRANSICOES_FASE)

    def test_cli_returns_zero_for_template_and_one_for_invalid_document(self) -> None:
        ok = subprocess.run(
            [sys.executable, str(CONTRACT), str(TEMPLATE), "--schema", str(SCHEMA)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, ok.returncode, ok.stdout + ok.stderr)
        self.assertIn("APROVADO", ok.stdout)

        document = copy.deepcopy(self.valid)
        document["fontes"][0]["catalogo_ref"] = "OUTRO_CATALOGO"
        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalido.json"
            invalid_path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
            bad = subprocess.run(
                [sys.executable, str(CONTRACT), str(invalid_path), "--schema", str(SCHEMA)],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, bad.returncode, bad.stdout + bad.stderr)
        self.assertIn("CATALOG_SCOPE", bad.stdout)


if __name__ == "__main__":
    unittest.main()
