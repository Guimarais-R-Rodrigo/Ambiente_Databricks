# B1 P2 — primeira campanha real governada

## Estado

Esta entrega materializa a arquitetura repo-side da P2 para a dupla SER03 L3 mensal/binária + SER05 L2 contexto. Ela **não executa a campanha, não certifica e não promove** as skills.

A P1 integrada permanece vinculada ao commit `d2b6079ee2e6ecec628d14411afbdbdb878a5fb9`. A P2 adiciona somente infraestrutura de campanha, testes e documentação; os bytes funcionais das fachadas P1 não devem ser alterados por esta etapa.

## Decisão arquitetural

O B0 mantém registry e release identity deliberadamente fechados em comandos `b0:*`. O `launcher.py` e o `verifier.py` importam o resolver B0 diretamente. Portanto, criar apenas outro JSON de comandos não produziria uma campanha verificável.

A P2 usa um adapter aditivo em `tools/skill_enforcement/real_campaigns/b1/`. Ele:

1. mantém `tools/skill_enforcement/parallel/**` byte-idêntico à base;
2. define registry B1 fechado, com command IDs e argv exatos;
3. cria release spec B1 que liga SHA/tree/base, registry, coverage, policy, host, interpreter e digest dos componentes B0 reutilizados;
4. injeta o resolver/validator B1 somente no processo que chama o launcher/verifier B0 e restaura os globals no `finally`;
5. reutiliza scheduler, lease, sandbox, process supervision, result schema e verifier B0;
6. mantém campanha read-only, effects `NONE` e concorrência qualificada `2/1`.

Não existe segundo scheduler, segundo sandbox, segundo verifier de processo ou engine paralelo.

## DAG

As duas frentes começam independentes:

```text
SER03 preflight ─→ SER03 execute+Receipt+verify ─→ SER03 domain audit ─┐
                                                                    ├─→ evidence/coverage audit
SER05 preflight ────────────────────────→ SER05 domain audit ───────┘
```

O scheduler B0 decide ondas e recursos. `max_parallel=2`; `max_auditors=1`. Auditorias de domínio compartilham a classe `audit`, e o auditor de evidência/coverage só libera após ambas.

## Comandos e efeitos

O registry B1 contém apenas comandos Python exatos sobre:

- fixtures sintéticas versionadas;
- preflights P1;
- runner/Receipt/verifier SER03;
- auditorias de domínio;
- negativos discriminantes selecionados;
- verificação da cobertura.

Todos declaram `effects=none`. O sandbox B0 continua bloqueando escrita fora de scratch, subprocessos filhos e rede.

## Coverage

`coverage_registry.json` fecha o vínculo de 19 casos no escopo com:

`case_id → test_id P1 → oracle_id → command_id P2 → evidência`.

CE03, CE04, CE09, CE11 e CE12 permanecem explicitamente fora da etapa L2, sem serem reinterpretados como PASS.

## Gates locais ainda necessários

Nenhum resultado deste commit deve ser chamado de LOCAL_PASS antes de uma execução local, no mesmo SHA, em checkout limpo:

1. `python -B -m tools.skill_enforcement.real_campaigns.b1.preflight`;
2. `python -B -m unittest tools.tests.test_ser_b1_campaign -v`;
3. `python -B -m tools.skill_enforcement.real_campaigns.b1.prepare --output-dir <diretorio-externo-novo>`;
4. executar **uma única vez** o `execution_argv` gerado no `HANDOFF.json`;
5. auditar o bundle/evidence resultante antes de freeze/certificação.

Cada gate é fail-fast, sem retry-until-green. O diretório `EVIDENCE` precisa não existir antes do launcher.

## Autoridade

P2 não altera `policy.json`. SER03 permanece current L0/target L3 e SER05 current L0/target L4 até campanha, auditoria, eventual prova externa pertinente e gate humano específico.

Não autoriza Ready, merge, Databricks Free/Genie, SER06 ou 3/2.
