"""Equivalência conservadora MM12 só com legados fictícios."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import micromodelo_mm12_migration_lab as mm12


def row(key: str, classification: str, score: int | None):
    return {"fixture_namespace": "MM12_FICTICIO", "synthetic": True,
            "id_entidade": key, "classificacao": classification, "score": score}


class MigrationLabTests(unittest.TestCase):
    def test_equivalent_and_divergent_are_distinct(self):
        before = [row("a", "TRUE", 80), row("b", "INDETERMINADO", None)]
        same = mm12.rehearse_equivalence(before, copy.deepcopy(before))
        self.assertEqual("EQUIVALENT_LAB", same["status"])
        self.assertFalse(same["corporate_v1_verified"])
        after = [row("a", "FALSE", 80), row("c", "INDETERMINADO", None)]
        different = mm12.rehearse_equivalence(before, after)
        self.assertEqual("DIVERGENT_LAB", different["status"])
        self.assertEqual(["b"], different["missing_keys"])
        self.assertEqual(["c"], different["extra_keys"])
        self.assertEqual(["a"], different["changed_keys"])

    def test_rejects_non_fixture_and_duplicate(self):
        with self.assertRaisesRegex(mm12.MigrationLabError, "EMPTY_COMPARISON"):
            mm12.rehearse_equivalence([], [])
        bad = row("a", "TRUE", 80)
        bad["synthetic"] = False
        with self.assertRaisesRegex(mm12.MigrationLabError, "NON_SYNTHETIC_INPUT"):
            mm12.rehearse_equivalence([bad], [])
        with self.assertRaisesRegex(mm12.MigrationLabError, "INVALID_OR_DUPLICATE_KEY"):
            mm12.rehearse_equivalence([row("a", "TRUE", 80)] * 2, [])


if __name__ == "__main__":
    unittest.main()
