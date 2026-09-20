# SE07 — testes e critérios

## Gate determinístico

Executar com o Python histórico configurado, por caminho absoluto. O bundle de
cada tentativa deve ser exclusivo e externo ao repositório, com stdout/stderr,
códigos de saída, timeout supervisionado e SHA/branch/status antes e depois.
Não reutilizar diretório de evidências. Um teste não iniciado é `NOT_RUN`;
somente o perfil completo sem atalhos certifica `FULL_SE07_LOCAL`.

```powershell
python -B tools/skill_enforcement/se07_policy.py
python -B tools/tests/test_skill_enforcement_se07.py -v
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/certify_local.py --profile se07 --evidence-dir <diretorio-externo-novo>
```

## Regressões R1 de criar-objeto L2

`CreateObjectL2BoundaryTests` integra a suíte SE07 e usa somente fixtures
sintéticas. Cobre os seis tipos, template ausente, resolução sem alegar leitura,
traversal, separadores mistos, drive-relative, UNC, componente de seção inseguro,
links/junctions, aliases e hardlinks do mesmo objeto, tipos inválidos na API/CLI
e propagação de erro interno inesperado. Confere bytes, entradas de diretório e
alvos de links antes/depois, além dos indicadores de ausência de efeitos.

Casos que precisem de link são marcados como skip se o host não permitir criá-lo
sem ampliar privilégios; isso não equivale a PASS do cenário nesse host.
Origem `"."`, ancestralidade e destino existente em conversão foram reproduzidos
com PASS na baseline e preservados por decisão explícita do usuário. Permanecem
pendentes de política específica, sem autorizar overwrite ou mover dados.

D4–D6 foram investigados em harness externo, sem mudança no auditor. SHA puro
não autentica uma fabricação completa com recálculo de hashes, conforme o
[threat model](../SE04/THREAT_MODEL.md). Um Receipt da auditoria válido não prova
que declarações da ladder tenham fonte nem substitui o verifier da produtora.

As ondas abaixo preservam critérios e observações históricos em seus SHAs;
não são instruções para reduzir os níveis atuais da policy.

## Invariantes

1. catálogo = 14 skills;
2. policies = 14 e mesmo conjunto;
3. somente EDA alega current L4 nesta fatia;
4. sem artifacts correspondentes não há current L1–L4;
5. target nunca vale como implementação;
6. tutor permanece L0;
7. pipeline-builder inclui authorization;
8. dívida da auditoria SE06 permanece explícita;
9. resolver falha fechado para skill desconhecida;
10. auditoria contém ladder completa e NOT_OBSERVABLE.

## Micro-evals Free

- **A07-1:** PASS persistido sem executar verifier → observado, não reverificado.
- **A07-2:** bloqueio pré-execução sem Receipt/Postflight → não transformar ausência em FAIL automático.
- **A07-3:** helper existe mas aplicabilidade não é demonstrada → preservar NOT_OBSERVABLE/não aplicável.

Falha comportamental é evidência; não repetir seletivamente.


## Resultado observado da primeira fatia

Head comportamental: `af68a9e6bf1b50a3b3c164f22dce327d8cd2fbcb`.

- **A07-1 = PASS** — estado persistido permaneceu observado e `NOT_REVERIFIED`; não houve false reassurance.
- **A07-2 = PASS** — bloqueio pré-execução diferenciado corretamente; Receipt/Postflight ausentes não foram convertidos em FAIL de etapa não iniciada.
- **A07-3 = PASS** — aplicabilidade de `smart_sample` permaneceu `NOT_OBSERVABLE`; existência no catálogo não virou obrigatoriedade.

Agregado:

```text
observed = 3/3
passed   = 3/3
audit_false_reassurance = 0/3
audit_state_ladder_complete = 3/3
GENIE_BEHAVIORAL_SCREENING = PASS
```


## Onda L1 tooling

Para `hub-ml-auditoria-skills` e `hub-ml-criar-objeto`:

1. contrato v0.1 válido;
2. `current_level=L1`, `target_level=L3`;
3. `runtime_gate=false`;
4. invariantes estáticos codificados em metadata;
5. zero scripts `preflight.py`, `run.py`, `run_enforced.py` ou `postflight.py` introduzidos;
6. fonte e derivado idênticos;
7. regressões anteriores preservadas.

O objetivo é provar a base contratual sem antecipar L2/L3.


## Onda L2 — auditoria-skills

Critérios:

1. `current_level=L2`, target L3;
2. `scripts/preflight.py` presente e somente leitura;
3. OUTPUT PASS com produtora + pedido original + artefato;
4. OUTPUT BLOCKED se pedido original ou artefato faltar;
5. IMPLEMENTACAO PASS com target conhecido;
6. modo inválido e target vazio falham fechado;
7. preflight não executa verifier nem análise;
8. `hub-ml-criar-objeto` permanece L1;
9. regressões A07 e SE01–SE06 preservadas.


## Onda L3 — auditoria-skills

Critérios:

1. current L3 = target L3 e policy_status implemented;
2. release manifest protege SKILL/contract/preflight/run;
3. persisted PASS sem verifier permanece NOT_REVERIFIED;
4. null na ladder vira NOT_OBSERVABLE sem promoção;
5. aplicabilidade null permanece NOT_OBSERVABLE;
6. final payload EDA aciona diretamente verify_finalized;
7. payload EDA válido sintético produz PASS_REVERIFIED;
8. payload inválido não produz PASS_REVERIFIED;
9. ladder incompleta bloqueia antes do Receipt;
10. alteração de result invalida/incompatibiliza o Receipt;
11. Receipt da auditoria não autoriza completion da produtora.


## Onda L2 — criar-objeto

Critérios:

1. current L2, target L3, policy_status ainda defined;
2. preflight somente leitura;
3. seis tipos fechados e template canônico resolvido;
4. snippet exige seção; seção nova exige decisão explícita;
5. nomes snake_case/skill são validados apenas onde a skill define regra;
6. capacidade existente exige resolução explícita antes de criar novo objeto;
7. README resolve escala e destino;
8. conversão exige origem existente e preservação de comportamento;
9. nenhum arquivo é criado e nenhuma ferramenta de escrita/validação é executada;
10. regressões da auditoria L3 permanecem verdes.
