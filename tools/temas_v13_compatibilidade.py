"""Compatibilidade e acessibilidade operacional V13-S5.

O núcleo é local, determinístico e read-only. Ele calcula contraste WCAG/sRGB
somente para pares de cor explicitamente fornecidos como provenientes de export
real revisado. Não lê Databricks, não autentica a evidência externa, não inventa
schema nativo e não transforma formatação condicional em token do Hub.

Estados não observados não são inferidos: um par com ``observed=false`` recebe
NOT_APPLICABLE e nenhum ratio é calculado.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ENGINE = "V13-S5"
REPORT_VERSION = 1
MAX_INPUT_BYTES = 262_144
SUPPORTED_SURFACE = "aibi_dashboard"
EVIDENCE_BASIS = "REVIEWED_REAL_EXPORT"
STATUSES = {"PASS", "FAIL", "NOT_APPLICABLE"}
MODES = {"LIGHT", "DARK", "HIGH_CONTRAST"}
TEXT_CLASSES = {"NORMAL": 4.5, "LARGE": 3.0}

_HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PAIR_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$")

REQUEST_FIELDS = {
    "schema_version",
    "engine",
    "surface_id",
    "evidence_basis",
    "export_sha256",
    "synthetic_fixture_used",
    "pairs",
}

STABLE_CODES = {
    "REQUEST_VALID",
    "REQUEST_TYPE",
    "REQUEST_FIELDS",
    "REQUEST_VERSION",
    "SURFACE_UNSUPPORTED",
    "EVIDENCE_BASIS_INVALID",
    "EXPORT_HASH_INVALID",
    "SYNTHETIC_FIXTURE_FORBIDDEN",
    "PAIRS_INVALID",
    "PAIR_SHAPE_INVALID",
    "PAIR_ID_INVALID",
    "PAIR_ID_DUPLICATE",
    "COLOR_INVALID",
    "MODE_INVALID",
    "TEXT_CLASS_INVALID",
    "OBSERVED_INVALID",
    "CONTRAST_PASS",
    "CONTRAST_FAIL",
    "STATE_NOT_EXERCISED",
}


class CompatibilityRequestError(ValueError):
    """Erro fail-closed com código estável e mensagem segura."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.safe_message = message
        super().__init__(f"{code}: {message}")


def _fail(code: str, message: str) -> None:
    raise CompatibilityRequestError(code, message) from None


def _linearized_channel(value: int) -> float:
    channel = value / 255.0
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    """Calcula luminância relativa WCAG para uma cor #RRGGBB."""
    if type(hex_color) is not str or _HEX_RE.fullmatch(hex_color) is None:
        _fail("COLOR_INVALID", "Cor precisa usar o formato #RRGGBB.")
    raw = hex_color[1:]
    red, green, blue = (int(raw[index:index + 2], 16) for index in (0, 2, 4))
    r = _linearized_channel(red)
    g = _linearized_channel(green)
    b = _linearized_channel(blue)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground: str, background: str) -> float:
    """Calcula ratio de contraste sem arredondar para decisão."""
    first = relative_luminance(foreground)
    second = relative_luminance(background)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def _validate_request(request: Any) -> list[dict[str, Any]]:
    if type(request) is not dict:
        _fail("REQUEST_TYPE", "Request S5 precisa ser objeto JSON.")
    if set(request) != REQUEST_FIELDS:
        _fail("REQUEST_FIELDS", "Request S5 possui campos ausentes ou inesperados.")
    if request.get("schema_version") != 1 or request.get("engine") != ENGINE:
        _fail("REQUEST_VERSION", "Versão ou engine S5 divergente.")
    if request.get("surface_id") != SUPPORTED_SURFACE:
        _fail("SURFACE_UNSUPPORTED", "O preflight de contraste S5 atual suporta somente dashboard AI/BI.")
    if request.get("evidence_basis") != EVIDENCE_BASIS:
        _fail("EVIDENCE_BASIS_INVALID", "Contraste operacional exige export real revisado declarado.")
    export_sha = request.get("export_sha256")
    if type(export_sha) is not str or _SHA256_RE.fullmatch(export_sha) is None:
        _fail("EXPORT_HASH_INVALID", "export_sha256 precisa ser SHA-256 completo.")
    if request.get("synthetic_fixture_used") is not False:
        _fail("SYNTHETIC_FIXTURE_FORBIDDEN", "Fixture sintético não pode ser tratado como export nativo real.")
    pairs = request.get("pairs")
    if type(pairs) is not list or not pairs:
        _fail("PAIRS_INVALID", "Ao menos um par de contraste explícito é obrigatório.")

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    expected = {"pair_id", "foreground", "background", "mode", "text_class", "observed"}
    for raw in pairs:
        if type(raw) is not dict or set(raw) != expected:
            _fail("PAIR_SHAPE_INVALID", "Par de contraste possui shape inválido.")
        pair_id = raw.get("pair_id")
        if type(pair_id) is not str or _PAIR_ID_RE.fullmatch(pair_id) is None:
            _fail("PAIR_ID_INVALID", "pair_id precisa ser identificador sanitizado.")
        if pair_id in seen:
            _fail("PAIR_ID_DUPLICATE", "pair_id duplicado.")
        seen.add(pair_id)

        foreground = raw.get("foreground")
        background = raw.get("background")
        if type(foreground) is not str or _HEX_RE.fullmatch(foreground) is None:
            _fail("COLOR_INVALID", "Foreground precisa usar #RRGGBB.")
        if type(background) is not str or _HEX_RE.fullmatch(background) is None:
            _fail("COLOR_INVALID", "Background precisa usar #RRGGBB.")
        mode = raw.get("mode")
        if mode not in MODES:
            _fail("MODE_INVALID", "Modo precisa ser LIGHT, DARK ou HIGH_CONTRAST.")
        text_class = raw.get("text_class")
        if text_class not in TEXT_CLASSES:
            _fail("TEXT_CLASS_INVALID", "text_class precisa ser NORMAL ou LARGE.")
        observed = raw.get("observed")
        if type(observed) is not bool:
            _fail("OBSERVED_INVALID", "observed precisa ser booleano.")

        normalized.append(
            {
                "pair_id": pair_id,
                "foreground": foreground.upper(),
                "background": background.upper(),
                "mode": mode,
                "text_class": text_class,
                "observed": observed,
            }
        )
    return normalized


def evaluate(request: Any) -> dict[str, Any]:
    """Executa preflight local; não autentica o export ou o ambiente."""
    pairs = _validate_request(request)
    results: list[dict[str, Any]] = []
    observed_statuses: list[str] = []
    exercised_modes: set[str] = set()

    for pair in pairs:
        if not pair["observed"]:
            results.append(
                {
                    "pair_id": pair["pair_id"],
                    "mode": pair["mode"],
                    "status": "NOT_APPLICABLE",
                    "code": "STATE_NOT_EXERCISED",
                    "ratio": None,
                    "required_ratio": TEXT_CLASSES[pair["text_class"]],
                }
            )
            continue

        exercised_modes.add(pair["mode"])
        ratio = contrast_ratio(pair["foreground"], pair["background"])
        required = TEXT_CLASSES[pair["text_class"]]
        status = "PASS" if ratio >= required else "FAIL"
        code = "CONTRAST_PASS" if status == "PASS" else "CONTRAST_FAIL"
        observed_statuses.append(status)
        results.append(
            {
                "pair_id": pair["pair_id"],
                "mode": pair["mode"],
                "status": status,
                "code": code,
                "ratio": ratio,
                "required_ratio": required,
            }
        )

    if "FAIL" in observed_statuses:
        overall = "FAIL"
    elif observed_statuses:
        overall = "PASS"
    else:
        overall = "NOT_APPLICABLE"

    coverage = {
        mode: ("EXERCISED" if mode in exercised_modes else "NOT_EXERCISED")
        for mode in ("LIGHT", "DARK", "HIGH_CONTRAST")
    }

    return {
        "report_version": REPORT_VERSION,
        "engine": ENGINE,
        "surface_id": SUPPORTED_SURFACE,
        "overall_status": overall,
        "decision_code": (
            "CONTRAST_FAIL"
            if overall == "FAIL"
            else "CONTRAST_PASS"
            if overall == "PASS"
            else "STATE_NOT_EXERCISED"
        ),
        "evidence_basis": EVIDENCE_BASIS,
        "evidence_authenticated": False,
        "scope": "LOCAL_CONTRAST_PREFLIGHT_ONLY",
        "mode_coverage": coverage,
        "pairs": results,
        "network_access": False,
        "remote_mutation_performed": False,
        "v11_binding_contract_changed": False,
    }


def _load_request(path: Path) -> Any:
    try:
        if path.stat().st_size > MAX_INPUT_BYTES:
            _fail("REQUEST_TYPE", "Request excede o limite local permitido.")
        return json.loads(path.read_text(encoding="utf-8"))
    except CompatibilityRequestError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        _fail("REQUEST_TYPE", "Request não pôde ser lido como JSON local válido.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = evaluate(_load_request(args.request))
    except CompatibilityRequestError as exc:
        print(f"FAIL V13-S5 {exc.code}: {exc.safe_message}")
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
