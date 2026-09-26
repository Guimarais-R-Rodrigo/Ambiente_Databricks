"""Detecção canônica de notebook Databricks a partir do arquivo `.py`.

Um `.py` no repositório pode ser duas coisas incompatíveis: módulo da biblioteca,
que precisa ser publicado como arquivo para que o import funcione, ou notebook
didático, que precisa ser publicado como notebook para ter células executáveis.
A única diferença entre eles é o marcador na primeira linha de conteúdo.

Por que existe um módulo só para isto: a detecção é usada pela publicação, pela
validação e pelo smoke test, e cada uma dela tira uma conclusão diferente. Se as
três discordarem, o sintoma é silencioso — o notebook é publicado como arquivo, a
conferência aprova porque o nome bate, e o smoke test passa a importá-lo, o que
executa o notebook inteiro fora de contexto.

A versão anterior lia a primeira linha crua e falhava com BOM, linha em branco ou
comentário de encoding antes do marcador — este último é convenção usada por
onze módulos deste repositório.
"""

from __future__ import annotations

from pathlib import Path

MARCADOR_NOTEBOOK = "# Databricks notebook source"

# Linhas que legitimamente antecedem o marcador e não descaracterizam o notebook.
_PREFIXOS_TOLERADOS = ("#!", "# -*-", "# coding", "# vim:")


def texto_e_notebook(texto: str) -> bool:
    """Decide pelo conteúdo já lido, sem tocar no disco.

    Tolera BOM, linhas em branco e comentários de encoding/shebang antes do
    marcador. Qualquer outra linha de código antes dele significa que o arquivo
    é um módulo — o marcador ali seria comentário solto, não declaração.
    """
    for linha in texto.lstrip("﻿").splitlines():
        despida = linha.strip()
        if not despida:
            continue
        if despida == MARCADOR_NOTEBOOK:
            return True
        if despida.startswith(_PREFIXOS_TOLERADOS):
            continue
        return False
    return False


def eh_notebook(caminho: Path) -> bool:
    """Decide pelo arquivo. Só `.py` pode ser notebook neste repositório."""
    if caminho.suffix != ".py":
        return False
    try:
        with caminho.open(encoding="utf-8") as arquivo:
            # 4 KB cobre folgadamente qualquer preâmbulo tolerado.
            return texto_e_notebook(arquivo.read(4096))
    except OSError:
        return False
