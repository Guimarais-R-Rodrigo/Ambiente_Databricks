# Prompt: análise de safra/vintage

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe tabela e dicionário com
> **Add context**/`@`. Skill: `@hub-ml-analise-safra`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-analise-safra/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers) é o catálogo integrado.

## Pré-requisito crítico

Defina coorte, idade/maturação, numerador, denominador e censura. Não trate uma
definição analítica como exigência regulatória sem fonte normativa e revisão jurídica.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{DATASET}}` | Anexe painel ou nomeie a tabela. | Ancora a curva nos snapshots reais. | `@main.risco.vintage` |
| `{{ENTIDADE_E_CHAVE}}` | Defina contrato/entidade e chave estável. | Evita contar a mesma exposição várias vezes. | contrato; `id_contrato` |
| `{{COLUNA_SAFRA}}` | Informe data de originação/entrada. | Determina a coorte correta. | `dt_contratacao` |
| `{{MENSAL_SEMANAL_OUTRA}}` | Escolha frequência e calendário. | Muda MOB e comparabilidade. | mensal, mês civil |
| `{{COLUNAS_TEMPO}}` | Informe snapshot e idade observada. | Distingue célula ausente de zero. | `dt_snapshot`, `mob` |
| `{{EVENTO_E_REGRA}}` | Defina numerador e se é cumulativo. | Evita converter nulo em não-evento. | ever 30+ DPD até o MOB |
| `{{DENOMINADOR}}` | Defina exposição elegível por célula. | Controla maturidade e taxa. | contratos observados no MOB |
| `{{TAXA_SALDO_VALOR_CUMULATIVO}}` | Defina fórmula, unidade e acumulação. | Evita curva que cai indevidamente. | taxa cumulativa em % |
| `{{CENSURA_E_MATURIDADE}}` | Declare regra de célula completa. | Evita tratar imaturo como saudável. | somente snapshots observados |
| `{{SEGMENTOS_PERIODO}}` | Liste cortes e safras incluídas. | Torna comparação reproduzível. | produto; safras 2024–2026 |
| `{{FONTE_OFICIAL_OU_NAO_APLICAVEL}}` | Cite norma aplicável ou declare não aplicável. | Separa regra regulatória de política interna. | política interna v3 |
| `{{RESTRICOES}}` | Declare custo, PII e escrita. | Limita exposição e processamento. | somente leitura; dados agregados |

## Prompt pronto para colar

```text
Use @hub-ml-analise-safra para realizar análise de safra reproduzível e comparável,
com denominadores e maturação explícitos.

CONTEXTO
- Dataset: {{DATASET}}
- Entidade/contrato e chave: {{ENTIDADE_E_CHAVE}}
- Data de entrada na safra: {{COLUNA_SAFRA}}
- Frequência da safra: {{MENSAL_SEMANAL_OUTRA}}
- Data de observação e idade: {{COLUNAS_TEMPO}}
- Evento/numerador: {{EVENTO_E_REGRA}}
- Exposição/denominador: {{DENOMINADOR}}
- Métrica: {{TAXA_SALDO_VALOR_CUMULATIVO}}
- Censura/maturidade mínima: {{CENSURA_E_MATURIDADE}}
- Segmentos e período: {{SEGMENTOS_PERIODO}}
- Referência normativa, se houver: {{FONTE_OFICIAL_OU_NAO_APLICAVEL}}
- Restrições: {{RESTRICOES}}

FLUXO
1. Confirme granularidade, calendário, timezone e regra de entrada/saída da coorte.
2. Crie grade safra × idade, preservando células imaturas como não observáveis; não
   converta ausência de maturação em zero.
3. Calcule numerador, denominador e taxa por célula. Para acumulados, deduplicate
   eventos/entidades conforme a definição; não some taxas cumulativas.
4. Compare safras somente em idades equivalentes e destaque mix, exposição e volume.
5. Faça sanity checks de monotonicidade apenas quando a própria métrica exigir.
6. Use agregações Spark em alto volume, sem expor registros individuais.
7. Não grave tabela ou atribua conformidade normativa sem autorização e validação.

CONTRATO DE SAÍDA
- Dicionário formal da métrica e linha do tempo.
- Matriz safra × maturidade com volume, numerador, denominador e taxa.
- Curvas/heatmap, achados comparáveis e intervalos/alertas de baixo volume.
- Limitações por censura, composição e dados incompletos.
- Código reprodutível, se solicitado, e testes de reconciliação.

VALIDAÇÃO FINAL
- Reconcilie totais e entidades únicas.
- Confirme células imaturas, denominadores e duplicidade.
- Separe tendência observada, hipótese causal e afirmação normativa.
```

## Exemplo mínimo

Safra = mês da contratação; idade = meses desde contratação; evento = primeiro atraso
de 30+ dias; denominador = contratos ativos na origem; comparar até M6.

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

- “Compare safras somente até a maturidade comum.”
- “Audite o acumulado para evitar dupla contagem.”
- “Faça análise de mix antes de atribuir causa à piora.”
