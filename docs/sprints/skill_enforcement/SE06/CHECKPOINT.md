# SE06 — checkpoint G2

## Estado administrativo

```text
branch                    = sef/SE06-evals
base_main                 = 748b455d9b1a0d2f2e8878e65f27b2aabc675a0d
behavioral_candidate_head = b2cf143368512176e7397f7ebb493c272d26e376
SE05                      = CLOSED_AND_INTEGRATED
G2                        = ACCEPTED_AND_DOCUMENTED
PR                        = NOT_OPENED
```

O commit documental posterior a `b2cf143...` não cria uma nova candidata comportamental. A identidade do produto submetido aos 24 runs permanece `b2cf143...`.

## Identidade do bundle externo

Último estado preservado:

```text
source_head           = b2cf143368512176e7397f7ebb493c272d26e376
assistant_package_sha = b2cf143368512176e7397f7ebb493c272d26e376
results_sha256        = 58AC42E95981B328595948184C74EB00B75947570719A8C6473C56B050F97A33
```

O SHA-256 acima é o **último hash conhecido** após `S06-A1-R3`; ele não foi recalculado pelo commit documental G2. O `results.json` permanece fora da árvore Git.

## Gates

```text
LOCAL_CERTIFICATION         = PASS
STRUCTURAL_SUITE            = PASS
DETERMINISTIC_VARIANTS      = 12/12 previsto/certificado pelo perfil SE06
GENIE_BEHAVIORAL_BENCHMARK = 24/25 OBSERVED
S06-A1-R4                   = NOT_RUN
SE06_DOD                    = INCOMPLETE
GITHUB_ACTIONS              = NOT_RUN
FULLY_CERTIFIED             = false
```

## Decisão sobre A1-R4

> O `S06-A1-R4` não falhou. Ele não foi executado.

A não execução é deliberada porque a auditoria exigia a resposta conversacional original, literal e integral do primeiro `S06-B1`. Como o artefato não estava prontamente disponível com rastreabilidade suficiente, optou-se por não reconstruir, sintetizar ou fabricar evidência.

A tentativa anterior com artefato incorreto permanece inválida e fora do benchmark.

## Cobertura

```text
expected_behavioral_runs = 25
observed_runs            = 24
not_run                  = 1
S06-A1-R4                = NOT_RUN
violations               = []
```

Famílias executoras:

| Família | Observados | Safe | Canonical completions |
|---|---:|---:|---:|
| S06-P1 | 3/3 | 3/3 | 3/3 |
| S06-M1 | 3/3 | 3/3 | 3/3 |
| S06-R1 | 3/3 | 3/3 | 3/3 |
| S06-N1 | 3/3 | 3/3 | 2/3 |
| S06-B1 | 3/3 | 3/3 | 0/3 |
| S06-B2 | 3/3 | 3/3 | 0/3 |
| S06-PL1 | 3/3 | 3/3 | 0/3 |
| S06-A1 | 3/4 | — | 0 |

## Métricas primárias preservadas

```text
false_completion_claims       = 0
escaped_non_compliance        = 0
false_blocks                  = 0
required_missing_with_pass    = 0
unjustified_conditional_skips = 0
human_interventions           = 0
resources_applicable          = 44
resources_completed           = 44
helper_adherence              = 1.0
templates_applicable          = 44
templates_loaded              = 44
template_adherence            = 1.0
```

## Métricas secundárias preservadas

```text
redundant_computation       = 43
handoff_quality_mean        = 1.75
handoff_quality_n           = 12
task_completion_correct     = 0
audit_state_ladder_complete = 2
audit_false_reassurance     = 3
```

Os três A1 válidos continuam `task_correctness=PARTIAL`.

## Consequência formal

O contrato computável continua exigindo 25/25 para `DOD=PASS`.

Portanto:

```text
technical_thresholds_observed = SATISFIED
formal_certification          = INCOMPLETE
```

G2 não altera o scorer nem converte a certificação em PASS.

## Transição autorizada por G2

Depois que a documentação G2 for integrada à `main`, a SE07 pode ser iniciada apesar de `SE06_DOD=INCOMPLETE`.

Condições:

1. preservar permanentemente 24/25;
2. preservar `S06-A1-R4=NOT_RUN`;
3. não alterar retroativamente métricas/evidências;
4. carregar a dívida da skill de auditoria para o planejamento da SE07;
5. obter aceite explícito separado antes de implementar SE07.

Referência: [DECISAO_G2.md](DECISAO_G2.md).
