"""Visual Lab V05: rascunhos de notebook, sem aprovação ou publicação.

O import não carrega a interface opcional. O laboratório usa os adaptadores
V03/V04 explicitamente, sem consulta externa, treinamento ou tema global.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from typing import Any, Mapping

from hub_snippets.visual.tema import (
    ResolvedTheme, ThemeError, export_theme, normalize_color, resolve_theme,
)


class ThemeLabError(ValueError):
    """Erro operacional sem repetir conteúdo arbitrário recebido."""

    def __init__(self, code: str, message: str, *, action: str):
        self.code = code
        self.action = action
        super().__init__(f"{code}: {message} {action}")


@dataclass(frozen=True)
class ControlSpec:
    """Metadados do contrato; disponibilidade na galeria não é autorização."""

    token: str
    label: str
    description: str
    unit: str | None
    control: str | None
    minimum: int | float | None
    maximum: int | float | None
    enum: tuple[str, ...]
    primary: bool
    preview_supported: bool = True
    unavailable_reason: str = ""


@dataclass(frozen=True)
class ProposalReceipt:
    """Recibo local após conferir bytes; não é recibo de publicação."""

    filename: str
    sha256: str
    bytes_written: int
    revision: int
    destination: str = ""


@dataclass(frozen=True)
class ThemeLabPreview:
    """Galeria sintética produzida pelos adaptadores reais V03/V04."""

    header_html: str
    kpi_html: str
    table_html: str
    bar_figure: Any
    series_figure: Any
    heatmap_figure: Any


@dataclass(frozen=True)
class ThemeLabComparison:
    """Mesmo conjunto sintético no ponto de partida e na proposta."""

    current: ThemeLabPreview
    proposal: ThemeLabPreview


_PRIMARY_TOKENS = (
    "brand.primary", "text.primary", "text.secondary", "surface.section",
    "surface.card", "chart.title_px", "section.title_px",
)
_LABELS = {
    "brand.primary": "Cor principal", "brand.accent": "Cor de destaque",
    "text.primary": "Texto principal", "text.plot": "Texto dos gráficos",
    "text.secondary": "Texto secundário", "surface.section": "Fundo de seção",
    "surface.card": "Fundo de cartão", "table.header_text": "Texto do cabeçalho da tabela",
    "divider.light": "Separador fino", "divider.medium": "Separador médio",
    "status.ok_bg": "Status OK — fundo", "status.ok_text": "Status OK — texto",
    "status.warn_bg": "Status alerta — fundo", "status.warn_text": "Status alerta — texto",
    "status.fail_bg": "Status falha — fundo", "status.fail_text": "Status falha — texto",
    "semantic.positive": "Semântica positiva", "semantic.negative": "Semântica negativa",
    "semantic.neutral": "Semântica neutra", "semantic.warning": "Semântica de alerta",
    "palette.categorical": "Paleta categórica", "palette.curves_legacy": "Paleta histórica de curvas",
    "palette.sequential": "Paleta sequencial", "palette.diverging": "Paleta divergente",
    "font.family": "Família tipográfica", "chart.font_px": "Gráfico — texto",
    "chart.title_px": "Gráfico — título", "chart.footer_px": "Gráfico — rodapé",
    "chart.height_px": "Gráfico — altura", "chart.width_px": "Gráfico — largura",
    "chart.margin_left_px": "Gráfico — margem esquerda", "chart.margin_right_px": "Gráfico — margem direita",
    "chart.margin_top_px": "Gráfico — margem superior", "chart.margin_bottom_px": "Gráfico — margem inferior",
    "section.title_px": "Seção — título", "section.description_px": "Seção — descrição",
    "section.radius_px": "Seção — raio", "section.padding_y_px": "Seção — espaçamento vertical",
    "section.padding_x_px": "Seção — espaçamento horizontal", "section.border_px": "Seção — borda",
    "card.font_px": "Cartão — texto", "card.radius_px": "Cartão — raio",
    "card.padding_y_px": "Cartão — espaçamento vertical", "card.padding_x_px": "Cartão — espaçamento horizontal",
    "badge.font_px": "Badge — texto", "badge.radius_px": "Badge — raio",
    "badge.padding_y_px": "Badge — espaçamento vertical", "badge.padding_x_px": "Badge — espaçamento horizontal",
}
# A cobertura é da galeria V05, não uma segunda definição de tipo/limite/default.
_NO_PREVIEW = frozenset({
    "brand.accent", "semantic.positive", "semantic.neutral", "semantic.warning",
    "palette.curves_legacy", "palette.sequential", "divider.light", "divider.medium",
    "status.ok_bg", "status.ok_text", "status.warn_bg", "status.warn_text",
    "status.fail_bg", "status.fail_text", "badge.font_px", "badge.radius_px",
    "badge.padding_y_px", "badge.padding_x_px",
})
_FILENAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,62}\.json$")
_PREFIX_RE = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
_MAX_HISTORY = 100


def _verified(theme: ResolvedTheme) -> ResolvedTheme:
    if type(theme) is not ResolvedTheme:
        raise ThemeLabError("LAB_THEME_TYPE", "O laboratório exige um ResolvedTheme.",
                            action="Carregue ou resolva uma configuração notebook com o núcleo V02.")
    return resolve_theme(export_theme(theme), expected_context="notebook")


def _schema_path() -> Path:
    return Path(__file__).absolute().parents[3] / "hub_padroes/identidade_visual/theme.schema.json"


def get_control_specs(theme: ResolvedTheme) -> tuple[ControlSpec, ...]:
    """Deriva campos, unidades e limites do schema verificado pelo núcleo V02."""
    verified = _verified(theme)
    try:
        with _schema_path().open("rb") as stream:
            raw = stream.read(131073)
    except OSError:
        raise ThemeLabError("LAB_SCHEMA_READ", "O contrato do pacote não pôde ser lido.",
                            action="Restaure o pacote do Hub antes de continuar.") from None
    if len(raw) > 131072 or hashlib.sha256(raw).hexdigest() != verified.schema_sha256:
        raise ThemeLabError("LAB_SCHEMA_HASH", "O schema difere do contrato verificado.",
                            action="Restaure o pacote compatível; não altere hashes para continuar.")
    try:
        props = json.loads(raw)["$defs"]["notebookTokens"]["properties"]
    except (ValueError, KeyError, TypeError):
        raise ThemeLabError("LAB_SCHEMA_FORMAT", "Metadados notebook indisponíveis.",
                            action="Restaure o contrato canônico.") from None
    result = []
    for token in verified.tokens:
        prop = props[token]
        meta = prop.get("x-hub", {})
        if not set(meta.get("editable_by", ())).intersection(("proponente", "mantenedor")):
            continue
        supported = token not in _NO_PREVIEW
        result.append(ControlSpec(
            token=token, label=_LABELS.get(token, prop.get("description", token)),
            description=prop.get("description", meta.get("effect", "")),
            unit=meta.get("unit"), control=meta.get("control"),
            minimum=prop.get("minimum"), maximum=prop.get("maximum"),
            enum=tuple(prop.get("enum", ())), primary=token in _PRIMARY_TOKENS,
            preview_supported=supported,
            unavailable_reason="" if supported else "Sem componente correspondente nesta galeria; valor preservado, controle desabilitado.",
        ))
    return tuple(result)


def _coerce_token(current: Any, raw: Any) -> Any:
    if type(current) is str:
        if current.startswith("#"):
            return normalize_color(raw)
        if type(raw) is str:
            return raw
    elif type(current) is int:
        if type(raw) is int:
            return raw
        if type(raw) is str and len(raw) <= 32 and re.fullmatch(r"-?(0|[1-9][0-9]*)", raw.strip()):
            return int(raw.strip())
    elif type(current) in (tuple, list):
        if type(raw) is str and len(raw) <= 131072:
            values = [item.strip() for item in raw.split(",")]
        elif type(raw) in (list, tuple):
            values = list(raw)
        else:
            values = None
        if values is not None:
            if not values or len(values) > 256 or any(not item for item in values):
                raise ThemeLabError("LAB_VALUE_TYPE", "A paleta contém entradas vazias ou excessivas.",
                                    action="Separe cores válidas por vírgula, sem itens vazios.")
            return [normalize_color(item) for item in values]
    raise ThemeLabError("LAB_VALUE_TYPE", "O valor não tem o tipo esperado pelo controle.",
                        action="Use texto, inteiro sem booleano ou uma lista de cores conforme o campo.")


def _candidate(theme: ResolvedTheme, updates: Mapping[str, Any]) -> ResolvedTheme:
    if not isinstance(updates, Mapping):
        raise ThemeLabError("LAB_UPDATES_TYPE", "As alterações precisam ser um mapeamento.",
                            action="Forneça token e valor explícitos, nunca código ou CSS.")
    data = _verified(theme).to_dict()
    for token, raw in updates.items():
        if type(token) is not str or token not in data["tokens"]:
            raise ThemeLabError("LAB_TOKEN_UNKNOWN", "Um campo não pertence ao contrato notebook.",
                                action="Use somente tokens do contrato carregado.")
        data["tokens"][token] = _coerce_token(data["tokens"][token], raw)
    return resolve_theme(data, expected_context="notebook")


@dataclass
class ThemeLabDraft:
    """Rascunho em memória, isolado por instância; histórico limitado a 100 estados."""

    base: ResolvedTheme
    current: ResolvedTheme = field(init=False)
    revision: int = field(default=0, init=False)
    _history: list[ResolvedTheme] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self.base = _verified(self.base)
        self.current = self.base

    @property
    def dirty(self) -> bool:
        return self.current.content_sha256 != self.base.content_sha256

    @property
    def history_depth(self) -> int:
        return len(self._history)

    def _commit(self, candidate: ResolvedTheme) -> ResolvedTheme:
        if candidate.content_sha256 != self.current.content_sha256:
            self._history.append(self.current)
            del self._history[:-_MAX_HISTORY]
            self.current = candidate
            self.revision += 1
        return self.current

    def apply_updates(self, updates: Mapping[str, Any]) -> ResolvedTheme:
        """Valida a configuração inteira antes de trocar o estado; erro não grava parcialmente."""
        return self._commit(_candidate(self.current, updates))

    def set_token(self, token: str, value: Any) -> ResolvedTheme:
        return self.apply_updates({token: value})

    def undo(self) -> ResolvedTheme:
        if not self._history:
            raise ThemeLabError("LAB_UNDO_EMPTY", "Não há alteração anterior no rascunho.",
                                action="Aplique uma mudança válida antes de Desfazer.")
        self.current = self._history.pop()
        self.revision += 1
        return self.current

    def restore(self) -> ResolvedTheme:
        return self._commit(_verified(self.base))

    def export_bytes(self) -> bytes:
        """Devolve JSON canônico em memória; não salva, submete, aprova ou publica."""
        return export_theme(self.current)

    def save_proposal(self, root: str | Path, filename: str) -> ProposalReceipt:
        """Cria arquivo exclusivo em pasta controlada; não sobrescreve nem apaga arquivos.

        Não é transação de filesystem ou sandbox contra outro processo hostil.
        Uma falha pode deixar arquivo parcial, que nunca recebe recibo de sucesso.
        A pasta e seus pais devem ter permissões controladas pelo mantenedor.
        """
        if type(filename) is not str or _FILENAME_RE.fullmatch(filename) is None:
            raise ThemeLabError("LAB_FILENAME", "Nome de arquivo inválido.",
                                action="Use nome simples em minúsculas terminado em .json, sem pastas.")
        try:
            root_path = Path(root).absolute()
            if not root_path.is_dir() or root_path.is_symlink() or any(p.is_symlink() for p in root_path.parents):
                raise ValueError
        except (TypeError, ValueError, OSError):
            raise ThemeLabError("LAB_SAVE_ROOT", "A raiz de rascunhos precisa ser uma pasta regular existente.",
                                action="Escolha uma pasta autorizada explicitamente, sem atalhos simbólicos.") from None
        target = root_path / filename
        payload = self.export_bytes()
        revision = self.revision
        fd = None
        try:
            flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open(target, flags, 0o600)
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode):
                raise OSError
            with os.fdopen(fd, "w+b") as stream:
                fd = None
                written = stream.write(payload)
                if written != len(payload):
                    raise OSError
                stream.flush()
                os.fsync(stream.fileno())
                stream.seek(0)
                observed = stream.read(len(payload) + 1)
                if observed != payload:
                    raise OSError
            final = target.lstat()
            if not stat.S_ISREG(final.st_mode) or (final.st_dev, final.st_ino, final.st_size) != (opened.st_dev, opened.st_ino, len(payload)):
                raise OSError
        except FileExistsError:
            raise ThemeLabError("LAB_SAVE_EXISTS", "Já existe um arquivo com esse nome.",
                                action="Escolha outro nome; nenhum arquivo existente será sobrescrito.") from None
        except OSError:
            # Nunca apagar target: uma falha de open pode ocorrer antes de termos
            # criado qualquer arquivo. Remover um arquivo vazio aqui apagaria dado alheio.
            raise ThemeLabError("LAB_SAVE_IO", "A proposta não foi confirmada no destino.",
                                action="Nenhum sucesso foi registrado. Pode haver arquivo parcial; peça inspeção ao mantenedor e não o importe como salvo.") from None
        finally:
            if fd is not None:
                os.close(fd)
        return ProposalReceipt(filename, hashlib.sha256(payload).hexdigest(), len(payload), revision, str(target))


def create_theme_lab(theme: ResolvedTheme) -> ThemeLabDraft:
    """Cria um rascunho notebook revalidado e isolado."""
    return ThemeLabDraft(theme)


def build_preview(theme: ResolvedTheme) -> ThemeLabPreview:
    """Monta somente dados sintéticos; não modifica o template global do Plotly."""
    verified = _verified(theme)
    if verified.to_dict()["mode"] != "light":
        raise ThemeLabError("LAB_PREVIEW_MODE", "A galeria completa requer o adaptador Plotly light.",
                            action="Use light; dark e high_contrast não estão homologados nesta galeria.")
    try:
        import pandas as pd
        import plotly.graph_objects as go
        from hub_snippets.display.dataframe_styled import display_styled_resolvido
        from hub_snippets.visual.kpi_card import kpi_card_html_resolvido
        from hub_snippets.visual.section_header import section_header_html_resolvido
        from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido
    except ImportError:
        raise ThemeLabError("LAB_PREVIEW_DEPENDENCY", "Dependências da galeria indisponíveis.",
                            action="Peça o ambiente declarado ao mantenedor; não há instalação automática.") from None
    bar = go.Figure()
    # Quatro séries mantêm nomes e valores fixos ao comparar paletas.
    for name, values in (("Volume A", [12, 7, 15, 9]), ("Volume B", [9, 6, 11, 7]),
                         ("Volume C", [5, 8, 10, 6]), ("Volume D", [7, 4, 8, 12])):
        bar.add_trace(go.Bar(x=["A", "B", "C", "D"], y=values, name=name))
    bar.update_layout(title="Barras — quatro séries sintéticas", barmode="group")
    aplicar_tema_resolvido(bar, verified, fonte="Dados sintéticos", n=16)
    series = go.Figure(go.Scatter(x=["Jan", "Fev", "Mar", "Abr", "Mai"], y=[100, 112, None, 109, 121], mode="lines+markers", name="Índice"))
    series.update_layout(title="Série temporal — inclui valor ausente")
    aplicar_tema_resolvido(series, verified, fonte="Dados sintéticos", n=5)
    heat = go.Figure(go.Heatmap(
        z=[[1.0, -0.2, 0.4], [-0.2, 1.0, -0.7], [0.4, -0.7, 1.0]],
        x=["X1", "X2", "X3"], y=["X1", "X2", "X3"], zmin=-1, zmax=1, zmid=0,
        colorscale=list(verified.tokens["palette.diverging"]),
    ))
    heat.update_layout(title="Mapa de calor — matriz sintética, não estimativa")
    aplicar_tema_resolvido(heat, verified, fonte="Dados sintéticos", n=9)
    table = pd.DataFrame({"Segmento": ["A", "B", "C", "Nulo"],
                          "Valor": [120.0, -35.0, 80.0, None], "Taxa": [0.12, -0.04, 0.08, None]})
    table_html = display_styled_resolvido(table, verified, highlight_cols=["Valor", "Taxa"],
                                         format_dict={"Valor": "{:.1f}", "Taxa": "{:.1%}"})
    return ThemeLabPreview(
        header_html=section_header_html_resolvido(verified, emoji="🎛️", titulo="Prévia do tema",
                                                descricao="Somente dados sintéticos; aparência não muda cálculos."),
        kpi_html=kpi_card_html_resolvido({"Linhas": 4, "Variação": "-3,5%", "Nulos": 1}, verified),
        table_html=table_html, bar_figure=bar, series_figure=series, heatmap_figure=heat,
    )


def compare_preview(draft: ThemeLabDraft) -> ThemeLabComparison:
    """Constrói as mesmas seis representações para base e proposta."""
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError("LAB_DRAFT_TYPE", "A comparação exige um rascunho.", action="Use create_theme_lab.")
    return ThemeLabComparison(build_preview(draft.base), build_preview(draft.current))


def _widget_name(prefix: str, token: str) -> str:
    if type(prefix) is not str or _PREFIX_RE.fullmatch(prefix) is None:
        raise ThemeLabError("LAB_WIDGET_PREFIX", "Prefixo de widgets inválido.",
                            action="Use de 1 a 40 letras minúsculas, números ou underscores, começando por letra.")
    return prefix + token.replace(".", "_")


def install_dbutils_fallback(draft: ThemeLabDraft, dbutils: Any, *, prefix: str = "hub_tema_") -> dict[str, str]:
    """Cria controles nativos explicitamente; valores existentes são preservados quando legíveis."""
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError("LAB_DRAFT_TYPE", "Rascunho inválido.", action="Use create_theme_lab.")
    widgets = getattr(dbutils, "widgets", None)
    if widgets is None or not callable(getattr(widgets, "text", None)):
        raise ThemeLabError("LAB_DBUTILS", "dbutils.widgets indisponível.", action="Use notebook compatível ou ipywidgets.")
    names = {token: _widget_name(prefix, token) for token in _PRIMARY_TOKENS}
    values = _verified(draft.current).tokens
    for token, name in names.items():
        existing = False
        if callable(getattr(widgets, "get", None)):
            try:
                widgets.get(name)
                existing = True
            except Exception:
                # A API nativa não oferece um tipo de exceção portátil de ausência.
                # Não removemos widgets; text usa a API do ambiente. Homologar no destino.
                pass
        if not existing:
            widgets.text(name, str(values[token]), _LABELS[token])
    return names


def apply_dbutils_fallback(draft: ThemeLabDraft, dbutils: Any, *, prefix: str = "hub_tema_") -> ResolvedTheme:
    """Captura strings dos controles e aplica a configuração inteira de uma vez."""
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError("LAB_DRAFT_TYPE", "Rascunho inválido.", action="Use create_theme_lab.")
    widgets = getattr(dbutils, "widgets", None)
    if widgets is None or not callable(getattr(widgets, "get", None)):
        raise ThemeLabError("LAB_DBUTILS", "dbutils.widgets indisponível.", action="Use notebook compatível.")
    names = {token: _widget_name(prefix, token) for token in _PRIMARY_TOKENS}
    try:
        updates = {token: widgets.get(name) for token, name in names.items()}
    except Exception:
        raise ThemeLabError("LAB_WIDGET_READ", "Não foi possível ler todos os controles.",
                            action="Confira prefixo e instalação do fallback; nenhum campo foi aplicado.") from None
    return draft.apply_updates(updates)


@dataclass
class ThemeLabUI:
    """Referências de interface; não representam sessão persistida ou aprovada."""

    root: Any
    draft: ThemeLabDraft
    controls: Mapping[str, Any]
    status: Any
    preview: Any


def build_ipywidgets_lab(draft: ThemeLabDraft, *, save_root: str | Path | None = None,
                        render_initial: bool = True) -> ThemeLabUI:
    """Constrói a UI opcional; o notebook chama display(ui.root).

    Campos não aplicados impedem exportar/salvar uma versão antiga por engano.
    A geração da nova galeria precede a troca do rascunho. Entrega ao navegador
    e permissões da pasta continuam dependendo de homologação no ambiente real.
    """
    if type(draft) is not ThemeLabDraft:
        raise ThemeLabError("LAB_DRAFT_TYPE", "Rascunho inválido.", action="Use create_theme_lab.")
    try:
        import ipywidgets as widgets
        import IPython  # disponibilidade da infraestrutura de notebook; não exibe a UI
    except ImportError:
        raise ThemeLabError("LAB_IPYWIDGETS_MISSING", "ipywidgets/IPython indisponíveis.",
                            action="Use o fallback nativo ou ambiente compatível; não há instalação automática.") from None
    specs = get_control_specs(draft.current)
    control_widgets, readers = {}, {}
    primary_boxes, advanced_boxes = [], []
    status = widgets.HTML(value="<b>Prévia pessoal:</b> nenhuma publicação realizada.")

    def safe_error(exc: Exception) -> str:
        if isinstance(exc, (ThemeLabError, ThemeError)):
            return escape(str(exc))
        return "Falha na apresentação. Registre o problema com o mantenedor; não considere a prévia homologada."

    def formatted(value: Any) -> Any:
        return ", ".join(value) if type(value) in (tuple, list) else value

    def make_control(spec: ControlSpec) -> Any:
        value = draft.current.tokens[spec.token]
        label = widgets.HTML(value=f"<b>{escape(spec.label)}</b> <code>{escape(spec.token)}</code><br><small>{escape(spec.description)}</small>")
        details = widgets.HTML(value=f"<small>Unidade: {escape(str(spec.unit))}; limites: {spec.minimum} a {spec.maximum}. {escape(spec.unavailable_reason)}</small>")
        if type(value) is str and value.startswith("#"):
            picker = widgets.ColorPicker(value=value, description="Cor", disabled=not spec.preview_supported)
            field_widget = widgets.Text(value=value, description="HEX", disabled=not spec.preview_supported)
            busy = {"value": False}
            def from_picker(change):
                if not busy["value"]:
                    busy["value"] = True
                    try:
                        field_widget.value = change["new"].upper()
                    finally:
                        busy["value"] = False
            def from_text(change):
                if not busy["value"]:
                    try:
                        normalized = normalize_color(change["new"])
                    except ThemeError as exc:
                        status.value = f"<b>{escape(spec.label)}:</b> {safe_error(exc)} A proposta válida não foi alterada."
                        return
                    busy["value"] = True
                    try:
                        picker.value = normalized
                    finally:
                        busy["value"] = False
            picker.observe(from_picker, names="value")
            field_widget.observe(from_text, names="value")
            field_box = widgets.HBox([picker, field_widget])
        elif type(value) is int:
            field_widget = widgets.IntText(value=value, description="Valor", disabled=not spec.preview_supported)
            field_box = field_widget
        elif type(value) in (tuple, list):
            field_widget = widgets.Textarea(value=formatted(value), description="Cores", disabled=not spec.preview_supported)
            field_box = field_widget
        elif spec.enum:
            field_widget = widgets.Dropdown(options=list(spec.enum), value=value, description="Valor", disabled=not spec.preview_supported)
            field_box = field_widget
        else:
            field_widget = widgets.Text(value=str(value), description="Valor", disabled=not spec.preview_supported)
            field_box = field_widget
        control_widgets[spec.token] = field_widget
        if spec.preview_supported:
            readers[spec.token] = lambda widget=field_widget: widget.value
        restore_field = widgets.Button(description="Restaurar este campo", disabled=not spec.preview_supported)
        def restore_one(_):
            field_widget.value = formatted(draft.base.tokens[spec.token])
            status.value = "Campo restaurado no formulário. Clique Aplicar na prévia para validar."
        restore_field.on_click(restore_one)
        return widgets.VBox([label, details, field_box, restore_field])

    for spec in specs:
        (primary_boxes if spec.primary else advanced_boxes).append(make_control(spec))
    preview, export_output = widgets.Output(), widgets.Output()
    filename = widgets.Text(value="proposta-tema.json", description="Arquivo")
    confirm_discard = widgets.Checkbox(value=False, description="Confirmo descartar campos pendentes / restaurar a base")
    apply_button = widgets.Button(description="Aplicar na prévia", button_style="primary")
    undo_button = widgets.Button(description="Desfazer")
    restore_button = widgets.Button(description="Restaurar ponto de partida")
    export_button = widgets.Button(description="Exportar JSON na saída")
    save_button = widgets.Button(description="Salvar proposta", disabled=save_root is None)
    submit_button = widgets.Button(description="Submeter para revisão", disabled=True)
    publish_button = widgets.Button(description="Publicar versão aprovada", disabled=True)

    def pending() -> bool:
        return any(reader() != formatted(draft.current.tokens[token]) for token, reader in readers.items())

    def sync_controls() -> None:
        for token, widget in control_widgets.items():
            widget.value = formatted(draft.current.tokens[token])
        confirm_discard.value = False

    def present(comparison: ThemeLabComparison) -> None:
        # Materializa toda a saída antes de trocar outputs. Não usa contexto
        # Output (que pode capturar exceções) nem injeta JS/CDN de um renderer.
        outputs = []
        def html_output(text):
            outputs.append({"output_type": "display_data", "data": {"text/html": text}, "metadata": {}})
        for title, panel in (("Ponto de partida", comparison.current), ("Proposta", comparison.proposal)):
            html_output(f"<h4>{title}</h4>")
            html_output(panel.header_html)
            html_output(panel.kpi_html)
            for figure in (panel.bar_figure, panel.series_figure, panel.heatmap_figure):
                outputs.append({"output_type": "display_data", "data": {
                    "application/vnd.plotly.v1+json": json.loads(figure.to_json()),
                    "text/plain": "Figura Plotly sintética. Se aparecer apenas este texto, use a rota de comparação fora do painel descrita no guia.",
                }, "metadata": {}})
            html_output(panel.table_html)
        if len(json.dumps(outputs, ensure_ascii=False).encode("utf-8")) > 4_000_000:
            raise ThemeLabError("LAB_PREVIEW_SIZE", "A saída excede o orçamento local da galeria.",
                                action="Não aplique esta prévia; peça revisão ao mantenedor.")
        preview.outputs = tuple(outputs)

    def on_apply(_):
        try:
            candidate = _candidate(draft.current, {token: read() for token, read in readers.items()})
            comparison = ThemeLabComparison(build_preview(draft.base), build_preview(candidate))
            present(comparison)
            draft._commit(candidate)
            sync_controls()
            status.value = f"Prévia enviada à saída. Revisão local {draft.revision}. Nada salvo ou publicado."
        except Exception as exc:
            status.value = f"<b>Não aplicado:</b> {safe_error(exc)} O estado válido do rascunho foi preservado."

    def on_undo(_):
        if pending() and not confirm_discard.value:
            status.value = "Há campos não aplicados. Marque a confirmação para descartá-los antes de Desfazer."
            return
        try:
            if not draft._history:
                raise ThemeLabError("LAB_UNDO_EMPTY", "Não há alteração anterior.", action="Aplique uma alteração válida.")
            comparison = ThemeLabComparison(build_preview(draft.base), build_preview(draft._history[-1]))
            present(comparison)
            draft.undo()
            sync_controls()
            status.value = "Alteração desfeita. Nada publicado."
        except Exception as exc:
            status.value = f"<b>Não desfeito:</b> {safe_error(exc)}"

    def on_restore(_):
        if (pending() or draft.dirty) and not confirm_discard.value:
            status.value = "Confirme a restauração na caixa de confirmação; desmarcada, não altera seu trabalho."
            return
        try:
            comparison = ThemeLabComparison(build_preview(draft.base), build_preview(draft.base))
            present(comparison)
            draft.restore()
            sync_controls()
            status.value = "Ponto de partida restaurado. Nada publicado."
        except Exception as exc:
            status.value = f"<b>Não restaurado:</b> {safe_error(exc)}"

    def require_applied() -> None:
        if pending():
            raise ThemeLabError("LAB_PENDING_FIELDS", "Há campos ainda não aplicados.",
                                action="Clique Aplicar na prévia; não exporte ou salve uma revisão antiga por engano.")

    def on_export(_):
        try:
            require_applied()
            payload = draft.export_bytes()
            text = (payload.decode("utf-8") + f"SHA-256: {hashlib.sha256(payload).hexdigest()}\n"
                    "JSON na saída: copie somente o JSON completo. Nenhum arquivo foi salvo; não é publicação.\n")
            export_output.outputs = ({"output_type": "stream", "name": "stdout", "text": text},)
        except Exception as exc:
            status.value = f"<b>Não exportado:</b> {safe_error(exc)}"

    def on_save(_):
        try:
            require_applied()
            receipt = draft.save_proposal(save_root, filename.value)
            status.value = (f"<b>Rascunho salvo:</b> {escape(receipt.destination)}<br>"
                            f"SHA-256 {receipt.sha256}; {receipt.bytes_written} bytes; revisão {receipt.revision}. "
                            "Não submetido, aprovado ou publicado.")
        except Exception as exc:
            status.value = f"<b>Não salvo:</b> {safe_error(exc)}"

    apply_button.on_click(on_apply)
    undo_button.on_click(on_undo)
    restore_button.on_click(on_restore)
    export_button.on_click(on_export)
    save_button.on_click(on_save)
    advanced = widgets.Accordion(children=[widgets.VBox(advanced_boxes)])
    advanced.set_title(0, "Avançado — cobertura e limites")
    base_data = draft.base.to_dict()
    intro = widgets.HTML(value=(
        "<h3>Aparência do Hub — prévia pessoal V05</h3><p>Alterações aqui não mudam o padrão da equipe.</p>"
        f"<p>Ponto de partida: {escape(base_data['display_name'])}; contexto notebook; revisão visual {escape(base_data['theme_version'])}. "
        "Referência empacotada não significa tema aprovado.</p>"
        "<p>Guia: abra GUIA_PRIMEIRO_USO.md na mesma pasta do notebook. A galeria usa light, dados sintéticos e quatro séries; "
        "imagens e consumidores externos não são recoloridos.</p>"
    ))
    destination_note = widgets.HTML(value="Salvar desabilitado: mantenedor não definiu pasta." if save_root is None else f"Pasta de rascunhos indicada: {escape(str(save_root))}. A permissão será conferida na escrita.")
    controls_panel = widgets.VBox([
        intro, status, *primary_boxes, advanced, confirm_discard,
        widgets.HBox([apply_button, undo_button, restore_button]), destination_note,
        widgets.HBox([filename, save_button, export_button]), export_output,
        widgets.HBox([submit_button, publish_button]),
        widgets.HTML(value="Submissão, aprovação e publicação não estão implementadas. Botões desabilitados não são autorização de servidor."),
    ])
    root = widgets.Tab(children=[controls_panel, widgets.VBox([preview])])
    root.set_title(0, "Escolher e ajustar")
    root.set_title(1, "Comparar")
    if render_initial:
        try:
            present(compare_preview(draft))
        except Exception as exc:
            status.value = f"<b>Prévia indisponível:</b> {safe_error(exc)}"
    return ThemeLabUI(root, draft, control_widgets, status, preview)
