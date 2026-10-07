# Micromodelo fictício de recência de contato

Este caso mostra **todos os blocos do contrato** com sete pessoas e seis eventos inteiramente inventados. A pergunta didática é: “há contato recente verificável com idade de zero a sete dias, inclusive, em 2026-09-30?”. `TRUE`, `FALSE` e `INDETERMINADO` são estados de evidência; nenhum deles é decisão sobre uma pessoa real.

## Roteiro para avaliar

1. Leia [micromodelo.yaml](micromodelo.yaml), depois [dados_sinteticos.json](dados_sinteticos.json).
2. Execute `python hub_micromodelos/exemplos/recencia_contato/executar_exemplo.py --conferir` a partir da pasta `.assistant`, com Python, `jsonschema`, `regex` e `PyYAML` disponíveis.
3. Compare as sete linhas e o resumo com [resultado_esperado.json](resultado_esperado.json). O comando `--conferir` faz essa comparação automaticamente e falha se houver divergência.
4. Preserve os arquivos originais. Se houver autorização para explorar, faça uma cópia de trabalho da pasta do exemplo e edite nela `classificacao.limiares[0].valor` de `7` para `2`; execute a cópia sem `--conferir`. `pessoa_f` deixa de ser `TRUE`, pois seu contato de 23/09 tem sete dias; a assinatura material muda. `--conferir` e `conferir_entrega.py` validam o contrato original. Não altere o oráculo só para obter PASS.
5. Execute `python hub_micromodelos/exemplos/recencia_contato/conferir_entrega.py` para reconciliar o mesmo resultado e ver o rascunho de handoff. Esse comando exige o YAML original e o oráculo inalterado.

Os scripts leem somente os arquivos desta pasta, não consultam o Databricks e não gravam saídas ou tabelas. O hash no resultado é a assinatura dos campos materiais calculada pelo módulo [assinatura](../../execucao/assinatura.py).

## Resultado calculado

| Pessoa | Evento relevante | Classe | Score | Motivo |
|---|---|---|---:|---|
| `pessoa_a` | contato confirmado em 28/09 | `TRUE` | 82 | contato recente confirmado |
| `pessoa_b` | atestado explícito sem contato em 30/09 | `FALSE` | 0 | ausência verificada, com cobertura completa |
| `pessoa_c` | contato confirmado em 10/09 | `INDETERMINADO` | `null` | apenas contato antigo |
| `pessoa_d` | sem evento e cobertura parcial | `INDETERMINADO` | `null` | cobertura incompleta |
| `pessoa_e` | contato e estorno em 29/09 | `INDETERMINADO` | `null` | sinais conflitantes |
| `pessoa_f` | contato confirmado em 23/09 | `TRUE` | 39 | limite inclusivo de sete dias |
| `pessoa_g` | nenhum evento, cobertura completa | `INDETERMINADO` | `null` | ausência não prova `FALSE` |

O resumo tem população 7, contagens `TRUE=2`, `FALSE=1`, `INDETERMINADO=4` e três scores emitidos. Para contatos recentes válidos, `score = round(100 × [peso_proximidade × (1 − idade_em_dias / (janela_dias + 1)) + peso_cobertura])`; neste YAML, os pesos são `0,7` e `0,3` e a janela é `7`. O score mede **força de evidência sob esta regra sintética**; não é probabilidade. `FALSE` usa 0 apenas porque há evidência negativa explícita. Ausência simples, contato antigo e conflito não recebem 0.

## Reconciliação e rascunho de entrega

`conferir_entrega.py` recalcula as contagens das sete linhas, verifica que somam a população, confere os três scores emitidos e só então chama `execucao/entrega.py`. O agregado local tem mínimo 0, máximo 82 e média 40,33. O handoff devolve a mesma assinatura da especificação, `DRAFT_NOT_SUBMITTED`, `published=false` e a lista de decisões pendentes. A API rotula o agregado recebido como `SUPPLIED_UNVERIFIED`: a checagem deste script é uma **reconciliação didática local**, não autenticação de medição externa. Não há run MLflow deste caso (`NOT_RUN`), aceite humano ou Produto de Dados.

## Mapa de todos os atributos do YAML

Os caminhos abaixo cobrem cada bloco de topo do [JSON Schema](../../contratos/micromodelo.schema.json). Campos `proveniencia` aparecem em fontes, regras, limiares, score e experimentos; seguem sempre o mesmo conjunto descrito na última linha da tabela. `[]` indica uma lista cujos itens têm os mesmos atributos.

| Atributos | Valor neste exemplo e onde entram |
|---|---|
| `schema_version` | `1.0.0` seleciona a versão do contrato validado por `especificacao.py`. |
| `identidade.nome`, `titulo`, `micromodel_version` | Identificador, título legível e versão `0.1.0` do estudo fictício. O nome aparece na saída. |
| `identidade.estado.fase_atual`, `fase_anterior`, `condicao`, `motivo_condicao` | Estudo em `EM_ESTUDO`, vindo de `EM_DESCOBERTA`, ativo. `motivo_condicao=null` porque não houve suspensão ou encerramento. O validador impede saltos de fase inconsistentes. |
| `negocio.caracteristica`, `objetivo`, `definicao_operacional` | Dizem qual característica inferir, por quê e qual regra observável aplica. O script implementa a definição operacional sintética. |
| `negocio.uso_pretendido[]`, `nao_usar_para[]` | Limitam o uso ao aprendizado e excluem decisões reais, oferta e publicação. São contexto para revisão humana, não permissões técnicas. |
| `entidade.tipo`, `chave_logica`, `granularidade`, `populacao_elegivel`, `referencia_temporal` | Identificam pessoas fictícias por `id_entidade`; cada pessoa recebe uma linha na data 2026-09-30. O script confere chaves e data de referência. |
| `fontes[].id`, `catalogo_ref`, `schema`, `objeto`, `tipo_objeto`, `campos[]`, `papel` | Duas fontes fictícias: cobertura (`ELEGIBILIDADE`) e eventos (`EVIDENCIA`). `CATALOGO_PRODUTO` é o marcador permitido pelo contrato, não uma permissão de acesso. Os nomes demonstram binding documental; os dados vêm apenas do JSON local. |
| `evidencias[].id`, `descricao`, `fontes_ref[]`, `regra` | Contato `CONFIRMADO` recente remete à fonte de eventos; a regra é aplicada pelo script. O identificador permite rastrear a evidência. |
| `contra_evidencias[].id`, `descricao`, `fontes_ref[]`, `regra` | `NEGATIVO_VERIFICADO` é a contraevidência explícita para `FALSE`; `ESTORNADO` com confirmação produz conflito. Nenhuma ausência silenciosa vira `FALSE`. |
| `classificacao.tipo`, `semantica.quando_true`, `quando_false`, `quando_indeterminado` | Definem o domínio de três valores e suas condições distintas. A tabela acima mostra cada saída. |
| `classificacao.ausencia_evidencia.tratamento`, `resultado_sem_evidencia`, `regra_ref` | Tratamento `INDETERMINADO`, resultado igual e `regra_ref=null` porque não existe regra aprovada para converter falta de registros em `FALSE`. |
| `classificacao.limiares[].id`, `descricao`, `operador`, `valor`, `unidade` | `janela_recencia_dias`, `LTE`, `7`, `dias`: contato com idade de sete dias ainda conta. O script usa esse valor e recusa outra forma de limiar que não implementa. |
| `score.habilitado`, `tipo_semantica`, `semantica_ref` | Score ativo de `FORCA_EVIDENCIA`; `semantica_ref=null` porque a semântica está descrita no próprio YAML, sem documento externo. |
| `score.escala.min`, `max`, `normalizacao.metodo`, `referencia` | Escala 0–100; `SOMA_PONDERADA_0_100`; `referencia=null` porque a fórmula sintética está aqui e no código, sem método institucional externo. |
| `score.componentes[].id`, `descricao`, `peso` | Proximidade temporal (`0.7`) e cobertura confirmada (`0.3`). O script usa os pesos e exige soma igual a um. |
| `score.calibracao`, `proveniencia` | `calibracao=null`: força de evidência não é probabilidade calibrada. A proveniência do score registra proposta sintética, sem medição corporativa. |
| `experimentos[].id`, `hipotese`, `status`, `resultado` | Ensaio de recência `PROPOSTO`; `resultado=null` até uma medição registrada como experimento. Rodar o exemplo é uma checagem didática e não muda esse estado por conta própria. |
| `validacao.status`, `criterios[]`, `resultado` | `PENDENTE`; os critérios explicam o que revisar. `resultado=null` porque ainda não há validação institucional medida. |
| `validacao.aprovacao_humana.status`, `por`, `em_utc`, `referencia` | `PENDENTE` e demais campos `null`. Nenhuma pessoa ou aprovação foi simulada como fato. |
| `saida.estudo.campo_classificacao`, `valores_classificacao[]`, `campo_score` | Nomes `classificacao` e `score` e os três valores possíveis; correspondem às linhas emitidas. |
| `saida.publicacao.estado`, `campo_booleano`, `politica_indeterminado` | `PENDENTE`, `null`, `null`; ainda não existe produto de dados nem política externa para publicar. |
| `tracking.backend`, `politica`, `armazenar_historico_runs_no_yaml` | Backend previsto `MLFLOW`, política `PENDENTE_MM06`, histórico de runs fora do YAML (`false`). O exemplo local registra `mlflow=NOT_RUN`. |
| `governanca.classificacao_dados`, `lgpd`, `gestor_informacao`, `observacoes[]` | Declaram a fixture sintética e a necessidade de responsável para qualquer uso real. São lembretes documentais, não homologação. |
| `publicacao.status`, `autoridade`, `handoff_ref`, `produto_dados_ref` | `NAO_INICIADA`, `GOVERNANCA_EXTERNA` e referências `null`; nenhuma publicação ocorre. |
| `proveniencia.criado_em_utc`, `gerado_por`, `pedido_original_ref`, `registros[].alvo` | Data, autoria sintética, referência do briefing e trilha dos campos propostos. Os registros explicam a origem do texto, não um aceite. |
| `*.proveniencia.status`, `origem`, `referencia`, `observado_em_utc`, `aprovacao`, `medicao` | Status indica `PROPOSTO` ou metadado `DESCOBERTO` na fixture; origem e referência apontam para o caso. Datas, aprovações e medições permanecem `null` quando não ocorreram. O validador confere combinações de status e metadados. |

## Atributos condicionais do schema

O contrato também aceita estados posteriores, sujeitos a evidências adicionais. Aqui eles aparecem com `null` ou `PENDENTE` para não inventar aprovações:

| Variante | Campos que passariam a ser preenchidos | Condição |
|---|---|---|
| `score.tipo_semantica=PROBABILIDADE_CALIBRADA` | `score.calibracao.metodo`, `evidencia_ref`, `proveniencia` | Exige experimento executado e medição válida. Não se aplica à fórmula atual. |
| `classificacao.ausencia_evidencia.tratamento=REGRA_EXPLICITA_APROVADA` | `regra_ref` e proveniência aprovada | Exigiria regra auditável e decisão humana; por isso falta de eventos continua indeterminada. |
| `validacao.status=APROVADO` ou `REPROVADO` | `validacao.resultado.resumo` e proveniência `MEDIDO`; `aprovacao_humana.por`, `em_utc`, `referencia` | Exige medição e decisão humana correspondentes. |
| `saida.publicacao.estado=DEFINIDO` | `campo_booleano.nome`, `tipo=BOOLEAN`; política de indeterminado com tratamento, `indeterminado_vira_false=false`, proveniência e `regra_ref` conforme opção | Só após definição externa da saída; o exemplo não transforma `INDETERMINADO` em `FALSE`. |
| `publicacao.status` posterior a `NAO_INICIADA` | `handoff_ref`, `produto_dados_ref` conforme etapa | Depende dos gates de validação e da autoridade externa. |

Uma mudança editorial em `negocio.objetivo` pode preservar a assinatura; alterar o limiar, uma fonte, uma regra ou os pesos produz nova assinatura. O script recusa formatos que esta demonstração não implementa. O [laboratório de execução](../../execucao/README.md) mostra outros recursos da biblioteca; este caso foi feito para inspeção dos atributos e da semântica, não para estimar desempenho real.
