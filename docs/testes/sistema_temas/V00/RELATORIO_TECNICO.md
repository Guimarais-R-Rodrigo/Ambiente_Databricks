# Resultado técnico V00

Estado da sprint: **CANDIDATA_PENDENTE_DE_AUDITORIA_E_ACEITE**.

Baseline: `8744157fe9c3e0603f689fb2bcad52445e96cb41`. Candidata executada: `8f0c732c37d29242ba74430e08d7fb268c632718`.

Gate técnico: **FAIL_OU_BLOQUEADO**. Não é aceite humano, auditoria independente ou publicação.

| Execução | Estado | Casos unittest reportados | Skips reportados |
|---|---|---:|---:|
| ci_base | PASS | 153 | 7 |
| publicador_visual_base | PASS | 29 | 0 |
| legado_base | PASS | 12 | 0 |
| captura_base | PASS | 0 | 0 |
| assets_v2_base | FAIL | 0 | 0 |
| figuras_base_top | PASS | 0 | 0 |
| figuras_base_snippets | PASS | 0 | 0 |
| figuras_base_scripts | PASS | 0 | 0 |
| figuras_base_skills | PASS | 0 | 0 |
| figuras_base_prompts | PASS | 0 | 0 |
| ci_candidata | PASS | 153 | 7 |
| publicador_visual_candidata | PASS | 29 | 0 |
| legado_candidata | PASS | 12 | 0 |
| captura_candidata | PASS | 0 | 0 |
| assets_v2_candidata | FAIL | 0 | 0 |
| figuras_candidata_top | PASS | 0 | 0 |
| figuras_candidata_snippets | PASS | 0 | 0 |
| figuras_candidata_scripts | PASS | 0 | 0 |
| figuras_candidata_skills | PASS | 0 | 0 |
| figuras_candidata_prompts | PASS | 0 | 0 |
| guardas_inventario | PASS | 27 | 0 |
| guardas_runner | PASS | 9 | 0 |

Contagens não incluem verificações sem unittest; não somar base e candidata como testes distintos.

Arquivos protegidos: 861. Diferenças: 0.
Capturas sintéticas iguais: True. Checkouts preservados durante os testes: True.

## Inventário automático

```json
{
  "arquivos": 1036,
  "camadas": {
    "governanca": 115,
    "derivado": 430,
    "produto": 430,
    "experimental": 19,
    "ferramenta": 42
  },
  "ocorrencias": 31340,
  "modulos_python": 444,
  "arquivos_com_ocorrencias": 488,
  "imagens": 102,
  "readmes_com_imagens": 15
}
```

## Pendências de saída

- Classificação semântica nominal por revisor independente.
- Capturas e teste de uso no Databricks; não há acesso de runtime nesta execução.
- Matriz de browsers, compute, ipywidgets, Apps e AI/BI autorizados.
- Leitura operacional por usuário novo e aceite de Rodrigo antes de V01.
- Reconciliar orientação do renderer geral em sprint documental pertinente.
- Resolver colisão da numeração ADR-0011 quando integrar R01; não mesclar automaticamente.
