# SE01 — checkpoint

## Veredito atual

**ABERTA / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE01 iniciou a camada L1 (`Contract`) do Skill Enforcement Framework na branch `sef/SE01-contrato`, baseada em `main@99161fdeb9253c30a82243644ba89af8cd50d79e`.

Contrato, suíte, renderer e CI já possuem evidência positiva. O gate final continua aberto porque a primeira publicação real no Databricks Free foi interrompida por uma incompatibilidade operacional do publicador antes do `--verify --conteudo`. A correção de compatibilidade está implementada e precisa ser revalidada localmente/CI e exercitada novamente no Free.

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
- [x] coerência de vocabulário entre JSON Schema e validador coberta por teste;
- [x] fonte ↔ `Novo_Ambiente_Simulado` regenerada pelo renderer canônico;
- [x] snapshot raiz atualizado por medição real: 1494 arquivos / 1961 links;
- [x] HEAD `dc4059a3bd7c116bcf40009ec66b1da7a2f809fd` validado localmente: contrato 1/1, suíte 12/12, validador 0/0;
- [x] 10/10 workflows aplicáveis da PR em `dc4059a3bd7c116bcf40009ec66b1da7a2f809fd`: `success`;
- [x] autenticação do profile pessoal do Databricks CLI validada;
- [x] dry-run do publicador: 550 arquivos, espelho em dia;
- [x] incidente de publicação diagnosticado sem repetição cega da escrita completa;
- [x] objeto didático observado no remoto como `NOTEBOOK` após `import-dir`;
- [x] reenvio individual redundante reproduziu `PROTOCOL_ERROR` em 3/3 tentativas;
- [x] publicador corrigido para preservar notebook já materializado e manter fallback SOURCE;
- [x] suíte ampliada para cobrir ambos os caminhos de compatibilidade (14 testes previstos);
- [ ] CI do HEAD com a correção de compatibilidade executado integralmente;
- [ ] nova execução local da suíte ampliada 14/14;
- [ ] publicação no Databricks Free concluída pelo publicador corrigido;
- [ ] `--verify --conteudo` no Free em PASS;
- [ ] capability probe executado em chat novo;
- [ ] regressão natural SE00-P1 executada em chat novo;
- [ ] limitações reais do Genie Code registradas;
- [ ] registrar entrada SE01 no `CHANGELOG.md` antes do fechamento da sprint;
- [ ] decisão sobre remover/promover o probe;
- [ ] aceite explícito do usuário;
- [ ] merge da PR.

## Evidência técnica consolidada

No commit `dc4059a3bd7c116bcf40009ec66b1da7a2f809fd`:

- contrato: **1/1 PASS**;
- recursos: **10**;
- templates: **4**;
- suíte local: **12/12 PASS**;
- schema ↔ validator: **PASS**;
- probe local read-only: **PASS**;
- `validate_assistant.py --conferir-readme`: **0 falhas / 0 avisos**;
- snapshot: **1494 arquivos / 1961 links / 0 extras**;
- GitHub Actions: **10/10 workflows aplicáveis em success**.

## Incidente do gate Databricks Free

A primeira chamada real do publicador atingiu o workspace. O `workspace import-dir --overwrite` materializou a árvore; em seguida, o publicador tentou reenviar individualmente um notebook didático como `SOURCE` e recebeu `PROTOCOL_ERROR`.

O diagnóstico controlado confirmou:

- o destino sem `.py` já era `object_type=NOTEBOOK` e `language=PYTHON`;
- o caminho com `.py` não existia;
- o reenvio individual redundante falhou 3/3 com o mesmo erro;
- a publicação completa não foi repetida depois do diagnóstico;
- o verify por conteúdo não foi executado e nenhum PASS de publicação foi registrado.

A correção mantém compatibilidade regressiva: depois do `import-dir`, o publicador consulta `get-status`; se o objeto já for `NOTEBOOK`, não faz uma segunda escrita. Se não for, mantém o fallback individual `SOURCE/PYTHON/--overwrite`.

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

1. sincronizar o worktree isolado com o HEAD corrigido;
2. executar a suíte local ampliada e o validador estrutural;
3. obter CI verde do HEAD corrigido;
4. repetir a publicação canônica no Free;
5. executar `--verify --conteudo` e registrar o relatório;
6. executar capability probe em chat novo;
7. executar regressão natural da skill em outro chat novo;
8. registrar resultados e limitações;
9. registrar a entrada SE01 no changelog antes do fechamento;
10. decidir se o probe é removido ou promovido ao componente definitivo;
11. reconciliar a branch com a `main` vigente se ela tiver avançado;
12. pedir homologação da SE01.

SE02 permanece bloqueada até esse fechamento.