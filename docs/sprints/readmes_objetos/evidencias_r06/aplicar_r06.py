"""Aplica somente a integração editorial/transversal prevista na matriz R06.

O script é fail-closed: cada substituição exige uma única âncora. Ele não altera
implementações/fachadas e não renderiza o simulado; o workflow faz isso depois.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OBJECTS = ["arima_wrapper", "lgbm_temporal", "prophet_wrapper", "split_temporal", "walk_forward"]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    assert count == 1, (path, count, old[:120])
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before_once(path: str, marker: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    assert text.count(marker) == 1, (path, text.count(marker), marker[:120])
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
    # ARIMA — qualificar seleção automática e interpretações causais/estruturais.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/exemplo_arima_wrapper.py"
    replace_once(
        path,
        "# MAGIC **O problema.** Escolher (p, d, q) no olho leva a modelo que passa no teste e falha fora dele. E ARIMA aplicado a série não estacionária produz previsão que diverge com confiança.",
        "# MAGIC **O problema.** Escolher (p, d, q) sem protocolo explícito torna a comparação difícil. Não estacionariedade e diferenciação também precisam ser tratadas de acordo com a série e verificadas fora da amostra.",
    )
    replace_once(
        path,
        "# MAGIC **O que este helper faz.** Roda `auto_arima`, que busca a ordem por critério de informação e já resolve a diferenciação necessária.",
        "# MAGIC **O que este helper faz.** Roda `auto_arima`, que pesquisa uma especificação segundo o procedimento/configuração da biblioteca e pode selecionar diferenciação. A ordem escolhida continua sendo um candidato a validar fora da amostra.",
    )
    replace_once(
        path,
        "# MAGIC **Como ler.** A ordem escolhida é **(0, 1, 0)** — zero termos autorregressivos,\n# MAGIC **uma** diferenciação, zero médias móveis. Traduzindo: a busca concluiu que\n# MAGIC a melhor descrição desta série é \"passeio aleatório com deriva\", e que\n# MAGIC **não há estrutura a modelar** além da tendência.\n# MAGIC\n# MAGIC Está certo — foi assim que a série foi gerada. E é o resultado mais útil\n# MAGIC que o `auto_arima` pode dar, porque é o que ninguém escolheria à mão. Quem\n# MAGIC ajusta ordem no olho tende a pôr termos AR e MA \"para melhorar\", e cada um\n# MAGIC deles ajusta ruído.",
        "# MAGIC **Como ler.** Nesta execução a busca selecionou **(0, 1, 0)**: zero termos\n# MAGIC autorregressivos, uma diferenciação e zero médias móveis. Isso é a especificação\n# MAGIC escolhida pelo procedimento para esta amostra e este espaço de busca; não prova\n# MAGIC que o processo gerador real foi identificado nem que termos adicionais seriam\n# MAGIC necessariamente ruído. A coincidência com a forma usada para gerar este exemplo\n# MAGIC sintético é uma checagem didática, não uma garantia geral do método.",
    )
    replace_once(
        path,
        "# MAGIC - **Para horizonte longo.** O intervalo de confiança abre rápido; a partir de certo ponto ele cobre qualquer coisa e deixa de informar.",
        "# MAGIC - **Quando o horizonte excede a evidência disponível.** Incerteza tende a crescer com o horizonte; meça cobertura e erro por horizonte em backtest em vez de assumir um ponto universal de inutilidade.",
    )

    # lgbm_temporal — API atual não exige entidade e recusa duplicatas por padrão.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py"
    replace_once(
        path,
        "# MAGIC **O que este helper faz.** Cria features temporais exigindo a coluna de entidade, e derruba a ambiguidade em vez de assumir uma.",
        "# MAGIC **O que este helper faz.** Cria lags, rollings, calendário e tendência em pandas. `entity_cols` é opcional para série única; em painel, declará-la isola o histórico por entidade. O objeto não treina LightGBM apesar do nome legado.",
    )
    replace_once(
        path,
        "# MAGIC ## 3. Sem a entidade declarada — e o resultado parece melhor",
        "# MAGIC ## 3. Sem a entidade declarada — bloco histórico e política atual\n# MAGIC\n# MAGIC O código abaixo foi escrito antes da política atual de duplicatas. Hoje, com várias\n# MAGIC entidades na mesma data e `on_duplicate_dates='raise'` (default), a chamada sem\n# MAGIC `entity_cols` é recusada antes de produzir o resultado histórico. Para estudar\n# MAGIC conscientemente a sequência única com empates, seria necessário optar por\n# MAGIC `on_duplicate_dates='keep'`; o código executável e o output antigo são preservados\n# MAGIC aqui como evidência, não como receita vigente.",
    )
    replace_once(
        path,
        "# MAGIC - **Com o painel desordenado.** Lag pressupõe ordem; ordene por entidade e data antes.",
        "# MAGIC - **Com data que não possa ser normalizada ou grão temporal mal definido.** A implementação atual ordena internamente; o risco é fornecer data/grão sem semântica adequada, não deixar de pré-ordenar.",
    )

    # Prophet — métricas são in-sample e feriado em grão agregado precisa coincidir com a data.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/exemplo_prophet_wrapper.py"
    replace_once(
        path,
        "# MAGIC **O que este helper faz.** Ajusta Prophet com sazonalidade declarada e feriados do país, devolvendo previsão e componentes separados.",
        "# MAGIC **O que este helper faz.** Ajusta Prophet com sazonalidade declarada e calendário do país, devolvendo previsão, componentes e métricas in-sample. Em dados mensais, um feriado só entra pelo calendário nativo quando sua data coincide com a data representativa observada; não presuma efeito mensal automático.",
    )
    replace_once(
        path,
        "# MAGIC **Como ler.** O ajuste é bom: MAPE de **1,02%** sobre a própria amostra, e a\n# MAGIC previsão continua a subida da série com a ondulação anual no lugar certo.",
        "# MAGIC **Como ler.** O MAPE de **1,02%** descreve o ajuste **sobre a própria amostra**.\n# MAGIC Ele não estima o erro futuro. O `yhat` prolonga tendência/ciclo neste exemplo, mas\n# MAGIC a qualidade de forecast precisa ser medida em períodos que não participaram do fit.",
    )
    replace_once(
        path,
        "# MAGIC - **Em série curta.** Sem dois ciclos completos, a sazonalidade anual é chute com intervalo de confiança.",
        "# MAGIC - **Quando o histórico é curto para a sazonalidade proposta.** Poucos ciclos tornam a decomposição pouco sustentada; valide estabilidade em vez de usar dois ciclos como corte universal.",
    )
    replace_once(
        path,
        "# MAGIC - **Como caixa-preta de negócio.** O valor dele está nos componentes separados — tendência, sazonalidade, feriado. Olhar só o `yhat` desperdiça o método.",
        "# MAGIC - **Como narrativa causal de negócio.** Componentes ajudam a inspecionar o ajuste, mas não provam causas. Use `yhat` e componentes conforme a decisão, sempre com validação futura.",
    )

    # split_temporal — períodos observados, não linha de corte simples.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/exemplo_split_temporal.py"
    replace_once(
        path,
        "# MAGIC **O que este helper faz.** Corta por período de calendário, não por sorteio:\n# MAGIC tudo até uma data treina, tudo depois testa.",
        "# MAGIC **O que este helper faz.** Divide períodos observados em treino, validação e teste,\n# MAGIC com gaps opcionais. As proporções são sobre períodos únicos presentes na base, não\n# MAGIC sobre linhas nem sobre uma grade de calendário preenchida automaticamente.",
    )
    replace_once(
        path,
        "# MAGIC `temporal_split` separa por **período de calendário**, não por posição de\n# MAGIC linha, e aceita um intervalo de segurança (`gap_periods`) entre treino e\n# MAGIC teste — útil quando o target leva tempo para se materializar.",
        "# MAGIC `temporal_split` separa por **períodos observados**, não por posição de linha,\n# MAGIC e aceita `gap_periods` entre as partições. Esse gap pode representar maturação do\n# MAGIC target quando a quantidade configurada corresponde à latência real; buracos na\n# MAGIC série significam que um período observado não equivale necessariamente a uma\n# MAGIC unidade contínua de calendário.",
    )
    replace_once(
        path,
        "# MAGIC | Impedir que a mesma entidade caia nos dois lados | `group_col` | o modelo reconhece a entidade, não o padrão |",
        "# MAGIC | Avaliar apenas entidades novas entre partições | `group_col` | entidades vistas antes são removidas; em painel recorrente isso pode ser inadequado |",
    )

    # walk_forward — o callback é quem treina; gap é posição em períodos observados.
    path = "ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/exemplo_walk_forward.py"
    replace_once(
        path,
        "# MAGIC **O que este helper faz.** Roda validação que avança no tempo, retreinando a cada janela, com `gap` entre treino e teste.",
        "# MAGIC **O que este helper faz.** Cria janelas expansivas e chama `model_fn(train, test)` em cada uma, com `gap` opcional. O callback é quem precisa treinar/preprocessar somente no treino e devolver métricas.",
    )
    replace_once(
        path,
        "# MAGIC **Como ler.** O `gap` descarta os períodos entre treino e teste, e existe\n# MAGIC para um caso concreto: **quando o alvo demora a se realizar**. Se a\n# MAGIC inadimplência só é conhecida três meses depois da originação, treinar com\n# MAGIC dados até maio para prever junho usa rótulos que, em junho, ainda não\n# MAGIC existiriam.\n# MAGIC\n# MAGIC Sem `gap` a validação fica otimista e nada acusa: o número sai bom porque\n# MAGIC a informação vazou pela janela, não pela feature. É a forma de vazamento\n# MAGIC que sobrevive tanto ao `pit_join` quanto ao `split_temporal`.",
        "# MAGIC **Como ler.** O `gap` pula posições entre treino e teste e pode representar\n# MAGIC **maturação do alvo** quando configurado de acordo com a latência real. Aqui ele\n# MAGIC conta períodos observados; uma base com meses ausentes não transforma `gap=3`\n# MAGIC automaticamente em três meses corridos. Sem gap, a validação **pode** ficar\n# MAGIC otimista quando rótulos recentes ainda não estariam disponíveis no instante\n# MAGIC simulado. `pit_join` e `split_temporal` resolvem outros eixos e não escolhem\n# MAGIC essa latência por você.",
    )


def edit_shared_docs() -> None:
    # Catálogo narrativo.
    path = "ambiente_fonte/.assistant/hub_snippets/README.md"
    anchor = "#### 🕒 Engenharia Temporal e Séries Temporais\n"
    block = """#### 📘 Guias locais R06 — séries e validação temporal\n\nAntes de modelar uma série, separe as camadas: features, partição/backtest e modelo. Os guias locais R06 documentam os contratos atuais:\n\n- [ARIMA](ml/arima_wrapper/README.md) — candidato auto-ARIMA e métricas in-sample;\n- [Features temporais](ml/lgbm_temporal/README.md) — lags/rollings pandas; **não treina LightGBM**;\n- [Prophet](ml/prophet_wrapper/README.md) — tendência, sazonalidade, feriados e forecast;\n- [Split temporal](ml/split_temporal/README.md) — treino/validação/teste por períodos observados;\n- [Walk-forward](ml/walk_forward/README.md) — múltiplos folds expansivos por callback.\n\nOs cinco recursos são customizados pelo Hub, driver-side e executados explicitamente. Nenhum guia transforma métrica in-sample em validação futura nem aprova modelo para produção.\n\n"""
    insert_before_once(path, anchor, block)
    replace_once(
        path,
        "- **`lgbm_temporal`**: prepara atributos temporais e treina LightGBM com parâmetros declarados.\n  - *Quando usar:* em problemas temporais nos quais a disponibilidade histórica de cada atributo foi validada. LightGBM é dependência opcional; ausência do pacote impede esse fluxo.",
        "- **`lgbm_temporal`**: cria em pandas lags, estatísticas móveis, calendário e tendência; apesar do nome legado, a implementação atual não treina LightGBM.\n  - *Quando usar:* depois de definir grão, entidade e semântica temporal; `lag_n` conta observações anteriores e o processamento ocorre no driver.",
    )

    # Manual: rota para usuário iniciante antes do catálogo ML detalhado.
    path = "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
    anchor = "### 27.4. Modelagem, tempo, métricas e monitoramento\n\n"
    block = """### 27.4. Modelagem, tempo, métricas e monitoramento\n\n#### Guias locais R06 — como montar uma avaliação temporal sem misturar as camadas\n\nPara um usuário começando no Hub, a ordem conceitual recomendada é: **(1) construir features sem futuro → (2) definir partições/gaps → (3) avaliar em um ou vários cortes → (4) ajustar e comparar candidatos**. Os objetos R06 não formam um pipeline automático; cada um cobre uma parte:\n\n- `hub_snippets/ml/lgbm_temporal/README.md` — lags/rollings/calendário em pandas; não treina LightGBM;\n- `hub_snippets/ml/split_temporal/README.md` — um split treino/validação/teste por períodos observados;\n- `hub_snippets/ml/walk_forward/README.md` — vários folds expansivos; o callback faz o treino;\n- `hub_snippets/ml/arima_wrapper/README.md` — candidato auto-ARIMA; métricas retornadas são in-sample;\n- `hub_snippets/ml/prophet_wrapper/README.md` — candidato Prophet; atenção a feriados e grão agregado.\n\n`gap` e `gap_periods` não descobrem a maturação do target. Eles contam períodos observados da base e precisam ser configurados de acordo com o processo real. Métrica in-sample, validação temporal e teste final são evidências diferentes. Todos esses helpers operam no driver.\n\n"""
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    assert text.count(anchor) == 1 and "#### Guias locais R06" not in text
    p.write_text(text.replace(anchor, block, 1), encoding="utf-8")

    # Controle de migração: exatamente cinco R06/A.
    control_path = ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    data = json.loads(control_path.read_text(encoding="utf-8"))
    removed = {f"hub_snippets/ml/{obj}" for obj in OBJECTS}
    assert removed <= set(data["pending"]), removed - set(data["pending"])
    for key in sorted(removed):
        assert data["pending"][key] == {"sprint": "R06", "lote": "A"}, (key, data["pending"][key])
        data["pending"].pop(key)
    assert len(data["pending"]) == 32, len(data["pending"])
    control_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Índice da iniciativa.
    path = "docs/sprints/readmes_objetos/README.md"
    old = """O contrato vigente é **1.0.0**. A R04-B foi aceita e integrada pelo PR nº 18 no commit `d9da056`, já reconciliada com a V03 e com cinco CIs pós-merge verdes. A R05 documenta `lgbm_ranker`, `mlp_embeddings`, `optuna_lgbm`, `tabnet_wrapper`, `train_catboost` e `train_lgbm` sem alterar suas implementações/fachadas. A cobertura esperada é **38/75 operacionais e 3/3 exemplares, com 37 pendências**; a saída do validador da árvore fechada é a fonte de verdade. Isso não significa publicação no workspace nem aceite antecipado dos seis textos.\n\nConsulte o [relatório R05](RELATORIO_R05.md), a [matriz nominal](MATRIZ_ALTERACOES_R05.md) e os [achados](ACHADOS_R05.md). A próxima parada é a revisão desta leva antes da R06."""
    new = """O contrato vigente é **1.0.0**. A R05 foi aceita e integrada pelo PR nº 19 no commit `cae94988`, com CI geral e V00/V01/V02/V03 pós-merge verdes. A R06 documenta `arima_wrapper`, `lgbm_temporal`, `prophet_wrapper`, `split_temporal` e `walk_forward` sem alterar suas implementações/fachadas. A cobertura esperada é **43/75 operacionais e 3/3 exemplares, com 32 pendências**; somente a saída do validador da árvore fechada é fonte de verdade. Isso não significa publicação no workspace nem aceite antecipado dos cinco textos.\n\nConsulte o [relatório R06](RELATORIO_R06.md), a [matriz nominal](MATRIZ_ALTERACOES_R06.md) e os [achados](ACHADOS_R06.md). A próxima parada é a revisão desta leva antes da R07."""
    replace_once(path, old, new)
    replace_once(path, "[Matriz R05](MATRIZ_ALTERACOES_R05.md)", "[Matriz R06](MATRIZ_ALTERACOES_R06.md)")
    replace_once(path, "[Achados R05](ACHADOS_R05.md)", "[Achados R06](ACHADOS_R06.md)")
    replace_once(path, "[Relatório R05](RELATORIO_R05.md)", "[Relatório R06](RELATORIO_R06.md)")

    # Checkpoints aditivos: histórico anterior permanece intacto.
    append_once(
        "CLAUDE.md",
        "### Estado da migração de READMEs — R06",
        """### Estado da migração de READMEs — R06\nA R05 foi aceita e integrada na `main` em `cae94988`. A R06 documenta cinco objetos de séries/validação temporal sem alterar implementações/fachadas; consulte `docs/sprints/readmes_objetos/RELATORIO_R06.md`. Cobertura estrutural não é aceite editorial nem homologação.""",
    )
    append_once(
        "PLANO_HUB.md",
        "### Checkpoint R06 — séries e validação temporal",
        """### Checkpoint R06 — séries e validação temporal\nCinco objetos `hub_snippets/ml` recebem README local no contrato 1.0.0: ARIMA, features temporais, Prophet, split e walk-forward. A leva preserva implementações e pausa antes da R07 para revisão. Fonte: `docs/sprints/readmes_objetos/RELATORIO_R06.md`.""",
    )
    append_once(
        "docs/sprints/README.md",
        "### READMEs de objeto — R06",
        """### READMEs de objeto — R06\nA R05 está integrada em `cae94988`. A R06 cobre cinco objetos de séries/validação temporal e pausa para revisão antes da R07. Consulte `readmes_objetos/RELATORIO_R06.md` e `readmes_objetos/MATRIZ_ALTERACOES_R06.md`.""",
    )
    append_once(
        "README.md",
        "### Continuidade R06",
        """### Continuidade R06\n\nApós o aceite e merge da R05 pelo PR nº 19 (`cae94988`), a R06 documenta cinco objetos de séries e validação temporal. A candidata não altera implementações/fachadas e deve chegar a **43/75 READMEs operacionais**, com 32 pendências, sujeito ao validador. A leva pausa antes da R07 para revisão editorial.""",
    )

    # CHANGELOG aditivo.
    p = ROOT / "CHANGELOG.md"
    text = p.read_text(encoding="utf-8")
    heading = "## 2026-09-12 — R06: READMEs de séries e validação temporal (ChatGPT)"
    assert heading not in text
    entry = f"""{heading}\n\n- Documenta `{OBJECTS[0]}`, `{OBJECTS[1]}`, `{OBJECTS[2]}`, `{OBJECTS[3]}` e `{OBJECTS[4]}` no contrato 1.0.0.\n- Corrige somente prosa/backlinks dos cinco notebooks; código, magics executáveis e outputs históricos permanecem protegidos.\n- Corrige no catálogo o papel de `lgbm_temporal`: geração de features pandas, sem treino LightGBM.\n- Retira exatamente cinco dispensas R06 do controle de migração e registra achados, matriz, rubrica e testes.\n- Sem alteração de implementação/fachada, dependência permanente, publicação Databricks, auditoria independente ou início da R07.\n\n"""
    pos = text.index("## 2026-")
    p.write_text(text[:pos] + entry + text[pos:], encoding="utf-8")

    # Relatório conhece o run sem presumir sucesso.
    if os.environ.get("GITHUB_RUN_ID"):
        report = ROOT / "docs/sprints/readmes_objetos/RELATORIO_R06.md"
        text = report.read_text(encoding="utf-8")
        old = "**PENDENTE.** Esta seção será substituída apenas pelo fechamento remoto depois de gate, preservação e testes específicos concluírem. Falha em qualquer etapa impede a materialização da árvore final."
        new = f"Workflow de fechamento: **run {os.environ['GITHUB_RUN_ID']}**. Resultado ainda não presumido; a árvore só será materializada depois de gate, preservação e runtimes temporal/forecasting."
        assert text.count(old) == 1
        report.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    add_backlinks()
    edit_notebooks()
    edit_shared_docs()
    print("R06_PREPARADA")


if __name__ == "__main__":
    main()
