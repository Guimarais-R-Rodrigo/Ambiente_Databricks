# Prompt: validação estatística pré-modelagem

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe dataset, notebook e desenho
> experimental com **Add context**/`@`. Skill: `@rodrigo-validacao-estatistica`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Antes de usar

Declare se o objetivo é diagnóstico preditivo, inferência/estimativa ou experimento.
Esses objetivos exigem pressupostos e interpretações diferentes.

## Prompt pronto para colar

```text
Use @rodrigo-validacao-estatistica para avaliar se o método pretendido é adequado ao
desenho e aos dados anexados. Não transforme automaticamente um teste significativo
em causalidade ou relevância prática.

BRIEFING
- Dataset/recurso: {{DATASET}}
- Unidade, chave e grupos repetidos: {{GRANULARIDADE_CHAVE_GRUPOS}}
- Target/desfecho e tipo: {{TARGET}}
- Objetivo: {{PREDICAO_INFERENCIA_EXPERIMENTO}}
- Método pretendido: {{METODO}}
- População, amostra e seleção: {{POPULACAO_AMOSTRA}}
- Tempo, horizonte e split: {{TEMPO_HORIZONTE_SPLIT}}
- Hipóteses primária/secundárias: {{HIPOTESES}}
- Alfa, potência/MDE e correção múltipla: {{CRITERIOS_OU_PROPOR}}
- Volume: {{VOLUME}}
- Restrições/dependências: {{RESTRICOES}}
- Modo: {{DIAGNOSTICO_CODIGO_OU_EXECUCAO_AUTORIZADA}}

FLUXO
1. Confirme desenho, unidade independente, mecanismo de amostragem e disponibilidade
   temporal. Identifique pseudorreplicação, leakage e seleção pós-tratamento.
2. Mapeie cada pergunta a estimando, método, pressupostos e diagnóstico. Não execute
   uma bateria indiscriminada de testes.
3. Avalie tamanho de efeito e incerteza, não apenas p-valor. Quando houver múltiplas
   comparações, proponha correção e diferencie análise confirmatória de exploratória.
4. Em grandes volumes, evite testes que detectam efeitos irrelevantes só pelo N;
   combine relevância prática, gráficos e amostra computacional quando apropriado.
5. Em séries/tempo, preserve ordem e avalie dependência/estacionariedade conforme o
   método. Em grupos/entidades repetidas, use validação ou erros compatíveis.
6. Não alegue causalidade sem desenho de identificação e pressupostos defensáveis.

SEGURANÇA E CUSTO
- Faça somente leitura; não exponha PII nem exemplos de linhas identificáveis.
- Explique dependências antes de instalar bibliotecas ou executar análise pesada.
- Aguarde autorização para executar; código proposto deve ser reprodutível e ter seed.

CONTRATO DE SAÍDA
- Pergunta, estimando, método e pressupostos em uma matriz.
- Diagnósticos com evidências, tamanho de efeito e incerteza.
- Resultado interpretado em linguagem de negócio, sem extrapolação indevida.
- Código/testes somente no nível solicitado.
- Limitações, ameaças à validade e decisão técnica recomendada.

VALIDAÇÃO FINAL
- Confirme direção do target e unidades.
- Declare tratamento de nulos/outliers e todas as exclusões.
- Separe significância estatística, relevância prática e poder preditivo.
```

## Exemplo mínimo

Objetivo = inferência; método = diferença de conversão A/B; unidade = cliente;
hipótese = campanha aumenta conversão em 2 p.p.; critérios = alfa 5%, teste bilateral
e IC 95%.

## Follow-ups úteis

- “Faça uma análise de sensibilidade dos pressupostos mais frágeis.”
- “Converta o diagnóstico em testes reproduzíveis sem executar.”
- “Explique por que o resultado não sustenta causalidade, se aplicável.”
