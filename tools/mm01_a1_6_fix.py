from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('.')
SCHEMA = ROOT / 'docs/sprints/micromodelos/MM01/micromodelo.schema.json'
TESTS = ROOT / 'tools/tests/test_micromodelo_mm01.py'
MM01_README = ROOT / 'docs/sprints/micromodelos/MM01/README.md'
CHECKPOINT = ROOT / 'docs/sprints/micromodelos/MM01/CHECKPOINT.md'
TESTES_MD = ROOT / 'docs/sprints/micromodelos/MM01/TESTES.md'
CONTRATO = ROOT / 'docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md'
MICRO_INDEX = ROOT / 'docs/sprints/micromodelos/README.md'
ROOT_README = ROOT / 'README.md'


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f'{label}: esperado 1 match, encontrado {count}')
    return text.replace(old, new, 1)


def get_node(schema: dict, path: tuple[str, ...]) -> dict:
    node = schema
    for part in path:
        node = node[part]
    if not isinstance(node, dict):
        raise AssertionError(f'node não-dict em {path!r}')
    return node


# 1) DIVERGE-01: remover a segunda autoridade textual genérica.
schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
competing_paths = {
    '$defs.proveniencia.properties.origem': (
        '$defs', 'proveniencia', 'properties', 'origem'
    ),
    '$defs.proveniencia.properties.aprovacao.properties.por': (
        '$defs', 'proveniencia', 'properties', 'aprovacao', 'properties', 'por'
    ),
    'properties.validacao.properties.aprovacao_humana.properties.por': (
        'properties', 'validacao', 'properties', 'aprovacao_humana', 'properties', 'por'
    ),
}
for label, path in competing_paths.items():
    node = get_node(schema, path)
    if node.get('format') != 'material-text':
        raise AssertionError(f'{label}: material-text ausente')
    if node.get('pattern') != r'.*\S.*':
        raise AssertionError(f'{label}: pattern inesperado {node.get("pattern")!r}')
    node.pop('pattern')

# A única família de regex remanescente deve ser estrutural e fechada por path+valor.
expected_structural_patterns = {
    '$defs.id': r'^[a-z][a-z0-9_]{2,63}$',
    'properties.identidade.properties.nome': r'^[a-z][a-z0-9-]{2,63}$',
    'properties.identidade.properties.micromodel_version': r'^\d+\.\d+\.\d+$',
}
seen_patterns: dict[str, str] = {}
competing_material_patterns: list[str] = []


def walk_schema(node: object, path: tuple[str, ...] = ()) -> None:
    if isinstance(node, dict):
        joined = '.'.join(path)
        if 'pattern' in node:
            seen_patterns[joined] = node['pattern']
        if node.get('format') == 'material-text' and 'pattern' in node:
            competing_material_patterns.append(joined)
        for key, value in node.items():
            walk_schema(value, path + (str(key),))
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            walk_schema(value, path + (str(idx),))


walk_schema(schema)
if competing_material_patterns:
    raise AssertionError(
        'material-text ainda combina pattern: ' + ', '.join(competing_material_patterns)
    )
if seen_patterns != expected_structural_patterns:
    raise AssertionError(
        f'patterns estruturais divergentes: observado={seen_patterns!r} '
        f'esperado={expected_structural_patterns!r}'
    )

SCHEMA.write_text(
    json.dumps(schema, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# 2) DIVERGE-02: tornar o guard fail-closed e provar o escape sintético.
test_text = TESTS.read_text(encoding='utf-8')
start_marker = '    def test_required_minlength_text_fields_have_explicit_material_policy(self) -> None:\n'
end_marker = '    def test_canonical_required_text_fields_reject_nonmaterial_content(self) -> None:\n'
start = test_text.find(start_marker)
end = test_text.find(end_marker)
if start < 0 or end < 0 or end <= start:
    raise AssertionError('bloco do guard de materialidade não encontrado')

replacement = r'''    def _required_minlength_without_material_text(self, schema: dict) -> list[str]:
        violations: list[str] = []

        def walk(node: object, path: tuple[str, ...] = ()) -> None:
            if isinstance(node, dict):
                if node.get("type") == "string" and "minLength" in node:
                    if node.get("format") != "material-text":
                        violations.append(".".join(path))
                for key, value in node.items():
                    walk(value, path + (str(key),))
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, path + (str(index),))

        walk(schema)
        return violations

    def test_required_minlength_text_fields_have_explicit_material_policy(self) -> None:
        self.assertEqual([], self._required_minlength_without_material_text(self.schema))

    def test_generic_textual_pattern_cannot_replace_material_text(self) -> None:
        mutated = copy.deepcopy(self.schema)
        mutated["$defs"]["synthetic_textual_escape"] = {
            "type": "string",
            "minLength": 3,
            "pattern": r".*\S.*",
        }
        self.assertIn(
            "$defs.synthetic_textual_escape",
            self._required_minlength_without_material_text(mutated),
        )

    def test_schema_patterns_are_exact_structural_allowlist(self) -> None:
        expected = {
            "$defs.id": r"^[a-z][a-z0-9_]{2,63}$",
            "properties.identidade.properties.nome": r"^[a-z][a-z0-9-]{2,63}$",
            "properties.identidade.properties.micromodel_version": r"^\d+\.\d+\.\d+$",
        }
        observed: dict[str, str] = {}

        def walk(node: object, path: tuple[str, ...] = ()) -> None:
            if isinstance(node, dict):
                joined = ".".join(path)
                if "pattern" in node:
                    observed[joined] = node["pattern"]
                self.assertFalse(
                    node.get("format") == "material-text" and "pattern" in node,
                    msg=f"autoridade textual concorrente em {joined}",
                )
                for key, value in node.items():
                    walk(value, path + (str(key),))
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    walk(value, path + (str(index),))

        walk(self.schema)
        self.assertEqual(expected, observed)

'''

test_text = test_text[:start] + replacement + test_text[end:]
TESTS.write_text(test_text, encoding='utf-8')

# 3) Documentação canônica e operacional.
readme = MM01_README.read_text(encoding='utf-8')
readme = replace_once(
    readme,
    'Status da sprint: **QUINTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` BLOQUEANTE CONFIRMADA E CORRIGIDA; RETESTE DE CONSTRUÇÃO VERDE; SEXTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    'Status da sprint: **SEXTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` E `DIVERGE-02` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO PENDENTE; SÉTIMA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    label='MM01 README status',
)
readme = readme.replace('suíte automatizada com **34 métodos**', 'suíte automatizada com **36 métodos**')
readme = readme.replace(
    'pacote de auditoria A1 com contexto, prompt e cinco resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);',
    'pacote de auditoria A1 com contexto, prompt e seis resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);',
)
needle = '''O contraditório confirmou a divergência. A correção reutiliza `material-text` nos demais textos obrigatórios do contrato e acrescenta uma invariável estrutural para impedir novos `string + minLength` sem política explícita. `governanca.observacoes[]` permanece narrativa opcional. A suíte passa a **34 métodos**.\n\n## Fronteiras preservadas'''
replacement_doc = '''O contraditório confirmou a divergência. A correção reutiliza `material-text` nos demais textos obrigatórios do contrato e acrescenta uma invariável estrutural para impedir novos `string + minLength` sem política explícita. `governanca.observacoes[]` permanece narrativa opcional. A suíte passou a **34 métodos**.\n\n### Sexta A1\n\nA sexta auditoria independente sobre `e0b6ed916386bef19006e7d41e183ffde25e360a` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com duas divergências bloqueantes. `DIVERGE-01` mostrou três regex genéricas `.*\\S.*` ainda concorrendo com `material-text`; `DIVERGE-02` mostrou que o guard permanente aceitava qualquer `pattern` como política suficiente. O resultado histórico permanece em `08_resultado_a1_reauditoria_5.md`.\n\nO contraditório confirmou ambos os achados. A correção remove as três regex textuais genéricas, exige `material-text` em todo `type=string + minLength` e congela os únicos patterns remanescentes por path e regex exata como contratos estruturais. Um adversarial sintético prova que `minLength + pattern: .*\\S.*` sem `material-text` é violação. A suíte passa a **36 métodos**.\n\n## Fronteiras preservadas'''
readme = replace_once(readme, needle, replacement_doc, label='MM01 README sexta A1')
readme = readme.replace('A suíte MM01 possui **34 métodos automatizados**', 'A suíte MM01 possui **36 métodos automatizados**')
readme = replace_once(
    readme,
    'Como o contrato mudou materialmente depois da quinta A1, a MM01 só pode ser aceita após uma **sexta A1 independente** sobre o novo HEAD congelado.',
    'Como o contrato mudou materialmente depois da sexta A1, a MM01 só pode ser aceita após uma **sétima A1 independente** sobre o novo HEAD congelado.',
    label='MM01 README gate',
)
readme = readme.replace('após uma sexta A1 limpa e contraditório final', 'após uma sétima A1 limpa e contraditório final')
readme = readme.replace('até sexta A1, eventual contraditório', 'até sétima A1, eventual contraditório')
MM01_README.write_text(readme, encoding='utf-8')

checkpoint = CHECKPOINT.read_text(encoding='utf-8')
checkpoint = replace_once(
    checkpoint,
    'Status: **QUINTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` BLOQUEANTE CONFIRMADA E CORRIGIDA; RETESTE DE CONSTRUÇÃO VERDE; SEXTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    'Status: **SEXTA A1 `APTA_COM_CORRECOES`; `DIVERGE-01` E `DIVERGE-02` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO PENDENTE; SÉTIMA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    label='CHECKPOINT status',
)
checkpoint = checkpoint.replace('suíte com **34 métodos de teste**', 'suíte com **36 métodos de teste**')
checkpoint = checkpoint.replace('resultados históricos das cinco A1 preservados', 'resultados históricos das seis A1 preservados')
insert = '''\n## Sexta auditoria A1\n\nA sexta A1 independente sobre `e0b6ed916386bef19006e7d41e183ffde25e360a` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`. Dois desvios bloqueantes foram confirmados: três `pattern: ".*\\\\S.*"` ainda competiam com `material-text`, e o guard de `string + minLength` considerava qualquer `pattern` suficiente. O relatório foi preservado em `08_resultado_a1_reauditoria_5.md`.\n\n## Correções da sexta A1\n\nA correção remove as três regex textuais genéricas e deixa `_has_material_text` → `format: material-text` como única autoridade de conteúdo material. Os únicos patterns remanescentes são contratos de estrutura (`$defs.id`, `identidade.nome` e `micromodel_version`) e ficam congelados por path + regex exata em regressão permanente. Todo `type=string + minLength` passa a exigir `material-text`; um nó sintético `minLength + pattern: .*\\\\S.*` sem format deve ser detectado como violação. A suíte passa a **36 métodos**.\n'''
checkpoint = replace_once(checkpoint, '\n## Dívida documental antes do merge\n', insert + '\n## Dívida documental antes do merge\n', label='CHECKPOINT sexta A1')
checkpoint = replace_once(
    checkpoint,
    'Como a candidata mudou materialmente após a quinta A1, é obrigatória uma **sexta A1 independente** sobre o novo HEAD congelado.',
    'Como a candidata mudou materialmente após a sexta A1, é obrigatória uma **sétima A1 independente** sobre o novo HEAD congelado.',
    label='CHECKPOINT gate independente',
)
checkpoint = checkpoint.replace('executar sexta A1 em sessão independente', 'executar sétima A1 em sessão independente')
checkpoint = checkpoint.replace('se a sexta A1 for limpa', 'se a sétima A1 for limpa')
CHECKPOINT.write_text(checkpoint, encoding='utf-8')

testes = TESTES_MD.read_text(encoding='utf-8')
testes = replace_once(
    testes,
    '| T49 | todo `type=string` + `minLength` possui `material-text`, `pattern` ou exceção narrativa explícita | invariável estrutural |',
    '| T49 | todo `type=string` + `minLength` possui `material-text` | invariável estrutural fail-closed |\n| T50 | qualquer `pattern` do schema pertence à allowlist estrutural exata por path + regex | invariável estrutural |\n| T51 | nó sintético `string + minLength + pattern: .*\\\\S.*` sem `material-text` | detectado como violação |',
    label='TESTES matriz T49',
)
testes = testes.replace('contém **34 métodos de teste**', 'contém **36 métodos de teste**')
testes += '''\n\n## Sexta A1 — `APTA_COM_CORRECOES`\n\nA sexta auditoria independente identificou duas divergências bloqueantes preservadas em `08_resultado_a1_reauditoria_5.md`: três regex genéricas `.*\\S.*` ainda coexistiam com `material-text`, e o guard estrutural aceitava qualquer `pattern` como política suficiente.\n\n### Correção da sexta A1\n\n- removidos os três `pattern: ".*\\\\S.*"` concorrentes de proveniência/aprovação;\n- todo `type=string + minLength` passa a exigir `format: material-text`;\n- os patterns remanescentes são congelados por allowlist exata de path + regex e correspondem somente a ID interno, nome técnico e versão;\n- um adversarial sintético prova que `minLength + pattern: .*\\\\S.*` sem `material-text` não satisfaz a invariável;\n- a suíte passa a **36 métodos**, preservando os adversariais Unicode e os caminhos positivos multilíngues.\n\nO próximo gate é uma sétima A1 independente sobre o HEAD permanente corrigido.\n'''
TESTES_MD.write_text(testes, encoding='utf-8')

contrato = CONTRATO.read_text(encoding='utf-8')
old_contract = '''A quinta A1 mostrou que a distinção entre texto material e narrativa livre precisava ser explícita. Todo campo textual obrigatório protegido por `minLength` deve ter uma política executável: `format: material-text`, quando participa da definição canônica, ou `pattern`, quando a sintaxe fechada já exige conteúdo material. A autoridade de materialidade continua sendo exclusivamente `_has_material_text` após NFKC; não há regex, `.strip()` ou segundo predicado concorrente.'''
new_contract = '''A quinta A1 mostrou que a distinção entre texto material e narrativa livre precisava ser explícita. Após a sexta A1, a classificação ficou fail-closed: todo `type=string` protegido por `minLength` deve usar `format: material-text`. Regex não substitui materialidade. `pattern` permanece somente em contratos estritamente estruturais e é congelado por path + expressão exata (`$defs.id`, `identidade.nome` e `micromodel_version`). A autoridade de materialidade é exclusivamente `_has_material_text` após NFKC; não há regex genérica, `.strip()` ou segundo predicado concorrente.'''
contrato = replace_once(contrato, old_contract, new_contract, label='CONTRATO política')
contrato += '''\n\n### Hardening após a sexta A1\n\nA sexta A1 encontrou três ocorrências residuais de `pattern: ".*\\\\S.*"` nos campos materiais `proveniencia.origem`, `proveniencia.aprovacao.por` e `validacao.aprovacao_humana.por`, além de um guard que tratava qualquer `pattern` como suficiente. Esses caminhos foram removidos. A regressão permanente agora exige `material-text` para `string + minLength`, rejeita explicitamente um pattern textual genérico sintético e compara todos os patterns existentes com uma allowlist estrutural exata. `governanca.observacoes[]` continua narrativa opcional e sem função de gate.\n'''
CONTRATO.write_text(contrato, encoding='utf-8')

index = MICRO_INDEX.read_text(encoding='utf-8')
old_state_start = index.split('\n', 3)[2]
if not old_state_start.startswith('> Estado: '):
    raise AssertionError('linha de estado do índice de micromodelos não encontrada')
new_state = '> Estado: **MM00 encerrada e integrada. MM01 passou por seis A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`); os dois desvios bloqueantes da sexta A1 foram confirmados e corrigidos; reteste e sétima A1 independentes pendentes. MM01 ainda não aceita nem integrada.**'
index = index.replace(old_state_start, new_state, 1)
index = index.replace('suíte com **31 métodos de teste**', 'suíte com **36 métodos de teste**')
anchor = '\nA skill roteável `hub-ml-micromodelos` continua reservada para MM04;'
new_history = '''\n### Quinta e sexta A1\n\nA quinta A1 concluiu `APTA_COM_CORRECOES` e levou a política `material-text` aos demais textos obrigatórios, elevando a suíte a 34 métodos. A sexta A1, também `APTA_COM_CORRECOES`, encontrou duas sobras da mesma classe: três regex genéricas concorrentes e um guard que aceitava qualquer `pattern`. O sexto relatório está preservado em `08_resultado_a1_reauditoria_5.md`.\n\nA correção da sexta A1 remove as regex genéricas, exige `material-text` em todo `string + minLength` e congela os únicos patterns estruturais por path + regex exata. A suíte passa a 36 métodos.\n'''
index = replace_once(index, anchor, new_history + anchor, label='índice histórico A1')
start_gate = index.find('## Próximo gate\n')
if start_gate < 0:
    raise AssertionError('Próximo gate não encontrado no índice')
index = index[:start_gate] + '''## Próximo gate\n\n1. concluir o reteste de construção e obter os workflows permanentes verdes no HEAD corrigido;\n2. executar uma **sétima A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;\n3. confrontar qualquer novo achado e corrigir somente se procedente;\n4. se a sétima A1 for limpa, executar contraditório final;\n5. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;\n6. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;\n7. integrar a PR #51 somente após o aceite.\n\n**MM02 permanece bloqueada.**\n'''
MICRO_INDEX.write_text(index, encoding='utf-8')

root = ROOT_README.read_text(encoding='utf-8')
root = replace_once(
    root,
    'repo (identidade)  : 1426 arquivos varridos no repositório editável/derivado',
    'repo (identidade)  : 1427 arquivos varridos no repositório editável/derivado',
    label='README métrica',
)
ROOT_README.write_text(root, encoding='utf-8')

print('Correção sexta A1 aplicada: schema, guard, regressões e documentação sincronizados.')
