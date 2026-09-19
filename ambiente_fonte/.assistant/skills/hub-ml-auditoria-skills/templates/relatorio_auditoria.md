# Template — Relatorio de Auditoria de Output

> Usar este template para gerar o relatorio padronizado.
> Substituir placeholders `{...}` pelos valores reais.

---

## Cabecalho

```markdown
# Auditoria de Output — {nome_notebook}

| Campo | Valor |
|---|---|
| **Notebook auditado** | `{path_notebook}` |
| **Skill de origem** | `{nome_skill}` |
| **Data da auditoria** | {data_auditoria} |
| **Auditor** | hub-ml-auditoria-skills |
| **Celulas no output** | {n_celulas} ({n_code} code + {n_markdown} markdown) |
| **Linhas de codigo** | {n_linhas} |
```

---

## Matriz de Evidencia SEF

Preencher antes do score editorial quando houver enforcement/recursos declarados.

```markdown
## Matriz de Evidencia SEF

| Recurso | Citado | Localizado | Lido | Importado | Chamado | Concluido | Aplicabilidade | Fonte |
|---|---|---|---|---|---|---|---|---|
| {recurso} | SIM/NAO/NOT_OBSERVABLE | ... | ... | ... | ... | ... | APLICAVEL/NAO_APLICAVEL/NOT_OBSERVABLE | {celula/receipt/verifier} |

**Policy current_level:** {L0-L4}
**Policy target_level:** {L0-L4} — roadmap, nao prova implementacao
**Verifier independente executado?:** SIM/NAO
**Estado de canonical compliance:** {REVERIFICADO / ESTADO_PERSISTIDO_OBSERVADO / NOT_OBSERVABLE / NAO_APLICAVEL}
```

Nunca preencher um estado por heranca do anterior. Se o verifier nao foi executado, nao escrever “reverificado”.

---

## Score Consolidado

```markdown
## Score Consolidado: {score_final}/10 — {semaforo}

| Dimensao | Peso | Nota | Contribuicao |
|---|---|---|---|
| D1 Completude | 15% | {d1}/10 | {d1*0.15:.2f} |
| D2 Reprodutibilidade | 10% | {d2}/10 | {d2*0.10:.2f} |
| D3 Rigor Metodologico | 15% | {d3}/10 | {d3*0.15:.2f} |
| D4 Documentacao | 10% | {d4}/10 | {d4*0.10:.2f} |
| D5 Rastreabilidade | 10% | {d5}/10 | {d5*0.10:.2f} |
| D6 Governanca | 10% | {d6}/10 | {d6*0.10:.2f} |
| D7 Acionabilidade | 15% | {d7}/10 | {d7*0.15:.2f} |
| D8 Visual | 5% | {d8}/10 | {d8*0.05:.2f} |
| D9 Robustez | 5% | {d9}/10 | {d9*0.05:.2f} |
| D10 Ecossistema | 5% | {d10}/10 | {d10*0.05:.2f} |
| **TOTAL** | **100%** | — | **{score_final}/10** |
```

---

## Detalhamento por Dimensao

Para cada dimensao, usar este formato:

```markdown
### D{n} — {nome_dimensao} — {nota}/10

**Ancora de referencia:** {ancora_escolhida} (rubrica)

**Evidencias (OBJ):**
- {evidencia_objetiva_1}
- {evidencia_objetiva_2}

**Julgamento (JUL):**
- {avaliacao_qualitativa}

**Checkpoints skill-especificos:**
- [x] {checkpoint_atendido}
- [ ] {checkpoint_ausente} <-- GAP

**Justificativa da nota:**
{paragrafo_explicando_por_que_esta_nota_e_nao_outra}

**Para subir a nota:**
- {acao_concreta_para_melhorar}
```

---

## Checkpoints Skill-Especificos (D1)

```markdown
## Checkpoints: {nome_skill}

Etapas esperadas (extraidas do SKILL.md):

| # | Etapa | Presente? | Celula | Observacao |
|---|---|---|---|---|
| 1 | {etapa_1} | SIM/NAO | Cell {n} | {obs} |
| 2 | {etapa_2} | SIM/NAO | Cell {n} | {obs} |
| ... | ... | ... | ... | ... |

Cobertura: {presentes}/{total} = {percentual}%
```

---

## Semaforo e Veredito

```markdown
## Veredito Final

| Item | Valor |
|---|---|
| **Score** | {score_final}/10 |
| **Semaforo** | {emoji} {classificacao} |
| **Veto aplicado?** | {sim_nao} — {motivo_se_sim} |
| **Pronto para compartilhar?** | {sim_nao_condicional} |
```

---

## Prescricoes Priorizadas

```markdown
## Prescricoes (ordenadas por impacto no score)

| # | Prioridade | Dimensao | Gap | Acao | Esforco | Ganho estimado |
|---|---|---|---|---|---|---|
| 1 | ALTA | D{n} | {gap} | {acao} | {min} min | +{delta} pts |
| 2 | ALTA | D{n} | {gap} | {acao} | {min} min | +{delta} pts |
| 3 | MEDIA | D{n} | {gap} | {acao} | {min} min | +{delta} pts |
| ... | ... | ... | ... | ... | ... | ... |

**Score projetado apos correcoes ALTA:** {score_projetado}/10
```

---

## Radar Chart (opcional, recomendado)

Gerar grafico radar (Plotly) com as 10 dimensoes, mostrando visualmente
o perfil de qualidade do output. Usar tema institucional.

---

## Rodape

```markdown
---
*Auditoria gerada com `hub-ml-auditoria-skills`*
*Rubrica: `templates/rubrica_universal.md` | Contrato: `{skill_path}/SKILL.md`*
*Nota: scores de julgamento (JUL) refletem avaliacao tecnica do auditor.*
```
