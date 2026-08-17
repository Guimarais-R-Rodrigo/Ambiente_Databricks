---
name: hub-ml-comentar-notebook
description: Documenta notebooks Databricks com células `%md` antes e depois do código, explicando objetivo, entradas, lógica, resultado, impacto de negócio, riscos e próximo passo sem poluir o fluxo. Usar quando pedirem comentar, documentar, tornar didático, revisar narrativa ou adicionar Markdown a notebook PySpark, SQL, ML, EDA ou pipeline.
---

# Comentar notebooks Databricks

## Preservar o comportamento

Não alterar código, ordem de execução, parâmetros, resultados nem linguagem da célula sem pedido explícito. Inserir documentação somente onde ela reduz ambiguidade ou melhora a rastreabilidade.

## Ler antes de escrever

1. Identificar o objetivo global, os parâmetros, as tabelas de entrada e os artefatos de saída.
2. Mapear dependências entre células, estado de sessão e variáveis reutilizadas.
3. Separar transformação, validação, visualização e decisão.
4. Detectar células obsoletas, com erro ou sem saída; sinalizar sem inventar resultado.
5. Preservar segredos, PII e caminhos sensíveis; não reproduzi-los no Markdown.

## Escolher a densidade

- Inserir **PRÉ + PÓS** em transformações centrais, decisões, validações, treinos e resultados materiais.
- Inserir apenas **PRÉ curto** em preparação com intenção não óbvia.
- Agrupar células pequenas e consecutivas sob uma única introdução.
- Não comentar imports triviais, display exploratório isolado ou código autoexplicativo.

## Escrever a célula PRÉ

Incluir somente o necessário:

```markdown
%md
### Etapa — título orientado a ação

**Objetivo:** por que este bloco existe.
**Entradas:** tabelas, DataFrames, parâmetros e granularidade.
**Lógica:** transformação ou teste e suposições relevantes.
**Saída esperada:** nome, schema/granularidade e uso posterior.
**Atenção:** risco de custo, leakage, duplicidade ou qualidade, se aplicável.
```

## Escrever a célula PÓS

Usar valores realmente observados na saída. Se o notebook não tiver sido executado, marcar os campos como pendentes.

```markdown
%md
#### Resultado da etapa

- **Evidência:** métrica, contagem ou alteração observada.
- **Interpretação técnica:** o que o resultado sustenta e o que não sustenta.
- **Impacto de negócio:** consequência prática, quando houver contexto suficiente.
- **Risco remanescente:** limitação ou validação pendente.
- **Próximo passo:** ação concreta no fluxo.
```

Não transformar AUC em “percentual de acerto”, associação em causalidade ou SHAP em impacto percentual sem base matemática.

## Criar o cabeçalho

No início do notebook, registrar:

- objetivo e escopo;
- proprietário/equipe apenas se fornecido;
- entradas e saídas;
- parâmetros e data de corte;
- ambiente/catálogo/schema quando necessário;
- pré-requisitos, dependências e política de execução;
- limitações conhecidas.

Não prometer que a documentação reflete execução atual sem validar outputs.

## Usar os templates

Carregar conforme a necessidade:

- [templates/cabecalho_notebook.md](templates/cabecalho_notebook.md) para o início;
- [templates/bloco_markdown_pre_codigo.md](templates/bloco_markdown_pre_codigo.md) para bloco crítico;
- [templates/bloco_markdown_pre_compacto.md](templates/bloco_markdown_pre_compacto.md) para bloco simples;
- [templates/bloco_markdown_pos_codigo.md](templates/bloco_markdown_pos_codigo.md) para resultado material;
- [templates/bloco_markdown_pos_compacto.md](templates/bloco_markdown_pos_compacto.md) para confirmação curta.

Adaptar; não preencher placeholders com suposições.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md).

| Demanda | Módulo |
|---|---|
| Medir cobertura de documentação do notebook | `hub_scripts.doc_coverage` |
| Headers de seção, separadores e índice | `hub_snippets.visual.section_header`, `.divider`, `.index_generator` |
| Badges de status e KPI cards | `hub_snippets.visual.badge`, `hub_snippets.visual.kpi_card` |
| Números no padrão brasileiro | `hub_snippets.constants.format_br` |

Os helpers visuais escapam a entrada antes de renderizar HTML; montar HTML por concatenação manual para contornar o escape reintroduz risco de injeção. Documentação é conteúdo adicionado ao redor do código — nenhuma célula existente deve ser alterada.

## Validar a entrega

- Confirmar que cada Markdown descreve a célula adjacente correta.
- Remover repetições e seções vazias.
- Verificar que métricas e nomes batem com os outputs.
- Confirmar que links, âncoras e caracteres UTF-8 renderizam.
- Entregar o notebook comentado e um resumo separado das inconsistências técnicas encontradas.
