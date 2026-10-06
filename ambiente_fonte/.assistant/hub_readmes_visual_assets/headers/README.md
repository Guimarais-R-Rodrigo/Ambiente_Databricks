# Cabeçalhos CRM e Squad

Cabeçalhos editoriais aprovados, compartilhados entre guias e notebooks.
São identidade visual do projeto, não logotipos nem recursos nativos da Databricks.

## CRM — guias e notebooks gerais

![CRM — Missão Modelos Analíticos CRM](png/cabecalho_crm.png)

Texto: **CRM** · **Missão Modelos Analíticos CRM**.

Um único PNG atende aos dois usos. O formato de 1920 × 480 px cria uma faixa
horizontal. A composição avaliada usa referência de 720 px de largura, com menor texto calculado em 18 px; isso não comprova acessibilidade em todo dispositivo. Confira zoom, contraste e leitura na superfície real.

## Squad — notebooks específicos

![Squad Modelos Analíticos e Preditivos](png/cabecalho_squad.png)

Texto: **Squad Modelos Analíticos e Preditivos**. As quebras de linha mantêm a
frase exata e o tamanho da tipografia. Este banner substitui o de CRM quando
a identificação específica da Squad é a apropriada; não empilhe os dois.

## Uso no Markdown e em notebooks

O [suporte oficial a imagens de workspace](https://docs.databricks.com/aws/en/notebooks/notebook-media)
permite caminhos relativos ou absolutos em células Markdown. Não é necessário
iniciar compute, usar Mermaid ou executar `displayHTML` para exibir o PNG.

Em um documento localizado nesta pasta, o cabeçalho CRM usa:

```markdown
![CRM — Missão Modelos Analíticos CRM](./png/cabecalho_crm.png)

# Título do documento
```

Em uma célula Markdown de notebook localizado nesta pasta:

```markdown
%md
![Squad Modelos Analíticos e Preditivos](./png/cabecalho_squad.png)

# Título do notebook
```

Em outro diretório, ajuste o caminho a partir do documento consumidor, mantendo
o arquivo central. Publique a árvore de assets junto do documento. Imagens
embutidas não são importações Python, nem usam o prefixo de links entre notebooks.

### Caminhos em outros documentos

Na raiz `.assistant`, o caminho é `hub_readmes_visual_assets/headers/png/cabecalho_crm.png`. Em um notebook dentro de `hub_snippets/ml/metrics_report/`, o caminho relativo é `../../../hub_readmes_visual_assets/headers/png/cabecalho_crm.png`. Derive o caminho a partir do documento consumidor e confira a imagem sem iniciar compute. Preserve título e identificação em texto, além do alt. Não copie o PNG para cada pasta.

### Acessibilidade e contexto textual

- Mantenha título, finalidade, instruções e exemplos em Markdown normal. A
  identificação nunca deve ser a única informação legível fora dos pixels.
- Preserve alt descritivo; se toda a identificação estiver imediatamente
  repetida em texto, pode usar alt vazio para tratar o banner como decorativo.
- Não dependa de leitura de imagens pela IA para regras, paths ou critérios de
  aceite. A Genie Code pode usar contexto visual, mas o texto continua explícito.
- As conexões da arte são decorativas: não representam execução, permissões,
  disponibilidade de serviços ou automação do Hub.

## Origem, licença e alteração

Para usar, referencie o PNG compartilhado e preserve identificação em texto. Para alterar o banner, solicite revisão ao mantenedor. O fundo é arte raster gerada e congelada; não é um logotipo solicitado. A tipografia Inter tem [licença própria](../licenses/Inter-OFL.txt). A procedência e os hashes acompanham o asset; a nova geração pelo mesmo prompt não garante bytes idênticos.

O procedimento de composição está no [guia externo do mantenedor](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/readme-readequacao-20261006/tools/readme_visuals/README.md). O arquivo-fonte de proveniência continua preservado em `src/PROMPT_FUNDO.md`; não é leitura necessária para inserir o cabeçalho.
