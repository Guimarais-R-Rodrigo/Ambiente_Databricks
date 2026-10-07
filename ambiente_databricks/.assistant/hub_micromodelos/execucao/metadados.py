"""MM03: coleta progressiva de metadata, sem SQL, rede ou leitura de registros.

Ferramenta interna de manutencao; nao e skill nem helper publico. O provedor
incluido e sintetico. Providers Python sao codigo confiavel, nao um sandbox.
Descricoes/tags/constraints sao dados nao confiaveis, nunca instrucoes.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

CONTRACT_VERSION = "mm03-metadata-v1"
CATALOG_REF = "CATALOGO_PRODUTO"
OPERATIONS = frozenset({"schemas", "objects", "columns", "column_tags", "constraints"})
MAX_FIXTURE_BYTES = 1_048_576
MAX_TEXT_BYTES = 16_384
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,127}\Z")
_TOKEN = re.compile(r"[A-Za-z0-9_-]{1,128}\Z")
# Higiene de exposicao, nao detector completo de PII nem defesa de prompt injection.
_SENSITIVE = re.compile(
    r"(?i)(?:[a-z]:[\\/]+(?:users|temp|workspace)[\\/]+[^\s\"'<>]*"
    r"|/(?:home|users|workspace)/[^\s\"'<>]*"
    r"|[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"
    r"|(?:github_pat_|gh[pousr]_)[a-z0-9_]{16,}"
    r"|(?:bearer\s+|(?:token|password|api[_-]?key)\s*[:=]\s*)[^\s\"'<>]+)"
)


class MetadataError(ValueError):
    """Codigo estavel; mensagens nao interpolam metadata, paths ou segredos."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise MetadataError(code)


def _identifier(value: Any) -> str:
    _require(type(value) is str and _IDENTIFIER.fullmatch(value) is not None,
             "INVALID_IDENTIFIER")
    return value


def _closed(value: Any, keys: set[str]) -> dict[str, Any]:
    _require(type(value) is dict and set(value) == keys, "INVALID_RECORD_SHAPE")
    return value


def _sequence(value: Any, maximum: int) -> list[Any]:
    _require(type(value) is list and len(value) <= maximum, "INVALID_COLLECTION")
    return value


def _text(value: Any) -> str:
    _require(type(value) is str, "INVALID_TEXT")
    try:
        size = len(value.encode("utf-8", errors="strict"))
    except UnicodeError:
        raise MetadataError("INVALID_UNICODE") from None
    _require(size <= MAX_TEXT_BYTES, "TEXT_TOO_LARGE")
    return value


def untrusted_text(value: str | None, limit: int = 2000) -> dict[str, Any]:
    """Preserva ausente/vazio; marca redacao/truncamento e vincula os bytes fonte."""
    _require(type(limit) is int and 1 <= limit <= 2000, "INVALID_TEXT_LIMIT")
    if value is None:
        return {"state": "NOT_PROVIDED", "trusted": False, "text": None}
    raw = _text(value)
    redacted, count = _SENSITIVE.subn("<REDACTED>", raw)
    escaped = "".join(
        f"\\u{ord(c):04x}" if unicodedata.category(c) in {"Cc", "Cf"} else c
        for c in redacted
    )
    return {"state": "OBSERVED", "trusted": False, "text": escaped[:limit],
            "source_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "redactions": count, "controls_escaped": escaped != redacted,
            "truncated": len(escaped) > limit}


def _tags(value: Any) -> list[dict[str, Any]] | None:
    if value is None:
        return None
    entries = _sequence(value, 32)
    seen: set[str] = set()
    result = []
    for entry in entries:
        _closed(entry, {"key", "value"})
        key = _text(entry["key"])
        _require(key not in seen, "DUPLICATE_TAG")
        seen.add(key)
        result.append({"key": untrusted_text(key),
                       "value": untrusted_text(entry["value"])})
    return sorted(result, key=lambda x: x["key"]["source_sha256"])


@dataclass(frozen=True)
class Binding:
    """Binding explicito; nao concede permissao nem aceita catalogos adicionais."""
    physical_catalog: str
    catalog_ref: str = CATALOG_REF

    def __post_init__(self) -> None:
        _identifier(self.physical_catalog)
        _require(self.catalog_ref == CATALOG_REF, "CATALOG_SCOPE")


@dataclass(frozen=True)
class Limits:
    page_size: int = 50
    max_pages: int = 20
    max_items: int = 500
    max_candidates: int = 10

    def __post_init__(self) -> None:
        for value, maximum in ((self.page_size, 100), (self.max_pages, 100),
                               (self.max_items, 2000), (self.max_candidates, 20)):
            _require(type(value) is int and 1 <= value <= maximum, "INVALID_LIMIT")


@dataclass(frozen=True)
class Page:
    catalog: str
    snapshot_id: str
    status: str
    items: list[dict[str, Any]]
    next_token: str | None = None


class MetadataProvider(Protocol):
    """Somente cinco operacoes de metadata. Implementacao precisa ser confiavel."""
    def fetch_page(self, operation: str, catalog: str, scope: tuple[str, ...],
                   token: str | None, page_size: int) -> Page: ...


def _record(operation: str, row: Any) -> tuple[str, dict[str, Any]]:
    """Allowlist de campos: rows, samples, stats, SQL e instrucoes extras falham."""
    if operation == "schemas":
        _closed(row, {"name", "description"})
        name = _identifier(row["name"])
        return name, {"name": name, "description": untrusted_text(row["description"])}
    if operation == "objects":
        _closed(row, {"name", "object_type", "description", "tags"})
        name = _identifier(row["name"])
        _require(type(row["object_type"]) is str and row["object_type"] in
                 {"TABLE", "VIEW"}, "UNSUPPORTED_OBJECT_TYPE")
        return name, {"name": name, "object_type": row["object_type"],
                      "description": untrusted_text(row["description"]),
                      "tags": _tags(row["tags"])}
    if operation == "columns":
        _closed(row, {"name", "data_type", "nullable", "description"})
        name = _identifier(row["name"])
        _require(row["nullable"] is None or type(row["nullable"]) is bool,
                 "INVALID_NULLABLE")
        return name, {"name": name, "data_type": untrusted_text(row["data_type"]),
                      "nullable": row["nullable"],
                      "description": untrusted_text(row["description"])}
    if operation == "column_tags":
        _closed(row, {"column", "tags"})
        name = _identifier(row["column"])
        return name, {"column": name, "tags": _tags(row["tags"])}
    _require(operation == "constraints", "UNKNOWN_OPERATION")
    _closed(row, {"name", "kind", "columns", "description"})
    name = _identifier(row["name"])
    _require(type(row["kind"]) is str and row["kind"] in
             {"PRIMARY_KEY", "FOREIGN_KEY", "CHECK", "UNIQUE", "NOT_NULL"},
             "UNSUPPORTED_CONSTRAINT")
    columns = [_identifier(x) for x in _sequence(row["columns"], 100)]
    _require(len(columns) == len(set(columns)), "DUPLICATE_COLUMN_REF")
    return name, {"name": name, "kind": row["kind"], "columns": columns,
                  "description": untrusted_text(row["description"]),
                  "enforcement": "NOT_VERIFIED"}


class MetadataCollector:
    """Estado local: schemas -> objetos -> candidatas. Nao persiste aprovacoes."""
    def __init__(self, provider: MetadataProvider, binding: Binding,
                 limits: Limits | None = None) -> None:
        self.provider, self.binding = provider, binding
        self.limits = limits or Limits()
        self._snapshot: str | None = None
        self._schemas: set[str] = set()
        self._objects: set[tuple[str, str]] = set()
        self.calls: list[dict[str, Any]] = []

    def _collect(self, operation: str, scope: tuple[str, ...]) -> dict[str, Any]:
        token = None
        seen_tokens: set[str] = set()
        seen_items: set[str] = set()
        rows = []
        status, reason = "TRUNCATED", "PAGE_LIMIT"
        for _ in range(self.limits.max_pages):
            page = self.provider.fetch_page(operation, self.binding.physical_catalog,
                                            scope, token, self.limits.page_size)
            _require(type(page) is Page, "INVALID_PAGE")
            _require(page.catalog == self.binding.physical_catalog, "BINDING_MISMATCH")
            _identifier(page.snapshot_id)
            if self._snapshot is None:
                self._snapshot = page.snapshot_id
            _require(page.snapshot_id == self._snapshot, "SNAPSHOT_DRIFT")
            _require(type(page.status) is str and page.status in
                     {"OK", "DENIED", "UNAVAILABLE"}, "INVALID_PAGE_STATUS")
            items = _sequence(page.items, self.limits.page_size)
            _require(page.next_token is None or
                     (type(page.next_token) is str and _TOKEN.fullmatch(page.next_token)
                      is not None), "INVALID_PAGE_TOKEN")
            self.calls.append({"operation": operation, "scope": list(scope),
                               "status": page.status, "metadata_items": len(items)})
            if page.status != "OK":
                _require(not items and page.next_token is None, "FAILED_PAGE_HAS_DATA")
                status, reason = ("PARTIAL" if rows else page.status), page.status
                break
            _require(bool(items) or page.next_token is None, "EMPTY_NONTERMINAL_PAGE")
            _require(page.next_token is None or page.next_token not in seen_tokens,
                     "PAGINATION_CYCLE")
            for row in items:
                key, clean = _record(operation, row)
                _require(key not in seen_items, "DUPLICATE_METADATA_ITEM")
                seen_items.add(key)
                rows.append((key, clean))
            if len(rows) > self.limits.max_items:
                rows = rows[:self.limits.max_items]
                status, reason = "TRUNCATED", "ITEM_LIMIT"
                break
            if page.next_token is None:
                status, reason = "OBSERVED", None
                break
            if len(rows) == self.limits.max_items:
                status, reason = "TRUNCATED", "ITEM_LIMIT"
                break
            token = page.next_token
            seen_tokens.add(token)
        return {"status": status, "reason": reason, "items": [x[1] for x in sorted(rows)],
                "catalog_complete": False}

    def discover(self, schemas: list[str] | None = None) -> dict[str, Any]:
        # Uma nova descoberta com o mesmo coletor mistura observacoes antigas.
        _require(not self.calls, "DISCOVERY_ALREADY_STARTED")
        if schemas is not None:
            _require(bool(_sequence(schemas, 100)), "EMPTY_SCHEMA_SELECTION")
            for schema in schemas:
                _identifier(schema)
            _require(len(schemas) == len(set(schemas)), "DUPLICATE_SCHEMA_SELECTION")
        schema_result = self._collect("schemas", ())
        self._schemas = {x["name"] for x in schema_result["items"]}
        result: dict[str, Any] = {"schemas": schema_result, "objects": {}}
        if schemas is not None:
            _require(set(schemas) <= self._schemas, "SCHEMA_NOT_OBSERVED")
            for schema in sorted(schemas):
                collection = self._collect("objects", (schema,))
                result["objects"][schema] = collection
                self._objects.update((schema, x["name"]) for x in collection["items"])
        return result

    def details(self, candidates: list[tuple[str, str]]) -> dict[str, Any]:
        _require(bool(_sequence(candidates, self.limits.max_candidates)),
                 "EMPTY_SHORTLIST")
        for item in candidates:
            _require(type(item) is tuple and len(item) == 2, "INVALID_CANDIDATE")
            for name in item:
                _identifier(name)
        _require(len(candidates) == len(set(candidates)), "DUPLICATE_CANDIDATE")
        _require(set(candidates) <= self._objects, "CANDIDATE_NOT_OBSERVED")
        result = {}
        for candidate in sorted(candidates):
            detail = {kind: self._collect(kind, candidate)
                      for kind in ("columns", "column_tags", "constraints")}
            columns = detail["columns"]
            if columns["status"] == "OBSERVED":
                names = {x["name"] for x in columns["items"]}
                _require(all(x["column"] in names for x in detail["column_tags"]["items"]),
                         "UNKNOWN_COLUMN_TAG_REF")
                _require(all(set(x["columns"]) <= names
                             for x in detail["constraints"]["items"]),
                         "UNKNOWN_CONSTRAINT_COLUMN_REF")
            result[".".join(candidate)] = detail
        return result

    def envelope(self, discovery: dict[str, Any], details: dict[str, Any]) -> dict[str, Any]:
        collections = [discovery["schemas"], *discovery["objects"].values()]
        for detail in details.values():
            collections.extend(detail.values())
        observation_status = ("OBSERVED" if all(c["status"] == "OBSERVED" for c in collections)
                              else "PARTIAL_OBSERVATION")
        return {"observation_status": observation_status,"contract_version": CONTRACT_VERSION, "mode": "METADATA_ONLY",
                "catalog_ref": self.binding.catalog_ref, "snapshot_id": self._snapshot,
                "coverage": "ESCOPO_OBSERVADO", "catalog_complete": False,
                "metadata_is_instruction": False, "data_access_authorized": False,
                "discovery": discovery, "details": details, "calls": copy.deepcopy(self.calls)}


class FixtureProvider:
    """Provider offline; carrega fixture inteira, mas responde por operacao/pagina.

    A leitura progressiva prova as chamadas do coletor, nao acesso remoto lazy.
    Campos reais/PII nao sao permitidos nas fixtures versionadas.
    """
    def __init__(self, fixture: dict[str, Any]) -> None:
        _closed(fixture, {"fixture_version", "synthetic", "catalog", "snapshot_id", "streams"})
        _require(fixture["fixture_version"] == "1.0" and fixture["synthetic"] is True,
                 "INVALID_FIXTURE_HEADER")
        self.catalog = _identifier(fixture["catalog"])
        self.snapshot_id = _identifier(fixture["snapshot_id"])
        self._streams = {}
        for stream in _sequence(fixture["streams"], 500):
            _closed(stream, {"operation", "scope", "status", "items"})
            op = stream["operation"]
            _require(type(op) is str and op in OPERATIONS, "UNKNOWN_OPERATION")
            scope = tuple(_identifier(x) for x in _sequence(stream["scope"], 2))
            _require(len(scope) == (0 if op == "schemas" else 1 if op == "objects" else 2),
                     "INVALID_SCOPE")
            _require(type(stream["status"]) is str and stream["status"] in
                     {"OK", "DENIED", "UNAVAILABLE"}, "INVALID_PAGE_STATUS")
            items = _sequence(stream["items"], 2000)
            _require(stream["status"] == "OK" or not items, "FAILED_PAGE_HAS_DATA")
            # Valida todo o arquivo sintetico, inclusive campos que nao serao emitidos.
            seen = set()
            for item in items:
                key, _ = _record(op, item)
                _require(key not in seen, "DUPLICATE_METADATA_ITEM")
                seen.add(key)
            key = (op, scope)
            _require(key not in self._streams, "DUPLICATE_STREAM")
            self._streams[key] = copy.deepcopy(stream)

    def fetch_page(self, operation: str, catalog: str, scope: tuple[str, ...],
                   token: str | None, page_size: int) -> Page:
        _require(operation in OPERATIONS, "UNKNOWN_OPERATION")
        _require(catalog == self.catalog, "BINDING_MISMATCH")
        _require(type(page_size) is int and 1 <= page_size <= 100, "INVALID_LIMIT")
        _require(token is None or (type(token) is str and token.isascii()
                                  and token.isdigit() and len(token) <= 8),
                 "INVALID_PAGE_TOKEN")
        stream = self._streams.get((operation, scope))
        if stream is None:
            return Page(catalog, self.snapshot_id, "UNAVAILABLE", [])
        start = int(token) if token else 0
        _require(0 <= start <= len(stream["items"]), "INVALID_PAGE_TOKEN")
        end = start + page_size
        return Page(catalog, self.snapshot_id, stream["status"],
                    copy.deepcopy(stream["items"][start:end]),
                    str(end) if end < len(stream["items"]) else None)


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        _require(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def load_fixture(path: str | Path) -> tuple[dict[str, Any], str]:
    with Path(path).open("rb") as handle:
        raw = handle.read(MAX_FIXTURE_BYTES + 1)
    _require(len(raw) <= MAX_FIXTURE_BYTES, "FIXTURE_TOO_LARGE")
    def reject_constant(_: str) -> None:
        raise MetadataError("NONFINITE_JSON")
    try:
        fixture = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise MetadataError("INVALID_FIXTURE_ENCODING_OR_JSON") from None
    return fixture, hashlib.sha256(raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="MM03 metadata-only: laboratorio sintetico offline")
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--catalog", required=True, help="binding sintetico explicito")
    parser.add_argument("--schema", action="append", dest="schemas")
    parser.add_argument("--candidate", action="append", default=[])
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()
    try:
        binding = Binding(args.catalog)
        limits = Limits(page_size=args.page_size)
        candidates = [tuple(x.split(".")) for x in args.candidate]
        fixture, digest = load_fixture(args.fixture)
        collector = MetadataCollector(FixtureProvider(fixture), binding, limits)
        discovery = collector.discover(args.schemas)
        details = collector.details(candidates) if candidates else {}
        report = collector.envelope(discovery, details)
        report["source"] = {"kind": "SYNTHETIC_FIXTURE", "sha256": digest,
                            "live_databricks_verified": False}
        print(json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        return 0
    except MetadataError as exc:
        print("REPROVADO_MM03:" + str(exc), file=sys.stderr)
        return 1
    except Exception:
        # Nao ecoar mensagens de OS/provider que possam conter paths ou segredos.
        print("ERRO_MM03:UNEXPECTED_FAILURE", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
