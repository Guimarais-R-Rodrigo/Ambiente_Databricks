from __future__ import annotations

import json
from pathlib import Path

SCHEMA = Path("docs/sprints/micromodelos/MM01/micromodelo.schema.json")
CONTRACT = Path("tools/micromodelo_mm01_contract.py")
TESTS = Path("tools/tests/test_micromodelo_mm01.py")

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

material_ref = schema["$defs"]["material_ref"]
material_ref.pop("pattern", None)
material_ref["format"] = "material-text"
material_ref["description"] = (
    "Referência auditável com ao menos uma letra ou número Unicode após NFKC; "
    "o format customizado é aplicado pelo validador MM01."
)

format_paths = [
    ("$defs", "proveniencia", "properties", "origem"),
    ("$defs", "proveniencia", "properties", "aprovacao", "properties", "por"),
    ("properties", "identidade", "properties", "titulo"),
    ("properties", "identidade", "properties", "estado", "properties", "motivo_condicao"),
    ("properties", "negocio", "properties", "caracteristica"),
    ("properties", "negocio", "properties", "objetivo"),
    ("properties", "negocio", "properties", "definicao_operacional"),
    ("properties", "negocio", "properties", "uso_pretendido", "items"),
    ("properties", "negocio", "properties", "nao_usar_para", "items"),
    ("properties", "entidade", "properties", "tipo"),
    ("properties", "entidade", "properties", "chave_logica"),
    ("properties", "entidade", "properties", "granularidade"),
    ("properties", "entidade", "properties", "populacao_elegivel"),
    ("properties", "entidade", "properties", "referencia_temporal"),
    ("properties", "fontes", "items", "properties", "schema"),
    ("properties", "fontes", "items", "properties", "objeto"),
    ("properties", "fontes", "items", "properties", "campos", "items"),
    ("properties", "evidencias", "items", "properties", "descricao"),
    ("properties", "evidencias", "items", "properties", "regra"),
    ("properties", "contra_evidencias", "items", "properties", "descricao"),
    ("properties", "contra_evidencias", "items", "properties", "regra"),
    ("properties", "classificacao", "properties", "semantica", "properties", "quando_true"),
    ("properties", "classificacao", "properties", "semantica", "properties", "quando_false"),
    ("properties", "classificacao", "properties", "semantica", "properties", "quando_indeterminado"),
    ("properties", "classificacao", "properties", "limiares", "items", "properties", "descricao"),
    ("properties", "classificacao", "properties", "limiares", "items", "properties", "unidade"),
    ("properties", "score", "properties", "componentes", "items", "properties", "descricao"),
    ("properties", "score", "properties", "calibracao", "properties", "metodo"),
    ("properties", "experimentos", "items", "properties", "hipotese"),
    ("properties", "experimentos", "items", "properties", "resultado"),
    ("properties", "validacao", "properties", "criterios", "items"),
    ("properties", "validacao", "properties", "resultado", "properties", "resumo"),
    ("properties", "validacao", "properties", "aprovacao_humana", "properties", "por"),
    ("properties", "saida", "properties", "estudo", "properties", "campo_classificacao"),
    ("properties", "saida", "properties", "estudo", "properties", "campo_score"),
    ("properties", "saida", "properties", "publicacao", "properties", "campo_booleano", "properties", "nome"),
    ("properties", "governanca", "properties", "classificacao_dados"),
    ("properties", "governanca", "properties", "lgpd"),
    ("properties", "governanca", "properties", "gestor_informacao"),
    ("properties", "governanca", "properties", "observacoes", "items"),
    ("properties", "proveniencia", "properties", "gerado_por"),
    ("properties", "proveniencia", "properties", "pedido_original_ref"),
    ("properties", "proveniencia", "properties", "registros", "items", "properties", "alvo"),
]

for path in format_paths:
    node = schema
    for key in path:
        node = node[key]
    node["format"] = "material-text"

SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

contract = CONTRACT.read_text(encoding="utf-8")
needle = '''def _semver_tuple(value: str) -> tuple[int, int, int]:\n'''
insert = '''MATERIAL_FORMAT_CHECKER = FormatChecker()\n\n\n@MATERIAL_FORMAT_CHECKER.checks("material-text")\ndef _check_material_text_format(value: Any) -> bool:\n    """Implementa no schema a mesma política Unicode usada pelos gates semânticos."""\n    if not isinstance(value, str):\n        return True\n    return _has_material_text(value)\n\n\n'''
if insert not in contract:
    if needle not in contract:
        raise SystemExit("anchor _semver_tuple não encontrado")
    contract = contract.replace(needle, insert + needle, 1)

old = 'validator = Draft202012Validator(schema, format_checker=FormatChecker())'
new = 'validator = Draft202012Validator(schema, format_checker=MATERIAL_FORMAT_CHECKER)'
if old not in contract and new not in contract:
    raise SystemExit("instanciação do FormatChecker não encontrada")
contract = contract.replace(old, new, 1)
CONTRACT.write_text(contract, encoding="utf-8")

tests = TESTS.read_text(encoding="utf-8")
anchor = '\n\nif __name__ == "__main__":\n'
methods = r'''
    def test_material_text_unicode_policy_is_shared_by_schema_and_validator(self) -> None:
        positives = ["é", "文档", "١", "देवनागरी", "Cafe\u0301"]
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
            "\u00a0",
            "\u2003",
            "!!!",
            "€",
            "\u034f\u200b\u0301",
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
        for field in ("gerado_por", "pedido_original_ref"):
            with self.subTest(field=field):
                document = copy.deepcopy(self.valid)
                document["proveniencia"][field] = "\u200b!!!"
                self.assertIn("SCHEMA", self.codes(document))

        record = copy.deepcopy(self.valid)
        record["proveniencia"]["registros"] = [
            {
                "alvo": "\u034f",
                "proveniencia": copy.deepcopy(
                    self.valid["classificacao"]["semantica"]["proveniencia"]
                ),
            }
        ]
        self.assertIn("SCHEMA", self.codes(record))

        positive = copy.deepcopy(self.valid)
        positive["proveniencia"]["gerado_por"] = "生成器"
        positive["proveniencia"]["pedido_original_ref"] = "文档١"
        positive["proveniencia"]["registros"] = [
            {
                "alvo": "目标",
                "proveniencia": copy.deepcopy(
                    self.valid["classificacao"]["semantica"]["proveniencia"]
                ),
            }
        ]
        self.assertEqual([], module.validate_spec(positive, self.schema))

    def test_material_content_gates_reject_nonmaterial_and_accept_unicode(self) -> None:
        mutations = [
            lambda d: d["classificacao"]["semantica"].__setitem__("quando_true", "\u200b" * 5),
            lambda d: d["validacao"].__setitem__("criterios", ["!!!"]),
            lambda d: d["fontes"][0].__setitem__("schema", "\u200b"),
            lambda d: d["fontes"][0].__setitem__("objeto", "\u200b"),
            lambda d: d["fontes"][0]["campos"].__setitem__(0, "\u200b"),
            lambda d: d["saida"]["estudo"].__setitem__("campo_classificacao", "\u200b"),
            lambda d: d["saida"]["estudo"].__setitem__("campo_score", "\u200b"),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                document = copy.deepcopy(self.valid)
                mutate(document)
                self.assertIn("SCHEMA", self.codes(document))

        unicode_document = copy.deepcopy(self.valid)
        unicode_document["classificacao"]["semantica"]["quando_true"] = "证据充分确认特征"
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
'''
if "test_material_text_unicode_policy_is_shared_by_schema_and_validator" not in tests:
    if anchor not in tests:
        raise SystemExit("anchor final dos testes não encontrado")
    tests = tests.replace(anchor, "\n" + methods + anchor, 1)
TESTS.write_text(tests, encoding="utf-8")

print("MM01 terceira A1: patch aplicado")
