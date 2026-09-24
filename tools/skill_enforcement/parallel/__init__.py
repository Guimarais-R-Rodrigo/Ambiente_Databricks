"""Infraestrutura local declarativa para execução paralela governada da SER."""
from .contract import (
    CAMPAIGN_SCHEMA_VERSION,
    digest_json,
    validate_campaign,
    validate_result,
    validate_task,
)

__all__ = [
    "CAMPAIGN_SCHEMA_VERSION",
    "digest_json",
    "validate_campaign",
    "validate_result",
    "validate_task",
]
