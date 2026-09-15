from __future__ import annotations

import json
from pathlib import Path

SCHEMA = Path("docs/sprints/micromodelos/MM01/micromodelo.schema.json")
CONTRACT = Path("tools/micromodelo_mm01_contract.py")
TESTS = Path("tools/tests/test_micromodelo_mm01.py")

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

# Reutiliza a autoridade Unicode já existente. Não introduz regex/predicado paralelo.
material_paths = [
    ("properties", "identidade", "properties", "estado", "properties", "motivo_condicao"),
    ("properties", "evidencias", "items", "properties", "regra"),
    ("properties", "contra_evidencias", "items", "properties", "regra"),
    ("properties", "experimentos", "items", "properties", "hipotese"),
    ("properties", "experimentos", "items", "properties", "resultado"),
    ("properties", "validacao", "properties", "resultado", "properties", "resumo"),
]

for path in material_paths:
    node = schema
    for key in path:
        node = node[key]
    node["format"] = "material-text"

SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

contract = CONTRACT.read_text(encoding="utf-8")
old_condition = 'if condicao != "ATIVO" and not (isinstance(motivo, str) and motivo.strip()):'
new_condition = 'if condicao != "ATIVO" and not _has_material_text(motivo):'
if old_condition not in contract and new_condition not in contract:
    raise SystemExit("gate de motivo_condicao não encontrado")
contract = contract.replace(old_condition, new_condition, 1)

old_result = 'if not isinstance(experiment["resultado"], str) or not experiment["resultado"].strip():'
new_result = 'if not _has_material_text(experiment["resultado"]):'
if old_result not in contract and new_result not in contract:
    raise SystemExit("gate de resultado de experimento não encontrado")
contract = contract.replace(old_result, new_result, 1)
CONTRACT.write_text(contract, encoding="utf-8")

tests = TESTS.read_text(encoding="utf-8")
anchor = '\n\nif __name__ == "__main__":\n'
methods = r'''
    def test_normative_material_fields_reject_nonmaterial_unicode_classes(self) -> None:
        negatives = [
            "\u0301",          # Mn
            "\u093e",          # Mc
            "\u20dd",          # Me
            "\u200b",          # Cf / ZWSP
            "\u200c",          # ZWNJ
            "\u200d",          # ZWJ
            "\u2060",          # WORD JOINER
            "\u2063",          # INVISIBLE SEPARATOR
            "   ",
            "\u00a0",          # NBSP
            "\u2003",          # EM SPACE
            "\u2007",          # FIGURE SPACE
            "\u202f",          # NARROW NO-BREAK SPACE
            "!!!!!",
            "∑€🧿",
            "\u0301\u093e\u20dd\u200b\u2060\u00a0!!!€",
        ]

        mutations = [
            ("evidencias.regra", lambda d, v: d["evidencias"][0].__setitem__("regra", v)),
            ("contra_evidencias.regra", lambda d, v: d["contra_evidencias"][0].__setitem__("regra", v)),
            ("experimentos.hipotese", lambda d, v: d["experimentos"][0].__setitem__("hipotese", v)),
            ("experimentos.resultado", lambda d, v: d["experimentos"][0].__setitem__("resultado", v)),
            ("validacao.resultado.resumo", lambda d, v: d["validacao"]["resultado"].__setitem__("resumo", v)),
        ]

        for field, mutate in mutations:
            for value in negatives:
                with self.subTest(field=field, value=repr(value)):
                    document = copy.deepcopy(self.valid)
                    mutate(document, value)
                    self.assertIn("SCHEMA", self.codes(document))

        for value in negatives:
            with self.subTest(field="identidade.estado.motivo_condicao", value=repr(value)):
                document = copy.deepcopy(self.valid)
                document["identidade"]["estado"]["condicao"] = "SUSPENSO"
                document["identidade"]["estado"]["motivo_condicao"] = value
                self.assertIn("SCHEMA", self.codes(document))

    def test_normative_material_fields_accept_legitimate_unicode(self) -> None:
        document = copy.deepcopy(self.valid)
        document["evidencias"][0]["regra"] = "规则有效 ٤٢"
        document["contra_evidencias"][0]["regra"] = "नियम वैध ४२"
        document["experimentos"][0]["hipotese"] = "Δοκιμή δεδομένων"
        document["experimentos"][0]["resultado"] = "результат Jose\u0301"
        document["validacao"]["resultado"]["resumo"] = "結果 válido ٤٢"
        document["identidade"]["estado"]["condicao"] = "SUSPENSO"
        document["identidade"]["estado"]["motivo_condicao"] = "تعليق تشغيلي ١"
        self.assertEqual([], module.validate_spec(document, self.schema))
'''

if "test_normative_material_fields_reject_nonmaterial_unicode_classes" not in tests:
    if anchor not in tests:
        raise SystemExit("anchor final dos testes não encontrado")
    tests = tests.replace(anchor, "\n" + methods + anchor, 1)
TESTS.write_text(tests, encoding="utf-8")

print("MM01 quarta A1: correção de materialidade normativa aplicada")
