from __future__ import annotations

from pathlib import Path

ROOT = Path('.')


def read(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding='utf-8')


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: esperado 1 anchor, encontrado {count}')
    return text.replace(old, new, 1)


# 1) Evidência histórica imutável da terceira A1. Não reclassifica auditorias anteriores.
report_path = 'docs/auditoria/2026-09-14_micromodelos-mm01/05_resultado_a1_reauditoria_2.md'
report = '''# MM01 — Terceira reauditoria independente A1

## Natureza deste registro

Este arquivo preserva o resultado histórico da terceira auditoria independente A1 da MM01. Ele registra o que o auditor concluiu na árvore examinada naquela rodada. Correções posteriores não alteram retroativamente este veredito e não transformam os achados abaixo em `PASS`.

## Veredito histórico

**VEREDITO: APTA_COM_CORRECOES**

- `QUEBRA`: 0
- divergências bloqueantes confirmadas: 3
- merge/aceite da MM01: não autorizado por esta auditoria

## DIVERGE-01 — `$defs.material_ref` exigia ASCII

O schema ainda usava uma regra equivalente a `.*[A-Za-z0-9].*`, enquanto o validador semântico aceitava letra ou número Unicode após NFKC. Isso criava duas autoridades incompatíveis para materialidade textual.

O auditor demonstrou falsos negativos multilíngues: referências legítimas como `é`, `文档`, `١` e texto em Devanagari eram rejeitadas pelo schema. Em contraste, uma forma como `Café`, contendo caracteres ASCII e combining mark, conseguia satisfazer a regex.

A correção exigida foi unificar a política: materialidade deve significar presença de pelo menos uma letra ou número Unicode real após normalização, sem ampliar uma regex ASCII como segunda fonte de verdade.

## DIVERGE-02 — proveniência de topo escapava da materialidade

Os campos auditáveis de proveniência de topo `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo` aceitavam conteúdo materialmente vazio.

Foram exercitados casos compostos por U+034F, U+FE0F, U+0301, U+093E isolado, U+20DD, U+200B, U+200C, U+200D, U+2060, NBSP, EM SPACE, pontuação, símbolos e combinações desses caracteres.

A correção exigida foi submeter esses campos à mesma política de materialidade apropriada às demais provas auditáveis.

## DIVERGE-03 — gates de conteúdo material aceitavam strings visualmente vazias

Campos materialmente relevantes ainda podiam satisfazer o schema apenas por `minLength`, inclusive com whitespace, pontuação pura, símbolos ou zero-width. O achado alcançou ao menos:

- `classificacao.semantica.quando_true`, `quando_false` e `quando_indeterminado`;
- `validacao.criterios[]`;
- `fontes[].schema`, `fontes[].objeto` e `fontes[].campos[]`;
- `saida.estudo.campo_classificacao`;
- `saida.estudo.campo_score`, quando aplicável;
- `saida.publicacao.campo_booleano.nome`.

O auditor também registrou que a restrição não deveria ser aplicada indiscriminadamente a toda string: campos narrativos podem legitimamente conter pontuação/símbolos, enquanto identificadores, referências, nomes operacionais, semânticas obrigatórias e critérios materiais precisam de conteúdo efetivo.

## Condição para nova auditoria

A candidata precisava corrigir as três divergências, manter suporte multilíngue real, preservar os guardrails anteriores e voltar a uma auditoria independente. Esta A1 não declarou a MM01 aprovada e não autorizou MM02.
'''
if Path(report_path).exists():
    if read(report_path) != report:
        raise SystemExit(f'{report_path}: arquivo já existe com conteúdo diferente')
else:
    write(report_path, report)

# 2) TESTES.md: matriz, contagem e cronologia.
path = 'docs/sprints/micromodelos/MM01/TESTES.md'
text = read(path)
text = replace_once(
    text,
    '| T41 | CI agregado da PR | regressão zero no head final técnico |\n',
    '| T41 | CI agregado da PR | regressão zero no head final técnico |\n'
    '| T42 | política `material-text`: marcas/formatos/whitespace/pontuação/símbolo isolados | `SCHEMA` |\n'
    '| T43 | materialidade Unicode positiva (`é`, CJK, algarismos Unicode, Devanagari, combining mark com base material) | APROVADO |\n'
    '| T44 | proveniência de topo e gates materiais usam a mesma política Unicode | rejeição/aceite coerentes |\n',
    label='TESTES matriz Unicode',
)
text = replace_once(
    text,
    'A suíte `tools/tests/test_micromodelo_mm01.py` contém **26 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz.',
    'A suíte `tools/tests/test_micromodelo_mm01.py` contém **29 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz.',
    label='TESTES contagem',
)
old_tail = '''## Próxima auditoria A1

Uma **terceira auditoria A1 independente** é obrigatória porque a candidata mudou materialmente depois da segunda A1. Ela deve trabalhar sobre o próximo HEAD congelado e não pode reutilizar como prova os relatórios `03_resultado_a1.md` ou `04_resultado_a1_reauditoria.md`.

Deve repetir instalação, 26+ testes, gate estrutural, CLI direta do template e adversariais próprios sobre: marcas Unicode `M*`, ausência de prosa normativa, políticas de `INDETERMINADO`, semântica probabilística estruturada, integridade da calibração e continuidade histórica por `--previous`.

MM02 permanece bloqueada até nova A1, contraditório se necessário, aceite explícito e integração da MM01.
'''
new_tail = '''## Terceira A1 — `APTA_COM_CORRECOES`

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, e registrou três divergências bloqueantes de materialidade textual/Unicode:

1. `$defs.material_ref` impunha ASCII no schema enquanto o validador aceitava letra/número Unicode;
2. `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo` escapavam da política material;
3. semânticas obrigatórias, critérios, nomes de fonte e campos de saída podiam satisfazer gates com whitespace, zero-width, pontuação ou símbolos sem conteúdo material.

O resultado histórico está versionado em `05_resultado_a1_reauditoria_2.md` e permanece `APTA_COM_CORRECOES`, independentemente das correções posteriores.

### Reteste das correções da terceira A1

O mecanismo transitório foi executado novamente no run `34955861169`. Antes de publicar qualquer artefato permanente, ele removeu seus próprios arquivos e concluiu com sucesso:

- instalação por `python -m pip install -r tools/requirements-dev.txt`;
- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`, com **29 métodos**;
- CLI direta sobre template, fixture positiva, caso Unicode positivo, caso Unicode negativo e continuidade por `--previous`;
- `python -B tools/validate_assistant.py --root ambiente_fonte`;
- publicação do commit permanente `4f686e5de163b649c4ee5e7643f75ecd56db47e7`.

Esse reteste é evidência de construção. A candidata documental final ainda precisa dos workflows permanentes verdes no SHA exato e de uma nova auditoria independente.

## Próxima auditoria A1

Uma **quarta auditoria A1 independente** é obrigatória porque a candidata mudou materialmente depois da terceira A1. Ela deve trabalhar sobre o novo HEAD congelado e não pode usar os relatórios anteriores, a narrativa do autor, o changelog ou mensagens de commit como prova.

A quarta A1 deve repetir instalação, 29 testes, gate estrutural, CLI direta e adversariais próprios; verificar simultaneamente falsos positivos e falsos negativos Unicode; cobrir todos os campos equivalentes; confirmar a unicidade da autoridade de materialidade; validar `--previous`; e confirmar que MM01 não antecipou MM02/MM03/MM04/MM06.

MM02 permanece bloqueada até nova A1, contraditório se necessário, fechamento do changelog, aceite explícito e integração da MM01.
'''
text = replace_once(text, old_tail, new_tail, label='TESTES próxima A1')
write(path, text)

# 3) CHECKPOINT.md.
path = 'docs/sprints/micromodelos/MM01/CHECKPOINT.md'
text = read(path)
text = replace_once(
    text,
    'Status: **CORRIGIDA APÓS SEGUNDA A1; RETESTE DE CONSTRUÇÃO VERDE; TERCEIRA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    'Status: **TERCEIRA A1 `APTA_COM_CORRECOES`; TRÊS DIVERGÊNCIAS CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; QUARTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    label='CHECKPOINT status',
)
text = replace_once(text, 'suíte com **26 métodos de teste**;', 'suíte com **29 métodos de teste**;', label='CHECKPOINT contagem')
text = replace_once(
    text,
    'pacote neutro de auditoria com os resultados históricos da primeira e segunda A1 preservados.',
    'pacote neutro de auditoria com os resultados históricos das três A1 preservados, sem reclassificação retroativa.',
    label='CHECKPOINT pacote A1',
)
anchor = '## Dívida documental antes do merge\n'
insert = '''## Terceira auditoria A1

A terceira A1 independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: autoridade ASCII conflitante em `$defs.material_ref`, campos de proveniência de topo fora da política material e gates de conteúdo material aceitando strings visualmente vazias. O resultado histórico foi preservado em `05_resultado_a1_reauditoria_2.md`.

## Correções da terceira A1

A política de materialidade foi unificada sem ampliar o escopo da MM01:

- `_has_material_text` continua a autoridade Unicode: NFKC seguido da exigência de pelo menos uma categoria Unicode `L*` ou `N*`;
- o JSON Schema usa `format: material-text`, registrado no `FormatChecker` do próprio validador e delegado à mesma função;
- referências, proveniência material, semânticas obrigatórias, critérios, nomes de fontes e campos operacionais relevantes usam essa autoridade;
- prosa narrativa livre não recebeu a restrição indiscriminadamente;
- CJK, árabe/algarismos Unicode, Devanagari, caracteres acentuados e combining marks acompanhados de base material permanecem válidos.

O run transitório `34955861169` executou a suíte ampliada, CLI positiva/negativa/`--previous` e `validate_assistant` antes de publicar `4f686e5de163b649c4ee5e7643f75ecd56db47e7`. O mecanismo transitório não permaneceu na árvore candidata.

'''
if anchor not in text:
    raise SystemExit('CHECKPOINT anchor dívida não encontrado')
text = text.replace(anchor, insert + anchor, 1)
old_gate = '''## Gate independente pendente

Como a candidata mudou materialmente após a segunda A1, é obrigatória uma **terceira A1 independente** sobre o próximo HEAD congelado. O auditor deve repetir os gates mínimos e construir adversariais próprios, sem usar `03_resultado_a1.md` ou `04_resultado_a1_reauditoria.md` como prova da correção.

## Gates restantes

1. congelar e validar os workflows permanentes do HEAD documental final;
2. executar terceira A1 em sessão independente;
3. confrontar qualquer novo achado com a árvore e corrigir/retestar somente se procedente;
4. sincronizar o bloco MM01 do `CHANGELOG.md` preservando o histórico;
5. revalidar a árvore exata depois dessa sincronização;
6. apresentar checkpoint final para aceite explícito;
7. integrar a PR #51 somente após o aceite.
'''
new_gate = '''## Gate independente pendente

Como a candidata mudou materialmente após a terceira A1, é obrigatória uma **quarta A1 independente** sobre o novo HEAD congelado. O auditor deve repetir os gates mínimos e construir adversariais próprios, sem usar os relatórios A1 anteriores, narrativa do autor, changelog ou mensagens de commit como prova da correção.

## Gates restantes

1. congelar e validar os workflows permanentes do HEAD documental final;
2. executar quarta A1 em sessão independente;
3. confrontar qualquer novo achado com a árvore e corrigir/retestar somente se procedente;
4. se a quarta A1 for `APTA`, executar contraditório final;
5. sincronizar o bloco MM01 do `CHANGELOG.md` preservando o histórico;
6. revalidar a árvore exata depois dessa sincronização e reconfirmar `main`/`behind_by`/mergeabilidade;
7. apresentar checkpoint final para aceite explícito;
8. integrar a PR #51 somente após o aceite.
'''
text = replace_once(text, old_gate, new_gate, label='CHECKPOINT gate quarta A1')
write(path, text)

# 4) README da MM01.
path = 'docs/sprints/micromodelos/MM01/README.md'
text = read(path)
text = replace_once(
    text,
    'Status da sprint: **CORRIGIDA APÓS SEGUNDA A1; RETESTE DE CONSTRUÇÃO VERDE; TERCEIRA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    'Status da sprint: **TERCEIRA A1 `APTA_COM_CORRECOES`; TRÊS DIVERGÊNCIAS CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; QUARTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**',
    label='MM01 README status',
)
text = replace_once(text, 'suíte automatizada com **26 métodos** e múltiplos subtests;', 'suíte automatizada com **29 métodos** e múltiplos subtests;', label='MM01 README contagem entrega')
text = replace_once(
    text,
    'pacote de auditoria A1 com contexto, prompt e os dois resultados históricos `NAO_APTA`;',
    'pacote de auditoria A1 com contexto, prompt e três resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`);',
    label='MM01 README pacote A1',
)
text = replace_once(
    text,
    'A segunda A1 demonstrou que uma blacklist de whitespace/controles não era suficiente para caracteres Unicode `M*`. A regra atual é positiva: após NFKC, uma referência auditável precisa conter ao menos uma letra ou número Unicode.\n\nIsso rejeita strings compostas somente por espaços, zero-width, variation selectors, COMBINING GRAPHEME JOINER ou outros combining marks isolados em aprovação, medição, handoff e referência de Produto de Dados.',
    'A segunda A1 demonstrou que uma blacklist de whitespace/controles não era suficiente para caracteres Unicode `M*`. A terceira A1 mostrou que schema e validador ainda podiam divergir e que campos materiais equivalentes não compartilhavam a mesma autoridade. A regra atual é positiva e única: após NFKC, conteúdo material precisa conter ao menos uma letra ou número Unicode.\n\nO JSON Schema usa `format: material-text` e o `FormatChecker` do validador delega esse formato à mesma função `_has_material_text`. Isso rejeita strings compostas somente por espaços, zero-width, variation selectors, combining marks isolados, pontuação ou símbolos nos campos materiais, sem rejeitar CJK, Devanagari, caracteres acentuados, algarismos Unicode ou combining marks acompanhados de texto material. Campos puramente narrativos não foram restringidos indiscriminadamente.',
    label='MM01 README política Unicode',
)
anchor = '## Fronteiras preservadas\n'
insert = '''### Terceira A1

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: `$defs.material_ref` ainda impunha ASCII no schema, campos auditáveis de proveniência de topo escapavam da materialidade e alguns gates de conteúdo material podiam ser satisfeitos por strings visualmente vazias.

O resultado histórico permanece em `05_resultado_a1_reauditoria_2.md`. As três divergências foram corrigidas por uma autoridade Unicode única e testes positivos/negativos multilíngues. O run de construção `34955861169` removeu os mecanismos transitórios, executou suíte, CLI adversarial e `validate_assistant`, e só então publicou o commit permanente `4f686e5de163b649c4ee5e7643f75ecd56db47e7`.

'''
if anchor not in text:
    raise SystemExit('MM01 README anchor fronteiras não encontrado')
text = text.replace(anchor, insert + anchor, 1)
text = replace_once(
    text,
    'A suíte MM01 possui **26 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da segunda A1 ficou verde antes da publicação do commit permanente.',
    'A suíte MM01 possui **29 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da terceira A1 ficou verde antes da publicação do commit permanente.',
    label='MM01 README evidência atual',
)
old_gate = '''Como o contrato mudou materialmente depois da segunda A1, a MM01 só pode ser aceita após uma **terceira A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e criar adversariais próprios sem usar os relatórios anteriores como prova.

O bloco MM01 do `CHANGELOG.md` também precisa ser sincronizado antes do merge por operação preservadora do histórico e a árvore resultante deve ser novamente validada.

**MM02 permanece bloqueada até terceira A1, eventual contraditório, fechamento documental, aceite explícito e integração da MM01.**
'''
new_gate = '''Como o contrato mudou materialmente depois da terceira A1, a MM01 só pode ser aceita após uma **quarta A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e criar adversariais próprios, incluindo falsos positivos e falsos negativos Unicode, sem usar os relatórios anteriores, a narrativa do autor, o changelog ou mensagens de commit como prova.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma quarta A1 limpa e contraditório final. A árvore resultante deverá ser novamente validada.

**MM02 permanece bloqueada até quarta A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**
'''
text = replace_once(text, old_gate, new_gate, label='MM01 README gate')
write(path, text)

# 5) README da iniciativa.
path = 'docs/sprints/micromodelos/README.md'
text = read(path)
text = replace_once(
    text,
    '> Estado: **MM00 encerrada e integrada. MM01 corrigida após duas auditorias A1 `NAO_APTA`; reteste de construção da segunda correção verde; terceira A1 independente pendente. MM01 ainda não aceita nem integrada.**',
    '> Estado: **MM00 encerrada e integrada. MM01 passou por três A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`); as três divergências da terceira A1 foram corrigidas e o reteste de construção ficou verde; quarta A1 independente pendente. MM01 ainda não aceita nem integrada.**',
    label='README iniciativa status',
)
text = replace_once(text, 'suíte com **26 métodos de teste**', 'suíte com **29 métodos de teste**', label='README iniciativa contagem')
anchor = 'A skill roteável `hub-ml-micromodelos` continua reservada para MM04;'
insert = '''### Terceira A1

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências de materialidade textual/Unicode: conflito ASCII no schema, proveniência de topo fora da política material e gates operacionais que aceitavam strings visualmente vazias. O resultado está preservado em `05_resultado_a1_reauditoria_2.md`.

A terceira correção unificou a autoridade em NFKC + letra/número Unicode por `format: material-text`, sem impor essa restrição a toda prosa narrativa. O run transitório `34955861169` executou 29 métodos, CLI positiva/negativa/`--previous` e o gate estrutural antes de publicar `4f686e5de163b649c4ee5e7643f75ecd56db47e7`; os mecanismos transitórios foram removidos.

Os três resultados A1 permanecem históricos e não são reclassificados depois das correções.

'''
if anchor not in text:
    raise SystemExit('README iniciativa anchor skill não encontrado')
text = text.replace(anchor, insert + anchor, 1)
old_gate = '''## Próximo gate

1. congelar o HEAD documental pós-segunda A1 e obter todos os workflows permanentes verdes;
2. executar uma **terceira A1 independente** sobre esse HEAD, sem usar os relatórios anteriores como prova;
3. confrontar qualquer novo achado e corrigir somente se procedente;
4. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
5. revalidar a árvore exata após o changelog;
6. solicitar aceite final e integrar a PR #51.

**MM02 permanece bloqueada.**
'''
new_gate = '''## Próximo gate

1. congelar o HEAD documental pós-terceira A1 e obter todos os workflows permanentes verdes;
2. executar uma **quarta A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;
3. confrontar qualquer novo achado e corrigir somente se procedente;
4. se a quarta A1 for `APTA`, executar contraditório final;
5. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
6. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;
7. integrar a PR #51 somente após o aceite.

**MM02 permanece bloqueada.**
'''
text = replace_once(text, old_gate, new_gate, label='README iniciativa próximo gate')
write(path, text)

# 6) Documentação técnica: adicionar a regra unificada sem reescrever seções históricas.
for path, section in {
    'docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md': '''\n## Autoridade única de materialidade textual Unicode\n\nCampos materiais — referências auditáveis, proveniência material, nomes operacionais, semânticas obrigatórias e critérios — são validados pelo formato customizado `material-text`. O `FormatChecker` do JSON Schema não contém uma segunda heurística: ele delega à mesma `_has_material_text` usada pelos gates semânticos. A regra normaliza por NFKC e exige ao menos um caractere cuja categoria Unicode comece por `L` ou `N`.\n\nConsequentemente, whitespace, NBSP/EM SPACE, `Cf`, zero-width, variation selectors, combining marks isolados, pontuação e símbolos isolados não satisfazem um campo material. CJK, Devanagari, caracteres acentuados, algarismos Unicode e combining marks acompanhados de uma base material continuam válidos. Campos narrativos livres não recebem `material-text` apenas por serem strings.\n''',
    'docs/sprints/micromodelos/MM01/ESTADOS_E_PROVENIENCIA.md': '''\n## Materialidade das provas e da proveniência\n\nA proveniência só serve como evidência auditável quando seus campos materiais possuem conteúdo efetivo. A MM01 aplica a autoridade Unicode compartilhada (`material-text` → `_has_material_text`) tanto às referências aninhadas quanto a `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo`.\n\nA política é positiva: após NFKC, deve existir pelo menos uma letra ou número Unicode. Marcas combinantes isoladas, zero-width, formatos invisíveis, whitespace, pontuação ou símbolos sem letra/número não constituem prova. Essa regra não altera a máquina de estados nem cria fingerprint; `--previous` continua sendo comparação explícita de snapshots fornecidos.\n''',
}.items():
    text = read(path)
    marker = section.splitlines()[1]
    if marker not in text:
        if not text.endswith('\n'):
            text += '\n'
        text += section
        write(path, text)

print('MM01 terceira A1: documentação e evidência histórica sincronizadas')
