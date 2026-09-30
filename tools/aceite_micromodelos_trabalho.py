"""Aceite E0 sintético do pacote técnico de Micromodelos extraído.

Pode ser chamado de uma célula Python: ``run(package_root)``. Não consulta catálogo,
registros, MLflow, rede ou autoridade de publicação. O manifesto é conferido antes
de importar qualquer módulo Micromodelos do pacote.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


class AcceptanceError(ValueError):
    """Falha de aceite com código estável, sem conteúdo de fixtures."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise AcceptanceError(code)


def _stage(report: dict[str, Any], name: str, status: str, detail: str) -> None:
    report["stages"].append({"name": name, "status": status, "detail": detail})


def _verify_product(root: Path, manifest_path: Path, expected_commit: str | None,
                    expected_sha256: str | None) -> dict[str, Any]:
    """Confere o produto do ZIP 01 antes de executar o ensaio sintético."""
    _require(root.is_dir() and manifest_path.is_file() and not manifest_path.is_symlink(),
             "PACKAGE_OR_MANIFEST_MISSING")
    raw = manifest_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    _require(expected_sha256 is None or digest == expected_sha256, "MANIFEST_HASH_MISMATCH")
    try:
        manifest = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError):
        raise AcceptanceError("INVALID_MANIFEST") from None
    _require(type(manifest) is dict and manifest.get("schema_version") == 2
             and manifest.get("worktree_dirty") is False
             and type(manifest.get("files")) is list,
             "INVALID_MANIFEST")
    _require(expected_commit is None or manifest.get("source_commit") == expected_commit,
             "COMMIT_MISMATCH")
    seen: set[str] = set()
    for entry in manifest["files"]:
        _require(type(entry) is dict, "INVALID_MANIFEST")
        rel = entry.get("path")
        _require(type(rel) is str and rel not in seen
                 and (rel == ".assistant_instructions.md" or rel.startswith(".assistant/"))
                 and rel == PurePosixPath(rel).as_posix()
                 and not PurePosixPath(rel).is_absolute()
                 and all(part not in {"", ".", ".."} for part in rel.split("/")),
                 "INVALID_MANIFEST_PATH")
        seen.add(rel)
        if not rel.startswith(".assistant/hub_micromodelos/"):
            continue
        _require(entry.get("object_type") == "FILE", "MICROMODELO_TYPE_MISMATCH")
        path = root / rel
        _require(path.is_file() and not path.is_symlink()
                 and path.resolve().is_relative_to(root), "MICROMODELO_FILE_MISSING")
        content = path.read_bytes()
        _require(len(content) == entry.get("bytes")
                 and hashlib.sha256(content).hexdigest() == entry.get("sha256"),
                 "MICROMODELO_FILE_HASH_MISMATCH")
    required = {
        ".assistant/hub_micromodelos/README.md",
        ".assistant/hub_micromodelos/contratos/micromodelo.schema.json",
        ".assistant/hub_micromodelos/contratos/micromodelo.template.yaml",
        ".assistant/hub_micromodelos/execucao/execucao.py",
        ".assistant/hub_micromodelos/exemplos/README.md",
        ".assistant/hub_micromodelos/exemplos/recencia_contato/README.md",
        ".assistant/hub_micromodelos/exemplos/recencia_contato/micromodelo.yaml",
        ".assistant/hub_micromodelos/exemplos/recencia_contato/dados_sinteticos.json",
        ".assistant/hub_micromodelos/exemplos/recencia_contato/resultado_esperado.json",
        ".assistant/hub_micromodelos/exemplos/recencia_contato/executar_exemplo.py",
    }
    _require(required <= seen, "MICROMODELO_INCOMPLETE")
    return {"source_commit": manifest["source_commit"], "manifest_sha256": digest}


def _package_module(root: Path, name: str, relative: str):
    module = importlib.import_module(name)
    expected = (root / ".assistant" / "hub_micromodelos" / relative).resolve()
    _require(Path(module.__file__).resolve() == expected, "IMPORT_OUTSIDE_PACKAGE")
    return module


def _execute_synthetic(root: Path, report: dict[str, Any]) -> None:
    capabilities = ("yaml", "jsonschema", "regex")
    missing = [name for name in capabilities if importlib.util.find_spec(name) is None]
    _require(not missing, "MISSING_DEPENDENCIES:" + ",".join(missing))
    _stage(report, "dependencies", "PASS", "yaml,jsonschema,regex disponíveis")

    product_path = str(root / ".assistant")
    if product_path not in sys.path:
        sys.path.insert(0, product_path)
    mm01 = _package_module(root, "hub_micromodelos.execucao.especificacao", "execucao/especificacao.py")
    mm02 = _package_module(root, "hub_micromodelos.execucao.assinatura", "execucao/assinatura.py")
    _package_module(root, "hub_micromodelos.execucao.metadados", "execucao/metadados.py")
    mm04 = _package_module(root, "hub_micromodelos.execucao.fluxo", "execucao/fluxo.py")
    _package_module(root, "hub_micromodelos.execucao.artefatos", "execucao/artefatos.py")
    mm09 = _package_module(root, "hub_micromodelos.execucao.execucao", "execucao/execucao.py")
    mm10 = _package_module(root, "hub_micromodelos.execucao.entrega", "execucao/entrega.py")
    mm12 = _package_module(root, "hub_micromodelos.exemplos.migracao_simulada", "exemplos/migracao_simulada.py")
    mm13 = _package_module(root, "hub_micromodelos.execucao.catalogo", "execucao/catalogo.py")
    _stage(report, "imports", "PASS", "módulos carregados da raiz conferida")

    pilot = mm09.run_greenfield_lab()
    _require(pilot["environment"] == "E0_SYNTHETIC_IN_MEMORY"
             and pilot["mm04_mode"] == "OBJETIVO_CONHECIDO"
             and pilot["metadata_coverage"] == "ESCOPO_OBSERVADO"
             and pilot["metadata_catalog_complete"] is False,
             "LAB_SCOPE_MISMATCH")
    _stage(report, "briefing_metadata", "PASS", "briefing e fixture sintéticos; escopo observado")

    discovery = mm04.discover_opportunities(
        mm09._metadata_fixture(), "catalogo_sintetico", ["crm_sintetico"],
        proposals=[mm04.OpportunityProposal(
            characteristic="eventos sintéticos recorrentes",
            decision="triagem sintética para estudo",
            population="entidades fictícias",
            grain="entidade e janela sintética",
            decision_time="fim da janela sintética",
            horizon="janela sintética seguinte",
            candidates=(("crm_sintetico", "eventos_sinteticos"),),
        )],
    )
    _require(discovery["mode"] == "DESCOBRIR_OPORTUNIDADES"
             and discovery["metadata"]["coverage"] == "ESCOPO_OBSERVADO"
             and len(discovery["shortlist"]) == 1
             and discovery["shortlist"][0]["hypothesis"]["status"] == "PROPOSTO"
             and discovery["shortlist"][0]["observed"]["status"] == "DESCOBERTO",
             "SYNTHETIC_DISCOVERY_MISMATCH")
    _stage(report, "metadata_discovery", "PASS", "hipótese sintética; sem leitura de linhas")

    schema = mm01.load_schema(mm04.SCHEMA)
    history = pilot["spec_history"]
    spec = pilot["spec"]
    _require(not mm01.validate_spec(history["IDEIA"], schema)
             and not mm01.validate_spec(history["EM_DESCOBERTA"], schema,
                                        previous_spec=history["IDEIA"])
             and not mm01.validate_spec(spec, schema,
                                        previous_spec=history["EM_DESCOBERTA"]),
             "INVALID_MM01_PHASES")
    yaml = importlib.import_module("yaml")
    with tempfile.TemporaryDirectory(prefix="aceite-mm-") as temporary:
        document = Path(temporary) / "micromodelo.yaml"
        document.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False),
                            encoding="utf-8")
        _require(mm01.load_document(document) == spec, "YAML_READBACK_MISMATCH")
    _stage(report, "mm01_yaml", "PASS", "transições válidas e YAML relido")

    digest = mm02.calculate_spec_fingerprint(spec, schema)
    _require(digest.sha256 == pilot["spec_fingerprint"], "FINGERPRINT_MISMATCH")
    _require(digest.sha256 in pilot["artifacts"]["notebook_source"]
             and digest.sha256 in pilot["artifacts"]["readme_markdown"],
             "ARTIFACT_FINGERPRINT_MISMATCH")
    _stage(report, "fingerprint_artifacts", "PASS", digest.sha256)

    scoring = pilot["scoring"]
    individual = scoring["individual"]
    aggregate = scoring["aggregate"]
    counted = {label: sum(row["classificacao"] == label for row in individual)
               for label in ("TRUE", "FALSE", "INDETERMINADO")}
    scores = [row["score_heuristico_0_100"] for row in individual
              if row["score_heuristico_0_100"] is not None]
    _require(len(individual) == 6 and aggregate["populacao"] == 6
             and aggregate["contagens"] == counted
             and counted == {"TRUE": 1, "FALSE": 2, "INDETERMINADO": 3}
             and aggregate["scores_emitidos"] == len(scores) == 4
             and all(0 <= value <= 100 for value in scores)
             and scoring["score_semantics"] == "HEURISTICA_FORCA_EVIDENCIA_NAO_PROBABILIDADE",
             "SYNTHETIC_SCORING_MISMATCH")
    _stage(report, "classification_score", "PASS", "6 entidades; TRUE=1 FALSE=2 INDETERMINADO=3; scores=4")

    handoff = mm10.prepare_handoff(spec, schema, aggregate)
    _require(handoff["status"] == "DRAFT_NOT_SUBMITTED"
             and handoff["aggregate"]["status"] == "SUPPLIED_UNVERIFIED"
             and handoff["spec_fingerprint"] == digest.sha256
             and handoff["published"] is False and handoff["run_ref"] is None,
             "HANDOFF_GOVERNANCE_MISMATCH")
    _stage(report, "handoff", "PASS", "rascunho reconciliado; publicação não executada")

    catalogue = mm13.build_catalog([spec], schema)
    _require(len(catalogue) == 1 and catalogue[0]["fingerprint"] == digest.sha256
             and catalogue[0]["execution_status"] == "NOT_OBSERVED",
             "CATALOG_MISMATCH")
    fictitious = [{"fixture_namespace": "MM12_FICTICIO", "synthetic": True,
                   "id_entidade": row["id_entidade"], "classificacao": row["classificacao"],
                   "score": row["score_heuristico_0_100"]} for row in individual]
    rehearsal = mm12.rehearse_equivalence(fictitious, fictitious)
    _require(rehearsal["status"] == "EQUIVALENT_LAB"
             and rehearsal["corporate_v1_verified"] is False
             and rehearsal["publication_authorized"] is False,
             "MIGRATION_LAB_MISMATCH")
    _stage(report, "catalog_migration", "PASS", "catálogo declarado; equivalência apenas fictícia")
    report["synthetic_summary"] = {"population": 6, "counts": counted,
                                   "score_count": len(scores), "fingerprint": digest.sha256}


def run(package_root: str | Path, manifest: str | Path | None = None, *,
        expected_commit: str | None = None, expected_manifest_sha256: str | None = None,
        testar_mlflow: bool = False, testar_metadata: bool = False) -> dict[str, Any]:
    """Confere e executa E0 do Hub extraído; devolve vereditos sem linhas de dados."""
    report: dict[str, Any] = {"status": "FAIL", "mode": "E0_SYNTHETIC_PACKAGE",
                              "stages": [], "source_commit": None,
                              "manifest_sha256": None, "synthetic_summary": None,
                              "limits": {"mlflow": "NOT_RUN", "metadata_real": "NOT_RUN",
                                         "genie": "NOT_RUN", "corporate_runtime": "NOT_VERIFIED",
                                         "publication": "NOT_EXECUTED"}}
    if type(testar_mlflow) is not bool or type(testar_metadata) is not bool:
        _stage(report, "input", "FAIL", "INVALID_OPTIONS")
        return report
    root = Path(package_root).resolve()
    manifest_path = (root / "MANIFEST.json") if manifest is None else Path(manifest).resolve()
    try:
        _require(manifest_path.parent == root, "MANIFEST_OUTSIDE_PACKAGE")
        verified = _verify_product(root, manifest_path, expected_commit,
                                   expected_manifest_sha256)
        report["source_commit"] = verified["source_commit"]
        report["manifest_sha256"] = verified["manifest_sha256"]
        _stage(report, "integrity", "PASS", "manifesto e hashes conferidos")
    except AcceptanceError as exc:
        _stage(report, "integrity", "FAIL", str(exc))
        return report
    except Exception:
        _stage(report, "integrity", "FAIL", "PACKAGE_INTEGRITY_ERROR")
        return report
    if testar_mlflow or testar_metadata:
        _stage(report, "destination_opt_in", "UNAVAILABLE",
               "REQUIRES_DESTINATION_CONFIGURATION")
        return report
    try:
        _execute_synthetic(root, report)
    except AcceptanceError as exc:
        _stage(report, "acceptance", "FAIL", str(exc))
        return report
    except Exception:
        _stage(report, "acceptance", "FAIL", "PACKAGE_OR_RUNTIME_ERROR")
        return report
    report["status"] = "PASS"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aceite E0 sintético do ZIP Micromodelos")
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--testar-mlflow", action="store_true")
    parser.add_argument("--testar-metadata", action="store_true")
    args = parser.parse_args(argv)
    report = run(args.package_root, args.manifest, testar_mlflow=args.testar_mlflow,
                 testar_metadata=args.testar_metadata)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
