# Databricks notebook source
# Execute somente no Databricks Free e somente com catálogo/schema de laboratório.
# As células de escrita ficam desativadas até decisão explícita do usuário.
RUN_SETUP = False
LAB_CATALOG = "PREENCHER_CATALOGO_SINTETICO"
LAB_SCHEMA = "micromodelos_lab_sintetico"
LAB_TABLE = "eventos_mm_lab_sintetico"

if RUN_SETUP:
    if "spark" not in globals():
        raise RuntimeError("Spark indisponível")
    if LAB_CATALOG == "PREENCHER_CATALOGO_SINTETICO":
        raise ValueError("Escolha o catálogo sintético do Free antes da escrita")
    import re
    identifier = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,127}\Z")
    if not all(identifier.fullmatch(x) for x in (LAB_CATALOG, LAB_SCHEMA, LAB_TABLE)):
        raise ValueError("Identificador de laboratório fora do subconjunto MM03")
    schema_sql = f"`{LAB_CATALOG}`.`{LAB_SCHEMA}`"
    table_sql = f"{schema_sql}.`{LAB_TABLE}`"
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_sql}")
    rows = [
        ("entidade_a", "2026-09-01", "POSITIVO"),
        ("entidade_a", "2026-09-12", "POSITIVO"),
        ("entidade_b", "2026-09-03", "CONTRARIO"),
    ]
    frame = spark.createDataFrame(rows, ["id_entidade", "data_evento", "tipo_evento"])
    frame.write.mode("errorifexists").saveAsTable(table_sql)
    print("CREATED_SYNTHETIC_TABLE", table_sql)

# COMMAND ----------
# Limpeza manual posterior, somente após confirmar que a tabela acima foi criada
# por este notebook: DROP TABLE `catalogo_free`.`micromodelos_lab_sintetico`.`eventos_mm_lab_sintetico`.
# Não remova schema/catálogo nem objetos alheios por padrão.
