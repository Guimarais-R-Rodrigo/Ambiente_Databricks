# Recursos visuais: trechos de manutenção realocados

Baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`. Textos históricos preservados; receita vigente no [compositor](../../../tools/readme_visuals/README.md).

## R0081

## Geração candidata por tema — V06

A V06 acrescenta uma rota de manutenção **separada do pacote ativo**. Um
`theme_id` canônico é resolvido pelo núcleo `hub_snippets.visual.tema`; somente
depois disso o compositor v2 recebe os tokens validados. A geração vai para
`.artifacts/visual-v2/theme-variants/` e nunca substitui automaticamente os PNGs
deste diretório.

O contrato está em [specs/theme_generation.yaml](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_readmes_visual_assets/specs/theme_generation.yaml).
Assets congelados continuam protegidos por hash e não são recoloridos. Quando um
asset paramétrico muda de bytes, a saída é marcada `variant_review_required` e
precisa de nova revisão antes de qualquer promoção.

Para o operador comum do Hub, nada muda: continue consumindo os PNGs canônicos.
A rota V06 é uma ferramenta de manutenção local; gerar uma variante não significa
aprovar, publicar ou instalar um tema no Databricks.

## Como manter

A partir da raiz do repositório de autoria, com as dependências fixadas instaladas:

```powershell
node tools/readme_visuals/headers.mjs
node tools/readme_visuals/production.mjs --family all
node tools/readme_visuals/validate_production.mjs
python tools/validate_assistant.py
python tools/render_simulado.py --write
```

Os layouts ficam em `tools/readme_visuals/archetypes/`, apoiados por
`tools/readme_visuals/lib.mjs`. Os cinco PNGs de assinatura e os dois cabeçalhos
aprovados são preservados por hashes. Os contratos delimitam finalidade,
limites, legenda e consumidor; o [índice textual das figuras](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_readmes_visual_assets/CONTEUDO_FIGURAS.md)
permite conferir o conteúdo renderizado sem depender de OCR.

O manifesto lista os ativos vigentes, não os históricos. As versões anteriores
permanecem no histórico Git e no baseline de avaliação, fora deste pacote ativo.
No workspace, consuma os PNGs; a autoria e os gates pertencem ao repositório.

`tools/render_readme_visuals.mjs` e o renderer da Sprint 0 são ferramentas da
rodada anterior; não use esses comandos para regenerar o pacote v2.

## R0082

## Manutenção sem cópias concorrentes

| Local | Papel | Como alterar |
|---|---|---|
| `src/fundo_tecnologico_original.png` | arte raster original sem texto | nova proposta visual, preservando a referência aprovada |
| `src/copy.json` | textos, pesos, cores e posicionamento | editar o texto exato e regenerar |
| `src/*_tipografia.svg` | camada tipográfica gerada | não editar manualmente |
| `png/` | dois arquivos finais usados pelos documentos | regenerar, conferir e publicar |
| `manifest.json` e `qa/` | hashes e verificações | gerados pelo compositor |

Comando de autoria, na raiz do repositório:

```powershell
node tools/readme_visuals/headers.mjs
```

O fundo foi gerado pela ferramenta nativa de imagem e congelado como entrada;
a composição e a tipografia Inter são determinísticas. Não existe um SVG da
ilustração completa. A [proveniência](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/src/PROMPT_FUNDO.md) e a
[licença Inter](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/../licenses/Inter-OFL.txt) acompanham os arquivos.

## R0082

horizontal: preserva espaço para o conteúdo e permite leitura a partir de
720 px de largura sem reduzir o menor texto abaixo de 18 px.

## R0082

### Acessibilidade e contexto textual

## R0206

## Regeneração

Execute com o Node.js que tenha o pacote `sharp` disponível:

```powershell
node tools/readme_visuals/headers.mjs
node tools/readme_visuals/production.mjs --family all
node tools/readme_visuals/validate_production.mjs
```


## R0207

O código de composição fica em `tools/readme_visuals/`. Dependências, fontes e
ícones têm versões fixadas no lockfile; a tipografia dos SVGs é convertida em
paths para evitar substituição por fontes da máquina leitora.
