"""Fingerprint semântico MM02 para a especificação canônica de micromodelos.

Este módulo é repo-side e sintético. Ele consome o contrato MM01 já integrado,
não cria skill, prompt, tracking, publicação ou acesso a Databricks.

O fingerprint identifica a definição analítica material. Evidência de ciclo de
vida (proveniência, aprovação, runs, timestamps, fase, tracking e publicação
institucional) permanece fora do preimage para não transformar execução ou
governança em identidade semântica da especificação.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

import micromodelo_mm01_contract as mm01


ALGORITHM_ID = "mm02-spec-fingerprint-v1"
ALGORITHM_VERSION = "1.0.0"


class InvalidSpecificationError(ValueError):
    """A especificação não satisfaz o contrato MM01 e não pode ser fingerprintada."""


@dataclass(frozen=True)
class FingerprintResult:
    algorithm: str
    algorithm_version: str
    sha256: str
    canonical_json: str


def _editorial_text(value: str) -> str:
    """Reusa a equivalência editorial conservadora congelada na MM01."""
    return mm01._normalize_editorial_text(value)


def _canonical_number(value: Any) -> str:
    """Representa int/float canônico sem depender de 1 versus 1.0."""
    if type(value) is int:
        return str(value)
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("número não finito fora do domínio canônico")
        if value == 0.0:
            return "0"
        rendered = format(Decimal(repr(value)), "f")
        if "." in rendered:
            rendered = rendered.rstrip("0").rstrip(".")
        return "0" if rendered in {"-0", "+0"} else rendered
    raise TypeError(f"tipo numérico fora do domínio canônico: {type(value).__name__}")


def _sorted_editorial(values: list[str]) -> list[str]:
    return sorted({_editorial_text(value) for value in values})


def _canonical_sources(spec: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for item in spec["fontes"]:
        result.append(
            {
                "id": item["id"],
                "catalogo_ref": item["catalogo_ref"],
                "schema": item["schema"],
                "objeto": item["objeto"],
                "tipo_objeto": item["tipo_objeto"],
                "campos": sorted(item["campos"]),
                "papel": item["papel"],
            }
        )
    return sorted(result, key=lambda item: item["id"])


def _canonical_evidence(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = [
        {
            "id": item["id"],
            "fontes_ref": sorted(item["fontes_ref"]),
            "regra": _editorial_text(item["regra"]),
        }
        for item in items
    ]
    return sorted(result, key=lambda item: item["id"])


def _canonical_thresholds(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = [
        {
            "id": item["id"],
            "operador": item["operador"],
            "valor": _canonical_number(item["valor"]),
            "unidade": item["unidade"],
        }
        for item in items
    ]
    return sorted(result, key=lambda item: item["id"])


def _canonical_score(score: dict[str, Any]) -> dict[str, Any]:
    scale = score["escala"]
    normalization = score["normalizacao"]
    calibration = score["calibracao"]

    components = [
        {
            "id": item["id"],
            "peso": _canonical_number(item["peso"]),
        }
        for item in score["componentes"]
    ]

    semantic_ref = (
        score["semantica_ref"]
        if score["tipo_semantica"] == "OUTRA_APROVADA"
        else None
    )

    return {
        "habilitado": score["habilitado"],
        "tipo_semantica": score["tipo_semantica"],
        # Para tipos estruturados, semantica_ref é trilha auditável. Em
        # OUTRA_APROVADA ela é a única referência da definição customizada.
        "semantica_ref": semantic_ref,
        "escala": (
            None
            if scale is None
            else {
                "min": _canonical_number(scale["min"]),
                "max": _canonical_number(scale["max"]),
            }
        ),
        "normalizacao": (
            None
            if normalization is None
            else {
                "metodo": normalization["metodo"],
                # Referência é material somente quando a normalização é
                # customizada; nos métodos estruturados ela é audit trail.
                "referencia": (
                    normalization["referencia"]
                    if normalization["metodo"] == "CUSTOM_APROVADO"
                    else None
                ),
            }
        ),
        "componentes": sorted(components, key=lambda item: item["id"]),
        "calibracao": (
            None
            if calibration is None
            else {
                # Método e ID do experimento de calibração participam da
                # definição. Resultado, run, timestamp e proveniência do
                # experimento permanecem evidência e ficam fora do preimage.
                "metodo": _editorial_text(calibration["metodo"]),
                "evidencia_ref": calibration["evidencia_ref"],
            }
        ),
    }


def _canonical_output(output: dict[str, Any]) -> dict[str, Any]:
    publication = output["publicacao"]
    boolean_field = publication["campo_booleano"]
    indeterminate_policy = publication["politica_indeterminado"]

    return {
        "estudo": {
            "campo_classificacao": output["estudo"]["campo_classificacao"],
            "valores_classificacao": list(output["estudo"]["valores_classificacao"]),
            "campo_score": output["estudo"]["campo_score"],
        },
        "publicacao": {
            # estado=PENDENTE/DEFINIDO é ciclo de vida. O contrato material é
            # representado pelos campos/política efetivamente declarados.
            "campo_booleano": (
                None
                if boolean_field is None
                else {
                    "nome": boolean_field["nome"],
                    "tipo": boolean_field["tipo"],
                }
            ),
            "politica_indeterminado": (
                None
                if indeterminate_policy is None
                else {
                    "tratamento": indeterminate_policy["tratamento"],
                    "indeterminado_vira_false": indeterminate_policy[
                        "indeterminado_vira_false"
                    ],
                    "regra_ref": indeterminate_policy["regra_ref"],
                }
            ),
        },
    }


def canonical_material_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Extrai somente a definição analítica material do contrato MM01.

    Deliberadamente excluídos:
    - identidade humana/versionamento/estado do artefato;
    - objetivo explicativo e descrições auxiliares;
    - toda proveniência/aprovação/timestamp;
    - experimentos e validação observada;
    - tracking, governança e estado institucional de publicação.

    A separação impede que avanço de fase, nova run ou nova aprovação altere o
    fingerprint quando a definição analítica permaneceu igual.
    """
    classification = spec["classificacao"]
    semantics = classification["semantica"]
    missing = classification["ausencia_evidencia"]

    return {
        "schema_version": spec["schema_version"],
        "negocio": {
            "caracteristica": _editorial_text(spec["negocio"]["caracteristica"]),
            "definicao_operacional": _editorial_text(
                spec["negocio"]["definicao_operacional"]
            ),
            "uso_pretendido": _sorted_editorial(spec["negocio"]["uso_pretendido"]),
            "nao_usar_para": _sorted_editorial(spec["negocio"]["nao_usar_para"]),
        },
        "entidade": {
            "tipo": _editorial_text(spec["entidade"]["tipo"]),
            "chave_logica": spec["entidade"]["chave_logica"],
            "granularidade": _editorial_text(spec["entidade"]["granularidade"]),
            "populacao_elegivel": _editorial_text(
                spec["entidade"]["populacao_elegivel"]
            ),
            "referencia_temporal": _editorial_text(
                spec["entidade"]["referencia_temporal"]
            ),
        },
        "fontes": _canonical_sources(spec),
        "evidencias": _canonical_evidence(spec["evidencias"]),
        "contra_evidencias": _canonical_evidence(spec["contra_evidencias"]),
        "classificacao": {
            "tipo": classification["tipo"],
            "semantica": {
                "quando_true": _editorial_text(semantics["quando_true"]),
                "quando_false": _editorial_text(semantics["quando_false"]),
                "quando_indeterminado": _editorial_text(
                    semantics["quando_indeterminado"]
                ),
            },
            "ausencia_evidencia": {
                "tratamento": missing["tratamento"],
                "resultado_sem_evidencia": missing["resultado_sem_evidencia"],
                "regra_ref": missing["regra_ref"],
            },
            "limiares": _canonical_thresholds(classification["limiares"]),
        },
        "score": _canonical_score(spec["score"]),
        "saida": _canonical_output(spec["saida"]),
    }


def canonical_preimage(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "algorithm": ALGORITHM_ID,
        "algorithm_version": ALGORITHM_VERSION,
        "material_spec": canonical_material_spec(spec),
    }


def canonical_json(spec: dict[str, Any]) -> str:
    return json.dumps(
        canonical_preimage(spec),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def calculate_spec_fingerprint(
    spec: dict[str, Any],
    schema: dict[str, Any],
) -> FingerprintResult:
    issues = mm01.validate_spec(spec, schema)
    if issues:
        rendered = "\n".join(str(issue) for issue in issues)
        raise InvalidSpecificationError(
            "especificação inválida segundo MM01; fingerprint recusado:\n" + rendered
        )

    serialized = canonical_json(spec)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return FingerprintResult(
        algorithm=ALGORITHM_ID,
        algorithm_version=ALGORITHM_VERSION,
        sha256=digest,
        canonical_json=serialized,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calcula spec_fingerprint semântico MM02 sobre contrato MM01 válido"
    )
    parser.add_argument("documento", help="micromodelo.yaml/.yml/.json")
    parser.add_argument(
        "--schema",
        required=True,
        help="caminho para micromodelo.schema.json da MM01",
    )
    parser.add_argument(
        "--show-canonical",
        action="store_true",
        help="imprime o preimage JSON canônico usado pelo SHA-256",
    )
    args = parser.parse_args()

    try:
        spec = mm01.load_document(args.documento)
        schema = mm01.load_schema(args.schema)
        result = calculate_spec_fingerprint(spec, schema)
    except InvalidSpecificationError as exc:
        print(f"REPROVADO_MM02: {exc}")
        return 1
    except Exception as exc:
        print(f"ERRO_MM02: {exc}")
        return 2

    print(f"FINGERPRINT_ALGORITHM={result.algorithm}")
    print(f"FINGERPRINT_ALGORITHM_VERSION={result.algorithm_version}")
    print(f"SPEC_FINGERPRINT_SHA256={result.sha256}")
    if args.show_canonical:
        print(result.canonical_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
