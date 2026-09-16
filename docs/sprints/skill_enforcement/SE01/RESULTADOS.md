# SE01 — resultados

## Estado

**EVIDÊNCIA LOCAL/CI REGISTRADA; PUBLICAÇÃO DATABRICKS FREE AINDA NÃO CERTIFICADA.**

Este arquivo recebe somente resultados realmente observados. Implementação, PR e autorrelato não são promovidos a evidência do Genie Code.

## Candidata observada

- branch: `sef/SE01-contrato`;
- commit que materializou fonte + simulado: `fda26d130e559d3fdb8ee69fcb785ffecc76a049`;
- commit de snapshot medido: `264981cb4ce1a5aff8d3c1f6dd54caa1fa57c174`;
- HEAD validado localmente pelo usuário antes do primeiro publish: `dc4059a3bd7c116bcf40009ec66b1da7a2f809fd`;
- candidata de compatibilidade do publicador: `77a26173e30929157216da3f9d6734cfa4018de3`;
- PR: #69, Draft;
- skill piloto: `hub-ml-eda-profissional`;
- modo do contrato: `audit`.

## Evidência estática confirmada

No workflow dedicado SE01 do commit `fda26d130e559d3fdb8ee69fcb785ffecc76a049`, antes do gate de snapshot:

- contrato v0.1: **PASS — 1/1 contrato válido**;
- recursos declarados: **10**;
- templates declarados: **4**;
- suíte `test_skill_enforcement_se01.py`: **11/11 PASS**;
- `validate_assistant.py`: **APROVADO — 0 falhas / 0 avisos**;
- renderer canônico: **limpo após materialização do espelho**.

Depois da inclusão do gate schema ↔ validator, a validação local do HEAD `dc4059a3bd7c116bcf40009ec66b1da7a2f809fd` confirmou:

- contrato: **1/1 PASS**;
- recursos: **10**;
- templates: **4**;
- suíte SE01: **12/12 PASS**;
- `test_schema_vocabularies_match_validator`: **PASS**;
- capability probe local read-only: **PASS**;
- `validate_assistant.py --conferir-readme`: **APROVADO — 0 falhas / 0 avisos**;
- worktree extras: **0**.

No mesmo HEAD `dc4059a3bd7c116bcf40009ec66b1da7a2f809fd`, os **10/10 workflows aplicáveis da PR concluíram em `success`**, incluindo `Skill Enforcement SE01`, `CI local reproduzível`, V00, V01, V02, V08, V10, V11, V12 e V13.

## Snapshot medido

A árvore validada mantém:

- Markdown: **222 arquivos / 1396 links relativos**;
- Python AST: **222 arquivos**;
- repo identidade: **1494 arquivos**;
- repo links: **1961**;
- worktree extras: **0**;
- instruções: **9043/20000 caracteres**.

O README raiz registra esses valores medidos.

## Incidente de publicação no Databricks Free

A autenticação do profile pessoal foi validada e o dry-run do publicador passou com:

- árvore publicável: **550 arquivos**;
- fonte ↔ simulado: **em dia**;
- destino pessoal explicitamente protegido por profile + expected-host.

Na primeira execução real do `tools/publicar_free.py --execute`, a fase `workspace import-dir --overwrite` materializou a árvore remota. Em seguida, a segunda fase histórica do publicador tentou reenviar individualmente o primeiro notebook didático como `SOURCE` e recebeu `PROTOCOL_ERROR`.

O diagnóstico controlado observou:

- o destino sem extensão já existia no workspace como `object_type=NOTEBOOK`, `language=PYTHON`;
- o caminho equivalente com `.py` não existia;
- o reenvio individual do mesmo notebook falhou **3/3** com o mesmo `PROTOCOL_ERROR`;
- a publicação completa não foi repetida após esse diagnóstico;
- o `--verify --conteudo` não foi executado nessa tentativa e, portanto, **nenhum PASS de publicação é declarado**.

### Classificação do incidente

A evidência demonstra que a premissa histórica do publicador — “`import-dir` sempre deixa o notebook didático como FILE e exige reenvio individual” — não vale para a CLI/runtime observados nesta rodada. O próprio `import-dir` já materializou o objeto como `NOTEBOOK`; a segunda escrita era redundante e foi o ponto de falha.

Isso é classificado como **incompatibilidade operacional do publicador com o comportamento atual da CLI**, não como falha do contrato SE01 nem como falha do capability probe.

## Correção de compatibilidade do publicador

A candidata foi ajustada para um fluxo compatível e fail-safe:

1. executar `workspace import-dir --overwrite`;
2. para cada notebook didático, consultar `workspace get-status`;
3. se o objeto já for `NOTEBOOK`, preservar o resultado e não fazer segunda escrita;
4. se não for `NOTEBOOK`, usar o reenvio individual legado como fallback `SOURCE/PYTHON/--overwrite`;
5. manter `--verify --conteudo` como autoridade final de inventário, tipo e bytes.

A suíte dirigida ganhou dois casos adicionais:

- notebook já materializado pelo `import-dir` → **não reimportar**;
- objeto não materializado como notebook → **usar fallback SOURCE**.

A suíte passa de 12 para **14 testes**. O gate dessa correção permanece pendente até execução efetiva do CI do HEAD correspondente e nova publicação + verify no Free.

## Capability probe no Free

- status: **PENDENTE**;
- branch/commit publicado e verificado: —;
- verify por conteúdo: —;
- chat novo: —;
- prompt exato: definido em `TESTES.md`;
- marcador bruto: —;
- execução do script observável: —;
- limitações: —;
- veredito: **PENDENTE**.

## Regressão de uso da EDA

- status: **PENDENTE**;
- prompt natural SE00-P1: congelado em `TESTES.md`;
- skill observada: —;
- degradação atribuível ao contrato/probe: —;
- veredito: **PENDENTE**.

## Regra

Não preencher lacunas por inferência. `NOT_OBSERVABLE` é resultado válido e distinto de `PASS`. Publicação parcial ou execução interrompida antes do `--verify --conteudo` também não é convertida em PASS.