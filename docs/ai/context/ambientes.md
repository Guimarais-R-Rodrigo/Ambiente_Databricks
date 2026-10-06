# Ambientes e limites de evidência

Leia antes de usar Free/trabalho ou interpretar testes. Regra durável é contrato
do projeto; observação datada é evidência do ambiente identificado; configuração
atual precisa confirmação. Nenhuma frase aqui prova acesso a esta máquina.

## Regras duraveis

| Assunto | Regra durável | Observação de origem | Confirmação exigida | Owner |
|---|---|---|---|---|
| Dados Free | somente fixtures sintéticas, sem dado/tabela/path/identificador corporativo | laboratório pessoal descrito nos controles de 2026 | inspecionar entradas e saídas sanitizadas antes de cada operação | AGENTS e `tools/project_policy.py` |
| Dados trabalho | reais apenas no destino autorizado, sob UC, PII e compliance corporativos | Azure Databricks/Genie habilitado era o contexto relatado | conferir política, ACL, catálogo e escopo do destino | governança corporativa e runbook |
| Acesso Free | resolver identidade/host/profile em runtime; não persistir username ou credenciais | CLI instalada/autenticada na máquina da sessão antiga | sondar instalação, versão e identidade atuais sem expor segredo | operador da sessão e skill publicar-free |
| Replicação | caminho aprovado é manual; não presumir CLI ou acesso corporativo | trabalho era outro computador, sem CLI | confirmar operador, destino e canal autorizado; mudança desse caminho exige decisão própria | [runbook](../../playbooks/replicacao-trabalho.md) |
| Compute | recursos dependem de edição, versão, quotas e política | Spark serverless e bibliotecas variaram em agosto/setembro | medir capacidades necessárias antes de executar | fonte oficial e probe da sessão |
| Publicação | Free usa publicador próprio; trabalho usa kit e runbook | ADR-0005/0008 | conferir manifesto e alvo; execute não é implícito | [fontes/efeitos](../rules/fontes-e-derivados.md#publicacao) |
| Evidência | Free pode exercitar estrutura, descoberta/@, Spark e forward tests; não certifica trabalho | resultados antigos estão em [histórico](observacoes-2026.md) | runtime real, ACL, UC e políticas corporativas exigem gates no trabalho | runbook e owner da homologação |

O laboratório ajuda a calibrar descriptions com casos positivo/negativo/@ em
chat novo. Uma descrição alterada invalida a prova afetada de roteamento. O
passado não autoriza editar description do produto numa migração apenas editorial.

## Confirmacao

1. Registre data UTC, SHA/pacote, ambiente, versão/runtime e pré-condições reais.
   Falta de acesso ou dependência é BLOCKED, não impossibilidade da plataforma.
2. Antes de uma tarefa conversacional, teste a disponibilidade/orçamento do Genie
   em chat novo. Cota antiga vencida não significa bloqueio atual nem PASS.
   Se houver bloqueio, meça separadamente chat, compute e workspace; não estenda
   automaticamente o resultado de um aos demais.
3. Confirme bibliotecas e política de instalação. Pins, tempo de instalação,
   `cache`/`persist`, `spark.conf`, Spark Connect, `pyspark.ml`, `spark` em módulo,
   MLflow e dependências de pandas têm observações em [histórico](observacoes-2026.md#runtime-free).
   São pontos de probe, não recomendações executáveis atuais. Helpers que usam
   cache devem degradar em ambiente incompatível; confira o código atual.
4. Antes de replicar, reexecute os casos relevantes no ambiente autorizado. A
   diferença MLflow/Prophet registrada em 2026 mostra por que a prova tem data.
5. Toda nova diferença Free/trabalho ganha nota datada nesta matriz ou em
   observações vinculadas, com fonte, versão e resultado; impacto relevante em
   uso/compatibilidade entra como marco no changelog. Preserve a
   observação anterior; não a reescreva para fingir uma plataforma estável.

Os limites oficiais atuais do Free estão na [referência](../references/databricks-genie-code.md#limites-revalidados).
Não conservar as antigas frases “sem jobs permanentes” ou “sem serving” como
negações universais: a documentação consultada descreve recursos com limites.

## Destinos

Paths são placeholders, não autorização para escrever:

- pessoal: `/Users/<username-trabalho>/.assistant_instructions.md` e
  `/Users/<username-trabalho>/.assistant/skills/`;
- squad: `Workspace/.assistant/skills/`, com revisão/admin e governança próprias;
- username real do trabalho, backups e erros brutos ficam no ambiente autorizado.

Não fazer busca/substituição improvisada. Use o runbook e o manifesto físico do
kit, preserve MCP e conteúdo alheio, faça backup/staging e instruções por último.
MLflow e consultas UC começam desativados; ativação tem escopo próprio. Aceite
local do kit não certifica o destino; nova sessão Python/chat e gates humanos
continuam necessários após promoção.
