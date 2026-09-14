from pathlib import Path
p=Path('CHANGELOG.md')
t=p.read_text(encoding='utf-8')
a='Template: `.claude/templates/changelog-entry.md`.\n\n'
e='## 2026-09-14 — pós-R13 D01–D04 (ChatGPT)\n\n- Documentação viva reconciliada com R00–R13 encerrada.\n- Sem alteração de implementação nem homologação Databricks.\n\n'
if e not in t:
    assert a in t
    t=t.replace(a,a+e,1)
p.write_text(t,encoding='utf-8')
