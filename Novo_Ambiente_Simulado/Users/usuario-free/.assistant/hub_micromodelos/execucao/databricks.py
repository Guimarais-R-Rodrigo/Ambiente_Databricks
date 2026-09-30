"""Adapter MM03 para metadata Unity Catalog via Spark.sql injetado.

Somente SELECTs de views allowlisted de <catalog>.information_schema. Este
arquivo não conecta por si, não lê tabelas de dados e não prova E1. Cada stream
é materializado uma vez, com LIMIT 2001, para paginar sem misturar páginas de
consultas diferentes. ``snapshot_id`` identifica essa observação local, não um
snapshot transacional do Unity Catalog entre as diferentes views.

Referências oficiais (consultadas em 2026-09-29):
https://docs.databricks.com/aws/en/sql/language-manual/information-schema/schemata
https://docs.databricks.com/aws/en/sql/language-manual/information-schema/tables
https://docs.databricks.com/aws/en/sql/language-manual/information-schema/columns
https://docs.databricks.com/aws/en/sql/language-manual/information-schema/column_tags
https://docs.databricks.com/aws/en/sql/language-manual/information-schema/table_constraints
https://docs.databricks.com/aws/en/sql/language-manual/information-schema/key_column_usage
"""
from __future__ import annotations

import uuid
from typing import Any

from . import metadados as mm03

_MAX_RAW_ROWS = 2001  # max_items MM03 <= 2000; linha extra sinaliza truncamento.
_SCOPE_LENGTH = {"schemas": 0, "objects": 1, "columns": 2,
                 "column_tags": 2, "constraints": 2}
_TABLE_TYPES = {"VIEW": "VIEW", "MATERIALIZED_VIEW": "VIEW",
                "MANAGED": "TABLE", "EXTERNAL": "TABLE", "FOREIGN": "TABLE",
                "STREAMING_TABLE": "TABLE", "MANAGED_SHALLOW_CLONE": "TABLE",
                "EXTERNAL_SHALLOW_CLONE": "TABLE"}
_CONSTRAINT_TYPES = {"PRIMARY KEY": "PRIMARY_KEY", "FOREIGN KEY": "FOREIGN_KEY"}


def _row_dict(row: Any) -> dict[str, Any]:
    if type(row) is dict:
        return row
    if callable(getattr(row, "asDict", None)):
        value = row.asDict(recursive=False)
        if type(value) is dict:
            return value
    raise mm03.MetadataError("INVALID_SPARK_ROW")


def _field(row: dict[str, Any], name: str) -> Any:
    # Spark Row aliases preserve spelling; no positional fallback or SELECT *.
    if name not in row:
        raise mm03.MetadataError("MISSING_METADATA_FIELD")
    return row[name]


def _error_status(exc: Exception) -> str | None:
    """Classifica somente códigos estruturados; nunca reproduz mensagem/SQL."""
    codes = []
    for method in ("getCondition", "getErrorClass", "getSqlState"):
        reader = getattr(exc, method, None)
        if callable(reader):
            try:
                code = reader()
            except Exception:
                continue
            if type(code) is str:
                codes.append(code.upper())
    if any("PERMISSION" in c or "PRIVILEGE" in c or c == "42501" for c in codes):
        return "DENIED"
    if any("TABLE_OR_VIEW_NOT_FOUND" in c or "SCHEMA_NOT_FOUND" in c
           or "UNSUPPORTED_FEATURE" in c or c == "42P01" for c in codes):
        return "UNAVAILABLE"
    return None


class DatabricksMetadataProvider:
    """MetadataProvider MM03 sobre um SparkSession confiável fornecido pelo caller.

    O binding e os scopes usam o envelope conservador de identificadores MM03.
    ``capabilities`` reflete o resultado das views consultadas neste provider.
    ``table_tags`` fica NOT_IMPLEMENTED: objetos têm ``tags=None``, nunca lista
    vazia que fingiria inspeção. Se COLUMN_TAGS ou as views de constraints não
    existirem/forem negadas, retornamos UNAVAILABLE/DENIED, sem fallback a dados.
    Descrição de constraint fica NOT_COLLECTED: a view no Free observada em
    2026-09-29 não expôs ``comment`` apesar da documentação geral da view.
    """

    def __init__(self, spark: Any, binding: mm03.Binding) -> None:
        if not callable(getattr(spark, "sql", None)):
            raise mm03.MetadataError("INVALID_SPARK")
        if type(binding) is not mm03.Binding:
            raise mm03.MetadataError("INVALID_BINDING")
        self.spark = spark
        self.binding = binding
        self.snapshot_id = "obs_" + uuid.uuid4().hex
        self.capabilities: dict[str, str] = {
            "table_tags": "NOT_IMPLEMENTED", "constraint_comment": "NOT_COLLECTED"}
        self._streams: dict[tuple[str, tuple[str, ...]], tuple[str, list[dict[str, Any]]]] = {}

    def _query(self, operation: str, scope: tuple[str, ...]) -> str:
        catalog = self.binding.physical_catalog
        prefix = f"`{catalog}`.information_schema"
        cat = catalog.lower()
        if operation == "schemas":
            return (f"SELECT schema_name, comment FROM {prefix}.schemata "
                    f"WHERE catalog_name = '{cat}' ORDER BY schema_name LIMIT {_MAX_RAW_ROWS}")
        schema = scope[0].lower()
        if operation == "objects":
            return (f"SELECT table_name, table_type, comment FROM {prefix}.tables "
                    f"WHERE table_catalog = '{cat}' AND table_schema = '{schema}' "
                    f"ORDER BY table_name LIMIT {_MAX_RAW_ROWS}")
        obj = scope[1].lower()
        if operation == "columns":
            return (f"SELECT column_name, full_data_type, is_nullable, comment "
                    f"FROM {prefix}.columns WHERE table_catalog = '{cat}' "
                    f"AND table_schema = '{schema}' AND table_name = '{obj}' "
                    f"ORDER BY ordinal_position LIMIT {_MAX_RAW_ROWS}")
        if operation == "column_tags":
            return (f"SELECT column_name, tag_name, tag_value FROM {prefix}.column_tags "
                    f"WHERE catalog_name = '{cat}' AND schema_name = '{schema}' "
                    f"AND table_name = '{obj}' ORDER BY column_name, tag_name, tag_value "
                    f"LIMIT {_MAX_RAW_ROWS}")
        if operation == "constraints":
            return (f"SELECT tc.constraint_name, tc.constraint_type, "
                    f"CAST(NULL AS STRING) AS comment, "
                    f"ku.column_name, ku.ordinal_position FROM {prefix}.table_constraints tc "
                    f"LEFT JOIN {prefix}.key_column_usage ku ON "
                    f"tc.constraint_catalog = ku.constraint_catalog AND "
                    f"tc.constraint_schema = ku.constraint_schema AND "
                    f"tc.constraint_name = ku.constraint_name "
                    f"WHERE tc.table_catalog = '{cat}' AND tc.table_schema = '{schema}' "
                    f"AND tc.table_name = '{obj}' "
                    f"ORDER BY tc.constraint_name, ku.ordinal_position LIMIT {_MAX_RAW_ROWS}")
        raise mm03.MetadataError("UNKNOWN_OPERATION")

    def _map(self, operation: str, raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if operation == "schemas":
            return [{"name": _field(r, "schema_name"),
                     "description": _field(r, "comment")} for r in raw]
        if operation == "objects":
            result = []
            for r in raw:
                kind = _field(r, "table_type")
                if kind not in _TABLE_TYPES:
                    raise mm03.MetadataError("UNSUPPORTED_TABLE_TYPE")
                result.append({"name": _field(r, "table_name"),
                               "object_type": _TABLE_TYPES[kind],
                               "description": _field(r, "comment"), "tags": None})
            return result
        if operation == "columns":
            result = []
            for r in raw:
                nullable = _field(r, "is_nullable")
                if nullable not in ("YES", "NO"):
                    raise mm03.MetadataError("INVALID_NULLABILITY")
                result.append({"name": _field(r, "column_name"),
                               "data_type": _field(r, "full_data_type"),
                               "nullable": nullable == "YES",
                               "description": _field(r, "comment")})
            return result
        if operation == "column_tags":
            grouped: dict[str, list[dict[str, str]]] = {}
            for r in raw:
                name = _field(r, "column_name")
                grouped.setdefault(name, []).append({"key": _field(r, "tag_name"),
                                                      "value": _field(r, "tag_value")})
            if any(len(tags) > 32 for tags in grouped.values()):
                raise mm03.MetadataError("TAG_LIMIT")
            return [{"column": name, "tags": tags}
                    for name, tags in sorted(grouped.items())]
        grouped_constraints: dict[str, dict[str, Any]] = {}
        for r in raw:
            name = _field(r, "constraint_name")
            kind = _field(r, "constraint_type")
            # KEY_COLUMN_USAGE documenta colunas de PK/FK; outras classes não
            # podem ser declaradas completas por este adapter.
            if kind not in _CONSTRAINT_TYPES:
                raise mm03.MetadataError("UNSUPPORTED_CONSTRAINT_KIND")
            entry = grouped_constraints.setdefault(name, {"name": name,
                "kind": _CONSTRAINT_TYPES[kind], "columns": [],
                "description": _field(r, "comment")})
            column = _field(r, "column_name")
            if column is None:
                raise mm03.MetadataError("INCOMPLETE_CONSTRAINT")
            entry["columns"].append(column)
        return [grouped_constraints[name] for name in sorted(grouped_constraints)]

    def _materialize(self, operation: str, scope: tuple[str, ...]
                     ) -> tuple[str, list[dict[str, Any]]]:
        query = self._query(operation, scope)
        try:
            raw = [_row_dict(row) for row in self.spark.sql(query).collect()]
        except Exception as exc:
            status = _error_status(exc)
            if status:
                self.capabilities[operation] = status
                return status, []
            raise mm03.MetadataError("METADATA_QUERY_FAILED") from None
        if len(raw) > _MAX_RAW_ROWS:
            raise mm03.MetadataError("UNBOUNDED_SPARK_RESULT")
        # Agregações precisam de todas as tags/linhas da constraint. O limite
        # atingido não autoriza emitir grupo parcial como coleção completa.
        if operation in {"column_tags", "constraints"} and len(raw) == _MAX_RAW_ROWS:
            self.capabilities[operation] = "UNAVAILABLE_LIMIT"
            return "UNAVAILABLE", []
        try:
            rows = self._map(operation, raw)
            # O envelope MM03 rejeita identificadores como `eventos-sinteticos`.
            # Não os renomeie nem emita uma lista aparentemente completa: uma
            # única linha irrepresentável torna o stream indisponível.
            for row in rows:
                mm03._record(operation, row)
        except mm03.MetadataError:
            self.capabilities[operation] = "UNAVAILABLE_MAPPING"
            return "UNAVAILABLE", []
        self.capabilities[operation] = "AVAILABLE"
        return "OK", rows

    def fetch_page(self, operation: str, catalog: str, scope: tuple[str, ...],
                   token: str | None, page_size: int) -> mm03.Page:
        if operation not in _SCOPE_LENGTH:
            raise mm03.MetadataError("UNKNOWN_OPERATION")
        if catalog != self.binding.physical_catalog:
            raise mm03.MetadataError("BINDING_MISMATCH")
        if type(scope) is not tuple or len(scope) != _SCOPE_LENGTH[operation]:
            raise mm03.MetadataError("INVALID_SCOPE")
        for item in scope:
            mm03._identifier(item)
        if type(page_size) is not int or not 1 <= page_size <= 100:
            raise mm03.MetadataError("INVALID_LIMIT")
        key = (operation, scope)
        if token is None:
            if key not in self._streams:
                self._streams[key] = self._materialize(operation, scope)
            start = 0
        else:
            if key not in self._streams or not token.isascii() or not token.isdigit():
                raise mm03.MetadataError("INVALID_PAGE_TOKEN")
            start = int(token)
            if token != str(start) or start < 0:
                raise mm03.MetadataError("INVALID_PAGE_TOKEN")
        status, rows = self._streams[key]
        if status != "OK":
            if token is not None:
                raise mm03.MetadataError("INVALID_PAGE_TOKEN")
            return mm03.Page(catalog, self.snapshot_id, status, [])
        if start > len(rows):
            raise mm03.MetadataError("INVALID_PAGE_TOKEN")
        end = min(start + page_size, len(rows))
        next_token = str(end) if end < len(rows) else None
        return mm03.Page(catalog, self.snapshot_id, "OK", rows[start:end], next_token)
