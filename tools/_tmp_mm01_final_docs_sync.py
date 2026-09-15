from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: esperado 1 match, encontrado {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before(path: Path, marker: str, block: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(marker) != 1:
        raise SystemExit(f"{label}: marker esperado uma vez, encontrado {text.count(marker)}")
    path.write_text(text.replace(marker, block + marker, 1), encoding="utf-8")


root_readme = ROOT / "README.md"
replace_once(
    root_readme,
    "repo (identidade)  : 1430 arquivos varridos no repositório editável/derivado",
    "repo (identidade)  : 1431 arquivos varridos no repositório editável/derivado",
    "root identity 1431",
)

mm01 = ROOT / "docs" / "sprints" / "micromodelos" / "MM01"
readme = mm01 / "README.md"
replace_once(
    readme,
    "Status da sprint: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status da sprint: **OITAVA A1 `NAO_APTA` PRESERVADA; CONTRADITÓRIO DE ESCOPO CONCLUÍDO; MATRIZ DE ACEITE FINAL CONGELADA; 47 TESTES DE CONSTRUÇÃO VERDES; AUDITORIA FINAL FECHADA PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "MM01 README status",
)
replace_once(readme, "suíte automatizada com **39 métodos**", "suíte automatizada com **47 métodos**", "MM01 README method count")
replace_once(
    readme,
    "pacote de auditoria A1 com contexto, prompt e sete resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);",
    "pacote de auditoria A1 com contexto, prompt e oito resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `NAO_APTA`), além da `MATRIZ_ACEITE_FINAL.md` congelada após o contraditório da oitava A1;",
    "MM01 README audit count",
)
replace_once(
    readme,
    "`fase_anterior` torna o par declarado localmente verificável, mas não é tratada como prova autorreferente de histórico. Quando um snapshot anterior confiável existe, a CLI aceita `--previous` e valida a transição contra a fase efetivamente observada nele. Uma versão já `PUBLICADO` não pode ser silenciosamente reescrita para fase anterior mantendo a mesma `micromodel_version`.",
    "`fase_anterior` torna o par declarado localmente verificável, mas não é tratada como prova autorreferente de histórico. Sem `--previous`, a CLI certifica apenas a consistência interna do snapshot e declara explicitamente `HISTORICO_NAO_CERTIFICADO`. Quando um snapshot anterior confiável é fornecido por `--previous`, a validação passa a certificar evolução histórica: confere identidade/versão, valida a transição observada e impede rewind de uma versão já `PUBLICADO`. Esse modo não descobre histórico por conta própria nem antecipa fingerprint/MM02.",
    "MM01 README snapshot evolution",
)
replace_once(
    readme,
    "O contrato exige três definições distintas: `quando_true`, `quando_false` e `quando_indeterminado`. A comparação normaliza diferenças editoriais simples; não é possível contornar o gate copiando a mesma definição com caixa, acento ou pontuação diferente.",
    "O contrato exige três definições distintas: `quando_true`, `quando_false` e `quando_indeterminado`. A comparação é deliberadamente **editorial, não semântica**: aplica NFKC/casefold, remove `Default_Ignorable_Code_Point`, normaliza whitespace e tolera apenas pontuação terminal editorial prevista. Diacríticos, operadores e pontuação interna potencialmente semânticos são preservados; a MM01 não tenta resolver equivalência geral de linguagem natural.",
    "MM01 README editorial equivalence",
)
replace_once(
    readme,
    "A regra atual é positiva e única: após NFKC, conteúdo material precisa conter ao menos uma letra ou número Unicode.",
    "A regra atual é positiva e única: após NFKC, caracteres com a propriedade Unicode `Default_Ignorable_Code_Point` são removidos e o conteúdo restante precisa conter ao menos uma letra ou número Unicode.",
    "MM01 README material authority",
)
insert_before(
    readme,
    "## Fronteiras preservadas\n",
    "### Oitava A1, contraditório e matriz final\n\nA oitava A1 independente sobre `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630` concluiu `NAO_APTA` e permanece historicamente preservada em `10_resultado_a1_reauditoria_7.md`. O relatório trouxe seis `QUEBRA`, dois `DIVERGE` bloqueantes e uma melhoria. O contraditório confirmou defeitos materiais, mas também demonstrou que a auditoria exploratória vinha ampliando o threat model a cada rodada.\n\nPara encerrar o ciclo de expansão aberta, `MATRIZ_ACEITE_FINAL.md` congela os requisitos R01–R08, as entradas suportadas, o perfil de autoria do schema e os não requisitos. A candidata foi corrigida contra essa matriz: materialidade passa a usar `Default_Ignorable_Code_Point`; a comparação passa a ser editorial conservadora; o domínio numérico canônico é determinístico; decisão humana e proveniência têm invariantes intrínsecos; resultado observado só existe após `EXECUTADO`; snapshot e evolução histórica têm níveis de garantia distintos; e o schema oficial permanece dentro do perfil de composição revisado. A suíte passa a **47 métodos**.\n\nA próxima auditoria é **final e fechada contra a matriz**. Um adversarial novo só pode bloquear se demonstrar violação de requisito já assumido na matriz ou ADR aceito; não pode criar novo requisito implicitamente.\n\n",
    "MM01 README final matrix section",
)
replace_once(
    readme,
    "A suíte MM01 possui **39 métodos automatizados**, além de mutações e subtests. O reteste das correções da sétima A1 ficou verde, e os sete workflows permanentes executaram com sucesso antes da sincronização documental para a oitava A1.",
    "A suíte MM01 possui **47 métodos automatizados**, além de mutações e subtests. O reteste de construção da matriz final ficou verde antes da sincronização documental; a certificação dos workflows permanentes será executada sobre o HEAD documental final antes da auditoria final fechada.",
    "MM01 README current evidence",
)
replace_once(
    readme,
    "Como o contrato mudou materialmente depois da sétima A1, a MM01 só pode ser aceita após uma **oitava A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural, CLI e construir adversariais próprios sobre as três classes corrigidas.\n\nO bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma oitava A1 limpa e contraditório final.\n\n**MM02 permanece bloqueada até oitava A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**",
    "A MM01 agora possui condição objetiva de término em `MATRIZ_ACEITE_FINAL.md`. O próximo gate é uma **auditoria final fechada** sobre o HEAD congelado: ela deve reproduzir instalação, 47 testes, CLI, gate estrutural e adversariais próprios, mas só pode classificar como bloqueante uma violação de requisito já assumido pela matriz ou ADR aceito.\n\nO bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após auditoria final limpa e contraditório final.\n\n**MM02 permanece bloqueada até auditoria final, contraditório final, fechamento do changelog, aceite explícito e integração da MM01.**",
    "MM01 README final gate",
)

checkpoint = mm01 / "CHECKPOINT.md"
replace_once(
    checkpoint,
    "Status: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "Status: **OITAVA A1 `NAO_APTA` PRESERVADA; CONTRADITÓRIO DE ESCOPO CONCLUÍDO; MATRIZ DE ACEITE FINAL CONGELADA; 47 TESTES DE CONSTRUÇÃO VERDES; AUDITORIA FINAL FECHADA PENDENTE; NÃO ACEITA; NÃO INTEGRADA**",
    "checkpoint status",
)
replace_once(checkpoint, "MM02: bloqueada até nova A1, aceite explícito e merge desta sprint.", "MM02: bloqueada até auditoria final fechada, contraditório final, aceite explícito e merge desta sprint.", "checkpoint MM02")
replace_once(
    checkpoint,
    "4. comparação opcional com especificação anterior confiável (`--previous`) para verificar transição real, impedir rewind pós-`PUBLICADO` na mesma versão e recusar regressão de versão, sem antecipar fingerprint/MM02;",
    "4. dois níveis explícitos de garantia: validação standalone certifica apenas o snapshot (`HISTORICO_NAO_CERTIFICADO`); `--previous` certifica evolução histórica, impede rewind pós-`PUBLICADO` na mesma versão e recusa regressão de versão, sem antecipar fingerprint/MM02;",
    "checkpoint previous",
)
replace_once(
    checkpoint,
    "7. regra positiva de materialidade textual: referências auditáveis precisam conter letra/número Unicode após NFKC; whitespace, controles, zero-width, variation selectors e marcas combinantes isoladas não contam;",
    "7. regra positiva de materialidade textual: após NFKC, `Default_Ignorable_Code_Point` é removido e referências auditáveis precisam conter letra/número Unicode restante; fillers invisíveis não contam;",
    "checkpoint materiality",
)
replace_once(
    checkpoint,
    "8. proteção explícita de `FALSE` versus `INDETERMINADO`, inclusive contra equivalência apenas cosmeticamente diferente;",
    "8. proteção explícita de `FALSE` versus `INDETERMINADO` por equivalência editorial conservadora, sem tentar inferir equivalência semântica de linguagem natural;",
    "checkpoint editorial",
)
replace_once(checkpoint, "suíte com **39 métodos de teste**", "suíte com **47 métodos de teste**", "checkpoint methods")
replace_once(
    checkpoint,
    "23. pacote neutro de auditoria com os resultados históricos das sete A1 preservados, sem reclassificação retroativa.",
    "23. pacote neutro de auditoria com os resultados históricos das oito A1 preservados, sem reclassificação retroativa, e `MATRIZ_ACEITE_FINAL.md` congelando o threat model e a condição de término.",
    "checkpoint audit package",
)
insert_before(
    checkpoint,
    "## Dívida documental antes do merge\n",
    "## Oitava auditoria A1 e mudança de governança\n\nA oitava A1 independente sobre `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630` concluiu `NAO_APTA`. O resultado permanece em `10_resultado_a1_reauditoria_7.md`. O contraditório separou violações reais do contrato, decisões arquiteturais e hardening fora do threat model.\n\n`MATRIZ_ACEITE_FINAL.md` foi então congelada. Ela define R01–R08, entradas suportadas, não requisitos e a regra de que a auditoria final pode criar adversariais, mas não criar requisitos novos implicitamente. As correções permanentes associadas elevaram a suíte a **47 métodos** e cobrem materialidade por propriedade Unicode, equivalência editorial conservadora, domínio numérico canônico, decisão humana/proveniência intrínsecas, resultado somente após execução, distinção snapshot × evolução e perfil de autoria do schema.\n\n",
    "checkpoint eighth matrix",
)
replace_once(
    checkpoint,
    "## Gate independente pendente\n\nComo a candidata mudou materialmente após a sétima A1, é obrigatória uma **oitava A1 independente** sobre o novo HEAD congelado.\n\n## Gates restantes\n\n1. executar oitava A1 em sessão independente;\n2. confrontar qualquer novo achado com a árvore;\n3. se a oitava A1 for limpa, executar contraditório final;\n4. sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;\n5. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;\n6. obter aceite explícito;\n7. só então integrar a PR #51.",
    "## Auditoria final fechada pendente\n\nA candidata deve passar por **uma única auditoria final contra `MATRIZ_ACEITE_FINAL.md`**. Achado novo só é bloqueante se demonstrar violação de requisito da matriz ou ADR aceito. Ampliação de threat model exige decisão explícita do usuário e não pode nascer implicitamente da auditoria.\n\n## Gates restantes\n\n1. certificar os workflows permanentes no HEAD documental final;\n2. executar a auditoria final fechada em sessão independente;\n3. executar contraditório final sobre qualquer achado dentro da matriz;\n4. se limpa, sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;\n5. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;\n6. obter aceite explícito;\n7. só então integrar a PR #51.",
    "checkpoint final gates",
)

contract_doc = mm01 / "CONTRATO_MICROMODELO.md"
replace_once(
    contract_doc,
    "`micromodelo.yaml` é a especificação estruturada canônica do micromodelo. Ele registra **o que o micromodelo significa e como deve ser avaliado**, não o histórico crescente das execuções. README, notebook, catálogo e handoffs futuros devem ser derivados ou confrontados com esse contrato.",
    "`micromodelo.yaml` é a especificação estruturada canônica do micromodelo. Ele registra **o que o micromodelo significa e como deve ser avaliado**, não o histórico crescente das execuções. README, notebook, catálogo e handoffs futuros devem ser derivados ou confrontados com esse contrato. Para a finalização da sprint, `MATRIZ_ACEITE_FINAL.md` congela o threat model, as entradas suportadas e a condição objetiva de aceite.",
    "contract matrix authority",
)
replace_once(
    contract_doc,
    "`fase_anterior` e `fase_atual` tornam o par declarado localmente verificável, mas o documento corrente não é prova suficiente do próprio histórico. Quando existe uma especificação anterior confiável, o validador pode recebê-la por `--previous`: nesse modo ele confere identidade, versão e transição real entre snapshots, impede regressão de versão e recusa rewind de uma versão já `PUBLICADO`. Isso resolve a auditabilidade da MM01 sem introduzir fingerprint antecipadamente.",
    "`fase_anterior` e `fase_atual` tornam o par declarado localmente verificável, mas o documento corrente não é prova suficiente do próprio histórico. A CLI standalone certifica somente o snapshot e declara `HISTORICO_NAO_CERTIFICADO`. Quando existe uma especificação anterior confiável, `--previous` ativa a certificação de evolução: identidade, versão e transição real entre snapshots são comparadas, regressão de versão e rewind pós-`PUBLICADO` são recusados. A MM01 não descobre histórico automaticamente nem introduz fingerprint antecipadamente.",
    "contract snapshot evolution",
)
replace_once(
    contract_doc,
    "A distinção é verificada após normalização editorial de caixa, acentuação, pontuação e espaços. Caracteres Unicode default-ignorable (`Cf`) e variation selectors são removidos antes da tokenização, para que inserções invisíveis dentro de palavras não fabriquem uma diferença semântica artificial; não basta copiar a mesma definição mudando apenas forma textual.",
    "A distinção é verificada por **equivalência editorial conservadora**, não por inferência semântica: NFKC, `casefold`, remoção de `Default_Ignorable_Code_Point`, normalização de whitespace e tolerância somente a pontuação terminal editorial prevista. Diacríticos, operadores (`<`, `>`, `≤`, `≥`, `+`, `-`) e pontuação interna potencialmente semânticos são preservados. A MM01 não tenta decidir se duas frases diferentes têm o mesmo significado.",
    "contract editorial",
)
replace_once(
    contract_doc,
    "Limiar material pode ser registrado como `PROPOSTO` enquanto o micromodelo ainda está em descoberta/estudo. A partir de `EM_VALIDACAO`, todo limiar existente precisa carregar proveniência `APROVADO`. `classificacao.limiares[].valor` precisa ser um número finito: NaN e ±Infinity são recusados. Dessa forma, a fonte canônica preserva propostas sem permitir que elas atravessem o gate formal como decisões inválidas.",
    "Limiar material pode ser registrado como `PROPOSTO` enquanto o micromodelo ainda está em descoberta/estudo. A partir de `EM_VALIDACAO`, todo limiar existente precisa carregar proveniência `APROVADO`. `classificacao.limiares[].valor` pertence ao domínio numérico canônico JSON/YAML: inteiros Python, inclusive arbitrariamente grandes, são finitos; floats precisam ser finitos; NaN/±Infinity e tipos numéricos externos ao domínio canônico são recusados deterministicamente. Dessa forma, a fonte canônica preserva propostas sem permitir que elas atravessem o gate formal como decisões inválidas.",
    "contract threshold numeric",
)
replace_once(
    contract_doc,
    "Assim como limiares, pesos podem permanecer `PROPOSTO` nas fases pré-gate, mas todo peso existente precisa estar `APROVADO` ao entrar em `EM_VALIDACAO` ou fase posterior. `score.componentes[].peso` também precisa ser finito; NaN e ±Infinity não são valores materiais válidos.",
    "Assim como limiares, pesos podem permanecer `PROPOSTO` nas fases pré-gate, mas todo peso existente precisa estar `APROVADO` ao entrar em `EM_VALIDACAO` ou fase posterior. `score.componentes[].peso` segue o mesmo domínio numérico canônico: inteiros são finitos sem conversão para float, floats precisam ser finitos e tipos numéricos externos são recusados em vez de interpretados implicitamente.",
    "contract weight numeric",
)
replace_once(
    contract_doc,
    "Registra hipóteses relevantes da especificação. Um experimento `EXECUTADO` exige resultado e proveniência `MEDIDO`. O identificador da execução é referência externa; o YAML não incorpora o histórico das runs.",
    "Registra hipóteses relevantes da especificação. Um experimento `EXECUTADO` exige resultado observado material e proveniência `MEDIDO`. Enquanto estiver `PROPOSTO`, `EM_EXECUCAO` ou `DESCARTADO`, `resultado` deve permanecer `null`; resultado esperado pertence à hipótese, não ao campo de resultado observado. O identificador da execução é referência externa; o YAML não incorpora o histórico das runs.",
    "contract experiment result",
)
replace_once(
    contract_doc,
    "Fase `VALIDADO` ou posterior não é aceita se esse gate não estiver satisfeito.",
    "Fase `VALIDADO` ou posterior não é aceita se esse gate não estiver satisfeito. Além disso, a decisão humana é intrinsecamente coerente em qualquer fase: `APROVADO`/`REPROVADO` exigem `por`, `em_utc` e `referencia`, precisam coincidir com `validacao.status`, e `PENDENTE` não pode carregar metadados de decisão final.",
    "contract human approval",
)
replace_once(
    contract_doc,
    "A definição de “texto material” é positiva: após normalização NFKC, o validador exige ao menos uma letra ou número Unicode. Espaços, controles, caracteres de formatação, variation selectors e marcas combinantes isoladas não satisfazem uma prova auditável. Isso se aplica a aprovação, medição e referências externas de publicação.",
    "A definição de “texto material” é positiva: após NFKC, o validador remove caracteres com a propriedade Unicode `Default_Ignorable_Code_Point` e exige ao menos uma letra ou número Unicode restante. Assim, fillers invisíveis também não satisfazem uma prova auditável. Isso se aplica a aprovação, medição e referências externas de publicação sem depender de blacklist manual de code points.",
    "contract material text",
)
replace_once(
    contract_doc,
    "`APROVADO` exige bloco de aprovação com conteúdo auditável; `MEDIDO` exige medição com referência de execução material. Presença sintática de caracteres invisíveis não satisfaz esses estados.",
    "`APROVADO` exige bloco de aprovação com conteúdo auditável; `MEDIDO` exige medição com referência de execução material. Esses invariantes são verificados sempre que um bloco de proveniência existe, independentemente da fase; a fase apenas define quando determinado status se torna obrigatório. Presença sintática de caracteres invisíveis/default-ignorable não satisfaz esses estados.",
    "contract provenance intrinsic",
)
replace_once(
    contract_doc,
    "A regra normaliza por NFKC e exige ao menos um caractere cuja categoria Unicode comece por `L` ou `N`.",
    "A regra normaliza por NFKC, remove `Default_Ignorable_Code_Point` usando propriedade Unicode padronizada e exige ao menos um caractere restante cuja categoria Unicode comece por `L` ou `N`.",
    "contract authority section",
)

states = mm01 / "ESTADOS_E_PROVENIENCIA.md"
replace_once(
    states,
    "A validação isolada do documento corrente consegue conferir somente o par declarado `fase_anterior → fase_atual`. Para provar continuidade histórica entre snapshots, a MM01 aceita uma especificação anterior confiável por `--previous`. Nesse modo, o validador confere identidade e versão, usa a fase efetivamente observada no snapshot anterior como origem da transição e recusa rewind de `PUBLICADO` na mesma versão. Esse mecanismo não calcula nem substitui o `spec_fingerprint` da MM02.",
    "A validação isolada do documento corrente consegue conferir somente o par declarado `fase_anterior → fase_atual` e, por isso, a CLI a classifica como `SNAPSHOT_VALIDO` com `HISTORICO_NAO_CERTIFICADO`. Para provar continuidade histórica, uma especificação anterior confiável deve ser fornecida por `--previous`; nesse modo, o validador certifica evolução, confere identidade/versão, usa a fase observada no snapshot anterior como origem e recusa rewind de `PUBLICADO` na mesma versão. Esse mecanismo não descobre histórico nem substitui o `spec_fingerprint` da MM02.",
    "states snapshot evolution",
)
replace_once(
    states,
    "`APROVADO` sem bloco de aprovação é inválido. `MEDIDO` sem execução referenciável é inválido. Inversamente, blocos de aprovação/medição não podem ser pendurados em outro status apenas para guardar contexto.",
    "`APROVADO` sem bloco de aprovação é inválido. `MEDIDO` sem execução referenciável é inválido. Inversamente, blocos de aprovação/medição não podem ser pendurados em outro status apenas para guardar contexto. Essas invariantes são locais ao bloco e são validadas sempre que a proveniência existe; a fase apenas determina quando um status específico se torna obrigatório.",
    "states intrinsic provenance",
)
replace_once(
    states,
    "Os campos que funcionam como prova auditável usam uma regra positiva, não uma blacklist incompleta de whitespace/invisíveis. Depois de normalização NFKC, precisa existir ao menos um caractere Unicode de categoria letra (`L*`) ou número (`N*`). Portanto strings compostas apenas por espaços, controles, zero-width, variation selectors ou marcas combinantes (`M*`) não são referência material.",
    "Os campos que funcionam como prova auditável usam uma regra positiva, não uma blacklist incompleta. Depois de NFKC, caracteres com a propriedade Unicode `Default_Ignorable_Code_Point` são removidos; precisa restar ao menos uma letra (`L*`) ou número (`N*`). Portanto espaços, controles, zero-width, variation selectors, fillers default-ignorable ou marcas combinantes isoladas não são referência material.",
    "states materiality",
)
replace_once(
    states,
    "- semântica `TRUE/FALSE/INDETERMINADO` deve estar aprovada e as três definições precisam permanecer distintas após normalização editorial que remove acentos, pontuação/espaçamento e caracteres Unicode default-ignorable antes da tokenização;",
    "- semântica `TRUE/FALSE/INDETERMINADO` deve estar aprovada e as três definições precisam permanecer distintas após equivalência editorial conservadora (NFKC/casefold, remoção de `Default_Ignorable_Code_Point`, whitespace normalizado e somente pontuação terminal editorial tolerada), preservando diacríticos, operadores e pontuação interna potencialmente semânticos;",
    "states editorial",
)
replace_once(
    states,
    "- limiares e pesos existentes precisam estar `APROVADO` e seus valores numéricos precisam ser finitos; antes de `EM_VALIDACAO`, podem permanecer `PROPOSTO`.",
    "- limiares e pesos existentes precisam estar `APROVADO` e seus valores precisam pertencer ao domínio numérico canônico finito; inteiros arbitrariamente grandes não são convertidos para float e tipos numéricos externos são recusados; antes de `EM_VALIDACAO`, podem permanecer `PROPOSTO`.",
    "states numbers",
)
replace_once(
    states,
    "`saida.publicacao.politica_indeterminado` também não aceita prosa normativa. `indeterminado_vira_false` é constante `false`. O tratamento é fechado e, se for `OUTRA_APROVADA`, precisa de `regra_ref` auditável.",
    "`saida.publicacao.politica_indeterminado` também não aceita prosa normativa. `indeterminado_vira_false` é constante `false`. O tratamento é fechado e, se for `OUTRA_APROVADA`, precisa de `regra_ref` auditável. Se a política for preenchida antecipadamente, sua proveniência já precisa ser intrinsecamente válida; chegar a `CANDIDATO_PRODUTO` apenas passa a exigir que ela esteja efetivamente `APROVADO`.",
    "states publication provenance",
)
replace_once(
    states,
    "A política é positiva: após NFKC, deve existir pelo menos uma letra ou número Unicode. Marcas combinantes isoladas, zero-width, formatos invisíveis, whitespace, pontuação ou símbolos sem letra/número não constituem prova.",
    "A política é positiva: após NFKC e remoção de `Default_Ignorable_Code_Point`, deve existir pelo menos uma letra ou número Unicode. Marcas combinantes isoladas, zero-width, fillers invisíveis, whitespace, pontuação ou símbolos sem letra/número não constituem prova.",
    "states bottom materiality",
)

# TESTES.md
tests_doc = mm01 / "TESTES.md"
replace_once(
    tests_doc,
    "| T54 | NaN/±Infinity em limiar/peso e constantes JSON não padrão | `SCHEMA` / carga fail-closed |",
    "| T54 | NaN/±Infinity em limiar/peso e constantes JSON não padrão | `SCHEMA` / carga fail-closed |\n| T55 | fillers/default-ignorables Unicode (`U+115F/U+1160/U+3164/U+FFA0`) como texto material | `SCHEMA` / `_has_material_text=False` |\n| T56 | equivalência editorial com invisíveis em múltiplas posições + pares distintos por operador/diacrítico | invisíveis equivalentes; diferenças semânticas preservadas |\n| T57 | inteiro finito acima do intervalo de float + tipos numéricos externos | inteiro aceito; tipos externos rejeitados deterministicamente |\n| T58 | aprovação humana final durante validação pendente ou sem metadados | `VALIDATION_HUMAN_GATE` |\n| T59 | política de publicação antecipada com proveniência intrinsecamente inválida | `PROV_APPROVAL_REQUIRED` |\n| T60 | experimento não `EXECUTADO` com resultado observado material | `EXPERIMENT_RESULT` |\n| T61 | CLI sem/com `--previous` | `SNAPSHOT_VALIDO/HISTORICO_NAO_CERTIFICADO` vs `APROVADO_EVOLUCAO` |\n| T62 | perfil canônico de autoria do schema | recusa `allOf`/`oneOf`, `anyOf` fora da allowlist e constraints irmãs de `$ref` |",
    "tests matrix T55-T62",
)
replace_once(tests_doc, "contém **39 métodos de teste**", "contém **47 métodos de teste**", "tests method count")
replace_once(
    tests_doc,
    "A segunda A1 demonstrou que excluir apenas categorias `Z*`/`C*` deixava passar marcas Unicode `M*`. A suíte agora testa U+034F, U+FE0F e U+0301 nos campos auditáveis relevantes. A regra semântica positiva exige, após NFKC, pelo menos uma letra ou número Unicode; marcas combinantes/variation selectors isolados não satisfazem aprovação, medição ou confirmação externa.",
    "As auditorias exploratórias demonstraram que categorias Unicode e listas manuais de code points não bastam para materialidade. A suíte cobre marcas, variation selectors e fillers como U+115F/U+1160/U+3164/U+FFA0. A autoridade agora usa a propriedade Unicode `Default_Ignorable_Code_Point`: após NFKC e remoção desses caracteres, precisa restar letra ou número Unicode. Os positivos multilíngues continuam protegidos.",
    "tests Unicode regressions",
)
insert_before(
    tests_doc,
    "## Fixtures\n",
    "## Matriz de aceite final e condição de término\n\nA oitava A1 (`NAO_APTA`) foi preservada em `10_resultado_a1_reauditoria_7.md`. O contraditório posterior congelou `MATRIZ_ACEITE_FINAL.md` para separar requisitos materiais de hardening e adversariais fora do threat model. As regressões T55–T62 exercitam diretamente R01–R08.\n\nA próxima auditoria é final e fechada contra essa matriz. Ela pode construir novos adversariais, mas um caso só é bloqueante quando demonstra violação de requisito já assumido pela matriz ou ADR aceito. `Decimal`/NumPy como suporte positivo, resolução universal de composição JSON Schema e coerções históricas YAML 1.1 não são gates de aceite da MM01.\n\n",
    "tests final matrix section",
)
insert_before(
    tests_doc,
    "## Sétima A1 — `APTA_COM_CORRECOES`\n",
    "",
    "noop before seventh",
) if False else None
# Acrescenta após a seção da sétima A1, que fecha o arquivo atualmente.
text = tests_doc.read_text(encoding="utf-8")
ending = "As regressões adicionadas após o contraditório cobrem os três vetores: default-ignorables em posição interna, arrays de tipos e branches aninhados, além de valores não finitos via objeto Python, YAML e constantes JSON permissivas."
if text.count(ending) != 1:
    raise SystemExit("tests ending anchor inválido")
text = text.replace(
    ending,
    ending + "\n\n## Oitava A1 — `NAO_APTA` e contraditório de escopo\n\nA oitava auditoria independente sobre `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630` encontrou seis `QUEBRA`, dois `DIVERGE` bloqueantes e uma melhoria; o resultado histórico permanece em `10_resultado_a1_reauditoria_7.md`. O contraditório confirmou defeitos materiais, mas classificou suporte positivo a tipos numéricos externos, resolução universal de JSON Schema e coerções YAML 1.1 como fora do gate final.\n\nA matriz final congelada levou a suíte de 39 para **47 métodos**. O run de construção correspondente deve permanecer como evidência técnica da correção, enquanto a certificação final depende dos workflows permanentes no HEAD documental congelado.",
    1,
)
tests_doc.write_text(text, encoding="utf-8")

index = ROOT / "docs" / "sprints" / "micromodelos" / "README.md"
replace_once(
    index,
    "> Estado: **MM00 encerrada e integrada. MM01 passou por sete A1 (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`); os três desvios bloqueantes da sétima A1 foram confirmados e corrigidos; reteste e sete workflows permanentes verdes; oitava A1 independente pendente. MM01 ainda não aceita nem integrada.**",
    "> Estado: **MM00 encerrada e integrada. MM01 possui oito A1 históricas (`NAO_APTA`, `NAO_APTA`, cinco `APTA_COM_CORRECOES`, `NAO_APTA`); após o contraditório da oitava A1, a `MATRIZ_ACEITE_FINAL.md` congelou o threat model e a condição de término. As correções da matriz têm 47 testes de construção verdes; auditoria final fechada ainda pendente. MM01 não aceita nem integrada.**",
    "index status",
)
replace_once(index, "suíte com **39 métodos de teste**", "suíte com **47 métodos de teste**", "index methods")
insert_before(
    index,
    "A skill roteável `hub-ml-micromodelos` continua reservada para MM04;",
    "### Oitava A1 e matriz de aceite final\n\nA oitava A1 concluiu `NAO_APTA` e está preservada em `10_resultado_a1_reauditoria_7.md`. O contraditório posterior encerrou as auditorias exploratórias abertas: requisitos reais foram separados de hardening e de adversariais fora do threat model, e `MATRIZ_ACEITE_FINAL.md` foi congelada. A candidata agora usa materialidade baseada em `Default_Ignorable_Code_Point`, equivalência editorial conservadora, domínio numérico canônico, invariantes intrínsecos de aprovação/proveniência, resultado observado apenas após execução, níveis distintos de garantia para snapshot/evolução e perfil canônico de autoria do schema. A suíte passa a 47 métodos.\n\n",
    "index eighth matrix",
)
replace_once(
    index,
    "## Próximo gate\n\n1. executar uma **oitava A1 independente** sobre esse HEAD, sem usar relatórios anteriores, narrativa do autor, changelog ou mensagens de commit como prova;\n2. confrontar qualquer novo achado e corrigir somente se procedente;\n3. se a oitava A1 for limpa, executar contraditório final;\n4. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;\n5. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;\n6. integrar a PR #51 somente após o aceite.",
    "## Próximo gate\n\n1. certificar os sete workflows permanentes sobre o HEAD documental final;\n2. executar **uma auditoria final fechada contra `MATRIZ_ACEITE_FINAL.md`**, sem permitir expansão implícita de requisitos;\n3. executar contraditório final sobre achados que efetivamente violem a matriz/ADRs;\n4. se limpa, sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;\n5. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;\n6. integrar a PR #51 somente após o aceite.",
    "index final gate",
)

print("Documentação pós-matriz final sincronizada.")
