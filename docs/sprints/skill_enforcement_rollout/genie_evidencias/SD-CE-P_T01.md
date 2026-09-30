# SD-CE-P/T01 — snapshots sintéticos e cobertura de join — 2026-09-29

(Codex) O prompt e a resposta completos foram enviados diretamente nesta
conversa. Notebook exportado preservado em
`.artifacts/skills-delivery-evidence/genie-20260929-ce-p/8-original.ipynb`,
SHA256 `1ece701f9e20ecef3ef39a27d97122f4af6663465cc4211f8a5764481fd6f3a2`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário informou explicitamente que **nenhuma skill foi chamada**. O próprio
texto do Genie disse “No skill needed”.

## Vereditos separados

- Roteamento: **FAIL**. O pedido avaliava cobertura e viabilidade de join
  entre duas fontes, demanda atribuída a `hub-ml-cross-eda-ml` pela instrução
  geral e pelo roteiro. A resposta não carregou essa skill nem seguiu seu
  contrato; classificou a tarefa como simples apesar de criar notebook e
  executar Spark.
- Oráculo de dados: **PASS**. O notebook tem três células de código com outputs:
  âncora `a,b,c` únicos, atributos `a,b` únicos; `2/3` cobertos e `1/3` sem
  atributo (`c`), nenhuma chave órfã e zero duplicatas em atributos.
  A conclusão de ausência de fan-out nos dados presentes é correta. Não há
  criação de tabela persistente no código exportado.
- Execução: **OBSERVED para notebook exploratório Spark**, pelos outputs
  exportados. **NOT_RUN para a rota canônica Cross-EDA**: não há
  `run_diagnostic.py`, contexto/hashes, Receipt ou `verify_diagnostic.py`.
  Outputs do notebook não podem ser promovidos a verificação canônica.
- Precisão: o texto chama crescimento de cobertura de `2` para `3` linhas
  em inner join de “fator de expansão potencial”; isso é inclusão de um novo
  ID, não fan-out. Com âncora única e duplicação apenas em atributos, o join
  passaria a `1:N`, não necessariamente `N:N`. Essas imprecisões não alteram
  os números da fixture nem justificam alegação de cardinalidade validada
  fora dela.

**Veredito T01: FAIL de roteamento/aderência canônica, com cálculo local
correto.** O texto publicado já aponta Cross-EDA para viabilidade de joins;
esta coleta não motivou edição de produto/publicação. Reteste eventual deve
preservar T01 e separar indicação @ de roteamento espontâneo.
