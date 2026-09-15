from __future__ import annotations

from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: esperado 1 anchor, encontrado {count}")
    return text.replace(old, new, 1)

# TESTES.md
path = "docs/sprints/micromodelos/MM01/TESTES.md"
text = read(path)
text = replace_once(text,
    "| T44 | proveniência de topo e gates materiais usam a mesma política Unicode | rejeição/aceite coerentes |\n",
    "| T44 | proveniência de topo e gates materiais usam a mesma política Unicode | rejeição/aceite coerentes |\n"
    "| T45 | regras de evidência, hipótese/resultado experimental, resumo de validação e motivo operacional não materiais | `SCHEMA` / gate fail-closed |\n"
    "| T46 | os mesmos campos normativos com conteúdo Unicode legítimo multilíngue | APROVADO |\n",
    "TESTES matriz round4")
text = replace_once(text,
    "A suíte `tools/tests/test_micromodelo_mm01.py` contém **29 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz.",
    "A suíte `tools/tests/test_micromodelo_mm01.py` contém **31 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz.",
    "TESTES contagem")
old_tail = '''## Próxima auditoria A1

Uma **quarta auditoria A1 independente** é obrigatória porque a candidata mudou materialmente depois da terceira A1. Ela deve trabalhar sobre o novo HEAD congelado e não pode usar os relatórios anteriores, a narrativa do autor, o changelog ou mensagens de commit como prova.

A quarta A1 deve repetir instalação, 29 testes, gate estrutural, CLI direta e adversariais próprios; verificar simultaneamente falsos positivos e falsos negativos Unicode; cobrir todos os campos equivalentes; confirmar a unicidade da autoridade de materialidade; validar `--previous`; e confirmar que MM01 não antecipou MM02/MM03/MM04/MM06.

MM02 permanece bloqueada até nova A1, contraditório se necessário, fechamento do changelog, aceite explícito e integração da MM01.
'''
new_tail = '''## Quarta A1 — `APTA_COM_CORRECOES`

A quarta auditoria independente sobre `c0b6f5872f47f8e37ed8f55f262c276b8c105063` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência bloqueante: a autoridade comum `material-text` já era única, porém campos normativos/materialmente decisivos equivalentes ainda dependiam apenas de `minLength` ou `.strip()`.

O achado alcançou `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao`. O resultado histórico está preservado em `06_resultado_a1_reauditoria_3.md` e não é reclassificado pelas correções posteriores.

### Reteste das correções da quarta A1

A correção reutilizou exclusivamente a autoridade existente `material-text` → `_has_material_text`:

- os seis campos citados passaram a usar `format: material-text` no schema;
- os gates semânticos de resultado `EXECUTADO` e motivo de condição não `ATIVO` deixaram de usar `.strip()` e passaram a chamar `_has_material_text`;
- a suíte ganhou adversariais permanentes para `Mn`, `Mc`, `Me`, `Cf`, zero-width, espaços Unicode, pontuação, símbolos e combinações, além de caminhos positivos multilíngues.

O run transitório `34960256357` removeu seus próprios mecanismos e concluiu com sucesso **31 métodos**, CLI direta positiva/negativa/`--previous`, `validate_assistant`, métrica congelada e invariantes históricos antes de publicar o commit permanente `8fd8e7892ead1bb63a554b5283f7062adf582976`.

## Próxima auditoria A1

Uma **quinta auditoria A1 independente** é obrigatória porque a candidata mudou materialmente depois da quarta A1. Ela deve auditar o HEAD efetivamente encontrado e não pode usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova.

A quinta A1 deve repetir instalação, 31 testes, gate estrutural, CLI direta e adversariais próprios; testar isoladamente todos os seis campos corrigidos com `Mn/Mc/Me`, `Cf`, zero-width, espaços Unicode, pontuação, símbolos e combinações; confirmar positivos multilíngues; provar que não surgiu uma segunda autoridade de materialidade; validar `--previous`; e confirmar as fronteiras MM02/MM03/MM04/MM06.

MM02 permanece bloqueada até nova A1, contraditório se necessário, fechamento do changelog, aceite explícito e integração da MM01.
'''
text = replace_once(text, old_tail, new_tail, "TESTES quinta A1")
write(path, text)

# CHECKPOINT.md
path = "docs/sprints/micromodelos/MM01/CHECKPOINT.md"
text = read(path)
text = replace_once(text,
    "Status: **TERCEIRA A1 `APTA_COM_CORRECOES`; TRÊS DIVERGÊNCIAS CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; QUARTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status: **QUARTA A1 `APTA_COM_CORRECOES`; DIVERGÊNCIA BLOQUEANTE CORRIGIDA; RETESTE DE CONSTRUÇÃO VERDE; QUINTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "CHECKPOINT status")
text = replace_once(text, "suíte com **29 métodos de teste**;", "suíte com **31 métodos de teste**;", "CHECKPOINT tests")
text = replace_once(text,
    "pacote neutro de auditoria com os resultados históricos das três A1 preservados, sem reclassificação retroativa.",
    "pacote neutro de auditoria com os resultados históricos das quatro A1 preservados, sem reclassificação retroativa.",
    "CHECKPOINT audits")
anchor = "## Dívida documental antes do merge\n"
insert = '''## Quarta auditoria A1

A quarta A1 independente sobre `c0b6f5872f47f8e37ed8f55f262c276b8c105063` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência bloqueante: seis campos normativos equivalentes ainda aceitavam conteúdo não material por `minLength` ou `.strip()`. O resultado está preservado em `06_resultado_a1_reauditoria_3.md`.

## Correções da quarta A1

A correção não criou nova heurística: `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao` passaram a usar a autoridade já existente `material-text`. Os gates semânticos de resultado executado e motivo operacional também passaram a chamar `_has_material_text` em vez de `.strip()`.

A suíte passou para **31 métodos**, incluindo negativos de `Mn/Mc/Me`, `Cf`, zero-width, whitespace Unicode, pontuação, símbolos e combinações, e positivos multilíngues. O run transitório `34960256357` executou suíte, CLI positiva/negativa/`--previous`, `validate_assistant`, conferência do README e invariantes históricos antes de publicar `8fd8e7892ead1bb63a554b5283f7062adf582976`; os mecanismos transitórios foram removidos.

'''
if anchor not in text:
    raise SystemExit("CHECKPOINT debt anchor ausente")
text = text.replace(anchor, insert + anchor, 1)
old_gate = '''## Gate independente pendente

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
new_gate = '''## Gate independente pendente

Como a candidata mudou materialmente após a quarta A1, é obrigatória uma **quinta A1 independente** sobre o novo HEAD congelado. O auditor deve repetir os gates mínimos e construir adversariais próprios, sem usar relatórios A1 anteriores, narrativa do autor, changelog ou mensagens de commit como prova da correção.

## Gates restantes

1. congelar e validar os workflows permanentes do HEAD documental final;
2. executar quinta A1 em sessão independente;
3. confrontar qualquer novo achado com a árvore e corrigir/retestar somente se procedente;
4. se a quinta A1 for `APTA`, executar contraditório final;
5. sincronizar o bloco MM01 do `CHANGELOG.md` preservando o histórico;
6. revalidar a árvore exata depois dessa sincronização e reconfirmar `main`/`behind_by`/mergeabilidade;
7. apresentar checkpoint final para aceite explícito;
8. integrar a PR #51 somente após o aceite.
'''
text = replace_once(text, old_gate, new_gate, "CHECKPOINT gate")
write(path, text)

# MM01 README
path = "docs/sprints/micromodelos/MM01/README.md"
text = read(path)
text = replace_once(text,
    "Status da sprint: **TERCEIRA A1 `APTA_COM_CORRECOES`; TRÊS DIVERGÊNCIAS CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; QUARTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status da sprint: **QUARTA A1 `APTA_COM_CORRECOES`; DIVERGÊNCIA BLOQUEANTE CORRIGIDA; RETESTE DE CONSTRUÇÃO VERDE; QUINTA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "MM01 README status")
text = replace_once(text, "suíte automatizada com **29 métodos**", "suíte automatizada com **31 métodos**", "MM01 README tests delivery")
text = replace_once(text,
    "pacote de auditoria A1 com contexto, prompt e três resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`);",
    "pacote de auditoria A1 com contexto, prompt e quatro resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);",
    "MM01 README audits")
old_material = "O JSON Schema usa `format: material-text` e o `FormatChecker` do validador delega esse formato à mesma função `_has_material_text`. Isso rejeita strings compostas somente por espaços, zero-width, variation selectors, combining marks isolados, pontuação ou símbolos nos campos materiais, sem rejeitar CJK, Devanagari, caracteres acentuados, algarismos Unicode ou combining marks acompanhados de texto material. Campos puramente narrativos não foram restringidos indiscriminadamente."
new_material = old_material + "\n\nA quarta A1 identificou seis campos normativos equivalentes que ainda escapavam dessa autoridade. `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao` agora usam o mesmo `material-text`; os gates de resultado executado e motivo operacional chamam `_has_material_text` em vez de `.strip()`."
text = replace_once(text, old_material, new_material, "MM01 README material")
anchor = "## Fronteiras preservadas\n"
insert = '''### Quarta A1

A quarta auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência bloqueante: a autoridade Unicode comum estava correta, mas seis campos normativos/materialmente decisivos equivalentes ainda aceitavam conteúdo não material por `minLength` ou `.strip()`.

O resultado histórico permanece em `06_resultado_a1_reauditoria_3.md`. A correção aplicou a mesma autoridade `material-text` aos seis campos, removeu `.strip()` dos dois gates materiais correspondentes e ampliou a suíte para **31 métodos**. O run `34960256357` validou a árvore sem seus mecanismos transitórios e só então publicou `8fd8e7892ead1bb63a554b5283f7062adf582976`.

'''
if anchor not in text:
    raise SystemExit("MM01 README frontier anchor ausente")
text = text.replace(anchor, insert + anchor, 1)
text = replace_once(text,
    "A suíte MM01 possui **29 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da terceira A1 ficou verde antes da publicação do commit permanente.",
    "A suíte MM01 possui **31 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da quarta A1 ficou verde antes da publicação do commit permanente.",
    "MM01 README evidence")
old_exit = '''Como o contrato mudou materialmente depois da terceira A1, a MM01 só pode ser aceita após uma **quarta A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e criar adversariais próprios, incluindo falsos positivos e falsos negativos Unicode, sem usar os relatórios anteriores, a narrativa do autor, o changelog ou mensagens de commit como prova.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma quarta A1 limpa e contraditório final. A árvore resultante deverá ser novamente validada.

**MM02 permanece bloqueada até quarta A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**
'''
new_exit = '''Como o contrato mudou materialmente depois da quarta A1, a MM01 só pode ser aceita após uma **quinta A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e criar adversariais próprios sobre todos os campos corrigidos, sem usar os relatórios anteriores, a narrativa do autor, o changelog ou mensagens de commit como prova.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma quinta A1 limpa e contraditório final. A árvore resultante deverá ser novamente validada.

**MM02 permanece bloqueada até quinta A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**
'''
text = replace_once(text, old_exit, new_exit, "MM01 README exit")
write(path, text)

# Initiative README
path = "docs/sprints/micromodelos/README.md"
text = read(path)
text = replace_once(text,
    "> Estado: **MM00 encerrada e integrada. MM01 passou por três A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`); as três divergências da terceira A1 foram corrigidas e o reteste de construção ficou verde; quarta A1 independente pendente. MM01 ainda não aceita nem integrada.**",
    "> Estado: **MM00 encerrada e integrada. MM01 passou por quatro A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`); a divergência bloqueante da quarta A1 foi corrigida e o reteste de construção ficou verde; quinta A1 independente pendente. MM01 ainda não aceita nem integrada.**",
    "initiative status")
text = replace_once(text, "suíte com **29 métodos de teste**", "suíte com **31 métodos de teste**", "initiative tests")
anchor = "Os três resultados A1 permanecem históricos e não são reclassificados depois das correções.\n"
insert = anchor + '''
### Quarta A1

A quarta auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência: regras de evidência/contra-evidência, hipótese/resultado experimental, resumo de validação e motivo operacional ainda escapavam da autoridade comum de materialidade. O resultado está preservado em `06_resultado_a1_reauditoria_3.md`.

A correção reutilizou `material-text` → `_has_material_text` nos seis campos e removeu `.strip()` dos gates de resultado executado e motivo de condição. A suíte passou para 31 métodos. O run transitório `34960256357` executou suíte, CLI adversarial, `--previous` e gates estruturais antes de publicar `8fd8e7892ead1bb63a554b5283f7062adf582976`; os mecanismos transitórios foram removidos.

Os quatro resultados A1 permanecem históricos e não são reclassificados depois das correções.
'''
text = replace_once(text, anchor, insert, "initiative fourth A1")
old_next = '''## Próximo gate

1. congelar o HEAD documental pós-terceira A1 e obter todos os workflows permanentes verdes;
2. executar uma **quarta A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;
3. confrontar qualquer novo achado e corrigir somente se procedente;
4. se a quarta A1 for `APTA`, executar contraditório final;
5. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
6. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;
7. integrar a PR #51 somente após o aceite.
'''
new_next = '''## Próximo gate

1. congelar o HEAD documental pós-quarta A1 e obter todos os workflows permanentes verdes;
2. executar uma **quinta A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;
3. confrontar qualquer novo achado e corrigir somente se procedente;
4. se a quinta A1 for `APTA`, executar contraditório final;
5. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
6. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;
7. integrar a PR #51 somente após o aceite.
'''
text = replace_once(text, old_next, new_next, "initiative next")
write(path, text)

# Contract doc
path = "docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md"
text = read(path)
old = "Consequentemente, whitespace, NBSP/EM SPACE, `Cf`, zero-width, variation selectors, combining marks isolados, pontuação e símbolos isolados não satisfazem um campo material. CJK, Devanagari, caracteres acentuados, algarismos Unicode e combining marks acompanhados de uma base material continuam válidos. Campos narrativos livres não recebem `material-text` apenas por serem strings."
new = old + "\n\nA mesma autoridade cobre também os campos normativos que satisfazem gates de evidência e validação: `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e, quando a condição não é `ATIVO`, `identidade.estado.motivo_condicao`. Resultado `EXECUTADO` e motivo operacional não possuem uma heurística paralela por `.strip()`; ambos usam `_has_material_text`."
text = replace_once(text, old, new, "contract normative material")
write(path, text)

# States/provenance doc
path = "docs/sprints/micromodelos/MM01/ESTADOS_E_PROVENIENCIA.md"
text = read(path)
old = "A política é positiva: após NFKC, deve existir pelo menos uma letra ou número Unicode. Marcas combinantes isoladas, zero-width, formatos invisíveis, whitespace, pontuação ou símbolos sem letra/número não constituem prova. Essa regra não altera a máquina de estados nem cria fingerprint; `--previous` continua sendo comparação explícita de snapshots fornecidos."
new = old + "\n\nA política também é aplicada aos campos normativos equivalentes que atravessam gates: regras de evidência e contra-evidência, hipótese e resultado de experimento, resumo do resultado de validação e motivo de condição operacional. Em especial, experimento `EXECUTADO` e condição não `ATIVO` são verificados por `_has_material_text`, não por `.strip()`."
text = replace_once(text, old, new, "states normative material")
write(path, text)

print("MM01 quarta A1: documentação sincronizada para quinta auditoria")
