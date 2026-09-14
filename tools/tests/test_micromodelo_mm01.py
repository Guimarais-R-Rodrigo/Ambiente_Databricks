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
        cls.valid = json.loads(
            (FIXTURES / "valido_validado.json").read_text(encoding="utf-8")
        )
        cls.invalid_cases = json.loads(
            (FIXTURES / "casos_invalidos.json").read_text(encoding="utf-8")
        )

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

    def test_cosmetic_semantic_duplicates_are_rejected(self) -> None:
        document = copy.deepcopy(self.valid)
        original = document["classificacao"]["semantica"]["quando_true"]
        document["classificacao"]["semantica"]["quando_false"] = (
            f"  {original.upper()} !!!  "
        )
        self.assertIn("AMBIGUOUS_BINARY_SEMANTICS", self.codes(document))

    def test_probability_language_requires_calibrated_semantics(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["semantica"] = (
            "probabilidade estimada de o cliente possuir a característica"
        )
        self.assertIn("SCORE_PROBABILITY_LANGUAGE", self.codes(document))

        calibrated = copy.deepcopy(self.valid)
        calibrated["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"
        calibrated["score"]["semantica"] = (
            "probabilidade calibrada de o cliente possuir a característica"
        )
        calibrated["score"]["calibracao"] = {
            "metodo": "calibracao_sintetica",
            "evidencia_ref": "exp_001",
            "proveniencia": {
                "status": "MEDIDO",
                "origem": "execucao sintetica",
                "referencia": "calibracao_sintetica",
                "observado_em_utc": "2026-09-14T13:30:00Z",
                "aprovacao": None,
                "medicao": {
                    "referencia_execucao": "run-calibracao-001",
                    "medido_em_utc": "2026-09-14T13:30:00Z",
                },
            },
        }
        self.assertEqual([], module.validate_spec(calibrated, self.schema))

    def test_duplicate_ids_are_rejected_in_components_and_experiments(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["componentes"].append(
            copy.deepcopy(document["score"]["componentes"][0])
        )
        self.assertIn("DUPLICATE_ID", self.codes(document))

        document = copy.deepcopy(self.valid)
        document["experimentos"].append(
            copy.deepcopy(document["experimentos"][0])
        )
        self.assertIn("DUPLICATE_ID", self.codes(document))

    def test_validation_phase_requires_nonempty_material_content(self) -> None:
        for field in ("fontes", "evidencias", "contra_evidencias"):
            with self.subTest(field=field):
                document = copy.deepcopy(self.valid)
                document[field] = []
                self.assertIn("PHASE_CONTENT_GATE", self.codes(document))

        document = copy.deepcopy(self.valid)
        document["validacao"]["criterios"] = []
        self.assertIn("PHASE_CONTENT_GATE", self.codes(document))

    def test_publication_status_must_match_lifecycle_phase(self) -> None:
        document = copy.deepcopy(self.valid)
        document["publicacao"]["status"] = "PUBLICADA"
        document["publicacao"]["produto_dados_ref"] = "produto-sintetico"
        self.assertIn("PUBLICATION_STATUS_PHASE", self.codes(document))

    def test_publication_lifecycle_has_valid_positive_path(self) -> None:
        ready = copy.deepcopy(self.valid)
        ready["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {
                "nome": "possui_caracteristica",
                "tipo": "BOOLEAN",
            },
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "descricao": "publicar cobertura separada para preservar casos indeterminados",
                "proveniencia": {
                    "status": "APROVADO",
                    "origem": "decisao humana sintetica",
                    "referencia": "PUB-001",
                    "observado_em_utc": "2026-09-14T15:00:00Z",
                    "aprovacao": {
                        "por": "analista_responsavel",
                        "em_utc": "2026-09-14T15:00:00Z",
                        "referencia": "PUB-001",
                    },
                    "medicao": None,
                },
            },
        }

        candidate = copy.deepcopy(ready)
        candidate["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        candidate["identidade"]["estado"]["fase_atual"] = "CANDIDATO_PRODUTO"
        candidate["publicacao"]["status"] = "CANDIDATA"
        self.assertEqual([], module.validate_spec(candidate, self.schema))

        external = copy.deepcopy(ready)
        external["identidade"]["estado"]["fase_anterior"] = "CANDIDATO_PRODUTO"
        external["identidade"]["estado"]["fase_atual"] = "EM_VALIDACAO_GOVERNANCA"
        external["publicacao"]["status"] = "EM_VALIDACAO_EXTERNA"
        external["publicacao"]["handoff_ref"] = "handoff-sintetico-001"
        self.assertEqual([], module.validate_spec(external, self.schema))

        published = copy.deepcopy(ready)
        published["identidade"]["estado"]["fase_anterior"] = "EM_VALIDACAO_GOVERNANCA"
        published["identidade"]["estado"]["fase_atual"] = "PUBLICADO"
        published["publicacao"]["status"] = "PUBLICADA"
        published["publicacao"]["handoff_ref"] = "handoff-sintetico-001"
        published["publicacao"]["produto_dados_ref"] = "produto-sintetico-001"
        self.assertEqual([], module.validate_spec(published, self.schema))

    def test_unknown_property_in_material_block_is_rejected(self) -> None:
        document = copy.deepcopy(self.valid)
        document["classificacao"]["campo_desconhecido"] = "nao permitido"
        self.assertIn("SCHEMA", self.codes(document))

    def test_duplicate_yaml_and_json_keys_are_rejected_on_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            yaml_path = Path(tmp) / "duplicado.yaml"
            yaml_path.write_text(
                'schema_version: "1.0.0"\nschema_version: "2.0.0"\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicada"):
                module.load_document(yaml_path)

            json_path = Path(tmp) / "duplicado.json"
            json_path.write_text(
                '{"schema_version":"1.0.0","schema_version":"2.0.0"}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicada"):
                module.load_document(json_path)

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
            invalid_path.write_text(
                json.dumps(document, ensure_ascii=False), encoding="utf-8"
            )
            bad = subprocess.run(
                [
                    sys.executable,
                    str(CONTRACT),
                    str(invalid_path),
                    "--schema",
                    str(SCHEMA),
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
            bypass = subprocess.run(
                [
                    sys.executable,
                    str(CONTRACT),
                    str(invalid_path),
                    "--schema",
                    str(SCHEMA),
                    "--catalog-ref",
                    "OUTRO_CATALOGO",
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, bad.returncode, bad.stdout + bad.stderr)
        self.assertIn("CATALOG_SCOPE", bad.stdout)
        self.assertEqual(2, bypass.returncode, bypass.stdout + bypass.stderr)
        self.assertIn("unrecognized arguments", bypass.stderr)


if __name__ == "__main__":
    unittest.main()
