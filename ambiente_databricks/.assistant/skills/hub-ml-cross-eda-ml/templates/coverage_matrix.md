<!-- Template: matriz de cobertura entidade × fonte (skill hub-ml-cross-eda-ml) -->

# 🗺️ Coverage Matrix — Entidade × Fonte

## Cobertura por fonte (em relação à âncora)

| Fonte | Entidades cobertas | Coverage Rate | Status |
|---|---|---|---|
| **Âncora** (`[tabela]`) | [N total] | 100% (referência) | — |
| Fonte B (`[tabela]`) | [N com match] | [X%] | [comparar ao limite aprovado] |
| Fonte C (`[tabela]`) | [N com match] | [X%] | [✅ / 🟡 / 🔴] |
| Fonte D (`[tabela]`) | [N com match] | [X%] | [✅ / 🟡 / 🔴] |

## Matriz cruzada (presença combinada)

| Combinação | N entidades | % da âncora | Observação |
|---|---|---|---|
| Em TODAS as fontes | [N] | [X%] | Base efetiva para modelo (inner join) |
| Âncora + B (sem C) | [N] | [X%] | [Interpretar] |
| Âncora + C (sem B) | [N] | [X%] | [Interpretar] |
| Apenas na âncora | [N] | [X%] | Registros sem enriquecimento |

## Perfil dos não-cobertos

> ⚠️ Analisar o perfil dos órfãos sempre que a cobertura puder alterar a representatividade ou a decisão.

### Fonte [X] — Entidades sem match (N = [valor])

| Variável | Cobertos (média/moda) | Não cobertos (média/moda) | Diverge? |
|---|---|---|---|
| [var_1] | [valor] | [valor] | [Sim/Não] |
| [var_2] | [valor] | [valor] | [Sim/Não] |
| [var_3] | [valor] | [valor] | [Sim/Não] |

**Conclusão sobre ausência**:
- [ ] Ausência estrutural explicada pelo contrato da fonte
- [ ] Ausência associada a período/segmento observável
- [ ] Ausência sem causa confirmada — requer investigação

Não classificar MCAR/MAR/MNAR apenas por comparação descritiva e não concluir que `LEFT JOIN` é seguro sem validar granularidade e disponibilidade temporal.

## Impacto na base de modelagem

| Estratégia de join | N final | % da âncora | Nulos médios por linha |
|---|---|---|---|
| INNER (todas as fontes) | [N] | [X%] | [medir; match de chave não elimina NULL original] |
| LEFT (âncora + lefts) | [N] | [X%] | [Y colunas com NULL] |
| Híbrido (inner B, left C) | [N] | [X%] | [Y colunas com NULL] |

**Recomendação**: [Inner / Left / Híbrido] — justificativa: [1-2 linhas].

---

**Plano de validação** (pseudocódigo; não executar como célula):
A cobertura de chave não mede completude dos atributos. Declarar denominador,
filtros, política de chaves nulas, grão e disponibilidade temporal. Usar a rota
canônica da skill e `diagnosticar_join` quando aplicável; o perfil somente de
contexto não consulta dados nem mede coverage. Contagens Spark têm custo.
Cache/persist só se permitidos pelo compute e pela política, com liberação
prevista; não adicionar cache obrigatório a esta validação.

```text
confirmar fontes, chaves, grão, filtros, denominador e autorização de leitura
usar diagnóstico canônico de cardinalidade e cobertura, sem substituir o runner
se âncora vazia: registrar indefinição, sem dividir por zero
medir match de chave e, separadamente, NULL por atributo na população pós-join
reportar valores observados, Receipt/verificador aplicáveis e limites
```
