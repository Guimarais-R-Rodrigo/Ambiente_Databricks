"""Compatibilidade do comando histórico; implementação no produto do Hub."""
from __future__ import annotations
import sys
from pathlib import Path
_PRODUTO = Path(__file__).resolve().parents[1] / "ambiente_fonte" / ".assistant"
if str(_PRODUTO) not in sys.path:
    sys.path.insert(0, str(_PRODUTO))
from hub_micromodelos.execucao import assinatura as _impl

def __getattr__(nome: str):
    return getattr(_impl, nome)

if __name__ == "__main__":
    raise SystemExit(_impl.main())
