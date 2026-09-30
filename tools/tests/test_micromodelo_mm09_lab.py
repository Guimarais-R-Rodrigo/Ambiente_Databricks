from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import micromodelo_mm01_contract as mm01
import micromodelo_mm02_fingerprint as mm02
import micromodelo_mm09_lab as lab


class MM09GreenfieldLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = lab.run_greenfield_lab()
        cls.schema = mm01.load_schema(REPO / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")

    def test_uses_canonical_flow_spec_fingerprint_and_artifacts(self) -> None:
        result = self.report
        spec = result["spec"]
        self.assertEqual("OBJETIVO_CONHECIDO", result["mm04_mode"])
        self.assertEqual("ESCOPO_OBSERVADO", result["metadata_coverage"])
        self.assertFalse(result["metadata_catalog_complete"])
        self.assertEqual("EM_ESTUDO", spec["identidade"]["estado"]["fase_atual"])
        idea = result["spec_history"]["IDEIA"]
        discovery = result["spec_history"]["EM_DESCOBERTA"]
        self.assertEqual([], mm01.validate_spec(discovery, self.schema, previous_spec=idea))
        self.assertEqual([], mm01.validate_spec(spec, self.schema, previous_spec=discovery))
        self.assertEqual([], mm01.validate_spec(spec, self.schema))
        expected = mm02.calculate_spec_fingerprint(spec, self.schema).sha256
        self.assertEqual(expected, result["spec_fingerprint"])
        self.assertIn(expected, result["artifacts"]["notebook_source"])
        self.assertIn(expected, result["artifacts"]["readme_markdown"])
        self.assertEqual("NAO_INICIADA", spec["publicacao"]["status"])
        self.assertEqual("PENDENTE", spec["validacao"]["aprovacao_humana"]["status"])
        self.assertTrue(all(item["proveniencia"]["status"] == "PROPOSTO"
                            for item in spec["evidencias"] + spec["contra_evidencias"]))

    def test_known_synthetic_oracle_and_indeterminate_reasons(self) -> None:
        rows = {item["id_entidade"]: item for item in self.report["scoring"]["individual"]}
        self.assertEqual(("TRUE", 100), (rows["entidade_a"]["classificacao"],
                                           rows["entidade_a"]["score_heuristico_0_100"]))
        self.assertEqual(("FALSE", 0), (rows["entidade_b"]["classificacao"],
                                           rows["entidade_b"]["score_heuristico_0_100"]))
        self.assertEqual("EVIDENCIA_INSUFICIENTE", rows["entidade_c"]["motivo"])
        self.assertEqual("COBERTURA_INCOMPLETA", rows["entidade_d"]["motivo"])
        self.assertIsNone(rows["entidade_d"]["score_heuristico_0_100"])
        self.assertEqual(("FALSE", 60, 2, 1),
                         (rows["entidade_e"]["classificacao"],
                          rows["entidade_e"]["score_heuristico_0_100"],
                          rows["entidade_e"]["eventos_positivos"],
                          rows["entidade_e"]["eventos_contrarios"]))
        self.assertEqual("AUSENCIA_NAO_E_FALSE", rows["entidade_f"]["motivo"])
        self.assertEqual("INDETERMINADO", rows["entidade_f"]["classificacao"])

    def test_aggregate_reconciles_independent_of_reported_counts(self) -> None:
        rows = self.report["scoring"]["individual"]
        aggregate = self.report["scoring"]["aggregate"]
        self.assertEqual(6, len(rows))
        self.assertEqual(aggregate["populacao"], len({item["id_entidade"] for item in rows}))
        for label in ("TRUE", "FALSE", "INDETERMINADO"):
            self.assertEqual(sum(item["classificacao"] == label for item in rows),
                             aggregate["contagens"][label])
        self.assertEqual(len(rows), sum(aggregate["contagens"].values()))
        scores = [item["score_heuristico_0_100"] for item in rows
                  if item["score_heuristico_0_100"] is not None]
        self.assertEqual(aggregate["scores_emitidos"], len(scores))
        self.assertEqual(aggregate["score_media"], sum(scores) / len(scores))
        self.assertTrue(all(0 <= score <= 100 for score in scores))

    def test_no_mlflow_or_institutional_execution_is_claimed(self) -> None:
        result = self.report
        self.assertEqual("E0_SYNTHETIC_IN_MEMORY", result["environment"])
        self.assertEqual("HEURISTICA_FORCA_EVIDENCIA_NAO_PROBABILIDADE",
                         result["scoring"]["score_semantics"])
        self.assertEqual({"DEVELOPMENT", "VALIDATION", "SCORING"}, set(result["tracking"]))
        self.assertTrue(all(item == {"status": "NOT_RUN", "run_id": None}
                            for item in result["tracking"].values()))
        self.assertFalse(result["governance_handoff"]["publication_executed"])
        self.assertEqual("NOT_READY_VALIDATION_PENDING", result["governance_handoff"]["status"])

    def test_unknown_event_and_duplicate_population_fail_closed(self) -> None:
        spec = self.report["spec"]
        population, events = lab._synthetic_rows()
        bad_events = copy.deepcopy(events)
        bad_events.append({"event_id": "evento_extra", "id_entidade": "inexistente", "data_evento": "2026-09-09",
                           "tipo_evento": "POSITIVO"})
        with self.assertRaisesRegex(lab.LabError, "INVALID_EVENT"):
            lab.evaluate_synthetic_population(spec, population, bad_events)
        with self.assertRaisesRegex(lab.LabError, "INVALID_POPULATION"):
            lab.evaluate_synthetic_population(spec, population + [population[0]], events)

    def test_out_of_window_or_unknown_signal_fails_closed(self) -> None:
        spec = self.report["spec"]
        population, events = lab._synthetic_rows()
        changed = copy.deepcopy(events)
        changed[0]["data_evento"] = "2026-10-01"
        with self.assertRaisesRegex(lab.LabError, "EVENT_OUTSIDE_LAB_WINDOW"):
            lab.evaluate_synthetic_population(spec, population, changed)
        changed[0]["data_evento"] = "2026-09-01"
        changed[0]["tipo_evento"] = "DESCONHECIDO"
        with self.assertRaisesRegex(lab.LabError, "INVALID_EVENT"):
            lab.evaluate_synthetic_population(spec, population, changed)

    def test_invalid_or_wrong_phase_spec_cannot_be_scored(self) -> None:
        population, events = lab._synthetic_rows()
        invalid = copy.deepcopy(self.report["spec"])
        invalid["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] = "FALSE"
        with self.assertRaisesRegex(lab.LabError, "INVALID_MM01_LAB_SPEC"):
            lab.evaluate_synthetic_population(invalid, population, events)
        wrong_phase = copy.deepcopy(self.report["spec"])
        wrong_phase["identidade"]["estado"].update(
            {"fase_anterior": "IDEIA", "fase_atual": "EM_DESCOBERTA"}
        )
        with self.assertRaisesRegex(lab.LabError, "LAB_PHASE_REQUIRED"):
            lab.evaluate_synthetic_population(wrong_phase, population, events)

    def test_material_profile_changes_are_rejected_but_editorial_change_is_allowed(self) -> None:
        population, events = lab._synthetic_rows()
        baseline = self.report["spec"]
        variants = []
        changed = copy.deepcopy(baseline)
        changed["classificacao"]["limiares"][0]["operador"] = "GT"
        variants.append(changed)
        changed = copy.deepcopy(baseline)
        changed["entidade"]["referencia_temporal"] = "janela sintética fixa de outubro de 2026"
        variants.append(changed)
        changed = copy.deepcopy(baseline)
        changed["classificacao"]["semantica"]["quando_false"] = "dois eventos CONTRARIO observados na janela"
        variants.append(changed)
        for changed in variants:
            with self.subTest(fingerprint=mm02.calculate_spec_fingerprint(changed, self.schema).sha256):
                self.assertEqual([], mm01.validate_spec(changed, self.schema))
                self.assertNotEqual(self.report["spec_fingerprint"],
                                    mm02.calculate_spec_fingerprint(changed, self.schema).sha256)
                with self.assertRaisesRegex(lab.LabError, "LAB_PROFILE_MISMATCH"):
                    lab.evaluate_synthetic_population(changed, population, events)
        editorial = copy.deepcopy(baseline)
        editorial["negocio"]["objetivo"] = "objetivo editorial atualizado do piloto sintético"
        self.assertEqual([], mm01.validate_spec(editorial, self.schema))
        self.assertEqual(self.report["spec_fingerprint"],
                         mm02.calculate_spec_fingerprint(editorial, self.schema).sha256)
        self.assertEqual(lab.evaluate_synthetic_population(baseline, population, events),
                         lab.evaluate_synthetic_population(editorial, population, events))

    def test_explicit_counter_evidence_precedes_incomplete_coverage(self) -> None:
        population, events = lab._synthetic_rows()
        events.append({"event_id": "evento_008", "id_entidade": "entidade_d",
                       "data_evento": "2026-09-08", "tipo_evento": "CONTRARIO"})
        rows, _ = lab.evaluate_synthetic_population(self.report["spec"], population, events)
        target = next(item for item in rows if item["id_entidade"] == "entidade_d")
        self.assertEqual("FALSE", target["classificacao"])
        self.assertEqual("CONTRA_EVIDENCIA_EXPLICITA", target["motivo"])
        self.assertIsNone(target["score_heuristico_0_100"])

    def test_duplicate_event_id_is_rejected_before_double_counting(self) -> None:
        population, events = lab._synthetic_rows()
        duplicated = copy.deepcopy(events)
        duplicated.append(copy.deepcopy(events[0]))
        with self.assertRaisesRegex(lab.LabError, "DUPLICATE_EVENT_ID"):
            lab.evaluate_synthetic_population(self.report["spec"], population, duplicated)


if __name__ == "__main__":
    unittest.main()
