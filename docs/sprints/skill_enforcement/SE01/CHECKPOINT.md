# SE01 — checkpoint

## Veredito atual

**ABERTA / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE01 iniciou a camada L1 (`Contract`) do Skill Enforcement Framework na branch `sef/SE01-contrato`, baseada em `main@99161fdeb9253c30a82243644ba89af8cd50d79e`.

O contrato, a suíte dirigida e a validação local do HEAD atual possuem evidência positiva. O gate final ainda não está fechado porque o Databricks Free não foi testado e as rodadas recentes do GitHub Actions não obtiveram runner/steps executáveis.

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
- [x] contrato v0.1 observado em PASS no CI anterior;
- [x] suíte SE01 observada em 11/11 PASS no CI anterior;
- [x] validador estrutural observado com 0 falhas / 0 avisos no CI anterior;
- [x] HEAD `e442b2423c02de59f23183783b493f4b8fb44497` validado localmente em worktree isolado;
- [x] contrato local atual: 1/1 PASS;
- [x] suíte local atual: 12/12 PASS;
- [x] `validate_assistant.py --conferir-readme` local: 0 falhas / 0 avisos;
- [x] worktree local SE01 limpo e separado das alterações locais V12;
- [ ] registrar entrada SE01 no `CHANGELOG.md` antes do fechamento da sprint;
- [ ] CI final executado integralmente no HEAD corrente;
- [ ] publicação no Databricks Free;
- [ ] `--verify --conteudo` no Free;
- [ ] capability probe executado em chat novo;
- [ ] regressão natural SE00-P1 executada em chat novo;
- [ ] limitações reais do Genie Code registradas;
- [ ] decisão sobre remover/promover o probe;
- [ ] aceite explícito do usuário;
- [ ] merge da PR.

## Evidência técnica já obtida

No commit `fda26d130e559d3fdb8ee69fcb785ffecc76a049`, o workflow dedicado executou efetivamente:

- validação do contrato: PASS;
- 11/11 testes SE01: PASS;
- `validate_assistant.py`: 0 falhas / 0 avisos;
- renderer: sem diff depois da materialização do simulado.

O gate de snapshot desse mesmo run mediu 1494 arquivos e 1961 links; o README foi então corrigido no commit `264981cb4ce1a5aff8d3c1f6dd54caa1fa57c174`.

## Validação local do HEAD atual

Em 16/09/2026, a candidata `e442b2423c02de59f23183783b493f4b8fb44497` foi sincronizada em worktree Git dedicado, separado do worktree local usado pela frente V12.

Resultados observados no worktree SE01:

- branch: `sef/SE01-contrato`;
- `git status --short`: limpo;
- contrato: **1/1 PASS**;
- recursos: **10**;
- templates: **4**;
- suíte SE01: **12/12 PASS**;
- teste schema ↔ validator: **PASS**;
- probe local read-only: **PASS**;
- `validate_assistant.py --conferir-readme`: **0 falhas / 0 avisos**;
- snapshot: **1494 arquivos / 1961 links / 0 extras**.

Essa evidência confirma o HEAD localmente, mas não substitui o gate real do Genie Code no Free nem o CI final.

## Incidente de CI após o snapshot

As rodadas recentes do GitHub Actions terminaram como `failure` sem executar steps. O job SE01 e workflows independentes registraram `steps=[]`/`steps=null` e ausência de execução material dos comandos.

Esse evento permanece classificado como **gate operacional pendente**, não como falha funcional da candidata. Nenhum PASS anterior é promovido para o novo HEAD, mas também não se atribui regressão a comandos que não chegaram a executar.

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

## Achado de modelagem incorporado

A validação do contrato usa `module` + `symbol` e a fachada pública `__init__.py`. Isso evita transportar cegamente nomes de inventários históricos.

Exemplo: o recurso `index_generator` está atualmente em `hub_snippets.visual.index_generator` e exporta `gerar_indice_eda`. A evidência congelada da SE00 não é reescrita retroativamente; o contrato SE01 usa a API pública atual.

As quatro políticas de templates também foram confrontadas com a SE00 e coincidem: `roteiro_eda` e `relatorio_executivo_eda` required; `matriz_graficos_eda` e `estilo_visual_eda` conditional.

## Próximos gates

1. publicar a candidata no Databricks Free a partir do worktree isolado;
2. executar `--verify --conteudo` e registrar o relatório;
3. executar capability probe em chat novo;
4. executar regressão natural da skill em outro chat novo;
5. registrar resultados e limitações;
6. obter uma execução real de CI no HEAD final;
7. registrar a entrada SE01 no changelog antes do fechamento;
8. decidir se o probe é removido ou promovido ao componente definitivo;
9. reconciliar a branch com a `main` vigente se ela tiver avançado;
10. pedir homologação da SE01.

SE02 permanece bloqueada até esse fechamento.