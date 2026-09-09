"""Acompanha métricas do modelo contra uma política de monitoramento explícita.

Migração de chave: o relatório antigo já devolvia ``ks`` em pontos percentuais
(0–100). A migração preservou esses valores, renomeou a chave para ``ks_pct``
e corrigiu os limiares do monitor para pontos percentuais. Não multiplique nem
divida o KS antigo por 100: um KS de 40 continua sendo 40.

Os dois vocabulários ainda não coincidem em tudo: o relatório devolve ``auc_roc``
e a política de exemplo fala em ``auc``. Passar o dicionário inteiro do relatório
ao monitor **falha alto**, com ``policy is missing monitored metrics`` — o
relatório traz accuracy, precision, recall e outras que não têm limiar. O risco
silencioso está no contorno óbvio: selecionar à mão só as chaves cujo nome já
coincide com a política deixa a AUC de fora, porque ela se chama ``auc_roc``, e o
monitoramento passa a rodar sem a métrica principal sem nunca reclamar.
``selecionar_metricas_do_relatorio`` faz a seleção e a tradução no mesmo passo.
"""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Dict, List, Optional


from hub_snippets.constants import colors

# Derivado, nao redeclarado: o valor tem uma fonte so. A forma e atribuicao
# porque `api_publica.py` nao reexporta nome importado, e estes tres fazem
# parte da API publica deste modulo desde a Sprint 7.
AZUL_CAIXA = colors.AZUL_CAIXA
LARANJA = colors.LARANJA
VERMELHO = colors.VERMELHO

# Example policy for backward compatibility. It is not a Databricks default and
# must be reviewed for the model, metric scale, sample size, and business risk.
EXAMPLE_THRESHOLDS = {
    "auc": {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"},
    "ks_pct": {"warning": 3.0, "critical": 5.0, "direction": "higher", "delta": "absolute"},
    "gini": {"warning": 0.05, "critical": 0.08, "direction": "higher", "delta": "absolute"},
    "rmse": {"warning": 0.10, "critical": 0.20, "direction": "lower", "delta": "relative"},
    "mape": {"warning": 0.10, "critical": 0.20, "direction": "lower", "delta": "relative"},
    "ndcg_at_10": {"warning": 0.05, "critical": 0.10, "direction": "higher", "delta": "absolute"},
    "c_index": {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"},
}


# Vocabulário do relatório -> vocabulário da política. Explícito de propósito:
# uma conversão por heurística de nome erraria em silêncio, que é exatamente o
# defeito que este mapa existe para impedir.
CHAVES_DO_RELATORIO = {
    "auc_roc": "auc",
    "ks_pct": "ks_pct",
    "gini": "gini",
    "rmse": "rmse",
    "mape": "mape",
}


def _is_finite_number(value: object) -> bool:
    """Aceite números reais finitos, mas nunca booleanos disfarçados de 0/1."""
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(float(value))


def selecionar_metricas_do_relatorio(
    relatorio: Dict[str, Any],
    politica: Optional[Dict[str, Any]] = None,
    *,
    metricas_obrigatorias: Optional[List[str]] = None,
) -> Dict[str, float]:
    """Traduza a saída de ``metrics_report`` para o vocabulário da política.

    Args:
        relatorio: dicionário devolvido por ``calculate_binary_metrics`` ou
            ``calculate_regression_metrics``.
        politica: política de limiares; ``EXAMPLE_THRESHOLDS`` por padrão.
        metricas_obrigatorias: nomes da política exigidos pela tarefa, por
            exemplo ['auc', 'ks_pct']; não exige todas as métricas da política
            genérica. Para excluir uma métrica, retire-a explicitamente da política.

    Returns:
        Somente as métricas presentes na política, já com a chave dela e com
        valor numérico finito. Métrica sem política é descartada de propósito:
        limiar ausente não é limiar zero.

    Raises:
        ValueError: métrica selecionada inválida, alias conflitante, obrigação
            ausente ou nenhuma métrica do relatório pertencente à política. Devolver
            um dicionário vazio faria o monitor aceitar um período sem medir
            nada, que é pior do que falhar.
    """
    alvo = EXAMPLE_THRESHOLDS if politica is None else politica
    selecionadas: Dict[str, float] = {}
    for chave_relatorio, valor in relatorio.items():
        chave_politica = CHAVES_DO_RELATORIO.get(chave_relatorio, chave_relatorio)
        if chave_politica not in alvo:
            continue
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not math.isfinite(float(valor)):
            raise ValueError(f"métrica selecionada inválida: {chave_relatorio}")
        if chave_politica in selecionadas and selecionadas[chave_politica] != float(valor):
            raise ValueError(f"aliases conflitantes para a métrica {chave_politica}")
        selecionadas[chave_politica] = float(valor)
    obrigatorias = set(metricas_obrigatorias or [])
    if obrigatorias - set(alvo):
        raise ValueError(f"métricas obrigatórias sem política: {sorted(obrigatorias - set(alvo))}")
    if obrigatorias - set(selecionadas):
        raise ValueError(f"métricas obrigatórias ausentes: {sorted(obrigatorias - set(selecionadas))}")
    if not selecionadas:
        raise ValueError(
            "nenhuma métrica do relatório pertence à política: "
            f"relatório={sorted(relatorio)}, política={sorted(alvo)}"
        )
    return selecionadas


class PerformanceMonitor:
    """Store periodic metric evidence and flag investigation candidates.

    This class never authorizes retraining or deployment. ``should_retrain`` is kept
    as a compatibility name but returns a governance recommendation requiring root
    cause analysis, offline validation, and approval.
    """

    THRESHOLDS = EXAMPLE_THRESHOLDS

    def __init__(
        self,
        baseline_metrics: Dict[str, float],
        model_name: str = "model",
        *,
        policy: Optional[Dict[str, Dict[str, Any]]] = None,
        consecutive_alert_periods: int = 3,
        require_complete_metrics: bool = True,
    ) -> None:
        if not baseline_metrics:
            raise ValueError("baseline_metrics cannot be empty")
        if (
            isinstance(consecutive_alert_periods, bool)
            or not isinstance(consecutive_alert_periods, int)
            or consecutive_alert_periods <= 0
        ):
            raise ValueError("consecutive_alert_periods must be positive")
        if not isinstance(require_complete_metrics, bool):
            raise ValueError("require_complete_metrics must be boolean")
        if any(not _is_finite_number(value) for value in baseline_metrics.values()):
            raise ValueError("baseline metrics must be finite numeric values")
        self.baseline = {metric: float(value) for metric, value in baseline_metrics.items()}
        self.model_name = model_name
        self.policy = deepcopy(policy if policy is not None else EXAMPLE_THRESHOLDS)
        self.using_example_policy = policy is None
        self.consecutive_alert_periods = consecutive_alert_periods
        self.require_complete_metrics = require_complete_metrics
        self.history: List[Dict[str, Any]] = []
        self._validate_policy()

    def _validate_policy(self) -> None:
        missing = set(self.baseline) - set(self.policy)
        if missing:
            raise ValueError(f"policy is missing monitored metrics: {sorted(missing)}")
        for metric, rule in self.policy.items():
            required = {"warning", "critical", "direction", "delta"}
            if not required <= set(rule):
                raise ValueError(f"policy for {metric} must contain {sorted(required)}")
            if not _is_finite_number(rule["warning"]) or not _is_finite_number(rule["critical"]):
                raise ValueError(f"thresholds must be finite numeric values for {metric}")
            if not 0 <= rule["warning"] < rule["critical"]:
                raise ValueError(f"invalid warning/critical thresholds for {metric}")
            if rule["direction"] not in {"higher", "lower"} or rule["delta"] not in {"absolute", "relative"}:
                raise ValueError(f"invalid direction/delta for {metric}")
            if rule["delta"] == "relative" and self.baseline.get(metric) == 0:
                raise ValueError(f"relative delta is undefined for zero baseline: {metric}")

    def _deterioration(self, metric: str, value: float) -> float:
        baseline = self.baseline[metric]
        rule = self.policy[metric]
        raw = baseline - value if rule["direction"] == "higher" else value - baseline
        return raw / abs(baseline) if rule["delta"] == "relative" else raw

    def add_period(self, period: str, metrics: Dict[str, float], n_predictions: int = 0) -> None:
        """Add one monitoring period and calculate one-sided deterioration."""
        if isinstance(n_predictions, bool) or not isinstance(n_predictions, int) or n_predictions < 0:
            raise ValueError("n_predictions must be a non-negative integer")
        unknown = set(metrics) - set(self.baseline)
        if unknown:
            raise ValueError(f"metrics missing from the baseline/policy: {sorted(unknown)}")
        missing = set(self.baseline) - set(metrics)
        if self.require_complete_metrics and missing:
            raise ValueError(f"period is missing monitored metrics: {sorted(missing)}")
        if not metrics:
            raise ValueError("metrics cannot be empty")
        if any(not _is_finite_number(value) for value in metrics.values()):
            raise ValueError("period metrics must be finite numeric values")
        entry: Dict[str, Any] = {"period": period, "n_predictions": n_predictions, **metrics}
        entry["missing_metrics"] = sorted(missing)
        for metric, value in metrics.items():
            deterioration = self._deterioration(metric, float(value))
            entry[f"{metric}_delta"] = deterioration
            rule = self.policy[metric]
            entry[f"{metric}_status"] = (
                "🔴" if deterioration >= rule["critical"] else "🟡" if deterioration >= rule["warning"] else "🟢"
            )
        self.history.append(entry)

    def get_current_status(self) -> str:
        if not self.history:
            return "⚪ Sem dados"
        latest = self.history[-1]
        if latest.get("missing_metrics"):
            return "⚪ Incompleto"
        statuses = [value for key, value in latest.items() if key.endswith("_status")]
        return "🔴 Crítico" if "🔴" in statuses else "🟡 Atenção" if "🟡" in statuses else "🟢 Saudável"

    def should_retrain(self) -> Dict[str, object]:
        """Return investigation/governance guidance, never an automatic retrain order."""
        if not self.history:
            return {"decision": "NO_EVIDENCE", "reason": "No monitoring periods were supplied."}
        latest = self.history[-1]
        critical = [metric for metric in self.baseline if latest.get(f"{metric}_status") == "🔴"]
        consecutive = 0
        for entry in reversed(self.history):
            statuses = [value for key, value in entry.items() if key.endswith("_status")]
            if "🟡" in statuses or "🔴" in statuses:
                consecutive += 1
            else:
                break
        candidate = bool(critical or consecutive >= self.consecutive_alert_periods)
        return {
            "decision": "INVESTIGATE_RETRAINING_CANDIDATE" if candidate else "NO_TRIGGER",
            "automatic_retrain_authorized": False,
            "critical_metrics": critical,
            "consecutive_alert_periods": consecutive,
            "required_next_steps": (
                ["validate data/label quality", "analyze drift/root cause", "run offline champion-challenger evaluation", "obtain model-governance approval"]
                if candidate else []
            ),
            "policy_source": "caller-provided" if not self.using_example_policy else "example-policy-requires-calibration",
        }

    def generate_report(self) -> str:
        status = self.get_current_status()
        recommendation = self.should_retrain()
        report = (
            f"## Monitoramento — {self.model_name}\n\n"
            f"**Status**: {status}\n"
            f"**Períodos monitorados**: {len(self.history)}\n"
            f"**Decisão**: {recommendation['decision']} (retreino automático: não autorizado)\n"
            f"**Política**: {recommendation.get('policy_source', 'n/a')}\n\n"
        )
        if self.history:
            latest = self.history[-1]
            report += "| Métrica | Baseline | Atual | Deterioração | Status |\n|---|---:|---:|---:|---|\n"
            for metric in self.baseline:
                if metric in latest:
                    report += f"| {metric} | {self.baseline[metric]:.4f} | {latest[metric]:.4f} | {latest[f'{metric}_delta']:+.4f} | {latest[f'{metric}_status']} |\n"
        return report

    def plot_timeline(self, metric: str) -> Any:
        """Plot the metric and policy thresholds; Plotly is imported lazily."""
        import plotly.graph_objects as go

        if metric not in self.baseline:
            raise ValueError(f"metric not monitored: {metric}")
        if not self.history:
            return go.Figure()
        periods = [item["period"] for item in self.history]
        values = [item.get(metric) for item in self.history]
        rule = self.policy[metric]
        baseline = self.baseline[metric]

        def boundary(amount: float) -> float:
            degradation = amount * abs(baseline) if rule["delta"] == "relative" else amount
            return baseline - degradation if rule["direction"] == "higher" else baseline + degradation

        fig = go.Figure(go.Scatter(x=periods, y=values, mode="lines+markers", name=metric, line={"color": AZUL_CAIXA}))
        fig.add_hline(y=baseline, line_dash="dash", annotation_text="Baseline")
        fig.add_hline(y=boundary(rule["warning"]), line_dash="dot", line_color=LARANJA, annotation_text="Warning policy")
        fig.add_hline(y=boundary(rule["critical"]), line_dash="dot", line_color=VERMELHO, annotation_text="Critical policy")
        fig.update_layout(template="plotly_white", title=f"{metric} ao longo do tempo", xaxis_title="Período", yaxis_title=metric)
        return fig
