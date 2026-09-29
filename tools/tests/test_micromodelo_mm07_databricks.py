"""Contrato E0 do adapter SQL; fake Spark não prova Databricks Free."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import micromodelo_mm03_metadata as mm03
import micromodelo_mm07_databricks as adapter


class SqlFailure(Exception):
    def __init__(self, code):
        self.code = code

    def getErrorClass(self):
        return self.code


class FakeFrame:
    def __init__(self, rows):
        self.rows = rows

    def collect(self):
        return self.rows


class FakeSpark:
    """Inspeciona o SQL construído antes de devolver metadata sintética."""
    def __init__(self, rows=None, errors=None):
        self.rows = rows or {}
        self.errors = errors or {}
        self.queries = []

    def sql(self, query):
        self.queries.append(query)
        self.assert_safe(query)
        view = re.search(r"FROM `laboratorio`\.information_schema\.([a-z_]+)", query)
        name = view.group(1)
        if name in self.errors:
            raise SqlFailure(self.errors[name])
        return FakeFrame(self.rows.get(name, []))

    @staticmethod
    def assert_safe(query):
        assert re.fullmatch(r"[\x20-\x7e]+", query), "SQL deve ser ASCII imprimível"
        assert "SELECT " in query and " LIMIT 2001" in query
        assert "SELECT *" not in query and "COUNT(" not in query.upper()
        assert ";" not in query and "--" not in query and "/*" not in query
        assert "`laboratorio`.information_schema." in query
        assert not re.search(r"(?:FROM|JOIN)\s+(?!`laboratorio`\.information_schema)", query,
                             re.IGNORECASE)
        views = re.findall(r"(?:FROM|JOIN) `laboratorio`\.information_schema\.([a-z_]+)",
                           query, re.IGNORECASE)
        assert views and set(views) <= {"schemata", "tables", "columns",
                                       "column_tags", "table_constraints",
                                       "key_column_usage"}


def synthetic_rows():
    return {
        "schemata": [{"schema_name": "crm_sintetico", "comment": "Schema fictício"}],
        "tables": [{"table_name": "eventos_sinteticos", "table_type": "MANAGED",
                    "comment": "Eventos fictícios"}],
        "columns": [{"column_name": "id_entidade", "full_data_type": "STRING",
                     "is_nullable": "NO", "comment": "Chave sintética"},
                    {"column_name": "data_evento", "full_data_type": "TIMESTAMP",
                     "is_nullable": "YES", "comment": None}],
        "column_tags": [{"column_name": "id_entidade", "tag_name": "papel",
                         "tag_value": "identificador sintético"}],
        "table_constraints": [{"constraint_name": "pk_evento",
                               "constraint_type": "PRIMARY KEY", "comment": None,
                               "column_name": "id_entidade", "ordinal_position": 1}],
    }


class DatabricksAdapterTests(unittest.TestCase):
    def provider(self, rows=None, errors=None):
        spark = FakeSpark(rows if rows is not None else synthetic_rows(), errors)
        return spark, adapter.DatabricksMetadataProvider(spark, mm03.Binding("laboratorio"))

    def test_progressive_collector_maps_allowlisted_views(self):
        spark, provider = self.provider()
        collector = mm03.MetadataCollector(provider, mm03.Binding("laboratorio"))
        discovery = collector.discover(["crm_sintetico"])
        self.assertEqual(["schemata", "tables"],
                         [re.search(r"FROM `laboratorio`\.information_schema\.([a-z_]+)", q)
                          .group(1) for q in spark.queries])
        self.assertEqual("TABLE", discovery["objects"]["crm_sintetico"]["items"][0]
                         ["object_type"])
        self.assertIsNone(discovery["objects"]["crm_sintetico"]["items"][0]["tags"])
        details = collector.details([("crm_sintetico", "eventos_sinteticos")])
        result = details["crm_sintetico.eventos_sinteticos"]
        columns = {item["name"]: item for item in result["columns"]["items"]}
        self.assertFalse(columns["id_entidade"]["nullable"])
        self.assertTrue(columns["data_evento"]["nullable"])
        self.assertEqual("papel", result["column_tags"]["items"][0]["tags"][0]
                         ["key"]["text"])
        self.assertEqual("NOT_VERIFIED", result["constraints"]["items"][0]["enforcement"])
        self.assertEqual("OBSERVED", collector.envelope(discovery, details)
                         ["observation_status"])
        self.assertEqual("NOT_IMPLEMENTED", provider.capabilities["table_tags"])
        self.assertEqual(5, len(spark.queries))

    def test_pagination_has_bounded_query_and_stable_batch_id(self):
        rows = synthetic_rows()
        rows["schemata"] = [{"schema_name": f"s_{i}", "comment": None} for i in range(3)]
        spark, provider = self.provider(rows)
        first = provider.fetch_page("schemas", "laboratorio", (), None, 1)
        second = provider.fetch_page("schemas", "laboratorio", (), first.next_token, 1)
        third = provider.fetch_page("schemas", "laboratorio", (), second.next_token, 1)
        self.assertEqual(["s_0", "s_1", "s_2"],
                         [first.items[0]["name"], second.items[0]["name"],
                          third.items[0]["name"]])
        self.assertEqual(first.snapshot_id, third.snapshot_id)
        self.assertIsNone(third.next_token)
        self.assertEqual(1, len(spark.queries))

    def test_scopes_and_binding_rejected_before_sql(self):
        spark, provider = self.provider()
        for operation, catalog, scope in (
            ("objects", "outro", ("crm_sintetico",)),
            ("objects", "laboratorio", ("x';drop",)),
            ("columns", "laboratorio", ("crm_sintetico",)),
            ("query", "laboratorio", ()),
        ):
            with self.subTest(operation=operation, scope=scope), self.assertRaises(mm03.MetadataError):
                provider.fetch_page(operation, catalog, scope, None, 50)
        self.assertEqual([], spark.queries)

    def test_optional_view_unavailable_is_not_empty_observation(self):
        spark, provider = self.provider(errors={"column_tags": "TABLE_OR_VIEW_NOT_FOUND",
                                                "table_constraints": "UNSUPPORTED_FEATURE"})
        collector = mm03.MetadataCollector(provider, mm03.Binding("laboratorio"))
        discovery = collector.discover(["crm_sintetico"])
        details = collector.details([("crm_sintetico", "eventos_sinteticos")])
        item = details["crm_sintetico.eventos_sinteticos"]
        self.assertEqual("UNAVAILABLE", item["column_tags"]["status"])
        self.assertEqual("UNAVAILABLE", item["constraints"]["status"])
        self.assertEqual("PARTIAL_OBSERVATION", collector.envelope(discovery, details)
                         ["observation_status"])
        self.assertEqual("UNAVAILABLE", provider.capabilities["column_tags"])

    def test_permission_failure_is_explicit_and_unknown_error_fails_closed(self):
        spark, provider = self.provider(errors={"schemata": "INSUFFICIENT_PRIVILEGES"})
        page = provider.fetch_page("schemas", "laboratorio", (), None, 50)
        self.assertEqual("DENIED", page.status)
        self.assertEqual([], page.items)
        self.assertEqual("DENIED", provider.capabilities["schemas"])
        spark2, provider2 = self.provider(errors={"schemata": "SOMETHING_ELSE"})
        with self.assertRaisesRegex(mm03.MetadataError, "METADATA_QUERY_FAILED"):
            provider2.fetch_page("schemas", "laboratorio", (), None, 50)
        self.assertEqual(1, len(spark2.queries))

    def test_constraints_with_unsupported_class_are_unavailable(self):
        rows = synthetic_rows()
        rows["table_constraints"] = [{"constraint_name": "u_exemplo",
                                       "constraint_type": "UNIQUE", "comment": None,
                                       "column_name": None, "ordinal_position": None}]
        _, provider = self.provider(rows)
        page = provider.fetch_page("constraints", "laboratorio",
                                   ("crm_sintetico", "eventos_sinteticos"), None, 50)
        self.assertEqual("UNAVAILABLE", page.status)
        self.assertEqual("UNAVAILABLE_MAPPING", provider.capabilities["constraints"])

    def test_unrepresentable_object_name_fails_closed_without_renaming(self):
        rows = synthetic_rows()
        rows["tables"].append({"table_name": "eventos-sinteticos", "table_type": "MANAGED",
                               "comment": "Nome válido no UC, fora do envelope MM03"})
        spark, provider = self.provider(rows)
        collector = mm03.MetadataCollector(provider, mm03.Binding("laboratorio"))
        discovery = collector.discover(["crm_sintetico"])
        objects = discovery["objects"]["crm_sintetico"]
        self.assertEqual("UNAVAILABLE", objects["status"])
        self.assertEqual([], objects["items"])
        self.assertEqual("UNAVAILABLE_MAPPING", provider.capabilities["objects"])
        self.assertEqual("PARTIAL_OBSERVATION", collector.envelope(discovery, {})
                         ["observation_status"])
        self.assertEqual(2, len(spark.queries))

    def test_unrepresentable_column_name_fails_closed_without_renaming(self):
        rows = synthetic_rows()
        rows["columns"].append({"column_name": "customer-id", "full_data_type": "STRING",
                                "is_nullable": "YES", "comment": None})
        _, provider = self.provider(rows)
        collector = mm03.MetadataCollector(provider, mm03.Binding("laboratorio"))
        discovery = collector.discover(["crm_sintetico"])
        details = collector.details([("crm_sintetico", "eventos_sinteticos")])
        columns = details["crm_sintetico.eventos_sinteticos"]["columns"]
        self.assertEqual("UNAVAILABLE", columns["status"])
        self.assertEqual([], columns["items"])
        self.assertEqual("UNAVAILABLE_MAPPING", provider.capabilities["columns"])
        self.assertEqual("PARTIAL_OBSERVATION", collector.envelope(discovery, details)
                         ["observation_status"])


if __name__ == "__main__":
    unittest.main()
