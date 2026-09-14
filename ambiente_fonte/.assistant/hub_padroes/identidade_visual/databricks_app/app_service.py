"""Serviço V10 do App de gestão visual, sem aprovação ou publicação.

A camada reaproveita o Visual Lab V05 e nunca aceita identidade ou papel vindos
do tema. Em Databricks Apps, a identidade do usuário vem dos headers encaminhados
pelo proxy. A persistência usa uma raiz fornecida como recurso de UC Volume.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from hub_snippets.visual.theme_lab import (
    ThemeLabDraft,
    ThemeLabError,
    ThemeLabSessionInfo,
    ThemeLabSessionReceipt,
    list_theme_lab_sessions,
    reopen_theme_lab_session,
    save_theme_lab_session,
)


class ThemeAppError(ValueError):
    """Erro operacional V10 sem promover falha a sucesso silencioso."""

    def __init__(self, code: str, message: str, *, action: str):
        self.code = code
        self.action = action
        super().__init__(f"{code}: {message} {action}")


@dataclass(frozen=True)
class ThemeAppUser:
    """Identidade em memória; o identificador bruto não é usado como caminho."""

    subject: str
    display_name: str
    namespace: str
    source: str


@dataclass(frozen=True)
class ThemeAppConfig:
    """Configuração validada do App V10."""

    storage_root: Path
    local_dev: bool
    app_mode: str = "authoring_only"
    retention: str = "no_automatic_delete"


_HEADER_USER = "x-forwarded-user"
_HEADER_PREFERRED = "x-forwarded-preferred-username"
_LOCAL_FLAG = "HUB_THEME_LOCAL_DEV"
_LOCAL_USER = "HUB_THEME_LOCAL_USER_ID"
_VOLUME_ENV = "HUB_THEME_VOLUME"
_MODE_ENV = "HUB_THEME_APP_MODE"
_ALLOWED_MODE = "authoring_only"
_STORAGE_DIR = "hub-theme-manager-v10"


def _true(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def resolve_user(headers: Mapping[str, str] | None, *, env: Mapping[str, str] | None = None) -> ThemeAppUser:
    """Resolve identidade encaminhada pelo Databricks; fallback local exige opt-in."""
    env = os.environ if env is None else env
    normalized = {str(key).lower(): str(value) for key, value in (headers or {}).items()}
    subject = normalized.get(_HEADER_USER, "").strip()
    preferred = normalized.get(_HEADER_PREFERRED, "").strip()
    source = "databricks_forwarded_header"
    if not subject:
        if not _true(env.get(_LOCAL_FLAG)):
            raise ThemeAppError(
                "APP_IDENTITY_MISSING",
                "O App não recebeu identidade confiável do proxy Databricks.",
                action="Execute dentro de Databricks Apps ou habilite explicitamente o modo local de desenvolvimento.",
            )
        subject = str(env.get(_LOCAL_USER, "")).strip()
        preferred = preferred or subject
        source = "explicit_local_dev"
        if not subject:
            raise ThemeAppError(
                "APP_LOCAL_USER_MISSING",
                "O modo local foi habilitado sem usuário sintético.",
                action="Defina HUB_THEME_LOCAL_USER_ID somente no ambiente local de desenvolvimento.",
            )
    if len(subject.encode("utf-8")) > 1024 or len(preferred.encode("utf-8")) > 1024:
        raise ThemeAppError(
            "APP_IDENTITY_SIZE",
            "A identidade recebida excede o limite defensivo.",
            action="Não persista a sessão e verifique o proxy ou o ambiente local.",
        )
    namespace = hashlib.sha256(subject.encode("utf-8")).hexdigest()
    return ThemeAppUser(subject=subject, display_name=preferred or "usuário autenticado", namespace=namespace, source=source)


def load_config(*, env: Mapping[str, str] | None = None) -> ThemeAppConfig:
    """Carrega somente configuração estática; recusa storage não governado em produção."""
    env = os.environ if env is None else env
    local_dev = _true(env.get(_LOCAL_FLAG))
    mode = str(env.get(_MODE_ENV, _ALLOWED_MODE)).strip()
    if mode != _ALLOWED_MODE:
        raise ThemeAppError(
            "APP_MODE_UNSUPPORTED",
            "O modo solicitado não pertence à V10.",
            action="Use authoring_only; aprovação e publicação não são implementadas por este App.",
        )
    raw_root = str(env.get(_VOLUME_ENV, "")).strip()
    if not raw_root:
        raise ThemeAppError(
            "APP_STORAGE_MISSING",
            "A persistência do App não foi configurada.",
            action="Associe um Unity Catalog Volume ao recurso theme_storage antes de usar o App.",
        )
    root = Path(raw_root).absolute()
    if not local_dev and not root.as_posix().startswith("/Volumes/"):
        raise ThemeAppError(
            "APP_STORAGE_NOT_VOLUME",
            "Em produção, a raiz precisa ser um Unity Catalog Volume.",
            action="Configure o recurso theme_storage; não use DBFS, /tmp ou caminho pessoal.",
        )
    if not root.is_dir() or root.is_symlink():
        raise ThemeAppError(
            "APP_STORAGE_UNAVAILABLE",
            "A raiz persistente não está disponível como diretório regular.",
            action="Verifique o recurso do App e a permissão de leitura/gravação do service principal.",
        )
    return ThemeAppConfig(storage_root=root, local_dev=local_dev, app_mode=mode)


def _user_root(config: ThemeAppConfig, user: ThemeAppUser, *, create: bool) -> Path | None:
    """Calcula namespace próprio sem incorporar identificador bruto do usuário."""
    if type(config) is not ThemeAppConfig or type(user) is not ThemeAppUser:
        raise ThemeAppError("APP_ARGUMENT", "Configuração ou identidade inválida.", action="Reconstrua o contexto do App.")
    root = config.storage_root / _STORAGE_DIR / "sessions" / user.namespace
    try:
        if create:
            root.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not root.exists():
            return None
        if not root.is_dir() or root.is_symlink():
            raise OSError
        return root
    except OSError:
        raise ThemeAppError(
            "APP_STORAGE_NAMESPACE",
            "O namespace persistente do usuário não pôde ser preparado.",
            action="Não considere a sessão salva; verifique Volume e permissões do App.",
        ) from None


def save_own_session(
    draft: ThemeLabDraft,
    config: ThemeAppConfig,
    user: ThemeAppUser,
    session_name: str,
) -> ThemeLabSessionReceipt:
    """Persiste somente a sessão do usuário autenticado; nunca aprova ou publica."""
    root = _user_root(config, user, create=True)
    assert root is not None
    try:
        return save_theme_lab_session(draft, root, session_name)
    except ThemeLabError:
        raise


def list_own_sessions(config: ThemeAppConfig, user: ThemeAppUser) -> tuple[ThemeLabSessionInfo, ...]:
    """Lista apenas o namespace derivado da identidade corrente."""
    root = _user_root(config, user, create=False)
    if root is None:
        return ()
    return list_theme_lab_sessions(root)


def reopen_own_session(
    config: ThemeAppConfig,
    user: ThemeAppUser,
    session_name: str,
) -> ThemeLabDraft:
    """Reabre somente sessão do namespace atual, preservando validações V05."""
    root = _user_root(config, user, create=False)
    if root is None:
        raise ThemeAppError(
            "APP_SESSION_ROOT_MISSING",
            "O usuário ainda não possui sessões persistidas.",
            action="Crie uma sessão própria antes de tentar reabrir.",
        )
    return reopen_theme_lab_session(root, session_name)


def retention_policy() -> dict[str, str | bool]:
    """Política V10: nenhum apagamento automático ou pelo usuário final."""
    return {
        "automatic_delete": False,
        "user_delete_action": False,
        "history_rewrite": False,
        "policy": "no_automatic_delete",
        "cleanup_owner": "administrador_do_destino_autorizado",
    }


def publication_policy() -> dict[str, str | bool]:
    """Torna verificável que a V10 não possui caminho técnico de publicação."""
    return {
        "approve_implemented": False,
        "publish_implemented": False,
        "promote_implemented": False,
        "scope": "authoring_and_persistence_only",
        "next_gate": "processo_governado_separado_com_identidade_papeis_e_guardas_reais",
    }
