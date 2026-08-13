<!-- Template: análise de viabilidade de join por par (skill rodrigo-cross-eda-ml) -->

# 🔗 Etapa 4 — Join Feasibility Analysis

## Resumo por par de fontes

| Par | Chave de join | Tipo de relação | Jaccard | Overlap | Explosão? | Viabilidade |
|---|---|---|---|---|---|---|
| A × B | `[coluna]` | [1:1 / 1:N / M:N] | [0.XX] | [0.XX] | [Sim/Não] | [✅/🟡/🔴] |
| A × C | `[coluna]` | [1:1 / 1:N / M:N] | [0.XX] | [0.XX] | [Sim/Não] | [✅/🟡/🔴] |
| B × C | `[coluna]` | [1:1 / 1:N / M:N] | [0.XX] | [0.XX] | [Sim/Não] | [✅/🟡/🔴] |

## Detalhamento por par

### Par A × B

| Métrica | Valor | Interpretação |
|---|---|---|
| Entidades em A | [N] | — |
| Entidades em B | [N] | — |
| Interseção (A ∩ B) | [N] | — |
| Só em A (órfãos A) | [N] ([X%]) | [Preocupante se > 20%] |
| Só em B (órfãos B) | [N] ([X%]) | [Preocupante se > 20%] |
| **Jaccard** | [0.XX] | [Alta/Moderada/Baixa sobreposição] |
| **Overlap Coefficient** | [0.XX] | [Relevante se tamanhos muito diferentes] |
| Cardinalidade chave em A | [N distintos / N total] | [1:1 se iguais] |
| Cardinalidade chave em B | [N distintos / N total] | [1:1 se iguais] |
| Fator de explosão (M:N) | [X.Xx] | [comparar ao contrato de granularidade] |

**Tipo de join recomendado**: [INNER / LEFT / ...]
**Pré-agregação necessária?**: [Sim — agregar B por [chave] antes / Não]
**Risco principal**: [explosão / viés de sobrevivência / nenhum]

### Par A × C

[Repetir estrutura acima]

### Par B × C

[Repetir estrutura acima — incluir apenas se join direto B×C for relevante]

## Estratégia de join consolidada

### Ordem recomendada

```
[Âncora: tabela_A (1 linha/entidade)]
    │
    ├── LEFT JOIN tabela_B ON [chave] (pré-agregada por [chave])
    │   └── Coverage: [X%] | Explosão: Não
    │
    └── LEFT JOIN tabela_C ON [chave]
        └── Coverage: [X%] | Explosão: Não

Resultado esperado: [N] linhas (1 por entidade)
```

### Validações pós-join obrigatórias

- [ ] Count pós-join = count da âncora (sem explosão)
- [ ] Nenhuma chave duplicada após join
- [ ] % de NULLs em colunas de fontes secundárias = (1 - coverage)
- [ ] Distribuição da chave pré/pós join é estável

## Registros órfãos — análise de perfil

> ⚠️ Preencher apenas se Jaccard < 0.80 em algum par.

**Pergunta central**: Os registros que ficam de fora do join têm perfil
diferente dos que ficam? Se sim, o modelo treinado no inner join não
generalizará para a população completa.

| Segmento | N | % | Hipótese de causa |
|---|---|---|---|
| Órfãos de A (não estão em B) | [N] | [X%] | [ex.: clientes inativos sem transações] |
| Órfãos de B (não estão em A) | [N] | [X%] | [ex.: contas encerradas antes do cadastro] |

---

> **Interpretação**: Jaccard mede sobreposição de conjuntos, não segurança do join. Definir limites conforme a população esperada. Qualquer fator de explosão incompatível com a granularidade contratada exige investigação; pré-agregar apenas quando essa for a semântica correta.
