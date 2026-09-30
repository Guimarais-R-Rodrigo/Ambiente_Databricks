"""Catálogo MM13 sintético: derivação, identidade e impacto declarado."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import micromodelo_mm01_contract as mm01
import micromodelo_mm13_catalog as mm13


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = mm01.load_document(ROOT / "docs/sprints/micromodelos/MM01/micromodelo.template.yaml")
        cls.schema = mm01.load_schema(ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")

    def test_catalog_is_derived_and_impact_is_scoped(self):
        first = copy.deepcopy(self.spec)
        first["identidade"]["nome"] = "modelo-primeiro"
        first["fontes"] = [{
            "id": "fonte_001", "catalogo_ref": "CATALOGO_PRODUTO", "schema": "lab",
            "objeto": "eventos", "tipo_objeto": "TABLE", "campos": ["id_cliente"],
            "papel": "APOIO", "proveniencia": {"status": "DESCOBERTO",
            "origem": "metadata sintética", "referencia": "snapshot_lab",
            "observado_em_utc": None, "aprovacao": None, "medicao": None},
        }]
        second = copy.deepcopy(self.spec)
        second["identidade"]["nome"] = "modelo-segundo"
        catalog = mm13.build_catalog([second, first], self.schema)
        self.assertEqual(["modelo-primeiro", "modelo-segundo"], [x["nome"] for x in catalog])
        self.assertTrue(all(x["execution_status"] == "NOT_OBSERVED" for x in catalog))
        impact = mm13.impact_by_source(catalog, catalogo_ref="CATALOGO_PRODUTO",
                                       schema="lab", objeto="eventos")
        self.assertEqual(["modelo-primeiro"], [x["nome"] for x in impact["declared_consumers"]])
        self.assertFalse(impact["runtime_lineage_verified"])

    def test_rejects_duplicate_and_invalid_spec(self):
        with self.assertRaisesRegex(mm13.CatalogError, "DUPLICATE_IDENTITY_VERSION"):
            mm13.build_catalog([self.spec, copy.deepcopy(self.spec)], self.schema)
        invalid = copy.deepcopy(self.spec)
        invalid["publicacao"]["autoridade"] = "AUTO"
        with self.assertRaisesRegex(mm13.CatalogError, "INVALID_MM01_SPEC"):
            mm13.build_catalog([invalid], self.schema)


if __name__ == "__main__":
    unittest.main()
