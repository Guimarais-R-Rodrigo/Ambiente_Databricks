"""Confere contagens E0 e prepara um handoff fictício sem submeter ou publicar."""
from __future__ import annotations

import json

from executar_exemplo import PASTA, executar
from hub_micromodelos.execucao import entrega, especificacao, fluxo


def main() -> int:
    resultado = executar()
    esperado = json.loads((PASTA / "resultado_esperado.json").read_text(encoding="utf-8"))
    if resultado != esperado:
        raise ValueError("O resultado sintético diverge do oráculo antes do handoff")

    linhas = resultado["resultado"]
    contagens = {classe: sum(linha["classificacao"] == classe for linha in linhas)
                 for classe in ("TRUE", "FALSE", "INDETERMINADO")}
    scores = [linha["score"] for linha in linhas if linha["score"] is not None]
    agregado = {
        "populacao": len(linhas),
        "contagens": contagens,
        "scores_emitidos": len(scores),
        "score_min": min(scores) if scores else None,
        "score_max": max(scores) if scores else None,
        "score_media": sum(scores) / len(scores) if scores else None,
    }
    if sum(contagens.values()) != agregado["populacao"] or len(scores) != resultado["resumo"]["scores_emitidos"]:
        raise ValueError("Contagens ou cobertura de score não reconciliadas")

    modelo = especificacao.load_document(PASTA / "micromodelo.yaml")
    schema = especificacao.load_schema(fluxo.SCHEMA)
    rascunho = entrega.prepare_handoff(modelo, schema, agregado)
    if (rascunho["spec_fingerprint"] != resultado["assinatura_especificacao"]
            or rascunho["aggregate"]["status"] != "SUPPLIED_UNVERIFIED"
            or rascunho["published"] is not False):
        raise ValueError("Handoff sintético inconsistente")
    print(json.dumps({
        "ambiente": resultado["ambiente"],
        "especificacao": rascunho["spec_fingerprint"],
        "agregado_conferido_localmente": agregado,
        "estado_handoff": rascunho["status"],
        "estado_agregado_no_handoff": rascunho["aggregate"]["status"],
        "decisoes_pendentes": rascunho["required_decisions"],
        "publicado": rascunho["published"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
