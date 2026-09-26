# SE07 — runbook Free

## Objetivo

Validar registry/resolver e a correção epistemológica da auditoria.

## Situação corrente — checkpoint R1-C aceito e F-03 local

O checkpoint humano aceito `b6fb595225e139329df450edfc33158ceb1e1253` cobre
somente F-01/F-02 e gates locais Windows/Linux; ele não homologa Free/Genie.
R1 `2d25bd2...` continua NAO_APTA historicamente. A próxima candidata local
trata F-03/D6 no adapter da auditoria e precisa de certificação e revisão
próprias. F-04 e decisões de conversão antes de L3 permanecem pendentes.

Publicação e probes no Free não estão autorizados nesta rodada. O próximo gate
proposto é a revisão independente da candidata local, conforme
[CHECKPOINT.md](CHECKPOINT.md). A certificação local precisa corresponder ao SHA
da candidata, e não a uma execução de onda anterior.

Quando houver autorização específica para novo gate Free, registrar o SHA e o
fingerprint do pacote efetivamente verificado antes de interpretar os probes.
Na baseline local R1, a policy declara EDA L4, auditoria L3, criar-objeto L2 e
tutor L0. O último verify Free histórico disponível pertence a `3b75edf04c1f`
(criar-objeto ainda L1), sem conferência atual nesta R1.

O exemplo abaixo pertence à primeira fatia (`af68a9e6bf1b`), quando auditoria
ainda era L0. Foi preservado como histórico; não é um probe corrente da R1.

## Pré-condição histórica da primeira fatia

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE07_LOCAL
DERIVED_STALE       = false
failures            = 0
```

## Probe histórico da primeira fatia

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy

eda = get_skill_enforcement_policy("hub-ml-eda-profissional")
audit = get_skill_enforcement_policy("hub-ml-auditoria-skills")
tutor = get_skill_enforcement_policy("hub-ml-tutor-databricks")

assert eda.current_level == "L4"
assert audit.current_level == "L0"
assert audit.target_level == "L3"
assert tutor.current_level == tutor.target_level == "L0"
```

Sem escrita persistente e sem execução analítica.

Depois executar A07-1..A07-3 de [TESTES.md](TESTES.md), cada um em chat novo. Registrar primeira resposta; não repetir resultado ruim seletivamente.
