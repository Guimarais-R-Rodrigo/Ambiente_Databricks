# Relatório R04-B — seis Hub Scripts

Data: 2026-09-12. Base: `a8f314a31106aceb52db2661544146cc2bddcc99`, `main` após integração e pós-merge verde da R04-A.

## Objetivo

Documentar os seis objetos `hub_scripts` previstos no controle de migração sem alterar suas implementações: `data_quality_check`, `doc_coverage`, `drift_detector`, `naming_checker`, `rfv_calculator` e `schema_to_yaml`.

A sprint mantém o contrato de README **1.0.0**, preserva o comportamento funcional existente, registra limitações encontradas e atualiza as rotas necessárias para que uma pessoa que nunca entrou no Hub consiga localizar, entender e validar cada script.

## Entregas canônicas

Seis novos `README.md` foram criados nas pastas dos scripts. Cada documento contém Visão rápida e exatamente quinze seções numeradas, com conceito antes da sintaxe, situações adequadas/inadequadas, entradas, retorno real, configurações, limitações, alternativas e verificações.

Os notebooks de exemplo recebem apenas documentação/backlinks. A guarda da sprint impede mudança do AST, magics executáveis, blocos históricos de output e linhas executáveis/comentários Python.

## Achados que mudaram a redação

O [registro de achados](ACHADOS_R04B.md) separa comportamento observado de recomendação. Entre os pontos principais:

- o score de `data_quality_check` é uma fórmula local e a atualidade usa `date.today()`;
- `doc_coverage` mede adjacência e pode retornar 100% para Markdown vazio ou notebook sem código;
- `drift_detector` implementa PSI numérico, classifica apenas quando os dois limiares são fornecidos e usa `epsilon` sem renormalizar proporções;
- `naming_checker` produz apenas warnings e separa recomendação de contexto de políticas locais;
- `rfv_calculator` usa um corte global, conta linhas como frequência e não resolve atraso de disponibilidade;
- `schema_to_yaml` usa cardinalidade aproximada e pode retornar YAML ou JSON válido em YAML 1.2 conforme a presença de PyYAML.

Nenhum desses pontos foi “corrigido” alterando código nesta sprint.

## Documentação além dos READMEs

A sprint também atualiza:

- `ambiente_fonte/.assistant/hub_scripts/README.md`, com rotas locais aos seis guias;
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md` e sua cópia de leitura na raiz;
- `README.md`, `CLAUDE.md`, `PLANO_HUB.md` e `docs/sprints/README.md`, para continuidade e contagens reais;
- `docs/sprints/readmes_objetos/README.md`, com checkpoint e rotas da R04-B;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`, retirando somente as seis dispensas desta leva;
- `CHANGELOG.md`, por entrada aditiva;
- simulado, exclusivamente por `tools/render_simulado.py --write`.

A [matriz nominal](MATRIZ_ALTERACOES_R04B.md) diferencia autoria, agregadores e derivados.

## Estratégia de testes

O fechamento exige quatro camadas:

1. gate permanente do repositório, incluindo sistema de temas, validador, biblioteca, ferramentas, transição, READMEs e Concierge;
2. suítes V00/V01/V02 já existentes, para evitar regressão da frente paralela de temas;
3. `evidencias_r04b/verificar_preservacao.py`, comparando produto e documentação protegida contra a base `a8f314a`;
4. `evidencias_r04b/verificar_r04b.py --require-spark`, com PySpark real, exercitando os seis scripts e os contratos estáticos dos novos guias.

O resultado remoto final, versões, run ID, árvore materializada e contagem líquida serão acrescentados no fechamento técnico antes da abertura do PR final. Enquanto esse bloco não estiver preenchido, a sprint **não** deve ser tratada como concluída.

## Estado de cobertura

A base possui 26/75 objetos operacionais documentados e 49 pendentes. A entrega destes seis scripts deve levar a estrutura para **32/75 operacionais**, 3/3 exemplares e **43 pendências**, mas a fonte de verdade será a saída do validador sobre a árvore final — não esta conta manual.

## Limites

- Autoria e autorrevisão ChatGPT, nível A0_light.
- Sem auditoria independente.
- Sem publicação/homologação no Databricks ou Genie Code.
- Sem mudança funcional dos seis scripts.
- Sem início da R05 antes do aceite da R04-B.

## Fechamento técnico remoto

Workflow de fechamento: **run 34725459631 — success até esta etapa**. Na árvore final: gate permanente de 9 etapas aprovado; validador com 0 falhas/0 avisos; V00 48/48; V01 138/138; V02 105/105; preservação PASS; suíte R04-B **14/14 aprovada sem skips** com Java 17, PySpark 4.0.1 e PyYAML 6.0.2. A cobertura validada é **32/75 operacionais, 3/3 exemplares e 43 pendências**. A materialização ocorre somente após a reconferência abaixo.

## Addendum de integração com V03

Após o freeze original, a `main` avançou para `b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2` com a V03. O run `34726148034` recompõe a entrega sobre essa base e só materializa a árvore se todas as guardas passarem. Registro detalhado: `CONCILIACAO_R04B_V03.md`.
