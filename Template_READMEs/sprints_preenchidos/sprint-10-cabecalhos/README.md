<a id="cabeçalhos-crm-e-squad"></a>

# Cabeçalhos CRM e Squad

Cabeçalhos editoriais aprovados, compartilhados entre guias e notebooks.
São identidade visual do projeto, não logotipos nem recursos nativos da Databricks.

> **Rascunho de sprint 10 — não publicado.** Destino previsto:
> `ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/README.md`.

O banner identifica o documento. O **título e as instruções continuam em
Markdown**, abaixo da imagem — não estão “dentro” do PNG de forma obrigatória.

---

<a id="crm-guias-e-notebooks-gerais"></a>

## CRM — guias e notebooks gerais

![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

Texto aprovado: **CRM** · **Missão Modelos Analíticos CRM**. Não use a palavra
“Área”.

Um único PNG (1920 × 480) serve a README e notebook. A faixa horizontal
preserva espaço para o conteúdo e permanece legível a partir de cerca de 720 px
de largura, com o menor texto nominal da arte em 18 px nessa largura (48 × 720 / 1920). Abaixo disso, confira a leitura no preview; dimensão não substitui inspeção visual.

Não crie uma versão “só para notebook”: o arquivo canônico é este.

---

<a id="squad-notebooks-específicos"></a>

## Squad — notebooks específicos

![Squad Modelos Analíticos e Preditivos](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_squad.png)

Texto: **Squad Modelos Analíticos e Preditivos**. Use quando a identificação da
Squad for a apropriada. **Não empilhe** CRM e Squad no mesmo documento. Não
invente variação de nome.

**Decisão.** Guia geral da missão → CRM. Notebook claramente da Squad → Squad.

---

<a id="uso-no-markdown-e-em-notebooks"></a>

## Uso no Markdown e em notebooks

O [suporte a imagens de workspace](https://docs.databricks.com/aws/en/notebooks/notebook-media)
aceita caminhos relativos ou absolutos em células Markdown. Não é necessário
ligar compute, Mermaid ou `displayHTML` só para exibir o PNG. Confirme o
comportamento da sua versão se a documentação local divergir.

<a id="escolher"></a>

### Escolher

CRM ou Squad, um só.

<a id="localizar-o-arquivo-central"></a>

### Localizar o arquivo central

`hub_readmes_visual_assets/headers/png/cabecalho_crm.png` (ou `_squad`).

<a id="inserir-readme-nesta-pasta"></a>

### Inserir — README nesta pasta

```markdown
![CRM — Missão Modelos Analíticos CRM](./png/cabecalho_crm.png)

# Título do documento
```

Cada segmento: `.` = pasta atual (`headers/`), `png/` = subpasta, arquivo = PNG
canônico.

<a id="inserir-célula-de-notebook-nesta-pasta"></a>

### Inserir — célula de notebook nesta pasta

```markdown
%md
![Squad Modelos Analíticos e Preditivos](./png/cabecalho_squad.png)

# Título do notebook
```

A célula precisa ser Markdown (`%md`). O preview deve mostrar a faixa; o título
H1 aparece **abaixo**.

<a id="inserir-outro-diretório"></a>

### Inserir — outro diretório

Calcule o relativo. Exemplo a partir de `hub_snippets/README.md`:

```markdown
![CRM — Missão Modelos Analíticos CRM](../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)
```

`..` sobe de `hub_snippets/` para `.assistant/`. Publique a árvore de assets
junto. Imagem no Markdown **não** é import Python nem link de notebook (`../`
de notebook Databricks tem outra semântica).

Não forneça URL de workspace como se fosse o arquivo.

<a id="inserir-notebook-em-outra-pasta"></a>

### Inserir — notebook em outra pasta

Considere o notebook `.assistant/hub_snippets/ml/split_temporal/exemplo_split_temporal`. De sua pasta, três subidas chegam a `.assistant`: `split_temporal → ml → hub_snippets → .assistant`.

```markdown
%md
![Squad Modelos Analíticos e Preditivos](../../../hub_readmes_visual_assets/headers/png/cabecalho_squad.png)

# Divisão temporal: exemplo acompanhado
```

Esse caminho pertence ao notebook descrito, não à localização deste README. Se o notebook for movido, calcule o relativo novamente. Não acrescente o prefixo `$` usado para links de navegação entre notebooks a um caminho de imagem.

<a id="conferir"></a>

### Conferir

Preview com imagem visível, alt descritivo, título em texto. Sem compute.

<a id="resolver-imagem-ausente"></a>

### Resolver imagem ausente

Caminho errado, PNG não publicado, ou maiúsculas diferentes. Corrija a
referência; não duplique o arquivo “para funcionar”.

<a id="acessibilidade-e-contexto-textual"></a>

### Acessibilidade e contexto textual

- Título, finalidade e exemplos em Markdown normal.
- Alt descritivo; se a identificação já está no texto imediatamente abaixo,
  alt vazio pode tratar o banner como decorativo.
- Não dependa de a IA ler pixels para regras ou aceite.
- Linhas da arte de fundo são decorativas: não significam execução, ACL ou
  automação.

---

<a id="manutenção-sem-cópias-concorrentes"></a>

## Manutenção sem cópias concorrentes

| Local | Papel | Como alterar |
|---|---|---|
| `src/fundo_tecnologico_original.png` | arte raster sem texto | nova proposta, preservando a referência |
| `src/copy.json` | textos, pesos, cores, posição | editar e regenerar |
| `src/*_tipografia.svg` | camada tipográfica gerada | não editar à mão |
| `png/` | dois arquivos finais | regenerar, conferir, publicar |
| `manifest.json` e `qa/` | hashes | gerados pelo compositor |

Na raiz do repositório de autoria:

```powershell
node tools/readme_visuals/headers.mjs
```

O fundo foi gerado por ferramenta de imagem e congelado; a composição e a
tipografia Inter são determinísticas. **Não existe SVG da ilustração completa.**
Proveniência: [src/PROMPT_FUNDO.md](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/src/PROMPT_FUNDO.md). Licença:
[Inter OFL](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/licenses/Inter-OFL.txt).
