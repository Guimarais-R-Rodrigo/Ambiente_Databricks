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
- run `34845937711`: 5/5 V06, 364/364 regressões e 12/12 V00 **PASS**; o workflow reprovou somente porque o README raiz ainda continha métricas documentais anteriores.
- run `34846291082`: 5/5 V06, 364/364 regressões e 12/12 V00 **PASS**; a validação documental mediu `1383` links Markdown, `1339` arquivos de identidade e `1841` links fora da raiz, enquanto o README ainda registrava `1382`, `1334` e `1838`. A execução permanece **FAILURE** documental.

As correções mantêm essas execuções como reprovadas e não relaxam qualquer guarda.

## Aceite

Rodrigo concedeu aceite explícito de integração da V06 em 14/09/2026. O aceite cobre o merge Git somente após os checks verdes do head final; não equivale a publicação Databricks, homologação de navegador/runtime, acessibilidade, ACL real ou UAT e não inicia a V07.

## Pendências de fechamento

1. reconciliar as métricas do README raiz com a árvore final;
2. executar V06, regressões V01–V06, V00 e validador estrutural/documental na árvore final;
3. revisar diff final e sincronismo fonte/espelho;
4. abrir PR final e repetir os checks no head exato;
5. integrar somente com checks verdes e o aceite já registrado.

Browser/runtime Databricks, acessibilidade, UAT, ACL e publicação permanecem fora deste checkpoint.
