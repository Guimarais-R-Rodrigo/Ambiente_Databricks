from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[4]
SNIPPETS = ROOT / "ambiente_fonte/.assistant/hub_snippets"

CATEGORIES = {
    "constants": {
        "titulo": "constantes, formatos e identidade compartilhada",
        "intro": "Reúne valores e convenções reutilizáveis para formatação brasileira, cores, estilos e símbolos usados por outros componentes do Hub.",
        "quando": "Entre aqui quando a dúvida for sobre apresentação padronizada, formatação monetária/percentual ou constantes compartilhadas, e não sobre cálculo analítico do dado.",
        "cuidado": "Alterar uma constante pode afetar vários consumidores. Leia o README do objeto e procure imports cruzados antes de mudar valores públicos.",
    },
    "display": {
        "titulo": "exibição e leitura de resultados analíticos",
        "intro": "Agrupa helpers de apresentação de DataFrames, matrizes e distribuições para tornar resultados mais legíveis sem confundir visualização com transformação de negócio.",
        "quando": "Use quando o dado já existe e a necessidade principal é inspecionar ou comunicar o resultado em tabela, matriz ou grade.",
        "cuidado": "Recursos de display podem coletar ou materializar dados no driver dependendo do objeto. Confira volume, efeito e dependências no guia local.",
    },
    "ml": {
        "titulo": "Machine Learning e estatística aplicada",
        "intro": "É a maior categoria do Hub: modelos, séries temporais, avaliação, explicabilidade, sobrevivência, drift, score, clustering, anomalias e utilitários de MLOps.",
        "quando": "Entre aqui quando a pergunta for de modelagem, validação, métrica, explicabilidade, coorte, detecção de anomalia ou monitoramento de modelo.",
        "cuidado": "Objetos diferentes respondem perguntas diferentes. Métrica, explicação, drift, causalidade e aprovação de produção não são equivalentes.",
    },
    "spark": {
        "titulo": "operações distribuídas e diagnósticos Spark",
        "intro": "Reúne helpers para datas, joins, nulos, amostragem, PSI, exibição segura e relações point-in-time sobre DataFrames Spark.",
        "quando": "Use quando a operação precisa permanecer distribuída ou quando cardinalidade, temporalidade e volume tornam inadequada uma solução puramente local.",
        "cuidado": "A API curta não elimina custo de shuffle, coleta ou join. Confira o plano, o grão e os efeitos de cada helper antes de escalar.",
    },
    "testing": {
        "titulo": "fixtures e dados sintéticos para testes e exemplos",
        "intro": "Contém geradores de dados sintéticos usados por notebooks e testes para exercitar contratos sem depender de dados reais do workspace.",
        "quando": "Use para exemplos reproduzíveis, testes de contrato e cenários controlados antes de envolver dados reais.",
        "cuidado": "Fixtures não representam distribuição real nem homologam comportamento em produção. Não confunda esta categoria com `hub_snippets/tests/`, que é a suíte interna de regressão.",
    },
    "visual": {
        "titulo": "componentes visuais, tema e composição",
        "intro": "Agrupa componentes de identidade visual, cards, divisores, cabeçalhos e temas usados para padronizar a apresentação dos notebooks e gráficos do Hub.",
        "quando": "Entre aqui quando o objetivo for composição visual, tema ou consistência de apresentação, e não cálculo estatístico ou transformação do dataset.",
        "cuidado": "A aparência não valida a análise. Mantenha separado o que é tema, o que é dado e o que é decisão de negócio.",
    },
}


def h1_description(readme: Path) -> str:
    for raw in readme.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("# "):
            continue
        title = line[2:].replace("`", "").strip()
        if " — " in title:
            return title.split(" — ", 1)[1].strip().rstrip(".")
        if " - " in title:
            return title.split(" - ", 1)[1].strip().rstrip(".")
        return title
    return readme.parent.name.replace("_", " ")


def objects(category: str) -> list[Path]:
    root = SNIPPETS / category
    out = []
    for child in sorted(root.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        readme = child / "README.md"
        if not readme.is_file():
            raise RuntimeError(f"objeto sem README em {category}: {child.name}")
        out.append(child)
    if not out:
        raise RuntimeError(f"categoria vazia: {category}")
    return out


def render(category: str) -> str:
    meta = CATEGORIES[category]
    items = objects(category)
    rows = []
    for child in items:
        desc = re.sub(r"\s+", " ", h1_description(child / "README.md"))
        rows.append(f"| [`{child.name}`]({child.name}/README.md) | {desc} | [guia local]({child.name}/README.md) |")
    note = ""
    if category == "testing":
        note = "\n> `hub_snippets/tests/` é infraestrutura interna de regressão e não faz parte deste catálogo de objetos.\n"
    return f"""# Categoria `{category}` — {meta['titulo']}

<!-- readme-categoria: 1.0.0 -->

{meta['intro']}

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais já validados; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

{meta['quando']}

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Papel resumido | Documentação |
|---|---|---|
{chr(10).join(rows)}
{note}
## Cuidados da categoria

{meta['cuidado']}

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** {len(items)} objeto(s) com README local encontrado(s) diretamente em `hub_snippets/{category}/`.
"""


def main() -> None:
    for category in CATEGORIES:
        target = SNIPPETS / category / "README.md"
        target.write_text(render(category), encoding="utf-8")
        print(f"{category}: {len(objects(category))} objetos -> {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
