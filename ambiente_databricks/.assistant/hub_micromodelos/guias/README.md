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

| Capacidade | Entrada e resultado | Limite |
|---|---|---|
| Validar e assinar | YAML e schema; problemas estruturados e fingerprint | Estrutura válida não aprova fontes/regras. |
| Descobrir metadados | Sessão/catálogo/escopo autorizados; envelope observado | Não lê registros de negócio nem garante completude. |
| Classificar o exemplo | Fixture fictícia; classes e scores reconciliados | Sem calibração ou validade em dados reais. |
| Preparar artefatos/tracking | Contrato e política; scaffold `NOT_RUN` ou run se executada | Gerar texto não abre MLflow; run não aprova. |
| Preparar entrega | Contrato e evidência; `DRAFT_NOT_SUBMITTED` | `published=false`; governança externa decide. |
| Comparar legados | Saídas sintéticas; diferenças explícitas | Não migra nem promove um caso institucional. |

Pare quando metadados forem negados, parciais ou insuficientes para a decisão. Não complete fontes por inferência. Leitura de registros exige autorização e plano de minimização próprios. Validação pendente e handoff não submetido impedem declarar publicação. Ensaios locais não homologam uma instalação nova.

## O que vai para cada lugar

| Registro | Lugar | Motivo |
|---|---|---|
| Definição, estado, regras, fonte e proveniência | `micromodelo.yaml` do caso | Especificação canônica versionável. |
| Código reutilizável | `hub_micromodelos/execucao/` | Mesmo código instalado pelo pacote do Hub. |
| Dados e resultados do ensaio | `hub_micromodelos/exemplos/` | Demonstração E0 sem dados corporativos. |
| Runs e métricas efetivamente observadas | MLflow do ambiente autorizado | Histórico de execução, separado do YAML. |
| Decisão de aceite e publicação | Canal de governança externo | Autoridade não pertence ao código nem à skill. |

O [README principal](../README.md) é a entrada; o [contrato](../contratos/README.md) explica os estados; [execução](../execucao/README.md) aponta as funções; o [Manual Técnico](../../MANUAL_TECNICO_V2.md#micromodelos) explica a integração com o Hub.
