"""Visual Lab V05 para propostas de tema em notebook.

A lógica de rascunho não depende de Databricks nem de ipywidgets. A interface
ipywidgets é opcional e importada somente na chamada. Nenhuma função publica,
aprova, consulta dados externos, treina modelos ou altera tema global de sessão.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from hub_snippets.visual.tema import (
    ResolvedTheme,
    ThemeError,
    export_theme,
    normalize_color,
    resolve_theme,
)


class ThemeLabError(ValueError):
    """Erro seguro e operacional do laboratório, sem repetir valores não confiáveis."""

    def __init__(self, code: str, message: str, *, action: str):
        self.code = code
        self.action = action
        super().__init__(f"{code}: {message} {action}")


@dataclass(frozen=True)
class ControlSpec:
    """Metadado de controle derivado do schema canônico, não regra de validação."""

    token: str
    label: str
    description: str
    unit: str | None
    control: str | None
    minimum: int | float | None
    maximum: int | float | None
    enum: tuple[str, ...]
    primary: bool


@dataclass(frozen=True)
class ProposalReceipt:
    """Recibo local de gravação de rascunho; nunca recibo de publicação."""

    filename: str
    sha256: str
    bytes_written: int
    revision: int


@dataclass(frozen=True)
class ThemeLabPreview:
    """Prévia sintética construída pelos adaptadores reais V03/V04."""

    header_html: str
    kpi_html: str
    table_html: str
    bar_figure: Any
    series_figure: Any
    heatmap_figure: Any


@dataclass(frozen=True)
class ThemeLabComparison:
    """Mesmo dataset sintético em referência e proposta."""

    current: ThemeLabPreview
    proposal: ThemeLabPreview


_PRIMARY_TOKENS = (
    "brand.primary",
    "text.primary",
    "text.secondary",
    "surface.section",
    "surface.card",
    "chart.title_px",
    "section.title_px",
)

_LABELS = {
    "brand.primary": "Cor principal",
    "brand.accent": "Cor de destaque",
    "text.primary": "Texto principal",
    "text.plot": "Texto dos gráficos",
    "text.secondary": "Texto secundário",
    "surface.section": "Fundo de seção",
    "surface.card": "Fundo de cartão",
    "table.header_text": "Texto do cabeçalho da tabela",
    "divider.light": "Separador fino",
    "divider.medium": "Separador médio",
    "status.ok_bg": "Status OK — fundo",
    "status.ok_text": "Status OK — texto",
    "status.warn_bg": "Status alerta — fundo",
    "status.warn_text": "Status alerta — texto",
    "status.fail_bg": "Status falha — fundo",
    "status.fail_text": "Status falha — texto",
    "semantic.positive": "Semântica positiva",
    "semantic.negative": "Semântica negativa",
    "semantic.neutral": "Semântica neutra",
    "semantic.warning": "Semântica de alerta",
    "palette.categorical": "Paleta categórica",
    "palette.curves_legacy": "Paleta histórica de curvas",
    "palette.sequential": "Paleta sequencial",
    "palette.diverging": "Paleta divergente",
    "font.family": "Família tipográfica",
    "chart.font_px": "Gráfico — texto",
    "chart.title_px": "Gráfico — título",
    "chart.footer_px": "Gráfico — rodapé",
    "chart.height_px": "Gráfico — altura",
    "chart.width_px": "Gráfico — largura",
    "chart.margin_left_px": "Gráfico — margem esquerda",
    "chart.margin_right_px": "Gráfico — margem direita",
    "chart.margin_top_px": "Gráfico — margem superior",
    "chart.margin_bottom_px": "Gráfico — margem inferior",
    "section.title_px": "Seção — título",
    "section.description_px": "Seção — descrição",
    "section.radius_px": "Seção — raio",
    "section.padding_y_px": "Seção — espaçamento vertical",
    "section.padding_x_px": "Seção — espaçamento horizontal",
    "section.border_px": "Seção — borda",
    "card.font_px": "Cartão — texto",
    "card.radius_px": "Cartão — raio",
    "card.padding_y_px": "Cartão — espaçamento vertical",
    "card.padding_x_px": "Cartão — espaçamento horizontal",
    "badge.font_px": "Badge — texto",
    "badge.radius_px": "Badge — raio",
    "badge.padding_y_px": "Badge — espaçamento vertical",
    "badge.padding_x_px": "Badge — espaçamento horizontal",
}

_FILENAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,62}\.json$")


def _verified(theme: ResolvedTheme) -> ResolvedTheme:
    if type(theme) is not ResolvedTheme:
        raise ThemeLabError(
            "LAB_THEME_TYPE",
            "O laboratório exige um ResolvedTheme do núcleo V02.",
            action="Carregue ou resolva uma configuração notebook antes de abrir o laboratório.",
        )
    verified = resolve_theme(export_theme(theme), expected_context="notebook")
    return verified


def _schema_path() -> Path:
    assistant_root = Path(__file__).absolute().parents[3]
    return assistant_root / "hub_padroes" / "identidade_visual" / "theme.schema.json"


def get_control_specs(theme: ResolvedTheme) -> tuple[ControlSpec, ...]:
    """Lê metadados de UI do schema cujo hash já integra o ResolvedTheme."""
    verified = _verified(theme)
    path = _schema_path()
    try:
        raw = path.read_bytes()
    except OSError:
        raise ThemeLabError(
            "LAB_SCHEMA_READ",
            "O contrato visual do pacote não pôde ser lido.",
            action="Restaure o pacote do Hub antes de continuar.",
        ) from None
    if hashlib.sha256(raw).hexdigest() != verified.schema_sha256:
        raise ThemeLabError(
            "LAB_SCHEMA_HASH",
            "O schema disponível não corresponde ao tema resolvido.",
            action="Recarregue uma versão compatível do Hub; não continue com metadados divergentes.",
        )
    try:
        schema = json.loads(raw)
        props = schema["$defs"]["notebookTokens"]["properties"]
    except (ValueError, KeyError, TypeError):
        raise ThemeLabError(
            "LAB_SCHEMA_FORMAT",
            "O schema não contém os metadados notebook esperados.",
            action="Restaure o contrato canônico antes de abrir controles.",
        ) from None

    specs: list[ControlSpec] = []
    for token in verified.tokens:
        prop = props[token]
        meta = prop.get("x-hub", {})
        editable_by = tuple(meta.get("editable_by", ()))
        if "proponente" not in editable_by and "mantenedor" not in editable_by:
            continue
        specs.append(
            ControlSpec(
                token=token,
                label=_LABELS.get(token, prop.get("description", token)),
                description=prop.get("description", meta.get("effect", "")),
                unit=meta.get("unit"),
                control=meta.get("control"),
                minimum=prop.get("minimum"),
                maximum=prop.get("maximum"),
                enum=tuple(prop.get("enum", ())),
                primary=token in _PRIMARY_TOKENS,
            )
        )
    return tuple(specs)


def _coerce_token(current: Any, raw: Any) -> Any:
    if type(current) is str:
        if current.startswith("#"):
            return normalize_color(raw)
        if type(raw) is not str:
            raise ThemeLabError(
                "LAB_VALUE_TYPE",
                "O campo textual recebeu outro tipo.",
                action="Informe texto e aplique novamente.",
            )
        return raw
    if type(current) is int:
        if type(raw) is bool:
            raise ThemeLabError(
                "LAB_VALUE_TYPE",
                "O campo numérico não aceita verdadeiro/falso.",
                action="Informe um número inteiro dentro do limite mostrado.",
            )
        if type(raw) is int:
            return raw
        if type(raw) is str and re.fullmatch(r"-?(0|[1-9][0-9]*)", raw.strip()):
            return int(raw.strip())
        raise ThemeLabError(
            "LAB_VALUE_TYPE",
            "O campo numérico exige inteiro.",
            action="Informe um número inteiro dentro do limite mostrado.",
        )
    if type(current) in (tuple, list):
        if type(raw) is str:
            values = [item.strip() for item in raw.split(",") if item.strip()]
        elif type(raw) in (list, tuple):
            values = list(raw)
        else:
            raise ThemeLabError(
                "LAB_VALUE_TYPE",
                "A paleta exige uma lista de cores.",
                action="Informe cores #RRGGBB separadas por vírgula.",
            )
        return [normalize_color(item) for item in values]
    raise ThemeLabError(
        "LAB_VALUE_TYPE",
        "O tipo deste token ainda não possui controle no laboratório.",
        action="Mantenha o valor atual e consulte o mantenedor.",
    )


@dataclass
class ThemeLabDraft:
    """Rascunho isolado por instância; nenhuma variável global de tema é alterada."""

    base: ResolvedTheme
    current: ResolvedTheme = field(init=False)
    revision: int = field(default=0, init=False)
    _history: list[ResolvedTheme] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        verified = _verified(self.base)
        self.base = verified
        self.current = verified

    @property
    def dirty(self) -> bool:
        return self.current.content_sha256 != self.base.content_sha256

    @property
    def history_depth(self) -> int:
        return len(self._history)

    def apply_updates(self, updates: Mapping[str, Any]) -> ResolvedTheme:
        """Aplica todos os campos de forma atômica; erro preserva a última prévia válida."""
        if not isinstance(updates, Mapping):
            raise ThemeLabError(
                "LAB_UPDATES_TYPE",
                "As alterações precisam ser fornecidas como mapeamento.",
                action="Use token e valor explícitos; não passe código nem CSS.",
            )
        data = self.current.to_dict()
        tokens = data["tokens"]
        for token, raw in updates.items():
            if type(token) is not str or token not in tokens:
                raise ThemeLabError(
                    "LAB_TOKEN_UNKNOWN",
                    "Um controle não pertence ao contrato notebook carregado.",
                    action="Atualize a interface e escolha somente controles exibidos pelo laboratório.",
                )
            tokens[token] = _coerce_token(tokens[token], raw)
        candidate = resolve_theme(data, expected_context="notebook")
        if candidate.content_sha256 == self.current.content_sha256:
            return self.current
        self._history.append(self.current)
        self.current = candidate
        self.revision += 1
        return self.current

    def set_token(self, token: str, value: Any) -> ResolvedTheme:
        return self.apply_updates({token: value})

    def undo(self) -> ResolvedTheme:
        if not self._history:
            raise ThemeLabError(
                "LAB_UNDO_EMPTY",
                "Não há alteração anterior neste rascunho.",
                action="Aplique uma mudança válida antes de usar Desfazer.",
            )
        self.current = self._history.pop()
        self.revision += 1
        return self.current

    def restore(self) -> ResolvedTheme:
        if self.current.content_sha256 == self.base.content_sha256:
            return self.current
        self._history.append(self.current)
        self.current = self.base
        self.revision += 1
        return self.current

    def export_bytes(self) -> bytes:
        """Exporta JSON canônico em memória; não salva, submete, aprova ou publica."""
        return export_theme(self.current)

    def save_proposal(self, root: str | Path, filename: str) -> ProposalReceipt:
        """Grava um novo rascunho JSON em raiz explícita, sem sobrescrever arquivo existente."""
        if type(filename) is not str or _FILENAME_RE.fullmatch(filename) is None:
            raise ThemeLabError(
                "LAB_FILENAME",
                "Use nome simples em minúsculas terminado em .json.",
                action="Não use pastas, espaços, caminhos absolutos ou nomes de publicação.",
            )
        root_path = Path(root).absolute()
        try:
            if not root_path.is_dir() or root_path.is_symlink() or any(p.is_symlink() for p in root_path.parents):
                raise ThemeLabError(
                    "LAB_SAVE_ROOT",
                    "A raiz de rascunhos precisa ser uma pasta regular já existente.",
                    action="Escolha uma pasta autorizada e explícita para propostas.",
                )
            target = root_path / filename
            payload = self.export_bytes()
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open(target, flags, 0o600)
            try:
                with os.fdopen(fd, "wb") as stream:
                    fd = -1
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
            finally:
                if fd >= 0:
                    os.close(fd)
        except FileExistsError:
            raise ThemeLabError(
                "LAB_SAVE_EXISTS",
                "Já existe um arquivo com esse nome.",
                action="Escolha outro nome; o laboratório V05 não sobrescreve rascunhos.",
            ) from None
        except ThemeLabError:
            raise
        except OSError:
            try:
                if 'target' in locals() and target.exists() and target.stat().st_size == 0:
                    target.unlink()
            except OSError:
                pass
            raise ThemeLabError(
                "LAB_SAVE_IO",
                "A proposta não foi confirmada no destino.",
                action="Confira a pasta, a permissão e o espaço disponível; não trate a tentativa como salva.",
            ) from None
        return ProposalReceipt(filename, hashlib.sha256(payload).hexdigest(), len(payload), self.revision)


def create_theme_lab(theme: ResolvedTheme) -> ThemeLabDraft:
    """Cria rascunho isolado a partir de tema notebook já resolvido."""
    return ThemeLabDraft(theme)


def build_preview(theme: ResolvedTheme) -> ThemeLabPreview:
    """Monta galeria sintética pelos adaptadores V03/V04; nunca lê tabela externa."""
    verified = _verified(theme)
    if verified.to_dict()["mode"] != "light":
        raise ThemeLabError(
            "LAB_PREVIEW_MODE",
            "A galeria completa V05 ainda depende do adaptador Plotly light da V03.",
            action="Use modo light para a prévia completa; dark/high_contrast continuam sem homologação Plotly.",
        )
    try:
        import pandas as pd
        import plotly.graph_objects as go
        from hub_snippets.display.dataframe_styled import display_styled_resolvido
        from hub_snippets.visual.kpi_card import kpi_card_html_resolvido
        from hub_snippets.visual.section_header import section_header_html_resolvido
        from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido
    except ImportError:
        raise ThemeLabError(
            "LAB_PREVIEW_DEPENDENCY",
            "As dependências de prévia não estão disponíveis neste runtime.",
            action="Use o ambiente declarado do Hub; o laboratório não instala bibliotecas automaticamente.",
        ) from None

    bar = go.Figure(go.Bar(x=["A", "B", "C", "D"], y=[12, 7, 15, 9], name="Volume"))
    bar.update_layout(title="Barras — categorias sintéticas")
    aplicar_tema_resolvido(bar, verified, fonte="Dados sintéticos", n=4)

    series = go.Figure(go.Scatter(x=["Jan", "Fev", "Mar", "Abr", "Mai"], y=[100, 112, None, 109, 121], mode="lines+markers", name="Índice"))
    series.update_layout(title="Série temporal — inclui valor ausente")
    aplicar_tema_resolvido(series, verified, fonte="Dados sintéticos", n=5)

    heat = go.Figure(go.Heatmap(z=[[1.0, -0.2, 0.4], [-0.2, 1.0, -0.7], [0.4, -0.7, 1.0]], x=["X1", "X2", "X3"], y=["X1", "X2", "X3"], zmin=-1, zmax=1))
    heat.update_layout(title="Mapa de calor — correlação sintética")
    aplicar_tema_resolvido(heat, verified, fonte="Dados sintéticos", n=3)

    table = pd.DataFrame({
        "Segmento": ["A", "B", "C", "Nulo"],
        "Valor": [120.0, -35.0, 80.0, None],
        "Taxa": [0.12, -0.04, 0.08, None],
    })
    table_html = display_styled_resolvido(
        table,
        verified,
        highlight_cols=["Valor", "Taxa"],
        format_dict={"Valor": "{:.1f}", "Taxa": "{:.1%}"},
    )
    return ThemeLabPreview(
        header_html=section_header_html_resolvido(
            verified,
            emoji="🎛️",
            titulo="Prévia do tema",
            descricao="Somente dados sintéticos; alterar aparência não muda cálculos.",
        ),
        kpi_html=kpi_card_html_resolvido({"Linhas": 4, "Variação": "-3,5%", "Nulos": 1}, verified),
        table_html=table_html,
        bar_figure=bar,
        series_figure=series,
        heatmap_figure=heat,
    )


def compare_preview(draft: ThemeLabDraft) -> ThemeLabComparison:
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError(
            "LAB_DRAFT_TYPE",
            "A comparação exige um rascunho do Visual Lab.",
            action="Crie o rascunho com create_theme_lab.",
        )
    return ThemeLabComparison(build_preview(draft.base), build_preview(draft.current))


def _widget_name(prefix: str, token: str) -> str:
    safe = token.replace(".", "_")
    return f"{prefix}{safe}"


def install_dbutils_fallback(draft: ThemeLabDraft, dbutils: Any, *, prefix: str = "hub_tema_") -> dict[str, str]:
    """Cria fallback de widgets nativos; valores só entram no rascunho em apply_dbutils_fallback."""
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError("LAB_DRAFT_TYPE", "Rascunho inválido.", action="Crie-o com create_theme_lab.")
    widgets = getattr(dbutils, "widgets", None)
    if widgets is None or not callable(getattr(widgets, "text", None)):
        raise ThemeLabError(
            "LAB_DBUTILS",
            "A API dbutils.widgets não está disponível.",
            action="Use ipywidgets ou execute o fallback em notebook Databricks compatível.",
        )
    names: dict[str, str] = {}
    for token in _PRIMARY_TOKENS:
        name = _widget_name(prefix, token)
        value = draft.current.tokens[token]
        widgets.text(name, str(value), _LABELS[token])
        names[token] = name
    return names


def apply_dbutils_fallback(draft: ThemeLabDraft, dbutils: Any, *, prefix: str = "hub_tema_") -> ResolvedTheme:
    """Lê widgets nativos como strings e aplica tudo atomicamente após reexecução da célula."""
    widgets = getattr(dbutils, "widgets", None)
    if widgets is None or not callable(getattr(widgets, "get", None)):
        raise ThemeLabError("LAB_DBUTILS", "A API dbutils.widgets não está disponível.", action="Use um notebook compatível.")
    updates = {token: widgets.get(_widget_name(prefix, token)) for token in _PRIMARY_TOKENS}
    return draft.apply_updates(updates)


@dataclass
class ThemeLabUI:
    """Referências da UI para notebook e testes; não representa estado persistente."""

    root: Any
    draft: ThemeLabDraft
    controls: Mapping[str, Any]
    status: Any
    preview: Any


def build_ipywidgets_lab(
    draft: ThemeLabDraft,
    *,
    save_root: str | Path | None = None,
    render_initial: bool = True,
) -> ThemeLabUI:
    """Constrói o laboratório ipywidgets sem exibi-lo automaticamente.

    O chamador faz ``display(ui.root)``. A interface não cria compute, não salva
    sem clique explícito e não disponibiliza submissão/aprovação/publicação.
    """
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError("LAB_DRAFT_TYPE", "Rascunho inválido.", action="Crie-o com create_theme_lab.")
    try:
        import ipywidgets as widgets
        from IPython.display import HTML, display
    except ImportError:
        raise ThemeLabError(
            "LAB_IPYWIDGETS_MISSING",
            "ipywidgets/IPython não estão disponíveis neste runtime.",
            action="Use o fallback dbutils ou um runtime Databricks compatível; o laboratório não instala pacotes automaticamente.",
        ) from None

    specs = get_control_specs(draft.current)
    control_widgets: dict[str, Any] = {}
    readers: dict[str, Any] = {}
    primary_boxes: list[Any] = []
    advanced_boxes: list[Any] = []

    def make_control(spec: ControlSpec) -> Any:
        value = draft.current.tokens[spec.token]
        description = widgets.HTML(
            value=f"<b>{spec.label}</b><br><small>{spec.description}</small>"
            + (f"<br><small>Unidade: {spec.unit}</small>" if spec.unit else "")
        )
        if type(value) is str and value.startswith("#"):
            picker = widgets.ColorPicker(value=value, concise=False, description="Cor")
            text = widgets.Text(value=value, description="HEX")
            guard = {"busy": False}
            def from_picker(change):
                if change.get("name") == "value" and not guard["busy"]:
                    guard["busy"] = True
                    text.value = change["new"].upper()
                    guard["busy"] = False
            def from_text(change):
                if change.get("name") == "value" and not guard["busy"]:
                    try:
                        normalized = normalize_color(change["new"])
                    except Exception:
                        return
                    guard["busy"] = True
                    picker.value = normalized
                    guard["busy"] = False
            picker.observe(from_picker, names="value")
            text.observe(from_text, names="value")
            readers[spec.token] = lambda field=text: field.value
            control_widgets[spec.token] = text
            return widgets.VBox([description, widgets.HBox([picker, text])])
        if type(value) is int:
            field = widgets.IntText(value=value, description="Valor")
            readers[spec.token] = lambda field=field: field.value
            control_widgets[spec.token] = field
            limits = ""
            if spec.minimum is not None or spec.maximum is not None:
                limits = f"Limites do contrato: {spec.minimum if spec.minimum is not None else '—'} a {spec.maximum if spec.maximum is not None else '—'}"
            return widgets.VBox([description, field, widgets.HTML(value=f"<small>{limits}</small>")])
        if type(value) in (tuple, list):
            field = widgets.Textarea(value=", ".join(value), description="Cores", layout=widgets.Layout(width="100%", height="70px"))
            readers[spec.token] = lambda field=field: field.value
            control_widgets[spec.token] = field
            return widgets.VBox([description, field])
        if spec.enum:
            field = widgets.Dropdown(options=list(spec.enum), value=value, description="Valor")
        else:
            field = widgets.Text(value=str(value), description="Valor")
        readers[spec.token] = lambda field=field: field.value
        control_widgets[spec.token] = field
        return widgets.VBox([description, field])

    for spec in specs:
        box = make_control(spec)
        (primary_boxes if spec.primary else advanced_boxes).append(box)

    status = widgets.HTML(value="<b>Estado:</b> rascunho carregado; nenhuma publicação foi realizada.")
    preview = widgets.Output()
    export_output = widgets.Output()
    filename = widgets.Text(value="proposta-tema.json", description="Arquivo")
    apply_button = widgets.Button(description="Aplicar na prévia", button_style="primary")
    undo_button = widgets.Button(description="Desfazer")
    restore_button = widgets.Button(description="Restaurar ponto de partida")
    export_button = widgets.Button(description="Exportar JSON na saída")
    save_button = widgets.Button(description="Salvar proposta")
    if save_root is None:
        save_button.disabled = True
        save_button.tooltip = "Defina save_root explicitamente para habilitar gravação de rascunho."

    submit_button = widgets.Button(description="Submeter para revisão", disabled=True)
    publish_button = widgets.Button(description="Publicar versão aprovada", disabled=True)
    governance_note = widgets.HTML(
        value="<small><b>V05:</b> submissão, aprovação e publicação não estão implementadas. "
              "Botões desabilitados não substituem autorização de servidor.</small>"
    )

    def sync_controls() -> None:
        for token, widget in control_widgets.items():
            value = draft.current.tokens[token]
            if type(value) in (tuple, list):
                widget.value = ", ".join(value)
            else:
                widget.value = value

    def render() -> None:
        with preview:
            preview.clear_output(wait=True)
            try:
                comparison = compare_preview(draft)
                display(HTML("<h4>Atual preservado</h4>"))
                display(HTML(comparison.current.header_html))
                display(comparison.current.bar_figure)
                display(HTML("<h4>Proposta</h4>"))
                display(HTML(comparison.proposal.header_html))
                display(HTML(comparison.proposal.kpi_html))
                display(comparison.proposal.bar_figure)
                display(comparison.proposal.series_figure)
                display(comparison.proposal.heatmap_figure)
                display(HTML(comparison.proposal.table_html))
            except (ThemeLabError, ThemeError) as exc:
                display(HTML(f"<b>Prévia não atualizada.</b> {str(exc)}"))

    def on_apply(_button):
        try:
            draft.apply_updates({token: reader() for token, reader in readers.items()})
            status.value = f"<b>Estado:</b> prévia atualizada na revisão local {draft.revision}. Nada foi publicado."
            sync_controls()
            render()
        except (ThemeLabError, ThemeError) as exc:
            status.value = f"<b>Correção necessária:</b> {str(exc)} <b>A última prévia válida foi preservada.</b>"

    def on_undo(_button):
        try:
            draft.undo()
            sync_controls()
            status.value = f"<b>Estado:</b> alteração desfeita. Revisão local {draft.revision}."
            render()
        except ThemeLabError as exc:
            status.value = f"<b>Sem alteração:</b> {str(exc)}"

    def on_restore(_button):
        draft.restore()
        sync_controls()
        status.value = f"<b>Estado:</b> ponto de partida restaurado. Revisão local {draft.revision}."
        render()

    def on_export(_button):
        with export_output:
            export_output.clear_output(wait=True)
            payload = draft.export_bytes()
            print(payload.decode("utf-8"))
            print(f"SHA-256: {hashlib.sha256(payload).hexdigest()}")
            print("Exportação em memória; isto não é publicação.")

    def on_save(_button):
        try:
            receipt = draft.save_proposal(save_root, filename.value)
            status.value = (
                f"<b>Proposta salva:</b> {receipt.filename} · SHA-256 {receipt.sha256} · "
                f"{receipt.bytes_written} bytes. Não submetida nem publicada."
            )
        except (ThemeLabError, ThemeError) as exc:
            status.value = f"<b>Proposta não salva:</b> {str(exc)}"

    apply_button.on_click(on_apply)
    undo_button.on_click(on_undo)
    restore_button.on_click(on_restore)
    export_button.on_click(on_export)
    save_button.on_click(on_save)

    advanced = widgets.Accordion(children=[widgets.VBox(advanced_boxes)])
    advanced.set_title(0, "Avançado — paletas e propriedades")
    controls_panel = widgets.VBox(
        [
            widgets.HTML(value="<h3>Aparência do Hub — prévia pessoal V05</h3><p>Alterações aqui não mudam o padrão da equipe.</p>"),
            status,
            widgets.HTML(value="<h4>Ajustar</h4>"),
            *primary_boxes,
            advanced,
            widgets.HBox([apply_button, undo_button, restore_button]),
            widgets.HTML(value="<h4>Salvar / exportar proposta</h4>"),
            widgets.HBox([filename, save_button, export_button]),
            export_output,
            widgets.HTML(value="<h4>Governança</h4>"),
            widgets.HBox([submit_button, publish_button]),
            governance_note,
        ]
    )
    compare_panel = widgets.VBox([widgets.HTML(value="<h4>Comparar — Atual / Proposta</h4>"), preview])
    root = widgets.Tab(children=[controls_panel, compare_panel])
    root.set_title(0, "Escolher e ajustar")
    root.set_title(1, "Comparar")
    if render_initial:
        render()
    return ThemeLabUI(root=root, draft=draft, controls=control_widgets, status=status, preview=preview)
