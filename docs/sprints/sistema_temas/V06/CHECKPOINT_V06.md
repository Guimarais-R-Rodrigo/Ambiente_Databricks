# Checkpoint V06 — assets e geração

## Base e isolamento

- base de criação: `main` em `d728b872c77c89723a016919bd80534fb297b488`;
- branch: `codex/temas-v06-assets-geracao-20260914`;
- `main` não recebeu commits V06 durante a execução;
- nenhuma publicação Databricks foi feita.

## Decisão arquitetural

A V06 evolui o compositor v2 existente. `ResolvedTheme` permanece fonte de verdade; `theme_bridge.py` emite apenas um derivado controlado e `theme_assets.mjs` usa o renderer existente. Não existe novo catálogo de tema em YAML/JSON dentro da pipeline de assets.

O pacote ativo não é destino de geração V06. Variantes ficam em `.artifacts`; bytes congelados são conferidos antes da renderização e qualquer divergência paramétrica é marcada para revisão, nunca promovida automaticamente.

## Evidências já observadas

- run `34845378370`: **FAILURE** antes dos testes; `setup-node` solicitou cache de pnpm antes de o executável existir.
- run `34845593931`: **FAILURE** antes dos testes; o `pnpm-workspace.yaml` legado não declarava o pacote raiz.
- run `34845754341`: 5/5 testes V06 **PASS**, mas a regressão agregada falhou porque o workflow ainda não havia instalado `plotly`/`pandas`; foi um defeito do ambiente do novo gate, não uma falha dos contratos V06.

As correções mantêm essas execuções como reprovadas e alinham o gate V06 ao conjunto de dependências já necessário às regressões V03–V05.

## Pendências de fechamento

1. concluir a regressão agregada com dependências completas;
2. executar V00 e validador estrutural/documental na árvore final;
3. reconciliar métricas do README raiz caso o validador detecte contagens desatualizadas;
4. revisar diff final e sincronismo fonte/espelho;
5. abrir PR draft e repetir os checks no head exato;
6. parar para aceite explícito antes de merge.

Browser/runtime Databricks, acessibilidade, UAT, ACL e publicação permanecem fora deste checkpoint.
