# SE01 — resultados

## Estado

**EVIDÊNCIA LOCAL/CI, DATABRICKS FREE E CAPABILITY PROBE CERTIFICADAS; REGRESSÃO NATURAL SE00-P1 = PASS SEM DEGRADAÇÃO MATERIAL.**

Este arquivo recebe somente resultados realmente observados. Implementação, PR e autorrelato não são promovidos a evidência do Genie Code sem material observável.

## Candidata observada

- branch: `sef/SE01-contrato`;
- commit publicado e certificado no Databricks Free: `637a4b38178c63ffee12ece801e847eedd83a054`;
- base reconciliada antes da publicação: `main@350dcf0b37e730042ef961f12f11b30b2660d2c6`;
- PR: #69, Draft;
- skill piloto: `hub-ml-eda-profissional`;
- modo do contrato: `audit`.

## Evidência estática e CI do HEAD publicado

No HEAD `637a4b38178c63ffee12ece801e847eedd83a054`:

- contrato v0.1: **PASS — 1/1 contrato válido**;
- recursos declarados: **10**;
- templates declarados: **4**;
- suíte `test_skill_enforcement_se01.py`: **14/14 PASS**;
- capability probe local read-only: **PASS**;
- compatibilidade do publicador, notebook já materializado: **PASS**;
- compatibilidade do publicador, fallback SOURCE: **PASS**;
- `validate_assistant.py --conferir-readme`: **APROVADO — 0 falhas / 0 avisos**;
- renderer canônico: **sem diff**;
- GitHub Actions: **10/10 workflows aplicáveis em `success`**.

## Snapshot medido

A árvore reconciliada e publicada mantém:

- Markdown: **222 arquivos / 1396 links relativos**;
- Python AST: **222 arquivos**;
- repo identidade: **1495 arquivos**;
- repo links: **1962**;
- worktree extras: **0**;
- instruções: **9043/20000 caracteres**.

## Incidente de compatibilidade do publicador — histórico preservado

A primeira execução real do `tools/publicar_free.py --execute` materializou a árvore pelo `workspace import-dir --overwrite`. A segunda fase histórica tentou reenviar individualmente o primeiro notebook didático como `SOURCE` e recebeu `PROTOCOL_ERROR`.

O diagnóstico controlado observou:

- o destino sem extensão já existia como `object_type=NOTEBOOK`, `language=PYTHON`;
- o caminho equivalente com `.py` não existia;
- o reenvio individual redundante falhou **3/3** com o mesmo `PROTOCOL_ERROR`.

A correção passou a consultar `workspace get-status` depois do `import-dir`: notebook já materializado é preservado; caso contrário, o fallback `SOURCE/PYTHON/--overwrite` permanece disponível. A suíte cobre os dois caminhos.

## Publicação corrigida no Databricks Free

Em 16/09/2026, o HEAD `637a4b38178c63ffee12ece801e847eedd83a054` foi publicado no workspace pessoal/Free com o publicador corrigido.

Resultados observados:

- dry-run: **PASS**;
- arquivos publicáveis: **550**;
- fonte ↔ simulado: **em dia**;
- `workspace import-dir --overwrite`: **PASS**;
- notebooks já materializados pelo `import-dir`: **80**;
- reenvios redundantes desses notebooks: **0**;
- inventário do pacote: **14/14 skills**;
- diretórios `hub_`: **5/5**;
- conteúdo exportado/comparado: **550/550**;
- divergências de conteúdo observadas: **0**;
- arquivo gerenciado pela plataforma `.assistant/.mcp_servers.json`: reconhecido e permitido.

O primeiro verify corrigido encontrou um único objeto extra: `.assistant/EDA Profissional - NYC Taxi Trips`, resíduo histórico da SE00. O objeto foi tratado fail-closed:

- `object_type`: **NOTEBOOK**;
- linguagem: **PYTHON**;
- artefato histórico correspondente: `B00-P1-R1`;
- SHA-256 congelado na SE00: `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`;
- SHA-256 do export Jupyter remoto: `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`;
- identidade byte a byte: **PASS**;
- exclusão executada somente depois da coincidência de tipo + SHA: **PASS**.

Depois da remoção controlada, `tools/publicar_free.py --verify --conteudo` retornou:

- esperados: **550**;
- remotos: **551**, sendo 550 do pacote + 1 arquivo gerenciado pela plataforma;
- ausentes: **0**;
- obsoletos: **0**;
- skills: **14/14**;
- diretórios `hub_`: **5/5**;
- conteúdo: **550/550 exportados e comparados**;
- resultado: **APROVADO — 0 problema(s)**.

**Gate Databricks Free: PASS.**

## Drift da main após a certificação

Depois da certificação do pacote, a `main` avançou da base reconciliada. A comparação feita antes dos testes comportamentais mostrou somente arquivos da frente V14 e documentação/CI associada, sem alteração em `ambiente_fonte/.assistant`, `Novo_Ambiente_Simulado/Users/usuario-free`, `tools/publicar_free.py` ou no capability probe publicado. O drift foi classificado como ortogonal ao pacote certificado; a reconciliação final permanece obrigatória antes do fechamento/merge.

## Capability probe no Free

### Run 1 — evidência inicial e complemento do canvas

Em 16/09/2026, em chat novo informado pelo usuário, foi enviado o prompt canônico com seleção explícita de `@hub-ml-eda-profissional`.

A resposta da Genie Code afirmou que carregaria a skill, localizaria e leria `scripts/capability_probe.py` e executaria sua função principal. Na cópia textual inicial, o ponto em que deveria aparecer o marcador bruto foi representado apenas por `canvascanvas`; por isso a classificação **provisória** baseada somente naquele texto foi `NOT_OBSERVABLE`.

Em seguida, o usuário abriu o canvas da mesma execução e forneceu o conteúdo bruto que estava oculto na transcrição textual:

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

Essa evidência adicional pertence ao **mesmo Run 1**; não é um rerun e não reescreve a observação inicial. Ela complementa a superfície que a cópia textual não preservou.

Critérios finais do Run 1:

- skill explicitamente selecionada: **SIM**;
- script relativo declarado como localizado/lido/executado: **SIM**;
- marcador bruto `SEF_CAPABILITY_PROBE_V0_1`: **OBSERVADO**;
- `status = PASS`: **OBSERVADO**;
- `assistant_root_resolved = true`: **OBSERVADO**;
- `import_target = hub_snippets.constants.format_br.fmt_int`: **OBSERVADO**;
- `sample_result = 1.234`: **OBSERVADO**;
- `writes_performed = false`: **OBSERVADO**;
- reimplementação manual: **não observada**;
- EDA iniciada indevidamente durante o probe: **não**.

**Veredito final do capability probe Run 1: `PASS`.**

Limitação observacional registrada: o JSON foi renderizado em canvas e desapareceu da cópia textual como `canvascanvas`. Para auditorias futuras, evidência visual/canvas deve ser preservada quando a superfície textual não serializar o conteúdo rico.

## Regressão natural de uso da EDA — SE00-P1

Em outro chat novo, foi repetido o prompt natural congelado da SE00-P1, sem instruções adicionais sobre helpers, templates ou enforcement. O usuário forneceu o trace/pensamento da Genie Code e o notebook final `x1 - EDA NYC Taxi Trips.ipynb`.

### Identificação do artefato

- notebook: `EDA NYC Taxi Trips`;
- arquivo recebido: `x1 - EDA NYC Taxi Trips.ipynb`;
- tamanho observado: **109100 bytes**;
- SHA-256 observado: `49b21342ef27059124c12d5cf7d05ed9d6c5bd9a5bb12fc8f210e878a11c8fc4`;
- estrutura: **16 células — 3 Markdown e 13 de código**;
- células de código com output persistido: **13/13**;
- outputs de exceção persistidos no notebook final: **0**;
- janela persistida das células finais executadas: aproximadamente `2026-09-16T18:34:13Z` a `2026-09-16T18:39:00Z`;
- notebook bruto não deve ser versionado porque contém caminho pessoal de workspace hardcoded; integridade preservada pelo SHA-256 acima.

### Roteamento e carregamento

O trace observa explicitamente a correspondência do pedido com `hub-ml-eda-profissional`, a decisão de carregar a skill antes das ferramentas e a confirmação subsequente de que a skill foi carregada.

**Routing natural: PASS / OBSERVÁVEL.**

Isso é uma melhora de observabilidade em relação à baseline SE00-P1, na qual 3/3 runs ficaram `NOT_OBSERVABLE` para routing.

### Recursos do contrato observados

Estado por recurso relevante:

| Recurso | Política | Aplicabilidade observada | Estado máximo observado |
|---|---|---|---|
| `quick_profile` | required | sim | **called/completed** |
| `data_quality_check` | required | sim pelo contrato | **read/considered, não chamado; substituído por resumo manual** |
| `null_summary` | required | sim | **called/completed** |
| `smart_sample` | conditional | sim — houve amostra local para correlação | **não chamado; `.sample(..., seed=42).toPandas()` manual** |
| `correlation_matrix` | conditional | sim — >=2 numerais relevantes | **não chamado; `pandas.corr()` manual** |
| `distribution_grid` | conditional | sim — distribuições foram solicitadas/produzidas | **não chamado; bins/Plotly manuais** |
| `safe_display` | conditional | ambígua para o denominador comparável — os displays foram majoritariamente agregados/helpers, não preview de linhas brutas | **não chamado** |
| `theme_plotly` | conditional | não — nenhum `ResolvedTheme` selecionado | `not_applicable` |
| `index_generator` | optional | fora do denominador | não usado |
| `format_br` | optional | fora do denominador | não usado |

No conjunto diretamente comparável aos seis recursos usados como denominador no P1 da SE00, a aderência observada sobe de **0/6 para 2/6 (33,3%)**. Se `safe_display` for considerado aplicável pela existência de previews tabulares, o denominador formal seria 2/7; por conservadorismo comparativo, ele permanece fora da taxa principal e registrado separadamente.

A melhora é real, mas **não equivale a enforcement** e não satisfaz o contrato inteiro.

### Templates

O trace mostra carregamento da skill, mas não preserva evidência de leitura individual dos quatro templates. Como houve visual diagnostics, os quatro são materialmente relevantes (`roteiro_eda`, `relatorio_executivo_eda` required; `matriz_graficos_eda` e `estilo_visual_eda` conditional).

- templates aplicáveis: **4**;
- carregamentos individualmente comprovados: **0/4**;
- resultado: **NOT_OBSERVABLE**.

Sem trace de `loaded`, semelhança estrutural do notebook não é promovida a consumo comprovado.

### Reimplementação e redundância

Reimplementações/omissões canônicas observadas, de forma conservadora:

1. `data_quality_check` requerido foi pulado e substituído por resumo manual;
2. `smart_sample` foi substituído por `.sample(...).toPandas()`;
3. `correlation_matrix` foi substituído por `pandas.corr()`;
4. `distribution_grid` foi substituído por agregações/bins + Plotly manuais.

Total conservador: **4**. Se `safe_display` for considerado aplicável, há uma quinta substituição por `display()` direto.

Redundância conservadora observada:

1. `df.count()` antes de `quick_profile`, que volta a fornecer row count;
2. null analysis completa pelo `quick_profile` seguida de nova execução via `null_summary`;
3. zeros/negativos calculados por múltiplas ações `filter(...).count()` separadas.

Total conservador: **>=3 padrões**. É melhora frente aos P1 da SE00 (`>=4` a `>=8` por run), mas ainda há computação evitável.

### Achados analíticos e documentais do notebook

O notebook é funcional e cobre o pedido em linhas gerais, mas mantém problemas materiais independentes do teste de degradação:

1. **Alto — resumo persistido contradiz o próprio output:** afirma que a base contém “milhões de registros”, enquanto o inventário executado mostra **21.932**.
2. **Alto — referências a colunas inexistentes:** o resumo pede validar `payment_type`/`rate_code_id` e atribui variabilidade a pedágios/gorjetas, embora o schema observado tenha somente timestamps, `trip_distance`, `fare_amount`, `pickup_zip` e `dropoff_zip`.
3. **Alto — risco de leakage na recomendação:** recomenda `tarifa por milha` como feature e, no mesmo handoff, sugere modelagem para previsão de tarifa sem separar os cenários; se `fare_amount` for target, essa feature contém diretamente o target.
4. **Médio/alto — granularidade/chave não foi validada:** a lógica procura apenas colunas cujo nome contenha `id`; ausência desse nome não prova inexistência de chave candidata nem que cada linha represente inequivocamente uma viagem única.
5. **Médio/alto — qualidade superestimada:** o fluxo destaca zero nulos e declara qualidade forte, mas não executa `data_quality_check`, não mede duplicidade com chave candidata, não valida consistência pickup→dropoff/duração e já observa tarifas negativas e distâncias zero.
6. **Médio — mistura de população:** a resposta final usa médias de `quick_profile` calculadas na amostra (2,91 milhas; 12,41) sem rotulá-las como amostrais, embora o resumo full-table mostre médias ~2,85 e ~12,35. A própria skill exige preservar a distinção full-table versus sample.
7. **Médio — resumo descreve coordenadas que não existem no schema:** recomenda engenharia geoespacial “a partir de coordenadas”, mas a fonte observada contém ZIP codes, não latitude/longitude.
8. **Médio — descrição de amostragem é imprecisa:** o Markdown diz que “visualizações e correlações” usam amostras; as distribuições e séries temporais são agregações do conjunto completo, enquanto apenas a correlação usa amostra local explícita.
9. **Médio — assinatura de helper foi inventada antes da inspeção:** o trace mostra tentativa inicial incorreta de `quick_profile(df=...)`; a implementação só foi lida depois do erro. O mesmo padrão ocorreu com `data_quality_check`. A instrução da skill era verificar API antes de inventar assinatura.
10. **Governança/portabilidade — caminho pessoal hardcoded:** o notebook adiciona `.assistant` ao `sys.path` por um caminho pessoal fixo, reproduzindo uma fragilidade já observada na SE00.

### Veredito da regressão natural

O objetivo deste gate era detectar se adicionar contrato/probe degradou materialmente o carregamento/uso normal da skill; ele **não** exigia enforcement novo.

Evidência positiva:

- routing natural da skill tornou-se observável;
- notebook foi concluído e executado sem exceção persistida;
- `quick_profile` e `null_summary` foram chamados/concluídos;
- agregações Spark foram usadas para as visualizações principais;
- amostra da correlação teve seed explícita;
- houve melhora material de aderência e redução de reimplementação/redundância frente à SE00-P1.

Evidência negativa, mas não atribuível a degradação causada pela SE01:

- contrato continua apenas parcialmente seguido;
- templates continuam sem prova de carregamento;
- erros analíticos/documentais permanecem;
- não existe Receipt/Postflight que impeça conclusão com obrigações não cumpridas.

**Veredito da regressão natural SE00-P1: `PASS — nenhuma degradação material atribuível ao contrato/probe`.**

Esse PASS **não** é PASS de enforcement nem aprovação científica integral do notebook. Ele confirma somente que a introdução do contrato v0.1 e do capability probe não quebrou o uso natural da skill e produziu sinais de melhora de aderência.

## Limitações reais do Genie Code observadas na SE01 até aqui

1. scripts relativos de Agent Skill são executáveis no cenário testado e o probe conseguiu importar API pública/retornar marcador;
2. conteúdo rico em canvas pode não sobreviver à cópia textual (`canvascanvas`), exigindo preservação visual para auditoria;
3. carregar a skill e declarar recursos não garante verificar assinaturas antes de gerar código;
4. carregar a skill não garante chamada de todos os helpers required/conditional;
5. carregar a skill não deixa prova automática de consumo dos templates;
6. sem preflight/runner/receipt/postflight, reimplementações e omissões continuam possíveis mesmo em `mode="audit"`;
7. qualidade analítica continua independente da aderência ao contrato.

## Regra

Não preencher lacunas por inferência. `NOT_OBSERVABLE` continua distinto de `PASS`. O PASS do probe e o PASS da regressão têm escopos diferentes: nenhum deles autoriza declarar enforcement implementado.