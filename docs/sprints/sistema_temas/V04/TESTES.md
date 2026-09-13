# V04 — testes e evidências

Este arquivo registra execuções da V04 sem transformar tentativa anterior em
aprovação posterior. Runs repetidos não são somados como novos casos.

## Code-check transitório 1 — `34726526972`

**Resultado: FAILURE.**

O run executou com Python 3.12 e dependências declaradas. Os resultados foram:

| Bloco | Resultado |
|---|---|
| V04 | 29/29 PASS |
| Temas V01–V04 | 298/298 PASS |
| Regressão visual V00 | 12/12 PASS |
| `validate_assistant.py` | FAILURE |

A validação encontrou duas causas:

1. o workflow transitório usava checkout raso, enquanto o contrato de migração
   dos READMEs exige histórico completo;
2. `get_styles_resolvidos` passou a ser função pública, mas o notebook
   `exemplo_styles.py` ainda não a exercitava, violando a guarda permanente de
   notebooks de exemplo.

A primeira causa era do próprio instrumento de teste. A segunda era uma dívida
real da implementação e foi corrigida no notebook. Nenhum desses itens foi
ignorado, transformado em warning ou removido do gate.

## Code-check transitório 2 — `34726621227`

**Resultado: SUCCESS.**

O checkout passou a usar histórico completo e o notebook foi atualizado para
exercitar a nova API. Na mesma rodada:

| Bloco | Resultado |
|---|---|
| V04 | 29/29 PASS |
| Temas V01–V04 | 298/298 PASS |
| Regressão visual V00 | 12/12 PASS |
| `validate_assistant.py` | PASS |

O workflow transitório foi removido da branch depois dessa verificação. Ele não
faz parte da candidata.

## Reconciliação com a R04-B — tentativa 1 `34726990399`

**Resultado: FAILURE.**

A `main` avançou durante a implementação pelo PR #18. Esta rodada comprovou que
o merge era limpo e que os dois lados estavam preservados: **15 caminhos V04** e
**43 caminhos efetivos R04-B** permaneceram byte a byte conforme suas origens.

O primeiro teste V04, porém, falhou no import público porque as novas funções de
`constants.styles` ainda não tinham sido materializadas no `__init__.py` da
árvore versionada; no code-check anterior a fachada era criada somente na
worktree. O run parou antes do Spark R04-B e nenhum commit reconciliado foi
enviado. A correção foi materializar as fachadas pela ferramenta canônica, não
relaxar o teste nem importar o módulo interno diretamente.

## Reconciliação com a R04-B — tentativa 2 `34727070003`

**Resultado: SUCCESS.**

A segunda rodada repetiu o merge a partir da mesma `main`
`d9da056c95bf5c4209b2f208de1c9a987580efe7`, gerou as sete fachadas V04 e
reexecutou os gates. Resultado:

| Bloco | Resultado |
|---|---|
| Preservação V04 | 15 caminhos preservados |
| Preservação R04-B | 43 caminhos preservados |
| V04 + regressões de temas | PASS |
| Regressão V00 | PASS |
| `validate_assistant.py` | PASS |
| R04-B com Java 17/PySpark 4.0.1/PyYAML 6.0.2 | 14/14 PASS, sem skip |
| Workflow transitório na árvore final | removido antes do commit |

A reconciliação foi congelada no commit
`c2b91c5e3a3d80f754045dfc4fae8eb335e31bef`. Esta execução Spark é evidência no
GitHub Actions e não deve ser chamada de homologação Databricks.

## O que os 29 testes V04 medem

Os casos específicos cobrem quatro grupos.

### Compatibilidade legada

- assinaturas públicas históricas;
- equivalência da configuração de referência com as constantes legadas;
- HTML de badges, divisores, KPI cards, cabeçalho e índice;
- equivalência semântica da tabela pandas, normalizando apenas o UUID aleatório
  do `Styler` e o alias de cor `white`/`#FFFFFF`.

### Propagação de tokens

- cor principal, texto e superfícies;
- dimensões de seção, card e badge;
- divisores;
- estados `ok`, `warn`, `fail` e fallback informativo;
- fonte do HTML;
- fundo/texto do cabeçalho da tabela e `semantic.negative`.

### Integridade/fail-closed

- dicionário cru recusado;
- contexto não-notebook recusado;
- fingerprint adulterado recusado;
- `_values` adulterado não contamina a saída canônica;
- dicionário de estilos é cópia isolada;
- Markdown resolvido continua revalidando o tema.

### Comportamento

- cortes de score não mudam;
- escape HTML continua ativo nos componentes que já o faziam;
- DataFrame de entrada é preservado;
- `dark` e `high_contrast` podem ser materializados no caminho HTML quando o
  tema completo é válido, sem declarar homologação de acessibilidade.

## Gates ainda exigidos antes do PR final

As rodadas acima foram intermediárias. A candidata final ainda precisa rodar,
na árvore que contém documentação, fachadas versionadas e espelho renderizado:

1. `python -B tools/tests/test_temas_v04.py -v`;
2. descoberta completa `test_temas*.py`;
3. V00;
4. `python -B tools/validate_assistant.py --conferir-readme`;
5. `python -B tools/ci_local.py --verbose`;
6. workflow permanente V04;
7. verificação do diff contra a `main` `d9da056c...`, comprovando que arquivos
   específicos R04-B não foram alterados pela V04.

## Não medido por estes runs

- renderização real no Databricks;
- contraste percebido, zoom ou leitor de tela;
- navegação/foco de interface;
- operação por usuário iniciante;
- publicação, rollback ou governança operacional;
- auditoria independente.

Esses itens permanecem PENDING/NOT TESTED, nunca PASS por inferência.
