# Testes visuais do README de snippets

Esta pasta compara três formas de apresentar o mesmo conteúdo no Databricks sem
alterar o README usado como origem.

> **ESCOPO DE TESTE.** Os arquivos desta pasta são derivados e servem apenas
> para comparar renderização, navegação e legibilidade. Eles não substituem
> `README_snippets.md`, não ativam recursos da Genie Code e não devem ser
> editados como uma segunda fonte de verdade.

## Matriz dos testes

| Teste | Artefato local | Objeto esperado no workspace | O que avaliar |
|---|---|---|---|
| A · Markdown + PNG | `README_snippets_imagens.md` | arquivo Markdown | imagens relativas, tabelas, links e leitura sem execução |
| B · Notebook + Mermaid bruto | `README_snippets_mermaid.py` | notebook `README_snippets_mermaid` | se Mermaid vira diagrama ou permanece como código |
| C · Notebook + PNG | `README_snippets_imagens.py` | notebook `README_snippets_imagens` | imagens, sumário, células Markdown e leitura sem depender de Mermaid |

## Ordem sugerida de inspeção

1. Abra `README_snippets_imagens.md` e confirme se as três imagens aparecem.
2. Abra `README_snippets_mermaid` e procure os três blocos Mermaid.
3. Abra `README_snippets_imagens` e compare o resultado com o arquivo Markdown.
4. Teste títulos, tabelas, blocos de código e navegação em cada superfície.
5. Abra a Genie Code e adicione cada artefato separadamente com `@` ou
   **Add context**; faça a mesma pergunta de síntese e compare a fidelidade.

Pergunta sugerida para o teste de contexto:

```text
Usando somente o artefato anexado, explique:
1. quais são as seis categorias do Hub Snippets;
2. como uma pasta de objeto é organizada;
3. qual é o fluxo seguro para importar e usar um snippet.
Cite os nomes técnicos exatamente como aparecem no documento.
```

## Critérios de decisão

| Critério | Pergunta |
|---|---|
| renderização | todos os elementos aparecem sem código visual indesejado? |
| fidelidade | o conteúdo continua equivalente ao README de origem? |
| navegação | títulos, sumário e links levam ao destino esperado? |
| manutenção | existe uma única origem editável e uma geração reproduzível? |
| contexto da Genie | a resposta recupera relações e nomes sem depender só da imagem? |
| portabilidade | a solução funciona no workspace atual e pode ser repetida no corporativo? |

## Arquivos auxiliares

As fontes Mermaid ficam em `assets/diagramas/*.mmd`. Os PNGs de mesmo nome são
renderizações estáticas dessas fontes. O texto equivalente permanece junto às
imagens para acessibilidade e para consumo por modelos de linguagem.

Os PNGs foram renderizados com Mermaid CLI `11.17.0`. Para reproduzir um deles a
partir da raiz do projeto:

```powershell
npx -y @mermaid-js/mermaid-cli@11.17.0 `
  -i "READMEs_refeitos/readmes_viasual_melhorado/readmes_visual_testes/assets/diagramas/01_arquitetura_pasta.mmd" `
  -o "READMEs_refeitos/readmes_viasual_melhorado/readmes_visual_testes/assets/diagramas/01_arquitetura_pasta.png" `
  -b white -t neutral -w 1600
```

O README usado como origem foi
`../README_snippets.md` da variante visual aprimorada.
