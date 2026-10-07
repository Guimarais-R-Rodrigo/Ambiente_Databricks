# V09 — Sistema de Temas no kit de instalação/transição

> **Nota administrativa — 06/10/2026.** Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência. Para transporte vigente, consulte o [kit de transição](../../../../tools/README.md#pacotes-de-auditoria-e-implantação).

## Registro histórico preservado

> **Estado atual:** **ACEITA E INTEGRADA NO GIT; SEM PUBLICAÇÃO DATABRICKS.** Rodrigo deu aceite explícito em 14/09/2026. A entrega funcional foi integrada pelo PR #45 e o defeito real encontrado no primeiro pós-merge foi corrigido pelo PR #46. O head técnico final validado na `main` é `4ae714a35a0aafd930a8cd796d962b0a79449b88`.

## Objetivo

Integrar explicitamente o Sistema de Temas ao kit offline de transição para o ambiente de trabalho. A V09 não cria tema, não muda paleta, não altera o comportamento visual default e não publica nada no workspace Databricks.

Para quem nunca entrou no Hub, a distinção operacional é simples:

- **transportar**: o kit precisa levar as peças mínimas do Sistema de Temas e provar sua integridade;
- **instalar**: continua sendo uma ação separada no ambiente de destino;
- **ativar**: continua manual e opt-in;
- **promover**: continua um processo separado;
- **publicar**: não é realizado pela V09.

## Lacuna encontrada na base V08

O bundle já transportava toda a árvore sanitizada e, portanto, levava os arquivos de tema por consequência. Porém:

- o manifesto v2 não declarava quais peças do Sistema de Temas eram obrigatórias;
- a geração do kit não falhava especificamente se schema, tokens ou runtime temático desaparecessem do inventário;
- o checklist de transição não orientava o usuário não técnico a conferir esse contrato;
- transporte do tema podia ser confundido com ativação/publicação se o limite não fosse explicitado.

## Solução V09 integrada

`tools/temas_v09_transicao.py` mantém o contrato canônico de transporte com nove caminhos obrigatórios:

1. `.assistant/hub_padroes/identidade_visual/theme.schema.json`;
2. `.assistant/hub_padroes/identidade_visual/TOKENS.md`;
3. `.assistant/hub_padroes/identidade_visual/assets.json`;
4. `.assistant/hub_padroes/identidade_visual/README.md`;
5. `.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md`;
6. `.assistant/hub_snippets/visual/tema/__init__.py`;
7. `.assistant/hub_snippets/visual/tema/tema.py`;
8. `.assistant/hub_snippets/visual/theme_plotly/__init__.py`;
9. `.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

`tools/bundle_implantacao.py` chama essa guarda **antes** de escrever o ZIP. Se qualquer caminho obrigatório estiver ausente, a geração falha. Quando o inventário é válido, o `MANIFEST.json` recebe `theme_contract` com:

- `contract_version = 1`;
- `transport = required_and_hashed`;
- `activation = manual_opt_in`;
- `publication = not_performed`;
- lista exata de `required_paths`.

O schema geral do manifesto permanece **v2**, preservando compatibilidade com o notebook de aceite já existente.

O mesmo módulo reabre o `01_IMPORTAR_HUB_<commit>.zip` depois do build, lê o `MANIFEST.json`, exige o contrato exato, confirma que cada caminho obrigatório aparece uma única vez e compara tamanho e SHA256 dos bytes realmente armazenados no ZIP com o inventário. Tanto o workflow V09 quanto o workflow operacional do kit executam esse gate depois da geração; no workflow operacional, a conferência ocorre **antes** de `upload-artifact`.

## Por que o notebook de aceite não ganhou uma segunda implementação do contrato

`tools/aceite_trabalho.py` é embutido literalmente no notebook offline. Fazer esse núcleo importar `tools/temas_v09_transicao.py` criaria uma dependência que não existe no workspace de destino; copiar a mesma lista de caminhos para dentro dele criaria duas fontes de verdade.

A V09 mantém a divisão de responsabilidade:

1. **origem/build:** guarda canônica exige o contrato antes de gerar o bundle;
2. **artefato:** o ZIP final é reaberto e os nove arquivos são conferidos contra o próprio manifesto antes de distribuição;
3. **destino:** o notebook genérico continua verificando a identidade fixa do manifesto e SHA256 de todos os FILEs, enquanto o checklist instrui a pessoa a conferir o bloco `theme_contract` no staging.

Assim, o contrato específico de temas permanece em um único módulo de manutenção, sem enfraquecer a verificação já existente no destino.

## Integração funcional — PR #45

A candidata aceita tinha head `3b69dd25fd4af434fda414496c2ca3d80fd78a8e`. O PR #45 foi integrado por merge commit em 14/09/2026, produzindo `0f7234c4734f1974ebb1a20123f3c26626c67ef3` na `main`.

A árvore do merge e a árvore da candidata validada eram idênticas (`26689420a2c0693c0ff0c08f625e80babb2180a8`), portanto o merge não introduziu alteração inesperada de bytes.

No primeiro pós-merge, 12 workflows de `push` foram realmente disparados. Onze terminaram em `success`, mas o workflow operacional `Kit de transição para o trabalho`, run `34880619346`, terminou em **FAILURE** antes dos testes Spark, da geração do kit e do upload do artefato.

A causa não foi um defeito do contrato temático. O runner desse workflow não instalava previamente as dependências Node já exigidas pelo compositor editorial V06 antes de executar `python tools/ci_local.py --verbose`. O gate falhou corretamente e as etapas seguintes ficaram `skipped`. Esse run permanece registrado como **FAILURE** histórico.

## Correção pós-merge — PR #46

O defeito de preparação do runner foi corrigido em escopo mínimo pelo PR #46:

- configuração explícita de Node 22;
- instalação de `pnpm@10.34.5`;
- `pnpm --dir tools/readme_visuals install --frozen-lockfile` antes do `ci_local.py`;
- novo teste de regressão que exige essa preparação e sua ordem antes do gate local.

Nenhum gate foi removido ou relaxado. A correção não alterou `.assistant`, `Novo_Ambiente_Simulado`, schema, tokens, paleta, runtime do produto, cálculos ou lógica analítica.

O PR #46 teve head `d1c67f06d96b929a58961c50fc31c06ca7c0cfe2`, com cinco checks de PR em `success`, e foi integrado por merge commit `4ae714a35a0aafd930a8cd796d962b0a79449b88`. A árvore do merge e a árvore da candidata corretiva eram idênticas (`32de1224093407d6fc91e08842c6f5ef3d0f456a`).

## Evidência pós-merge final

No SHA técnico final `4ae714a35a0aafd930a8cd796d962b0a79449b88`, os **12/12 workflows realmente disparados por `push` concluíram com `success`**. O inventário nominal e os run IDs estão no `CHECKPOINT_V09.md`.

Em especial, o workflow operacional `Kit de transição para o trabalho`, run `34881426374`, comprovou na ordem correta:

- preparação Python, Java e Node no runner;
- instalação das dependências do compositor V06;
- `ci_local.py` aprovado;
- suíte V09 **12/12 PASS**;
- `tools/tests/test_transicao_trabalho.py --spark -v`: **43/43 PASS com Spark local**;
- geração do kit offline: **535 arquivos + `MANIFEST.json`**;
- `theme_contract` v1: **9/9 caminhos obrigatórios presentes e com SHA256 válido dentro do ZIP**;
- `activation = manual_opt_in`;
- `publication = not_performed`;
- verificação do ZIP concluída **antes** de `upload-artifact`;
- upload apenas do artefato do GitHub Actions, sem publicação Databricks.

No mesmo head, o CI local mediu **1355 arquivos**, **1850 links fora da raiz** e o validador terminou **APROVADO: 0 falha(s), 0 aviso(s)**.

## O que permanece inalterado

- todos os FILEs continuam protegidos pelos hashes já usados pelo kit;
- notebooks continuam com a mesma limitação de representação documentada;
- APIs legadas e rotas `_resolvido` não mudam;
- nenhum tema é registrado globalmente apenas por instalar o pacote;
- `theme_lab`, promoção de variante e publicação continuam processos distintos;
- o kit continua offline e sem credenciais Databricks;
- nenhuma alteração foi feita em `ambiente_databricks/.assistant` ou `Novo_Ambiente_Simulado` pela entrega funcional V09;
- nenhuma mudança foi feita em dados, métricas, amostragem, denominadores, thresholds, embeddings ou lógica analítica.

## Critérios de aceite — resultado final

1. remover qualquer caminho obrigatório faz a guarda V09 falhar — **PASS**;
2. o produto sanitizado real contém todos os caminhos do contrato — **PASS**;
3. bundle escreve `theme_contract` e valida a guarda antes da criação do ZIP — **PASS**;
4. manifesto continua v2 — **PASS**;
5. ZIP gerado é reaberto e os nove caminhos são validados por presença única, tamanho e SHA256 — **PASS**;
6. checklist explica `manual_opt_in` e `not_performed` para usuário não técnico — **PASS**;
7. workflows V09 e do kit permanecem read-only; no workflow do kit, verificação precede upload — **PASS**;
8. regressões do kit, V01–V09, V00 e validador permanecem verdes no fechamento — **PASS**;
9. o próprio kit é gerado offline no CI a partir do commit limpo — **PASS**;
10. nenhuma operação Databricks é executada pela sprint — **PASS**.

## Limites do fechamento

PASS na V09 comprova transporte e integridade do contrato mínimo no artefato gerado e os gates locais/CI documentados. Não comprova render no browser Databricks, acessibilidade, permissões/ACL corporativas, publicação, UAT humano ou promoção de uma variante temática no workspace.

**Nenhuma publicação Databricks foi realizada. A V10 não foi iniciada por este fechamento.**
