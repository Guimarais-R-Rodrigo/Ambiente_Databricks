# Checkpoint V06 — assets e geração

## Base e isolamento

- base de criação: `main` em `d728b872c77c89723a016919bd80534fb297b488`;
- branch de desenvolvimento: `codex/temas-v06-assets-geracao-20260914`;
- head final validado: `70499e1803ce0d61a148a0da975c4f52611046e0`;
- PR de integração: #38;
- merge efetivo na `main`: `418946de8d1e95e87cbfd9df528ddcced5075237`;
- árvore do head final e do merge: `68ddec3d691047e890ba2785e1e2e007039fa0e3`;
- nenhuma publicação Databricks foi feita;
- a V07 não foi iniciada.

## Decisão arquitetural

A V06 evolui o compositor v2 existente. `ResolvedTheme` permanece fonte de verdade; `theme_bridge.py` emite apenas um derivado controlado e `theme_assets.mjs` usa o renderer existente. Não existe novo catálogo de tema em YAML/JSON dentro da pipeline de assets.

O pacote ativo não é destino de geração V06. Variantes ficam em `.artifacts`; bytes congelados são conferidos antes da renderização e qualquer divergência paramétrica é marcada para revisão, nunca promovida automaticamente.

## Evidências históricas preservadas

- run `34845378370`: **FAILURE** antes dos testes; `setup-node` solicitou cache de pnpm antes de o executável existir.
- run `34845593931`: **FAILURE** antes dos testes; o `pnpm-workspace.yaml` legado não declarava o pacote raiz.
- run `34845754341`: suíte V06 **5/5 PASS**, mas a regressão agregada falhou porque o workflow ainda não havia instalado `plotly`/`pandas`; foi um defeito do ambiente do novo gate, não uma falha dos contratos V06.
- run `34845937711`: V06 **5/5**, regressões V01–V06 **364/364** e V00 **12/12 PASS**; o workflow reprovou somente porque o README raiz ainda continha métricas documentais anteriores.
- run `34846291082`: V06 **5/5**, regressões **364/364** e V00 **12/12 PASS**; a validação documental mediu `1383` links Markdown, `1339` arquivos de identidade e `1841` links fora da raiz, enquanto o README ainda registrava valores anteriores. A execução permanece **FAILURE** documental.
- run `34847723861`: permanece **FAILURE** histórico; não foi reclassificado.
- run `34848445012`: **FAILURE** no CI geral porque a descoberta cumulativa passou a executar V06 sem as dependências Node/compositor preparadas.
- runs `34848898532` (V04) e `34848898536` (V05): **FAILURE** na regressão cumulativa pela mesma ausência de pré-requisito Node; as suítes específicas anteriores permaneceram separadas dessa causa.

As correções mantêm essas execuções como reprovadas e não relaxam qualquer guarda.

## Correção final de ambiente

O head intermediário `dd40fcd2b55a6c8bca0a84d8076c70605a5b93ac` preparou Node 22, `pnpm@10.34.5` e dependências do compositor no CI geral, além de fazer `ci_local.py` conferir explicitamente os pré-requisitos Node sem instalá-los silenciosamente.

O head final `70499e1803ce0d61a148a0da975c4f52611046e0` corrigiu também V04 e V05 para preservar a descoberta cumulativa `test_temas*.py` até V06. Nenhum teste foi filtrado ou removido para obter verde.

## Validação do head final

No head final da PR #38, concluíram com `success`:

- `34849332915` — Regressões da instrumentação V00;
- `34849332504` — Contrato de temas V01;
- `34849332510` — Núcleo de temas V02;
- `34849332547` — Componentes HTML e tabelas V04;
- `34849332540` — Visual Lab notebook V05;
- `34849332509` — Assets e geração V06;
- `34849332601` — CI local reproduzível.

A suíte V06 permaneceu em **5/5**, a descoberta cumulativa V01–V06 em **364/364** e a compatibilidade visual V00 em **12/12**. O validador estrutural/documental e o escopo também passaram.

## Verificação pós-merge

O merge `418946de8d1e95e87cbfd9df528ddcced5075237` preserva exatamente a árvore testada do head final. Após o push na `main`, oito workflows concluíram com `success`:

- `34849703278` — V00;
- `34849703186` — V01;
- `34849703185` — V02;
- `34849703168` — V03;
- `34849703237` — V04;
- `34849703178` — V05;
- `34849703234` — V06;
- `34849703315` — CI local reproduzível.

O job V06 pós-merge executou dependências, suíte específica, regressões V01–V06, V00, validação estrutural/documental e escopo. O CI geral preparou Node e compositor antes de executar o gate sem credenciais.

## Aceite

Rodrigo concedeu aceite explícito de integração da V06 em 14/09/2026. O aceite cobriu a integração Git depois dos checks verdes do head final; não equivale a publicação Databricks, homologação de navegador/runtime, acessibilidade, ACL real ou UAT e não inicia a V07.

## Estado de fechamento

Os itens que antes eram pendências de fechamento foram concluídos:

1. métricas do README raiz reconciliadas pelo validador;
2. suíte V06, regressões V01–V06, V00 e validação estrutural/documental verdes na árvore final;
3. diff final e sincronismo fonte/espelho revisados;
4. PR #38 validada no head exato `70499e18...`;
5. integração concluída no merge `418946de...` e oito workflows pós-merge verdes.

Browser/runtime Databricks, acessibilidade, UAT, ACL, promoção visual e publicação permanecem fora deste fechamento. A V07 não foi iniciada.
