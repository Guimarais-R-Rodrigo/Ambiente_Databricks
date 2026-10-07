"""Destinos Markdown locais, sem dependências ou interpretação de HTML arbitrário.

Cobre links/imagens inline (parênteses balanceados, escapes, título opcional,
<destinos com espaços>) e referências completas, colapsadas e atalhos definidos.
Contêineres de citação/lista são normalizados antes de referências e cercas.
Imagens dentro de rótulos de links também têm seus recursos conferidos.
Cercas, comentários HTML e código inline seguem mask_code. Não é um renderizador
CommonMark completo; referências sem definição são texto, como no Markdown.
"""
from __future__ import annotations

import html
import re
from collections.abc import Iterator
from urllib.parse import unquote

from markdown_contract import mask_code

ESCAPE = re.compile(r'\\([!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~])')
DEFINITION = re.compile(r'^ {0,3}\[((?:\\.|[^\]\\\n])+)\]:[ \t]*(?:\n[ \t]*)?', re.M)
REMOTE = re.compile(r'^(?:https?|mailto|data|ftp|tel):', re.I)


def _decoded(value: str) -> str:
    return html.unescape(ESCAPE.sub(r'\1', value))


def _label(value: str) -> str:
    return ' '.join(_decoded(value).split()).casefold()


def _destination(text: str, start: int) -> tuple[str, int] | None:
    if start >= len(text):
        return None
    if text[start] == '<':
        i = start + 1
        while i < len(text):
            if text[i] == '\\' and i + 1 < len(text):
                i += 2
                continue
            if text[i] in '\n\r<':
                return None
            if text[i] == '>':
                return _decoded(text[start + 1:i]), i + 1
            i += 1
        return None
    i, depth = start, 0
    while i < len(text):
        c = text[i]
        if c == '\\' and i + 1 < len(text):
            i += 2
            continue
        if c.isspace() or ord(c) < 32:
            break
        if c == '(':
            depth += 1
        elif c == ')':
            if depth == 0:
                break
            depth -= 1
        i += 1
    if depth or i == start:
        return None
    return _decoded(text[start:i]), i


def _closing_label(text: str, start: int) -> int | None:
    i, depth = start + 1, 1
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            i += 2
            continue
        if text[i] == '[':
            depth += 1
        elif text[i] == ']':
            depth -= 1
            if not depth:
                return i
        i += 1
    return None


def _inline_end(text: str, index: int) -> int | None:
    start = index
    while index < len(text) and text[index].isspace():
        index += 1
    if index < len(text) and text[index] == ')':
        return index + 1
    if index == start or index >= len(text) or text[index] not in '\"\'(':
        return None
    delimiter = ')' if text[index] == '(' else text[index]
    index += 1
    while index < len(text):
        if text[index] == '\\' and index + 1 < len(text):
            index += 2
            continue
        if text[index] == delimiter:
            index += 1
            while index < len(text) and text[index].isspace():
                index += 1
            return index + 1 if index < len(text) and text[index] == ')' else None
        index += 1
    return None


def _container_source(text: str) -> str:
    """Expose blockquote/list contents before code masking and definitions."""
    result, list_indent = [], 0
    for line in text.splitlines(keepends=True):
        # Quotes can nest and contain lists/fences; removing prefixes first is
        # essential so quoted code examples remain examples.
        while re.match(r'^ {0,3}>[ \t]?', line):
            line = re.sub(r'^ {0,3}>[ \t]?', '', line, count=1)
        if list_indent and line.startswith(' ' * list_indent):
            line = line[list_indent:]
        elif line.strip():
            list_indent = 0
        while True:
            marker = re.match(r'^ {0,3}(?:[-+*]|[0-9]+[.)])[ \t]+', line)
            quote = re.match(r'^ {0,3}>[ \t]?', line)
            if marker:
                list_indent += marker.end()
                line = line[marker.end():]
            elif quote:
                line = line[quote.end():]
            else:
                break
        result.append(line)
    return ''.join(result)


def markdown_destinations(text: str) -> Iterator[str]:
    visible = mask_code(_container_source(text))
    definitions = {}
    spans = []
    for match in DEFINITION.finditer(visible):
        parsed = _destination(visible, match.end())
        if parsed:
            target, end = parsed
            definitions.setdefault(_label(match[1]), target)
            line_end = visible.find('\n', end)
            spans.append((match.start(), len(visible) if line_end < 0 else line_end))
    for start, end in reversed(spans):
        visible = visible[:start] + ' ' * (end - start) + visible[end:]
    for target, _ in _inline_destinations(visible, definitions):
        yield target


def _inline_destinations(visible: str, definitions: dict[str, str]) -> Iterator[tuple[str, bool]]:
    i = 0
    while i < len(visible):
        if visible[i] == '\\':
            i += 2
            continue
        if visible[i] != '[':
            i += 1
            continue
        close = _closing_label(visible, i)
        if close is None:
            i += 1
            continue
        label = visible[i + 1:close]
        # Nested images carry a resource; an inner normal link takes precedence
        # over the outer link-looking literal in CommonMark.
        nested = list(_inline_destinations(label, definitions)) if '[' in label else []
        yield from nested
        if any(not is_image for _, is_image in nested):
            i = close + 1
            continue
        is_image = i > 0 and visible[i - 1] == '!' and (i < 2 or visible[i - 2] != '\\')
        next_index = close + 1
        if next_index < len(visible) and visible[next_index] == '(':
            start = next_index + 1
            while start < len(visible) and visible[start].isspace():
                start += 1
            parsed = _destination(visible, start)
            end = _inline_end(visible, parsed[1]) if parsed else None
            if parsed and end:
                yield parsed[0], is_image
                i = end
                continue
        if next_index < len(visible) and visible[next_index] == '[':
            ref_end = _closing_label(visible, next_index)
            if ref_end is not None:
                reference = visible[next_index + 1:ref_end] or label
                if _label(reference) in definitions:
                    yield definitions[_label(reference)], is_image
                    i = ref_end + 1
                    continue
        if _label(label) in definitions:
            yield definitions[_label(label)], is_image
        i = close + 1


def is_remote_destination(raw: str) -> bool:
    return bool(REMOTE.match(raw)) or raw.startswith('//')


def local_destination_path(raw: str) -> str | None:
    """Remove URL query/fragment before decoding; encoded #/? remain filename bytes."""
    if is_remote_destination(raw):
        return None
    path = raw.partition('#')[0].partition('?')[0]
    return unquote(path) if path else None
