# Plano executável — READMEs com recursos visuais

Este plano transforma os cinco READMEs principais do ecossistema em uma
experiência editorial consistente no Git e no Databricks. O README da raiz e o
README de `.assistant/` formam uma única sprint de topo, embora sejam dois
arquivos físicos com públicos diferentes.

## Decisão arquitetural

Os recursos ficam em:

```text
ambiente_fonte/.assistant/hub_readmes_visual_assets/
```

O nome longo é intencional: o prefixo `hub_` marca uma extensão customizada, e
`readmes_visual_assets` restringe seu propósito aos recursos editoriais dos
READMEs. A pasta não é uma estrutura nativa da Databricks e não é descoberta
automaticamente pela Genie Code.

Cada conjunto separa:

- `sources/`: fontes SVG editáveis e versionáveis;
- `png/`: saídas rasterizadas referenciadas pelos READMEs e publicadas no
  workspace.

## Princípio visual

Cada gráfico precisa cumprir duas responsabilidades ao mesmo tempo:

1. **ser informativo**, tornando relações, hierarquias, sequências e decisões
   mais fáceis de compreender do que em prosa;
2. **ser visualmente bonito e estiloso**, com acabamento editorial suficiente
   para apoiar uma apresentação do projeto a outras pessoas e causar impacto
   sem parecer decorativo ou comprometer a precisão técnica.

Estética e informação não concorrem entre si: o impacto visual deve nascer da
hierarquia clara, do contraste, do ritmo, da consistência e da síntese correta.
Nenhuma informação essencial pode depender exclusivamente de cor ou imagem.

## Sistema comum

- tela horizontal de `1600 × 900`, adequada para leitura e apresentação;
- fundo escuro, grade discreta e cartões de alto contraste;
- rosa para extensões do Hub, azul para mecanismos nativos, amarelo para
  decisões humanas e verde para resultados/evidências;
- títulos e rótulos em PT-BR, com nomes técnicos preservados;
- texto alternativo e explicação equivalente no corpo do README;
- geração reproduzível por `tools/render_readme_visuals.mjs`.

## Sprint 1 — Hub Snippets

- substituir os três diagramas Mermaid por PNGs editoriais;
- explicar a pasta de objeto, o mapa funcional e o fluxo de uso;
- acrescentar o contrato de reuso: interface, execução e evidência;
- conferir imports e exemplos contra a API pública real.

## Sprint 2 — Hub Scripts

- substituir os quatro diagramas Mermaid por PNGs;
- diferenciar diagnóstico, política consumidora e enforcement;
- tornar os estados `PASS`, `WARN` e `FAIL` visualmente comparáveis;
- reforçar que o script mede e o fluxo consumidor decide.

## Sprint 3 — Agent Skills

- ilustrar descoberta por relevância e seleção explícita com `@`;
- separar método da skill e execução dos helpers;
- acrescentar a visão em três camadas: frontmatter, `SKILL.md` e recursos;
- manter explícito o limite entre mecanismo nativo e conteúdo customizado.

## Sprint 4 — Hub Prompts

- substituir os dois diagramas Mermaid por PNGs;
- acrescentar uma anatomia visual do briefing forte;
- mostrar a relação entre briefing, skill, Genie Code, helpers e entrega;
- preservar o checklist textual como contrato verificável.

## Sprint 5 — Topo do ecossistema

- alinhar `README.md` e `.assistant/README.md` sem criar duas verdades;
- substituir mapas, arquitetura, ciclo de vida e fluxo de contexto por PNGs;
- acrescentar no guia do workspace a escolha visual do ponto de partida;
- manter caminhos próprios para Git e workspace, porque os arquivos vivem em
  níveis diferentes.

## Gates de encerramento

1. renderizar todos os SVGs em PNG;
2. conferir dimensões, transparência, legibilidade e integridade dos arquivos;
3. validar links e ausência de Mermaid nos cinco READMEs;
4. executar `python tools/validate_assistant.py`;
5. regenerar `Novo_Ambiente_Simulado/` com a ferramenta oficial;
6. executar dry-run, publicar no Databricks via CLI e verificar o remoto.
