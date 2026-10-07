# Contexto do projeto

## Missao

Laboratório de engenharia do ecossistema `.assistant` do Databricks Genie Code
para trabalho de CRM bancário e modelos de machine learning. O projeto busca
uso profissional e escalável: pessoal, depois squad e missão. Esse contexto do
projeto não é uma preferência global atribuída ao usuário em outros assuntos.

Ciclo: editar no Git → validar → renderizar → publicar no Free para testes →
replicar manualmente no workspace de trabalho. Cada seta tem pré-condições,
autorização e evidência próprias. O [README raiz](../../../README.md) explica
arquitetura e contribuição; [ambientes](ambientes.md) separa o que cada prova vale.

## Convencoes

As convenções técnicas do produto estão em
[ambiente_databricks/.assistant_instructions.md](../../../ambiente_databricks/.assistant_instructions.md):
prosa PT-BR, PySpark/Spark SQL, Plotly, MLflow, serverless quando compatível,
prevenção de leakage obrigatória e números brasileiros na narrativa. Consulte
essa fonte ao editar o produto; uma convenção não autoriza efeito, instalação ou
mudança em configuração. A documentação deve ter exemplos e, quando úteis,
diagramas e tabelas, com a qualidade do README raiz como referência.

## Contratos

- [ADRs 0003–0009](../../decisions/README.md) delimitam quarentena, helpers
  explícitos, publicador próprio Free, identidade `hub_`/`hub-ml-`, forma por objeto
  e pacote mínimo sanitizado com manifesto. A reorganização não os revoga.
- A declaração explícita de helpers continua obrigatória (ADR-0004). A forma e
  localização evoluíram no ADR-0007; o catálogo/glossário unificados têm owner no
  Manual (ADR-0010). Não reintroduzir catálogos ou glossários concorrentes.
- O Concierge (ADR-0011) é entrada opcional de descoberta/composição, solicitada e
  progressiva. Não retira a declaração explícita nem transforma integração Git
  em publicação ou homologação conversacional.
- READMEs por objeto seguem ADR-0012 e contrato 1.0.0. Novos objetos entram já no
  contrato; veja a [regra editorial](../rules/documentacao.md#readme-de-objeto).
- Temas têm contrato central e configuração por contexto (ADR-0013).
  Transporte/kit não ativa tema nem comprova browser/runtime, acessibilidade,
  ACL, UAT, promoção visual ou publicação.
- Micromodelos (ADR-0014–0020) são artefatos de domínio: `micromodelo.yaml`
  especifica; MLflow registra runs; governança externa autoriza publicação;
  piloto greenfield precede legados; temas vêm do sistema central; fontes reais
  limitam-se ao catálogo configurado via binding autorizado.
- [ADR-0025](../../decisions/ADR-0025-arquitetura-instrucoes-ia.md) muda somente a
  hierarquia editorial CLAUDE/.claude do ADR-0001. Git canônico, derivação,
  rastreabilidade, dados e decisões do produto permanecem preservados.

A [arquitetura por tarefa e retenção](../../decisions/ADR-0026-arquitetura-projeto-e-historia.md)
separa marcos estratégicos, provas datadas e contexto de tarefa. O protótipo
Concierge permanece [histórico](../../historico/concierge.md); manutenção e uso
seguem a versão canônica do produto.

## Owners vivos

| Assunto | Onde consultar o estado | Como verificar |
|---|---|---|
| Decisões | [Índice ADR](../../decisions/README.md) | decisão e ratificação datadas |
| READMEs de objeto | [Índice da frente](../../sprints/readmes_objetos/README.md) | `tools/validate_assistant.py` e `tools/readme_objeto_contract.py` |
| Temas | [Índice da frente](../../sprints/sistema_temas/README.md) | contratos, gates e evidência da revisão atual |
| Micromodelos | [Índice](../../sprints/micromodelos/README.md), [plano de laboratório](../../sprints/micromodelos/PLANO_EXECUCAO_LAB.md) | SHA/campanha e limites da prova |
| Capacidade executável | [policy.json](../../../ambiente_databricks/.assistant/hub_padroes/skill_enforcement/policy.json) e [SER](../../sprints/skill_enforcement_rollout/README.md) | `current_level` é presente; `target_level` é roadmap |
| Inventário gerido | [project_policy.py](../../../tools/project_policy.py) | nomes atuais e saída efetiva do validador |

Não carregar sprints ou histórico inteiro em toda sessão. Consulte o owner
pertinente quando precisar da afirmação. Os marcos removidos do bootstrap estão
preservados em [observações datadas](observacoes-2026.md#frentes-na-baseline).
