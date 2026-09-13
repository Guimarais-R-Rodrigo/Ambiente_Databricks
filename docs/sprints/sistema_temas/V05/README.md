# V05 — Visual Lab em notebook

## Estado desta sprint

**EM DESENVOLVIMENTO; SEM ACEITE OU MERGE.** A V05 parte da `main`
`089fea3a33a202fb59ab776f734461e91e5b99c1`, onde V04 já está aceita,
integrada e pós-merge verde.

Esta sprint transforma a especificação textual da V01 em um laboratório de
notebook. Ela não publica tema, não aprova proposta, não muda o padrão da equipe
e não cria um Databricks App. O laboratório usa somente contexto `notebook` e
mantém o núcleo V02 independente de `ipywidgets`.

## Para quem nunca entrou no Hub

O Visual Lab é uma **prévia pessoal**. A primeira mensagem precisa ser lida como
regra operacional:

> Alterações aqui não mudam o padrão da equipe.

A pessoa pode partir de um tema notebook já resolvido, ajustar propriedades,
comparar **Atual / Proposta**, desfazer, restaurar e exportar ou salvar um
rascunho. Salvar um JSON não significa submeter, aprovar ou publicar.

Na V05, os controles **Submeter para revisão** e **Publicar versão aprovada**
aparecem desabilitados para explicar a separação de etapas. O fato de estarem
desabilitados na UI não é mecanismo de autorização; publicação real permanece
fora desta sprint.

## Arquitetura

A V05 usa um novo objeto:

`hub_snippets.visual.theme_lab`

Ele é separado de `visual.tema` de propósito:

- `visual.tema` continua sendo o núcleo V02 offline, sem dependência de UI;
- `theme_lab` depende do núcleo e dos adaptadores de apresentação;
- importar `theme_lab` não importa `ipywidgets`;
- `ipywidgets` só é exigido ao construir a interface;
- `dbutils.widgets` entra apenas por objeto injetado pelo notebook;
- nenhum global de tema é alterado.

## Quatro áreas da experiência V01

A V01 definiu quatro áreas: escolher, ajustar, comparar e salvar proposta. A V05
materializa esse desenho sem antecipar governança futura.

### 1. Escolher

O laboratório recebe explicitamente um `ResolvedTheme` notebook. A fixture
`legado_notebook` pode demonstrar compatibilidade, mas continua sendo fixture,
não um tema operacional aprovado.

Troca de contexto não é oferecida nesta primeira implementação V05: um laboratório
notebook aceita notebook. Isso evita conversão silenciosa para README ou
presentation.

### 2. Ajustar

`get_control_specs()` lê do schema canônico:

- tipo;
- descrição;
- unidade;
- limite mínimo/máximo;
- tipo de controle sugerido;
- quem pode editar segundo a especificação.

A UI acrescenta nomes em português. Cor possui seletor e campo HEX. Ao aplicar,
todos os valores são tratados como uma única proposta: se qualquer campo falhar,
`resolve_theme` recusa a configuração completa e a última prévia válida permanece.

Normalizar `#0066cc` para `#0066CC` é uma ação explícita da autoria; a importação
do núcleo V02 continua sem corrigir silenciosamente arquivos externos.

### 3. Comparar

A galeria usa os adaptadores reais V03/V04 com **dados sintéticos fixos**:

- barras;
- série temporal com um ponto ausente;
- mapa de calor;
- KPI;
- tabela com valor negativo e nulo;
- cabeçalho de seção.

A comparação Atual/Proposta usa os mesmos arrays e tabela. A V05 não consulta
Spark, SQL, MLflow, tabela corporativa ou endpoint para gerar a prévia.

A galeria completa exige `mode=light` porque o adaptador Plotly V03 continua
fail-closed para `dark` e `high_contrast`. A V04 HTML aceitar esses modos não é
razão para simular uma galeria completa que Plotly ainda não suporta.

### 4. Salvar/exportar proposta

`export_bytes()` devolve o JSON canônico em memória e não cria arquivo.

`save_proposal(root, filename)` exige:

- pasta já existente e explicitamente escolhida;
- nome simples em minúsculas terminado em `.json`;
- nenhum path embutido;
- nenhum sobrescrever de arquivo existente.

O recibo informa nome, SHA-256, bytes e revisão local. É recibo de **rascunho
salvo**, não de publicação.

## Desfazer e restaurar

Cada alteração válida troca o `ResolvedTheme` atual de forma atômica e preserva
o anterior no histórico da instância.

- **Desfazer**: retorna ao estado válido anterior;
- **Restaurar ponto de partida**: retorna ao tema carregado inicialmente;
- erro de validação: não cria item de histórico nem altera o hash atual;
- duas instâncias: não compartilham histórico ou tema.

Nenhuma dessas ações revoga uma publicação, porque V05 não publica.

## Interface `ipywidgets`

`build_ipywidgets_lab(draft)` retorna uma estrutura `ThemeLabUI`. O notebook
faz `display(ui.root)` explicitamente.

A UI contém:

- controles principais visíveis;
- seção Avançado em `Accordion`;
- Aplicar na prévia;
- Desfazer;
- Restaurar ponto de partida;
- Exportar JSON na saída;
- campo de nome + Salvar proposta;
- aba Comparar;
- Submeter e Publicar desabilitados com explicação.

Sem `save_root`, Salvar fica desabilitado. Informar `save_root` habilita somente
escrita de rascunho nesse diretório; não cria pasta nem publica.

## Fallback `dbutils.widgets`

Se `ipywidgets` não estiver disponível, a V05 oferece fallback para os controles
primários. A API recebe `dbutils` explicitamente; o módulo não presume um global.

`install_dbutils_fallback` cria widgets de texto. `apply_dbutils_fallback` lê os
valores como strings e aplica todos de forma atômica. Como widgets nativos não
oferecem o mesmo callback Python interativo, é necessário reexecutar a célula de
aplicação depois do ajuste.

Esse fallback é funcionalmente menor e deve ser apresentado como tal, não como
paridade visual falsa com `ipywidgets`.

## Dependências e Databricks

O produto não fixa nem instala `ipywidgets`. O workflow V05 instala `ipywidgets`
somente no runner para provar que a construção real da UI funciona e para impedir
que a ausência da biblioteca seja promovida a PASS.

Segundo a documentação oficial Databricks consultada durante esta sprint:

- ipywidgets é a rota recomendada para controles Python interativos em notebooks
  compatíveis;
- `dbutils.widgets` é apropriado para parâmetros e integrações com jobs;
- ipywidgets exige compute compatível;
- estado de widgets não deve ser tratado como persistente entre sessões;
- existem limitações de renderização, incluindo modo escuro.

Essas afirmações de plataforma não substituem homologação no workspace-alvo.

## Segurança e efeitos

O módulo V05 não deve conter:

- chamadas de rede;
- Spark/SQL;
- MLflow;
- publicação;
- `force_publish`;
- alteração de `pio.templates.default`;
- autenticação fictícia por campo da UI.

O schema e o manifesto continuam sendo revalidados pelo núcleo V02. Metadados de
controle são lidos do schema somente depois de conferir que seu SHA corresponde
ao tema resolvido.

## Testes da V05

A suíte `tools/tests/test_temas_v05.py` cobre, entre outros:

- contexto e tipo de tema;
- atualização atômica;
- cor e paleta;
- limites do schema;
- estado entre instâncias;
- undo/restore;
- exportação em memória;
- save sem sobrescrever;
- metadados do schema;
- preservação dos dados na comparação;
- ausência de mutação do template Plotly global;
- recusa de `dark/high_contrast` na galeria completa;
- fallback dbutils;
- import sem ipywidgets;
- construção real da UI com ipywidgets no workflow V05;
- documentação/forma do objeto.

O workflow permanente `.github/workflows/temas-v05-ci.yml` tem `contents: read`.
No gate específico, ipywidgets é obrigatório; ausência não vira SKIP aprovado.

## O que ainda não foi provado

Mesmo que todos os testes offline passem, permanecem NÃO TESTADOS/PENDENTES:

- renderização real do ipywidgets em Databricks Free/trabalho;
- callbacks e lifecycle em runtime Databricks específico;
- acessibilidade por teclado/leitor de tela;
- contraste percebido e zoom;
- tempo p95 da prévia no ambiente real;
- persistência/recuperação após reinício de sessão;
- permissões reais do destino de rascunhos;
- usuário iniciante operando sem ajuda;
- submissão, aprovação e publicação;
- Databricks App e AI/BI.

## Ponto de parada desta sprint

A V05 pode ser considerada **candidata técnica** quando, na mesma árvore:

1. suíte V05 sem falha e sem SKIP de ipywidgets no workflow específico;
2. regressões V01–V04 e V00 verdes;
3. fachada pública igual ao gerador canônico;
4. fonte e espelho sincronizados;
5. `validate_assistant.py --conferir-readme` verde;
6. `ci_local.py` verde;
7. documentação V05 e guia de primeiro uso completos;
8. nenhuma publicação Databricks;
9. mudanças paralelas da `main` reconciliadas;
10. aceite explícito solicitado antes do merge.

[Checkpoint](CHECKPOINT_V05.md) · [Testes e evidências](TESTES.md) · [Especificação V01](../V01/EXPERIENCIA_LABORATORIO.md)
