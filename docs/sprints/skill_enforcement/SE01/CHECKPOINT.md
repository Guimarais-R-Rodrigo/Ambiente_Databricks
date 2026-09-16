# SE01 — checkpoint

## Veredito atual

**ABERTA / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE01 iniciou a camada L1 (`Contract`) do Skill Enforcement Framework na branch `sef/SE01-contrato`, baseada em `main@99161fdeb9253c30a82243644ba89af8cd50d79e`.

O contrato e a suíte dirigida já possuem evidência positiva. O gate final ainda não está fechado porque o Databricks Free não foi testado e a rodada mais recente do GitHub Actions não obteve runner.

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
- [x] fonte ↔ `Novo_Ambiente_Simulado` regenerada pelo renderer canônico;
- [x] snapshot raiz atualizado por medição real: 1494 arquivos / 1961 links;
- [x] contrato v0.1 observado em PASS no CI;
- [x] suíte SE01 observada em 11/11 PASS no CI;
- [x] validador estrutural observado com 0 falhas / 0 avisos;
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

## Incidente de CI após o snapshot

Todos os workflows acionados no commit `264981cb4ce1a5aff8d3c1f6dd54caa1fa57c174` terminaram como `failure` sem executar steps. O job SE01 registrou `runner_id=0`, `runner_name=""` e lista de steps vazia. Um rerun do mesmo job, sem alteração da branch, repetiu o comportamento.

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

1. obter uma execução real de CI no HEAD corrente;
2. registrar a entrada SE01 no changelog antes do fechamento;
3. publicar a candidata no Free;
4. executar `--verify --conteudo`;
5. executar capability probe em chat novo;
6. executar regressão natural da skill em outro chat novo;
7. registrar resultados e limitações;
8. decidir se o probe é removido ou promovido ao componente definitivo;
9. reconciliar a branch com a `main` vigente se ela tiver avançado;
10. pedir homologação da SE01.

SE02 permanece bloqueada até esse fechamento.