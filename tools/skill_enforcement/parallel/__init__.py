"""Infraestrutura declarativa e fail-closed para campanhas paralelas da SER."""
from .contract import (
    CAMPAIGN_SCHEMA_VERSION, TASK_SCHEMA_VERSION, RESULT_SCHEMA_VERSION,
    digest_json, validate_campaign, validate_result, validate_task,
)

__all__ = [
    "CAMPAIGN_SCHEMA_VERSION", "TASK_SCHEMA_VERSION", "RESULT_SCHEMA_VERSION",
    "digest_json", "validate_campaign", "validate_result", "validate_task",
]
