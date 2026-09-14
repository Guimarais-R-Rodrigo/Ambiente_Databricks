# Checkpoint V10 — Databricks App de gestão visual

## Estado

**CANDIDATA; SEM ACEITE, MERGE OU DEPLOY DATABRICKS.**

Base: `d6655411ca4ac1834b0983f6ce6bdadc30b831bb`.

Branch: `codex/temas-v10-databricks-app-20260914`.

Head funcional/documental antes da reconciliação final: `0ddcdd6b92372186c130d226c4b72d141cb7d67e`.

## Escopo recuperado

V10 é a frente de Databricks App de gestão visual. V11 permanece reservada para AI/BI. O App reutiliza os contratos e o Visual Lab já integrados e deve ter identidade, papéis, persistência, retenção, custos e deploy/rollback explicitamente definidos.

## Decisões

- nenhum novo schema de tema;
- nenhum novo token/paleta;
- `context="app"` continua não implementado como contexto temático;
- o App gerencia temas `notebook` existentes;
- identidade vem do proxy Databricks, nunca do JSON de tema;
- persistência usa UC Volume via recurso `theme_storage`;
- namespace de usuário usa SHA-256 do identificador em memória;
- path produtivo precisa seguir `/Volumes/<catalog>/<schema>/<volume>` e traversal/symlink são recusados;
- política de retenção: sem delete automático/usuário e sem reescrita de histórico;
- aprovação/publicação/promoção ausentes do código;
- bundle de deploy é derivado em `.artifacts/`, nunca fonte editável paralela;
- CI é local/read-only e não recebe credenciais Databricks.

## Arquivos principais da candidata

- `ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app.py`;
- `.../app_service.py`;
- `.../app.yaml`;
- `.../requirements.txt`;
- `.../README.md`;
- `.../GUIA_PRIMEIRO_USO.md`;
- `.../DEPLOY_ROLLBACK.md`;
- espelho equivalente em `Novo_Ambiente_Simulado`;
- `tools/temas_v10_app.py`;
- `tools/tests/test_temas_v10.py`;
- `.github/workflows/temas-v10-ci.yml`;
- documentação V10 e matriz de papéis.

## Evidências já obtidas

### Run `34884790130` — FAILURE preservado

A suíte V10 passou, mas o cumulativo terminou **433/434** porque a etapa `py_compile` do próprio runner gerou dois `.pyc` transitórios apenas na árvore fonte. A correção passou a validar sintaxe em memória e a equivalência ignora somente caches não versionados. Não houve divergência versionada de produto.

### Run `34885407907` — FAILURE preservado

No head `0ddcdd6b92372186c130d226c4b72d141cb7d67e` passaram:

- V10 **19/19**;
- regressões V01–V10 **436/436**;
- V00 **12/12**;
- bundle **247 arquivos + `V10_APP_MANIFEST.json`**;
- verificação de hashes/tamanhos do bundle.

O validador reprovou com **7 falhas / 0 avisos** por métricas antigas no README raiz e um link relativo inválido no README espelhado do App. Nenhuma falha funcional do App permaneceu nesse run.

## Gates antes de pedir aceite

1. suíte V10 verde;
2. regressões V01–V10 verdes;
3. V00 verde;
4. bundle V10 criado e verificado;
5. source/simulado equivalentes;
6. validador 0 falhas / 0 avisos;
7. PR mergeável e checks reais verdes;
8. diff sem temporários e sem credenciais;
9. documentação atualizada com resultados reais e failures preservados.

Os gates 1–5 já foram exercitados com sucesso no run `34885407907`; o gate 6 exige a reconciliação documental corrente. Os gates 7–9 serão fechados no head final/PR.

## Pendências que não bloqueiam a candidata Git, mas bloqueiam homologação operacional

- deploy autorizado de Databricks App;
- associação real do UC Volume;
- permissões/grupos reais;
- teste de headers reais;
- teste multiusuário no workspace;
- browser/acessibilidade;
- UAT V12;
- custo observado;
- procedimento de deploy/rollback executado no destino.

## Próximo passo

Corrigir a navegação documental, repetir o validador e medir o estado final. Só depois atualizar o bloco verificável do README raiz com números observados, repetir o gate completo e abrir PR em draft. Merge continua dependente de aceite explícito de Rodrigo. V11 não deve ser iniciada.
