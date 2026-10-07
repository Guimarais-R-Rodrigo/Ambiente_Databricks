"""Databricks App V10 — gestão visual em modo de autoria, sem publicar temas."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _bootstrap_product_root() -> Path:
    here = Path(__file__).resolve()
    candidates = [here.parent, *here.parents]
    for candidate in candidates:
        if (candidate / "hub_snippets").is_dir() and (candidate / "hub_padroes").is_dir():
            value = str(candidate)
            if value not in sys.path:
                sys.path.insert(0, value)
            return candidate
    raise RuntimeError("Pacote do Hub ausente: hub_snippets/hub_padroes não encontrados.")


_BOOTSTRAP_ROOT = _bootstrap_product_root()

import streamlit as st

from app_service import (
    ThemeAppError,
    list_own_sessions,
    load_config,
    publication_policy,
    reopen_own_session,
    resolve_user,
    retention_policy,
    save_own_session,
)
from hub_snippets.visual.theme_lab import (
    ThemeLabError,
    compare_preview,
    create_theme_lab_from_preset,
    get_control_specs,
    get_demo_presets,
)


st.set_page_config(page_title="Hub — Gestão Visual", layout="wide")
st.title("Gestão Visual do Hub")
st.caption("V10 · autoria e persistência rastreável · sem aprovação ou publicação")

try:
    config = load_config(env=os.environ)
    headers = dict(getattr(st.context, "headers", {}) or {})
    user = resolve_user(headers, env=os.environ)
except ThemeAppError as exc:
    st.error(str(exc))
    st.stop()

st.info(
    "Este App não publica, promove ou aprova temas. O acesso ao App deve ser concedido "
    "pelo administrador somente ao público autorizado para autoria/manutenção."
)
st.caption(f"Sessão autenticada: {user.display_name} · identidade não é gravada no nome da pasta")

presets = get_demo_presets()
preset_labels = {item.key: f"{item.display_name} — demonstração" for item in presets}

if "v10_preset" not in st.session_state:
    st.session_state.v10_preset = presets[0].key
if "v10_draft" not in st.session_state:
    st.session_state.v10_draft = create_theme_lab_from_preset(presets, st.session_state.v10_preset)
if "v10_show_preview" not in st.session_state:
    st.session_state.v10_show_preview = True

with st.sidebar:
    st.header("Sessão")
    selected_preset = st.selectbox(
        "Ponto de partida",
        options=[item.key for item in presets],
        format_func=lambda key: preset_labels[key],
        index=[item.key for item in presets].index(st.session_state.v10_preset),
    )
    if st.button("Abrir novo rascunho", use_container_width=True):
        st.session_state.v10_preset = selected_preset
        st.session_state.v10_draft = create_theme_lab_from_preset(presets, selected_preset)
        st.rerun()

    sessions = list_own_sessions(config, user)
    st.divider()
    st.subheader("Retomar")
    if sessions:
        by_name = {item.session_name: item for item in sessions}
        session_name = st.selectbox("Sessão salva", options=list(by_name))
        if st.button("Reabrir sessão", use_container_width=True):
            try:
                st.session_state.v10_draft = reopen_own_session(config, user, session_name)
                st.rerun()
            except (ThemeAppError, ThemeLabError) as exc:
                st.error(str(exc))
    else:
        st.caption("Nenhuma sessão persistida para esta identidade.")


draft = st.session_state.v10_draft
specs = get_control_specs(draft.current)
primary = [spec for spec in specs if spec.primary]
advanced = [spec for spec in specs if not spec.primary]


def _render_control(spec, *, key_prefix: str):
    current = draft.current.tokens[spec.token]
    key = f"{key_prefix}:{spec.token}"
    disabled = not spec.preview_supported
    help_text = spec.description
    if disabled and spec.unavailable_reason:
        help_text += " " + spec.unavailable_reason
    if type(current) is int:
        kwargs = {"label": spec.label, "value": int(current), "key": key, "disabled": disabled, "help": help_text}
        if spec.minimum is not None:
            kwargs["min_value"] = int(spec.minimum)
        if spec.maximum is not None:
            kwargs["max_value"] = int(spec.maximum)
        return st.number_input(**kwargs)
    if isinstance(current, (tuple, list)):
        return st.text_input(spec.label, value=",".join(str(item) for item in current), key=key, disabled=disabled, help=help_text)
    return st.text_input(spec.label, value=str(current), key=key, disabled=disabled, help=help_text)


st.subheader("1. Ajustar proposta")
with st.form("v10-theme-controls", clear_on_submit=False):
    updates = {}
    for spec in primary:
        updates[spec.token] = _render_control(spec, key_prefix="primary")
    with st.expander("Controles avançados", expanded=False):
        for spec in advanced:
            updates[spec.token] = _render_control(spec, key_prefix="advanced")
    apply_clicked = st.form_submit_button("Aplicar e validar proposta", type="primary")

if apply_clicked:
    try:
        enabled = {spec.token for spec in specs if spec.preview_supported}
        draft.apply_updates({key: value for key, value in updates.items() if key in enabled})
        st.success("Proposta validada. O estado anterior permanece disponível no histórico.")
        st.session_state.v10_show_preview = True
    except Exception as exc:
        st.error(f"A proposta não foi aplicada. O último estado válido foi preservado. {exc}")

left, middle, right = st.columns(3)
with left:
    if st.button("Desfazer último ajuste", use_container_width=True):
        try:
            draft.undo()
            st.rerun()
        except ThemeLabError as exc:
            st.warning(str(exc))
with middle:
    if st.button("Restaurar base", use_container_width=True):
        draft.restore()
        st.rerun()
with right:
    st.metric("Revisão local", draft.revision)

st.subheader("2. Comparar")
if st.session_state.v10_show_preview:
    try:
        pair = compare_preview(draft)
        current_col, proposal_col = st.columns(2)
        for column, title, preview in (
            (current_col, "Base", pair.current),
            (proposal_col, "Proposta", pair.proposal),
        ):
            with column:
                st.markdown(f"### {title}")
                st.markdown(preview.header_html, unsafe_allow_html=True)
                st.markdown(preview.kpi_html, unsafe_allow_html=True)
                st.plotly_chart(preview.bar_figure, use_container_width=True)
                st.plotly_chart(preview.series_figure, use_container_width=True)
                st.plotly_chart(preview.heatmap_figure, use_container_width=True)
                st.markdown(preview.table_html, unsafe_allow_html=True)
    except ThemeLabError as exc:
        st.error(str(exc))

st.subheader("3. Salvar sessão própria")
st.caption(
    "Salvar preserva base, proposta, histórico e hashes no UC Volume configurado. "
    "Não submete, aprova, promove ou publica."
)
with st.form("v10-save-session"):
    new_session_name = st.text_input("Nome da sessão", placeholder="ex.: proposta-dashboard-risco")
    save_clicked = st.form_submit_button("Salvar sessão")
if save_clicked:
    try:
        receipt = save_own_session(draft, config, user, new_session_name)
        st.success(
            f"Sessão salva: {receipt.session_name}. Revisão {receipt.revision}; "
            f"histórico {receipt.history_depth}; manifesto {receipt.manifest_sha256[:12]}…"
        )
    except (ThemeAppError, ThemeLabError) as exc:
        st.error(str(exc))

with st.expander("Políticas desta V10"):
    st.json({"retention": retention_policy(), "publication": publication_policy()})
    st.caption(
        "Não existe ação de apagar sessão, aprovar ou publicar nesta superfície. "
        "Retenção e limpeza administrativa permanecem fora do usuário final."
    )
