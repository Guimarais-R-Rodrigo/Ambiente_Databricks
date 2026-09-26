# Guia visual dos READMEs

## Objetivo

Criar diagramas tecnicamente precisos que também funcionem como peças de
apresentação. A figura deve reduzir esforço cognitivo e transmitir maturidade do
projeto antes mesmo da leitura detalhada.

## Semântica de cor

| Cor | Significado |
|---|---|
| azul | mecanismo ou superfície nativa da Databricks |
| rosa | conteúdo customizado pelo Hub |
| amarelo | decisão, revisão ou responsabilidade humana |
| verde | resultado, evidência ou conclusão verificável |
| violeta | método, preparação ou camada de apoio |

Rótulos e legendas acompanham as cores; cor isolada nunca define significado.

## Regras de composição

- Uma figura responde a uma pergunta central.
- Título afirma a mensagem; subtítulo delimita a leitura.
- Cartões usam frases curtas, não parágrafos reduzidos.
- Setas representam dependência ou sequência real.
- O corpo do README contém o equivalente textual da informação essencial.
- PNG é a saída publicada; SVG é gerado pelo código de composição, com Inter em paths.
- Arquétipos variam conforme a pergunta: atlas, corte, pista, dossiê, jornada,
  ponte, bancada ou storyboard. Não repetir caixas e setas como solução universal.
- Cabeçalhos usam arte raster decorativa e texto exato; não herdam a legenda
  operacional dos diagramas. O brilho fica longe da região de leitura.

## Regeneração

Execute com o Node.js que tenha o pacote `sharp` disponível:

```powershell
node tools/readme_visuals/headers.mjs
node tools/readme_visuals/production.mjs --family all
node tools/readme_visuals/validate_production.mjs
```
