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

`PUBLICADO` é terminal para a versão corrente. Mudança material posterior deve gerar nova versão do micromodelo; o contrato não rebobina silenciosamente uma versão já publicada.

A validação isolada do documento corrente consegue conferir somente o par declarado `fase_anterior → fase_atual`. Para provar continuidade histórica entre snapshots, a MM01 aceita uma especificação anterior confiável por `--previous`. Nesse modo, o validador confere identidade e versão, usa a fase efetivamente observada no snapshot anterior como origem da transição e recusa rewind de `PUBLICADO` na mesma versão. Esse mecanismo não calcula nem substitui o `spec_fingerprint` da MM02.

## 2. Condição operacional

A condição é ortogonal à fase:

- `ATIVO`: fluxo normal;
- `BLOQUEADO`: impedimento que deve ser resolvido antes de avançar;
- `SUSPENSO`: trabalho/uso pausado conscientemente;
- `DEPRECATED`: versão/artefato não deve receber evolução normal.

Toda condição diferente de `ATIVO` exige `motivo_condicao`. `PUBLICADO` não usa `BLOQUEADO`; para um publicado indisponível use `SUSPENSO` ou `DEPRECATED` conforme o caso.

## 3. Proveniência controlada

Estados aceitos:

| Status | Significado | Evidência mínima |
|---|---|---|
| `DESCOBERTO` | informação observada em metadata/fonte | origem e, quando disponível, referência/timestamp |
| `INFERIDO` | conclusão derivada pelo agente/analista, ainda não aprovada | origem e referência quando houver |
| `PROPOSTO` | sugestão explícita aguardando decisão | origem |
| `APROVADO` | decisão humana material aceita | bloco `aprovacao` com responsável, timestamp e referência material |
| `MEDIDO` | resultado observado por execução | bloco `medicao` com `referencia_execucao` material e timestamp |

`APROVADO` sem bloco de aprovação é inválido. `MEDIDO` sem execução referenciável é inválido. Inversamente, blocos de aprovação/medição não podem ser pendurados em outro status apenas para guardar contexto.

### Materialidade textual

Os campos que funcionam como prova auditável usam uma regra positiva, não uma blacklist incompleta de whitespace/invisíveis. Depois de normalização NFKC, precisa existir ao menos um caractere Unicode de categoria letra (`L*`) ou número (`N*`). Portanto strings compostas apenas por espaços, controles, zero-width, variation selectors ou marcas combinantes (`M*`) não são referência material.

A regra se aplica, entre outros, a:

- responsável/referência de decisão humana;
- `referencia_execucao` de medição;
- referências de regra estruturada;
- `handoff_ref`;
- `produto_dados_ref`.

`PROPOSTO` continua deliberadamente representável no YAML. O estado serve para preservar propostas antes da decisão humana; ele só se torna insuficiente quando o micromodelo atravessa um gate de fase que exige aprovação.

## 4. Gates por fase

Ao entrar em `EM_VALIDACAO` ou fase posterior:

- `fontes`, `evidencias`, `contra_evidencias` e `validacao.criterios` devem estar não vazios;
- semântica `TRUE/FALSE/INDETERMINADO` deve estar aprovada e as três definições precisam permanecer distintas após normalização editorial básica;
- política de ausência de evidência precisa estar estruturalmente consistente e aprovada quando usar regra explícita;
- score habilitado precisa ter `tipo_semantica` e `semantica_ref` materiais, além de normalização estruturada/aprovada;
- regras de evidência e contra-evidência precisam estar aprovadas;
- limiares e pesos existentes precisam estar `APROVADO`; antes de `EM_VALIDACAO`, podem permanecer `PROPOSTO`.

Ao chegar em `VALIDADO` ou posterior, o resultado de validação precisa ser medido e a decisão humana precisa estar aprovada.

Ao chegar em `CANDIDATO_PRODUTO` ou posterior, o contrato de saída de publicação precisa estar definido, inclusive tratamento estruturado de `INDETERMINADO`.

A interface de publicação acompanha a fase:

- antes de `CANDIDATO_PRODUTO`: `publicacao.status=NAO_INICIADA`;
- em `CANDIDATO_PRODUTO`: `CANDIDATA` ou `REJEITADA`;
- em `EM_VALIDACAO_GOVERNANCA`: `EM_VALIDACAO_EXTERNA` e `handoff_ref` material obrigatório;
- em `PUBLICADO`: `PUBLICADA` e `produto_dados_ref` material obrigatório.

## 5. Semântica estruturada: ausência, indeterminado e score

### Ausência de evidência

`classificacao.ausencia_evidencia` não possui descrição normativa livre. O comportamento é determinado por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência.

- `INDETERMINADO` exige resultado `INDETERMINADO` e nenhuma `regra_ref`;
- `REGRA_EXPLICITA_APROVADA` exige proveniência `APROVADO` e `regra_ref` material.

Uma propriedade livre que tente mandar “classificar como FALSE” não é interpretada: o schema fechado a rejeita.

### Publicação de `INDETERMINADO`

`saida.publicacao.politica_indeterminado` também não aceita prosa normativa. `indeterminado_vira_false` é constante `false`. O tratamento é fechado e, se for `OUTRA_APROVADA`, precisa de `regra_ref` auditável.

### Score probabilístico

`score.tipo_semantica` é a única autoridade executável sobre a natureza do score. `semantica_ref` registra uma referência auditável, mas não pode sobrescrever o enum. Não existe campo livre `score.semantica` cujo vocabulário seja analisado por regex.

Somente `PROBABILIDADE_CALIBRADA` admite calibração probabilística; ela exige proveniência `MEDIDO` e `evidencia_ref` resolvida para experimento `EXECUTADO`/`MEDIDO`. Para tipos não probabilísticos, um bloco de calibração é recusado.

`score.normalizacao` é estruturada, não uma frase livre. Em `EM_VALIDACAO+` o método precisa estar definido e aprovado; `CUSTOM_APROVADO` exige referência material.

## 6. Escopo de fontes

Na MM01, `catalogo_ref` aceita exclusivamente o placeholder `CATALOGO_PRODUTO`. A ferramenta de validação não possui flag de linha de comando para ampliar esse conjunto. Fonte fora do catálogo padrão continua sendo decisão humana/arquitetural e não override local de validação.

## 7. Integridade sintática e referencial

- YAML e JSON com chaves duplicadas são rejeitados no carregamento; não se aceita “last key wins”.
- Referências `fontes_ref` precisam apontar para fontes existentes.
- IDs duplicados são rejeitados nas coleções controladas: fontes, evidências, contra-evidências, limiares, componentes do score e experimentos.
- `score.calibracao.evidencia_ref` pertence ao namespace de `experimentos[].id` e precisa apontar para experimento `EXECUTADO` com proveniência `MEDIDO`.
- quando uma especificação anterior é fornecida, nome e versão precisam ser coerentes e a transição entre snapshots é validada contra a fase observada no documento anterior.

## 8. Não equivalências que o contrato protege

```text
sem evidência ≠ FALSE
PROPOSTO ≠ APROVADO
INFERIDO ≠ MEDIDO
caractere invisível ≠ referência auditável
score 80 ≠ 80% de probabilidade
tipo_semantica ≠ texto livre inferido
semantica_ref ≠ autorização para sobrescrever tipo_semantica
normalização estruturada ≠ frase normativa livre
evidencia_ref textual ≠ evidência de calibração resolvida
notebook executado ≠ publicação autorizada
VALIDADO ≠ PUBLICADO
fase declarada ≠ histórico de fase provado
fase declarada ≠ gate da fase satisfeito
```

Essas diferenças são semânticas do domínio, não detalhes editoriais.

## Materialidade das provas e da proveniência

A proveniência só serve como evidência auditável quando seus campos materiais possuem conteúdo efetivo. A MM01 aplica a autoridade Unicode compartilhada (`material-text` → `_has_material_text`) tanto às referências aninhadas quanto a `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo`.

A política é positiva: após NFKC, deve existir pelo menos uma letra ou número Unicode. Marcas combinantes isoladas, zero-width, formatos invisíveis, whitespace, pontuação ou símbolos sem letra/número não constituem prova. Essa regra não altera a máquina de estados nem cria fingerprint; `--previous` continua sendo comparação explícita de snapshots fornecidos.

A política também é aplicada aos campos normativos equivalentes que atravessam gates: regras de evidência e contra-evidência, hipótese e resultado de experimento, resumo do resultado de validação e motivo de condição operacional. Em especial, experimento `EXECUTADO` e condição não `ATIVO` são verificados por `_has_material_text`, não por `.strip()`.
