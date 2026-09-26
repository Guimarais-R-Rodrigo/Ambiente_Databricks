# Regra — Fonte de verdade e camadas

- Este repositório git é a **única fonte canônica**. Workspaces Databricks (Free e
  trabalho) são cópias operacionais: nunca traga mudança feita lá de volta sem
  registrá-la aqui primeiro.
- `ambiente_fonte/` é o único lugar onde o produto (`.assistant_instructions.md` +
  `.assistant/`) é editado.
- `Novo_Ambiente_Simulado/` é **derivado**: gerado por `tools/render_simulado.py`.
  Nunca edite à mão; se divergir do fonte, apague e regenere.
- `Ambiente_Antigo/` é referência congelada local (read-only). Qualquer
  melhoria vai para `ambiente_fonte/`.
- Mudança de comportamento do produto exige, na mesma sessão: validação
  (`tools/validate_assistant.py`), re-render, entrada no `CHANGELOG.md` e, se for
  decisão estrutural, ADR em `docs/decisions/`.
