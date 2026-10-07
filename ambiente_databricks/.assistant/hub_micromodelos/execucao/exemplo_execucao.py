"""Entrada curta para o laboratório sintético do Hub."""
from __future__ import annotations
import json
from .execucao import run_greenfield_lab

if __name__ == "__main__":
    resultado = run_greenfield_lab()
    print(json.dumps({"ambiente": resultado["environment"], "resumo": resultado["scoring"]["aggregate"]}, ensure_ascii=False, indent=2))
