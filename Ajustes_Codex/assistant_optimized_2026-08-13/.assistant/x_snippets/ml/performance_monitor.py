"""Track model metrics against an explicit, calibrated monitoring policy."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Dict, List, Optional


AZUL_CAIXA = "#005CA9"
LARANJA = "#F7941D"
VERMELHO = "#C4262E"

# Example policy for backward compatibility. It is not a Databricks default and
# must be reviewed for the model, metric scale, sample size, and business risk.
EXAMPLE_THRESHOLDS = {
    "auc": {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"},
    "ks": {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"},
    "gini": {"warning": 0.05, "critical": 0.08, "direction": "higher", "delta": "absolute"},
    "rmse": {"warning": 0.10, "critical": 0.20, "direction": "lower", "delta": "relative"},
    "mape": {"warning": 0.10, "critical": 0.20, "direction": "lower", "delta": "relative"},
    "ndcg_at_10": {"warning": 0.05, "critical": 0.10, "direction": "higher", "delta": "absolute"},
    "c_index": {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"},
}


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
        if consecutive_alert_periods <= 0:
            raise ValueError("consecutive_alert_periods must be positive")
        if any(not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in baseline_metrics.values()):
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
            if not 0 <= rule["warning"] < rule["critical"]:
                raise ValueError(f"invalid warning/critical thresholds for {metric}")
            if not math.isfinite(float(rule["warning"])) or not math.isfinite(float(rule["critical"])):
                raise ValueError(f"thresholds must be finite for {metric}")
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
        if n_predictions < 0:
            raise ValueError("n_predictions cannot be negative")
        unknown = set(metrics) - set(self.baseline)
        if unknown:
            raise ValueError(f"metrics missing from the baseline/policy: {sorted(unknown)}")
        missing = set(self.baseline) - set(metrics)
        if self.require_complete_metrics and missing:
            raise ValueError(f"period is missing monitored metrics: {sorted(missing)}")
        if not metrics:
            raise ValueError("metrics cannot be empty")
        if any(not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in metrics.values()):
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
