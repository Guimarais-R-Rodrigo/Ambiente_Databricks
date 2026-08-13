<!-- Template: matriz de cobertura entidade × fonte (skill rodrigo-cross-eda-ml) -->

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
| INNER (todas as fontes) | [N] | [X%] | 0 |
| LEFT (âncora + lefts) | [N] | [X%] | [Y colunas com NULL] |
| Híbrido (inner B, left C) | [N] | [X%] | [Y colunas com NULL] |

**Recomendação**: [Inner / Left / Híbrido] — justificativa: [1-2 linhas].

---

**Código de validação** (célula Python no notebook):

```python
# Substitua os placeholders antes de executar.
chave = "[chave]"
ancora = spark.table("[catalog.schema.ancora]").select(chave).distinct().cache()
n_ancora = ancora.count()
if n_ancora == 0:
    raise ValueError("A fonte âncora está vazia após os filtros")

for nome, tabela in [("B", "[catalog.schema.b]"), ("C", "[catalog.schema.c]")]:
    fonte = spark.table(tabela).select(chave).distinct()
    n_match = ancora.join(fonte, chave, "left_semi").count()
    print(f"Coverage {nome}: {n_match / n_ancora:.2%} ({n_match}/{n_ancora})")

ancora.unpersist()
```
