# Template: Checklist MLflow

## Escolher a rota
Consultar a [skill](../SKILL.md) e a policy vigente antes de preencher.
- Cálculo local sem logging: tracking e Registry são NÃO APLICÁVEL; preservar
  request, Receipt e verificador exigidos pelo perfil.
- Tracking autorizado: registrar escopo, experimento, identidade e evidência.
- Registro UC/promoção: autorização e governança separadas; não decorrem do tracking.

O perfil `BINARY_TEMPORAL_LOCAL_V1` não grava MLflow. Seu adapter de tracking
exige `SER10-AUTH-1` e mantém o Registry fora do escopo. Respeitar verificação
live/finalizada, cleanup e estados UNKNOWN previstos no contrato; este checklist
não emite Receipt nem substitui os verificadores.

## Tracking, somente quando aplicável e autorizado

- [ ] Experimento, backend e identidade autorizados verificados
- [ ] Run efetivamente criado: [run_id ou NÃO EXECUTADO]
- [ ] Parâmetros, métricas por split e versões realmente observados
- [ ] Tags exigidas pelo perfil: [type, suite, algorithm, owner, versão real, dataset, target, split; N/A com motivo]
- [ ] Pipeline/modelo e assinatura, quando exigidos: [artefato e readback]
- [ ] Dataset/snapshot e exemplo de entrada seguros, sem PII/segredos
- [ ] Artefatos produzidos pela rota: [lista ou NÃO APLICÁVEL; não exigir SHAP/PNG inexistente]
- [ ] Estado de persistência, verificação e cleanup: [evidência ou UNKNOWN]

## Registro de modelo, somente com autorização própria

- [ ] Registro UC é suportado pela rota e foi solicitado: [autorização/destino]
- [ ] URI do modelo, assinatura, permissões e API instalada confirmadas
- [ ] Registro observado: [nome/versão/readback ou NÃO EXECUTADO]
- [ ] Promoção/alias/deploy: [decisão separada ou NÃO AUTORIZADO]

## Identificação

| Elemento | Valor fornecido/verificado |
|---|---|
| Experimento | [path/ID autorizado ou NÃO APLICÁVEL] |
| Run | [nome/ID observado ou NÃO EXECUTADO] |
| Modelo UC | [destino autorizado ou NÃO APLICÁVEL] |
| Responsável | [informado ou NÃO INFORMADO] |

## Resumo de evidência

| Item aplicável | Estado | Evidência/limite |
|---|---|---|
| [tracking/modelo/artefato/verificação/cleanup] | [NÃO EXECUTADO/observado/UNKNOWN/NÃO APLICÁVEL] | [fonte e motivo] |

Só marcar uma caixa após conferir sua evidência. A ausência de logging em perfil
local não é falha; um campo preenchido não comprova persistência ou autorização.
