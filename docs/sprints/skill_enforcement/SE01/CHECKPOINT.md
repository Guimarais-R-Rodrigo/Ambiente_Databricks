# SE01 — checkpoint

## Veredito atual

**ABERTA / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE01 iniciou a camada L1 (`Contract`) do Skill Enforcement Framework na branch
`sef/SE01-contrato`, baseada em
`main@99161fdeb9253c30a82243644ba89af8cd50d79e`.

## Estado implementado/candidato

- [x] branch SE01 criada da `main` vigente na abertura;
- [x] ADR-0021 proposta;
- [x] schema v0.1 definido;
- [x] contrato piloto da EDA em `mode="audit"`;
- [x] resolução estática de módulos/símbolos públicos;
- [x] resolução de templates relativos;
- [x] vocabulário fechado de conditions;
- [x] capability probe read-only criado;
- [x] testes positivos/negativos adicionados;
- [ ] fonte ↔ `Novo_Ambiente_Simulado` regenerada/conferida pelo renderer;
- [ ] snapshot raiz reconciliado com medição real;
- [ ] checks GitHub da candidata verdes;
- [ ] publicação no Databricks Free;
- [ ] `--verify --conteudo` no Free;
- [ ] capability probe executado em chat novo;
- [ ] regressão natural SE00-P1 executada em chat novo;
- [ ] limitações reais do Genie Code registradas;
- [ ] decisão sobre remover/promover o probe;
- [ ] aceite explícito do usuário;
- [ ] merge da PR.

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

## Achado de modelagem já incorporado

A validação do contrato usa `module` + `symbol` e a fachada pública
`__init__.py`. Isso evita transportar cegamente nomes de inventários históricos.

Exemplo: o recurso `index_generator` está atualmente em
`hub_snippets.visual.index_generator` e exporta `gerar_indice_eda`. A evidência
congelada da SE00 não é reescrita retroativamente; o contrato SE01 usa a API
pública atual.

## Próximo gate

1. regenerar o simulado pela ferramenta canônica;
2. medir/ajustar snapshot verificável somente pela saída real;
3. fechar CI;
4. publicar a candidata no Free;
5. executar capability probe em chat novo;
6. executar regressão natural da skill;
7. registrar resultados;
8. revisar/remover/promover o probe;
9. pedir homologação da SE01.

SE02 permanece bloqueada até esse fechamento.
