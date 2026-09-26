# Checkpoint V03 — aceite e integração Git

## Estado vigente — 12/09/2026

Rodrigo concedeu aceite explícito à V03 e autorizou sua integração Git com a instrução
“pode integrar a V03”. O aceite cobre o adaptador Plotly opt-in, sua documentação,
os testes e as garantias de compatibilidade desta sprint. Não autoriza publicação no
Databricks, homologação de Spark/widgets/Apps/AI-BI, migração automática de outros
consumidores nem início da V04.

Para quem nunca entrou no Hub: o merge Git da V03 não exige alterar o uso atual.
Quem já chama `aplicar_tema(fig, ...)` continua usando a mesma API e o mesmo
comportamento legado. A nova rota só é usada quando alguém fornece explicitamente
um `ResolvedTheme` de contexto notebook. Não há seletor de temas nem mudança visual
automática nesta sprint.

## Evidência técnica antes da ratificação documental

A candidata técnica aceita era o head `22392e557557f0faf908acb8f4dd2a9d358d785f`,
árvore `9e92a3073dbbc202afa3db817a6d61e1c050440b`. Nesse estado, os cinco workflows
permanentes concluíram com sucesso: CI geral, V00, V01, V02 e V03. A suíte específica
V03 terminou com 26 testes aprovados. O code review manual do Codex concluiu sobre
essa mesma candidata sem novos achados; os cinco threads P2 anteriores estavam
respondidos e resolvidos.

A ratificação documental deste aceite precisa ser revalidada integralmente antes do
merge. O PR #16 é o registro autoritativo do head final, dos checks e da efetivação
do merge. A presença deste documento em uma branch não prova que a integração ocorreu.

## Garantias preservadas

1. nenhuma chamada legada muda de assinatura;
2. `legado_notebook` mapeia exatamente para `get_tema_eda()`;
3. a nova aplicação é explícita por figura e não altera `pio.templates.default`;
4. registro configurado usa namespace `hub-*` e só ativa globalmente com `ativar=True`;
5. substituir um template já ativo sem `ativar=True` falha antes de trocar o objeto,
   inclusive quando o nome participa de um default composto;
6. dados, eixos e cores explícitas dos traces permanecem intactos;
7. temas não-notebook, modos ainda não suportados e resultados V02 adulterados falham
   sem fallback silencioso;
8. nenhum consumidor existente é migrado implicitamente.

## Limites e gates ainda pendentes

Auditoria independente: PENDENTE. Avaliação com usuário iniciante: PENDENTE.
Homologação visual real no Databricks, Spark, widgets, Apps e AI/BI: NÃO REALIZADA.
Testes Python e GitHub Actions não substituem esses gates. Não houve publicação nem
acesso a dados corporativos.

## Recuperação

Se a integração precisar ser desfeita após o merge, preparar uma reversão em branch
própria, preservando mudanças posteriores e repetindo os gates. Não resetar a `main`,
não fazer force-push e não publicar um pacote antigo no Databricks para desfazer uma
mudança exclusivamente de repositório.

## Próxima etapa

Após a integração e a conferência pós-merge, a próxima sprint planejada é V04. O
aceite da V03 não inicia a V04 automaticamente.
