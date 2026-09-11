"""Leitura conservadora de links Markdown sem interpretar exemplos como links.

Não é um renderizador CommonMark completo. Cobre links inline, imagens, cercas
backtick/tilde e código inline usados nos READMEs deste repositório. Mantém offsets
para que consumidores possam reescrever só o destino, sem reformatação do texto.
"""
from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterator

LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[\"'][^\n]*?[\"'])?\)")


def _blank(text: str) -> str:
    return ''.join('\n' if c == '\n' else ' ' for c in text)


def mask_fences(text: str) -> str:
    """Preserva tamanho/linhas e mascara blocos cercados e comentários HTML."""
    lines = text.splitlines(keepends=True)
    fence: tuple[str, int] | None = None
    out = []
    for line in lines:
        opening = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            out.append(_blank(line))
            if re.match(r'^ {0,3}' + re.escape(fence[0]) + r'{' + str(fence[1]) + r',}\s*$', line):
                fence = None
        elif opening:
            fence = (opening[1][0], len(opening[1]))
            out.append(_blank(line))
        else:
            out.append(line)
    return re.sub(r'<!--.*?-->', lambda m: _blank(m[0]), ''.join(out), flags=re.S)


def mask_code(text: str) -> str:
    masked = mask_fences(text)
    return re.sub(r'(`+)(?!`)([^\n]*?)(?<!`)\1(?!`)', lambda m: _blank(m[0]), masked)


def markdown_links(text: str) -> Iterator[re.Match[str]]:
    yield from LINK_RE.finditer(mask_code(text))


def slug(text: str) -> str:
    """Slug explícito estável usado na revisão; não simula toda versão do GitHub."""
    text = re.sub(r'<[^>]+>', '', text).replace('`', '').replace('*', '').lower()
    text = ''.join(c for c in text if c.isalnum() or c in ' _-')
    return re.sub(r'\s+', '-', text.strip()).strip('-')


def anchors(text: str) -> set[str]:
    visible = mask_fences(text)
    result = set(re.findall(r'<a\s+id=[\"\']([^\"\']+)[\"\']\s*>', visible))
    occurrences: dict[str, int] = {}
    for match in re.finditer(r'(?m)^#{1,6}\s+(.+?)\s*#*$', visible):
        raw = match[1]
        label = slug(raw)
        count = occurrences.get(label, 0)
        occurrences[label] = count + 1
        label = label + (f'-{count}' if count else '')
        result.add(label)
        # Compatibilidade com âncoras históricas geradas após emoji inicial.
        if raw and not raw[0].isalnum() and raw[0] != '`':
            result.add('-' + label)
            result.add('\ufe0f-' + label)
    return result


def python_blocks(text: str) -> Iterator[tuple[int, str]]:
    """Extrai blocos Python e sua linha inicial; não executa seu conteúdo."""
    for m in re.finditer(r'(?ms)^ {0,3}(`{3,})python\s*\n(.*?)^ {0,3}\1\s*$', text):
        yield text.count('\n', 0, m.start()) + 2, m[2]
