# V09 — Sistema de Temas no kit de instalação/transição

> **Estado atual:** candidata em execução na branch `codex/temas-v09-kit-transicao-20260914`, criada a partir da `main` `55f7006c47d90ae7f760992d252b658f53a59636`. Sem aceite, merge ou publicação Databricks.

## Objetivo

Integrar explicitamente o Sistema de Temas ao kit offline de transição para o Databricks do trabalho. A V09 não cria tema, não muda paleta, não altera o comportamento visual default e não publica nada no workspace.

## Lacuna encontrada na base V08

O bundle já transportava toda a árvore sanitizada e, portanto, levava os arquivos de tema por consequência. Porém:

- o manifesto v2 não declarava quais peças do Sistema de Temas eram obrigatórias;
- a geração do kit não falhava especificamente se schema, tokens ou runtime temático desaparecessem do inventário;
- o checklist de transição não orientava o usuário não técnico a conferir esse contrato;
- transporte do tema podia ser confundido com ativação/publicação se o limite não fosse explicitado.

## Solução V09

A candidata adiciona `tools/temas_v09_transicao.py`, que mantém um conjunto mínimo canônico para transporte:

- schema `theme.schema.json`;
- dicionário `TOKENS.md`;
- registro `assets.json`;
- README e guia operacional de identidade visual;
- núcleo `hub_snippets.visual.tema`;
- adaptador `hub_snippets.visual.theme_plotly`.

`tools/bundle_implantacao.py` chama essa guarda **antes** de escrever o ZIP. Se qualquer caminho obrigatório estiver ausente, a geração falha. Quando o inventário é válido, o `MANIFEST.json` recebe `theme_contract` com:

- `contract_version = 1`;
- `transport = required_and_hashed`;
- `activation = manual_opt_in`;
- `publication = not_performed`;
- lista exata de `required_paths`.

O schema geral do manifesto permanece **v2**, preservando compatibilidade com o notebook de aceite já existente.

## O que permanece inalterado

- todos os FILEs continuam protegidos pelos hashes já usados pelo kit;
- notebooks continuam com a mesma limitação de representação documentada;
- APIs legadas e rotas `_resolvido` não mudam;
- nenhum tema é registrado globalmente apenas por instalar o pacote;
- `theme_lab`, promoção de variante e publicação continuam processos distintos;
- o kit continua offline e sem credenciais Databricks.

## Critérios de aceite da candidata

1. remover qualquer caminho obrigatório faz a guarda V09 falhar;
2. o produto sanitizado real contém todos os caminhos do contrato;
3. bundle escreve `theme_contract` antes da criação do ZIP;
4. manifesto continua v2;
5. checklist explica `manual_opt_in` e `not_performed` para usuário não técnico;
6. workflow V09 permanente é read-only;
7. regressões do kit, V01–V09, V00 e validador permanecem verdes;
8. o próprio kit é gerado offline no CI a partir do commit limpo;
9. nenhuma operação Databricks é executada pela sprint.

## Limites

PASS na V09 comprova transporte e integridade do contrato mínimo no artefato gerado. Não comprova render no browser, acessibilidade, permissões corporativas, publicação, UAT humano ou que uma variante temática foi promovida no workspace.

A V10 não foi iniciada.
