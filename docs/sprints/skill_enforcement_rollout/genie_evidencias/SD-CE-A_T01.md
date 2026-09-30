# SD-CE-A/T01 — corte de disponibilidade PIT — 2026-09-29

(Codex) Prompt e resposta completos foram enviados diretamente nesta
conversa. O usuário informou que selecionou `hub-ml-cross-eda-ml` no menu @
e que a skill carregou. Versão Free esperada: 657/657 arquivos conferidos,
hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.

## Vereditos separados

- Roteamento: **PASS por confirmação humana** da seleção e carregamento de
  Cross-EDA.
- Oráculo PIT conceitual: **PASS**. O atributo tem referência de 9/jan, mas
  disponibilidade em 11/jan. A resposta excluiu esse atributo da decisão de
  10/jan e o considerou elegível para a decisão de 12/jan. Distinguiu tempo
  do fato de tempo de disponibilidade e identificou leakage se a decisão
  anterior usasse o valor.
- Escopo: a resposta declarou explicitamente que era análise hipotética,
  sem preencher fonte real ou executar runner PIT. Não há payload, Receipt,
  verificador ou notebook executado nesta evidência; execução canônica
  **NOT_RUN**. A elegibilidade temporal de 12/jan não comprova, por si só,
  compatibilidade de chave/grão nem prontidão de join.
- Precisão textual: a resposta escreveu que o dado “ainda não existia” em
  10/jan; o fato pode existir desde 9/jan, mas ainda não estava disponível
  ao sistema decisório. A conclusão temporal continua correta. Há também
  um termo chinês isolado sem efeito técnico.

**Veredito T01: PASS conceitual de PIT e roteamento**, sem certificação de
execução ou homologação do perfil `LOCAL_SYNTHETIC_PIT_V1`. Nenhuma edição
de produto/publicação decorre desta coleta.
