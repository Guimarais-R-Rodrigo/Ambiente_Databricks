<!-- Template: célula %md PRÉ-código COMPACTO (skill hub-ml-comentar-notebook) -->

# Template: PRÉ-código Compacto

Usar quando o bloco for **simples e autoexplicativo** — configuração,
imports agrupados, definições auxiliares, leitura direta sem lógica
complexa.

**Critério**: usar introdução curta quando a intenção não for óbvia. Não comentar imports triviais nem código autoexplicativo; agrupar células consecutivas quando útil.

---

## Estrutura

```markdown
### Etapa [N] — [Nome curto]

**Objetivo**: [1 linha: o que o bloco faz e por quê.]
**Entradas**: [lista inline: `tabela_x`, parâmetro `y`.]
**Saída**: [DataFrame/tabela/efeito esperado.]
```

---

## Exemplo ilustrativo fictício

```markdown
### Etapa 1 — Configuração e Imports

**Objetivo**: Carregar a configuração visual autorizada e os parâmetros necessários à análise, se esse preparo precisar de contexto.
**Entradas**: Nenhuma (célula de setup).
**Saída**: Variáveis de configuração disponíveis para o restante do notebook.
```

---

## Quando usar este template

- Blocos de configuração (imports, widgets, constantes).
- Definição de funções auxiliares curtas.
- Leitura direta de tabela sem transformação (`spark.read.table(...)`).
- Etapas simples que recebem apenas Markdown PRÉ conforme o fluxo atual da skill.

## Quando NÃO usar (preferir template PRÉ completo)

- Bloco com lógica de negócio (joins, filtros, agregações).
- Bloco que gera métricas ou visualizações.
- Bloco de escrita Delta.
- Qualquer etapa que também receberá Markdown PÓS.

---

## Diferença de formato em relação ao PRÉ completo

| Elemento | PRÉ completo | PRÉ compacto |
| --- | --- | --- |
| Labels | `**Negrito**:` (7 campos) | `**Negrito**:` (3 campos) |
| Tamanho | 15–25 linhas | 3–5 linhas |
| Lógica técnica | Sim (detalhada) | Não |
| Pontos de atenção | Sim | Não |
| Funções/APIs | Sim | Não |
