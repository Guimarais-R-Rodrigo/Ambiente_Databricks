from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "micromodelo_mm01_contract.py"
SCHEMA = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
TEMPLATE = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.template.yaml"
VALID = ROOT / "tools" / "tests" / "fixtures" / "micromodelos_mm01" / "valido_validado.json"
INVALID = ROOT / "tools" / "tests" / "fixtures" / "micromodelos_mm01" / "casos_invalidos.json"
TESTS = ROOT / "tools" / "tests" / "test_micromodelo_mm01.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1 match, encontrado {count}")
    return text.replace(old, new, 1)


def replace_method(text: str, method_name: str, next_method_name: str, new_body: str) -> str:
    start = text.index(f"    def {method_name}(")
    end = text.index(f"    def {next_method_name}(", start)
    return text[:start] + new_body.rstrip() + "\n\n" + text[end:]


# ---------------------------------------------------------------------------
# Validator: texto material positivo, políticas estruturadas e score sem prosa normativa
# ---------------------------------------------------------------------------
text = VALIDATOR.read_text(encoding="utf-8")
start = text.index("def _uses_probability_language(")
end = text.index("def _validate_previous_state(", start)
helpers = '''def _has_material_text(value: Any) -> bool:\n    \"\"\"Exige ao menos uma letra ou número Unicode após normalização.\n\n    Marcas combinantes, variation selectors, espaços, controles e pontuação\n    isolada não constituem identidade/referência auditável.\n    \"\"\"\n    if not isinstance(value, str):\n        return False\n    normalized = unicodedata.normalize(\"NFKC\", value)\n    return any(unicodedata.category(char)[0] in {\"L\", \"N\"} for char in normalized)\n\n\ndef _semver_tuple(value: str) -> tuple[int, int, int]:\n    match = re.fullmatch(r\"(\\d+)\\.(\\d+)\\.(\\d+)\", value)\n    if not match:\n        raise ValueError(f\"versão semântica inválida: {value!r}\")\n    return tuple(int(part) for part in match.groups())\n\n\n'''
text = text[:start] + helpers + text[end:]

old_absence = '''    if (\n        absence[\"tratamento\"] == \"REGRA_EXPLICITA_APROVADA\"\n        and absence[\"proveniencia\"][\"status\"] != \"APROVADO\"\n    ):\n        issues.append(\n            Issue(\n                \"classificacao.ausencia_evidencia.proveniencia.status\",\n                \"MISSING_POLICY_APPROVAL\",\n                \"REGRA_EXPLICITA_APROVADA exige proveniência APROVADO\",\n            )\n        )\n'''
new_absence = '''    if absence[\"tratamento\"] == \"INDETERMINADO\":\n        if (\n            absence[\"resultado_sem_evidencia\"] != \"INDETERMINADO\"\n            or absence[\"regra_ref\"] is not None\n        ):\n            issues.append(\n                Issue(\n                    \"classificacao.ausencia_evidencia\",\n                    \"MISSING_POLICY_CONTRADICTION\",\n                    \"tratamento INDETERMINADO exige resultado_sem_evidencia=INDETERMINADO e regra_ref=null\",\n                )\n            )\n    else:\n        if absence[\"proveniencia\"][\"status\"] != \"APROVADO\":\n            issues.append(\n                Issue(\n                    \"classificacao.ausencia_evidencia.proveniencia.status\",\n                    \"MISSING_POLICY_APPROVAL\",\n                    \"REGRA_EXPLICITA_APROVADA exige proveniência APROVADO\",\n                )\n            )\n        if not _has_material_text(absence[\"regra_ref\"]):\n            issues.append(\n                Issue(\n                    \"classificacao.ausencia_evidencia.regra_ref\",\n                    \"MISSING_POLICY_RULE_REF\",\n                    \"REGRA_EXPLICITA_APROVADA exige referência auditável para a regra\",\n                )\n            )\n'''
text = replace_once(text, old_absence, new_absence, "absence policy")

score_start = text.index('    experiment_by_id = {item["id"]: item for item in spec["experimentos"]}')
score_end = text.index('    _check_duplicate_ids(spec["experimentos"], "experimentos", issues)', score_start)
score_block = '''    experiment_by_id = {item[\"id\"]: item for item in spec[\"experimentos\"]}\n\n    score = spec[\"score\"]\n    _validate_provenance(score[\"proveniencia\"], \"score.proveniencia\", issues)\n    _check_duplicate_ids(score[\"componentes\"], \"score.componentes\", issues)\n    if score[\"habilitado\"]:\n        if not score[\"tipo_semantica\"]:\n            issues.append(\n                Issue(\n                    \"score.tipo_semantica\",\n                    \"SCORE_SEMANTICS\",\n                    \"score habilitado exige tipo_semantica estruturado\",\n                )\n            )\n        if (\n            not isinstance(score[\"escala\"], dict)\n            or score[\"escala\"].get(\"min\") != 0\n            or score[\"escala\"].get(\"max\") != 100\n        ):\n            issues.append(\n                Issue(\n                    \"score.escala\",\n                    \"SCORE_SCALE\",\n                    \"score habilitado neste contrato precisa usar escala 0–100\",\n                )\n            )\n        if spec[\"saida\"][\"estudo\"][\"campo_score\"] in (None, \"\"):\n            issues.append(\n                Issue(\n                    \"saida.estudo.campo_score\",\n                    \"SCORE_OUTPUT\",\n                    \"score habilitado exige campo_score no contrato de estudo\",\n                )\n            )\n\n        normalization = score[\"normalizacao\"]\n        if isinstance(normalization, dict):\n            _validate_provenance(\n                normalization[\"proveniencia\"],\n                \"score.normalizacao.proveniencia\",\n                issues,\n            )\n\n        for index, component in enumerate(score[\"componentes\"]):\n            _validate_provenance(\n                component[\"proveniencia\"],\n                f\"score.componentes[{index}].proveniencia\",\n                issues,\n            )\n            if (\n                FASE_ORDEM[phase] >= FASE_ORDEM[\"EM_VALIDACAO\"]\n                and component[\"proveniencia\"][\"status\"] != \"APROVADO\"\n            ):\n                issues.append(\n                    Issue(\n                        f\"score.componentes[{index}].proveniencia.status\",\n                        \"WEIGHT_APPROVAL\",\n                        \"peso material exige decisão humana APROVADO\",\n                    )\n                )\n\n        if FASE_ORDEM[phase] >= FASE_ORDEM[\"EM_VALIDACAO\"]:\n            if not _has_material_text(score[\"semantica_ref\"]):\n                issues.append(\n                    Issue(\n                        \"score.semantica_ref\",\n                        \"SCORE_SEMANTICS\",\n                        \"EM_VALIDACAO ou posterior exige referência auditável da semântica do score\",\n                    )\n                )\n            if not isinstance(normalization, dict) or normalization[\"metodo\"] == \"PENDENTE\":\n                issues.append(\n                    Issue(\n                        \"score.normalizacao\",\n                        \"SCORE_NORMALIZATION\",\n                        \"EM_VALIDACAO ou posterior exige método estruturado de normalização\",\n                    )\n                )\n            elif normalization[\"proveniencia\"][\"status\"] != \"APROVADO\":\n                issues.append(\n                    Issue(\n                        \"score.normalizacao.proveniencia.status\",\n                        \"SCORE_NORMALIZATION_APPROVAL\",\n                        \"normalização material exige decisão humana APROVADO\",\n                    )\n                )\n            if (\n                isinstance(normalization, dict)\n                and normalization[\"metodo\"] == \"CUSTOM_APROVADO\"\n                and not _has_material_text(normalization[\"referencia\"])\n            ):\n                issues.append(\n                    Issue(\n                        \"score.normalizacao.referencia\",\n                        \"SCORE_NORMALIZATION_REF\",\n                        \"CUSTOM_APROVADO exige referência auditável da regra de normalização\",\n                    )\n                )\n\n        if score[\"tipo_semantica\"] == \"PROBABILIDADE_CALIBRADA\":\n            if not isinstance(score[\"calibracao\"], dict):\n                issues.append(\n                    Issue(\n                        \"score.calibracao\",\n                        \"CALIBRATION_REQUIRED\",\n                        \"PROBABILIDADE_CALIBRADA exige bloco calibracao\",\n                    )\n                )\n            else:\n                _validate_provenance(\n                    score[\"calibracao\"][\"proveniencia\"],\n                    \"score.calibracao.proveniencia\",\n                    issues,\n                )\n                if score[\"calibracao\"][\"proveniencia\"][\"status\"] != \"MEDIDO\":\n                    issues.append(\n                        Issue(\n                            \"score.calibracao.proveniencia.status\",\n                            \"CALIBRATION_EVIDENCE\",\n                            \"probabilidade só pode ser declarada com calibração MEDIDA\",\n                        )\n                    )\n                evidence_ref = score[\"calibracao\"][\"evidencia_ref\"]\n                referenced_experiment = experiment_by_id.get(evidence_ref)\n                if referenced_experiment is None:\n                    issues.append(\n                        Issue(\n                            \"score.calibracao.evidencia_ref\",\n                            \"CALIBRATION_EVIDENCE_REF\",\n                            \"evidencia_ref deve apontar para experimentos[].id existente\",\n                        )\n                    )\n                elif (\n                    referenced_experiment[\"status\"] != \"EXECUTADO\"\n                    or referenced_experiment[\"proveniencia\"][\"status\"] != \"MEDIDO\"\n                ):\n                    issues.append(\n                        Issue(\n                            \"score.calibracao.evidencia_ref\",\n                            \"CALIBRATION_EVIDENCE_REF\",\n                            \"calibração exige experimento EXECUTADO com proveniência MEDIDO\",\n                        )\n                    )\n        elif score[\"calibracao\"] is not None:\n            issues.append(\n                Issue(\n                    \"score.calibracao\",\n                    \"CALIBRATION_UNEXPECTED\",\n                    \"calibração probabilística só é permitida para PROBABILIDADE_CALIBRADA\",\n                )\n            )\n    else:\n        if any(\n            (\n                score[\"tipo_semantica\"] is not None,\n                score[\"semantica_ref\"] is not None,\n                score[\"escala\"] is not None,\n                score[\"normalizacao\"] is not None,\n                score[\"componentes\"],\n                score[\"calibracao\"] is not None,\n            )\n        ):\n            issues.append(\n                Issue(\n                    \"score\",\n                    \"SCORE_DISABLED\",\n                    \"score desabilitado deve manter semântica, escala, normalização, componentes e calibração vazios/nulos\",\n                )\n            )\n        if spec[\"saida\"][\"estudo\"][\"campo_score\"] is not None:\n            issues.append(\n                Issue(\n                    \"saida.estudo.campo_score\",\n                    \"SCORE_DISABLED\",\n                    \"score desabilitado exige campo_score=null\",\n                )\n            )\n\n'''
text = text[:score_start] + score_block + text[score_end:]

old_policy = '''            policy = publication_output[\"politica_indeterminado\"]\n            if policy[\"indeterminado_vira_false\"] is not False:\n                issues.append(\n                    Issue(\n                        \"saida.publicacao.politica_indeterminado.indeterminado_vira_false\",\n                        \"INDETERMINATE_FALSE_POLICY\",\n                        \"INDETERMINADO nunca pode ser implicitamente convertido em FALSE\",\n                    )\n                )\n            if _description_maps_indeterminate_to_false(policy[\"descricao\"]):\n                issues.append(\n                    Issue(\n                        \"saida.publicacao.politica_indeterminado.descricao\",\n                        \"INDETERMINATE_POLICY_CONTRADICTION\",\n                        \"descricao contradiz a regra estruturada que preserva INDETERMINADO distinto de FALSE\",\n                    )\n                )\n'''
new_policy = '''            policy = publication_output[\"politica_indeterminado\"]\n            if policy[\"indeterminado_vira_false\"] is not False:\n                issues.append(\n                    Issue(\n                        \"saida.publicacao.politica_indeterminado.indeterminado_vira_false\",\n                        \"INDETERMINATE_FALSE_POLICY\",\n                        \"INDETERMINADO nunca pode ser implicitamente convertido em FALSE\",\n                    )\n                )\n            if policy[\"tratamento\"] == \"OUTRA_APROVADA\":\n                if not _has_material_text(policy[\"regra_ref\"]):\n                    issues.append(\n                        Issue(\n                            \"saida.publicacao.politica_indeterminado.regra_ref\",\n                            \"PUBLICATION_POLICY_RULE_REF\",\n                            \"OUTRA_APROVADA exige referência auditável da regra externa\",\n                        )\n                    )\n            elif policy[\"regra_ref\"] is not None:\n                issues.append(\n                    Issue(\n                        \"saida.publicacao.politica_indeterminado.regra_ref\",\n                        \"PUBLICATION_POLICY_RULE_REF\",\n                        \"regra_ref só é usada quando tratamento=OUTRA_APROVADA\",\n                    )\n                )\n'''
text = replace_once(text, old_policy, new_policy, "publication policy")
VALIDATOR.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Schema: referências auditáveis e comportamento sem prosa normativa
# ---------------------------------------------------------------------------
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
defs = schema["$defs"]
defs["material_ref"] = {
    "type": "string",
    "minLength": 1,
    "pattern": ".*[A-Za-z0-9].*",
    "description": "Referência auditável com ao menos um caractere alfanumérico ASCII; validação semântica aplica regra Unicode adicional.",
}
defs["material_ref_nullable"] = {
    "anyOf": [
        {"$ref": "#/$defs/material_ref"},
        {"type": "null"},
    ]
}

prov = defs["proveniencia"]["properties"]
prov["referencia"] = {"$ref": "#/$defs/material_ref_nullable"}
prov["aprovacao"]["properties"]["referencia"] = {"$ref": "#/$defs/material_ref"}
prov["medicao"]["properties"]["referencia_execucao"] = {"$ref": "#/$defs/material_ref"}

absence = schema["properties"]["classificacao"]["properties"]["ausencia_evidencia"]
absence["required"] = ["tratamento", "resultado_sem_evidencia", "regra_ref", "proveniencia"]
absence["properties"].pop("descricao", None)
absence["properties"]["resultado_sem_evidencia"] = {
    "enum": ["TRUE", "FALSE", "INDETERMINADO"],
    "description": "Resultado estruturado aplicável quando não há evidência suficiente.",
}
absence["properties"]["regra_ref"] = {"$ref": "#/$defs/material_ref_nullable"}

score = schema["properties"]["score"]
score["required"] = [
    "habilitado",
    "tipo_semantica",
    "semantica_ref",
    "escala",
    "normalizacao",
    "componentes",
    "calibracao",
    "proveniencia",
]
score["properties"].pop("semantica", None)
score["properties"]["semantica_ref"] = {"$ref": "#/$defs/material_ref_nullable"}
score["properties"]["normalizacao"] = {
    "type": ["object", "null"],
    "additionalProperties": False,
    "properties": {
        "metodo": {
            "enum": [
                "PENDENTE",
                "SOMA_PONDERADA_0_100",
                "MIN_MAX_0_100",
                "LINEAR_0_100",
                "CUSTOM_APROVADO",
            ]
        },
        "referencia": {"$ref": "#/$defs/material_ref_nullable"},
        "proveniencia": {"$ref": "#/$defs/proveniencia"},
    },
    "required": ["metodo", "referencia", "proveniencia"],
}
score["properties"]["calibracao"]["properties"]["evidencia_ref"] = {"$ref": "#/$defs/material_ref"}

validation_approval = schema["properties"]["validacao"]["properties"]["aprovacao_humana"]["properties"]
validation_approval["referencia"] = {"$ref": "#/$defs/material_ref_nullable"}

policy = schema["properties"]["saida"]["properties"]["publicacao"]["properties"]["politica_indeterminado"]
policy["required"] = ["tratamento", "indeterminado_vira_false", "regra_ref", "proveniencia"]
policy["properties"].pop("descricao", None)
policy["properties"]["regra_ref"] = {"$ref": "#/$defs/material_ref_nullable"}

publication = schema["properties"]["publicacao"]["properties"]
publication["handoff_ref"] = {"$ref": "#/$defs/material_ref_nullable"}
publication["produto_dados_ref"] = {"$ref": "#/$defs/material_ref_nullable"}

SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Template e fixture positivo
# ---------------------------------------------------------------------------
template = TEMPLATE.read_text(encoding="utf-8")
template = replace_once(
    template,
    '  ausencia_evidencia:\n    tratamento: "INDETERMINADO"\n    descricao: "ausência de evidência não é convertida automaticamente em FALSE"\n',
    '  ausencia_evidencia:\n    tratamento: "INDETERMINADO"\n    resultado_sem_evidencia: "INDETERMINADO"\n    regra_ref: null\n',
    "template absence",
)
template = replace_once(
    template,
    '  tipo_semantica: "FORCA_EVIDENCIA"\n  semantica: "intensidade relativa da evidência observada; não é probabilidade calibrada"\n',
    '  tipo_semantica: "FORCA_EVIDENCIA"\n  semantica_ref: null\n',
    "template score semantics",
)
template = replace_once(
    template,
    '  normalizacao: "combinação ainda a aprovar; nenhum peso foi definido neste template"\n',
    '  normalizacao:\n    metodo: "PENDENTE"\n    referencia: null\n    proveniencia:\n      status: "PROPOSTO"\n      origem: "template MM01"\n      referencia: null\n      observado_em_utc: null\n      aprovacao: null\n      medicao: null\n',
    "template normalization",
)
TEMPLATE.write_text(template, encoding="utf-8")

valid = json.loads(VALID.read_text(encoding="utf-8"))
absence_valid = valid["classificacao"]["ausencia_evidencia"]
absence_valid.pop("descricao", None)
absence_valid["resultado_sem_evidencia"] = "INDETERMINADO"
absence_valid["regra_ref"] = None
score_valid = valid["score"]
score_valid.pop("semantica", None)
score_valid["semantica_ref"] = "SEM-001"
score_valid["normalizacao"] = {
    "metodo": "SOMA_PONDERADA_0_100",
    "referencia": "NORM-001",
    "proveniencia": copy.deepcopy(score_valid["proveniencia"]),
}
VALID.write_text(json.dumps(valid, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

invalid = json.loads(INVALID.read_text(encoding="utf-8"))
for case in invalid:
    if case["nome"] == "score_sem_semantica":
        case["operacoes"] = [
            {
                "acao": "set",
                "path": ["score", "semantica_ref"],
                "value": None,
            }
        ]
INVALID.write_text(json.dumps(invalid, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Testes: atualizar políticas e fechar os três bypasses da segunda A1
# ---------------------------------------------------------------------------
tests = TESTS.read_text(encoding="utf-8")
# Todas as políticas de publicação construídas pela suíte deixam de carregar prosa normativa.
tests = tests.replace(
    '                "descricao": "preservar casos indeterminados em cobertura separada",\n',
    '                "regra_ref": None,\n',
)
tests = tests.replace(
    '                "descricao": "publicar cobertura separada para preservar casos indeterminados",\n',
    '                "regra_ref": None,\n',
)

probability_method = '''    def test_probability_language_requires_calibrated_semantics(self) -> None:\n        legacy = copy.deepcopy(self.valid)\n        legacy["score"]["semantica"] = "risco percentual de ocorrência da característica"\n        self.assertIn("SCHEMA", self.codes(legacy))\n\n        calibrated = copy.deepcopy(self.valid)\n        calibrated["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"\n        calibrated["score"]["semantica_ref"] = "SEM-PROB-001"\n        calibrated["score"]["calibracao"] = {\n            "metodo": "calibracao_sintetica",\n            "evidencia_ref": "exp_001",\n            "proveniencia": {\n                "status": "MEDIDO",\n                "origem": "execucao sintetica",\n                "referencia": "CAL-001",\n                "observado_em_utc": "2026-09-14T13:30:00Z",\n                "aprovacao": None,\n                "medicao": {\n                    "referencia_execucao": "run-calibracao-001",\n                    "medido_em_utc": "2026-09-14T13:30:00Z",\n                },\n            },\n        }\n        self.assertEqual([], module.validate_spec(calibrated, self.schema))\n\n'''
tests = replace_method(
    tests,
    "test_probability_language_requires_calibrated_semantics",
    "test_duplicate_ids_are_rejected_in_components_and_experiments",
    probability_method,
)

indeterminate_method = '''    def test_indeterminate_publication_policy_cannot_contradict_false_semantics(self) -> None:\n        document = copy.deepcopy(self.valid)\n        document["identidade"]["estado"]["fase_anterior"] = "VALIDADO"\n        document["identidade"]["estado"]["fase_atual"] = "CANDIDATO_PRODUTO"\n        document["saida"]["publicacao"] = {\n            "estado": "DEFINIDO",\n            "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},\n            "politica_indeterminado": {\n                "tratamento": "CAMPO_COBERTURA_SEPARADO",\n                "indeterminado_vira_false": False,\n                "regra_ref": None,\n                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),\n            },\n        }\n        document["publicacao"]["status"] = "CANDIDATA"\n        self.assertEqual([], module.validate_spec(document, self.schema))\n\n        contradictory = copy.deepcopy(document)\n        contradictory["saida"]["publicacao"]["politica_indeterminado"]["descricao"] = (\n            "casos INDETERMINADOS retornam FALSE"\n        )\n        self.assertIn("SCHEMA", self.codes(contradictory))\n\n        contradictory = copy.deepcopy(document)\n        contradictory["saida"]["publicacao"]["politica_indeterminado"]["indeterminado_vira_false"] = True\n        self.assertIn("SCHEMA", self.codes(contradictory))\n\n'''
tests = replace_method(
    tests,
    "test_indeterminate_publication_policy_cannot_contradict_false_semantics",
    "test_calibration_evidence_ref_must_resolve_to_executed_measured_experiment",
    indeterminate_method,
)

# A calibração deixa de editar campo textual removido.
tests = tests.replace(
    '        calibrated["score"]["semantica"] = "probabilidade calibrada da característica"\n',
    '        calibrated["score"]["semantica_ref"] = "SEM-PROB-001"\n',
)

# O teste de referências auditáveis passa a cobrir marcas Unicode Mn em todos os gates materiais.
audit_start = tests.index("    def test_audit_material_references_reject_whitespace_and_invisible_text(")
audit_end = tests.index("    def test_proposed_threshold_and_weight_are_allowed_before_validation_gate(", audit_start)
audit_method = '''    def test_audit_material_references_reject_whitespace_and_invisible_text(self) -> None:\n        invisible_marks = ("\\u034f", "\\ufe0f", "\\u0301")\n        for mark in invisible_marks:\n            with self.subTest(mark=mark, field="approval_por"):\n                approved = copy.deepcopy(self.valid)\n                approved["validacao"]["aprovacao_humana"]["por"] = mark\n                self.assertIn("VALIDATION_HUMAN_GATE", self.codes(approved))\n\n            with self.subTest(mark=mark, field="approval_ref"):\n                approved = copy.deepcopy(self.valid)\n                approved["validacao"]["aprovacao_humana"]["referencia"] = mark\n                self.assertTrue({"SCHEMA", "VALIDATION_HUMAN_GATE"} & self.codes(approved))\n\n            with self.subTest(mark=mark, field="measurement_ref"):\n                measured = copy.deepcopy(self.valid)\n                measured["experimentos"][0]["proveniencia"]["medicao"]["referencia_execucao"] = mark\n                self.assertTrue({"SCHEMA", "PROV_MEASUREMENT_REQUIRED"} & self.codes(measured))\n\n            with self.subTest(mark=mark, field="product_ref"):\n                published = copy.deepcopy(self.valid)\n                published["identidade"]["estado"]["fase_anterior"] = "EM_VALIDACAO_GOVERNANCA"\n                published["identidade"]["estado"]["fase_atual"] = "PUBLICADO"\n                published["saida"]["publicacao"] = {\n                    "estado": "DEFINIDO",\n                    "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},\n                    "politica_indeterminado": {\n                        "tratamento": "CAMPO_COBERTURA_SEPARADO",\n                        "indeterminado_vira_false": False,\n                        "regra_ref": None,\n                        "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),\n                    },\n                }\n                published["publicacao"]["status"] = "PUBLICADA"\n                published["publicacao"]["produto_dados_ref"] = mark\n                self.assertTrue({"SCHEMA", "PUBLICATION_GATE"} & self.codes(published))\n\n'''
tests = tests[:audit_start] + audit_method + tests[audit_end:]

extra_methods = '''    def test_absence_policy_is_structured_and_cannot_hide_false_in_prose(self) -> None:\n        contradiction = copy.deepcopy(self.valid)\n        contradiction["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] = "FALSE"\n        self.assertIn("MISSING_POLICY_CONTRADICTION", self.codes(contradiction))\n\n        legacy_prose = copy.deepcopy(self.valid)\n        legacy_prose["classificacao"]["ausencia_evidencia"]["descricao"] = (\n            "na ausência de evidência classificar como FALSE"\n        )\n        self.assertIn("SCHEMA", self.codes(legacy_prose))\n\n        explicit = copy.deepcopy(self.valid)\n        explicit["classificacao"]["ausencia_evidencia"]["tratamento"] = "REGRA_EXPLICITA_APROVADA"\n        explicit["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] = "FALSE"\n        explicit["classificacao"]["ausencia_evidencia"]["regra_ref"] = "REGRA-SEM-EVIDENCIA-001"\n        self.assertEqual([], module.validate_spec(explicit, self.schema))\n\n    def test_score_normalization_requires_structured_contract_at_validation(self) -> None:\n        legacy = copy.deepcopy(self.valid)\n        legacy["score"]["normalizacao"] = "percentual estimado de ocorrência"\n        self.assertIn("SCHEMA", self.codes(legacy))\n\n        pending = copy.deepcopy(self.valid)\n        pending["score"]["normalizacao"]["metodo"] = "PENDENTE"\n        pending["score"]["normalizacao"]["referencia"] = None\n        pending["score"]["normalizacao"]["proveniencia"]["status"] = "PROPOSTO"\n        pending["score"]["normalizacao"]["proveniencia"]["aprovacao"] = None\n        self.assertIn("SCORE_NORMALIZATION", self.codes(pending))\n\n'''
insert_at = tests.index("    def test_cli_previous_blocks_rewind(")
tests = tests[:insert_at] + extra_methods + tests[insert_at:]
TESTS.write_text(tests, encoding="utf-8")

print("MM01 segunda A1: patch aplicado")
