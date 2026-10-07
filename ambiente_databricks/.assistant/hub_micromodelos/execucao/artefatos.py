"""MM06: artefatos de estudo de laboratório derivados de micromodelo.yaml.

O gerador é puro: valida a especificação MM01, calcula o fingerprint MM02 e
devolve textos. Não lê dados, inicia runs, publica ou grava arquivos.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Any

from . import assinatura as mm02


RUN_POLICY_VERSION = "mm06-run-policy-v1"
RUN_TYPES = ("DEVELOPMENT", "VALIDATION", "SCORING")


@dataclass(frozen=True)
class StudyArtifacts:
    notebook_source: str
    readme_markdown: str
    spec_fingerprint: str
    fingerprint_algorithm: str


def _display(value: Any) -> str:
    """Mostra texto da spec em Markdown sem criar células ou markup ativo."""
    if value is None:
        return "PENDENTE"
    normalized = " ".join(str(value).split())
    normalized = "".join(c for c in normalized if c.isprintable())
    normalized = html.escape(normalized, quote=True)
    return re.sub(r"([\\`*\[\]()])", r"\\\1", normalized)


def _items(items: list[dict[str, Any]], *, description: str) -> list[str]:
    if not items:
        return ["- PENDENTE: nenhum item especificado."]
    lines = []
    for item in sorted(items, key=lambda entry: entry["id"]):
        provenance = item.get("proveniencia", {}).get("status", "NÃO DECLARADO")
        lines.append(
            f"- {_display(item['id'])} [{_display(provenance)}]: "
            f"{_display(item[description])}"
        )
    return lines


def _sections(spec: dict[str, Any], fingerprint: str, algorithm: str) -> list[tuple[str, list[str]]]:
    identity = spec["identidade"]
    state = identity["estado"]
    business = spec["negocio"]
    entity = spec["entidade"]
    classification = spec["classificacao"]
    score = spec["score"]
    output = spec["saida"]
    validation = spec["validacao"]
    publication = spec["publicacao"]
    sources = [
        f"- {_display(source['id'])} [{_display(source['proveniencia']['status'])}]: "
        f"{_display(source['catalogo_ref'])}.{_display(source['schema'])}."
        f"{_display(source['objeto'])}; campos: "
        + ", ".join(_display(field) for field in source["campos"])
        for source in sorted(spec["fontes"], key=lambda item: item["id"])
    ] or ["- PENDENTE: nenhuma fonte selecionada."]
    thresholds = [
        f"- {_display(item['id'])} [{_display(item['proveniencia']['status'])}]: "
        f"{_display(item['descricao'])}; {_display(item['operador'])} "
        f"{_display(item['valor'])} {_display(item['unidade'])}."
        for item in sorted(classification["limiares"], key=lambda entry: entry["id"])
    ] or ["- PENDENTE: nenhum limiar declarado."]
    components = [
        f"- {_display(item['id'])} [{_display(item['proveniencia']['status'])}]: "
        f"peso {_display(item['peso'])}; {_display(item['descricao'])}."
        for item in sorted(score["componentes"], key=lambda entry: entry["id"])
    ] or ["- PENDENTE: nenhum componente declarado."]
    experiments = []
    for item in sorted(spec["experimentos"], key=lambda entry: entry["id"]):
        experiments.append(
            f"- {_display(item['id'])} [{_display(item['status'])}; "
            f"{_display(item['proveniencia']['status'])}]: {_display(item['hipotese'])}. "
            f"Resultado declarado na spec: {_display(item['resultado'])}."
        )
    if not experiments:
        experiments = ["- PENDENTE: nenhum experimento declarado."]
    criteria = [f"- {_display(item)}" for item in validation["criterios"]]
    if not criteria:
        criteria = ["- PENDENTE: nenhum critério declarado."]
    observed_result = validation["resultado"]
    result_summary = (
        "- Resultado declarado na spec: PENDENTE."
        if observed_result is None else
        f"- Resultado declarado na spec [{_display(observed_result['proveniencia']['status'])}]: "
        f"{_display(observed_result['resumo'])}; referência de execução: "
        f"{_display((observed_result['proveniencia']['medicao'] or {}).get('referencia_execucao'))}."
    )
    limitations = [f"- {_display(item)}" for item in business["nao_usar_para"]]
    limitations.append("- O gerador não prova cobertura, execução, aprovação ou publicação.")
    sections = [
        ("0. Identificação e estado", [
            f"- Micromodelo: {_display(identity['nome'])}; versão: {_display(identity['micromodel_version'])}.",
            f"- Fase declarada: {_display(state['fase_atual'])}; condição: {_display(state['condicao'])}.",
            f"- Motivo da condição: {_display(state['motivo_condicao'])}.",
            f"- Fingerprint material ({algorithm}): {fingerprint}.",
            "- Estado desta geração: NOT_RUN. O fingerprint identifica a especificação, não uma execução.",
        ]),
        ("1. Problema de negócio", [
            f"- Característica: {_display(business['caracteristica'])}.",
            f"- Objetivo: {_display(business['objetivo'])}.",
            "- Usos pretendidos: " + "; ".join(_display(item) for item in business["uso_pretendido"]),
        ]),
        ("2. Definição operacional", [f"- {_display(business['definicao_operacional'])}"]),
        ("3. Contrato analítico", [
            f"- Entidade: {_display(entity['tipo'])}; chave lógica: {_display(entity['chave_logica'])}.",
            f"- Grão: {_display(entity['granularidade'])}.",
            f"- População elegível: {_display(entity['populacao_elegivel'])}.",
            f"- Referência temporal: {_display(entity['referencia_temporal'])}.",
        ]),
        ("4. Descoberta e seleção de fontes", sources + [
            "- Fontes declaradas não demonstram SELECT autorizado nem cobertura completa do catálogo."
        ]),
        ("5. Qualidade e cobertura", [
            "- PENDENTE: medir qualidade, disponibilidade temporal e cobertura somente sobre dados sintéticos autorizados.",
            "- Metadata parcial deve permanecer identificada como ESCOPO_OBSERVADO."
        ]),
        ("6. Evidências", _items(spec["evidencias"], description="regra")),
        ("7. Contra-evidências e falsos positivos", _items(spec["contra_evidencias"], description="regra")),
        ("8. Classificação", [
            f"- TRUE: {_display(classification['semantica']['quando_true'])}.",
            f"- FALSE: {_display(classification['semantica']['quando_false'])}.",
            f"- INDETERMINADO: {_display(classification['semantica']['quando_indeterminado'])}.",
            f"- Sem evidência: {_display(classification['ausencia_evidencia']['resultado_sem_evidencia'])} "
            f"({ _display(classification['ausencia_evidencia']['tratamento']) }).",
        ] + ["- Limiares declarados na spec:"] + thresholds),
        ("9. Score", [
            f"- Habilitado: {'sim' if score['habilitado'] else 'não'}; semântica: {_display(score['tipo_semantica'])}.",
            "- Score 0–100 não equivale a probabilidade sem calibração apropriada.",
            f"- Normalização declarada: {_display(score['normalizacao']['metodo']) if score['normalizacao'] else 'PENDENTE'}.",
        ] + ["- Componentes declarados na spec:"] + components),
        ("10. Experimentos", experiments + [
            "- Resultados são medidos somente depois de execução efetiva e referência de run."
        ]),
        ("11. Validação", [
            f"- Status declarado na spec: {_display(validation['status'])}.",
            "- Critérios declarados na spec:",
        ] + criteria + [
            result_summary,
            f"- Aprovação humana declarada na spec: {_display(validation['aprovacao_humana']['status'])}; "
            f"referência: {_display(validation['aprovacao_humana']['referencia'])}. "
            "Este gerador não autentica a decisão.",
            "- Uma run VALIDATION não substitui decisão humana. Este notebook não executou validação."
        ]),
        ("12. Resultados", [
            "- NOT_RUN neste notebook gerado: nenhuma contagem, percentual ou estatística foi medida.",
            "- Ao executar, reconciliar TRUE + FALSE + INDETERMINADO com a população elegível sintética."
        ]),
        ("13. Limitações", limitations),
        ("14. Contrato de saída", [
            "- Estudo: " + ", ".join(_display(item) for item in output["estudo"]["valores_classificacao"]),
            f"- Campo de classificação: {_display(output['estudo']['campo_classificacao'])}.",
            f"- Publicação: {_display(output['publicacao']['estado'])}; INDETERMINADO não vira FALSE por padrão."
        ]),
        ("15. Tracking", [
            f"- Política: {RUN_POLICY_VERSION}; backend previsto: MLflow; geração atual: NOT_RUN.",
            "- DEVELOPMENT: comparar hipóteses/configurações; registrar fingerprint, versão, dataset/corte sintético, parâmetros, limitações e métricas somente quando medidas.",
            "- VALIDATION: registrar critérios, agregados observados e referência de execução; aprovação humana permanece separada.",
            "- SCORING: somente após autorização de ambiente e governança externa; registrar agregados, nunca resultados individuais em artifacts MLflow.",
            "- Para regras sem modelo sklearn, use hub_snippets.ml.mlflow_run.run_micromodelo com contrato de saída, parâmetros e agregados medidos. Esta geração não abriu run. O run_governado legado mantém seu requisito de assinatura/modelo; não usar exigir_completo=False como comprovação de run completa."
        ]),
        ("16. Decisão de publicação", [
            f"- Status declarado: {_display(publication['status'])}; autoridade: {_display(publication['autoridade'])}.",
            "- Handoff é preparação para governança externa; este artefato não publica nem concede acesso."
        ]),
        ("17. Resumo executivo", [
            f"- {_display(identity['titulo'])}: especificação {_display(identity['estado']['fase_atual'])}.",
            "- Próximo passo: estudo sintético e revisão das lacunas antes de afirmar resultado medido."
        ]),
    ]
    return sections


def render_artifacts(spec: dict[str, Any], schema: dict[str, Any]) -> StudyArtifacts:
    """Valida MM01 e devolve notebook Databricks .py + README de domínio.

    A entrada deve ser sintética no E0. O gerador não consegue provar a origem dos
    valores recebidos e não acessa catálogo ou backend de tracking.
    """
    fingerprint = mm02.calculate_spec_fingerprint(spec, schema)
    sections = _sections(spec, fingerprint.sha256, fingerprint.algorithm)
    state = spec["identidade"]["estado"]
    code = [
        "# Databricks notebook source",
        "# Scaffold de estudo derivado de micromodelo.yaml (MM01); NOT_RUN.",
        "# A execução sintética pertence ao entrypoint do piloto; este arquivo não executa dados ou MLflow.",
        "ARTIFACT_KIND = 'STUDY_SCAFFOLD'",
        f"MICROMODEL_ID = {spec['identidade']['nome']!r}",
        f"MICROMODEL_VERSION = {spec['identidade']['micromodel_version']!r}",
        f"SPEC_FINGERPRINT = {fingerprint.sha256!r}",
        f"FINGERPRINT_ALGORITHM = {fingerprint.algorithm!r}",
        f"RUN_POLICY_VERSION = {RUN_POLICY_VERSION!r}",
        f"RUN_TYPES = {RUN_TYPES!r}",
        "GENERATION_EXECUTION_STATUS = 'NOT_RUN'",
    ]
    for title, lines in sections:
        code.extend(["", "# COMMAND ----------", "# MAGIC %md", f"# MAGIC ## {title}"])
        code.extend(f"# MAGIC {line}" for line in lines)
    notebook = "\n".join(code) + "\n"
    readme = [
        f"# {_display(spec['identidade']['titulo'])}",
        "",
        "Scaffold de domínio NOT_RUN derivado de micromodelo.yaml validado. Entrada E0 deve ser sintética; origem sintética não é verificada por este gerador.",
        "",
        f"**Identidade:** {_display(spec['identidade']['nome'])} v{_display(spec['identidade']['micromodel_version'])}.",
        f"**Fase/condição declaradas:** {_display(state['fase_atual'])} / {_display(state['condicao'])}.",
        f"**Motivo da condição:** {_display(state['motivo_condicao'])}.",
        f"**Fingerprint material:** {fingerprint.sha256} ({fingerprint.algorithm}).",
        "**Execução desta geração:** NOT_RUN. Fingerprint não prova execução, aprovação ou publicação.",
        "",
    ]
    for title, lines in sections[1:]:
        readme.extend([f"## {title}", "", *lines, ""])
    return StudyArtifacts(notebook, "\n".join(readme), fingerprint.sha256, fingerprint.algorithm)
