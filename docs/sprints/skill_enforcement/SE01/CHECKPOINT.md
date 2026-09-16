# SE01 — checkpoint

## Veredito atual

**ABERTA / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE01 iniciou a camada L1 (`Contract`) do Skill Enforcement Framework na branch `sef/SE01-contrato`.

Contrato, suíte, renderer, CI, publicação/verify por conteúdo no Databricks Free, capability probe real e regressão natural da EDA possuem evidência positiva nos respectivos escopos. O fechamento ainda depende da decisão sobre remover/promover o probe, da entrada final no `CHANGELOG.md`, da reconciliação final com a `main`, dos gates finais da árvore de fechamento e do aceite explícito do usuário.

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
- [x] coerência de vocabulário entre JSON Schema e validator coberta por teste;
- [x] publicador Free compatibilizado com `import-dir` que já materializa notebooks;
- [x] fallback SOURCE preservado e coberto por teste;
- [x] fonte ↔ `Novo_Ambiente_Simulado` regenerada pelo renderer canônico;
- [x] branch reconciliada com `main@350dcf0b37e730042ef961f12f11b30b2660d2c6`, sem force-push, antes da publicação;
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
- [x] drift posterior da `main` classificado como ortogonal ao pacote publicado para fins dos testes comportamentais;
- [x] capability probe Run 1 executado em chat novo;
- [x] JSON bruto do mesmo Run 1 recuperado do canvas;
- [x] capability probe Run 1: **PASS**;
- [x] regressão natural SE00-P1 executada em outro chat novo;
- [x] routing natural da `hub-ml-eda-profissional`: observável;
- [x] regressão natural: **PASS — sem degradação material atribuível ao contrato/probe**;
- [x] limitações reais do Genie Code registradas;
- [ ] decisão consciente sobre remover/promover o capability probe temporário;
- [ ] entrada SE01 registrada no `CHANGELOG.md` antes do fechamento;
- [ ] reconciliação final com `main`;
- [ ] gates finais/CI da árvore de fechamento;
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

## Capability probe — Run 1

O prompt canônico foi enviado com seleção explícita de `@hub-ml-eda-profissional`. A cópia textual inicial perdeu o conteúdo rico do marcador e mostrou apenas `canvascanvas`, gerando classificação provisória `NOT_OBSERVABLE`.

O usuário então abriu o canvas da mesma execução e forneceu o JSON bruto:

```json
{
  "assistant_root_resolved": true,
  "import_target": "hub_snippets.constants.format_br.fmt_int",
  "marker": "SEF_CAPABILITY_PROBE_V0_1",
  "sample_result": "1.234",
  "status": "PASS",
  "writes_performed": false
}
```

Como a evidência adicional pertence ao mesmo Run 1 e satisfaz o marcador esperado, o veredito final é:

**Capability probe Run 1: PASS.**

Limitação da superfície: conteúdo rico de canvas pode não sobreviver à cópia textual e deve ser preservado visualmente quando necessário para auditoria.

## Regressão natural SE00-P1

O prompt natural congelado foi executado em outro chat novo. O trace observou roteamento para `hub-ml-eda-profissional` e carregamento da skill antes da construção do notebook.

Artefato auditado:

- `x1 - EDA NYC Taxi Trips.ipynb`;
- SHA-256: `49b21342ef27059124c12d5cf7d05ed9d6c5bd9a5bb12fc8f210e878a11c8fc4`;
- 109100 bytes;
- 16 células: 3 Markdown + 13 código;
- 13/13 células de código com output persistido;
- 0 outputs de exceção no notebook final;
- caminho pessoal hardcoded observado; por isso o notebook bruto não deve ser versionado.

### Aderência observada — contexto de audit, não enforcement

- `quick_profile`: called/completed;
- `null_summary`: called/completed;
- `data_quality_check`: não chamado; resumo manual usado no lugar;
- `smart_sample`: não chamado; `.sample(...).toPandas()` manual;
- `correlation_matrix`: não chamado; correlação pandas manual;
- `distribution_grid`: não chamado; bins/Plotly manuais;
- `safe_display`: não chamado; aplicabilidade não incluída na taxa comparável principal;
- templates individualmente carregados: **0/4 observáveis**.

No denominador diretamente comparável ao P1 da SE00, helper adherence melhora de **0/6 para 2/6 (33,3%)**. Reimplementações conservadoras caem para **4** e redundância conservadora para **>=3 padrões**, sem prova de enforcement.

### Qualidade analítica independente do gate de regressão

O notebook contém achados que impedem tratá-lo como entrega científica plenamente aprovada, embora não indiquem degradação causada pela SE01:

1. resumo Markdown fala em “milhões” quando a execução mostra 21.932 registros;
2. cita `payment_type`, `rate_code_id`, pedágios, gorjetas e coordenadas ausentes do schema observado;
3. recomenda `tarifa por milha` junto a possível previsão de tarifa, criando risco de leakage se `fare_amount` for target;
4. valida granularidade apenas procurando coluna com `id` no nome;
5. superestima qualidade a partir de nulos sem duplicidade/chave e consistência temporal completas;
6. mistura médias amostrais do `quick_profile` com resultados full-table sem rotular a população;
7. descreve visualizações como amostradas quando várias são agregações do dataset inteiro;
8. o trace mostra assinatura de helper inventada antes da inspeção correta da API;
9. caminho pessoal do workspace permanece hardcoded.

### Veredito

O objetivo desta regressão era detectar degradação material do uso normal da skill após a introdução do contrato/probe, não exigir enforcement novo.

**Regressão natural SE00-P1: PASS — nenhuma degradação material atribuível ao contrato/probe.**

Esse PASS não aprova o notebook cientificamente e não transforma `mode="audit"` em enforcement. Ele mostra que o fluxo natural continua funcional e apresenta melhora parcial de aderência em relação à SE00.

## Limitações reais consolidadas

1. script relativo da Agent Skill foi executável no cenário testado;
2. canvas pode ocultar evidência da cópia textual;
3. carregar skill não garante inspeção prévia correta das assinaturas;
4. carregar skill não garante chamadas de todos os helpers requeridos/condicionais;
5. templates continuam sem telemetria automática de consumo;
6. sem preflight/runner/receipt/postflight, omissões e reimplementações ainda chegam à conclusão normal;
7. qualidade analítica continua independente da aderência contratual.

## Drift posterior da main

Depois da certificação, a `main` avançou em frente V14 sem tocar o pacote operacional publicado. Isso não exigiu republicação antes dos testes comportamentais, mas a branch precisa ser reconciliada com a `main` vigente antes do fechamento/merge.

## Fronteira de escopo

Não implementado nesta sprint:

- preflight;
- runner determinístico;
- receipt;
- postflight;
- modo `WARN`/`ENFORCE`;
- mudança global em `.assistant_instructions.md`;
- generalização para outra skill;
- promoção ao workspace do trabalho.

## Próximos gates

1. decidir, com base no probe real, se o `capability_probe.py` temporário é removido ou promovido a componente diagnóstico definitivo;
2. registrar a entrada final SE01 no `CHANGELOG.md`;
3. reconciliar novamente com a `main` vigente;
4. atualizar snapshot/documentação se a reconciliação exigir;
5. reexecutar os gates finais e confirmar CI da árvore exata de fechamento;
6. pedir homologação explícita da SE01;
7. somente após aceite, integrar a PR #69.

SE02 permanece bloqueada até esse fechamento.