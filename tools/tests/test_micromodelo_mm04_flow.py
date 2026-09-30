from __future__ import annotations

import json
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import micromodelo_mm01_contract as mm01
import micromodelo_mm03_metadata as mm03
import micromodelo_mm04_flow as flow

FIXTURE = REPO / "tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json"
SCRIPT = REPO / "tools/micromodelo_mm04_flow.py"


class MM04FlowTests(unittest.TestCase):
    def setUp(self):
        self.fixture, _ = mm03.load_fixture(FIXTURE)
        self.brief = flow.KnownObjective(
            "teste-mm04", "Estudo sintético", "Característica a estudar",
            "Avaliar uma característica no cenário sintético.",
            "Definição operacional proposta e pendente de validação.",
            "pedido_sintetico_001", "2026-09-29T00:00:00Z",
        )

    def known(self, fixture=None, candidates=None):
        return flow.known_objective(
            fixture or self.fixture, "catalogo_sintetico", ["crm_sintetico"],
            candidates if candidates is not None else
            [("crm_sintetico", "eventos_sinteticos")], self.brief,
        )

    def proposal(self, characteristic="Eventos sintéticos recentes",
                 source="eventos_sinteticos"):
        return flow.OpportunityProposal(
            characteristic, "Revisão humana de campanhas", "Clientes sintéticos",
            "entidade por mês", "data de referência", "trinta dias",
            (("crm_sintetico", source),),
        )

    def test_known_objective_is_valid_mm01_pre_study_and_mm02_fingerprinted(self):
        result = self.known()
        spec = result["spec"]
        self.assertEqual([], mm01.validate_spec(spec, mm01.load_schema(flow.SCHEMA)))
        self.assertEqual("IDEIA", spec["identidade"]["estado"]["fase_atual"])
        self.assertEqual("DESCOBERTO", spec["fontes"][0]["proveniencia"]["status"])
        self.assertEqual("APOIO", spec["fontes"][0]["papel"])
        self.assertEqual([], spec["evidencias"])
        self.assertEqual("PENDENTE", spec["validacao"]["status"])
        self.assertEqual(64, len(result["fingerprint"]["sha256"]))
        self.assertEqual(["schemas", "objects", "columns", "column_tags", "constraints"],
                         [x["operation"] for x in result["metadata"]["calls"]])
        self.assertFalse(result["metadata"]["metadata_is_instruction"])
        self.assertFalse(result["metadata"]["data_access_authorized"])
        records = spec["proveniencia"]["registros"]
        self.assertIn("negocio.objetivo", {item["alvo"] for item in records})
        self.assertIn("identidade.titulo", {item["alvo"] for item in records})
        self.assertNotIn("entidade.tipo", {item["alvo"] for item in records})
        for item in records:
            self.assertEqual("PROPOSTO", item["proveniencia"]["status"])
            self.assertEqual("briefing fornecido", item["proveniencia"]["origem"])
            self.assertEqual(self.brief.request_ref, item["proveniencia"]["referencia"])
            self.assertIsNone(item["proveniencia"]["aprovacao"])
            self.assertIsNone(item["proveniencia"]["medicao"])

    def test_injected_description_and_tag_cannot_change_brief_scope_or_approval(self):
        result = self.known(candidates=[("crm_sintetico", "apoio_sintetico")])
        spec = result["spec"]
        self.assertEqual(self.brief.objective, spec["negocio"]["objetivo"])
        self.assertEqual("APOIO", spec["fontes"][0]["papel"])
        self.assertEqual("DESCOBERTO", spec["fontes"][0]["proveniencia"]["status"])
        self.assertEqual([], spec["fontes"][0]["campos"])
        self.assertEqual("UNAVAILABLE", result["metadata"]["details"]
                         ["crm_sintetico.apoio_sintetico"]["columns"]["status"])
        self.assertEqual("NAO_INICIADA", spec["publicacao"]["status"])
        self.assertEqual("ESCOPO_OBSERVADO", result["metadata"]["coverage"])

    def test_discovery_is_limited_deduplicated_and_hypothetical(self):
        result = flow.discover_opportunities(
            self.fixture, "catalogo_sintetico", ["crm_sintetico"],
            limits=mm03.Limits(max_candidates=1),
            proposals=[self.proposal(), self.proposal("Apoio sintético", "apoio_sintetico")],
        )
        self.assertEqual(1, len(result["shortlist"]))
        self.assertTrue(result["shortlist_truncated"])
        self.assertEqual("SHORTLIST_LIMIT", result["rejected"][0]["reason"])
        self.assertEqual("DESCOBERTO", result["shortlist"][0]["observed"]["status"])
        self.assertEqual("PROPOSTO", result["shortlist"][0]["hypothesis"]["status"])
        self.assertTrue(result["shortlist"][0]["hypothesis"]["requires_human_review"])
        self.assertEqual(3, len(result["metadata"]["calls"][2:]))
        self.assertFalse(result["metadata"]["catalog_complete"])

    def test_discovery_deduplicates_business_hypothesis_and_filters_weak_signal(self):
        duplicate = self.proposal("  eventos   SINTÉTICOS recentes ", "apoio_sintetico")
        result = flow.discover_opportunities(
            self.fixture, "catalogo_sintetico", ["crm_sintetico"],
            proposals=[self.proposal("Pagamentos programados"), self.proposal(), duplicate],
        )
        self.assertEqual(1, len(result["shortlist"]))
        self.assertEqual(1, result["shortlist"][0]["variants_merged"])
        self.assertEqual(2, len(result["shortlist"][0]["observed"]["sources"]))
        self.assertEqual("NO_SEMANTIC_METADATA_SIGNAL", result["rejected"][0]["reason"])
        self.assertEqual("ORDEM_DAS_HIPOTESES_FORNECIDAS", result["priority_basis"])

    def test_without_business_proposal_objects_are_only_triage_not_opportunities(self):
        result = flow.discover_opportunities(
            self.fixture, "catalogo_sintetico", ["crm_sintetico"])
        self.assertEqual([], result["shortlist"])
        self.assertEqual(2, len(result["source_objects_for_triage"]))
        self.assertEqual(["schemas", "objects"],
                         [x["operation"] for x in result["metadata"]["calls"]])

    def test_duplicate_or_unobserved_candidate_fails_before_details(self):
        for candidates, code in (
            ([('crm_sintetico', 'eventos_sinteticos')] * 2, "DUPLICATE_CANDIDATE"),
            ([('crm_sintetico', 'desconhecido')], "CANDIDATE_NOT_OBSERVED"),
            ([], "EMPTY_SHORTLIST"),
        ):
            with self.subTest(candidates=candidates), self.assertRaisesRegex(mm03.MetadataError, code):
                self.known(candidates=candidates)

    def test_denied_schema_is_not_assumed_empty_catalog(self):
        result = flow.discover_opportunities(
            self.fixture, "catalogo_sintetico", ["restrito_sintetico"])
        self.assertEqual([], result["shortlist"])
        self.assertEqual("PARTIAL_OBSERVATION", result["metadata"]["observation_status"])
        self.assertEqual("DENIED", result["metadata"]["discovery"]["objects"]
                         ["restrito_sintetico"]["status"])

    def test_non_client_goal_never_inherits_client_defaults(self):
        contract = flow.KnownObjective(
            "contrato-mm04", "Contrato sintético", "Características contratuais",
            "Avaliar a característica de contratos sintéticos.",
            "Contrato ativo na data de referência proposta.", "pedido_contrato",
            "2026-09-29T00:00:00Z", entity_type="contrato", logical_key="id_contrato",
            grain="um contrato por data de referência", eligible_population="contratos sintéticos elegíveis",
            reference_time="data do contrato", intended_uses=("Revisão humana contratual",),
            prohibited_uses=("Decisão automática",),
        )
        result = flow.known_objective(
            self.fixture, "catalogo_sintetico", ["crm_sintetico"],
            [("crm_sintetico", "eventos_sinteticos")], contract,
        )
        spec = result["spec"]
        self.assertEqual("contrato", spec["entidade"]["tipo"])
        self.assertEqual("id_contrato", spec["entidade"]["chave_logica"])
        self.assertEqual(["Revisão humana contratual"], spec["negocio"]["uso_pretendido"])
        self.assertEqual([], mm01.validate_spec(spec, mm01.load_schema(flow.SCHEMA)))

    def test_missing_entity_fields_are_explicitly_pending(self):
        spec = self.known()["spec"]
        self.assertTrue(all(value.startswith("PENDENTE:") for value in spec["entidade"].values()))
        self.assertNotIn("cliente", json.dumps(spec["entidade"]))

    def test_progressive_update_preserves_sources_and_mm01_transition(self):
        first = self.known()["spec"]
        revised_brief = flow.KnownObjective(
            self.brief.name, self.brief.title, self.brief.characteristic,
            "Avaliar característica com escopo sintético revisado.",
            self.brief.operational_definition, self.brief.request_ref,
            self.brief.created_at_utc, entity_type="contrato",
            logical_key="id_contrato", grain="um contrato por mês",
            eligible_population="contratos sintéticos elegíveis",
            reference_time="fim do mês sintético",
            intended_uses=("Revisão humana de contratos",),
        )
        updated = flow.known_objective(
            self.fixture, "catalogo_sintetico", ["crm_sintetico"],
            [("crm_sintetico", "eventos_sinteticos"),
             ("crm_sintetico", "apoio_sintetico")], revised_brief,
            previous_spec=first, advance_to_discovery=True,
        )["spec"]
        self.assertEqual("EM_DESCOBERTA", updated["identidade"]["estado"]["fase_atual"])
        self.assertEqual("IDEIA", updated["identidade"]["estado"]["fase_anterior"])
        self.assertEqual(2, len(updated["fontes"]))
        self.assertEqual("fonte_001", updated["fontes"][0]["id"])
        self.assertEqual("contrato", updated["entidade"]["tipo"])
        self.assertEqual(revised_brief.objective, updated["negocio"]["objetivo"])
        self.assertEqual(["Revisão humana de contratos"], updated["negocio"]["uso_pretendido"])
        self.assertEqual("IDEIA", first["identidade"]["estado"]["fase_atual"])
        self.assertTrue(first["entidade"]["tipo"].startswith("PENDENTE:"))
        self.assertEqual([], mm01.validate_spec(updated, mm01.load_schema(flow.SCHEMA), first))
        added = updated["proveniencia"]["registros"][len(first["proveniencia"]["registros"]):]
        self.assertIn("negocio.objetivo", {item["alvo"] for item in added})
        self.assertIn("entidade.tipo", {item["alvo"] for item in added})
        self.assertNotIn("negocio.caracteristica", {item["alvo"] for item in added})
        self.assertTrue(all(item["proveniencia"]["status"] == "PROPOSTO" for item in added))

    def test_truncated_columns_are_not_written_as_complete_fields(self):
        result = flow.known_objective(
            self.fixture, "catalogo_sintetico", ["crm_sintetico"],
            [("crm_sintetico", "eventos_sinteticos")], self.brief,
            limits=mm03.Limits(page_size=1, max_pages=1, max_candidates=1),
        )
        self.assertEqual("TRUNCATED", result["metadata"]["details"]
                         ["crm_sintetico.eventos_sinteticos"]["columns"]["status"])
        self.assertEqual([], result["spec"]["fontes"][0]["campos"])
        self.assertEqual("PARTIAL_OBSERVATION", result["metadata"]["observation_status"])

    def test_bad_brief_cannot_emit_spec(self):
        bad = flow.KnownObjective("../invalido", self.brief.title,
                                  self.brief.characteristic, self.brief.objective,
                                  self.brief.operational_definition,
                                  self.brief.request_ref, self.brief.created_at_utc)
        with self.assertRaisesRegex(flow.FlowError, "INVALID_MODEL_NAME"):
            flow.known_objective(self.fixture, "catalogo_sintetico", ["crm_sintetico"],
                                 [("crm_sintetico", "eventos_sinteticos")], bad)

    def test_cli_known_and_discover(self):
        with tempfile.TemporaryDirectory() as directory:
            brief_file = Path(directory) / "brief.json"
            brief_file.write_text(json.dumps(self.brief.__dict__), encoding="utf-8")
            common = [sys.executable, "-B", str(SCRIPT), "--fixture", str(FIXTURE),
                      "--catalog", "catalogo_sintetico", "--schema", "crm_sintetico"]
            known = subprocess.run(common + ["--mode", "known", "--brief", str(brief_file),
                                          "--candidate", "crm_sintetico.eventos_sinteticos"],
                                   capture_output=True, text=True, cwd=directory)
            self.assertEqual(0, known.returncode, known.stderr)
            self.assertEqual("IDEIA", json.loads(known.stdout)["spec"]["identidade"]
                             ["estado"]["fase_atual"])
            discover = subprocess.run(common + ["--mode", "discover"],
                                      capture_output=True, text=True, cwd=directory)
            self.assertEqual(0, discover.returncode, discover.stderr)
            self.assertEqual(0, len(json.loads(discover.stdout)["shortlist"]))
            self.assertEqual(2, len(json.loads(discover.stdout)["source_objects_for_triage"]))
            proposals_file = Path(directory) / "proposals.json"
            proposals_file.write_text(json.dumps([self.proposal().__dict__]), encoding="utf-8")
            selected = subprocess.run(common + ["--mode", "discover", "--proposals",
                                            str(proposals_file)], capture_output=True,
                                      text=True, cwd=directory)
            self.assertEqual(0, selected.returncode, selected.stderr)
            self.assertEqual(1, len(json.loads(selected.stdout)["shortlist"]))

    def test_cli_yaml_round_trip_without_overwrite_or_discover_side_effect(self):
        with tempfile.TemporaryDirectory() as directory:
            brief_file = Path(directory) / "brief.json"
            brief_file.write_text(json.dumps(self.brief.__dict__), encoding="utf-8")
            output = Path(directory) / "micromodelo.yaml"
            common = [sys.executable, "-B", str(SCRIPT), "--fixture", str(FIXTURE),
                      "--catalog", "catalogo_sintetico", "--schema", "crm_sintetico"]
            known_args = common + ["--mode", "known", "--brief", str(brief_file),
                                   "--candidate", "crm_sintetico.eventos_sinteticos",
                                   "--output-yaml", str(output)]
            created = subprocess.run(known_args, capture_output=True, text=True, cwd=directory)
            self.assertEqual(0, created.returncode, created.stderr)
            from_disk = mm01.load_document(output)
            self.assertEqual(from_disk, json.loads(created.stdout)["spec"])
            self.assertEqual([], mm01.validate_spec(from_disk, mm01.load_schema(flow.SCHEMA)))
            saved = output.read_bytes()
            repeated = subprocess.run(known_args, capture_output=True, text=True, cwd=directory)
            self.assertEqual(1, repeated.returncode)
            self.assertEqual(saved, output.read_bytes())
            discover = subprocess.run(common + ["--mode", "discover", "--output-yaml",
                                             str(output)], capture_output=True, text=True,
                                      cwd=directory)
            self.assertEqual(1, discover.returncode)
            self.assertEqual(saved, output.read_bytes())

    def test_cli_readback_failure_removes_only_new_yaml_and_retry_succeeds(self):
        with tempfile.TemporaryDirectory() as directory:
            brief_file = Path(directory) / "brief.json"
            brief_file.write_text(json.dumps(self.brief.__dict__), encoding="utf-8")
            output = Path(directory) / "micromodelo.yaml"
            args = ["--fixture", str(FIXTURE), "--catalog", "catalogo_sintetico",
                    "--schema", "crm_sintetico", "--mode", "known", "--brief",
                    str(brief_file), "--candidate", "crm_sintetico.eventos_sinteticos",
                    "--output-yaml", str(output)]
            original_load = mm01.load_document

            def fail_readback(path):
                if Path(path) == output:
                    raise OSError("readback failure injected")
                return original_load(path)

            with mock.patch.object(flow.mm01, "load_document", side_effect=fail_readback):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(1, flow.main(args))
            self.assertFalse(output.exists())
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(0, flow.main(args))
            self.assertEqual([], mm01.validate_spec(mm01.load_document(output),
                                                   mm01.load_schema(flow.SCHEMA)))


if __name__ == "__main__":
    unittest.main()
