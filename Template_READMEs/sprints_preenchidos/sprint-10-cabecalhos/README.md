# Cabeçalhos CRM e Squad

Cabeçalhos editoriais aprovados, compartilhados entre guias e notebooks.
São identidade visual do projeto, não logotipos nem recursos nativos da Databricks.

> **Rascunho de sprint 10 — não publicado.** Destino previsto:
> `ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/README.md`.

O banner identifica o documento. O **título e as instruções continuam em
Markdown**, abaixo da imagem — não estão “dentro” do PNG de forma obrigatória.

---

## CRM — guias e notebooks gerais

![CRM — Missão Modelos Analíticos CRM](png/cabecalho_crm.png)

Texto aprovado: **CRM** · **Missão Modelos Analíticos CRM**. Não use a palavra
“Área”.

Um único PNG (1920 × 480) serve a README e notebook. A faixa horizontal
preserva espaço para o conteúdo e permanece legível a partir de cerca de 720 px
de largura, com o menor texto da arte acima de 18 px.

Não crie uma versão “só para notebook”: o arquivo canônico é este.

---

## Squad — notebooks específicos

![Squad Modelos Analíticos e Preditivos](png/cabecalho_squad.png)

Texto: **Squad Modelos Analíticos e Preditivos**. Use quando a identificação da
Squad for a apropriada. **Não empilhe** CRM e Squad no mesmo documento. Não
invente variação de nome.

**Decisão.** Guia geral da missão → CRM. Notebook claramente da Squad → Squad.

---

## Uso no Markdown e em notebooks

O [suporte a imagens de workspace](https://docs.databricks.com/aws/en/notebooks/notebook-media)
aceita caminhos relativos ou absolutos em células Markdown. Não é necessário
ligar compute, Mermaid ou `displayHTML` só para exibir o PNG. Confirme o
comportamento da sua versão se a documentação local divergir.

### Escolher

CRM ou Squad, um só.

### Localizar o arquivo central

`hub_readmes_visual_assets/headers/png/cabecalho_crm.png` (ou `_squad`).

### Inserir — README nesta pasta

```markdown
![CRM — Missão Modelos Analíticos CRM](./png/cabecalho_crm.png)

# Título do documento
```

Cada segmento: `.` = pasta atual (`headers/`), `png/` = subpasta, arquivo = PNG
canônico.

### Inserir — célula de notebook nesta pasta

```markdown
%md
![Squad Modelos Analíticos e Preditivos](./png/cabecalho_squad.png)

# Título do notebook
```

A célula precisa ser Markdown (`%md`). O preview deve mostrar a faixa; o título
H1 aparece **abaixo**.

### Inserir — outro diretório

Calcule o relativo. Exemplo a partir de `hub_snippets/README.md`:

```markdown
![CRM — Missão Modelos Analíticos CRM](../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)
```

`..` sobe de `hub_snippets/` para `.assistant/`. Publique a árvore de assets
junto. Imagem no Markdown **não** é import Python nem link de notebook (`../`
de notebook Databricks tem outra semântica).

Não forneça URL de workspace como se fosse o arquivo.

### Conferir

Preview com imagem visível, alt descritivo, título em texto. Sem compute.

### Resolver imagem ausente

Caminho errado, PNG não publicado, ou maiúsculas diferentes. Corrija a
referência; não duplique o arquivo “para funcionar”.

### Acessibilidade e contexto textual

- Título, finalidade e exemplos em Markdown normal.
- Alt descritivo; se a identificação já está no texto imediatamente abaixo,
  alt vazio pode tratar o banner como decorativo.
- Não dependa de a IA ler pixels para regras ou aceite.
- Linhas da arte de fundo são decorativas: não significam execução, ACL ou
  automação.

---

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
Proveniência: [src/PROMPT_FUNDO.md](src/PROMPT_FUNDO.md). Licença:
[Inter OFL](../licenses/Inter-OFL.txt).
