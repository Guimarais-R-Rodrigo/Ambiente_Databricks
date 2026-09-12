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
deve fazer parte da candidata final.

## O que os 29 testes V04 medem

Os casos específicos cobrem quatro grupos:

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

O code-check foi uma etapa intermediária. A candidata final ainda precisa rodar,
na árvore que contém documentação, fachadas regeneradas e espelho renderizado:

1. `python -B tools/tests/test_temas_v04.py -v`;
2. descoberta completa `test_temas*.py`;
3. V00;
4. `python -B tools/validate_assistant.py --conferir-readme`;
5. `python -B tools/ci_local.py --verbose`;
6. workflow permanente V04;
7. verificação de diff contra a `main` para confirmar que a R04-A não foi
   modificada fora dos agregadores/documentos deliberados.

## Não medido por estes runs

- renderização real no Databricks;
- contraste percebido, zoom ou leitor de tela;
- navegação/foco de interface;
- operação por usuário iniciante;
- publicação, rollback ou governança operacional;
- auditoria independente.

Esses itens permanecem PENDING/NOT TESTED, nunca PASS por inferência.
