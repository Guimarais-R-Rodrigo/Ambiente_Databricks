# Prompt: comparação controlada de tabelas

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Adicione as duas tabelas com **Add context**
> ou `@`. A skill adequada depende de o foco ser qualidade, EDA ou modelagem.

Não há uma skill única: use `@hub-ml-eda-profissional` para perfil/qualidade,
`@hub-ml-cross-eda-ml` para viabilidade de joins ou
`@hub-ml-monitoramento-modelo` para drift. Depois de escolher o objetivo, veja
os helpers declarados por essa skill em
[MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

A skill selecionada e sua [policy](../../hub_padroes/skill_enforcement/policy.json)
governam a execução. Uma checagem independente é alternativa antes da seleção;
não substitua a EDA protegida por SQL/helper direto depois de selecioná-la.

## Antes de usar

Defina se a comparação é de schema, conteúdo, reconciliação, migração, período ou
drift. Sem chaves comparáveis, peça primeiro uma análise de granularidade.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{TABELA_A}}` | Anexe ou nomeie a primeira versão. | Define o lado de referência. | `@main.silver.clientes_v1` |
| `{{TABELA_B}}` | Anexe ou nomeie a segunda versão. | Define o lado comparado. | `@main.silver.clientes_v2` |
| `{{TIPO_COMPARACAO}}` | Escolha schema, conteúdo, reconciliação ou migração. | Determina testes e tolerâncias. | reconciliação pós-migração |
| `{{GRANULARIDADE}}` | Defina o que uma linha representa em cada lado. | Evita comparar grãos diferentes. | cliente por mês |
| `{{CHAVES}}` | Liste correspondência e unicidade esperada. | Permite full join reconciliável. | `id_cliente, mes_ref` |
| `{{COL_DATA_E_PERIODO}}` | Defina coluna, janela e timezone. | Alinha populações comparadas. | `dt_ref`; 2026-07; UTC |
| `{{COLUNAS_CRITICAS_OU_TODAS}}` | Priorize colunas ou confirme todas. | Controla custo e materialidade. | saldo, status, segmento |
| `{{TOLERANCIAS_OU_PROPOR}}` | Informe tolerância por tipo ou peça proposta. | Evita falso alerta ou aceitação arbitrária. | saldo absoluto ≤ R$ 0,01 |
| `{{FILTROS}}` | Use filtros equivalentes e explícitos. | Impede diferença causada pela população. | ativos; excluir registros de teste |
| `{{RESTRICOES}}` | Declare PII, custo e escrita. | Limita inspeção e efeitos. | agregado; somente leitura |

## Prompt pronto para colar

```text
Compare os dois recursos anexados de modo reprodutível e somente leitura.

CONTEXTO
- Recurso A: {{TABELA_A}}
- Recurso B: {{TABELA_B}}
- Objetivo/tipo de comparação: {{TIPO_COMPARACAO}}
- Unidade de análise: {{GRANULARIDADE}}
- Chaves de correspondência: {{CHAVES}}
- Coluna temporal e período: {{COL_DATA_E_PERIODO}}
- Colunas críticas: {{COLUNAS_CRITICAS_OU_TODAS}}
- Tolerâncias: {{TOLERANCIAS_OU_PROPOR}}
- Filtros equivalentes: {{FILTROS}}
- Restrições: {{RESTRICOES}}

FLUXO
1. Verifique que A e B foram anexadas e confirme schemas, tipos e granularidade.
2. Compare cobertura temporal, contagens, chaves, duplicidade, colunas ausentes,
   mudanças de tipo, nulos e estatísticas relevantes.
3. Faça reconciliação por chave com categorias: somente A, somente B, iguais e
   divergentes. Antes, valide que o join não é muitos-para-muitos inesperado.
4. Para números, use tolerâncias absolutas/relativas explícitas; para timestamps,
   declare timezone e precisão; para strings, não normalize silenciosamente.
5. Em alto volume, use Spark SQL/PySpark, pruning e agregações. Não colete registros
   completos ao driver e não exponha valores sensíveis.
6. Não altere tabelas. Qualquer proposta de correção deve ficar separada da análise.

CONTRATO DE SAÍDA
- Veredito resumido: compatível, compatível com ressalvas ou incompatível.
- Matriz de diferenças de schema e scorecard de conteúdo.
- Métricas de reconciliação com numeradores, denominadores e taxas.
- Top diferenças priorizadas, causas prováveis marcadas como hipóteses.
- Código executável e parametrizado para repetir a comparação.
- Limitações e recomendação de aceite/rejeição sem tomar a decisão pelo usuário.

VALIDAÇÃO FINAL
- Confirme filtros idênticos e ausência de multiplicação pelo join.
- Inclua nulos nas comparações e explique tolerâncias.
- Declare contagens antes/depois e o escopo efetivamente lido.
```

## Exemplo mínimo

A = `@main.legacy.clientes`; B = `@main.silver.clientes`; chave = `id_cliente`;
tipo = reconciliação pós-migração; tolerância = 0,01 para saldo.

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Gere um teste automatizado de regressão a partir desta comparação.”
- “Investigue apenas as chaves divergentes, mantendo valores anonimizados.”
- “Proponha uma regra de aceite para a próxima carga.”
