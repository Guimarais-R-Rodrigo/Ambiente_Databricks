"""Fachada pública V11 para a ponte Databricks AI/BI.

A implementação detalhada permanece em ``_aibi_theme_impl``. Esta fachada mantém
a fronteira de contexto da V11 explícita antes de delegar ao núcleo V02, para que
entradas de outros contextos falhem com erro pertencente à própria ponte AI/BI.
"""
from __future__ import annotations

if __package__:
    from . import _aibi_theme_impl as _impl
else:
    import _aibi_theme_impl as _impl

AibiThemeError = _impl.AibiThemeError
AibiThemeProjection = _impl.AibiThemeProjection
AibiNativeCandidate = _impl.AibiNativeCandidate
export_projection = _impl.export_projection
bind_native_template = _impl.bind_native_template
workspace_theme_policy = _impl.workspace_theme_policy
dashboard_theme_policy = _impl.dashboard_theme_policy
authorize_local_operation = _impl.authorize_local_operation
synthetic_dashboard_semantic_fingerprint = _impl.synthetic_dashboard_semantic_fingerprint


def project_theme(theme):
    """Projeta somente ``ResolvedTheme`` do contexto notebook para AI/BI."""
    if type(theme) is not _impl.ResolvedTheme:
        raise AibiThemeError(
            "AIBI_THEME_TYPE",
            "Forneça um ResolvedTheme produzido pelo núcleo V02.",
        ) from None
    if theme.context != "notebook":
        raise AibiThemeError(
            "AIBI_THEME_INTEGRITY",
            "A ponte V11 aceita somente tema do contexto notebook.",
            action="Escolha uma configuração notebook íntegra; AI/BI continua como contexto reservado.",
        ) from None
    return _impl.project_theme(theme)


__all__ = [
    "AibiThemeError",
    "AibiThemeProjection",
    "AibiNativeCandidate",
    "project_theme",
    "export_projection",
    "bind_native_template",
    "workspace_theme_policy",
    "dashboard_theme_policy",
    "authorize_local_operation",
    "synthetic_dashboard_semantic_fingerprint",
]
