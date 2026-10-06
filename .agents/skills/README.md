# Skills de manutenção do repositório

Estas cinco skills orientam quem mantém o Git. A fonte editorial é
`.agents/skills/`; cópias de descoberta por cliente são adaptadores, não outra
política. Este catálogo é um índice, não uma sexta skill invocável.

## Famílias e limites

| Família | Fonte | Uso | Vai ao Databricks? |
|---|---|---|---|
| Mantenedor | este catálogo e suas cinco pastas | validar, renderizar, preparar publicação e gates | não |
| Produto | [catálogo do produto](../../ambiente_fonte/.assistant/skills/README.md) | skills `hub-ml-*` usadas no Genie Code | sim |
| Exemplar | [exemplo de skill](../../ambiente_fonte/.assistant/hub_padroes/skill/exemplo/SKILL.md) | material didático não roteável, fora do inventário de skills reais | transportado como exemplo |

Carregar uma skill não executa comandos nem concede autorização. O cliente,
versão, modo e configuração determinam a descoberta; uma cópia presente não
prova que a skill foi carregada. Os casos abaixo documentam comportamento
esperado, não testes reais de todos os clientes.

## Rotas disponíveis

| Intenção | Skill | Saída esperada |
|---|---|---|
| validar fonte e interpretar falhas locais | [validar-assistant](validar-assistant/SKILL.md) | comando, contadores, código de retorno e limites |
| conferir ou regenerar o espelho | [render-simulado](render-simulado/SKILL.md) | plano local; escrita somente após preflight e autorização |
| publicar ou conferir o laboratório Free | [publicar-free](publicar-free/SKILL.md) | fases e destino explícitos; inventário/tipos e conteúdo separados |
| testar seleção de skills no Genie | [forward-test-skills](forward-test-skills/SKILL.md) | casos positivos, negativos e menção com evidência observada |
| preparar ou conduzir cópia pessoal ao trabalho | [replicar-trabalho](replicar-trabalho/SKILL.md) | kit, runbook e gates humanos por destino |

`revisar-docs-oficiais` permanece **proposta, sem pasta e sem SKILL.md**.
Não é invocável. Documentar fontes oficiais ou revisá-las não cria uma sexta
skill. Um pedido de EDA/modelagem em dados é uma intenção de produto, não de
manutenção; siga o catálogo do produto.

## Usar ou alterar uma skill

1. Leia o [contrato do repositório](../../AGENTS.md), a skill pertinente e os
   owners que ela aponta. Execute comandos da raiz do checkout completo.
2. Edite somente `.agents/skills/<nome>/SKILL.md` e recursos locais necessários.
   Integre adaptadores pelo mecanismo de geração aprovado, sem edição paralela.
3. Use `name` igual ao nome da pasta e `description` com gatilho e exclusões.
   O frontmatter portátil contém apenas `name` e `description`. Campos de
   ferramentas, hooks, modelo ou permissões de um fornecedor não são controles
   de segurança portáveis e não entram na fonte comum.
4. Mantenha automação nos [owners em tools/](../../tools/README.md). A skill
   orquestra ferramentas; não duplica sua implementação ou contagens mutáveis.
5. Confira links com a caixa exata, recursos, flags e efeitos; teste intenção
   positiva, negativa e pré-requisito ausente de cada skill. Exercite bloqueios
   sem publicar, replicar ou excluir conteúdo real para provar a migração.
6. Registre a evidência no owner da tarefa; use o [critério de marcos](../../docs/ai/templates/changelog-entry.md)
   para o [CHANGELOG](../../CHANGELOG.md). Falha de
   ambiente ou etapa não executada não é PASS. Rollback restaura fonte, catálogo
   e adaptadores como conjunto coerente, preservando mudanças alheias.

Certificação de enforcement segue o [procedimento próprio](../../tools/skill_enforcement/README.md).
Validação estática, teste de descoberta do mantenedor, roteamento Genie,
publicação e homologação de runtime são gates distintos.

[Voltar ao README raiz](../../README.md)
