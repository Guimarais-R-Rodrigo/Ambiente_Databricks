# SE01 — resultados

## Estado

**EVIDÊNCIA LOCAL/CI E DATABRICKS FREE CERTIFICADAS; CAPABILITY PROBE RUN 1 = NOT_OBSERVABLE.**

Este arquivo recebe somente resultados realmente observados. Implementação, PR e autorrelato não são promovidos a evidência do Genie Code.

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

O README raiz registra esses valores medidos.

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
- ausentes antes da limpeza: **0**;
- conteúdo exportado/comparado: **550/550**;
- divergências de conteúdo observadas: **0**;
- arquivo gerenciado pela plataforma `.assistant/.mcp_servers.json`: reconhecido e permitido.

O primeiro verify corrigido encontrou um único objeto extra: `.assistant/EDA Profissional - NYC Taxi Trips`. O pacote publicado estava materialmente correto, mas o gate permaneceu FAIL por higiene de workspace até a identificação do extra.

## Identificação forense e limpeza do resíduo SE00

O objeto extra foi tratado fail-closed, sem remoção por nome apenas.

Evidência observada:

- caminho remoto: `.assistant/EDA Profissional - NYC Taxi Trips`;
- `object_type`: **NOTEBOOK**;
- linguagem: **PYTHON**;
- artefato histórico correspondente: `B00-P1-R1`, `EDA Profissional - NYC Taxi Trips.ipynb`;
- SHA-256 congelado na SE00: `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`;
- SHA-256 do export Jupyter remoto: `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`;
- identidade byte a byte: **PASS**;
- exclusão executada somente depois da coincidência de tipo + SHA: **PASS**.

O export forense, status remoto, verify pré-limpeza e verify final foram preservados localmente sob `.artifacts/sef/`, que é diretório ignorado pelo Git.

## Verify final do Databricks Free

Depois da remoção controlada do resíduo SE00, `tools/publicar_free.py --verify --conteudo` retornou:

- commit certificado: `637a4b38178c63ffee12ece801e847eedd83a054`;
- esperados: **550**;
- remotos: **551**, sendo 550 do pacote + 1 arquivo gerenciado pela plataforma;
- ausentes: **0**;
- obsoletos: **0**;
- skills: **14/14**;
- diretórios `hub_`: **5/5**;
- conteúdo: **550/550 exportados e comparados**;
- resultado: **APROVADO — 0 problema(s)**.

### Veredito do gate Free

**PASS — publicação e verify por conteúdo certificados no Databricks Free.**

Esse PASS certifica inventário, tipos e conteúdo do pacote publicado. Ainda não certifica execução previsível do script relativo pela Genie Code; esse é o capability probe seguinte.

## Drift da main após a certificação

Depois da certificação do pacote, a `main` avançou de `350dcf0b37e730042ef961f12f11b30b2660d2c6` para `e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`.

A comparação mostra apenas arquivos da frente V14 e documentação/CI associada:

- `.github/workflows/temas-v14-ci.yml`;
- `README.md` raiz;
- índices/documentação V14;
- `tools/tests/test_temas_v14_s0.py`.

Não houve alteração em `ambiente_fonte/.assistant`, `Novo_Ambiente_Simulado/Users/usuario-free`, `tools/publicar_free.py` ou nos artefatos SE01 publicados. Portanto, esse drift é classificado como **ortogonal ao pacote certificado** e não exige republicação antes do capability probe. A reconciliação final com a `main` permanece obrigatória antes do fechamento/merge.

## Capability probe no Free

### Run 1 — evidência conversacional

Em 16/09/2026, em chat novo informado pelo usuário, foi enviado o prompt canônico definido em `TESTES.md`, com seleção explícita de `@hub-ml-eda-profissional`.

A resposta da Genie Code afirmou, em sequência:

1. que carregaria a skill;
2. que localizaria o script;
3. que leria o script antes de executar;
4. que executaria o probe chamando sua função principal;
5. que o capability probe teria sido executado com sucesso.

No ponto em que a resposta anunciou `Segue o marcador JSON produzido integralmente`, o conteúdo bruto fornecido ao avaliador foi apenas:

```text
canvascanvas
```

Depois disso, a Genie Code resumiu narrativamente que:

- a raiz `.assistant` foi localizada;
- `hub_snippets.constants.format_br.fmt_int` foi importado;
- `fmt_int(1234)` retornou `"1.234"`;
- nenhuma escrita foi realizada;
- status declarado: `PASS`.

### Avaliação do Run 1

Critérios materiais do protocolo:

- skill explicitamente selecionada pelo prompt: **SIM**;
- alegação textual de leitura/execução do script: **SIM**;
- marcador JSON bruto `SEF_CAPABILITY_PROBE_V0_1`: **NÃO OBSERVADO**;
- `status = PASS` dentro do JSON bruto: **NÃO OBSERVADO**;
- `assistant_root_resolved = true` dentro do JSON bruto: **NÃO OBSERVADO**;
- `import_target = hub_snippets.constants.format_br.fmt_int` dentro do JSON bruto: **NÃO OBSERVADO**;
- `sample_result = 1.234` dentro do JSON bruto: **NÃO OBSERVADO**;
- `writes_performed = false` dentro do JSON bruto: **NÃO OBSERVADO**;
- tool trace/célula/execução material do `scripts/capability_probe.py`: **NÃO OBSERVADO na evidência textual recebida**;
- reimplementação manual: **NÃO PROVADA**;
- falha de execução do script: **NÃO PROVADA**.

**Veredito Run 1: `NOT_OBSERVABLE`.**

Racional: o protocolo proíbe promover autorrelato da LLM a evidência de execução. Os valores narrados são compatíveis com o resultado esperado, mas a resposta fornecida não preserva o JSON bruto nem um trace material que prove uso real do script relativo. A ausência dessa evidência também não prova que o script falhou; portanto o resultado não é `FAIL`.

Se a interface ainda expuser tool cards/trace da mesma execução, eles podem ser anexados como evidência adicional do mesmo run. Sem isso, um segundo run em chat novo deve repetir o prompt canônico e preservar visualmente qualquer tool trace/execução antes de copiar a resposta.

## Regressão de uso da EDA

- status: **PENDENTE**;
- prompt natural SE00-P1: congelado em `TESTES.md`;
- skill observada: —;
- degradação atribuível ao contrato/probe: —;
- veredito: **PENDENTE**.

## Regra

Não preencher lacunas por inferência. `NOT_OBSERVABLE` é resultado válido e distinto de `PASS`. O PASS de publicação não é promovido a PASS do capability probe e não prova aderência comportamental da Genie Code.