# 12 — Fontes, proveniência e limite de cada afirmação

## 12.1 Base de planejamento

A proposta aprovada P0 é a base desta especificação. As decisões novas detalham sua operacionalização e estão identificadas como desenho, fixtures propostas ou requisitos a implementar. Não transformar o plano em relatório de testes concluídos.

A `main` foi consultada nesta sessão no GitHub e apontou para `d2988e97e7b6c5fe1fd561852e947a155c2d731b`. As leituras diretas abaixo foram vinculadas a essa base. Cabeçalhos SER00 com SHAs antigos são evidência histórica, não a ref vigente.

| ID | Fonte | O que sustenta | Profundidade |
|---|---|---|---|
| P0 | `SER_PLANO_PARALELO_PROPOSTA_2026-09-23.md` | Proposta aprovada pelo usuário; terminologia, papéis, oito dossiês e limitações. | READ_IN_FULL |
| P1 | `SER01_medicoes_retrospectivas.json` | Tempos de summaries sanitizados; não mede autoria/auditoria/espera humana. | READ_IN_FULL |
| R01 | `CLAUDE.md` | Hierarquia, fonte/derivado, changelog e contexto canônico. | READ_AT_BASE |
| R02 | `.claude/CLAUDE.md` | Índice operacional e rota de leitura. | READ_AT_BASE |
| R03 | `.claude/rules/multi-llm.md` | Papéis, adaptação de contexto e auditoria multi-IA. | READ_AT_BASE |
| R04 | `.claude/rules/docs-e-readmes.md` | Documento dono, estados verificáveis, ADR aceito e linguagem. | READ_AT_BASE |
| R05 | `docs/sprints/skill_enforcement_rollout/PLANO_MESTRE.md` | Metas/sprints/gates/ordem histórica; trecho amplo lido, saída longa com truncamento. | READ_RELEVANT_SECTIONS |
| R06 | `docs/sprints/skill_enforcement_rollout/SER00/MATRIZ_DEPENDENCIAS.md` | Dependências reais e ordem de integração distinta de dependência universal. | READ_AT_BASE |
| R07 | `docs/sprints/skill_enforcement_rollout/SER00/MATRIZ_HELPERS_PRIMITIVES.md` | Public API versus declarado, lacunas SHAP/PIT/tracking/materialização. | READ_AT_BASE |
| R08 | `tools/skill_enforcement/certify_local.py` | Linhas 80–276; 21 gates do perfil SE08, process records e budgets. | READ_RELEVANT_SECTIONS |
| R09 | `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/__init__.py` | Fachada exporta compute_shap/importance/plots; não comprova assinatura ou execução. | READ_AT_BASE |
| R10 | `tools/ci_local.py` | Nove etapas não-SEF e sef cumulativo descritos na proposta e no histórico fornecido; reler integralmente em B0. | SOURCE_DERIVED_REVALIDATE_BEFORE_EXECUTION |
| R11 | `docs/decisions/ADR-0022-certificacao-prospectiva-ser.md` | Preservação de SEF histórico, certificação prospectiva, último ato funcional e aceite. | SOURCE_DERIVED_REVALIDATE_BEFORE_FORMALIZATION |
| R12 | `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json` | Vetor de capacidade confirmado no fechamento SER01 e proposta aprovada; reconfirmar no release preflight. | SOURCE_DERIVED_REVALIDATE_BEFORE_EXECUTION |
| H01 | `report(3).md: SER01 A4-FREE R2` | Erro de transporte com efeito servidor observado; preservar resultado de comando e efeito separadamente. | RETRIEVED_RELEVANT_EXCERPTS |
| H02 | `A4_GENIE_FORMULARIO_PREENCHIDO.md` | Transcrição sem indicador da UI; narrativa não equivale a chamada observada. | RETRIEVED_RELEVANT_EXCERPTS |
| W01 | `https://learn.chatgpt.com/docs/agent-configuration/subagents` | Agentes customizados, limites, herança de permissões e overrides; configuração efetiva precisa de qualificação local. | WEB_VERIFIED_2026_09_23 |

## 12.2 Evidência histórica versus inferência

P1 reporta duas durações de campanhas: 537,41721 s para A3-R3 e 375,12867 s para promoção R2. Não inclui autoria, preparação, auditoria, publicação ou espera humana. A conclusão de que padronização deve atacar também handoffs é uma inferência de desenho, não um percentual de desperdício calculado desses tempos.

A matriz de helpers R07 distingue export público, implementação inspecionada e simples declaração. A elaboração deste plano não executou cada helper nem enumerou todos os seus métodos de teste. A cobertura real por primitive continua tarefa explícita da autoria B0/B1.

Os casos e fixtures EX/VF/ST/CE/FE/BM/MO/PB são propostas novas desta entrega para materialização repo-side. Valores de referência simples foram definidos por raciocínio independente e podem ser conferidos sem a implementação produtora. A escolha final de método/semântica precisa respeitar o contrato fechado, não apenas copiar a fixture.

## 12.3 Documentação externa

W01 foi consultada para evitar pressupor configuração antiga do Codex. O plano usa aliases de modelos a resolver e testes de permissões efetivas. Nenhuma versão instalada, quota, hardware ou configuração do usuário foi observada nesta etapa; permanecem precondições de qualificação.

A disponibilidade de operações Databricks Free/MLflow/jobs/materialização não foi novamente verificada pela UI nesta sessão. O desenho exige descoberta autorizada e prova pessoal proporcional antes de declarar uma superfície L4 operacional.

## 12.4 Verificações feitas nesta entrega

Leitura da proposta e retrospectiva; leitura seletiva das fontes do repositório; conferência da ref main; consulta oficial sobre subagentes; geração do pacote documental e dos catálogos; validações locais do próprio pacote registradas no relatório de validação.

Não houve campanha de skill, treino/SHAP/PIT/Spark, probe Databricks, publicação, alteração de policy, commit GitHub ou merge. O validador desta entrega valida documentação/catálogos/links/DAG, não substitui testes B0 ou certificação do produto.

## 12.5 Disponibilidade de escrita no GitHub

O conector ativo foi inspecionado: as ações disponíveis nesta sessão são de leitura. A busca do plugin confirmou o GitHub instalado, mas não expôs ação de publicação de arquivos. Portanto esta entrega fornece bytes e patch preparados, sem alegar commit ou PR inexistente. Esse limite é operacional desta sessão, não uma afirmação de que o repositório nunca possa ser escrito pelo ChatGPT.
