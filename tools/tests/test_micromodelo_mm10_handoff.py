"""Handoff MM10 preserva autoridade externa e contagens reconciliadas."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import micromodelo_mm01_contract as mm01
import micromodelo_mm09_lab as mm09
import micromodelo_mm10_handoff as mm10


class HandoffTests(unittest.TestCase):
    def test_pilot_handoff_is_draft_and_not_publication(self):
        pilot = mm09.run_greenfield_lab()
        schema = mm01.load_schema(ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")
        handoff = mm10.prepare_handoff(pilot["spec"], schema,
                                       pilot["scoring"]["aggregate"])
        self.assertEqual("DRAFT_NOT_SUBMITTED", handoff["status"])
        self.assertEqual("SUPPLIED_UNVERIFIED", handoff["aggregate"]["status"])
        self.assertEqual(pilot["spec_fingerprint"], handoff["spec_fingerprint"])
        self.assertFalse(handoff["published"])
        self.assertIsNone(handoff["run_ref"])

    def test_rejects_unreconciled_count(self):
        pilot = mm09.run_greenfield_lab()
        schema = mm01.load_schema(ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")
        aggregate = copy.deepcopy(pilot["scoring"]["aggregate"])
        aggregate["contagens"]["TRUE"] += 1
        with self.assertRaisesRegex(mm10.HandoffError, "UNRECONCILED_COUNTS"):
            mm10.prepare_handoff(pilot["spec"], schema, aggregate)

    def test_zero_aggregate_is_not_claimed_as_measured(self):
        pilot = mm09.run_greenfield_lab()
        schema = mm01.load_schema(ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")
        empty = {"populacao": 0,
                 "contagens": {"TRUE": 0, "FALSE": 0, "INDETERMINADO": 0},
                 "scores_emitidos": 0, "score_min": None, "score_max": None,
                 "score_media": None}
        handoff = mm10.prepare_handoff(pilot["spec"], schema, empty)
        self.assertEqual("SUPPLIED_UNVERIFIED", handoff["aggregate"]["status"])
        self.assertIsNone(handoff["run_ref"])

    def test_output_contract_is_detached_from_spec(self):
        pilot = mm09.run_greenfield_lab()
        schema = mm01.load_schema(ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")
        handoff = mm10.prepare_handoff(pilot["spec"], schema)
        before = copy.deepcopy(pilot["spec"]["saida"])
        handoff["output_contract"]["estudo"]["campo_classificacao"] = "alterado"
        self.assertEqual(before, pilot["spec"]["saida"])


if __name__ == "__main__":
    unittest.main()
