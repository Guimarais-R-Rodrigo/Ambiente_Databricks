# Instalação e aceite do Concierge integrado

## Estado e próxima ação

A versão de manutenção é `ambiente_fonte/.assistant/skills/hub-ml-concierge/`.
A integração em Git foi autorizada em 12/09/2026. A cópia em
`novas_funcionalidades/` é histórica; não a instale em paralelo. Não houve
publicação no Free, no trabalho ou em escopo compartilhado nesta integração.

Para conferir o pacote localmente, siga [Testes](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/../tests/README.md).
Para revisar o procedimento, leia [SKILL.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/../SKILL.md). A interface e as
condições oficiais estão em [Fontes](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/fontes.md).

## Revisão sem instalação

Fornecer SKILL.md e seus recursos como contexto permite ensaiar o procedimento.
Isso não comprova seleção nativa por relevância nem por menção. Resultados de
simulação devem ser separados dos forward tests observados no Genie Code.

## Instalação pessoal de teste — ação futura autorizada separadamente

Use o fluxo de publicação do repositório, com validação da fonte e conferência
do espelho gerado. Não execute publicação no trabalho a partir deste guia.
A alternativa manual abaixo é somente para teste pessoal controlado:

1. Confirme ambiente, escopo e permissão. Use documentação autorizada e dados
   sintéticos. Preserve versões existentes antes de qualquer substituição.
2. Em Genie Code, use Settings -> Open skills folder quando disponível. O local
   pessoal documentado é `/Users/<username>/.assistant/skills/`; o compartilhado
   é `Workspace/.assistant/skills/`. Não transforme esses endereços em paths
   Python mecanicamente.
3. Copie somente a pasta canônica `hub-ml-concierge/`, preservando os caminhos
   relativos. SKILL.md, references e templates precisam estar disponíveis;
   mantenha o pacote completo para que documentação e testes continuem acessíveis.
4. Confirme também a instalação do Manual e dos componentes do Hub acessíveis ao
   assistente. Uma skill instalada sem arquivos/ferramentas de leitura não conhece
   o repositório por si. Não use o pacote histórico como fonte de helpers.
5. Abra chat novo, teste `@hub-ml-concierge` e depois os casos sem menção. Se a
   interface mantiver metadados antigos, atualize a página e abra novo chat.
6. Registre carregamento observado separadamente da resposta. O nome impresso
   pela IA não comprova ativação. Sem evidência, use NÃO VERIFICADO.

Não é necessário instalar bibliotecas analíticas para executar o procedimento
textual. O acesso de leitura depende das capacidades do assistente e das ACLs.

## Aceite e compartilhamento

O roteiro geral do repositório recebeu os casos 14P, 14N e 14M. A matriz detalhada
em `tests/casos_aceite.json` contém cenários de descoberta, colisão, versão e
segurança; expectativas continuam PENDENTE até execução registrada separadamente.
Reexecute os negativos das skills vizinhas e os testes afetados pelas instruções.
Os resultados antigos de outras skills não homologam o conjunto ampliado.

Antes de compartilhar com a squad, cumpra revisão independente e gates do
repositório. Produção, publicação compartilhada e dados reais continuam sujeitos
à autorização e à avaliação no ambiente de destino.

## Manutenção e rollback

Edite a fonte canônica. Atualizações do inventário pertencem ao Manual; sincronize
sua cópia da raiz quando ele mudar. Valide e regenere o simulado pelo renderer,
nunca editando a árvore derivada à mão. Registre mudanças no changelog canônico.

Para retirar um teste pessoal, remova/desative somente a instalação do Concierge
previamente identificada, com backup, e abra novo chat. Não remova outras skills.
No Git, reverta a integração em commit próprio e ajuste seus consumidores; apagar
um arquivo no Git não o retira automaticamente do workspace.
