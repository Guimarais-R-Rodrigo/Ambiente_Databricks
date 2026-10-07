# Preparar um tema para AI/BI

Este guia separa o que o projeto consegue preparar localmente do que precisa ser feito em um workspace Databricks autorizado.

## 1. Entenda os dois níveis de tema

**Tema do workspace:** é administrado no workspace e serve como padrão para dashboards novos. Gerenciá-lo exige administrador do workspace.

**Tema do dashboard:** é configurado em um dashboard em estado draft. Ele pode usar o tema do workspace, um preset ou uma customização local. `Color mappings` por valor pertencem ao nível do dashboard.

Ao aplicar o tema do workspace a um dashboard existente, o dashboard recebe um **snapshot**. Se o administrador mudar o tema do workspace depois, o dashboard existente não é atualizado automaticamente; é necessário reaplicar manualmente.

## 2. O que a ponte produz

A função `project_theme()` recebe um `ResolvedTheme` do contexto `notebook` e cria uma projeção auditável. Cada token recebe uma destas classes:

- `translated`: existe capacidade nativa com semântica suficientemente equivalente;
- `approximated`: há capacidade parecida, mas exige decisão/revisão;
- `unsupported`: a ponte não mapeia equivalência segura e não tenta esconder a lacuna.

A projeção exportada pelo Hub **não é um arquivo para o botão Import theme**.

## 3. Como preparar um arquivo nativo sem inventar o schema

Quando houver autorização para trabalhar em um dashboard real:

1. abra um dashboard **draft**;
2. acesse `Settings` e a seção `Theme`;
3. use `Export theme` para baixar o JSON nativo;
4. preserve esse arquivo original;
5. calcule/registre seu SHA-256;
6. um mantenedor técnico deve revisar o JSON e construir um binding entre as três capacidades diretas da ponte e JSON Pointers que já existam nesse export;
7. `bind_native_template()` só aceitará o template se o SHA-256 for exatamente o esperado e só substituirá campos já existentes;
8. o arquivo resultante ainda é **candidato local** até ser testado pelo `Import theme` do próprio Databricks.

Se o Databricks rejeitar o arquivo, não altere guardas para “fazer funcionar”. Reexporte a versão nativa, revise o binding e registre a diferença de formato.

## 4. Como testar sem alterar dados

Use o fixture `dashboard_sintetico.json` apenas como roteiro local. Ele representa KPI, série temporal, barras, tabela, texto e filtros com dados sintéticos; não é formato Databricks.

No workspace autorizado, o equivalente deve preservar:
- datasets/queries;
- filtros;
- campos;
- agregações;
- unidades;
- ordenações;
- semântica de categorias.

A mudança deve ser somente visual.

## 5. O que revisar visualmente

Confira em claro e escuro:
- paleta categórica;
- fundo de widget;
- raio de canto;
- textos;
- linhas de grade;
- seleção;
- gradientes;
- `Color mappings` locais, quando usados.

Itens `approximated` não devem ser tratados como equivalência exata. Itens `unsupported` permanecem sem tradução.

## 6. Publicação

Escolher/importar um tema e publicar um dashboard são ações separadas. A ponte não implementa publicação.

Se você não possui permissão administrativa, não tente gerenciar o tema do workspace. Use apenas o fluxo permitido para o dashboard que você pode editar.

## 7. Recuperação

Se uma tentativa de importação de tema falhar, o Databricks documenta que o dashboard permanece sem alteração. Mantenha o export original para restauração e registre a versão do template/binding usado.

Nenhuma etapa deste guia autoriza alteração no workspace sem a autorização operacional correspondente.
