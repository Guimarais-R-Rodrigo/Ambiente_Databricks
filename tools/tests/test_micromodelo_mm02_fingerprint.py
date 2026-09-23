from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import micromodelo_mm01_contract as mm01
import micromodelo_mm02_fingerprint as mm02


SCHEMA = REPO / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
FIXTURE = (
    REPO
    / "tools"
    / "tests"
    / "fixtures"
    / "micromodelos_mm01"
    / "valido_validado.json"
)
SCRIPT = REPO / "tools" / "micromodelo_mm02_fingerprint.py"


class MicromodeloMM02FingerprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = mm01.load_schema(SCHEMA)
        cls.valid = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.assert_valid_static(cls.valid)

    @classmethod
    def assert_valid_static(cls, document: dict) -> None:
        issues = mm01.validate_spec(document, cls.schema)
        if issues:
            raise AssertionError("\n".join(str(issue) for issue in issues))

    def fingerprint(self, document: dict) -> str:
        return mm02.calculate_spec_fingerprint(document, self.schema).sha256

    def assert_preserves(self, document: dict) -> None:
        self.assert_valid_static(document)
        self.assertEqual(self.fingerprint(self.valid), self.fingerprint(document))

    def assert_changes(self, document: dict) -> None:
        self.assert_valid_static(document)
        self.assertNotEqual(self.fingerprint(self.valid), self.fingerprint(document))

    def calibrated_score(self) -> dict:
        document = copy.deepcopy(self.valid)
        document["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"
        document["score"]["calibracao"] = {
            "metodo": "platt sintetico",
            "evidencia_ref": "exp_001",
            "proveniencia": copy.deepcopy(
                document["experimentos"][0]["proveniencia"]
            ),
        }
        self.assert_valid_static(document)
        return document

    def candidate_with_publication_contract(self) -> dict:
        candidate = copy.deepcopy(self.valid)
        candidate["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        candidate["identidade"]["estado"]["fase_atual"] = "CANDIDATO_PRODUTO"
        candidate["saida"]["publicacao"]["estado"] = "DEFINIDO"
        candidate["saida"]["publicacao"]["campo_booleano"] = {
            "nome": "flag_micromodelo",
            "tipo": "BOOLEAN",
        }
        candidate["saida"]["publicacao"]["politica_indeterminado"] = {
            "tratamento": "EXCLUIR_DA_PUBLICACAO",
            "indeterminado_vira_false": False,
            "regra_ref": None,
            "proveniencia": copy.deepcopy(
                self.valid["classificacao"]["semantica"]["proveniencia"]
            ),
        }
        candidate["publicacao"]["status"] = "CANDIDATA"
        self.assert_valid_static(candidate)
        return candidate

    def test_fingerprint_shape_and_algorithm_are_explicit(self) -> None:
        result = mm02.calculate_spec_fingerprint(self.valid, self.schema)
        self.assertEqual("mm02-spec-fingerprint-v1", result.algorithm)
        self.assertEqual("1.0.0", result.algorithm_version)
        self.assertRegex(result.sha256, r"^[0-9a-f]{64}$")
        parsed = json.loads(result.canonical_json)
        self.assertEqual(result.algorithm, parsed["algorithm"])
        self.assertEqual(result.algorithm_version, parsed["algorithm_version"])

    def test_raw_mapping_key_order_does_not_change_fingerprint(self) -> None:
        reordered = dict(reversed(list(self.valid.items())))
        self.assert_preserves(reordered)

    def test_source_column_serial_order_does_not_change_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["fontes"][0]["campos"] = list(reversed(document["fontes"][0]["campos"]))
        self.assert_preserves(document)

    def test_component_collection_order_does_not_change_fingerprint(self) -> None:
        base = copy.deepcopy(self.valid)
        second = copy.deepcopy(base["score"]["componentes"][0])
        second["id"] = "volume"
        second["descricao"] = "volume sintético observado"
        second["peso"] = 0.4
        base["score"]["componentes"].append(second)
        self.assert_valid_static(base)

        reversed_order = copy.deepcopy(base)
        reversed_order["score"]["componentes"].reverse()
        self.assertEqual(self.fingerprint(base), self.fingerprint(reversed_order))

    def test_editorial_semantic_text_normalization_preserves_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        original = document["negocio"]["definicao_operacional"]
        document["negocio"]["definicao_operacional"] = (
            "   " + "   ".join(original.upper().split()) + "?!…   "
        )
        self.assert_preserves(document)

    def test_human_version_title_and_objective_are_not_material_identity(self) -> None:
        document = copy.deepcopy(self.valid)
        document["identidade"]["micromodel_version"] = "1.0.1"
        document["identidade"]["titulo"] = "Título editorial alternativo do mesmo micromodelo"
        document["negocio"]["objetivo"] = (
            "Texto explicativo alternativo que não modifica a definição operacional."
        )
        self.assert_preserves(document)

    def test_structured_score_semantics_audit_reference_is_not_material(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["semantica_ref"] = "SEM-AUDIT-999"
        self.assert_preserves(document)

    def test_standard_normalization_audit_reference_is_not_material(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["normalizacao"]["referencia"] = "NORM-AUDIT-999"
        self.assert_preserves(document)

    def test_initial_punctuation_is_not_editorial_equivalent(self) -> None:
        document = copy.deepcopy(self.valid)
        document["negocio"]["definicao_operacional"] = (
            "?" + document["negocio"]["definicao_operacional"]
        )
        self.assert_changes(document)

    def test_provenance_approval_and_timestamps_do_not_change_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["evidencias"][0]["proveniencia"]["referencia"] = "DEC-999"
        document["evidencias"][0]["proveniencia"]["aprovacao"]["referencia"] = "DEC-999"
        document["validacao"]["aprovacao_humana"]["referencia"] = "VALID-999"
        document["proveniencia"]["criado_em_utc"] = "2026-09-15T00:00:00Z"
        self.assert_preserves(document)

    def test_experiment_result_is_evidence_not_material_definition(self) -> None:
        document = copy.deepcopy(self.valid)
        document["experimentos"][0]["resultado"] = (
            "nova execução sintética reproduziu a mesma hipótese por outra run"
        )
        document["experimentos"][0]["proveniencia"]["medicao"][
            "referencia_execucao"
        ] = "run-dev-999"
        self.assert_preserves(document)

    def test_explanatory_descriptions_do_not_change_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["evidencias"][0]["descricao"] = "Descrição editorial revisada"
        document["contra_evidencias"][0]["descricao"] = (
            "Descrição editorial alternativa da contra-evidência"
        )
        document["classificacao"]["limiares"][0]["descricao"] = "Limiar editorialmente renomeado"
        document["score"]["componentes"][0]["descricao"] = (
            "Descrição editorial do componente revisada"
        )
        self.assert_preserves(document)

    def test_equivalent_integer_and_float_numbers_share_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["classificacao"]["limiares"][0]["valor"] = 70.0
        self.assert_preserves(document)

    def test_publication_lifecycle_status_is_not_material_definition(self) -> None:
        candidate = self.candidate_with_publication_contract()
        rejected = copy.deepcopy(candidate)
        rejected["publicacao"]["status"] = "REJEITADA"
        self.assert_valid_static(rejected)
        self.assertEqual(self.fingerprint(candidate), self.fingerprint(rejected))

    def test_source_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["fontes"][0]["objeto"] = "eventos_sinteticos_v2"
        self.assert_changes(document)

    def test_entity_grain_or_time_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["entidade"]["referencia_temporal"] = (
            "último fechamento mensal anterior à data de decisão"
        )
        self.assert_changes(document)

    def test_evidence_rule_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["evidencias"][0]["regra"] = (
            "considerar recorrência somente quando houver dois eventos na janela definida"
        )
        self.assert_changes(document)

    def test_threshold_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["classificacao"]["limiares"][0]["valor"] = 71
        self.assert_changes(document)

    def test_missing_policy_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        missing = document["classificacao"]["ausencia_evidencia"]
        missing["tratamento"] = "REGRA_EXPLICITA_APROVADA"
        missing["resultado_sem_evidencia"] = "FALSE"
        missing["regra_ref"] = "REGRA-MISSING-001"
        self.assert_changes(document)

    def test_classification_semantics_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["classificacao"]["semantica"]["quando_true"] = (
            "há evidência suficiente e confirmação adicional para afirmar a característica"
        )
        self.assert_changes(document)

    def test_score_weight_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["componentes"][0]["peso"] = 0.7
        self.assert_changes(document)

    def test_score_meaning_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["score"]["tipo_semantica"] = "OUTRA_APROVADA"
        self.assert_changes(document)

    def test_custom_score_semantics_reference_is_material(self) -> None:
        first = copy.deepcopy(self.valid)
        first["score"]["tipo_semantica"] = "OUTRA_APROVADA"
        self.assert_valid_static(first)

        second = copy.deepcopy(first)
        second["score"]["semantica_ref"] = "SEM-CUSTOM-999"
        self.assert_valid_static(second)
        self.assertNotEqual(self.fingerprint(first), self.fingerprint(second))

    def test_custom_normalization_reference_is_material(self) -> None:
        first = copy.deepcopy(self.valid)
        first["score"]["normalizacao"]["metodo"] = "CUSTOM_APROVADO"
        self.assert_valid_static(first)

        second = copy.deepcopy(first)
        second["score"]["normalizacao"]["referencia"] = "NORM-CUSTOM-999"
        self.assert_valid_static(second)
        self.assertNotEqual(self.fingerprint(first), self.fingerprint(second))

    def test_calibration_evidence_id_is_material_but_run_is_not(self) -> None:
        first = self.calibrated_score()

        same_definition_new_run = copy.deepcopy(first)
        same_definition_new_run["experimentos"][0]["resultado"] = (
            "nova execução reproduziu a mesma calibração"
        )
        same_definition_new_run["experimentos"][0]["proveniencia"]["medicao"][
            "referencia_execucao"
        ] = "run-calibracao-999"
        self.assert_valid_static(same_definition_new_run)
        self.assertEqual(
            self.fingerprint(first),
            self.fingerprint(same_definition_new_run),
        )

        different_calibration = copy.deepcopy(first)
        second_experiment = copy.deepcopy(different_calibration["experimentos"][0])
        second_experiment["id"] = "exp_002"
        different_calibration["experimentos"].append(second_experiment)
        different_calibration["score"]["calibracao"]["evidencia_ref"] = "exp_002"
        self.assert_valid_static(different_calibration)
        self.assertNotEqual(
            self.fingerprint(first),
            self.fingerprint(different_calibration),
        )

    def test_study_output_contract_change_changes_fingerprint(self) -> None:
        document = copy.deepcopy(self.valid)
        document["saida"]["estudo"]["campo_classificacao"] = "classificacao_final"
        self.assert_changes(document)

    def test_publication_output_contract_change_changes_fingerprint(self) -> None:
        candidate = self.candidate_with_publication_contract()
        modified = copy.deepcopy(candidate)
        modified["saida"]["publicacao"]["campo_booleano"]["nome"] = "flag_micromodelo_v2"
        self.assert_valid_static(modified)
        self.assertNotEqual(self.fingerprint(candidate), self.fingerprint(modified))

    def test_invalid_mm01_spec_is_refused_before_hashing(self) -> None:
        document = copy.deepcopy(self.valid)
        document["fontes"][0]["catalogo_ref"] = "CATALOGO_NAO_AUTORIZADO"
        with self.assertRaises(mm02.InvalidSpecificationError):
            mm02.calculate_spec_fingerprint(document, self.schema)

    def test_cli_prints_sha256_for_valid_fixture(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT),
                str(FIXTURE),
                "--schema",
                str(SCHEMA),
            ],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("FINGERPRINT_ALGORITHM=mm02-spec-fingerprint-v1", completed.stdout)
        self.assertRegex(completed.stdout, r"SPEC_FINGERPRINT_SHA256=[0-9a-f]{64}")


if __name__ == "__main__":
    unittest.main()
