from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: esperado 1 match, encontrado {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


contract = ROOT / "tools" / "micromodelo_mm01_contract.py"
replace_once(
    contract,
    "import argparse\nimport json\nimport re\nimport unicodedata\n",
    "import argparse\nimport json\nimport math\nimport re\nimport unicodedata\n",
    "import math",
)
replace_once(
    contract,
    '''def load_document(path: str | Path) -> dict[str, Any]:\n    file_path = Path(path)\n    text = file_path.read_text(encoding="utf-8")\n    if file_path.suffix.lower() == ".json":\n        loaded = json.loads(text, object_pairs_hook=_pairs_without_duplicates)\n    else:\n        loaded = _load_yaml_without_duplicate_keys(text)\n''',
    '''def _reject_nonfinite_json_constant(value: str) -> Any:\n    raise ValueError(f"constante JSON não finita recusada: {value}")\n\n\ndef load_document(path: str | Path) -> dict[str, Any]:\n    file_path = Path(path)\n    text = file_path.read_text(encoding="utf-8")\n    if file_path.suffix.lower() == ".json":\n        loaded = json.loads(\n            text,\n            object_pairs_hook=_pairs_without_duplicates,\n            parse_constant=_reject_nonfinite_json_constant,\n        )\n    else:\n        loaded = _load_yaml_without_duplicate_keys(text)\n''',
    "json strict loader",
)
replace_once(
    contract,
    '''    loaded = json.loads(\n        Path(path).read_text(encoding="utf-8"),\n        object_pairs_hook=_pairs_without_duplicates,\n    )\n''',
    '''    loaded = json.loads(\n        Path(path).read_text(encoding="utf-8"),\n        object_pairs_hook=_pairs_without_duplicates,\n        parse_constant=_reject_nonfinite_json_constant,\n    )\n''',
    "schema strict loader",
)
replace_once(
    contract,
    '''def _normalize_semantic_text(value: str) -> str:\n    decomposed = unicodedata.normalize("NFKD", value).casefold()\n    without_accents = "".join(\n        char for char in decomposed if not unicodedata.combining(char)\n    )\n    words_only = re.sub(r"[\\W_]+", " ", without_accents, flags=re.UNICODE)\n    return " ".join(words_only.split())\n''',
    '''def _is_semantic_default_ignorable(char: str) -> bool:\n    codepoint = ord(char)\n    return (\n        unicodedata.category(char) == "Cf"\n        or 0xFE00 <= codepoint <= 0xFE0F\n        or 0xE0100 <= codepoint <= 0xE01EF\n    )\n\n\ndef _normalize_semantic_text(value: str) -> str:\n    decomposed = unicodedata.normalize("NFKD", value).casefold()\n    normalized = "".join(\n        char\n        for char in decomposed\n        if not unicodedata.combining(char)\n        and not _is_semantic_default_ignorable(char)\n    )\n    words_only = re.sub(r"[\\W_]+", " ", normalized, flags=re.UNICODE)\n    return " ".join(words_only.split())\n''',
    "semantic default ignorables",
)
replace_once(
    contract,
    '''@MATERIAL_FORMAT_CHECKER.checks("material-text")\ndef _check_material_text_format(value: Any) -> bool:\n    """Implementa no schema a mesma política Unicode usada pelos gates semânticos."""\n    if not isinstance(value, str):\n        return True\n    return _has_material_text(value)\n''',
    '''@MATERIAL_FORMAT_CHECKER.checks("material-text")\ndef _check_material_text_format(value: Any) -> bool:\n    """Implementa no schema a mesma política Unicode usada pelos gates semânticos."""\n    if not isinstance(value, str):\n        return True\n    return _has_material_text(value)\n\n\n@MATERIAL_FORMAT_CHECKER.checks("finite-number")\ndef _check_finite_number_format(value: Any) -> bool:\n    """Recusa NaN e infinitos em números materiais do contrato."""\n    if isinstance(value, bool) or not isinstance(value, (int, float)):\n        return True\n    return math.isfinite(value)\n''',
    "finite number format",
)

schema_path = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "micromodelo.schema.json"
schema = json.loads(schema_path.read_text(encoding="utf-8"))
schema["properties"]["classificacao"]["properties"]["limiares"]["items"]["properties"]["valor"]["format"] = "finite-number"
schema["properties"]["score"]["properties"]["componentes"]["items"]["properties"]["peso"]["format"] = "finite-number"
schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

tests = ROOT / "tools" / "tests" / "test_micromodelo_mm01.py"
replace_once(
    tests,
    '''                if node.get("type") == "string" and "minLength" in node:\n                    if node.get("format") != "material-text":\n                        violations.append(".".join(path))\n''',
    '''                node_type = node.get("type")\n                accepts_string = node_type == "string" or (\n                    isinstance(node_type, list) and "string" in node_type\n                )\n                if accepts_string and "minLength" in node:\n                    if node.get("format") != "material-text":\n                        violations.append(".".join(path))\n''',
    "string type array guard",
)
insert_marker = '''    def test_schema_patterns_are_exact_structural_allowlist(self) -> None:\n'''
new_tests = '''    def test_semantic_equivalence_rejects_default_ignorable_infix(self) -> None:\n        base = self.valid["classificacao"]["semantica"]["quando_indeterminado"]\n        self.assertIn("disponível", base)\n        invisibles = [\n            "\\u200b",  # ZWSP\n            "\\u200c",  # ZWNJ\n            "\\u200d",  # ZWJ\n            "\\u2060",  # WORD JOINER\n            "\\u2063",  # INVISIBLE SEPARATOR\n            "\\ufe0f",  # VS16\n            "\\U000e0100",  # supplementary variation selector\n        ]\n        for invisible in invisibles:\n            with self.subTest(invisible=hex(ord(invisible))):\n                document = copy.deepcopy(self.valid)\n                disguised = base.replace("disponível", f"dispo{invisible}nível", 1)\n                self.assertEqual(\n                    module._normalize_semantic_text(base),\n                    module._normalize_semantic_text(disguised),\n                )\n                document["classificacao"]["semantica"]["quando_false"] = disguised\n                self.assertIn("AMBIGUOUS_BINARY_SEMANTICS", self.codes(document))\n\n    def test_required_minlength_guard_handles_string_type_arrays(self) -> None:\n        for node_type in (["string"], ["string", "null"]):\n            with self.subTest(node_type=node_type):\n                mutated = copy.deepcopy(self.schema)\n                mutated["$defs"]["synthetic_type_array_escape"] = {\n                    "type": node_type,\n                    "minLength": 3,\n                }\n                self.assertIn(\n                    "$defs.synthetic_type_array_escape",\n                    self._required_minlength_without_material_text(mutated),\n                )\n\n        nested = copy.deepcopy(self.schema)\n        nested["$defs"]["synthetic_nested_escape"] = {\n            "allOf": [\n                {"type": ["string", "null"], "minLength": 3},\n            ]\n        }\n        self.assertIn(\n            "$defs.synthetic_nested_escape.allOf.0",\n            self._required_minlength_without_material_text(nested),\n        )\n\n    def test_nonfinite_material_numbers_and_json_constants_are_rejected(self) -> None:\n        values = [float("nan"), float("inf"), float("-inf")]\n        mutations = [\n            (\n                "classificacao.limiares.valor",\n                lambda d, v: d["classificacao"]["limiares"][0].__setitem__("valor", v),\n            ),\n            (\n                "score.componentes.peso",\n                lambda d, v: d["score"]["componentes"][0].__setitem__("peso", v),\n            ),\n        ]\n        for field, mutate in mutations:\n            for value in values:\n                with self.subTest(field=field, value=repr(value)):\n                    document = copy.deepcopy(self.valid)\n                    mutate(document, value)\n                    self.assertIn("SCHEMA", self.codes(document))\n\n        with tempfile.TemporaryDirectory() as tmp:\n            import yaml\n\n            yaml_document = copy.deepcopy(self.valid)\n            yaml_document["classificacao"]["limiares"][0]["valor"] = float("nan")\n            yaml_path = Path(tmp) / "nonfinite.yaml"\n            yaml_path.write_text(\n                yaml.safe_dump(yaml_document, allow_unicode=True, sort_keys=False),\n                encoding="utf-8",\n            )\n            loaded_yaml = module.load_document(yaml_path)\n            self.assertIn("SCHEMA", self.codes(loaded_yaml))\n\n            for token in ("NaN", "Infinity", "-Infinity"):\n                with self.subTest(json_token=token):\n                    json_path = Path(tmp) / "nonfinite.json"\n                    json_path.write_text(f'{{"valor": {token}}}', encoding="utf-8")\n                    with self.assertRaisesRegex(ValueError, "não finita"):\n                        module.load_document(json_path)\n\n'''
replace_once(tests, insert_marker, new_tests + insert_marker, "insert seventh A1 regressions")

root_readme = ROOT / "README.md"
replace_once(
    root_readme,
    "repo (identidade)  : 1428 arquivos varridos no repositório editável/derivado",
    "repo (identidade)  : 1429 arquivos varridos no repositório editável/derivado",
    "root identity metric",
)

mm01_readme = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "README.md"
replace_once(
    mm01_readme,
    "Status da sprint: **SEXTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` E `DIVERGE-02` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; SÉTIMA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status da sprint: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO PENDENTE; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "MM01 README status",
)
replace_once(mm01_readme, "suíte automatizada com **36 métodos**", "suíte automatizada com **39 métodos**", "MM01 README test count")
replace_once(
    mm01_readme,
    "pacote de auditoria A1 com contexto, prompt e seis resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);",
    "pacote de auditoria A1 com contexto, prompt e sete resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);",
    "MM01 README audit count",
)
replace_once(
    mm01_readme,
    "O contraditório confirmou ambos os achados. A correção remove as três regex textuais genéricas, exige `material-text` em todo `type=string + minLength` e congela os únicos patterns remanescentes por path e regex exata como contratos estruturais. Um adversarial sintético prova que `minLength + pattern: .*\\S.*` sem format é violação. A suíte passa a **36 métodos**.\n\n## Fronteiras preservadas",
    "O contraditório confirmou ambos os achados. A correção remove as três regex textuais genéricas, exige `material-text` em todo `type=string + minLength` e congela os únicos patterns remanescentes por path e regex exata como contratos estruturais. Um adversarial sintético prova que `minLength + pattern: .*\\S.*` sem format é violação. A suíte passa a **36 métodos**.\n\n### Sétima A1\n\nA sétima auditoria independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes. `DIVERGE-01` demonstrou bypass da equivalência `FALSE` × `INDETERMINADO` por caracteres Unicode default-ignorable inseridos dentro de palavras; `DIVERGE-02` mostrou que o guard de `string + minLength` não reconhecia `type` representado por array; `DIVERGE-03` demonstrou que `NaN` e `±Infinity` atravessavam limiares e pesos materiais. O resultado histórico permanece em `09_resultado_a1_reauditoria_6.md`.\n\nO contraditório confirmou os três achados. A correção remove `Cf` e variation selectors antes da tokenização semântica, torna o guard sensível a arrays de tipos contendo `string`, registra `finite-number` no mesmo `FormatChecker` para limiares/pesos e recusa constantes JSON não finitas no loader. A suíte passa a **39 métodos**.\n\n## Fronteiras preservadas",
    "MM01 README seventh A1",
)
replace_once(
    mm01_readme,
    "A suíte MM01 possui **36 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da sexta A1 está verde no HEAD reconciliado, e os sete workflows permanentes foram executados com sucesso antes do congelamento para a sétima A1.",
    "A suíte MM01 possui **39 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da sétima A1 deve ficar verde no novo HEAD antes da próxima auditoria independente.",
    "MM01 README evidence",
)
replace_once(
    mm01_readme,
    "Como o contrato mudou materialmente depois da sexta A1, a MM01 só pode ser aceita após uma **sétima A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e construir adversariais próprios sobre todos os campos adicionados à política comum.\n\nO bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma sétima A1 limpa e contraditório final.\n\n**MM02 permanece bloqueada até sétima A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**",
    "Como o contrato mudou materialmente depois da sétima A1, a MM01 só pode ser aceita após uma **oitava A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural, CLI e adversariais próprios das três classes corrigidas.\n\nO bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma oitava A1 limpa e contraditório final.\n\n**MM02 permanece bloqueada até oitava A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**",
    "MM01 README gate",
)

checkpoint = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "CHECKPOINT.md"
replace_once(
    checkpoint,
    "Status: **SEXTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` E `DIVERGE-02` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; SÉTIMA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO PENDENTE; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "checkpoint status",
)
replace_once(checkpoint, "suíte com **36 métodos de teste**", "suíte com **39 métodos de teste**", "checkpoint test count")
replace_once(checkpoint, "resultados históricos das seis A1 preservados", "resultados históricos das sete A1 preservados", "checkpoint audit count")
replace_once(
    checkpoint,
    "A correção remove as três regex textuais genéricas e deixa `_has_material_text` → `format: material-text` como única autoridade de conteúdo material. Os únicos patterns remanescentes são contratos de estrutura (`$defs.id`, `identidade.nome` e `micromodel_version`) e ficam congelados por path + regex exata em regressão permanente. Todo `type=string + minLength` passa a exigir `material-text`; um nó sintético `minLength + pattern: .*\\S.*` sem format deve ser detectado como violação. A suíte passa a **36 métodos**.\n\n## Dívida documental antes do merge",
    "A correção remove as três regex textuais genéricas e deixa `_has_material_text` → `format: material-text` como única autoridade de conteúdo material. Os únicos patterns remanescentes são contratos de estrutura (`$defs.id`, `identidade.nome` e `micromodel_version`) e ficam congelados por path + regex exata em regressão permanente. Todo `type=string + minLength` passa a exigir `material-text`; um nó sintético `minLength + pattern: .*\\S.*` sem format deve ser detectado como violação. A suíte passa a **36 métodos**.\n\n## Sétima auditoria A1\n\nA sétima A1 independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: equivalência semântica burlável por default-ignorables, guard incompleto para `type` em array e números não finitos em limiares/pesos. O resultado foi preservado em `09_resultado_a1_reauditoria_6.md`.\n\n## Correções da sétima A1\n\nA normalização semântica remove `Cf` e variation selectors antes da tokenização; o guard de `string + minLength` reconhece tanto `type=\"string\"` quanto listas contendo `string`; e `finite-number` recusa NaN/±Infinity nos valores materiais, enquanto o loader JSON recusa constantes não padrão. A suíte passa a **39 métodos**.\n\n## Dívida documental antes do merge",
    "checkpoint seventh A1",
)
replace_once(
    checkpoint,
    "Como a candidata mudou materialmente após a sexta A1, é obrigatória uma **sétima A1 independente** sobre o novo HEAD congelado.",
    "Como a candidata mudou materialmente após a sétima A1, é obrigatória uma **oitava A1 independente** sobre o novo HEAD congelado.",
    "checkpoint independent gate",
)
replace_once(
    checkpoint,
    "1. executar sétima A1 em sessão independente;\n2. confrontar qualquer novo achado com a árvore;\n3. se a sétima A1 for limpa, executar contraditório final;\n4. sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;\n5. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;\n6. obter aceite explícito;\n7. só então integrar a PR #51.",
    "1. concluir o reteste de construção e validar os workflows permanentes do novo HEAD;\n2. executar oitava A1 em sessão independente;\n3. confrontar qualquer novo achado com a árvore;\n4. se a oitava A1 for limpa, executar contraditório final;\n5. sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;\n6. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;\n7. obter aceite explícito;\n8. só então integrar a PR #51.",
    "checkpoint remaining gates",
)

index = ROOT / "docs" / "sprints" / "micromodelos" / "README.md"
replace_once(
    index,
    "> Estado: **MM00 encerrada e integrada. MM01 passou por seis A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`); os dois desvios bloqueantes da sexta A1 foram confirmados e corrigidos; reteste e sete workflows permanentes verdes; sétima A1 independente pendente. MM01 ainda não aceita nem integrada.**",
    "> Estado: **MM00 encerrada e integrada. MM01 passou por sete A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`); os três desvios bloqueantes da sétima A1 foram confirmados e corrigidos; reteste e oitava A1 independente pendentes. MM01 ainda não aceita nem integrada.**",
    "index state",
)
replace_once(index, "suíte com **36 métodos de teste**", "suíte com **39 métodos de teste**", "index test count")
replace_once(
    index,
    "### Quinta e sexta A1\n\nA quinta A1 concluiu `APTA_COM_CORRECOES` e levou a política `material-text` aos demais textos obrigatórios, elevando a suíte a 34 métodos. A sexta A1, também `APTA_COM_CORRECOES`, encontrou duas sobras da mesma classe: três regex genéricas concorrentes e um guard que aceitava qualquer `pattern`. O sexto relatório está preservado em `08_resultado_a1_reauditoria_5.md`.\n\nA correção da sexta A1 remove as regex genéricas, exige `material-text` em todo `string + minLength` e congela os únicos patterns estruturais por path + regex exata. A suíte passa a 36 métodos.",
    "### Quinta, sexta e sétima A1\n\nA quinta A1 concluiu `APTA_COM_CORRECOES` e levou a política `material-text` aos demais textos obrigatórios, elevando a suíte a 34 métodos. A sexta A1, também `APTA_COM_CORRECOES`, encontrou duas sobras da mesma classe: três regex genéricas concorrentes e um guard que aceitava qualquer `pattern`. O sexto relatório está preservado em `08_resultado_a1_reauditoria_5.md`.\n\nA correção da sexta A1 remove as regex genéricas, exige `material-text` em todo `string + minLength` e congela os únicos patterns estruturais por path + regex exata, elevando a suíte a 36 métodos. A sétima A1, novamente `APTA_COM_CORRECOES`, encontrou três bloqueios: bypass de equivalência por Unicode default-ignorable, guard incompleto para arrays de tipos e aceitação de números não finitos. O sétimo relatório está preservado em `09_resultado_a1_reauditoria_6.md`.\n\nA correção da sétima A1 remove default-ignorables antes da tokenização semântica, fecha o guard para listas contendo `string` e exige `finite-number` para limiar/peso, com JSON estrito contra `NaN/Infinity`. A suíte passa a 39 métodos.",
    "index seventh A1",
)
replace_once(
    index,
    "1. executar uma **sétima A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;\n2. confrontar qualquer novo achado e corrigir somente se procedente;\n3. se a sétima A1 for limpa, executar contraditório final;\n4. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;\n5. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;\n6. integrar a PR #51 somente após o aceite.",
    "1. concluir o reteste das correções da sétima A1 e obter os workflows permanentes verdes no HEAD corrigido;\n2. executar uma **oitava A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;\n3. confrontar qualquer novo achado e corrigir somente se procedente;\n4. se a oitava A1 for limpa, executar contraditório final;\n5. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;\n6. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;\n7. integrar a PR #51 somente após o aceite.",
    "index next gate",
)

test_doc = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "TESTES.md"
replace_once(
    test_doc,
    "| T51 | nó sintético `string + minLength + pattern: .*\\\\S.*` sem `material-text` | detectado como violação |\n\nA suíte `tools/tests/test_micromodelo_mm01.py` contém **36 métodos de teste**;",
    "| T51 | nó sintético `string + minLength + pattern: .*\\\\S.*` sem `material-text` | detectado como violação |\n| T52 | equivalência semântica mascarada por ZWSP/ZWNJ/ZWJ/WORD JOINER/U+2063/variation selector dentro de palavra | `AMBIGUOUS_BINARY_SEMANTICS` |\n| T53 | `type=[\\\"string\\\"]` ou `[\\\"string\\\",\\\"null\\\"]` + `minLength` sem `material-text`, inclusive aninhado | detectado pelo guard |\n| T54 | NaN/±Infinity em limiar/peso e constantes JSON não padrão | `SCHEMA` / erro de carga fail-closed |\n\nA suíte `tools/tests/test_micromodelo_mm01.py` contém **39 métodos de teste**;",
    "test matrix seventh A1",
)
test_doc.write_text(
    test_doc.read_text(encoding="utf-8")
    + "\n\n## Sétima A1 — `APTA_COM_CORRECOES`\n\nA sétima auditoria independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` encontrou três divergências bloqueantes: caracteres Unicode default-ignorable podiam mascarar equivalência `FALSE` × `INDETERMINADO`; o guard de `string + minLength` ignorava `type` em array; e NaN/±Infinity atravessavam limiares/pesos. O relatório histórico permanece em `09_resultado_a1_reauditoria_6.md`.\n\nAs regressões adicionadas após o contraditório cobrem os três vetores: default-ignorables em posição interna, arrays de tipos e branches aninhados, além de valores não finitos via objeto Python, YAML e constantes JSON permissivas.\n",
    encoding="utf-8",
)

contract_doc = ROOT / "docs" / "sprints" / "micromodelos" / "MM01" / "CONTRATO_MICROMODELO.md"
replace_once(
    contract_doc,
    "A distinção é verificada após normalização editorial básica de caixa, acentuação, pontuação e espaços; não basta copiar a mesma definição mudando apenas forma textual.",
    "A distinção é verificada após normalização editorial de caixa, acentuação, pontuação e espaços. Caracteres Unicode default-ignorable (`Cf`) e variation selectors são removidos antes da tokenização, para que inserções invisíveis dentro de palavras não fabriquem uma diferença semântica artificial; não basta copiar a mesma definição mudando apenas forma textual.",
    "contract semantic normalization",
)
replace_once(
    contract_doc,
    "Limiar material pode ser registrado como `PROPOSTO` enquanto o micromodelo ainda está em descoberta/estudo. A partir de `EM_VALIDACAO`, todo limiar existente precisa carregar proveniência `APROVADO`. Dessa forma, a fonte canônica preserva propostas sem permitir que elas atravessem o gate formal como decisões válidas.",
    "Limiar material pode ser registrado como `PROPOSTO` enquanto o micromodelo ainda está em descoberta/estudo. A partir de `EM_VALIDACAO`, todo limiar existente precisa carregar proveniência `APROVADO`. `classificacao.limiares[].valor` precisa ser um número finito: NaN e ±Infinity são recusados. Dessa forma, a fonte canônica preserva propostas sem permitir que elas atravessem o gate formal como decisões inválidas.",
    "contract finite threshold",
)
replace_once(
    contract_doc,
    "Assim como limiares, pesos podem permanecer `PROPOSTO` nas fases pré-gate, mas todo peso existente precisa estar `APROVADO` ao entrar em `EM_VALIDACAO` ou fase posterior.",
    "Assim como limiares, pesos podem permanecer `PROPOSTO` nas fases pré-gate, mas todo peso existente precisa estar `APROVADO` ao entrar em `EM_VALIDACAO` ou fase posterior. `score.componentes[].peso` também precisa ser finito; NaN e ±Infinity não são valores materiais válidos.",
    "contract finite weight",
)
replace_once(
    contract_doc,
    "A quinta A1 mostrou que a distinção entre texto material e narrativa livre precisava ser explícita. Após a sexta A1, a classificação ficou fail-closed: todo `type=string` protegido por `minLength` deve usar `format: material-text`. Regex não substitui materialidade.",
    "A quinta A1 mostrou que a distinção entre texto material e narrativa livre precisava ser explícita. Após a sétima A1, a classificação ficou fail-closed: todo nó que aceite instância `string` (inclusive `type` em array) e use `minLength` deve usar `format: material-text`. Regex não substitui materialidade.",
    "contract type array policy",
)

print("Correções da sétima A1 aplicadas.")
