# V10 — Databricks App de gestão visual

> **Nota administrativa — 06/10/2026.** Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência. Para uso do App, consulte o [guia distribuído](../../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md).

## Registro histórico preservado

## Estado

**ACEITA E INTEGRADA NO GIT; SEM DEPLOY DATABRICKS.**

Base de início: `d6655411ca4ac1834b0983f6ce6bdadc30b831bb`, fechamento documental da V09.

Após a integração e o fechamento documental da MM00 na `main`, a candidata V10 foi reconciliada no head `cb942ee955ff9236f19099e5ed4ceee9beb32000`. Rodrigo deu aceite explícito em 14/09/2026 e o PR #48 foi integrado no merge `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`.

## Escopo recuperado do plano

O plano V00–V14 posiciona a V10 como **Databricks App de gestão visual** e a V11 como superfície AI/BI. O App reutiliza núcleo, contratos, adaptadores e fixtures já existentes; identidade, papéis, persistência, retenção, custos e publicação permanecem explicitamente definidos. A documentação de App e AI/BI continua separada.

A política V01 continua sendo a fonte canônica dos cinco papéis e transições. A V10 não cria outro workflow de aprovação.

## Decisão arquitetural V10

A implementação é aditiva e evita duplicação:

- V02 continua dono de schema, parsing e `ResolvedTheme`;
- V03/V04 continuam donos dos consumidores visuais;
- V05 continua dono de rascunho, preview, comparação, sessão e hashes;
- V10 acrescenta somente a superfície Databricks App, identidade da requisição, isolamento de persistência por usuário e empacotamento implantável;
- V09 continua dono do kit geral de transição do Hub.

O App fica em `hub_padroes/identidade_visual/databricks_app/`, junto ao contrato que governa a identidade visual. O bundle implantável é **derivado** por `tools/temas_v10_app.py`; ele copia as fontes canônicas necessárias para `.artifacts/` sem criar cópias editáveis permanentes.

## Superfície funcional

O App Streamlit permite:

1. abrir um preset de demonstração V05;
2. editar controles já suportados pelo Visual Lab;
3. validar atomicamente a proposta;
4. desfazer/restaurar;
5. comparar base × proposta com dados sintéticos;
6. salvar sessão própria em Unity Catalog Volume;
7. listar e reabrir somente sessões do namespace da identidade atual.

Não existem ações de submeter, aprovar, rejeitar, revogar, promover, ativar ou publicar.

## Identidade

Dentro de Databricks Apps, `X-Forwarded-User` é a identidade operacional recebida do proxy. O valor bruto permanece apenas em memória; o namespace persistente usa SHA-256.

Sem header, a execução de produção falha. O fallback local exige simultaneamente:

```text
HUB_THEME_LOCAL_DEV=true
HUB_THEME_LOCAL_USER_ID=<identidade sintética>
```

Esse fallback não é permitido como substituto de autenticação no workspace.

## Papéis

A [matriz V10](MATRIZ_PAPEIS.json) reaproveita exatamente os papéis V01:

- leitor;
- proponente;
- aprovador;
- publicador;
- mantenedor.

A instância `authoring_only` tem como público-alvo grupos reais mapeados pelo proprietário do ambiente para proponente/mantenedor. O código não consulta grupo corporativo nem oferece seletor de papel. Atribuição de papel permanece externa e confiável; ausência de mapeamento não vira autopromoção.

## Persistência real projetada

O `app.yaml` exige o recurso de App `theme_storage` e o injeta em `HUB_THEME_VOLUME` com `valueFrom`. Databricks resolve esse recurso para o caminho `/Volumes/...` do Unity Catalog Volume.

Em produção, qualquer caminho fora de `/Volumes/` é recusado. O App cria somente subdiretórios sob:

```text
<volume>/hub-theme-manager-v10/sessions/<sha256-identidade>/
```

O conteúdo de cada sessão é gravado e verificado pelas funções V05 já integradas.

## Retenção

V10 define política explícita **sem exclusão automática**, **sem botão de delete** e **sem reescrita de histórico**. Retenção corporativa futura deve ser estabelecida administrativamente no destino; esta sprint não inventa prazo corporativo.

## Custos

O desenho padrão consome somente Databricks Apps + armazenamento de UC Volume. Não adiciona SQL warehouse, Lakebase, Model Serving, Jobs, Genie ou LLM. Custos monetários dependem do contrato/cloud/workspace e não são estimados pelo projeto sem fonte do ambiente.

## Bundle implantável

`tools/temas_v10_app.py` cria uma pasta autocontida derivada contendo:

- arquivos do App;
- `hub_snippets` canônico;
- `hub_padroes/identidade_visual` canônico, sem duplicar o próprio diretório do App;
- `V10_APP_MANIFEST.json` com hashes e metadados do commit.

O builder recusa destino existente, symlinks, `app.yaml` sem o recurso esperado ou declaração de publicação.

## Critérios de aceite Git atendidos

A integração V10 demonstrou:

1. fonte e simulado equivalentes para os arquivos de produto V10;
2. importação/compilação do App sem alterar o contrato anterior;
3. identidade ausente recusada;
4. fallback local somente com opt-in explícito;
5. produção recusando storage fora de Unity Catalog Volume;
6. duas identidades isoladas em namespaces diferentes;
7. save/list/reopen preservando contrato de sessão V05;
8. adulteração de sessão recusada;
9. nenhuma função de delete/aprovação/publicação;
10. `app.yaml` usando recurso `theme_storage` sem segredo ou ID corporativo hardcoded;
11. bundle derivado criado e revalidado por hashes;
12. regressões V01–V10 e V00 verdes;
13. validador estrutural/documental verde;
14. documentação de primeiro uso e deploy/rollback suficiente para operador não técnico/técnico respectivamente;
15. nenhuma chamada, criação ou deploy Databricks executado pela CI/implementação Git.

## Evidência de integração Git

- push final original `34887162337`: **SUCCESS**;
- head reconciliado aceito `cb942ee955ff9236f19099e5ed4ceee9beb32000`: dez workflows reais de PR em **success**;
- PR #48: integrado em `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`;
- pós-merge: **12/12 workflows de `push` em success**, incluindo V10 `34896944061`;
- failures históricos permanecem preservados em `TESTES.md` e não foram reclassificados.

## O que PASS não prova

Mesmo com CI verde, permanecem fora da prova local:

- criação real do Databricks App;
- headers reais no workspace;
- permissões/grupos corporativos;
- acesso real ao Unity Catalog Volume;
- concorrência multiusuário no serviço real;
- renderização e acessibilidade no navegador;
- custo observado;
- UAT com iniciante;
- deploy/rollback executado;
- publicação ou ativação de tema.

Esses itens não devem ser convertidos em PASS por inferência.

## Fronteira com V11

V11 trata AI/BI. A V10 não implementa tradutor AI/BI, não muda `context="aibi"`, não cria paleta específica para dashboards e não iniciou essa sprint. O fechamento Git da V10 apenas remove o bloqueio sequencial para que V11 possa ser planejada/executada separadamente.