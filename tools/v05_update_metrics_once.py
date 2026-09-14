"""Atualiza somente as 14 métricas medidas do README raiz da candidata V05."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
EXPECTED_SHA = "4dfc6f585e48742d839be75b64d7b3c7dcaf8388"


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


if blob_sha(README) != EXPECTED_SHA:
    raise SystemExit("README raiz mudou; não atualizar métricas sem nova medição")

text = README.read_text(encoding="utf-8")
replacements = {
    "markdown / links   : 215 arquivos / 1356 links relativos": "markdown / links   : 217 arquivos / 1382 links relativos",
    "notebooks / links  : 79 notebooks / 98 links relativos": "notebooks / links  : 80 notebooks / 101 links relativos",
    "readmes de objeto  : 75/75 operacionais; 3/3 exemplares; 0 pendentes (estrutura, não aceite editorial)": "readmes de objeto  : 76/76 operacionais; 3/3 exemplares; 0 pendentes (estrutura, não aceite editorial)",
    "pastas de objeto   : 61 conferidas (nome, arquivos, __init__)": "pastas de objeto   : 62 conferidas (nome, arquivos, __init__)",
    "forma da pasta     : 59 conferidas (o módulo tem o nome da pasta)": "forma da pasta     : 60 conferidas (o módulo tem o nome da pasta)",
    "contrato de dados  : 61 pares (saída: o que o notebook consome)": "contrato de dados  : 62 pares (saída: o que o notebook consome)",
    "contrato de entrada: 59 pares (entrada: o que o notebook passa)": "contrato de entrada: 60 pares (entrada: o que o notebook passa)",
    "saída colada       : 78 notebooks com bloco real, 0 sem": "saída colada       : 79 notebooks com bloco real, 0 sem",
    "idioma da docstring: 61 módulos, 0 com docstring em inglês": "idioma da docstring: 62 módulos, 0 com docstring em inglês",
    "normas do molde    : 71 arquivos, 0 violação(ões)": "normas do molde    : 72 arquivos, 0 violação(ões)",
    "notebook exercita  : 59 objetos, 0 notebook(s) que só importam": "notebook exercita  : 60 objetos, 0 notebook(s) que só importam",
    "python (AST)       : 214 arquivos": "python (AST)       : 217 arquivos",
    "repo (identidade)  : 1318 arquivos varridos no repositório editável/derivado": "repo (identidade)  : 1334 arquivos varridos no repositório editável/derivado",
    "repo (links)       : 1795 links fora da raiz analisada": "repo (links)       : 1838 links fora da raiz analisada",
}

for old, new in replacements.items():
    if text.count(old) != 1:
        raise SystemExit(f"métrica antiga ausente/duplicada: {old}")
    text = text.replace(old, new)

README.write_text(text, encoding="utf-8")
status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines()
changed = {line[3:] for line in status}
if changed != {"README.md"}:
    raise SystemExit(f"escopo inesperado: {sorted(changed)}")
subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
print("OK: somente as 14 métricas medidas do README raiz foram atualizadas.")
