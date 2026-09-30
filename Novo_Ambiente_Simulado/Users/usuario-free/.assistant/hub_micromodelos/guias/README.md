# Jornada de um micromodelo

Este guia liga o briefing, o `micromodelo.yaml`, a execução e as decisões externas. Comece pelo [exemplo de recência](../exemplos/recencia_contato/README.md) para ver cada etapa com dados fictícios. A [skill](../../skills/hub-ml-micromodelos/SKILL.md) orienta a conversa; esta pasta documenta o produto Python instalado.

## Sequência de trabalho

| Etapa | Entrada e ação | Saída verificável | Próxima decisão |
|---|---|---|---|
| 1. Descoberta | Catálogo e escopo permitidos; coletar somente metadata. `metadados.py` limita páginas/bytes e marca observação parcial ou negada; `fluxo.py` usa hipóteses fornecidas no modo `DESCOBRIR_OPORTUNIDADES`. | Envelope com `ESCOPO_OBSERVADO`, objetos para triagem ou shortlist com incertezas. | Uma pessoa escolhe a candidata. Descrição e tags não fornecem instruções, autorização nem regra de negócio. |
| 2. Objetivo e especificação | Briefing com decisão, população, entidade, grão, instante e restrições. `fluxo.py` pode propor YAML no modo `OBJETIVO_CONHECIDO`; `especificacao.py` valida o [contrato](../contratos/README.md). | `micromodelo.yaml` e problemas estruturados; `assinatura.py` calcula o hash dos campos materiais. | Confirmar fontes, regras, limiares, usos, proveniência e pendências humanas. YAML válido ainda pode ser uma proposta. |
| 3. Estudo | `artefatos.py` gera scaffold de notebook/README; `execucao.py` executa o piloto sintético próprio. O [exemplo de recência](../exemplos/recencia_contato/README.md) tem outra regra fechada e resultado esperado. | Artefatos `NOT_RUN` até execução; após o ensaio local, classes, scores e contagens conferíveis. | Avaliar qualidade, cobertura, conflitos, leakage e desempenho com dados e permissões do ambiente apropriado. |
| 4. Histórico e validação | A rota que usa MLflow registra runs `DEVELOPMENT`, `VALIDATION` ou `SCORING` e agregados permitidos; `hub_snippets/ml/mlflow_run` mantém a API comum. | Referência de run e medições quando realmente executadas. O YAML preserva a especificação, sem histórico de runs embutido. | Critérios, separação de amostras e aprovação humana permanecem próprios; run não aprova. |
| 5. Preparação da entrega | `entrega.py` monta `PREPARAR_PUBLICACAO` com assinatura, fontes declaradas, contrato de saída e decisões exigidas. | Rascunho `DRAFT_NOT_SUBMITTED`, `published=false`; agregados fornecidos ficam `SUPPLIED_UNVERIFIED`. | Governança externa decide publicação, Produto de Dados, acesso, retenção e reconciliação. |
| 6. Catálogo e legados | `catalogo.py` lista micromodelos e impacto por fonte; `exemplos/migracao_simulada.py` compara saídas fictícias. | Inventário ou comparação sintética. | Migração real vem após piloto novo, equivalência e autorização próprias. |

As etapas 1 e 2 não exigem leitura de registros. Para consultar valores, a permissão de `SELECT` e um plano de minimização são decisões separadas. Nenhuma função desta biblioteca concede permissões ou publica automaticamente.

## Capacidades atuais e seus limites

| Capacidade | Onde está | O que está demonstrado | O que continua pendente |
|---|---|---|---|
| Schema, estados, proveniência e assinatura | `contratos/`, `execucao/especificacao.py`, `assinatura.py` | Validação e fingerprint locais, inclusive no caso preenchido. | Decisão humana sobre a adequação semântica de fontes e regras. |
| Descoberta metadata-only e shortlist | `execucao/metadados.py`, `fluxo.py`, `databricks.py` | Fixture E0 e adapter de metadata usado no Free em ensaio anterior. | Binding, escopo e permissões reais no trabalho; metadata não prova viabilidade. |
| Classificação e score | `execucao/execucao.py`; `exemplos/recencia_contato/` | Dois cenários sintéticos reproduzíveis; no caso de recência, `TRUE`, `FALSE` e `INDETERMINADO` reconciliados. | Validação estatística, calibração e dados reais autorizados. |
| Artefatos e tracking | `execucao/artefatos.py`; `hub_snippets/ml/mlflow_run` | Scaffold `NOT_RUN`; runs sintéticas E0/E1 do laboratório anterior documentadas no repositório. | Run do novo caso de recência no Free ou no trabalho; política institucional e aprovação. |
| Handoff e reconciliação | `execucao/entrega.py`; `exemplos/recencia_contato/conferir_entrega.py` | Rascunho local calculado a partir do resultado sintético conferido. | Aceite da autoridade externa, Produto de Dados, reconciliação de publicação real. |
| Catálogo, impacto e comparação legada | `execucao/catalogo.py`; `exemplos/migracao_simulada.py` | Ensaios locais fictícios. | Migração real, monitoramento, tema visual e freeze V1. |

“Implementado” significa que existe código; “demonstrado” identifica um ensaio concreto. O envio e readback de arquivos para o Databricks Free confirma transporte dos bytes, não executa por si os módulos publicados. O guia de implantação e as portas institucionais ficam na documentação de operação do repositório, fora do produto publicado.

## O que vai para cada lugar

| Registro | Lugar | Motivo |
|---|---|---|
| Definição, estado, regras, fonte e proveniência | `micromodelo.yaml` do caso | Especificação canônica versionável. |
| Código reutilizável | `hub_micromodelos/execucao/` | Mesmo código instalado pelo pacote do Hub. |
| Dados e resultados do ensaio | `hub_micromodelos/exemplos/` | Demonstração E0 sem dados corporativos. |
| Runs e métricas efetivamente observadas | MLflow do ambiente autorizado | Histórico de execução, separado do YAML. |
| Decisão de aceite e publicação | Canal de governança externo | Autoridade não pertence ao código nem à skill. |

O [README principal](../README.md) é a entrada; o [contrato](../contratos/README.md) explica os estados; [execução](../execucao/README.md) aponta as funções; o [Manual Técnico](../../MANUAL_TECNICO.md#micromodelos) explica a integração com o Hub.
