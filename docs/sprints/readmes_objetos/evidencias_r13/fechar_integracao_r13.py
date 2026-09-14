from pathlib import Path

BASE = "b0e953cc6274b385e42dcd675f2d8dbd145f349b"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f"substituicao nao unica em {path}: {text.count(old)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    Path("README.md"),
    "> **READMEs R13 — auditoria final candidata:** revisão consolidada de contrato, checklist, skill de criação, validador, Manual, READMEs, índices e espelho, com mutantes negativos e regressão local.",
    "> **READMEs R13 — integrada e encerrada:** a auditoria final foi aceita e integrada pelo PR #33 (`b0e953cc`), concluindo a iniciativa R00–R13 com 75/75 READMEs operacionais, 3/3 exemplares e 0 pendências estruturais.",
)

replace_once(
    Path("docs/sprints/readmes_objetos/README.md"),
    "O contrato vigente é **1.0.0**. A R12 foi aceita e integrada pelo PR nº 32 no commit `ec4b559d`, preservando **75/75 operacionais, 3/3 exemplares e 0 pendências** e acrescentando os seis índices funcionais de `hub_snippets`. A R13 é a auditoria final consolidada desta iniciativa.\n\nConsulte o [relatório R13](RELATORIO_R13.md), a [matriz de auditoria](MATRIZ_AUDITORIA_R13.md), os [achados](ACHADOS_R13.md) e as evidências em `evidencias_r13/`. A R13 verifica coerência, regressões e integridade local; não transforma testes locais em homologação Databricks, publicação no workspace ou auditoria independente.",
    "O contrato vigente é **1.0.0**. A R13 foi aceita e integrada pelo PR nº 33 no commit `b0e953cc`, encerrando a iniciativa R00–R13 em **75/75 operacionais, 3/3 exemplares e 0 pendências**, com seis índices funcionais de `hub_snippets` e auditoria final local aprovada.\n\nConsulte o [relatório R13](RELATORIO_R13.md), a [matriz de auditoria](MATRIZ_AUDITORIA_R13.md), os [achados](ACHADOS_R13.md) e as evidências em `evidencias_r13/`. O encerramento é documental e local: não equivale a auditoria independente, publicação no workspace ou homologação Databricks/Genie Code.",
)

report = Path("docs/sprints/readmes_objetos/RELATORIO_R13.md")
replace_once(report, "## Resultado técnico da candidata", "## Resultado técnico integrado")
replace_once(
    report,
    "O resultado técnico é preenchido pelas evidências geradas no freeze R13. Aprovação automática significa estrutura/coerência/regressões locais aprovadas; aceite humano continua sendo gate separado.",
    "O resultado técnico foi preenchido pelas evidências do freeze R13 e aceito pelo usuário. A R13 foi integrada pelo PR #33 no commit `b0e953cc6274b385e42dcd675f2d8dbd145f349b`. A aprovação continua limitada a estrutura, coerência e regressões locais; auditoria independente, publicação e homologação Databricks/Genie Code permanecem gates separados.",
)

sprints = Path("docs/sprints/README.md")
marker = "### READMEs R13 — encerramento da iniciativa"
text = sprints.read_text(encoding="utf-8")
if marker not in text:
    sprints.write_text(
        text.rstrip()
        + "\n\n"
        + marker
        + "\nA R13 foi aceita e integrada pelo PR #33 (`b0e953cc`). A iniciativa própria de READMEs R00–R13 está encerrada no Git com 75/75 objetos operacionais, 3/3 exemplares, 0 pendências e auditoria final local `A0_light` aprovada. Homologação Databricks/Genie Code e auditoria independente continuam fora deste fechamento.\n",
        encoding="utf-8",
    )

changelog = Path("CHANGELOG.md")
heading = "## 2026-09-13 — R13: integração e encerramento da iniciativa de READMEs (ChatGPT)"
text = changelog.read_text(encoding="utf-8")
if heading not in text:
    anchor = "Template: `.claude/templates/changelog-entry.md`.\n\n"
    entry = (
        heading
        + "\n\n- Integra o PR #33 no commit `b0e953cc`, após auditoria R13, mutantes negativos e CIs permanentes aprovados.\n"
        + "- Encerra a iniciativa R00–R13 em 75/75 READMEs operacionais, 3/3 exemplares e 0 pendências estruturais.\n"
        + "- Mantém explícitos os limites: revisão `A0_light`, sem auditoria independente, publicação ou homologação Databricks/Genie Code.\n\n"
    )
    if anchor not in text:
        raise RuntimeError("ancora do changelog ausente")
    changelog.write_text(text.replace(anchor, anchor + entry, 1), encoding="utf-8")
