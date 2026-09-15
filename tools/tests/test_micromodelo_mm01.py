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
        legacy = copy.deepcopy(self.valid)
        legacy["score"]["semantica"] = "risco percentual de ocorrência da característica"
        self.assertIn("SCHEMA", self.codes(legacy))

        calibrated = copy.deepcopy(self.valid)
        calibrated["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"
        calibrated["score"]["semantica_ref"] = "SEM-PROB-001"
        calibrated["score"]["calibracao"] = {
            "metodo": "calibracao_sintetica",
            "evidencia_ref": "exp_001",
            "proveniencia": {
                "status": "MEDIDO",
                "origem": "execucao sintetica",
                "referencia": "CAL-001",
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
                "indeterminado_vira_false": False,
                "regra_ref": None,
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


    def test_previous_published_same_version_cannot_be_rewound(self) -> None:
        previous = copy.deepcopy(self.valid)
        previous["identidade"]["estado"]["fase_anterior"] = "EM_VALIDACAO_GOVERNANCA"
        previous["identidade"]["estado"]["fase_atual"] = "PUBLICADO"
        previous["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "indeterminado_vira_false": False,
                "regra_ref": None,
                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
            },
        }
        previous["publicacao"]["status"] = "PUBLICADA"
        previous["publicacao"]["handoff_ref"] = "handoff-001"
        previous["publicacao"]["produto_dados_ref"] = "produto-001"
        self.assertEqual([], module.validate_spec(previous, self.schema))

        rewritten = copy.deepcopy(self.valid)
        rewritten["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        rewritten["identidade"]["estado"]["fase_atual"] = "EM_ESTUDO"
        rewritten["publicacao"]["status"] = "NAO_INICIADA"
        self.assertIn(
            "STATE_REWIND",
            {issue.code for issue in module.validate_spec(rewritten, self.schema, previous)},
        )

    def test_previous_spec_allows_real_transition_and_rejects_version_rewind(self) -> None:
        previous = copy.deepcopy(self.valid)
        current = copy.deepcopy(self.valid)
        current["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        current["identidade"]["estado"]["fase_atual"] = "CANDIDATO_PRODUTO"
        current["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "indeterminado_vira_false": False,
                "regra_ref": None,
                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
            },
        }
        current["publicacao"]["status"] = "CANDIDATA"
        self.assertEqual([], module.validate_spec(current, self.schema, previous))

        newer_previous = copy.deepcopy(previous)
        newer_previous["identidade"]["micromodel_version"] = "2.0.0"
        self.assertIn(
            "VERSION_REWIND",
            {issue.code for issue in module.validate_spec(current, self.schema, newer_previous)},
        )

    def test_audit_material_references_reject_whitespace_and_invisible_text(self) -> None:
        invisible_marks = ("\u034f", "\ufe0f", "\u0301")
        for mark in invisible_marks:
            with self.subTest(mark=mark, field="approval_por"):
                approved = copy.deepcopy(self.valid)
                approved["validacao"]["aprovacao_humana"]["por"] = mark
                self.assertTrue(
                    {"SCHEMA", "VALIDATION_HUMAN_GATE"} & self.codes(approved)
                )

            with self.subTest(mark=mark, field="approval_ref"):
                approved = copy.deepcopy(self.valid)
                approved["validacao"]["aprovacao_humana"]["referencia"] = mark
                self.assertTrue({"SCHEMA", "VALIDATION_HUMAN_GATE"} & self.codes(approved))

            with self.subTest(mark=mark, field="measurement_ref"):
                measured = copy.deepcopy(self.valid)
                measured["experimentos"][0]["proveniencia"]["medicao"]["referencia_execucao"] = mark
                self.assertTrue({"SCHEMA", "PROV_MEASUREMENT_REQUIRED"} & self.codes(measured))

            with self.subTest(mark=mark, field="product_ref"):
                published = copy.deepcopy(self.valid)
                published["identidade"]["estado"]["fase_anterior"] = "EM_VALIDACAO_GOVERNANCA"
                published["identidade"]["estado"]["fase_atual"] = "PUBLICADO"
                published["saida"]["publicacao"] = {
                    "estado": "DEFINIDO",
                    "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},
                    "politica_indeterminado": {
                        "tratamento": "CAMPO_COBERTURA_SEPARADO",
                        "indeterminado_vira_false": False,
                        "regra_ref": None,
                        "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
                    },
                }
                published["publicacao"]["status"] = "PUBLICADA"
                published["publicacao"]["produto_dados_ref"] = mark
                self.assertTrue({"SCHEMA", "PUBLICATION_GATE"} & self.codes(published))

    def test_proposed_threshold_and_weight_are_allowed_before_validation_gate(self) -> None:
        study = copy.deepcopy(self.valid)
        study["identidade"]["estado"]["fase_anterior"] = "EM_DESCOBERTA"
        study["identidade"]["estado"]["fase_atual"] = "EM_ESTUDO"
        for prov in (
            study["classificacao"]["limiares"][0]["proveniencia"],
            study["score"]["componentes"][0]["proveniencia"],
        ):
            prov["status"] = "PROPOSTO"
            prov["aprovacao"] = None
        codes = self.codes(study)
        self.assertNotIn("THRESHOLD_APPROVAL", codes)
        self.assertNotIn("WEIGHT_APPROVAL", codes)

        formal = copy.deepcopy(study)
        formal["identidade"]["estado"]["fase_anterior"] = "EM_ESTUDO"
        formal["identidade"]["estado"]["fase_atual"] = "EM_VALIDACAO"
        formal_codes = self.codes(formal)
        self.assertIn("THRESHOLD_APPROVAL", formal_codes)
        self.assertIn("WEIGHT_APPROVAL", formal_codes)

    def test_indeterminate_publication_policy_cannot_contradict_false_semantics(self) -> None:
        document = copy.deepcopy(self.valid)
        document["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        document["identidade"]["estado"]["fase_atual"] = "CANDIDATO_PRODUTO"
        document["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "indeterminado_vira_false": False,
                "regra_ref": None,
                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
            },
        }
        document["publicacao"]["status"] = "CANDIDATA"
        self.assertEqual([], module.validate_spec(document, self.schema))

        contradictory = copy.deepcopy(document)
        contradictory["saida"]["publicacao"]["politica_indeterminado"]["descricao"] = (
            "casos INDETERMINADOS retornam FALSE"
        )
        self.assertIn("SCHEMA", self.codes(contradictory))

        contradictory = copy.deepcopy(document)
        contradictory["saida"]["publicacao"]["politica_indeterminado"]["indeterminado_vira_false"] = True
        self.assertIn("SCHEMA", self.codes(contradictory))

    def test_calibration_evidence_ref_must_resolve_to_executed_measured_experiment(self) -> None:
        calibrated = copy.deepcopy(self.valid)
        calibrated["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"
        calibrated["score"]["semantica_ref"] = "SEM-PROB-001"
        calibrated["score"]["calibracao"] = {
            "metodo": "calibracao_sintetica",
            "evidencia_ref": "exp_inexistente",
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
        self.assertIn("CALIBRATION_EVIDENCE_REF", self.codes(calibrated))

    def test_absence_policy_is_structured_and_cannot_hide_false_in_prose(self) -> None:
        contradiction = copy.deepcopy(self.valid)
        contradiction["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] = "FALSE"
        self.assertIn("MISSING_POLICY_CONTRADICTION", self.codes(contradiction))

        legacy_prose = copy.deepcopy(self.valid)
        legacy_prose["classificacao"]["ausencia_evidencia"]["descricao"] = (
            "na ausência de evidência classificar como FALSE"
        )
        self.assertIn("SCHEMA", self.codes(legacy_prose))

        explicit = copy.deepcopy(self.valid)
        explicit["classificacao"]["ausencia_evidencia"]["tratamento"] = "REGRA_EXPLICITA_APROVADA"
        explicit["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] = "FALSE"
        explicit["classificacao"]["ausencia_evidencia"]["regra_ref"] = "REGRA-SEM-EVIDENCIA-001"
        self.assertEqual([], module.validate_spec(explicit, self.schema))

    def test_score_normalization_requires_structured_contract_at_validation(self) -> None:
        legacy = copy.deepcopy(self.valid)
        legacy["score"]["normalizacao"] = "percentual estimado de ocorrência"
        self.assertIn("SCHEMA", self.codes(legacy))

        pending = copy.deepcopy(self.valid)
        pending["score"]["normalizacao"]["metodo"] = "PENDENTE"
        pending["score"]["normalizacao"]["referencia"] = None
        pending["score"]["normalizacao"]["proveniencia"]["status"] = "PROPOSTO"
        pending["score"]["normalizacao"]["proveniencia"]["aprovacao"] = None
        self.assertIn("SCORE_NORMALIZATION", self.codes(pending))

    def test_cli_previous_blocks_rewind(self) -> None:
        previous = copy.deepcopy(self.valid)
        previous["identidade"]["estado"]["fase_anterior"] = "EM_VALIDACAO_GOVERNANCA"
        previous["identidade"]["estado"]["fase_atual"] = "PUBLICADO"
        previous["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "indeterminado_vira_false": False,
                "regra_ref": None,
                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
            },
        }
        previous["publicacao"]["status"] = "PUBLICADA"
        previous["publicacao"]["handoff_ref"] = "handoff-001"
        previous["publicacao"]["produto_dados_ref"] = "produto-001"
        rewritten = copy.deepcopy(self.valid)
        rewritten["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        rewritten["identidade"]["estado"]["fase_atual"] = "EM_ESTUDO"
        with tempfile.TemporaryDirectory() as tmp:
            previous_path = Path(tmp) / "previous.json"
            current_path = Path(tmp) / "current.json"
            previous_path.write_text(json.dumps(previous, ensure_ascii=False), encoding="utf-8")
            current_path.write_text(json.dumps(rewritten, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(CONTRACT),
                    str(current_path),
                    "--schema",
                    str(SCHEMA),
                    "--previous",
                    str(previous_path),
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("STATE_REWIND", result.stdout)


    def test_material_text_unicode_policy_is_shared_by_schema_and_validator(self) -> None:
        positives = ["é", "文档", "١", "देवनागरी", "José", "Jose\u0301"]
        negatives = [
            "\u034f",
            "\ufe0f",
            "\u0301",
            "\u093e",
            "\u20dd",
            "\u200b",
            "\u200c",
            "\u200d",
            "\u2060",
            "   ",
            "\u00a0",
            "\u2003",
            "!!!",
            "€",
            "\u034f\u200b\u0301",
            "\u00a0\u2060!!!\u0301",
        ]

        for value in positives:
            with self.subTest(kind="positive", value=repr(value)):
                document = copy.deepcopy(self.valid)
                document["validacao"]["aprovacao_humana"]["referencia"] = value
                self.assertEqual([], module.validate_spec(document, self.schema))

        for value in negatives:
            with self.subTest(kind="negative", value=repr(value)):
                document = copy.deepcopy(self.valid)
                document["validacao"]["aprovacao_humana"]["referencia"] = value
                self.assertIn("SCHEMA", self.codes(document))

    def test_root_provenance_material_fields_are_guarded(self) -> None:
        negatives = [
            "\u034f",
            "\ufe0f",
            "\u0301",
            "\u093e",
            "\u20dd",
            "\u200b",
            "\u200c",
            "\u200d",
            "\u2060",
            "   ",
            "\u00a0",
            "\u2003",
            "!!!",
            "€",
            "\u034f\u200b\u0301",
        ]
        for field in ("gerado_por", "pedido_original_ref"):
            for value in negatives:
                with self.subTest(field=field, value=repr(value)):
                    document = copy.deepcopy(self.valid)
                    document["proveniencia"][field] = value
                    self.assertIn("SCHEMA", self.codes(document))

        for value in negatives:
            with self.subTest(field="registros.alvo", value=repr(value)):
                document = copy.deepcopy(self.valid)
                document["proveniencia"]["registros"] = [
                    {
                        "alvo": value,
                        "proveniencia": copy.deepcopy(
                            self.valid["classificacao"]["semantica"]["proveniencia"]
                        ),
                    }
                ]
                self.assertIn("SCHEMA", self.codes(document))

        positive = copy.deepcopy(self.valid)
        positive["proveniencia"]["gerado_por"] = "生成器"
        positive["proveniencia"]["pedido_original_ref"] = "文档١"
        positive["proveniencia"]["registros"] = [
            {
                "alvo": "लक्ष्य١",
                "proveniencia": copy.deepcopy(
                    self.valid["classificacao"]["semantica"]["proveniencia"]
                ),
            }
        ]
        self.assertEqual([], module.validate_spec(positive, self.schema))

    def test_material_content_gates_reject_nonmaterial_and_accept_unicode(self) -> None:
        mutations = [
            ("quando_true", lambda d, v: d["classificacao"]["semantica"].__setitem__("quando_true", v)),
            ("quando_false", lambda d, v: d["classificacao"]["semantica"].__setitem__("quando_false", v)),
            ("quando_indeterminado", lambda d, v: d["classificacao"]["semantica"].__setitem__("quando_indeterminado", v)),
            ("validacao.criterios", lambda d, v: d["validacao"].__setitem__("criterios", [v])),
            ("fontes.schema", lambda d, v: d["fontes"][0].__setitem__("schema", v)),
            ("fontes.objeto", lambda d, v: d["fontes"][0].__setitem__("objeto", v)),
            ("fontes.campos", lambda d, v: d["fontes"][0]["campos"].__setitem__(0, v)),
            ("saida.campo_classificacao", lambda d, v: d["saida"]["estudo"].__setitem__("campo_classificacao", v)),
            ("saida.campo_score", lambda d, v: d["saida"]["estudo"].__setitem__("campo_score", v)),
        ]
        representatives = ["   ", "!!!", "€", "\u200b", "\u034f"]
        for field, mutate in mutations:
            for value in representatives:
                with self.subTest(field=field, value=repr(value)):
                    document = copy.deepcopy(self.valid)
                    mutate(document, value)
                    self.assertIn("SCHEMA", self.codes(document))

        unicode_document = copy.deepcopy(self.valid)
        unicode_document["classificacao"]["semantica"]["quando_true"] = "证据充分确认特征"
        unicode_document["classificacao"]["semantica"]["quando_false"] = "证据充分否定特征"
        unicode_document["classificacao"]["semantica"]["quando_indeterminado"] = "जानकारी अपर्याप्त है"
        unicode_document["validacao"]["criterios"] = ["标准一"]
        unicode_document["fontes"][0]["schema"] = "数据域"
        unicode_document["fontes"][0]["objeto"] = "客户视图"
        unicode_document["fontes"][0]["campos"][0] = "字段一"
        unicode_document["saida"]["estudo"]["campo_classificacao"] = "分类"
        unicode_document["saida"]["estudo"]["campo_score"] = "评分"
        self.assertEqual([], module.validate_spec(unicode_document, self.schema))

        publication = copy.deepcopy(self.valid)
        publication["identidade"]["estado"]["fase_anterior"] = "VALIDADO"
        publication["identidade"]["estado"]["fase_atual"] = "CANDIDATO_PRODUTO"
        publication["publicacao"]["status"] = "CANDIDATA"
        publication["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {"nome": "\u200b", "tipo": "BOOLEAN"},
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "indeterminado_vira_false": False,
                "regra_ref": None,
                "proveniencia": copy.deepcopy(
                    self.valid["classificacao"]["semantica"]["proveniencia"]
                ),
            },
        }
        self.assertIn("SCHEMA", self.codes(publication))

        publication["saida"]["publicacao"]["campo_booleano"]["nome"] = "是否具备特征"
        self.assertEqual([], module.validate_spec(publication, self.schema))


if __name__ == "__main__":
    unittest.main()
