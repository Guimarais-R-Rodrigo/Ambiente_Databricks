# Databricks notebook source
"""Exemplo sintético de contexto: sem join, gravação ou promoção."""
from hub_scripts.skill_execution.domain_context import validate_temporal_context

result = validate_temporal_context(
    pit="APPLICABLE",
    decision_at="2026-01-10T00:00:00Z",
    temporal={"reference_column":"reference_at", "availability_column":"available_at",
              "lag_kind":"CONSTANT", "lag_days":1, "boundary":"LE", "timezone":"UTC",
              "tie_break":"REJECT", "bitemporal":False},
)
assert result["join_executed"] is False
print(result)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Saída observada em Python local — 24/09/2026
# MAGIC A saída valida apenas metadados e mantém `join_executed=False`; nenhuma fonte é consultada.
# MAGIC ```text
# MAGIC {'schema_version': 'SER-TEMPORAL-CONTEXT-1', 'pit': 'APPLICABLE', 'decision_at': '2026-01-10T00:00:00+00:00', 'reason': None, 'temporal': {'reference_column': 'reference_at', 'availability_column': 'available_at', 'lag_kind': 'CONSTANT', 'lag_days': 1, 'boundary': 'LE', 'timezone': 'UTC', 'tie_break': 'REJECT', 'bitemporal': False}, 'join_executed': False}
# MAGIC ```
