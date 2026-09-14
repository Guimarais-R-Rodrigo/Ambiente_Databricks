# Changelog

Toda mudança relevante deste projeto é registrada aqui, em entradas curtas, sem
expor identificadores corporativos, PII ou segredos. Formato: seções por data,
subseções Adicionado/Atualizado/Corrigido/Removido, cada item com a IA autora
entre parênteses. Template: `.claude/templates/changelog-entry.md`.

## 2026-09-14 — MM01: candidata do contrato canônico de micromodelos (ChatGPT)

### Adicionado

- (ChatGPT) Schema formal Draft 2020-12 `micromodelo.schema.json`, template YAML canônico, máquina de fases/condições, proveniência controlada e validador fail-closed de referência para a MM01.
- (ChatGPT) Fixtures sintéticos e suíte `test_micromodelo_mm01.py` com casos positivos, mutantes negativos, proteção `FALSE` × `INDETERMINADO`, score 0–100, calibração, aprovações humanas, escopo de fontes e gates de publicação.
- (ChatGPT) Workflow permanente read-only `micromodelos-mm01-ci.yml` e pacote neutro de auditoria A1 em `docs/auditoria/2026-09-14_micromodelos-mm01/`; a auditoria foi preparada, mas ainda não executada.

### Atualizado

- (ChatGPT) `tools/requirements-dev.txt` recebe PyYAML apenas como dependência de manutenção/CI; isso não cria dependência runtime para a futura skill.
- (ChatGPT) A candidata, iniciada sobre `main@ec52d379`, foi reconciliada de forma fail-closed com `main@a9480391c78e2402986885db0ce08b10e0619a1a` após a integração/fechamento da V10, sem reimplementar nem alterar a frente visual.

### Evidências

- (ChatGPT) A primeira materialização transitória (`34899029039`) permaneceu `failure` por corrupção do pacote gzip antes dos testes e não publicou os artefatos candidatos.
- (ChatGPT) Materialização corrigida `34899617125`, reconciliação pós-V10 `34900062786` e primeiro gate permanente MM01 `34900332458` concluíram com `success`; os dois workflows transitórios se removeram antes de publicar suas composições.
- (ChatGPT) O gate permanente executa instalação limpa, 9 testes MM01 e `validate_assistant.py --root ambiente_fonte`; CI agregado de PR e auditoria A1 permanecem pendentes.

### Limites

- (ChatGPT) MM01 não cria skill, sétimo tipo do Hub, fingerprint, crawler de catálogo, feature engineering, contrato definitivo de MLflow, integração visual própria, publicação real ou migração de legado. MM02 permanece bloqueada até auditoria, aceite explícito e integração.

## 2026-09-14 — MM00: integração e fechamento documental do Framework de Micromodelos (ChatGPT)

### Adicionado

- (ChatGPT) Fundação documental MM00–MM13 do Framework de Micromodelos, com Plano Mestre, inventário, matrizes de reuso/riscos/dependências, pacote de auditoria A1 e checkpoint fail-closed.
- (ChatGPT) ADR-0014 a ADR-0020 para congelar as fronteiras arquiteturais: micromodelo como artefato de domínio, `micromodelo.yaml` canônico, MLflow para histórico de runs, governança externa de publicação, piloto greenfield antes dos legados, consumo do Sistema de Temas e fontes limitadas ao catálogo configurado.

### Atualizado

- (ChatGPT) PR #43 integrada após aceite humano explícito; head final validado `e3809b15b61f2bc1eeec06c9de6f38a329868e98` e merge `36e89515a46df24f41deea4791b109f5a1f938f2`.
- (ChatGPT) ADR-0014 a ADR-0020 ratificados como aceitos sem ressalvas; MM01 continua condicionada às decisões detalhadas previstas nas sprints seguintes, sem antecipação silenciosa de schema, fingerprint ou tracking rule-based.
- (ChatGPT) Q-01 da auditoria A1 é fechado por esta manutenção pós-merge, conforme exceção D1-B: a entrada da MM00 foi diferida para preservar o histórico do changelog e agora é registrada de forma aditiva.

### Evidências

- (ChatGPT) Auditoria A1 independente: `APTA_COM_CORRECOES`; M-01 corrigido, nenhum `DIVERGE` atribuível à MM00 e Q-01 tratado pela D1-B até este fechamento.
- (ChatGPT) Bateria final da candidata: CI geral `34893158270`, V00 `34893158453`, V01 `34893158339` e V02 `34893158265`, todos `success` no mesmo head final; nenhum validador foi relaxado.

### Limites

- (ChatGPT) MM00 não cria skill, prompt funcional, helper, template executável, micromodelo real, consulta de dados, run MLflow, publicação ou migração de legado. Esta entrada fecha somente a pendência documental Q-01 antes da MM01.

## 2026-09-14 — V08: integração transversal e fechamento técnico (ChatGPT)

### Adicionado

- (ChatGPT) Matriz transversal de integração entre Sistema de Temas, skills, Hub Padrões, entrada `.assistant` e Manual Técnico.
- (ChatGPT) Suíte V08 e workflow permanente read-only com guarda explícita que proíbe alterações runtime Python em `hub_snippets` e `hub_scripts`.

### Atualizado