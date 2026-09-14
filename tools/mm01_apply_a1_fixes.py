from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "micromodelo_mm01_contract.py"
SCHEMA = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
TESTS = ROOT / "tools" / "tests" / "test_micromodelo_mm01.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1 match, encontrado {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# Validador semântico
# ---------------------------------------------------------------------------
text = VALIDATOR.read_text(encoding="utf-8")

marker = "\ndef _validate_provenance(prov: dict[str, Any], path: str, issues: list[Issue]) -> None:\n"
helpers = r'''
def _has_material_text(value: Any) -> bool:
    """True apenas quando há conteúdo auditável além de espaço/controle/formatação."""
    if not isinstance(value, str):
        return False
    normalized = unicodedata.normalize("NFKC", value)
    visible = "".join(
        char
        for char in normalized
        if unicodedata.category(char)[0] not in {"Z", "C"}
    )
    return bool(visible.strip())


def _semver_tuple(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if not match:
        raise ValueError(f"versão semântica inválida: {value!r}")
    return tuple(int(part) for part in match.groups())


def _description_maps_indeterminate_to_false(value: str) -> bool:
    normalized = _normalize_semantic_text(value)
    if not re.search(r"\bindetermin\w*\b", normalized):
        return False
    if not re.search(r"\b(?:false|falso)\b", normalized):
        return False
    if re.search(r"\bnao\b.{0,60}\b(?:false|falso)\b", normalized):
        return False
    return bool(
        re.search(
            r"\b(?:grav\w*|convert\w*|mape\w*|trat\w*|registr\w*|defin\w*|vira\w*|equival\w*)\b",
            normalized,
        )
    )


def _validate_previous_state(
    spec: dict[str, Any], previous_spec: dict[str, Any], issues: list[Issue]
) -> None:
    current_identity = spec["identidade"]
    previous_identity = previous_spec["identidade"]
    if current_identity["nome"] != previous_identity["nome"]:
        issues.append(
            Issue(
                "identidade.nome",
                "PREVIOUS_IDENTITY_MISMATCH",
                "a especificação anterior precisa pertencer ao mesmo micromodelo",
            )
        )
        return

    current_version = _semver_tuple(current_identity["micromodel_version"])
    previous_version = _semver_tuple(previous_identity["micromodel_version"])
    if current_version < previous_version:
        issues.append(
            Issue(
                "identidade.micromodel_version",
                "VERSION_REWIND",
                "micromodel_version não pode regredir em relação à especificação anterior",
            )
        )
        return

    # Uma nova versão material inicia seu próprio ciclo; MM02 ainda cuidará do fingerprint.
    if current_version > previous_version:
        return

    current_state = current_identity["estado"]
    previous_state = previous_identity["estado"]
    current_phase = current_state["fase_atual"]
    previous_phase = previous_state["fase_atual"]

    if current_phase == previous_phase:
        if current_state["fase_anterior"] != previous_state["fase_anterior"]:
            issues.append(
                Issue(
                    "identidade.estado.fase_anterior",
                    "PREVIOUS_HISTORY_REWRITE",
                    "a mesma versão não pode reescrever fase_anterior sem mudar de fase",
                )
            )
        return

    if previous_phase == "PUBLICADO":
        issues.append(
            Issue(
                "identidade.estado.fase_atual",
                "STATE_REWIND",
                "uma versão já PUBLICADA não pode voltar a fase anterior; crie versão material superior",
            )
        )
        return

    if current_state["fase_anterior"] != previous_phase:
        issues.append(
            Issue(
                "identidade.estado.fase_anterior",
                "PREVIOUS_STATE_MISMATCH",
                f"fase_anterior deve refletir a fase observada na especificação anterior: {previous_phase}",
            )
        )
        return

    if (previous_phase, current_phase) not in TRANSICOES_FASE:
        issues.append(
            Issue(
                "identidade.estado",
                "STATE_TRANSITION",
                f"transição observada {previous_phase!r} -> {current_phase!r} não é permitida",
            )
        )

'''
text = replace_once(text, marker, "\n" + helpers + marker.lstrip("\n"), "insert helpers")

start = text.index("def _validate_provenance(")
end = text.index("\n\ndef _check_duplicate_ids", start)
new_prov = r'''def _validate_provenance(prov: dict[str, Any], path: str, issues: list[Issue]) -> None:
    status = prov.get("status")
    approval = prov.get("aprovacao")
    measurement = prov.get("medicao")

    if not _has_material_text(prov.get("origem")):
        issues.append(Issue(f"{path}.origem", "PROV_ORIGIN_REQUIRED", "origem precisa ter conteúdo auditável"))
    if prov.get("referencia") is not None and not _has_material_text(prov.get("referencia")):
        issues.append(Issue(f"{path}.referencia", "PROV_REFERENCE_BLANK", "referencia não pode ser vazia/whitespace"))

    if status == "APROVADO":
        if not isinstance(approval, dict):
            issues.append(
                Issue(path, "PROV_APPROVAL_REQUIRED", "APROVADO exige bloco aprovacao completo")
            )
        elif not (
            _has_material_text(approval.get("por"))
            and _has_material_text(approval.get("referencia"))
        ):
            issues.append(
                Issue(
                    f"{path}.aprovacao",
                    "PROV_APPROVAL_REQUIRED",
                    "APROVADO exige por/referencia com conteúdo auditável",
                )
            )
    elif approval is not None:
        issues.append(
            Issue(path, "PROV_APPROVAL_MISMATCH", "aprovacao só é permitida quando status=APROVADO")
        )

    if status == "MEDIDO":
        if not isinstance(measurement, dict):
            issues.append(
                Issue(
                    path,
                    "PROV_MEASUREMENT_REQUIRED",
                    "MEDIDO exige medicao com referencia_execucao e medido_em_utc",
                )
            )
        elif not _has_material_text(measurement.get("referencia_execucao")):
            issues.append(
                Issue(
                    f"{path}.medicao.referencia_execucao",
                    "PROV_MEASUREMENT_REQUIRED",
                    "MEDIDO exige referencia_execucao com conteúdo auditável",
                )
            )
    elif measurement is not None:
        issues.append(
            Issue(path, "PROV_MEASUREMENT_MISMATCH", "medicao só é permitida quando status=MEDIDO")
        )'''
text = text[:start] + new_prov + text[end:]

text = replace_once(
    text,
    "def validate_spec(spec: dict[str, Any], schema: dict[str, Any]) -> list[Issue]:",
    "def validate_spec(\n    spec: dict[str, Any],\n    schema: dict[str, Any],\n    previous_spec: dict[str, Any] | None = None,\n) -> list[Issue]:",
    "validate signature",
)

old = '''    if issues:\n        return issues\n\n    estado = spec["identidade"]["estado"]\n    transition = (estado["fase_anterior"], estado["fase_atual"])'''
new = '''    if issues:\n        return issues\n\n    if previous_spec is not None:\n        previous_issues = validate_spec(previous_spec, schema)\n        if previous_issues:\n            issues.append(\n                Issue(\n                    "$previous",\n                    "PREVIOUS_SPEC_INVALID",\n                    "a especificação anterior fornecida também precisa ser válida no contrato MM01",\n                )\n            )\n            return issues\n        _validate_previous_state(spec, previous_spec, issues)\n\n    estado = spec["identidade"]["estado"]\n    phase = estado["fase_atual"]\n    transition = (estado["fase_anterior"], estado["fase_atual"])'''
text = replace_once(text, old, new, "previous validation")

text = replace_once(
    text,
    '''        if threshold["proveniencia"]["status"] != "APROVADO":''',
    '''        if (\n            FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]\n            and threshold["proveniencia"]["status"] != "APROVADO"\n        ):''',
    "threshold gate",
)
text = replace_once(
    text,
    '''            if component["proveniencia"]["status"] != "APROVADO":''',
    '''            if (\n                FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]\n                and component["proveniencia"]["status"] != "APROVADO"\n            ):''',
    "weight gate",
)

text = replace_once(
    text,
    '''    score = spec["score"]\n    _validate_provenance(score["proveniencia"], "score.proveniencia", issues)''',
    '''    experiment_by_id = {item["id"]: item for item in spec["experimentos"]}\n\n    score = spec["score"]\n    _validate_provenance(score["proveniencia"], "score.proveniencia", issues)''',
    "experiment index",
)

needle = '''                if score["calibracao"]["proveniencia"]["status"] != "MEDIDO":\n                    issues.append(\n                        Issue(\n                            "score.calibracao.proveniencia.status",\n                            "CALIBRATION_EVIDENCE",\n                            "probabilidade só pode ser declarada com calibração MEDIDA",\n                        )\n                    )'''
replacement = needle + '''\n                evidence_ref = score["calibracao"]["evidencia_ref"]\n                referenced_experiment = experiment_by_id.get(evidence_ref)\n                if referenced_experiment is None:\n                    issues.append(\n                        Issue(\n                            "score.calibracao.evidencia_ref",\n                            "CALIBRATION_EVIDENCE_REF",\n                            "evidencia_ref deve apontar para experimentos[].id existente",\n                        )\n                    )\n                elif (\n                    referenced_experiment["status"] != "EXECUTADO"\n                    or referenced_experiment["proveniencia"]["status"] != "MEDIDO"\n                ):\n                    issues.append(\n                        Issue(\n                            "score.calibracao.evidencia_ref",\n                            "CALIBRATION_EVIDENCE_REF",\n                            "calibração exige experimento EXECUTADO com proveniência MEDIDO",\n                        )\n                    )'''
text = replace_once(text, needle, replacement, "calibration ref")

old = '''        if approval["status"] != validation["status"] or not all(\n            approval.get(k) for k in ("por", "em_utc", "referencia")\n        ):'''
new = '''        if (\n            approval["status"] != validation["status"]\n            or not _has_material_text(approval.get("por"))\n            or not approval.get("em_utc")\n            or not _has_material_text(approval.get("referencia"))\n        ):'''
text = replace_once(text, old, new, "human approval blank")

# A atribuição repetida de phase é inofensiva, mas removemos para manter uma única fonte local.
text = replace_once(text, '    phase = estado["fase_atual"]\n    if FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]:', '    if FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]:', "phase duplicate")

needle = '''            if (\n                publication_output["politica_indeterminado"]["proveniencia"]["status"]\n                != "APROVADO"\n            ):\n                issues.append(\n                    Issue(\n                        "saida.publicacao.politica_indeterminado.proveniencia.status",\n                        "PUBLICATION_OUTPUT_APPROVAL",\n                        "tratamento de INDETERMINADO na publicação exige APROVADO",\n                    )\n                )'''
replacement = needle + '''\n            policy = publication_output["politica_indeterminado"]\n            if policy["indeterminado_vira_false"] is not False:\n                issues.append(\n                    Issue(\n                        "saida.publicacao.politica_indeterminado.indeterminado_vira_false",\n                        "INDETERMINATE_FALSE_POLICY",\n                        "INDETERMINADO nunca pode ser implicitamente convertido em FALSE",\n                    )\n                )\n            if _description_maps_indeterminate_to_false(policy["descricao"]):\n                issues.append(\n                    Issue(\n                        "saida.publicacao.politica_indeterminado.descricao",\n                        "INDETERMINATE_POLICY_CONTRADICTION",\n                        "descricao contradiz a regra estruturada que preserva INDETERMINADO distinto de FALSE",\n                    )\n                )'''
text = replace_once(text, needle, replacement, "indeterminate policy")

text = replace_once(
    text,
    '''        if publication_status != "EM_VALIDACAO_EXTERNA" or not publication["handoff_ref"]:''',
    '''        if (\n            publication_status != "EM_VALIDACAO_EXTERNA"\n            or not _has_material_text(publication["handoff_ref"])\n        ):''',
    "handoff material",
)
text = replace_once(
    text,
    '''        if publication_status != "PUBLICADA" or not publication["produto_dados_ref"]:''',
    '''        if (\n            publication_status != "PUBLICADA"\n            or not _has_material_text(publication["produto_dados_ref"])\n        ):''',
    "product ref material",
)

text = replace_once(
    text,
    '''    parser.add_argument(\n        "--schema",\n        required=True,\n        help="caminho para micromodelo.schema.json",\n    )\n    args = parser.parse_args()''',
    '''    parser.add_argument(\n        "--schema",\n        required=True,\n        help="caminho para micromodelo.schema.json",\n    )\n    parser.add_argument(\n        "--previous",\n        help="especificação anterior confiável para validar evolução/anti-rewind",\n    )\n    args = parser.parse_args()''',
    "cli previous arg",
)
text = replace_once(
    text,
    '''        spec = load_document(args.documento)\n        schema = load_schema(args.schema)\n        issues = validate_spec(spec, schema)''',
    '''        spec = load_document(args.documento)\n        schema = load_schema(args.schema)\n        previous_spec = load_document(args.previous) if args.previous else None\n        issues = validate_spec(spec, schema, previous_spec=previous_spec)''',
    "cli previous load",
)
VALIDATOR.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# JSON Schema: whitespace fail-closed + política estruturada de indeterminado
# ---------------------------------------------------------------------------
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
prov = schema["$defs"]["proveniencia"]["properties"]
prov["origem"]["pattern"] = r".*\S.*"
prov["aprovacao"]["properties"]["por"]["pattern"] = r".*\S.*"
prov["aprovacao"]["properties"]["referencia"]["pattern"] = r".*\S.*"
prov["medicao"]["properties"]["referencia_execucao"]["pattern"] = r".*\S.*"

validation = schema["properties"]["validacao"]["properties"]["aprovacao_humana"]["properties"]
validation["por"]["pattern"] = r".*\S.*"
validation["referencia"]["pattern"] = r".*\S.*"

publication_props = schema["properties"]["publicacao"]["properties"]
publication_props["handoff_ref"]["pattern"] = r".*\S.*"
publication_props["produto_dados_ref"]["pattern"] = r".*\S.*"

policy = schema["properties"]["saida"]["properties"]["publicacao"]["properties"]["politica_indeterminado"]
policy_props = policy["properties"]
new_policy_props = {}
for key, value in policy_props.items():
    new_policy_props[key] = value
    if key == "tratamento":
        new_policy_props["indeterminado_vira_false"] = {"const": False}
policy["properties"] = new_policy_props
required = policy["required"]
if "indeterminado_vira_false" not in required:
    required.insert(required.index("descricao"), "indeterminado_vira_false")

calibration = schema["properties"]["score"]["properties"]["calibracao"]["properties"]["evidencia_ref"]
calibration["description"] = "ID de experimentos[].id que sustenta a calibração; deve referenciar experimento EXECUTADO e MEDIDO."

SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------
# Testes: adaptar caminho positivo e adicionar regressões dos cinco achados A1
# ---------------------------------------------------------------------------
tests = TESTS.read_text(encoding="utf-8")
tests = replace_once(
    tests,
    '''                "tratamento": "CAMPO_COBERTURA_SEPARADO",\n                "descricao": "publicar cobertura separada para preservar casos indeterminados",''',
    '''                "tratamento": "CAMPO_COBERTURA_SEPARADO",\n                "indeterminado_vira_false": False,\n                "descricao": "publicar cobertura separada para preservar casos indeterminados",''',
    "positive policy field",
)

new_tests = r'''
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
                "descricao": "preservar casos indeterminados em cobertura separada",
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
                "descricao": "preservar casos indeterminados em cobertura separada",
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
        approved = copy.deepcopy(self.valid)
        approved["validacao"]["aprovacao_humana"]["por"] = "   "
        self.assertIn("VALIDATION_HUMAN_GATE", self.codes(approved))

        measured = copy.deepcopy(self.valid)
        measured["experimentos"][0]["proveniencia"]["medicao"]["referencia_execucao"] = "\u200b"
        self.assertIn("PROV_MEASUREMENT_REQUIRED", self.codes(measured))

        published = copy.deepcopy(self.valid)
        published["identidade"]["estado"]["fase_anterior"] = "EM_VALIDACAO_GOVERNANCA"
        published["identidade"]["estado"]["fase_atual"] = "PUBLICADO"
        published["saida"]["publicacao"] = {
            "estado": "DEFINIDO",
            "campo_booleano": {"nome": "possui_caracteristica", "tipo": "BOOLEAN"},
            "politica_indeterminado": {
                "tratamento": "CAMPO_COBERTURA_SEPARADO",
                "indeterminado_vira_false": False,
                "descricao": "preservar casos indeterminados em cobertura separada",
                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
            },
        }
        published["publicacao"]["status"] = "PUBLICADA"
        published["publicacao"]["produto_dados_ref"] = "   "
        self.assertIn("PUBLICATION_GATE", self.codes(published))

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
                "descricao": "indeterminado deve ser gravado como FALSE",
                "proveniencia": copy.deepcopy(self.valid["classificacao"]["semantica"]["proveniencia"]),
            },
        }
        document["publicacao"]["status"] = "CANDIDATA"
        self.assertIn("INDETERMINATE_POLICY_CONTRADICTION", self.codes(document))

    def test_calibration_evidence_ref_must_resolve_to_executed_measured_experiment(self) -> None:
        calibrated = copy.deepcopy(self.valid)
        calibrated["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"
        calibrated["score"]["semantica"] = "probabilidade calibrada da característica"
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
                "descricao": "preservar casos indeterminados em cobertura separada",
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
'''

tests = replace_once(
    tests,
    '\n\nif __name__ == "__main__":\n    unittest.main()\n',
    "\n" + new_tests + '\n\nif __name__ == "__main__":\n    unittest.main()\n',
    "append A1 tests",
)
TESTS.write_text(tests, encoding="utf-8")

print("MM01 A1 patch applied")
