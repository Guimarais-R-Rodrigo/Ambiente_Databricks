from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: esperado 1 match, encontrado {count}")
    write(path, text.replace(old, new, 1))


def replace_line_prefix(path: Path, prefix: str, new_line: str, label: str) -> None:
    lines = read(path).splitlines()
    indexes = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(indexes) != 1:
        raise SystemExit(f"{label}: esperado 1 linha, encontrado {len(indexes)}")
    lines[indexes[0]] = new_line
    write(path, "\n".join(lines) + "\n")


def insert_before(path: Path, marker: str, block: str, label: str) -> None:
    text = read(path)
    if block.strip() in text:
        raise SystemExit(f"{label}: bloco já existe")
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{label}: marcador esperado 1 vez, encontrado {count}")
    write(path, text.replace(marker, block.rstrip() + "\n\n" + marker, 1))


def replace_tail(path: Path, marker: str, new_tail: str, label: str) -> None:
    text = read(path)
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{label}: marcador esperado 1 vez, encontrado {count}")
    prefix = text.split(marker, 1)[0]
    write(path, prefix + new_tail.rstrip() + "\n")


mm01 = ROOT / "docs" / "sprints" / "micromodelos" / "MM01"
mm01_readme = mm01 / "README.md"
checkpoint = mm01 / "CHECKPOINT.md"
tests_doc = mm01 / "TESTES.md"
contract_doc = mm01 / "CONTRATO_MICROMODELO.md"
states_doc = mm01 / "ESTADOS_E_PROVENIENCIA.md"
index = ROOT / "docs" / "sprints" / "micromodelos" / "README.md"

replace_line_prefix(
    mm01_readme,
    "Status da sprint:",
    "Status da sprint: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "README status",
)
replace_once(
    mm01_readme,
    "`tools/tests/test_micromodelo_mm01.py`: suíte automatizada com **36 métodos** e múltiplos subtests;",
    "`tools/tests/test_micromodelo_mm01.py`: suíte automatizada com **39 métodos** e múltiplos subtests;",
    "README test count",
)
replace_line_prefix(
    mm01_readme,
    "- pacote de auditoria A1 com contexto, prompt e seis resultados históricos preservados",
    "- pacote de auditoria A1 com contexto, prompt e sete resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);",
    "README audit count",
)
insert_before(
    mm01_readme,
    "## Fronteiras preservadas",
    """### Sétima A1

A sétima auditoria independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes. `DIVERGE-01` demonstrou bypass da equivalência `FALSE` × `INDETERMINADO` por caracteres Unicode default-ignorable inseridos dentro de palavras; `DIVERGE-02` mostrou que o guard de `string + minLength` não reconhecia `type` representado por array; `DIVERGE-03` demonstrou que `NaN` e `±Infinity` atravessavam limiares e pesos materiais. O resultado histórico permanece em `09_resultado_a1_reauditoria_6.md`.

O contraditório confirmou os três achados. A correção remove `Cf` e variation selectors antes da tokenização semântica, torna o guard sensível a arrays de tipos contendo `string`, registra `finite-number` no mesmo `FormatChecker` para limiares/pesos e recusa constantes JSON não finitas no loader. A suíte passa a **39 métodos**.""",
    "README seventh A1",
)
replace_once(
    mm01_readme,
    "A suíte MM01 possui **36 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da sexta A1 está verde no HEAD reconciliado, e os sete workflows permanentes foram executados com sucesso antes do congelamento para a sétima A1.",
    "A suíte MM01 possui **39 métodos automatizados**, além de mutações e subtests. O reteste das correções da sétima A1 ficou verde, e os sete workflows permanentes executaram com sucesso antes da sincronização documental para a oitava A1.",
    "README evidence",
)
replace_tail(
    mm01_readme,
    "## Gate de saída",
    """## Gate de saída

Como o contrato mudou materialmente depois da sétima A1, a MM01 só pode ser aceita após uma **oitava A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural, CLI e construir adversariais próprios sobre as três classes corrigidas.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma oitava A1 limpa e contraditório final.

**MM02 permanece bloqueada até oitava A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**""",
    "README gate",
)

replace_line_prefix(
    checkpoint,
    "Status:",
    "Status: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "checkpoint status",
)
replace_once(
    checkpoint,
    "suíte com **36 métodos de teste**;",
    "suíte com **39 métodos de teste**;",
    "checkpoint methods",
)
replace_once(
    checkpoint,
    "pacote neutro de auditoria com os resultados históricos das seis A1 preservados",
    "pacote neutro de auditoria com os resultados históricos das sete A1 preservados",
    "checkpoint audit count",
)
insert_before(
    checkpoint,
    "## Dívida documental antes do merge",
    """## Sétima auditoria A1

A sétima A1 independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: equivalência semântica burlável por Unicode default-ignorable, guard incompleto para `type` em array e números não finitos em limiares/pesos. O resultado foi preservado em `09_resultado_a1_reauditoria_6.md`.

## Correções da sétima A1

A normalização semântica remove `Cf` e variation selectors antes da tokenização; o guard de `string + minLength` reconhece tanto `type=\"string\"` quanto listas contendo `string`; e `finite-number` recusa NaN/±Infinity nos valores materiais, enquanto o loader JSON recusa constantes não padrão. A suíte passa a **39 métodos**.""",
    "checkpoint seventh A1",
)
replace_tail(
    checkpoint,
    "## Gate independente pendente",
    """## Gate independente pendente

Como a candidata mudou materialmente após a sétima A1, é obrigatória uma **oitava A1 independente** sobre o novo HEAD congelado.

## Gates restantes

1. executar oitava A1 em sessão independente;
2. confrontar qualquer novo achado com a árvore;
3. se a oitava A1 for limpa, executar contraditório final;
4. sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;
5. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;
6. obter aceite explícito;
7. só então integrar a PR #51.

Enquanto qualquer item estiver pendente, **MM02 permanece bloqueada**.""",
    "checkpoint gate",
)

replace_line_prefix(
    index,
    "> Estado:",
    "> Estado: **MM00 encerrada e integrada. MM01 passou por sete A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`); os três desvios bloqueantes da sétima A1 foram confirmados e corrigidos; reteste e sete workflows permanentes verdes; oitava A1 independente pendente. MM01 ainda não aceita nem integrada.**",
    "index status",
)
replace_once(index, "suíte com **36 métodos de teste**", "suíte com **39 métodos de teste**", "index methods")
replace_once(index, "### Quinta e sexta A1", "### Quinta, sexta e sétima A1", "index heading")
insert_before(
    index,
    "A skill roteável `hub-ml-micromodelos` continua reservada para MM04;",
    """A sétima A1, novamente `APTA_COM_CORRECOES`, encontrou três bloqueios: bypass de equivalência por Unicode default-ignorable, guard incompleto para arrays de tipos e aceitação de números não finitos. O sétimo relatório está preservado em `09_resultado_a1_reauditoria_6.md`.

A correção da sétima A1 remove default-ignorables antes da tokenização semântica, fecha o guard para listas contendo `string` e exige `finite-number` para limiar/peso, com JSON estrito contra `NaN/Infinity`. A suíte passa a 39 métodos.""",
    "index seventh A1",
)
replace_tail(
    index,
    "## Próximo gate",
    """## Próximo gate

1. executar uma **oitava A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;
2. confrontar qualquer novo achado e corrigir somente se procedente;
3. se a oitava A1 for limpa, executar contraditório final;
4. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
5. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;
6. integrar a PR #51 somente após o aceite.

**MM02 permanece bloqueada.**""",
    "index gate",
)

text = read(tests_doc)
lines = text.splitlines()
idx = [i for i, line in enumerate(lines) if line.startswith("| T51 |")]
if len(idx) != 1:
    raise SystemExit(f"TESTES T51: esperado 1, encontrado {len(idx)}")
extra = [
    "| T52 | default-ignorables dentro de palavra em semânticas equivalentes | `AMBIGUOUS_BINARY_SEMANTICS` |",
    "| T53 | `type=[string]` / `[string,null]` + `minLength`, inclusive aninhado | detectado pelo guard |",
    "| T54 | NaN/±Infinity em limiar/peso e constantes JSON não padrão | `SCHEMA` / carga fail-closed |",
]
lines[idx[0] + 1:idx[0] + 1] = extra
text = "\n".join(lines) + "\n"
if text.count("contém **36 métodos de teste**") != 1:
    raise SystemExit("TESTES method count não encontrado de forma única")
text = text.replace("contém **36 métodos de teste**", "contém **39 métodos de teste**", 1)
if "## Sétima A1 — `APTA_COM_CORRECOES`" in text:
    raise SystemExit("TESTES seventh A1 já existe")
text += """
## Sétima A1 — `APTA_COM_CORRECOES`

A sétima auditoria independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` encontrou três divergências bloqueantes: caracteres Unicode default-ignorable podiam mascarar equivalência `FALSE` × `INDETERMINADO`; o guard de `string + minLength` ignorava `type` em array; e NaN/±Infinity atravessavam limiares/pesos. O relatório histórico permanece em `09_resultado_a1_reauditoria_6.md`.

As regressões adicionadas após o contraditório cobrem os três vetores: default-ignorables em posição interna, arrays de tipos e branches aninhados, além de valores não finitos via objeto Python, YAML e constantes JSON permissivas.
"""
write(tests_doc, text)

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

replace_once(
    states_doc,
    "semântica `TRUE/FALSE/INDETERMINADO` deve estar aprovada e as três definições precisam permanecer distintas após normalização editorial básica;",
    "semântica `TRUE/FALSE/INDETERMINADO` deve estar aprovada e as três definições precisam permanecer distintas após normalização editorial que remove acentos, pontuação/espaçamento e caracteres Unicode default-ignorable antes da tokenização;",
    "states semantic normalization",
)
replace_once(
    states_doc,
    "limiares e pesos existentes precisam estar `APROVADO`; antes de `EM_VALIDACAO`, podem permanecer `PROPOSTO`.",
    "limiares e pesos existentes precisam estar `APROVADO` e seus valores numéricos precisam ser finitos; antes de `EM_VALIDACAO`, podem permanecer `PROPOSTO`.",
    "states finite numbers",
)

print("Documentação pós-sétima A1 sincronizada.")
