# G6 — proposta de publicação corretiva mínima

## Estado

```text
PUBLICATION = PREPARED_NOT_AUTHORIZED
TARGET = PERSONAL_DATABRICKS_FREE
EFFECT = REMOTE_PACKAGE_WRITE
FULL_REPUBLISH = false
LOGICAL_OBJECTS = 17
```

A perícia demonstrou que o remoto já coincide com o produto atual em todos os demais objetos observáveis. Portanto a proposta é atualizar somente os 17 objetos que explicam integralmente o mismatch conhecido.

## Objetos

- `.assistant/hub_scripts/skill_execution/domain_context/README.md`
- `.assistant/hub_scripts/skill_execution/domain_context/__init__.py`
- `.assistant/hub_scripts/skill_execution/domain_context/exemplo_domain_context`
- `.assistant/hub_scripts/skill_execution/domain_context/release.py`
- `.assistant/hub_scripts/skill_execution/domain_context/temporal.schema.json`
- `.assistant/skills/hub-ml-analise-safra/execution_contract.json`
- `.assistant/skills/hub-ml-analise-safra/input.schema.json`
- `.assistant/skills/hub-ml-analise-safra/release_manifest.json`
- `.assistant/skills/hub-ml-analise-safra/scripts/README.md`
- `.assistant/skills/hub-ml-analise-safra/scripts/preflight.py`
- `.assistant/skills/hub-ml-analise-safra/scripts/run.py`
- `.assistant/skills/hub-ml-analise-safra/scripts/verify.py`
- `.assistant/skills/hub-ml-cross-eda-ml/execution_contract.json`
- `.assistant/skills/hub-ml-cross-eda-ml/input.schema.json`
- `.assistant/skills/hub-ml-cross-eda-ml/scripts/README.md`
- `.assistant/skills/hub-ml-cross-eda-ml/scripts/preflight.py`
- `.assistant/hub_padroes/skill_enforcement/policy.json`

## Regras

1. target explícito: profile `FREE`, host pessoal esperado;
2. preflight read-only confirma novamente auth/current-user;
3. cada destino deve estar no manifesto fechado acima;
4. os 16 missing são criados uma vez;
5. `policy.json` é sobrescrito uma vez somente se o hash remoto pré-write ainda corresponder ao histórico observado `b68d378b4552...`;
6. notebook `exemplo_domain_context.py` é publicado no destino sem extensão, como NOTEBOOK SOURCE;
7. demais objetos são FILE;
8. qualquer falha após uma escrita encerra a rodada; não retry-until-green;
9. preservar ledger por objeto com before-state, operation, exit code e after-state quando read-only ainda for possível;
10. após as 17 operações, executar verify por conteúdo uma única vez;
11. PASS exige zero errors e package remoto igual ao produto local;
12. probes, Genie, cleanup, policy promotion e merge permanecem fora desta autorização.

## Por que não usar a republicação ampla

`tools/publicar_free.py --execute` usa `workspace import-dir --overwrite` no pacote inteiro. Como 574 arquivos já foram comparados e somente 17 objetos lógicos explicam o mismatch conhecido, reescrever todo o pacote ampliaria desnecessariamente a superfície de efeito. Esta proposta prefere delta fechado e SHA-bound.

## Próximo gate

Antes de qualquer write remoto, esta proposta precisa:
- implementação de um publisher delta determinístico;
- testes locais;
- freeze do publisher;
- autorização humana específica para `REMOTE_PACKAGE_WRITE`.
