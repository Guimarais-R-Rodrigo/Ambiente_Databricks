# FG-CC-A/T01 — Concierge por @ e moeda brasileira — 2026-09-30

(Codex) A resposta completa foi colada diretamente pelo usuário nesta conversa;
não houve export de notebook ou log de ferramentas. O usuário confirmou chat
novo, seleção de `@hub-ml-concierge` no menu e indicador de carregamento.
O texto de entrada colado começa com `hub-ml-concierge cierge`, diferente dos
bytes do prompt 14M preparado; esta é uma **variante semântica de 14M**, não
prova de execução literal do primeiro prompt histórico.

## Versão e evidência

O último pacote B1 conferido tinha hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
Houve publicação paralela posterior de micromodelos, relatada pelo usuário;
a versão remota efetiva desta conversa não foi conferida. A resposta cita
arquivo do workspace pessoal e linhas, mas não há eventos de leitura para
verificar que o Genie abriu esses bytes. O Codex conferiu **na fonte local**
`hub_snippets/constants/format_br/format_br.py` e `__init__.py`.

## Vereditos separados

- Seleção @: **PASS por relato humano de seleção e indicador**.
- Recomendação: **PASS**. `fmt_brl` é exportada por
  `hub_snippets.constants.format_br`; a implementação formata em reais com
  duas casas e `ROUND_HALF_UP`, preserva sinal negativo e retorna texto.
  Importar do pacote `format_br` é a rota pública correta. As demais
  funções citadas são complementares, não necessárias para moeda.
- Proveniência: **NOT_OBSERVABLE para leitura remota**. Os caminhos e linhas
  citados são afirmações da resposta. O código local confirma o conteúdo,
  mas não prova acesso do Genie ao arquivo remoto nem identidade de versão.
- Execução/efeitos: **NOT_RUN na evidência fornecida**. A resposta não alegou
  execução ou modificação; não há notebook ou saída de helper.

**Veredito T01: PASS da seleção explícita e da recomendação no escopo pedido.**
O literal 14M permanece não executado como tal, pois o texto de entrada
apresentado pelo usuário é uma variante. Nenhuma edição de produto ou
publicação foi feita nesta coleta.
