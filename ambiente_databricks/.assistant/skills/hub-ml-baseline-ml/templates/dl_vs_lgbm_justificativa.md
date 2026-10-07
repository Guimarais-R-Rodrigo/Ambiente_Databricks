# Template: Justificativa DL vs LightGBM

## Uso
Documentar recomendação técnica entre modelos tabulares. Não pressupor que DL
exige cardinalidade mínima, GPU ou ganho fixo. Confirmar o perfil disponível na
[skill](../SKILL.md) antes de executar; fora dele, entregar plano.

## Contrato do benchmark

- Problema, target, população, período e métrica primária: [informados ou pendentes]
- Divisões iguais, preprocessamento ajustado no treino e teste intocado: [evidência]
- Baseline trivial e LightGBM comparáveis: [executado/NÃO EXECUTADO]
- Critério mínimo de ganho: [métrica, unidade, incerteza, custo e responsável]
- Compute/dependências autorizados e orçamento: [restrições]
- Cardinalidade, volume e diversidade: [observados; hipótese de benefício a testar]

## Comparação observada

| Aspecto | LightGBM | [Modelo DL] | Diferença e incerteza | Critério do caso |
|---|---|---|---|---|
| Métrica primária [nome/unidade] | [resultado ou NÃO EXECUTADO] | [resultado ou NÃO EXECUTADO] | [valor/método] | [aprovado ou NÃO INFORMADO] |
| Guardrails por segmento/período | [evidência] | [evidência] | [limites] | [critério] |
| Tempo/custo de treino | [medido] | [medido] | [diferença] | [orçamento] |
| Latência/custo de inferência | [medido] | [medido] | [diferença] | [SLA] |
| Interpretabilidade | [método e limitações] | [método e limitações] | [comparação] | [necessidade] |
| Deploy/manutenção | [requisitos verificados] | [requisitos verificados] | [custo] | [capacidade] |

Sem benchmark comparável, ganho permanece NÃO DEMONSTRADO. Um ponto percentual
só é unidade adequada quando a métrica é proporção; não é limiar universal.

## Recomendação e decisão

- Recomendação técnica: [avaliar DL/manter baseline/investigar; motivo]
- Evidência de ganho relevante frente a custo e incerteza: [fonte]
- Decisor e aprovação: [identidade, escopo, estado; NÃO INFORMADO se ausente]
- Tracking: [não aplicável/autorizado; experimento, artefatos e evidência]
- Registro de modelo/promoção: [autorização separada ou NÃO AUTORIZADO]
- Recuperação/fallback operacional: [plano aprovado, sem contornar gates]
- Monitoramento: [janela e critérios definidos pelo caso, owner]

A recomendação não treina, registra nem implanta modelos. MLflow depende da rota
e da autorização; registro UC, alias e deploy não decorrem deste relatório.
