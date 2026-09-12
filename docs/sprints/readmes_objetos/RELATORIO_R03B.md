# R03-B — seis READMEs de apresentação e navegação

Data: 2026-09-12. Autor e revisor próprio: ChatGPT (A0_light).
Base fixa: `c60f1e54743dc23ed60b32ad2260b9aa6a77af0a`, árvore da R03-A.
Branch de trabalho: `codex/readmes-r03b`, dependente de `codex/readmes-r03a`.

## Escopo e autorização

O pedido “Siga” autorizou a próxima leva. Não foi convertido em aceite editorial
antecipado, auditoria independente ou autorização de merge. O PR nº 9 da R03-A
estava aberto e em rascunho na consulta inicial; a main estava em `b88a9cc`.
Esta entrega não altera essas branches. O PR desta leva deve ser empilhado sobre
a R03-A enquanto ela não estiver integrada.

O contrato 1.0.0, as quinze seções, os três exemplares e os 13 READMEs operacionais
anteriores foram preservados. A revisão não autoriza reescrever os padrões a
cada lote nem alterar algoritmos para adequá-los ao texto.

## READMEs novos

| Pasta sob `.assistant/hub_snippets/` | Pergunta central |
|---|---|
| `display/correlation_matrix/` | Como investigar associação sem confundir correlação, corte e causa? |
| `display/dataframe_styled/` | Como apresentar uma pequena tabela e compreender realce, formato e HTML? |
| `display/distribution_grid/` | Como ler histogramas respeitando a amostra e os dados coletados? |
| `visual/index_generator/` | Como declarar um roteiro sem apresentá-lo como auditoria de execução? |
| `visual/section_header/` | Como anunciar corretamente uma seção usando mapa ou conteúdo próprio? |
| `visual/theme_plotly/` | Como aplicar um tema sabendo o que muda na figura e na sessão? |

As seis pastas receberam `README.md`; nenhum arquivo de implementação novo foi
criado. Cada guia tem cenário fictício, uso mínimo, situações inadequadas,
interpretação, riscos e verificação do resultado. Os links cruzados entre os
seis guias são reais nesta árvore, não referências a entregas futuras.

## Outras documentações atualizadas

A [matriz nominal](MATRIZ_ALTERACOES_R03B.md) é extraída do diff contra a base e
identifica cada caminho, não apenas grupos genéricos. As alterações abrangem:

- Seis `exemplo_*.py`: backlinks e prosa corrigida, preservando código, magics e
  blocos históricos de saída. O exemplo pandas mantém instalação e reinício,
  agora avisados antes do uso; nenhum notebook foi executado integralmente.
- `hub_snippets/README.md`: rotas para os seis guias, inclusão de correlação na
  descrição narrativa e correção da atribuição indevida de badges ao cabeçalho.
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`: rotas por pasta, limites de
  correlação/coleta/tema e correção da sugestão de links no índice. As URLs
  históricas foram preservadas; não são tratadas como implementação atual.
- `MANUAL_TECNICO.md` da raiz: cópia idêntica da autoria, não segunda redação.
- `CLAUDE.md`, `PLANO_HUB.md`, `docs/sprints/README.md` e índice da iniciativa:
  estado da R03-B, dependência da R03-A e ponto de parada antes da R04-A.
- `CONTROLE_MIGRACAO.json`: apenas seis dispensas retiradas, versão e demais
  campos preservados. Candidata: **19/74 operacionais, 3/3 exemplares, 55 pendentes**.
- `CHANGELOG.md`: entrada aditiva da sessão. `README.md` da raiz: continuidade
  e contagens reconciliadas com o validador, sem recertificar publicação antiga.
- Cópias derivadas: geradas exclusivamente por `tools/render_simulado.py --write`.

Registros novos: este relatório/checkpoint, matriz, [achados](ACHADOS_R03B.md),
[rubrica](RUBRICA_R03B.json) e evidências reproduzíveis em `evidencias_r03b/`.
Esses registros não contam como novos READMEs operacionais.

## Verificações e alcance

O baseline local passou nas oito etapas existentes. O fechamento local também passou nas oito etapas: 195 testes aprovados e sete
opcionais Spark pulados por execução, sem alterar validadores, dependências ou
workflows permanentes. As contagens e os resultados efetivos estão nos logs desta entrega;
o fechamento remoto posterior é registrado no PR, sem antecipá-lo neste texto.

O suplemento `evidencias_r03b/verificar_r03b.py` contém **45 casos**: 27 portáteis
e 18 com Spark. Localmente foram executados os 27 portáteis com sucesso; os 18
Spark foram pulados por ausência de PySpark. Os testes portáteis incluem os
quatro blocos Python de tabela, índice, cabeçalho e tema. Os dois blocos dos
READMEs Spark dependem da execução remota com `--require-spark`, que não aceita
skips. A falha inicial de um teste por whitespace no CSS foi corrigida no teste,
sem alterar o helper; a evidência inicial não foi apagada.

O runner de conferência deve usar Java 17/PySpark 4.0.1, Plotly 6.5.2 e pandas
2.2.3 em ambiente isolado, sem adicionar dependências permanentes. Criar uma
SparkSession local para esse teste não é homologar serverless, Spark Connect ou
Databricks. Histogramas são conferidos por estrutura/dados, não por contagens
calculadas visualmente pelo JavaScript. Não há alegação de revisão visual no
workspace, acessibilidade certificada, MLflow ou teste conversacional.

As três suítes V00 foram reexecutadas localmente: 27 + 12 + 9 = 48 aprovados.
Reexecuções do gate ou dos suplementos não são casos novos a somar. Os sete
skips opcionais do gate de transição permanecem distintos dos 18 Spark deste
suplemento. Resultados remotos, versões e árvore exata devem constar no comentário
de fechamento do PR e no pacote entregue, após a execução efetiva.

O verificador `evidencias_r03b/verificar_preservacao.py` compara a base Git,
notebooks, APIs, padrões, guias anteriores, formulários, Concierge, V00, ativos
visuais, changelog e espelhos. As contagens de grupos podem se sobrepor: não
somá-las como arquivos únicos. Presença de títulos não certifica didática.

## Achados e limites

Foram registrados 12 achados. Destaques: corte de correlação não pinta células;
custo não independe das linhas; descarte conjunto altera o recorte; HTML da
tabela não é escapado por padrão; histogramas incorporam dados amostrados;
índice declara seleção, não execução; cabeçalhos não consomem o estilo central;
tema modifica a figura, pode acumular rodapés e não confere a fonte declarada.

As limitações foram explicadas e caracterizadas, não corrigidas funcionalmente.
Os textos que descreviam capacidades inexistentes foram reconciliados sem
reescrever evidências históricas. Código, paleta, CSS e formulário não mudaram.

## Checkpoint e próxima ação

Estado: **seis guias escritos e autorrevisados, pendentes de aceite editorial e
integração do PR**. A cobertura reportada é da candidata, não da main nem de um
workspace. O PR da R03-B depende da R03-A; integrar em ordem e reconferir refs/CI
se houver trabalho paralelo. Não encerrar ou integrar PRs automaticamente.

Pausa antes da R04-A: a próxima leva prevista contém `date_features`,
`join_diagnostics`, `null_summary`, `psi_calculator`, `safe_display` e `smart_sample`.
Não executada nesta rodada. Nenhuma publicação Databricks ou auditoria independente.
