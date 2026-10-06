# V05 — Visual Lab em notebook

> **Nota administrativa — 06/10/2026.** A integração vigente é a PR #37; a PR #26 e candidatas anteriores são históricas/supersedidas. Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência.

## Registro histórico preservado

## Estado desta sprint

**CANDIDATA EM FECHAMENTO; SEM ACEITE OU MERGE.** A V05 está sendo reconciliada na branch `codex/temas-v05-fechamento-r13-20260913`, baseada na `main` pós-D05 (`24ffce298ed543755eb15d5d7c553d02ce15e73e`). A PR histórica #26 e as branches anteriores permanecem preservadas como evidência; elas não representam a candidata corrente.

Esta sprint transforma a especificação textual da V01 em um laboratório de notebook. Ela não publica tema, não aprova proposta, não muda o padrão da equipe e não cria um Databricks App. O laboratório usa somente contexto `notebook` e mantém o núcleo V02 independente de `ipywidgets`.

Na candidata atual, as quatro partes operacionais planejadas para o laboratório estão implementadas: **escolha guiada de ponto de partida**, **ajuste**, **comparação** e **salvamento/reabertura de sessão com linhagem local**. Isso foi exercitado em testes Python/GitHub Actions; não equivale a homologação de navegador/runtime Databricks, acessibilidade, permissões reais ou UAT.

O [checkpoint](CHECKPOINT_V05.md) registra a composição, as execuções reprovadas/aprovadas e os bloqueios atuais. O [registro de testes](TESTES.md) separa explicitamente evidência de código da evidência operacional ainda ausente.

## Para quem nunca entrou no Hub

O Visual Lab é uma **prévia pessoal**. A regra operacional é:

> Alterações aqui não mudam o padrão da equipe.

A pessoa abre um launcher, escolhe uma base disponível, ajusta propriedades visuais, aplica a proposta, compara **Atual / Proposta**, desfaz, restaura e pode salvar uma sessão para retomá-la depois. Salvar uma proposta ou uma sessão não significa submeter, aprovar ou publicar.

As referências empacotadas de demonstração são identificadas como demonstração. Um mantenedor também pode preparar outros presets `notebook`, que são revalidados antes de aparecerem no catálogo. Chave desconhecida ou contexto incompatível falham fechados, sem substituição silenciosa.

Quando existe uma pasta de sessões explicitamente preparada, o launcher lista somente sessões completas e permite reabri-las sem código de carregamento escrito pelo operador. A reabertura restaura **base original, proposta, revisão e histórico**; a proposta não vira silenciosamente uma nova base.

Os controles **Submeter para revisão** e **Publicar versão aprovada** permanecem fora da entrega funcional de governança. O fato de um controle estar desabilitado na UI não é mecanismo de autorização.

## Arquitetura

A V05 acrescenta o objeto:

`hub_snippets.visual.theme_lab`

Ele é separado de `visual.tema` de propósito:

- `visual.tema` continua sendo o núcleo V02 offline, sem dependência de UI;
- `theme_lab` consome o núcleo e os adaptadores de apresentação V03/V04;
- importar `theme_lab` não importa `ipywidgets`;
- `ipywidgets` só é exigido ao construir a interface;
- `dbutils.widgets` entra somente por objeto injetado pelo notebook;
- nenhum tema global é ativado e `pio.templates.default` não é alterado;
- rede, Spark, SQL e MLflow não fazem parte da geração da prévia.

A fachada pública inclui rascunho, metadados de controles, presets, prévias, recibos de persistência, listagem/reabertura de sessão e as duas superfícies de UI (`build_ipywidgets_lab` e `build_theme_lab_launcher`).

## As quatro áreas da experiência V01

### 1. Escolher

`get_demo_presets()` expõe referências notebook empacotadas e marcadas explicitamente como demonstração. `prepare_theme_lab_presets()` permite ao mantenedor fornecer outros `ResolvedTheme` notebook; cada entrada é revalidada pelo núcleo.

`create_theme_lab_from_preset()` cria o rascunho a partir de uma chave conhecida. O launcher apresenta a escolha em dropdown e diferencia visualmente referências de demonstração. Selecionar uma base não a aprova nem altera o padrão da equipe.

### 2. Ajustar

`get_control_specs()` deriva do schema canônico tipo, descrição, unidade, limites e controle sugerido. A UI acrescenta nomes legíveis em português. Cor possui seletor e campo HEX; paletas e dimensões continuam sujeitas ao contrato V02.

Ao aplicar, todos os campos pendentes formam uma única proposta. Se qualquer valor falhar, a configuração completa é recusada e o último estado válido permanece. Campos sem consumidor correspondente na galeria ficam desabilitados com motivo explícito, em vez de aparentar efeito inexistente.

### 3. Comparar

A galeria usa adaptadores reais V03/V04 com **dados sintéticos fixos** em seis representações por lado:

- cabeçalho de seção;
- KPI;
- barras;
- série temporal;
- mapa de calor;
- tabela.

A comparação Atual/Proposta preserva valores, nomes e ordem dos dados; somente a aparência deve variar. A galeria completa exige `mode=light`, porque o adaptador Plotly V03 continua fail-closed para `dark` e `high_contrast`.

### 4. Salvar e reabrir

Existem dois mecanismos distintos:

- `export_bytes()` / `save_proposal()` produzem somente o JSON canônico da proposta atual;
- `save_theme_lab_session()` cria uma sessão rastreável com base, proposta, histórico e manifesto.

Uma sessão completa contém `base.json`, `proposal.json`, estados do histórico e `session.json`. O manifesto é escrito por último, registra hashes e revisão e funciona como marcador de completude. Diretório parcial sem manifesto não aparece na listagem nem pode ser reaberto como sessão válida.

`reopen_theme_lab_session()` relê, revalida e confere os hashes. Divergência é recusada; o código não corrige hash para continuar. A linhagem é local ao laboratório e não autentica autor, não registra aprovação de governança e não é assinatura digital.

## Desfazer e restaurar

Cada alteração válida troca o `ResolvedTheme` atual de forma atômica e preserva o anterior no histórico da instância, limitado a cem estados.

- **Desfazer**: retorna ao estado válido anterior;
- **Restaurar ponto de partida**: retorna à base original;
- erro de validação: não cria histórico nem altera o hash atual;
- duas instâncias: não compartilham histórico ou tema;
- sessão reaberta: preserva histórico suficiente para continuar o `undo()` registrado.

Nenhuma dessas ações revoga publicação, porque V05 não publica.

## Interface `ipywidgets`

`build_ipywidgets_lab(draft)` constrói o editor para um rascunho já escolhido. `build_theme_lab_launcher()` acrescenta a entrada guiada por presets e sessões.

A interface oferece controles principais e avançados, aplicação da prévia, comparação, desfazer, restaurar, exportar JSON e persistência local quando `save_root` foi preparado. Campos editados e ainda não aplicados bloqueiam salvamento/exportação para evitar gravar algo diferente do que acabou de ser visualizado.

Sem `save_root`, operações persistentes não são habilitadas. Informar um diretório não concede permissões nem o transforma em destino aprovado.

## Fallback `dbutils.widgets`

Se `ipywidgets` não estiver disponível, `install_dbutils_fallback()` e `apply_dbutils_fallback()` oferecem os sete controles primários como texto. A API recebe `dbutils` explicitamente; o módulo não presume um global.

Esse fallback exige reexecução da célula para aplicar os valores e é funcionalmente menor: não oferece a experiência completa de catálogo/sessões do launcher. Ele não deve ser apresentado como paridade visual com `ipywidgets`.

## Dependências e Databricks

O produto não instala dependências. Validar tema requer `jsonschema` e `referencing`; a galeria usa pandas, Plotly e Jinja2; a interface completa usa ipywidgets/IPython quando construída.

O workflow V05 instala `ipywidgets` no runner para impedir que a ausência da biblioteca transforme testes da UI em um PASS com SKIP. Esse teste prova a construção/callback Python exercitada no runner, não a renderização no navegador Databricks.

Segundo a documentação oficial usada nesta iniciativa, ipywidgets e widgets de notebook possuem requisitos e limitações do ambiente. A compatibilidade do workspace-alvo continua sendo gate operacional separado.

## Segurança e efeitos

O módulo V05 não contém chamadas de rede, Spark/SQL, MLflow, publicação, `force_publish` ou autenticação fictícia por campo de UI. O schema e o manifesto continuam sendo revalidados pelo núcleo V02.

Salvamento exige pasta regular já existente e nome permitido, não sobrescreve destino existente e aplica guardas locais contra caminhos inadequados/symlinks previstos. Falha de I/O não gera recibo de sucesso. No JSON avulso, uma falha posterior à criação pode deixar resíduo parcial; isso precisa ser inspecionado antes de nova tentativa.

Essas guardas não substituem ACL do ambiente nem formam uma sandbox contra outro processo.

## Testes da V05

As suítes atuais são:

- `tools/tests/test_temas_v05.py`;
- `tools/tests/test_temas_v05_integracao.py`;
- `tools/tests/test_temas_v05_sessions.py`.

Elas cobrem contexto/tipo, edição atômica, limites do schema, isolamento, undo/restore, prévia sintética, persistência segura, callbacks Python, campos pendentes, presets, manifesto, hashes, sessão incompleta, adulteração, roundtrip de base/proposta/histórico/revisão e reabertura pelo launcher.

O workflow permanente `.github/workflows/temas-v05-ci.yml` usa `contents: read`. O [registro de testes](TESTES.md) preserva inclusive execuções reprovadas; não se converte falha histórica em PASS.

## O que ainda não foi provado ou entregue

Mesmo com os contratos Python exercitados, permanecem NÃO HOMOLOGADOS/PENDENTES:

- renderização real do ipywidgets em Databricks Free/trabalho;
- callbacks/lifecycle no frontend do runtime-alvo;
- acessibilidade por teclado e leitor de tela;
- contraste percebido e zoom;
- tempo p95 da prévia no ambiente real;
- permissões reais da pasta de sessões e comportamento após reinício do ambiente;
- usuário iniciante operando sem ajuda;
- submissão, aprovação e publicação;
- Databricks App e AI/BI;
- auditoria independente da experiência final.

Esses itens não invalidam os testes de unidade/integração; simplesmente pertencem a gates diferentes.

## Ponto de parada desta sprint

Antes de solicitar aceite integral, a mesma árvore candidata precisa satisfazer:

1. suíte específica V05 sem falha e sem SKIP de ipywidgets;
2. regressões V01–V05 e V00 verdes;
3. fonte e derivado sincronizados;
4. `validate_assistant.py --conferir-readme` verde;
5. `ci_local.py` e CI geral verdes;
6. Manual, CHANGELOG, índices, documentação V05 e guia de primeiro uso coerentes;
7. mudanças paralelas da `main` reconciliadas sem perda;
8. revisão final do diff e das guardas;
9. nova PR draft final com checks verdes;
10. aceite explícito antes de qualquer merge.

Mesmo depois desses itens, publicação/homologação Databricks continua separada. Esta sprint não inicia a V06.

[Checkpoint](CHECKPOINT_V05.md) · [Testes e evidências](TESTES.md) · [Especificação V01](../V01/EXPERIENCIA_LABORATORIO.md)
