# MM01 — Estados e proveniência

## 1. Máquina de fases

A fase representa o progresso analítico/institucional do micromodelo. A especificação guarda `fase_anterior` e `fase_atual` para tornar a transição corrente verificável sem carregar um log infinito no YAML.

Transições permitidas em `schema_version=1.0.0`:

| De | Para | Interpretação |
|---|---|---|
| `null` | `IDEIA` | criação da especificação |
| `IDEIA` | `EM_DESCOBERTA` | início da descoberta de fontes/evidências |
| `EM_DESCOBERTA` | `EM_ESTUDO` | fontes suficientes para iniciar estudo |
| `EM_ESTUDO` | `EM_VALIDACAO` | candidata pronta para validação formal |
| `EM_VALIDACAO` | `VALIDADO` | evidência técnica + decisão humana aprovadas |
| `EM_VALIDACAO` | `EM_ESTUDO` | retorno explícito para reformulação |
| `VALIDADO` | `CANDIDATO_PRODUTO` | contrato de saída preparado para publicação |
| `VALIDADO` | `EM_ESTUDO` | mudança material exige novo estudo/revalidação |
| `CANDIDATO_PRODUTO` | `EM_VALIDACAO_GOVERNANCA` | handoff submetido à autoridade externa |
| `CANDIDATO_PRODUTO` | `VALIDADO` | retorno após ajuste pré-submissão |
| `EM_VALIDACAO_GOVERNANCA` | `PUBLICADO` | publicação externa confirmada |
| `EM_VALIDACAO_GOVERNANCA` | `CANDIDATO_PRODUTO` | retorno da governança para ajuste |

`PUBLICADO` é terminal para a versão corrente. Mudança material posterior deve gerar nova versão do micromodelo; o contrato não “rebobina” silenciosamente uma versão já publicada.

A validação isolada do documento corrente consegue conferir somente o par declarado `fase_anterior → fase_atual`. Para provar a continuidade histórica entre snapshots, a MM01 aceita uma especificação anterior confiável por `--previous`. Nesse modo, o validador confere identidade e versão, usa a fase efetivamente observada no snapshot anterior como origem da transição e recusa rewind de `PUBLICADO` na mesma versão. Esse mecanismo é histórico/comparativo e não é o `spec_fingerprint` da MM02.

## 2. Condição operacional

A condição é ortogonal à fase:

- `ATIVO`: fluxo normal;
- `BLOQUEADO`: impedimento que deve ser resolvido antes de avançar;
- `SUSPENSO`: trabalho/uso pausado conscientemente;
- `DEPRECATED`: versão/artefato não deve receber evolução normal.

Toda condição diferente de `ATIVO` exige `motivo_condicao`. `PUBLICADO` não usa `BLOQUEADO`; para um publicado indisponível use `SUSPENSO` ou `DEPRECATED` conforme o caso.

Separar fase e condição resolve uma ambiguidade importante: não é necessário permitir “BLOQUEADO → qualquer fase” para retomar o trabalho, porque a fase continua registrada enquanto a condição muda.

## 3. Proveniência controlada

Estados aceitos:

| Status | Significado | Evidência mínima |
|---|---|---|
| `DESCOBERTO` | informação observada em metadata/fonte | origem e, quando disponível, referência/timestamp |
| `INFERIDO` | conclusão derivada pelo agente/analista, ainda não aprovada | origem e referência quando houver |
| `PROPOSTO` | sugestão explícita aguardando decisão | origem |
| `APROVADO` | decisão humana material aceita | bloco `aprovacao` com responsável, timestamp e referência material |
| `MEDIDO` | resultado observado por execução | bloco `medicao` com `referencia_execucao` material e timestamp |

`APROVADO` sem bloco de aprovação é inválido. `MEDIDO` sem execução referenciável é inválido. Inversamente, blocos de aprovação/medição não podem ser pendurados em outro status apenas para “guardar contexto”.

Referência “presente” apenas sintaticamente não é suficiente: strings compostas só por whitespace ou caracteres invisíveis são tratadas como ausência de conteúdo material pelos guardrails semânticos. O schema também rejeita os casos triviais de whitespace nos campos materiais que consegue expressar formalmente.

`PROPOSTO` é deliberadamente representável no YAML. O estado serve para preservar propostas antes da decisão humana; ele só se torna insuficiente quando o micromodelo atravessa um gate de fase que exige aprovação.

## 4. Gates por fase

Ao entrar em `EM_VALIDACAO` ou fase posterior:

- `fontes`, `evidencias`, `contra_evidencias` e `validacao.criterios` devem estar não vazios;
- semântica `TRUE/FALSE/INDETERMINADO` deve estar aprovada e as três definições precisam permanecer distintas mesmo após normalização editorial básica;
- política de ausência de evidência deve estar aprovada;
- score habilitado precisa ter semântica aprovada;
- regras de evidência e contra-evidência precisam estar aprovadas;
- limiares e pesos existentes precisam estar `APROVADO`; antes de `EM_VALIDACAO`, podem permanecer `PROPOSTO`;
- linguagem probabilística em score não calibrado é recusada, ainda que o enum tenha sido deixado como `FORCA_EVIDENCIA` ou `OUTRA_APROVADA`.

Ao chegar em `VALIDADO` ou posterior, o resultado de validação precisa ser medido e a decisão humana precisa estar aprovada.

Ao chegar em `CANDIDATO_PRODUTO` ou posterior, o contrato de saída de publicação precisa estar definido, inclusive tratamento de `INDETERMINADO`. O campo estruturado `indeterminado_vira_false` permanece `false`, e descrição contraditória que tente mandar converter `INDETERMINADO` em `FALSE` é recusada.

A interface de publicação acompanha a fase:

- antes de `CANDIDATO_PRODUTO`: `publicacao.status=NAO_INICIADA`;
- em `CANDIDATO_PRODUTO`: `CANDIDATA` ou `REJEITADA`;
- em `EM_VALIDACAO_GOVERNANCA`: `EM_VALIDACAO_EXTERNA` e `handoff_ref` material obrigatório;
- em `PUBLICADO`: `PUBLICADA` e `produto_dados_ref` material obrigatório.

Esses gates têm caminhos positivos cobertos pela suíte. A intenção não é tornar fases posteriores inalcançáveis, mas impedir que o rótulo de fase avance sem o contrato correspondente.

## 5. Escopo de fontes

Na MM01, `catalogo_ref` aceita exclusivamente o placeholder `CATALOGO_PRODUTO`. A ferramenta de validação não possui flag de linha de comando para ampliar esse conjunto. Fonte fora do catálogo padrão continua sendo decisão humana/arquitetural e não override local de validação.

## 6. Integridade sintática e referencial

- YAML e JSON com chaves duplicadas são rejeitados no carregamento; não se aceita “last key wins”.
- Referências `fontes_ref` precisam apontar para fontes existentes.
- IDs duplicados são rejeitados nas coleções controladas: fontes, evidências, contra-evidências, limiares, componentes do score e experimentos.
- `score.calibracao.evidencia_ref` pertence ao namespace de `experimentos[].id` e precisa apontar para experimento `EXECUTADO` com proveniência `MEDIDO`.
- quando uma especificação anterior é fornecida, nome e versão precisam ser coerentes e a transição entre snapshots é validada contra a fase realmente observada no documento anterior.

## 7. Não equivalências que o contrato protege

```text
sem evidência ≠ FALSE
PROPOSTO ≠ APROVADO
INFERIDO ≠ MEDIDO
string visualmente vazia ≠ referência auditável
score 80 ≠ 80% de probabilidade
linguagem de probabilidade ≠ probabilidade calibrada
evidencia_ref textual ≠ evidência de calibração resolvida
notebook executado ≠ publicação autorizada
VALIDADO ≠ PUBLICADO
fase declarada ≠ histórico de fase provado
fase declarada ≠ gate da fase satisfeito
```

Essas diferenças são semânticas do domínio, não detalhes editoriais.
