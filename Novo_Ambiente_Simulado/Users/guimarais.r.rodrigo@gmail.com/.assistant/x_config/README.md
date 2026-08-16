# `x_config` — configuração customizada/legada

> **Não auto-descoberto pelo Genie Code.**

## MCP está fora do escopo deste ecossistema

Este projeto não usa nem pretende usar conexões MCP — nem no laboratório, nem no
workspace do trabalho. Se você procurava configuração de integração externa, não
há nada aqui para ajustar.

O único arquivo de configuração desta pasta, `mcp_servers.legacy.json`, veio do ambiente anterior
e **contém apenas uma lista vazia**. Ele não configura coisa alguma: nem porque
está vazio, nem porque o Genie Code configura integrações pela página de
Settings, e não por arquivo no workspace. Está preservado somente como rastro da
exportação original.

Se em algum momento o assunto voltar — por decisão da squad, por exemplo —, o
caminho é a página **Settings** do Genie Code, com o menor privilégio que
atender ao caso, e nunca este diretório.

## Um arquivo parecido que a plataforma cria sozinha

Não confunda `x_config/mcp_servers.legacy.json` com `.assistant/.mcp_servers.json`,
um nível acima. Observado em 2026-08-15: **abrir o painel de MCP em Genie Code →
Settings faz a própria plataforma escrever** `.assistant/.mcp_servers.json`, com
a lista de conectores internos disponíveis. Ele não vem deste repositório e não
deve ser apagado nem versionado — `tools/publicar_free.py --verify` o reconhece e
o separa dos arquivos obsoletos, em vez de mandar removê-lo.

A distinção que importa: a plataforma **materializa** esse arquivo a partir do
que você configurou em Settings. Ela não o lê como entrada — escrever um à mão
não configura integração nenhuma.

## O que nunca guardar aqui

Token, senha, string de conexão com credencial embutida ou qualquer segredo.
Esta pasta é versionada em Git, e segredo em Git permanece no histórico mesmo
depois de removido do arquivo. Credenciais pertencem ao gerenciador de segredos
do workspace.
