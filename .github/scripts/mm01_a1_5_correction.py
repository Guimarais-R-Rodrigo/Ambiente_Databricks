from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(".")
SCHEMA_PATH = ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json"
TEST_PATH = ROOT / "tools/tests/test_micromodelo_mm01.py"

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

MATERIAL_PATHS = {
    "identidade.titulo": ("properties", "identidade", "properties", "titulo"),
    "negocio.caracteristica": ("properties", "negocio", "properties", "caracteristica"),
    "negocio.objetivo": ("properties", "negocio", "properties", "objetivo"),
    "negocio.definicao_operacional": ("properties", "negocio", "properties", "definicao_operacional"),
    "negocio.uso_pretendido[]": ("properties", "negocio", "properties", "uso_pretendido", "items"),
    "negocio.nao_usar_para[]": ("properties", "negocio", "properties", "nao_usar_para", "items"),
    "entidade.tipo": ("properties", "entidade", "properties", "tipo"),
    "entidade.chave_logica": ("properties", "entidade", "properties", "chave_logica"),
    "entidade.granularidade": ("properties", "entidade", "properties", "granularidade"),
    "entidade.populacao_elegivel": ("properties", "entidade", "properties", "populacao_elegivel"),
    "entidade.referencia_temporal": ("properties", "entidade", "properties", "referencia_temporal"),
    "fontes[].catalogo_ref": ("properties", "fontes", "items", "properties", "catalogo_ref"),
    "evidencias[].descricao": ("properties", "evidencias", "items", "properties", "descricao"),
    "contra_evidencias[].descricao": ("properties", "contra_evidencias", "items", "properties", "descricao"),
    "classificacao.limiares[].descricao": ("properties", "classificacao", "properties", "limiares", "items", "properties", "descricao"),
    "classificacao.limiares[].unidade": ("properties", "classificacao", "properties", "limiares", "items", "properties", "unidade"),
    "score.componentes[].descricao": ("properties", "score", "properties", "componentes", "items", "properties", "descricao"),
    "score.calibracao.metodo": ("properties", "score", "properties", "calibracao", "properties", "metodo"),
    "governanca.classificacao_dados": ("properties", "governanca", "properties", "classificacao_dados"),
    "governanca.lgpd": ("properties", "governanca", "properties", "lgpd"),
    "governanca.gestor_informacao": ("properties", "governanca", "properties", "gestor_informacao"),
}
NARRATIVE_EXEMPTIONS = {
    "properties.governanca.properties.observacoes.items",
}


def get_node(parts: tuple[str, ...]) -> dict:
    node = schema
    for part in parts:
        node = node[part]
    if not isinstance(node, dict):
        raise AssertionError(f"schema node is not object: {parts}")
    return node


for label, parts in MATERIAL_PATHS.items():
    node = get_node(parts)
    if node.get("type") != "string":
        raise AssertionError(f"{label}: expected string, got {node.get('type')!r}")
    if "minLength" not in node:
        raise AssertionError(f"{label}: minLength absent")
    node["format"] = "material-text"

unclassified: list[str] = []


def walk(node: object, path: tuple[str, ...] = ()) -> None:
    if isinstance(node, dict):
        if node.get("type") == "string" and "minLength" in node:
            joined = ".".join(path)
            if (
                node.get("format") != "material-text"
                and "pattern" not in node
                and joined not in NARRATIVE_EXEMPTIONS
            ):
                unclassified.append(joined)
        for key, value in node.items():
            walk(value, path + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            walk(value, path + (str(index),))


walk(schema)
if unclassified:
    raise AssertionError("unclassified minLength text fields: " + ", ".join(unclassified))

SCHEMA_PATH.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

test_text = TEST_PATH.read_text(encoding="utf-8")
sentinel = '\n\nif __name__ == "__main__":\n    unittest.main()\n'
if sentinel not in test_text:
    raise AssertionError("test sentinel not found")
if "test_required_minlength_text_fields_have_explicit_material_policy" in test_text:
    raise AssertionError("fifth-A1 regressions already present")

methods = r'''

    def test_required_minlength_text_fields_have_explicit_material_policy(self) -> None:
        narrative_exemptions = {
            "properties.governanca.properties.observacoes.items",
        }
        unclassified: list[str] = []

        def walk(node: object, path: tuple[str, ...] = ()) -> None:
            if isinstance(node, dict):
                if node.get("type") == "string" and "minLength" in node:
                    joined = ".".join(path)
                    if (
                        node.get("format") != "material-text"
                        and "pattern" not in node
                        and joined not in narrative_exemptions
                    ):
                        unclassified.append(joined)
                for key, value in node.items():
                    walk(value, path + (str(key),))
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, path + (str(index),))

        walk(self.schema)
        self.assertEqual([], unclassified)

    def test_canonical_required_text_fields_reject_nonmaterial_content(self) -> None:
        raw_negatives = [
            "\u0301",
            "\u093e",
            "\u20dd",
            "\u200b",
            "\u200c",
            "\u200d",
            "\u2060",
            "\u2063",
            " ",
            "\u00a0",
            "\u2003",
            "\u2007",
            "\u202f",
            "!",
            "€",
            "\u0301\u200b!€",
        ]

        mutations = [
            ("identidade.titulo", 3, lambda d, v: d["identidade"].__setitem__("titulo", v)),
            ("negocio.caracteristica", 3, lambda d, v: d["negocio"].__setitem__("caracteristica", v)),
            ("negocio.objetivo", 10, lambda d, v: d["negocio"].__setitem__("objetivo", v)),
            ("negocio.definicao_operacional", 10, lambda d, v: d["negocio"].__setitem__("definicao_operacional", v)),
            ("negocio.uso_pretendido[]", 3, lambda d, v: d["negocio"]["uso_pretendido"].__setitem__(0, v)),
            ("negocio.nao_usar_para[]", 3, lambda d, v: d["negocio"]["nao_usar_para"].__setitem__(0, v)),
            ("entidade.tipo", 2, lambda d, v: d["entidade"].__setitem__("tipo", v)),
            ("entidade.chave_logica", 2, lambda d, v: d["entidade"].__setitem__("chave_logica", v)),
            ("entidade.granularidade", 5, lambda d, v: d["entidade"].__setitem__("granularidade", v)),
            ("entidade.populacao_elegivel", 10, lambda d, v: d["entidade"].__setitem__("populacao_elegivel", v)),
            ("entidade.referencia_temporal", 5, lambda d, v: d["entidade"].__setitem__("referencia_temporal", v)),
            ("fontes.catalogo_ref", 1, lambda d, v: d["fontes"][0].__setitem__("catalogo_ref", v)),
            ("evidencias.descricao", 5, lambda d, v: d["evidencias"][0].__setitem__("descricao", v)),
            ("contra_evidencias.descricao", 5, lambda d, v: d["contra_evidencias"][0].__setitem__("descricao", v)),
            ("classificacao.limiares.descricao", 3, lambda d, v: d["classificacao"]["limiares"][0].__setitem__("descricao", v)),
            ("classificacao.limiares.unidade", 1, lambda d, v: d["classificacao"]["limiares"][0].__setitem__("unidade", v)),
            ("score.componentes.descricao", 3, lambda d, v: d["score"]["componentes"][0].__setitem__("descricao", v)),
            ("governanca.classificacao_dados", 1, lambda d, v: d["governanca"].__setitem__("classificacao_dados", v)),
            ("governanca.lgpd", 1, lambda d, v: d["governanca"].__setitem__("lgpd", v)),
            ("governanca.gestor_informacao", 1, lambda d, v: d["governanca"].__setitem__("gestor_informacao", v)),
        ]

        for field, min_length, mutate in mutations:
            for raw in raw_negatives:
                value = raw * (min_length // max(1, len(raw)) + 1)
                self.assertGreaterEqual(len(value), min_length)
                self.assertFalse(module._has_material_text(value))
                with self.subTest(field=field, value=repr(value)):
                    document = copy.deepcopy(self.valid)
                    mutate(document, value)
                    self.assertIn("SCHEMA", self.codes(document))

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
        for raw in raw_negatives:
            value = raw * (3 // max(1, len(raw)) + 1)
            self.assertGreaterEqual(len(value), 3)
            self.assertFalse(module._has_material_text(value))
            with self.subTest(field="score.calibracao.metodo", value=repr(value)):
                document = copy.deepcopy(calibrated)
                document["score"]["calibracao"]["metodo"] = value
                self.assertIn("SCHEMA", self.codes(document))

    def test_canonical_required_text_fields_accept_legitimate_unicode(self) -> None:
        document = copy.deepcopy(self.valid)
        material_long = "Texto válido 文档 देवनागरी ١٢٣ Jose\u0301"
        material_short = "文档١"
        document["identidade"]["titulo"] = material_long
        document["negocio"]["caracteristica"] = material_long
        document["negocio"]["objetivo"] = material_long
        document["negocio"]["definicao_operacional"] = material_long
        document["negocio"]["uso_pretendido"] = [material_long]
        document["negocio"]["nao_usar_para"] = [material_long]
        document["entidade"]["tipo"] = material_short
        document["entidade"]["chave_logica"] = material_short
        document["entidade"]["granularidade"] = material_long
        document["entidade"]["populacao_elegivel"] = material_long
        document["entidade"]["referencia_temporal"] = material_long
        document["evidencias"][0]["descricao"] = material_long
        document["contra_evidencias"][0]["descricao"] = material_long
        document["classificacao"]["limiares"][0]["descricao"] = material_long
        document["classificacao"]["limiares"][0]["unidade"] = material_short
        document["score"]["componentes"][0]["descricao"] = material_long
        document["governanca"]["classificacao_dados"] = material_short
        document["governanca"]["lgpd"] = material_short
        document["governanca"]["gestor_informacao"] = material_short
        self.assertEqual([], module.validate_spec(document, self.schema))

        calibrated = copy.deepcopy(document)
        calibrated["score"]["tipo_semantica"] = "PROBABILIDADE_CALIBRADA"
        calibrated["score"]["semantica_ref"] = "SEM-PROB-001"
        calibrated["score"]["calibracao"] = {
            "metodo": "校准方法 ١٢٣",
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
'''
TEST_PATH.write_text(test_text.replace(sentinel, methods + sentinel), encoding="utf-8")

contract_path = ROOT / "docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md"
contract = contract_path.read_text(encoding="utf-8")
section = '''
### Classificação explícita dos textos obrigatórios

A quinta A1 mostrou que a distinção entre texto material e narrativa livre precisava ser explícita. Todo campo textual obrigatório protegido por `minLength` deve ter uma política executável: `format: material-text`, quando participa da definição canônica, ou `pattern`, quando a sintaxe fechada já exige conteúdo material. A autoridade de materialidade continua sendo exclusivamente `_has_material_text` após NFKC; não há regex, `.strip()` ou segundo predicado concorrente.

Além dos campos já protegidos anteriormente, usam `material-text`: `identidade.titulo`; todos os valores textuais requeridos de `negocio`; todos os valores textuais requeridos de `entidade`; `fontes[].catalogo_ref`; `evidencias[].descricao`; `contra_evidencias[].descricao`; `classificacao.limiares[].descricao`; `classificacao.limiares[].unidade`; `score.componentes[].descricao`; `score.calibracao.metodo`; `governanca.classificacao_dados`; `governanca.lgpd`; e `governanca.gestor_informacao`.

Identificadores internos, `identidade.nome` e `identidade.micromodel_version` permanecem fechados por `pattern`. `fontes[].catalogo_ref` permanece adicionalmente sujeito ao gate semântico `CATALOGO_PRODUTO`.

`governanca.observacoes[]` é a exceção narrativa explícita: é opcional, não satisfaz gate material e não substitui campo normativo. Por isso não recebe `material-text` apenas por ser string.
'''
if "### Classificação explícita dos textos obrigatórios" not in contract:
    contract = contract.rstrip() + "\n\n" + section.strip() + "\n"
contract_path.write_text(contract, encoding="utf-8")

tests_doc_path = ROOT / "docs/sprints/micromodelos/MM01/TESTES.md"
tests_doc = tests_doc_path.read_text(encoding="utf-8")
tests_doc = tests_doc.replace(
    "A suíte `tools/tests/test_micromodelo_mm01.py` contém **31 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz.",
    "A suíte `tools/tests/test_micromodelo_mm01.py` contém **34 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz.",
    1,
)
if "| T47 |" not in tests_doc:
    anchor = "| T46 | os mesmos campos normativos com conteúdo Unicode legítimo multilíngue | APROVADO |"
    if anchor not in tests_doc:
        raise AssertionError("T46 anchor missing")
    tests_doc = tests_doc.replace(
        anchor,
        anchor
        + "\n| T47 | textos obrigatórios adicionais com conteúdo não material que ainda satisfaz `minLength` | `SCHEMA` |"
        + "\n| T48 | os mesmos campos adicionais com conteúdo Unicode legítimo multilíngue | APROVADO |"
        + "\n| T49 | todo `type=string` + `minLength` possui `material-text`, `pattern` ou exceção narrativa explícita | invariável estrutural |",
        1,
    )
next_heading = "## Próxima auditoria A1"
prefix = tests_doc.split(next_heading, 1)[0].rstrip() if next_heading in tests_doc else tests_doc.rstrip()
tests_doc = prefix + '''

## Quinta A1 — `APTA_COM_CORRECOES`

A quinta auditoria independente sobre `0b7a712cd2c897483da34517f10516012711f153` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com `DIVERGE-01` bloqueante: campos centrais ainda podiam satisfazer `minLength` usando apenas pontuação, zero-width, marks, whitespace ou símbolos. O resultado histórico permanece em `07_resultado_a1_reauditoria_4.md` e não é reclassificado por correções posteriores.

### Correção da quinta A1

A correção fecha a classe de defeito: textos obrigatórios com `minLength` precisam usar `material-text`, `pattern` ou constar na exceção narrativa explícita `governanca.observacoes[]`. `_has_material_text` e o `FormatChecker` não foram alterados. A suíte passa a **34 métodos**, com adversariais que deliberadamente excedem `minLength` usando conteúdo não material e positivos multilíngues.

## Próxima auditoria A1

Uma **sexta A1 independente** é obrigatória porque a candidata mudou materialmente depois da quinta A1. Ela deve auditar o HEAD efetivamente encontrado, repetir os gates mínimos e criar adversariais próprios sobre os campos adicionais submetidos à política comum.

MM02 permanece bloqueada até sexta A1, contraditório se necessário, fechamento do changelog, aceite explícito e integração da MM01.
'''
tests_doc_path.write_text(tests_doc, encoding="utf-8")

checkpoint_path = ROOT / "docs/sprints/micromodelos/MM01/CHECKPOINT.md"
checkpoint = checkpoint_path.read_text(encoding="utf-8")
checkpoint = checkpoint.replace(
    "Status: **QUARTA A1 `APTA_COM_CORRECOES`; DIVERGÊNCIA BLOQUEANTE CORRIGIDA; RETESTE DE CONSTRUÇÃO VERDE; QUINTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status: **QUINTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` BLOQUEANTE CONFIRMADA E CORRIGIDA; RETESTE DE CONSTRUÇÃO EM EXECUÇÃO; SEXTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    1,
)
checkpoint = checkpoint.replace("suíte com **31 métodos de teste**", "suíte com **34 métodos de teste**", 1)
checkpoint = checkpoint.replace(
    "pacote neutro de auditoria com os resultados históricos das quatro A1 preservados",
    "pacote neutro de auditoria com os resultados históricos das cinco A1 preservados",
    1,
)
if "## Quinta auditoria A1" not in checkpoint:
    marker = "## Dívida documental antes do merge"
    if marker not in checkpoint:
        raise AssertionError("checkpoint debt marker missing")
    addition = '''## Quinta auditoria A1

A quinta A1 independente sobre `0b7a712cd2c897483da34517f10516012711f153` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`. O único achado, `DIVERGE-01`, foi confirmado no contraditório: textos centrais de identidade, negócio, entidade, calibração e outros campos equivalentes ainda podiam ser materialmente vazios. O relatório histórico foi preservado em `07_resultado_a1_reauditoria_4.md`.

## Correções da quinta A1

A correção mantém `_has_material_text` como autoridade única e amplia `format: material-text` aos textos obrigatórios que participam do contrato. Um teste estrutural protege a classificação futura; `governanca.observacoes[]` é a exceção narrativa opcional explícita. A suíte passa a **34 métodos**.

'''
    checkpoint = checkpoint.replace(marker, addition + marker, 1)
gate_marker = "## Gate independente pendente"
if gate_marker in checkpoint:
    checkpoint = checkpoint.split(gate_marker, 1)[0].rstrip() + '''
    
## Gate independente pendente

Como a candidata mudou materialmente após a quinta A1, é obrigatória uma **sexta A1 independente** sobre o novo HEAD congelado.

## Gates restantes

1. concluir o reteste de construção e validar os workflows permanentes do novo HEAD;
2. executar sexta A1 em sessão independente;
3. confrontar qualquer novo achado com a árvore;
4. se a sexta A1 for limpa, executar contraditório final;
5. sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;
6. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;
7. obter aceite explícito;
8. só então integrar a PR #51.

Enquanto qualquer item estiver pendente, **MM02 permanece bloqueada**.
'''
checkpoint_path.write_text(checkpoint, encoding="utf-8")

mm01_readme_path = ROOT / "docs/sprints/micromodelos/MM01/README.md"
mm01_readme = mm01_readme_path.read_text(encoding="utf-8")
mm01_readme = mm01_readme.replace(
    "Status da sprint: **QUARTA A1 `APTA_COM_CORRECOES`; DIVERGÊNCIA BLOQUEANTE CORRIGIDA; RETESTE DE CONSTRUÇÃO VERDE; QUINTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status da sprint: **QUINTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` BLOQUEANTE CONFIRMADA E CORRIGIDA; RETESTE DE CONSTRUÇÃO EM EXECUÇÃO; SEXTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    1,
)
mm01_readme = mm01_readme.replace("suíte automatizada com **31 métodos**", "suíte automatizada com **34 métodos**", 1)
mm01_readme = mm01_readme.replace(
    "pacote de auditoria A1 com contexto, prompt e quatro resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`)",
    "pacote de auditoria A1 com contexto, prompt e cinco resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`)",
    1,
)
if "### Quinta A1" not in mm01_readme:
    marker = "## Fronteiras preservadas"
    if marker not in mm01_readme:
        raise AssertionError("MM01 README boundary marker missing")
    addition = '''### Quinta A1

A quinta auditoria independente sobre `0b7a712cd2c897483da34517f10516012711f153` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com `DIVERGE-01`: textos centrais ainda eram validados apenas por comprimento. O resultado permanece em `07_resultado_a1_reauditoria_4.md`.

O contraditório confirmou a divergência. A correção reutiliza `material-text` nos demais textos obrigatórios do contrato e acrescenta uma invariável estrutural para impedir novos `string + minLength` sem política explícita. `governanca.observacoes[]` permanece narrativa opcional. A suíte passa a **34 métodos**.

'''
    mm01_readme = mm01_readme.replace(marker, addition + marker, 1)
mm01_readme = mm01_readme.replace(
    "A suíte MM01 possui **31 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da quarta A1 ficou verde antes da publicação do commit permanente.",
    "A suíte MM01 possui **34 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da quinta A1 deve ficar verde no novo HEAD antes da próxima auditoria independente.",
    1,
)
gate = "## Gate de saída"
if gate not in mm01_readme:
    raise AssertionError("MM01 README gate marker missing")
mm01_readme = mm01_readme.split(gate, 1)[0].rstrip() + '''

## Gate de saída

Como o contrato mudou materialmente depois da quinta A1, a MM01 só pode ser aceita após uma **sexta A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e construir adversariais próprios sobre todos os campos adicionados à política comum.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma sexta A1 limpa e contraditório final.

**MM02 permanece bloqueada até sexta A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**
'''
mm01_readme_path.write_text(mm01_readme, encoding="utf-8")

root_readme_path = ROOT / "README.md"
root_readme = root_readme_path.read_text(encoding="utf-8")
old = "repo (identidade)  : 1425 arquivos varridos no repositório editável/derivado"
new = "repo (identidade)  : 1426 arquivos varridos no repositório editável/derivado"
if old not in root_readme:
    raise AssertionError("root README 1425 metric not found")
root_readme_path.write_text(root_readme.replace(old, new, 1), encoding="utf-8")
