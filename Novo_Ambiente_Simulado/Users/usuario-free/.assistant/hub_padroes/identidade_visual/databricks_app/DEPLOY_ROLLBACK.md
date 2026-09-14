# Deploy e rollback — Databricks App de Gestão Visual V10

> Este procedimento **não autoriza deploy**. Use somente depois de autorização explícita no ambiente de destino. O GitHub Actions da V10 nunca cria, atualiza ou publica Databricks Apps.

## Público

Mantenedor/publicador técnico autorizado a criar ou atualizar Databricks Apps e a configurar recursos e permissões. Usuário final não precisa executar estas etapas.

## Pré-requisitos verificáveis

- V10 integrada no Git em commit identificado e com CI verde;
- Databricks Apps habilitado no workspace;
- Unity Catalog Volume já existente para sessões;
- pessoa executora com permissão para gerenciar o App e associar o Volume;
- grupos reais de proponentes/mantenedores definidos pelo proprietário do ambiente;
- backup/conferência das sessões existentes quando houver atualização de App;
- nenhum segredo, PAT ou caminho corporativo gravado no repositório.

## 1. Gerar a fonte implantável

Em checkout limpo do commit aprovado:

```powershell
python -B tools/temas_v10_app.py --output .artifacts/v10-app
```

O comando cria uma pasta nova e falha se o destino já existir. O bundle contém os arquivos do App, `hub_snippets`, o contrato de identidade visual necessário e `V10_APP_MANIFEST.json` com SHA-256. Ele não executa Databricks CLI e não faz upload.

Execute em seguida:

```powershell
python -B tools/temas_v10_app.py --verify .artifacts/v10-app
```

Somente continue se a verificação terminar em `OK`.

## 2. Criar/configurar o App no workspace autorizado

Na interface Databricks Apps:

1. crie ou selecione o App destinado à gestão visual;
2. em **App resources**, adicione o Unity Catalog Volume de sessões;
3. use a resource key exatamente `theme_storage`;
4. conceda leitura e gravação ao service principal do App, porque a V10 persiste sessões;
5. restrinja **CAN USE** aos grupos que o proprietário do ambiente mapeou para autoria/manutenção;
6. não adicione SQL warehouse, Model Serving, Lakebase, Job, Genie ou segredo se não houver outra demanda aprovada;
7. não altere `app.yaml` para incorporar IDs ou caminhos corporativos.

O `app.yaml` recebe o caminho do Volume via `valueFrom: theme_storage`.

## 3. Implantar a pasta gerada

Use o mecanismo oficial autorizado pelo workspace para enviar o conteúdo de `.artifacts/v10-app/` como fonte do App. O arquivo `app.yaml` precisa ficar na raiz do projeto implantado.

A V10 não prescreve um nome corporativo de App, catálogo, schema ou Volume. Esses identificadores pertencem ao ambiente e não devem ser inventados no Git.

## 4. Smoke pós-deploy

Com usuário de teste autorizado:

1. abra o App e confirme que a identidade aparece sem pedir login adicional no próprio App;
2. abra um preset de demonstração;
3. faça uma alteração simples e valide;
4. compare base × proposta;
5. salve uma sessão de teste;
6. recarregue a página e reabra a sessão;
7. confirme revisão e histórico;
8. com uma segunda identidade autorizada, confirme que a sessão da primeira não aparece;
9. confirme visualmente que não existem ações de aprovar/publicar/promover;
10. registre somente evidência sanitizada no Git.

Esse smoke comprova operação do App/Volume naquele ambiente. Ele não substitui V12 (jornadas humanas, acessibilidade e usabilidade).

## 5. Falha durante deploy

Se o App não iniciar:

- confira logs do App;
- confirme que `theme_storage` existe e foi associado;
- confirme que o service principal tem privilégios de leitura/gravação no Volume;
- não troque o caminho para DBFS ou `/tmp` para contornar o erro;
- não habilite `HUB_THEME_LOCAL_DEV` em produção;
- não adicione PAT.

Se uma sessão não salvar, considere a operação falha até existir confirmação do App. Não invente recibo e não ajuste hash manualmente.

## 6. Rollback do App

Rollback da V10 significa voltar o **código do App** para um commit anterior ainda aprovado:

1. identifique o commit anterior e gere novamente seu bundle V10;
2. verifique `V10_APP_MANIFEST.json`;
3. mantenha o mesmo Volume; não apague sessões;
4. implante o bundle anterior pelo mesmo canal autorizado;
5. repita o smoke mínimo de abertura/listagem/reabertura;
6. registre commit anterior, commit revertido, motivo e resultado.

Não use force-push, limpeza recursiva ou exclusão do Volume como rollback.

## 7. O que este rollback não faz

O App V10 não publica temas. Portanto, retornar o App não significa retornar um tema compartilhado. O rollback de tema publicado continua sujeito à política V01: nova publicação de revisão anterior ainda aprovada, com guardas e histórico preservados.

## 8. Retenção e limpeza

A V10 não apaga automaticamente sessões e não oferece botão de exclusão. Se o ambiente exigir retenção, o administrador deve estabelecer política explícita para o Volume antes de executar qualquer limpeza. A ausência de política não autoriza descarte ad hoc.
