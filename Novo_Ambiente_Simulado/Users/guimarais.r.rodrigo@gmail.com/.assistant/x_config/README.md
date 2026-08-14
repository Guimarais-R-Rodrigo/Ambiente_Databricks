# `x_config` — configuração customizada/legada

> **Não auto-descoberto pela Genie Code.**

## O que é MCP, antes de tudo

MCP (*Model Context Protocol*) é um padrão que permite a um assistente conversar
com ferramentas externas — um banco de dados, um sistema de tickets, uma API
interna. Sem MCP, o assistente só enxerga o que está no chat; com MCP, ele
consegue consultar essas fontes durante a conversa.

Em várias ferramentas de IA, esse tipo de conexão se declara em um arquivo JSON
guardado junto do projeto. É exatamente daí que vem o arquivo desta pasta: ele
foi herdado do ambiente anterior, montado seguindo essa convenção de outras
ferramentas.

## Por que este arquivo não faz nada

A Genie Code não configura MCP por arquivo no workspace. `mcp_servers.legacy.json`
tem JSON sintaticamente válido e, ainda assim, **não ativa servidor nenhum** —
ninguém o lê. Ele permanece aqui apenas como rastro da exportação original, para
quem precisar comparar o ambiente antigo com o atual.

Ter um arquivo de configuração que não configura nada é confuso o bastante para
merecer aviso: se você mudar o conteúdo dele esperando efeito, não haverá
nenhum, e nenhuma mensagem de erro vai indicar o motivo.

## Como configurar MCP de verdade

1. Abra a Genie Code no workspace e vá em **Settings**.
2. Localize a seção de integrações/MCP e cadastre o servidor por lá.
3. Conceda o menor privilégio que atenda ao caso; conexões de leitura bastam
   para a maioria dos usos analíticos.

Confirme na documentação oficial vigente antes de cadastrar, porque a tela e os
tipos de servidor suportados mudam entre versões.

## O que nunca guardar aqui

Token, senha, string de conexão com credencial embutida ou qualquer segredo.
Esta pasta é versionada em Git, e segredo em Git permanece no histórico mesmo
depois de removido do arquivo. Credenciais pertencem ao gerenciador de segredos
do workspace.
