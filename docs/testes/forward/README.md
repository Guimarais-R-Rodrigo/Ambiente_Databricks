# Forward tests das Agent Skills

Forward test mede **roteamento**: diante de um pedido, qual skill o Genie Code
carrega? A relevância considera o pedido e a `description` da skill; `@menção`
permite seleção explícita.

Ele não mede qualidade da resposta nem execução de código.

## Matriz por skill

| Caso | Pergunta | PASS |
|---|---|---|
| positivo (`P`) | demanda típica carrega a skill alvo? | alvo carregada |
| negativo (`N`) | demanda vizinha deixa a skill alvo de fora? | alvo não carregada |
| menção (`M`) | `@nome-da-skill` seleciona explicitamente? | alvo carregada |

A matriz histórica deste protocolo prevê 14 skills × 3 casos = 42. Os casos 14P/14N/14M
foram acrescentados para o Concierge, mas ainda não foram executados. Os negativos
cobrem colisões como drift, materialização, explicação de notebook e auditoria.
A matriz detalhada do Concierge, em seu pacote canônico, acrescenta casos de qualidade
e segurança; ela não equivale a 26 forward tests aprovados.

## Evidência histórica preservada — conjunto anterior

| Escopo | Resultado | Situação |
|---|---:|---|
| 12 skills originais | **36/36 PASS** | fechado |
| `hub-ml-criar-objeto` | **3/3 PASS** | fechado em 09/09 |
| conjunto anterior | **39/39 PASS** | histórico; não homologa o conjunto ampliado |

O caso `11N-r2` foi aprovado no critério do teste — a skill alvo ficou de fora
—, embora a skill ideal também não tenha sido carregada. É item de vigilância,
não motivo para reclassificar o resultado.

O [catálogo corrente](../../../ambiente_fonte/.assistant/skills/README.md) inclui Micromodelos, adicionada depois desse protocolo. As [evidências Micromodelos](../../sprints/micromodelos/README.md) e os [screenings SER/B1](../../sprints/skill_enforcement_rollout/README.md) têm seus próprios casos. Não inferir 45/45 a partir de 39/39, da matriz 42 ou de outra campanha.

## Estado da integração — 12/09/2026

Concierge integrado ao Git; seus casos básicos e a matriz detalhada permanecem
PENDENTES no Genie Code. Reexecute também as vizinhas e os casos afetados pelo
mapa de instruções atualizado. Sem nova evidência, não declare 42/42 nem
homologação de todo o catálogo. A matriz detalhada vive no
[pacote canônico](../../../ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/README.md).

## Executar uma rodada

1. Abra [`roteiro.md`](roteiro.md).
2. Use um chat novo para cada caso.
3. Anexe qualquer artefato exigido pelo prompt.
4. Envie as duas mensagens do caso sem alterar o vocabulário.
5. Registre skill carregada, ausência e observação.
6. Copie [`template_resultados.md`](template_resultados.md) para
   `resultados/<YYYY-MM-DD>_rodada<N>.md`.

Se o Genie Code não permitir envio, registre a tentativa como bloqueada e não
invente veredito.

## Rodadas

| Data | Rodada | Resultado | Leitura |
|---|---|---:|---|
| 2026-08-14 | [1](resultados/2026-08-14_rodada1.md) | 33 PASS, 2 FAIL, 1 sem registro | falhas concentradas em prompts sem artefato anexado |
| 2026-08-14 | [2](resultados/2026-08-14_rodada2.md) | 5 PASS | prompts autocontidos confirmaram defeito do instrumento |
| 2026-08-29 | tentativa | sem casos enviados | [cota bloqueada](../2026-08-29_execucao-etapas-1-a-5.md) |
| 2026-09-09 | [3](resultados/2026-09-09_rodada3.md) | 3/3 PASS | skill 13 fechada; total 39/39 |

Nenhuma `description` foi alterada por causa da rodada 1: a rodada 2 isolou que
o problema estava no instrumento. Antes de editar uma `description`, leia o
[handoff de calibração](../../handoffs/2026-08-14_calibracao-descriptions.md).

## Critério de reabertura

Repita pelo menos os casos da skill e das vizinhas quando mudar:

- `name` ou `description`;
- fronteira temática;
- exemplo que altera o vocabulário esperado;
- estrutura/path de descoberta.

Mudança apenas editorial no corpo, sem alterar escopo, ainda exige revisão, mas
não invalida automaticamente todos os 39 casos.

[Voltar ao índice de testes](../README.md)
