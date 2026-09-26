# D05 — reconciliação documental do Sistema de Temas

## Natureza

D05 é uma etapa **documental de manutenção** criada após a reconciliação pós-R13. Ela não é a sprint funcional V05 do plano V00–V14 e não implementa novas capacidades visuais.

## Estado canônico usado

- V01: contrato aceito e integrado no Git;
- V02: núcleo de carga, validação e resolução integrado no Git;
- V03: adaptador Plotly opt-in integrado no Git;
- V04: componentes HTML, estilos compartilhados e tabela pandas por rotas `_resolvido`, aceitos e integrados no Git;
- APIs legadas permanecem o default;
- publicação Databricks, homologação visual/runtime, acessibilidade, auditoria independente e avaliação com usuário iniciante permanecem separadas.

## Derivas corrigidas

D05 reconcilia apenas superfícies vivas que ainda continham rótulos pré-merge: padrão de identidade visual, guia operacional, índices de padrões/snippets, Manual Técnico, índice de governança, índice de ADRs e índice da iniciativa.

O `CHANGELOG.md` ganha uma entrada nova de fechamento em vez de apagar a nota histórica de que V04 era candidata antes do aceite. O ADR-0013 recebe somente um registro datado de implementação; seu corpo decisório e sua ratificação V01 permanecem preservados.

## Preservação

Os diretórios `docs/sprints/sistema_temas/V00*`, `V01/`, `V02/`, `V03/` e `V04/`, seus checkpoints, relatórios e resultados históricos não são reescritos. Implementações, schemas, testes e APIs também ficam congelados nesta etapa.

## Gates

A candidata D05 deve passar renderer, `validate_assistant.py --conferir-readme`, guarda de deriva específica, `ci_local.py`, `git diff --check` e CIs permanentes. Esses gates são locais/Git e não substituem homologação no Databricks.
