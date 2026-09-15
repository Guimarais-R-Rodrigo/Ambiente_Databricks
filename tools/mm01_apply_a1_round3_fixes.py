from __future__ import annotations

import json
from pathlib import Path

SCHEMA = Path("docs/sprints/micromodelos/MM01/micromodelo.schema.json")
CONTRACT = Path("tools/micromodelo_mm01_contract.py")
TESTS = Path("tools/tests/test_micromodelo_mm01.py")

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

# A política material é deliberadamente Unicode e compartilhada com o validador.
# O schema não tenta reproduzi-la com regex ASCII/Unicode parcial.
material_ref = schema["$defs"]["material_ref"]
material_ref.pop("pattern", None)
material_ref["format"] = "material-text"
material_ref["description"] = (
    "Referência auditável com ao menos uma letra ou número Unicode após NFKC; "
    "o format customizado é aplicado pelo validador MM01."
)

# Somente campos cujo contrato exige conteúdo material recebem o format.
# Campos narrativos livres não são convertidos indiscriminadamente para
# material-text: pontuação/símbolos podem ser conteúdo legítimo em prosa livre.
format_paths = [
    ("$defs", "proveniencia", "properties", "origem"),
    ("$defs", "proveniencia", "properties", "aprovacao", "properties", "por"),
    ("properties", "fontes", "items", "properties", "schema"),
    ("properties", "fontes", "items", "properties", "objeto"),
    ("properties", "fontes", "items", "properties", "campos", "items"),
    ("properties", "classificacao", "properties", "semantica", "properties", "quando_true"),
    ("properties", "classificacao", "properties", "semantica", "properties", "quando_false"),
    ("properties", "classificacao", "properties", "semantica", "properties", "quando_indeterminado"),
    ("properties", "validacao", "properties", "criterios", "items"),
    ("properties", "validacao", "properties", "aprovacao_humana", "properties", "por"),
    ("properties", "saida", "properties", "estudo", "properties", "campo_classificacao"),
    ("properties", "saida", "properties", "estudo", "properties", "campo_score"),
    ("properties", "saida", "properties", "publicacao", "properties", "campo_booleano", "properties", "nome"),
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

# Um teste histórico verificava a camada semântica específica. Com material-text,
# o mesmo valor também pode ser recusado antes pelo schema; ambas as camadas são
# fail-closed e o requisito é a rejeição, não o código intermediário específico.
old_assert = '''                approved["validacao"]["aprovacao_humana"]["por"] = mark\n                self.assertIn("VALIDATION_HUMAN_GATE", self.codes(approved))\n'''
new_assert = '''                approved["validacao"]["aprovacao_humana"]["por"] = mark\n                self.assertTrue(\n                    {"SCHEMA", "VALIDATION_HUMAN_GATE"} & self.codes(approved)\n                )\n'''
if old_assert in tests:
    tests = tests.replace(old_assert, new_assert, 1)
elif new_assert not in tests:
    raise SystemExit("assert de materialidade da aprovação humana não encontrado")

anchor = '\n\nif __name__ == "__main__":\n'
methods = r'''
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
'''
if "test_material_text_unicode_policy_is_shared_by_schema_and_validator" not in tests:
    if anchor not in tests:
        raise SystemExit("anchor final dos testes não encontrado")
    tests = tests.replace(anchor, "\n" + methods + anchor, 1)
TESTS.write_text(tests, encoding="utf-8")

print("MM01 terceira A1: patch aplicado")
