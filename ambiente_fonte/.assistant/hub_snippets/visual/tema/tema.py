"""Núcleo do Sistema de Temas do Hub.

Carrega e valida documentos JSON completos do contrato 0.1.0 sem alterar estado
visual da sessão. A aplicação em Plotly/HTML começa em sprints posteriores.
"""
from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Mapping, Optional, Union

ENGINE_VERSION = "1.0.0"
MAX_THEME_BYTES_FALLBACK = 131_072
MAX_DEPTH_FALLBACK = 12


class ErroTema(ValueError):
    """Erro seguro e classificável ao carregar ou validar um tema."""

    def __init__(self, codigo: str, orientacao: str, campo: Optional[str] = None):
        self.codigo = codigo
        self.campo = campo
        self.orientacao = orientacao
        local = f" em {campo}" if campo else ""
        super().__init__(f"{codigo}{local}: {orientacao}")


@dataclass(frozen=True)
class TemaResolvido:
    """Representação validada e isolada de um documento de tema."""

    _json_semantico: str
    _bytes_originais: bytes
    sha256: str
    origem: str
    engine_version: str = ENGINE_VERSION

    @property
    def theme_id(self) -> str:
        return self._documento()["theme_id"]

    @property
    def theme_version(self) -> str:
        return self._documento()["theme_version"]

    @property
    def schema_version(self) -> str:
        return self._documento()["schema_version"]

    @property
    def context(self) -> str:
        return self._documento()["context"]

    @property
    def mode(self) -> str:
        return self._documento()["mode"]

    @property
    def asset_set_id(self) -> str:
        return self._documento()["asset_set_id"]

    def token(self, nome: str) -> Any:
        """Retorna cópia do token, evitando mutação do estado resolvido."""
        tokens = self._documento()["tokens"]
        if nome not in tokens:
            raise KeyError(nome)
        return deepcopy(tokens[nome])

    def como_dict(self) -> dict[str, Any]:
        """Retorna cópia independente do documento validado."""
        return deepcopy(self._documento())

    def bytes_originais(self) -> bytes:
        """Retorna os bytes exatos usados no hash da carga."""
        return bytes(self._bytes_originais)

    def _documento(self) -> dict[str, Any]:
        return json.loads(self._json_semantico)


def resolver_tema(
    tema: Optional[Union["TemaResolvido", str, Path, bytes, bytearray]],
    *,
    schema_path: Optional[Union[str, Path]] = None,
) -> Optional[TemaResolvido]:
    """Resolve tema opcional; ``None`` preserva explicitamente a rota legada."""
    if tema is None:
        return None
    if isinstance(tema, TemaResolvido):
        return tema
    return carregar_tema(tema, schema_path=schema_path)


def carregar_tema(
    origem: Union[str, Path, bytes, bytearray],
    *,
    schema_path: Optional[Union[str, Path]] = None,
) -> TemaResolvido:
    """Carrega, valida e resolve um tema sem aplicar efeitos visuais."""
    schema = _carregar_schema(schema_path)
    policy = schema.get("x-hub-policy", {})
    max_bytes = _positive_int(policy.get("max_bytes"), MAX_THEME_BYTES_FALLBACK)
    max_depth = _positive_int(policy.get("max_depth"), MAX_DEPTH_FALLBACK)
    raw, rotulo = _ler_origem(origem, max_bytes=max_bytes)
    documento = _parse_json_estrito(raw, max_depth=max_depth)
    _validar_schema(documento, schema, schema, path="$", max_depth=max_depth)
    _validar_compatibilidade(documento)
    _validar_regras_dominio(documento)
    semantico = json.dumps(
        documento,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return TemaResolvido(
        _json_semantico=semantico,
        _bytes_originais=raw,
        sha256=hashlib.sha256(raw).hexdigest(),
        origem=rotulo,
    )


def schema_padrao_path() -> Path:
    """Localiza o schema canônico instalado junto do produto."""
    assistant_root = Path(__file__).resolve().parents[3]
    return assistant_root / "hub_padroes" / "identidade_visual" / "theme.schema.json"


@lru_cache(maxsize=4)
def _carregar_schema_cached(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    if not path.exists():
        raise ErroTema("PATH_MISSING", "O schema do Sistema de Temas não foi encontrado.")
    if not path.is_file():
        raise ErroTema("PATH_NOT_FILE", "O caminho do schema precisa apontar para um arquivo regular.")
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
        parsed = json.loads(text, parse_constant=lambda _x: (_raise_json_constant()))
    except (UnicodeDecodeError, json.JSONDecodeError, ErroTema) as exc:
        raise ErroTema(
            "SCHEMA_INVALID",
            "O schema instalado está corrompido; não prossiga com o tema.",
        ) from exc
    if not isinstance(parsed, dict):
        raise ErroTema("SCHEMA_INVALID", "O schema instalado não possui objeto raiz válido.")
    return parsed


def _carregar_schema(schema_path: Optional[Union[str, Path]]) -> dict[str, Any]:
    path = Path(schema_path) if schema_path is not None else schema_padrao_path()
    if path.is_symlink():
        raise ErroTema("PATH_SYMLINK", "Use um schema regular instalado com o Hub.")
    return deepcopy(_carregar_schema_cached(str(path.resolve(strict=False))))


def _ler_origem(
    origem: Union[str, Path, bytes, bytearray],
    *,
    max_bytes: int,
) -> tuple[bytes, str]:
    if isinstance(origem, (bytes, bytearray)):
        raw = bytes(origem)
        rotulo = "<bytes>"
    elif isinstance(origem, (str, Path)):
        path = Path(origem)
        if path.is_symlink():
            raise ErroTema("PATH_SYMLINK", "Use um arquivo regular, não um link simbólico.")
        if not path.exists():
            raise ErroTema("PATH_MISSING", "O arquivo de tema não foi encontrado.")
        if not path.is_file():
            raise ErroTema("PATH_NOT_FILE", "O tema precisa ser um arquivo JSON regular.")
        try:
            size = path.stat().st_size
        except OSError as exc:
            raise ErroTema("PATH_READ", "Não foi possível inspecionar o arquivo de tema.") from exc
        if size > max_bytes:
            raise ErroTema("JSON_SIZE", f"O tema excede o limite de {max_bytes} bytes.")
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise ErroTema("PATH_READ", "Não foi possível ler o arquivo de tema.") from exc
        rotulo = path.name
    else:
        raise TypeError("origem deve ser caminho, bytes ou bytearray")
    if len(raw) > max_bytes:
        raise ErroTema("JSON_SIZE", f"O tema excede o limite de {max_bytes} bytes.")
    return raw, rotulo


def _parse_json_estrito(raw: bytes, *, max_depth: int) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ErroTema("JSON_BOM", "Salve o tema como UTF-8 sem BOM.")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ErroTema(
            "JSON_UTF8",
            "Salve o tema em UTF-8 válido, sem substituir bytes inválidos.",
        ) from exc

    def pares_sem_duplicata(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ErroTema(
                    "JSON_DUPLICATE_KEY",
                    "Remova a chave JSON duplicada.",
                    campo=key,
                )
            out[key] = value
        return out

    try:
        data = json.loads(
            text,
            object_pairs_hook=pares_sem_duplicata,
            parse_constant=lambda _x: (_raise_json_constant()),
        )
    except ErroTema:
        raise
    except json.JSONDecodeError as exc:
        raise ErroTema(
            "JSON_SYNTAX",
            "Corrija a sintaxe do JSON antes de tentar novamente.",
        ) from exc
    if not isinstance(data, dict):
        raise ErroTema("SCHEMA_ROOT", "O tema precisa ter um objeto JSON na raiz.")
    _validar_unicode(data)
    profundidade = _profundidade(data)
    if profundidade > max_depth:
        raise ErroTema(
            "JSON_DEPTH",
            f"O tema excede a profundidade máxima de {max_depth} níveis.",
        )
    return data


def _raise_json_constant() -> None:
    raise ErroTema("JSON_CONSTANT", "NaN e infinitos não são aceitos no tema.")


def _validar_unicode(value: Any, path: str = "$") -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise ErroTema(
                "JSON_SURROGATE",
                "Use texto Unicode válido, sem surrogate isolado.",
                campo=path,
            )
    elif isinstance(value, dict):
        for key, item in value.items():
            _validar_unicode(key, f"{path}.<chave>")
            _validar_unicode(item, f"{path}.{key}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _validar_unicode(item, f"{path}[{i}]")


def _profundidade(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + max((_profundidade(v) for v in value.values()), default=0)
    if isinstance(value, list):
        return 1 + max((_profundidade(v) for v in value), default=0)
    return 0


def _validar_schema(
    value: Any,
    rule: Mapping[str, Any],
    root: Mapping[str, Any],
    *,
    path: str,
    max_depth: int,
) -> None:
    if "$ref" in rule:
        target = _resolver_ref(rule["$ref"], root)
        _validar_schema(value, target, root, path=path, max_depth=max_depth)
        return
    if "const" in rule and value != rule["const"]:
        _schema_error(path)
    if "enum" in rule and value not in rule["enum"]:
        _schema_error(path)
    if "type" in rule:
        _validar_tipo(value, rule["type"], path)
    if isinstance(value, dict):
        required = rule.get("required", [])
        for key in required:
            if key not in value:
                raise ErroTema(
                    "SCHEMA_REQUIRED",
                    "Inclua todos os campos obrigatórios do contrato.",
                    campo=f"{path}.{key}",
                )
        props = rule.get("properties", {})
        if rule.get("additionalProperties") is False:
            unknown = [key for key in value if key not in props]
            if unknown:
                raise ErroTema(
                    "SCHEMA_UNKNOWN_FIELD",
                    "Remova campos não previstos pelo contrato.",
                    campo=f"{path}.{unknown[0]}",
                )
        for key, child in value.items():
            child_rule = props.get(key)
            if child_rule is not None:
                _validar_schema(
                    child,
                    child_rule,
                    root,
                    path=f"{path}.{key}",
                    max_depth=max_depth,
                )
    if isinstance(value, list):
        if "minItems" in rule and len(value) < rule["minItems"]:
            _schema_error(path)
        if "maxItems" in rule and len(value) > rule["maxItems"]:
            _schema_error(path)
        if rule.get("uniqueItems"):
            for i, item in enumerate(value):
                if any(item == previous for previous in value[:i]):
                    raise ErroTema(
                        "SCHEMA_UNIQUE",
                        "A lista não pode repetir valores.",
                        campo=path,
                    )
        if "items" in rule:
            for i, item in enumerate(value):
                _validar_schema(
                    item,
                    rule["items"],
                    root,
                    path=f"{path}[{i}]",
                    max_depth=max_depth,
                )
    if isinstance(value, str):
        if "minLength" in rule and len(value) < rule["minLength"]:
            _schema_error(path)
        if "maxLength" in rule and len(value) > rule["maxLength"]:
            _schema_error(path)
        pattern = rule.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            _schema_error(path)
    if _is_number(value):
        if "minimum" in rule and value < rule["minimum"]:
            _schema_error(path)
        if "maximum" in rule and value > rule["maximum"]:
            _schema_error(path)
    for branch in rule.get("allOf", []):
        _validar_schema(value, branch, root, path=path, max_depth=max_depth)
    if "if" in rule:
        chosen = (
            rule.get("then")
            if _matches_schema(value, rule["if"], root, path, max_depth)
            else rule.get("else")
        )
        if chosen is not None:
            _validar_schema(value, chosen, root, path=path, max_depth=max_depth)


def _matches_schema(
    value: Any,
    rule: Mapping[str, Any],
    root: Mapping[str, Any],
    path: str,
    max_depth: int,
) -> bool:
    try:
        _validar_schema(value, rule, root, path=path, max_depth=max_depth)
        return True
    except ErroTema:
        return False


def _resolver_ref(ref: str, root: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise ErroTema(
            "SCHEMA_INVALID",
            "O schema instalado contém referência não local.",
        )
    current: Any = root
    try:
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            current = current[part]
    except (KeyError, TypeError) as exc:
        raise ErroTema(
            "SCHEMA_INVALID",
            "O schema instalado contém referência inexistente.",
        ) from exc
    if not isinstance(current, dict):
        raise ErroTema(
            "SCHEMA_INVALID",
            "O schema instalado aponta para definição inválida.",
        )
    return current


def _validar_tipo(value: Any, expected: Any, path: str) -> None:
    allowed = expected if isinstance(expected, list) else [expected]
    for typ in allowed:
        if typ == "object" and isinstance(value, dict):
            return
        if typ == "array" and isinstance(value, list):
            return
        if typ == "string" and isinstance(value, str):
            return
        if typ == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return
        if typ == "number" and _is_number(value):
            return
        if typ == "boolean" and isinstance(value, bool):
            return
        if typ == "null" and value is None:
            return
    raise ErroTema(
        "SCHEMA_TYPE",
        "Use o tipo de valor definido pelo contrato.",
        campo=path,
    )


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _schema_error(path: str) -> None:
    raise ErroTema(
        "SCHEMA_VALUE",
        "Use um valor permitido pelo contrato do tema.",
        campo=path,
    )


def _validar_compatibilidade(documento: Mapping[str, Any]) -> None:
    compat = documento["engine_compatibility"]
    current = _parse_semver(ENGINE_VERSION)
    minimum = _parse_semver(compat["minimum_version"])
    if (
        compat["api_major"] != current[0]
        or current < minimum
        or current[0] >= compat["maximum_major_exclusive"]
    ):
        raise ErroTema(
            "ENGINE_VERSION",
            "Este tema exige uma versão de engine diferente da instalada.",
        )


def _parse_semver(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)",
        value,
    )
    if not match:
        raise ErroTema(
            "ENGINE_VERSION",
            "A versão de compatibilidade não segue major.minor.patch.",
        )
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def _validar_regras_dominio(documento: Mapping[str, Any]) -> None:
    diverging = documento.get("tokens", {}).get("palette.diverging")
    if isinstance(diverging, list) and len(diverging) % 2 == 0:
        raise ErroTema(
            "PALETTE_CENTER",
            "A paleta divergente precisa ter quantidade ímpar de cores para representar um centro.",
            campo="$.tokens.palette.diverging",
        )


def _positive_int(value: Any, fallback: int) -> int:
    return (
        value
        if isinstance(value, int) and not isinstance(value, bool) and value > 0
        else fallback
    )


__all__ = [
    "ENGINE_VERSION",
    "ErroTema",
    "TemaResolvido",
    "carregar_tema",
    "resolver_tema",
    "schema_padrao_path",
]
