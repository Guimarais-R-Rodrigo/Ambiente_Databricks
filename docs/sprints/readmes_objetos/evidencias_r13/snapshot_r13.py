from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("validator", type=Path)
    args = parser.parse_args()
    output = args.validator.read_text(encoding="utf-8").strip()
    if "APROVADO: 0 falha(s), 0 aviso(s)" not in output:
        raise RuntimeError("validador R13 não está aprovado")

    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start = text.find("### Estado verificável do gate local")
    fence = text.find("```text\n", start)
    end = text.find("\n```", fence)
    if min(start, fence, end) < 0:
        raise RuntimeError("snapshot do README raiz não encontrado")
    path.write_text(text[:fence + len("```text\n")] + output + text[end:], encoding="utf-8")


if __name__ == "__main__":
    main()
