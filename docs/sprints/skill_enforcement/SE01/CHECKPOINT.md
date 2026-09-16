# SE01 — checkpoint

## Veredito atual

**ABERTA / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE01 iniciou a camada L1 (`Contract`) do Skill Enforcement Framework na branch `sef/SE01-contrato`.

Contrato, suíte, renderer, CI e publicação/verify por conteúdo no Databricks Free possuem evidência positiva. O gate final continua aberto porque o capability probe real da Genie Code, a regressão natural da EDA, a decisão sobre o probe, o changelog final e o aceite explícito do usuário ainda estão pendentes.

## Estado implementado

- [x] branch SE01 criada da `main` vigente na abertura;
- [x] ADR-0021 proposta;
- [x] schema v0.1 definido;
- [x] contrato piloto da EDA em `mode="audit"`;
- [x] resolução estática de módulos/símbolos públicos;
- [x] resolução de templates relativos;
- [x] políticas do contrato confrontadas com o inventário congelado da SE00;
- [x] vocabulário fechado de conditions;
- [x] capability probe read-only criado;
- [x] testes positivos/negativos adicionados;
- [x] coerência JSON Schema ↔ validator coberta por teste;
- [x] publicador Free compatibilizado com `import-dir` que já materializa notebooks;
- [x] fallback SOURCE preservado e coberto por teste;
- [x] fonte ↔ `Novo_Ambiente_Simulado` regenerada pelo renderer canônico;
- [x] branch reconciliada com `main@350dcf0b37e730042ef961f12f11b30b2660d2c6`, sem force-push;
- [x] snapshot reconciliado: 1495 arquivos / 1962 links;
- [x] HEAD publicado `637a4b38178c63ffee12ece801e847eedd83a054` validado localmente: contrato 1/1, suíte 14/14, validador 0/0;
- [x] 10/10 workflows aplicáveis da PR no HEAD publicado: `success`;
- [x] autenticação do profile pessoal do Databricks CLI validada;
- [x] dry-run do publicador: 550 arquivos, espelho em dia;
- [x] publicação corrigida no Databricks Free concluída;
- [x] 80 notebooks reconhecidos como já materializados pelo `import-dir`;
- [x] conteúdo remoto exportado/comparado: 550/550 sem divergência;
- [x] resíduo SE00 identificado por `object_type=NOTEBOOK` + SHA-256 congelado;
- [x] resíduo SE00 removido somente após identidade byte a byte confirmada;
- [x] `--verify --conteudo` final no Free: **APROVADO — 0 problema(s)**;
- [ ] capability probe executado em chat novo;
- [ ] regressão natural SE00-P1 executada em chat novo;
- [ ] limitações reais do Genie Code registradas;
- [ ] decisão sobre remover/promover o probe;
- [ ] entrada SE01 registrada no `CHANGELOG.md` antes do fechamento;
- [ ] reconciliação final com `main` se ela avançar novamente;
- [ ] aceite explícito do usuário;
- [ ] merge da PR.

## Evidência técnica consolidada do HEAD publicado

No commit `637a4b38178c63ffee12ece801e847eedd83a054`:

- contrato: **1/1 PASS**;
- recursos: **10**;
- templates: **4**;
- suíte local/CI dirigida: **14/14 PASS**;
- schema ↔ validator: **PASS**;
- probe local read-only: **PASS**;
- compatibilidade do publicador, skip de reenvio redundante: **PASS**;
- compatibilidade do publicador, fallback SOURCE: **PASS**;
- `validate_assistant.py --conferir-readme`: **0 falhas / 0 avisos**;
- snapshot: **1495 arquivos / 1962 links / 0 extras**;
- GitHub Actions: **10/10 workflows aplicáveis em success**.

## Gate Databricks Free

A publicação corrigida observou:

- 550 arquivos publicáveis;
- `workspace import-dir --overwrite`: PASS;
- 80 notebooks já materializados corretamente;
- 14/14 skills presentes;
- 5/5 diretórios `hub_` presentes;
- 0 arquivos ausentes;
- 550/550 objetos exportados e comparados por conteúdo;
- 0 divergências de conteúdo.

O primeiro verify encontrou apenas `.assistant/EDA Profissional - NYC Taxi Trips`, resíduo do experimento SE00. A limpeza não foi feita por inferência nominal: o objeto remoto era `NOTEBOOK`, e o export Jupyter teve SHA-256 `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`, exatamente o SHA congelado de `B00-P1-R1`. Somente então o objeto foi removido.

O verify final retornou:

- esperados: **550**;
- ausentes: **0**;
- obsoletos: **0**;
- conteúdo: **550/550**;
- `.assistant/.mcp_servers.json`: reconhecido como gerenciado pela plataforma;
- resultado: **APROVADO — 0 problema(s)**.

**Gate Databricks Free: PASS.**

Esse PASS não prova execução do capability probe pela Genie Code. A prova comportamental continua separada.

## Fronteira de escopo

Não implementado nesta sprint:

- preflight;
- runner;
- receipt;
- postflight;
- modo `WARN`/`ENFORCE`;
- mudança global em `.assistant_instructions.md`;
- generalização para outra skill;
- promoção ao workspace do trabalho.

## Próximos gates

1. executar o capability probe em chat completamente novo do Genie Code;
2. classificar a evidência como `PASS`, `FAIL` ou `NOT_OBSERVABLE` sem inferência;
3. em outro chat completamente novo, executar a regressão natural SE00-P1;
4. registrar resultados e limitações reais do Genie Code;
5. decidir se o probe é removido ou promovido a componente definitivo;
6. registrar a entrada final SE01 no changelog;
7. reconciliar novamente com a `main` vigente se necessário;
8. reexecutar os gates finais da árvore de fechamento;
9. pedir homologação explícita da SE01;
10. somente após aceite, integrar a PR #69.

SE02 permanece bloqueada até esse fechamento.