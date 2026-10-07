"""Demonstra recência de contato com sete pessoas inteiramente fictícias."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

PASTA = Path(__file__).resolve().parent
RAIZ_ASSISTANT = PASTA.parents[2]
if str(RAIZ_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(RAIZ_ASSISTANT))

from hub_micromodelos.execucao import assinatura, especificacao, fluxo  # noqa: E402


class ExemploInvalido(ValueError):
    """Os dados não pertencem ao cenário sintético documentado."""


def executar() -> dict[str, Any]:
    """Lê apenas os arquivos sintéticos vizinhos e calcula o resultado local."""
    contrato = especificacao.load_schema(fluxo.SCHEMA)
    modelo = especificacao.load_document(PASTA / "micromodelo.yaml")
    problemas = especificacao.validate_spec(modelo, contrato)
    if problemas:
        raise ExemploInvalido("Especificação inválida: " + ", ".join(str(p) for p in problemas))
    dados = json.loads((PASTA / "dados_sinteticos.json").read_text(encoding="utf-8"))
    if set(dados) != {"ambiente", "data_referencia", "populacao", "eventos"}:
        raise ExemploInvalido("Estrutura dos dados sintéticos inesperada")
    if dados["ambiente"] != "E0_SINTETICO_LOCAL":
        raise ExemploInvalido("Este exemplo aceita apenas a fixture E0 sintética")
    referencia = date.fromisoformat(dados["data_referencia"])
    limiares = {item["id"]: item for item in modelo["classificacao"]["limiares"]}
    componentes = {item["id"]: item for item in modelo["score"]["componentes"]}
    if (set(limiares) != {"janela_recencia_dias"}
            or limiares["janela_recencia_dias"]["operador"] != "LTE"
            or limiares["janela_recencia_dias"]["unidade"] != "dias"
            or set(componentes) != {"proximidade_temporal", "cobertura_confirmada"}
            or modelo["score"]["tipo_semantica"] != "FORCA_EVIDENCIA"):
        raise ExemploInvalido("A execução didática não cobre esta variante da especificação")
    janela = limiares["janela_recencia_dias"]["valor"]
    if type(janela) is not int or not 0 < janela <= 365:
        raise ExemploInvalido("Janela sintética inválida")
    pesos = {nome: item["peso"] for nome, item in componentes.items()}
    if abs(sum(pesos.values()) - 1) > 1e-12:
        raise ExemploInvalido("Pesos sintéticos não somam um")

    pessoas: dict[str, bool] = {}
    for item in dados["populacao"]:
        if (type(item) is not dict or set(item) != {"id_entidade", "cobertura_completa"}
                or type(item["id_entidade"]) is not str or not item["id_entidade"]
                or type(item["cobertura_completa"]) is not bool
                or item["id_entidade"] in pessoas):
            raise ExemploInvalido("População sintética inválida")
        pessoas[item["id_entidade"]] = item["cobertura_completa"]
    if not pessoas:
        raise ExemploInvalido("População sintética vazia")
    sinais: dict[str, list[tuple[str, int]]] = {nome: [] for nome in pessoas}
    vistos: set[str] = set()
    for item in dados["eventos"]:
        if (type(item) is not dict
                or set(item) != {"event_id", "id_entidade", "data_evento", "tipo_evento"}
                or type(item["event_id"]) is not str or not item["event_id"]
                or item["event_id"] in vistos or item["id_entidade"] not in pessoas
                or item["tipo_evento"] not in {"CONFIRMADO", "NEGATIVO_VERIFICADO", "ESTORNADO"}):
            raise ExemploInvalido("Evento sintético inválido")
        vistos.add(item["event_id"])
        try:
            idade = (referencia - date.fromisoformat(item["data_evento"])).days
        except (TypeError, ValueError) as exc:
            raise ExemploInvalido("Data de evento inválida") from exc
        if idade < 0:
            raise ExemploInvalido("Evento posterior à referência")
        sinais[item["id_entidade"]].append((item["tipo_evento"], idade))

    linhas: list[dict[str, Any]] = []
    for pessoa, cobertura in sorted(pessoas.items()):
        eventos = sinais[pessoa]
        recentes = [idade for tipo, idade in eventos if tipo == "CONFIRMADO" and idade <= janela]
        negativo = any(tipo == "NEGATIVO_VERIFICADO" and idade <= janela
                       for tipo, idade in eventos)
        estornado = any(tipo == "ESTORNADO" and idade <= janela
                        for tipo, idade in eventos)
        if recentes and (negativo or estornado):
            classe, motivo, score = "INDETERMINADO", "SINAIS_CONFLITANTES", None
        elif not cobertura:
            classe, motivo, score = "INDETERMINADO", "COBERTURA_INCOMPLETA", None
        elif recentes:
            idade = min(recentes)
            forca = (pesos["proximidade_temporal"] * (1 - idade / (janela + 1))
                     + pesos["cobertura_confirmada"])
            classe, motivo, score = "TRUE", "CONTATO_RECENTE_CONFIRMADO", round(100 * forca)
        elif negativo and not estornado:
            classe, motivo, score = "FALSE", "AUSENCIA_EXPLICITAMENTE_VERIFICADA", 0
        elif estornado:
            classe, motivo, score = "INDETERMINADO", "CONTATO_ESTORNADO", None
        elif any(tipo == "CONFIRMADO" for tipo, _ in eventos):
            classe, motivo, score = "INDETERMINADO", "SOMENTE_CONTATO_ANTIGO", None
        else:
            classe, motivo, score = "INDETERMINADO", "AUSENCIA_NAO_E_FALSE", None
        linhas.append({"id_entidade": pessoa, "classificacao": classe, "score": score,
                      "motivo": motivo, "cobertura_completa": cobertura})
    contagens = {nome: sum(linha["classificacao"] == nome for linha in linhas)
                 for nome in ("TRUE", "FALSE", "INDETERMINADO")}
    scores = [linha["score"] for linha in linhas if linha["score"] is not None]
    return {"ambiente": dados["ambiente"], "micromodelo": modelo["identidade"]["nome"],
            "assinatura_especificacao": assinatura.calculate_spec_fingerprint(modelo, contrato).sha256,
            "data_referencia": dados["data_referencia"], "janela_dias": janela,
            "resultado": linhas,
            "resumo": {"populacao": len(linhas), "contagens": contagens,
                       "scores_emitidos": len(scores)},
            "limites": {"validacao_humana": "PENDENTE", "mlflow": "NOT_RUN",
                        "publicacao": "NAO_INICIADA"}}


def main() -> int:
    """Imprime o resultado e, opcionalmente, confere o oráculo versionado."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conferir", action="store_true", help="compara com resultado_esperado.json")
    argumentos = parser.parse_args()
    resultado = executar()
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if argumentos.conferir:
        esperado = json.loads((PASTA / "resultado_esperado.json").read_text(encoding="utf-8"))
        if resultado != esperado:
            raise ExemploInvalido("Resultado diverge de resultado_esperado.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
