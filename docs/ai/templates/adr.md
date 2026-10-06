# Template de ADR

## Uso

Crie `docs/decisions/ADR-NNNN-<slug-curto>.md` com próximo número livre no índice;
atualize índice e changelog. Uma decisão por ADR; contexto factual, alternativas
com motivo e consequências. Data/autoria são reais. Redigir não equivale a
aprovar. Corpo aceito é imutável; anexar errata factual datada ou superseder por
novo ADR, sem reescrever história. [Regra](../rules/documentacao.md#manutencao).

Modelo não executável: `launchable=false`, `execution_authorized=false`.
Nenhum preenchimento concede acesso, execução, publicação ou aceite.

## Modelo

```markdown
# ADR-<NNNN> — <Título>

Data: <YYYY-MM-DD>
Status: Proposto
Autor: <pessoa/agente e sessão reais>
Aprovador e evidência: <PENDENTE ou referência verificável da decisão>
Supersede: <nenhum ou ADR e apenas os pontos afetados>
launchable=false
execution_authorized=false
Evidência de execução: NOT_RUN
Observabilidade do destino: NOT_OBSERVABLE

## Contexto
<Problema, fatos, fontes, baseline SHA e escopo.>

## Decisão
<Decisão única proposta e limites; autoridade necessária para aceitá-la.>

## Alternativas consideradas
- <Alternativa>: <motivo verificável da escolha/rejeição>.

## Consequências
- <Benefício, custo, dívida, risco residual e owner>.

## Verificação e reversão
<Tests/gates, evidência faltante, rollback e condição de parada.>

## Referências
- <Fontes e ADRs diretamente relacionados>.
```
