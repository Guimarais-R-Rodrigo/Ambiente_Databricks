# MM00 — Inventário

## 1. Estado do repositório

Baseline: `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.

A busca por `micromodel` no código da `main` não retornou implementação ou documentação específica. A iniciativa começa, portanto, sem objeto homônimo concorrente no repositório.

## 2. Fonte de verdade e disciplina de alteração

- `CLAUDE.md` é contexto canônico para as IAs.
- `ambiente_fonte/` é a única camada editável do produto `.assistant`.
- `Novo_Ambiente_Simulado/` é derivado e não deve ser editado manualmente.
- Workspaces são superfícies operacionais, não fonte canônica.
- Mudanças estruturais exigem ADR; toda sessão que altera algo exige changelog.

### Achado MM00-A01

O `CLAUDE.md` ainda descreve a frente visual em estado anterior, enquanto a `main` já contém V00–V07 integradas. Isso é risco documental para sessões futuras e deve ser reconciliado em manutenção documental, sem alterar implementação visual.

## 3. Taxonomia do Hub

A taxonomia vigente é fechada em seis tipos:

1. snippet;
2. script;
3. prompt;
4. README;
5. notebook;
6. skill.

`hub-ml-criar-objeto` e `hub_padroes/skill/template.md` explicitam que não se deve inventar um sétimo tipo. Micromodelo deve permanecer artefato de domínio que consome esses tipos.

## 4. Padrões transversais existentes

`ambiente_fonte/.assistant/hub_padroes/` já contém padrões de:

- auditoria;
- identidade visual;
- notebook;
- output/proveniência;
- prompt;
- README;
- script;
- skill;
- snippet.

Conclusão: o framework de micromodelos deve especializar o domínio dentro de sua skill, sem criar convenções paralelas para estruturas já cobertas.

## 5. Skills relevantes

### Descoberta/composição

- `hub-ml-concierge`: encontra e compõe recursos existentes; não executa análise.

### Dados e modelagem

- `hub-ml-eda-profissional`: exploração de uma fonte.
- `hub-ml-cross-eda-ml`: múltiplas fontes, entidade, tempo, coverage, joins e readiness.
- `hub-ml-feature-engineering`: especificação e implementação de features, temporalidade e leakage.
- `hub-ml-validacao-estatistica`: validação de hipótese/evidência.

### Engenharia e governança local

- `hub-ml-comentar-notebook`: adiciona documentação sem mudar código.
- `hub-ml-auditoria-skills`: audita implementação de skills e outputs contra contrato.
- `hub-ml-criar-objeto`: cria objetos do Hub segundo `hub_padroes`.

### Decisão de MM00

A futura `hub-ml-micromodelos` deverá orquestrar o domínio e realizar handoff para essas skills quando a responsabilidade já estiver coberta. Não deve copiar suas metodologias.

## 6. Prompts existentes

`hub_prompts` já possui briefings de EDA, qualidade, cross-EDA, feature engineering, baseline, explicabilidade, monitoramento, auditoria, documentação e outros fluxos.

O contrato vigente exige README, briefing e notebook de demonstração; respostas conversacionais reais não podem ser inventadas. Novos prompts de micromodelos devem usar a mesma infraestrutura editorial.

## 7. Scripts relevantes

### `hub_scripts.schema_to_yaml`

- recebe nome de tabela;
- serializa nome, tipo, nulabilidade e comentários disponíveis;
- pode incluir estatísticas opcionais;
- não exporta ownership, tags completas, constraints, permissões ou lineage;
- é fotografia técnica, não catálogo governado.

Decisão: reutilizar para inspeção aprofundada de tabelas já selecionadas; não transformá-lo em crawler global.

### Outros candidatos

- `quick_profile` — perfil técnico quando leitura de dados já estiver autorizada.
- `data_quality_check` — diagnóstico de qualidade de tabela nomeada.
- `rfv_calculator` — recência/frequência/valor quando a hipótese exigir esse padrão.

## 8. Snippets relevantes

### Spark

- `join_diagnostics` — cobertura, multiplicidade e expansão de join.
- `pit_join` — alinhamento point-in-time.
- `null_summary` — nulos/cobertura por coluna.
- `smart_sample` e `safe_display` — amostragem/exibição limitada quando apropriadas.

### ML/MLOps

- `mlflow_run` — contexto governado de run MLflow.
- objetos de monitoramento/drift já existem na biblioteca e devem ser avaliados antes de qualquer helper novo.

## 9. `mlflow_run`

O helper atual registra parâmetros, métricas, tags, artefatos, dataset/split e limitações. Seu modo completo exige assinatura/modelo, refletindo foco em modelo tradicional.

Conclusão MM00: reutilização é obrigatória; uma extensão aditiva para micromodelos sem artefato sklearn pode ser proposta em MM06, mas modificar helper compartilhado é gate humano e exige regressão do contrato atual.

## 10. Sistema de Temas

No baseline:

- V00–V07 aceitas/integradas no Git;
- `ResolvedTheme` permanece fonte visual central;
- V07 adiciona consumidores opt-in para visualizações de display/ML sem alterar cálculo analítico;
- V08 é a próxima camada transversal segundo a documentação da frente visual.

Conclusão: MM00–MM10 não dependem da finalização visual; MM11 reconsulta o estado real e integra apenas por APIs centrais então vigentes.

## 11. Governança externa de Produto de Dados

As regras e skills institucionais vivem fora deste Hub. O framework deve produzir um handoff estruturado e permanecer fracamente acoplado aos nomes/versões reais das skills externas.

No repositório versionado, usar placeholders para nomes de catálogos, schemas, grupos e handles corporativos. A confirmação de nomes/versões acontece no workspace de trabalho durante homologação.

## 12. Ambiente Free versus trabalho

- Free valida estrutura, código compatível e fluxos com fixtures sintéticas.
- O ambiente de trabalho valida permissões, Unity Catalog real, dados reais e integrações institucionais.
- Evidência do Free não será promovida a homologação corporativa por inferência.

## 13. Lacunas reais a preencher

Não existem hoje no repositório:

- contrato canônico de micromodelo;
- máquina de estados do domínio;
- fingerprint semântico;
- coletor metadata-only específico do catálogo configurado;
- skill de micromodelos;
- prompts de criação/descoberta de micromodelos;
- notebook/README de domínio;
- contrato de tracking para micromodelos rule-based;
- handoff estruturado para governança externa;
- catálogo derivado de micromodelos;
- skill de migração de legados.

Essas lacunas são o backlog MM01–MM13; não autorizam criação antecipada na MM00.
