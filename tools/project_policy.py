"""Políticas compartilhadas pelas ferramentas locais do projeto.

As constantes aqui são invariantes operacionais. Mantê-las em um único módulo
evita que validador, renderer e publicador aceitem identidades ou inventários
diferentes.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit


EXPECTED_SKILL_NAMES = frozenset(
    {
        "hub-ml-analise-safra",
        "hub-ml-auditoria-skills",
        "hub-ml-baseline-ml",
        "hub-ml-comentar-notebook",
        "hub-ml-concierge",
        "hub-ml-criar-objeto",
        "hub-ml-cross-eda-ml",
        "hub-ml-eda-profissional",
        "hub-ml-explainability",
        "hub-ml-feature-engineering",
        "hub-ml-monitoramento-modelo",
        "hub-ml-pipeline-builder",
        "hub-ml-tutor-databricks",
        "hub-ml-validacao-estatistica",
    }
)

# Nomes antigos pertencentes a este projeto. Servem somente para a limpeza
# seletiva no runbook; nunca autorizam apagar a pasta `skills/` inteira.
LEGACY_MANAGED_SKILL_NAMES = frozenset(
    {
        "rodrigo-analise-safra",
        "rodrigo-auditoria-skills",
        "rodrigo-baseline-ml",
        "rodrigo-comentar-notebook",
        "rodrigo-cross-eda-ml",
        "rodrigo-eda-profissional",
        "rodrigo-explainability",
        "rodrigo-feature-engineering",
        "rodrigo-monitoramento-modelo",
        "rodrigo-pipeline-builder",
        "rodrigo-tutor-databricks",
        "rodrigo-validacao-estatistica",
    }
)

EXPECTED_HUB_DIRS = frozenset(
    {
        "hub_padroes",
        "hub_prompts",
        "hub_readmes_visual_assets",
        "hub_scripts",
        "hub_snippets",
    }
)

CORPORATE_RE = re.compile(
    r"\b[a-z]\d{6,8}\b"
    r"|corp(?:orativ)?[.@]"
    r"|\.gov\.br"
    r"|@[a-z0-9-]*(?:banco|caixa|bank)[a-z0-9-]*\."
    r"|(?<![A-Za-z0-9])GE[G]OD(?![A-Za-z0-9])",
    re.IGNORECASE,
)

# Padrões pessoais legados que não podem reaparecer em conteúdo ativo. As partes
# são concatenadas para o próprio arquivo de política não casar consigo mesmo.
PERSONAL_RE = re.compile(
    r"(?<![A-Za-z0-9])c\d{6}(?![A-Za-z0-9])"
    r"|corp\.caixa|caixa\.gov\.br|guimarais[._-]?r?[._-]?"
    + r"rodrigo@|C:\\Users\\"
    + r"Rodrigo"
    + r"|/Users/"
    + r"rodri\b",
    re.IGNORECASE,
)

SAFE_SIMULATED_USERNAME = "usuario-free"


def validate_username_component(username: str) -> str:
    """Valida um único componente de path usado no simulado."""
    value = username.strip()
    if not value or value in {".", ".."}:
        raise ValueError("username deve ser um componente de path não vazio")
    if Path(value).name != value or any(sep in value for sep in ("/", "\\")):
        raise ValueError("username não pode conter separadores nem navegação de path")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) or len(value) > 64:
        raise ValueError("username do simulado deve ser um placeholder neutro em kebab-case")
    if CORPORATE_RE.search(value):
        raise ValueError("username com aparência corporativa recusado (ADR-0003)")
    return value


def normalize_host(host: str) -> str:
    """Normaliza host da CLI para comparação explícita, sem aceitar subpaths."""
    value = host.strip()
    if not value:
        raise ValueError("host esperado não pode ser vazio")
    parsed = urlsplit(value if "://" in value else f"https://{value}")
    if parsed.scheme != "https" or not parsed.hostname or parsed.path not in {"", "/"}:
        raise ValueError("host deve ser uma origem HTTPS sem path")
    return f"https://{parsed.hostname.lower()}"
