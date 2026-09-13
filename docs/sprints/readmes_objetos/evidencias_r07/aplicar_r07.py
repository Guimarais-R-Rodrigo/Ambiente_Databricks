"""Aplica somente a integração editorial/transversal prevista na matriz R07.

Cada alteração depende de âncora única. O script não altera implementações nem
fachadas e não renderiza o simulado; o workflow faz isso depois.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OBJECTS = [
    "kaplan_meier",
    "score_bands",
    "scorecard_builder",
    "survival_cox",
    "vintage_analysis",
    "woe_iv_calculator",
]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    assert count == 1, (path, count, old[:160])
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before_once(path: str, marker: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    assert text.count(marker) == 1, (path, text.count(marker), marker[:160])
    p.write_text(text.replace(marker, block + marker, 1), encoding="utf-8")


def append_once(path: str, heading: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    assert heading not in text, (path, heading)
    p.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def add_backlinks() -> None:
    for obj in OBJECTS:
        path = f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/exemplo_{obj}.py"
        p = ROOT / path
        text = p.read_text(encoding="utf-8")
        marker = "\n# COMMAND ----------"
        assert marker in text and "Guia local completo:" not in text, obj
        intro = "\n# MAGIC\n# MAGIC **Guia local completo:** [README deste objeto](README.md)."
        p.write_text(text.replace(marker, intro + marker, 1), encoding="utf-8")


def edit_notebooks() -> None:
    # Kaplan-Meier: a censura entra no estimador, mas a figura local não a marca.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/exemplo_kaplan_meier.py"
    replace_once(
        path,
        "# MAGIC **Como ler.** As duas curvas descem, e a do premium desce mais devagar. O que\n# MAGIC vale reparar são os **degraus**: a curva só cai quando há evento, e fica\n# MAGIC plana entre eles. As marcas de censura aparecem sem produzir queda — o\n# MAGIC contrato sai do denominador sem contar como evento, que é exatamente o\n# MAGIC tratamento correto.",
        "# MAGIC **Como ler.** As duas curvas descem, e a do premium desce mais devagar. O que\n# MAGIC vale reparar são os **degraus**: a estimativa só cai quando há evento e fica\n# MAGIC plana entre eles. A censura entra corretamente no `KaplanMeierFitter`, mas\n# MAGIC **esta figura Plotly local não desenha marcas de censura**. Para auditar a\n# MAGIC cauda, confira também eventos/censurados e quantos casos ainda estão sob risco.",
    )
    replace_once(
        path,
        "# MAGIC χ² de **32,73** e p de **1,06 × 10⁻⁸**, a diferença entre padrão e premium\n# MAGIC não é acaso de amostra.",
        "# MAGIC χ² de **32,73** e p de **1,06 × 10⁻⁸**, há forte evidência contra a\n# MAGIC igualdade das curvas sob as hipóteses do teste. Isso não mede magnitude nem\n# MAGIC demonstra que pertencer ao grupo cause a diferença.",
    )

    # Score bands: a assinatura possui default True; aprovação acumulada é cobertura.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/score_bands/exemplo_score_bands.py"
    replace_once(
        path,
        "# MAGIC **O que este helper faz.** Gera bandas por quantil **exigindo** que a direção do score seja declarada.",
        "# MAGIC **O que este helper faz.** Gera bandas por quantil e ordena segundo `higher_score_is_better`. A API possui default `True`, mas em uso real a direção deve ser passada explicitamente para não depender de convenção implícita.",
    )
    replace_once(
        path,
        "# MAGIC O parâmetro não tem padrão silencioso de propósito. Um scorecard de crédito\n# MAGIC tradicional usa a convenção oposta: score alto é bom cliente.",
        "# MAGIC A implementação **tem** `higher_score_is_better=True` como default. Por isso,\n# MAGIC passe a direção explicitamente. Um scorecard de crédito tradicional pode usar\n# MAGIC a convenção de score alto = bom cliente, enquanto um score de risco pode inverter isso.",
    )
    replace_once(
        path,
        "# MAGIC Por isso a direção vale como informação a carregar junto do score, na\n# MAGIC documentação da tabela e no nome da coluna. `score_risco` e\n# MAGIC `score_qualidade` dizem sozinhos o que `score` não diz.",
        "# MAGIC Por isso a direção vale como informação a carregar junto do score, na\n# MAGIC documentação da tabela e no nome da coluna. `score_risco` e\n# MAGIC `score_qualidade` ajudam a reduzir ambiguidade. A coluna `aprovacao_acum` do\n# MAGIC helper é cobertura cumulativa da base ordenada; só vira aprovação real quando\n# MAGIC uma política/cutoff é efetivamente aplicada.",
    )

    # Scorecard: pontos favorecem rastreabilidade, mas odds não são chance.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/exemplo_scorecard_builder.py"
    replace_once(
        path,
        "# MAGIC cliente é a soma das faixas dele — aritmética que qualquer pessoa confere\n# MAGIC à mão. É essa a razão de o scorecard existir num setor regulado.",
        "# MAGIC cliente é a soma das faixas dele — aritmética que pode ser conferida\n# MAGIC manualmente. Isso melhora rastreabilidade, mas não substitui binning versionado,\n# MAGIC validação, governança, política de decisão ou aprovação regulatória quando aplicável.",
    )
    replace_once(
        path,
        "# MAGIC `base_score=600` com `base_odds=50` fixa a referência, e `pdo=20` diz\n# MAGIC quantos pontos dobram a chance.",
        "# MAGIC `base_score=600` com `base_odds=50` fixa a referência, e `pdo=20` diz\n# MAGIC quantos pontos dobram as **odds de referência**, não a probabilidade.",
    )
    replace_once(
        path,
        "# MAGIC Executado no laboratório, o resultado é:\n# MAGIC\n# MAGIC ```text",
        "# MAGIC Executado no laboratório, o bloco histórico abaixo é **abreviado**: o código\n# MAGIC imprime também as linhas de `tempo_woe`, mas o output colado antigo não as contém.\n# MAGIC O bloco é preservado como evidência histórica, não como schema completo do retorno.\n# MAGIC\n# MAGIC ```text",
    )

    # Cox: associação condicionada, métrica in-sample e não-rejeição do teste PH.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/exemplo_survival_cox.py"
    replace_once(
        path,
        "# MAGIC **O problema.** Kaplan-Meier compara grupos, e só. Para responder *quanto* a renda muda o risco de cancelamento, mantendo a idade constante, é preciso um modelo — e regressão comum não sabe o que fazer com censura.",
        "# MAGIC **O problema.** Kaplan-Meier compara curvas não ajustadas. Para estimar a associação entre renda e hazard de cancelamento condicionada às demais covariáveis do modelo, é preciso uma abordagem que também trate censura.",
    )
    replace_once(
        path,
        "# MAGIC O **C-index de 0,6848** é o contraponto necessário. Ele mede capacidade de\n# MAGIC ordenar quem falha antes, e 0,68 é modesto — os coeficientes estão certos e\n# MAGIC ainda assim o modelo prevê mal o caso individual. Efeito bem estimado e\n# MAGIC previsão boa são coisas diferentes, e confundi-las é como um modelo\n# MAGIC estatisticamente impecável vira uma decisão ruim.",
        "# MAGIC O **C-index de 0,6848** é calculado no próprio ajuste e mede ordenação de\n# MAGIC tempos/eventos nessa amostra. Não há corte universal que transforme 0,68 em\n# MAGIC `bom` ou `ruim`. Neste sintético, os coeficientes recuperam aproximadamente os\n# MAGIC parâmetros plantados, mas isso é diferente de demonstrar previsão individual\n# MAGIC fora da amostra.",
    )
    replace_once(
        path,
        "# MAGIC acima de 0,05 e nada é violado, o que era de esperar numa base gerada com\n# MAGIC efeito constante por construção.",
        "# MAGIC acima de 0,05 e o teste **não rejeita** proporcionalidade neste exemplo. Isso\n# MAGIC era esperado numa base gerada com efeito constante, mas p alto não prova que\n# MAGIC o pressuposto seja verdadeiro em dados reais.",
    )

    # Vintage: 30 dias é conveniência sintética, não definição de mês.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/exemplo_vintage_analysis.py"
    replace_once(
        path,
        "# MAGIC `dt_originacao` é a safra virada em data, e `dt_referencia` é a foto. O\n# MAGIC parâmetro `mob_col` diz que o MOB já está calculado — mas **não dispensa**\n# MAGIC `dt_referencia`, que continua obrigatório.",
        "# MAGIC `dt_originacao` é a safra virada em data, e `dt_referencia` é a foto. O\n# MAGIC parâmetro `mob_col` diz que o MOB já está calculado — mas **não dispensa**\n# MAGIC `dt_referencia`, que continua obrigatório. A célula abaixo fabrica `dt_ref` com\n# MAGIC `mob × 30 dias` apenas para satisfazer o exemplo sintético; como `mob_col` é\n# MAGIC fornecido, essa data não define o MOB e **30 dias não deve ser tratado como mês**.",
    )
    replace_once(
        path,
        "# MAGIC **Como ler.** Uma linha por safra × MOB. A taxa acumulada é a fração de\n# MAGIC contratos daquela safra que já tinham entrado em inadimplência **até**\n# MAGIC aquele MOB — e é por isso que ela nunca cai: uma vez inadimplente, o\n# MAGIC contrato não sai da conta.",
        "# MAGIC **Como ler.** Uma linha por safra × MOB. A taxa acumulada é a fração de\n# MAGIC contratos daquela safra que já tinham entrado em inadimplência **até**\n# MAGIC aquele MOB. O helper só publica essa taxa quando todos os contratos da safra\n# MAGIC estão observados naquele MOB; célula parcial fica `NaN`, não zero.",
    )

    # WOE/IV: IV alto é sinal de investigação, não diagnóstico automático de leakage.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/exemplo_woe_iv_calculator.py"
    replace_once(
        path,
        "# MAGIC O reflexo natural diante de um IV altíssimo é comemorar. Quase sempre é o\n# MAGIC contrário: significa que a variável **quase determina** o alvo, e isso\n# MAGIC costuma indicar vazamento.",
        "# MAGIC Um IV altíssimo merece investigação, não comemoração automática. Ele pode\n# MAGIC refletir leakage ou proxy do target, mas também concentração, bins muito\n# MAGIC específicos, seleção de amostra ou uma associação realmente forte no recorte.",
    )
    replace_once(
        path,
        "# MAGIC - **Com IV acima de 0,5, sem investigar.** Nessa faixa a hipótese mais\n# MAGIC   provável não é \"variável excelente\": é vazamento, ou variável derivada do\n# MAGIC   próprio alvo.",
        "# MAGIC - **Com IV acima de 0,5, sem investigar.** A faixa é uma heurística local,\n# MAGIC   não diagnóstico universal. Verifique leakage, origem, concentração, binning e\n# MAGIC   estabilidade antes de interpretar o valor como poder preditivo útil.",
    )
    replace_once(
        path,
        "# MAGIC - **Em variável contínua sem binning declarado.** O IV muda com o número de\n# MAGIC   faixas, e comparar IVs calculados com binnings diferentes não significa\n# MAGIC   nada.",
        "# MAGIC - **Em variável contínua sem binning declarado.** Este helper não cria bins;\n# MAGIC   valores distintos viram grupos. O IV depende da discretização, e comparar\n# MAGIC   resultados de regras de binning diferentes exige muito cuidado.",
    )


def edit_shared_docs() -> None:
    # Catálogo narrativo do Hub.
    path = "ambiente_fonte/.assistant/hub_snippets/README.md"
    marker = "#### 📊 Risco de Crédito e Scorecards\n"
    block = """#### 📘 Guias locais R07 — score, safra e sobrevivência\n\nEstes seis guias cobrem três perguntas diferentes: **como o score organiza risco**, **como coortes amadurecem** e **como analisar tempo até evento com censura**. Não misture as escalas:\n\n- [Kaplan–Meier](ml/kaplan_meier/README.md) — sobrevivência não ajustada e log-rank;\n- [Bandas de score](ml/score_bands/README.md) — quantis, evento e cobertura cumulativa;\n- [Scorecard](ml/scorecard_builder/README.md) — WOE + coeficientes em escala de pontos;\n- [Cox PH](ml/survival_cox/README.md) — hazard ratios condicionais e teste de proporcionalidade;\n- [Vintage](ml/vintage_analysis/README.md) — safra × MOB com maturidade observada;\n- [WOE/IV](ml/woe_iv_calculator/README.md) — separação por faixa em Spark; binning é externo.\n\nOs guias não definem política de crédito, causalidade, regulação ou cutoff. Cada contrato precisa ser validado no problema real antes de virar decisão.\n\n"""
    insert_before_once(path, marker, block)

    # Manual: guia R07 imediatamente antes da ficha Kaplan-Meier.
    path = "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
    marker = "#### `hub_snippets.ml.kaplan_meier`\n"
    block = """#### Guias locais R07 — score, maturidade e sobrevivência\n\nPara um usuário novo no Hub, separe as perguntas antes de escolher o objeto:\n\n- `hub_snippets/ml/score_bands/README.md` — diagnosticar como eventos se distribuem ao longo do score; `aprovacao_acum` é cobertura, não política pronta;\n- `hub_snippets/ml/woe_iv_calculator/README.md` — WOE/IV de uma feature **já discretizada** em Spark;\n- `hub_snippets/ml/scorecard_builder/README.md` — converter WOE + coeficientes em tabela de pontos; não aplica binning nem pontua linhas novas;\n- `hub_snippets/ml/vintage_analysis/README.md` — comparar safras no mesmo MOB sem preencher maturidade ausente;\n- `hub_snippets/ml/kaplan_meier/README.md` — descrever tempo até evento com censura;\n- `hub_snippets/ml/survival_cox/README.md` — associações de hazard ajustadas sob riscos proporcionais.\n\nTaxa acumulada de safra, função de sobrevivência, probabilidade de evento, hazard, odds e pontos são grandezas diferentes. Os helpers organizam cálculos; eles não escolhem política, causalidade ou aprovação regulatória.\n\n"""
    insert_before_once(path, marker, block)

    # Controle de migração: exatamente seis objetos R07/A.
    control_path = ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    data = json.loads(control_path.read_text(encoding="utf-8"))
    removed = {f"hub_snippets/ml/{obj}" for obj in OBJECTS}
    assert removed <= set(data["pending"]), removed - set(data["pending"])
    for key in sorted(removed):
        assert data["pending"][key] == {"sprint": "R07", "lote": "A"}, (key, data["pending"][key])
        data["pending"].pop(key)
    assert len(data["pending"]) == 26, len(data["pending"])
    control_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Índice da iniciativa: R06 integrada, R07 candidata.
    path = "docs/sprints/readmes_objetos/README.md"
    old = """O contrato vigente é **1.0.0**. A R05 foi aceita e integrada pelo PR nº 19 no commit `cae94988`, com CI geral e V00/V01/V02/V03 pós-merge verdes. A R06 documenta `arima_wrapper`, `lgbm_temporal`, `prophet_wrapper`, `split_temporal` e `walk_forward` sem alterar suas implementações/fachadas. A cobertura esperada é **43/75 operacionais e 3/3 exemplares, com 32 pendências**; somente a saída do validador da árvore fechada é fonte de verdade. Isso não significa publicação no workspace nem aceite antecipado dos cinco textos.\n\nConsulte o [relatório R06](RELATORIO_R06.md), a [matriz nominal](MATRIZ_ALTERACOES_R06.md) e os [achados](ACHADOS_R06.md). A próxima parada é a revisão desta leva antes da R07."""
    new = """O contrato vigente é **1.0.0**. A R06 foi aceita e integrada pelo PR nº 20 no commit `289731c`, com CI geral e V00/V01/V02/V03 pós-merge verdes. A R07 documenta `kaplan_meier`, `score_bands`, `scorecard_builder`, `survival_cox`, `vintage_analysis` e `woe_iv_calculator` sem alterar suas implementações/fachadas. A cobertura esperada é **49/75 operacionais e 3/3 exemplares, com 26 pendências**; somente a saída do validador da árvore fechada é fonte de verdade. Isso não significa publicação no workspace nem aceite antecipado dos seis textos.\n\nConsulte o [relatório R07](RELATORIO_R07.md), a [matriz nominal](MATRIZ_ALTERACOES_R07.md) e os [achados](ACHADOS_R07.md). A próxima parada é a revisão desta leva antes da R08."""
    replace_once(path, old, new)
    replace_once(path, "[Matriz R06](MATRIZ_ALTERACOES_R06.md)", "[Matriz R07](MATRIZ_ALTERACOES_R07.md)")
    replace_once(path, "[Achados R06](ACHADOS_R06.md)", "[Achados R07](ACHADOS_R07.md)")
    replace_once(path, "[Relatório R06](RELATORIO_R06.md)", "[Relatório R07](RELATORIO_R07.md)")

    # Checkpoints aditivos.
    append_once(
        "CLAUDE.md",
        "### Estado da migração de READMEs — R07",
        """### Estado da migração de READMEs — R07\nA R06 foi aceita e integrada na `main` em `289731c`. A R07 documenta seis objetos de score, vintage e sobrevivência sem alterar implementações/fachadas; consulte `docs/sprints/readmes_objetos/RELATORIO_R07.md`. Cobertura estrutural não é aceite editorial, política de crédito nem homologação.""",
    )
    append_once(
        "PLANO_HUB.md",
        "### Checkpoint R07 — score, vintage e sobrevivência",
        """### Checkpoint R07 — score, vintage e sobrevivência\nSeis objetos `hub_snippets/ml` recebem README local no contrato 1.0.0: Kaplan–Meier, bandas de score, scorecard, Cox PH, vintage e WOE/IV. A leva preserva implementações e pausa antes da R08 para revisão. Fonte: `docs/sprints/readmes_objetos/RELATORIO_R07.md`.""",
    )
    append_once(
        "docs/sprints/README.md",
        "### READMEs de objeto — R07",
        """### READMEs de objeto — R07\nA R06 está integrada em `289731c`. A R07 cobre seis objetos de score, vintage e sobrevivência e pausa para revisão antes da R08. Consulte `readmes_objetos/RELATORIO_R07.md` e `readmes_objetos/MATRIZ_ALTERACOES_R07.md`.""",
    )
    append_once(
        "README.md",
        "### Continuidade R07",
        """### Continuidade R07\n\nApós o aceite e merge da R06 pelo PR nº 20 (`289731c`), a R07 documenta seis objetos de score, vintage e sobrevivência. A candidata não altera implementações/fachadas e deve chegar a **49/75 READMEs operacionais**, com 26 pendências, sujeito ao validador. A leva pausa antes da R08 para revisão editorial.""",
    )

    # CHANGELOG aditivo, sem reescrever histórico.
    p = ROOT / "CHANGELOG.md"
    text = p.read_text(encoding="utf-8")
    heading = "## 2026-09-12 — R07: READMEs de score, vintage e sobrevivência (ChatGPT)"
    assert heading not in text
    entry = f"""{heading}\n\n- Documenta `{OBJECTS[0]}`, `{OBJECTS[1]}`, `{OBJECTS[2]}`, `{OBJECTS[3]}`, `{OBJECTS[4]}` e `{OBJECTS[5]}` no contrato 1.0.0.\n- Corrige somente prosa/backlinks dos seis notebooks; código, magics executáveis e outputs históricos permanecem protegidos.\n- Explicita limites de censura, hazard, score/odds/PDO, maturidade de safra e WOE/IV, sem transformar heurísticas em normas.\n- Retira exatamente seis dispensas R07 do controle de migração e registra achados, matriz, rubrica e testes.\n- Sem alteração de implementação/fachada, dependência permanente, publicação Databricks, homologação de política/modelo, auditoria independente ou início da R08.\n\n"""
    pos = text.index("## 2026-")
    p.write_text(text[:pos] + entry + text[pos:], encoding="utf-8")

    # O relatório passa a conhecer o run sem presumir o resultado.
    if os.environ.get("GITHUB_RUN_ID"):
        report = ROOT / "docs/sprints/readmes_objetos/RELATORIO_R07.md"
        text = report.read_text(encoding="utf-8")
        old = "**Pendente de freeze remoto nesta versão de autoria.** O relatório só deve ser promovido a fechamento técnico depois de registrar run, versões, contagem de testes, cobertura validada e árvore exata materializada."
        new = f"Workflow de fechamento: **run {os.environ['GITHUB_RUN_ID']}**. Resultado ainda não presumido; a árvore só será materializada depois de gate, preservação e runtime R07."
        assert text.count(old) == 1
        report.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    add_backlinks()
    edit_notebooks()
    edit_shared_docs()
    print("R07_PREPARADA")


if __name__ == "__main__":
    main()
