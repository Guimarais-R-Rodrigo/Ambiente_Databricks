# V03 — integração explícita do núcleo com Plotly

> **EM DESENVOLVIMENTO · NÃO INTEGRADA · 12/09/2026.** A V02 está aceita e integrada. Esta sprint acrescenta uma rota opt-in para Plotly; não muda gráficos existentes automaticamente.

## Para quem nunca entrou no Hub

Se você já usa `aplicar_tema(fig, ...)`, continue usando exatamente como hoje. A V03 não exige trocar código antigo nem escolher um novo tema. A nova rota existe para quando você quiser testar conscientemente uma configuração completa validada pelo núcleo V02.

A ordem segura é: obter/resolver uma configuração de notebook → aplicar à figura com a nova função → conferir visualmente → fazer ajustes específicos depois. Não registre template global para experimentar uma única figura.

## Escopo

A V03 conecta `hub_snippets.visual.tema.ResolvedTheme` ao helper `hub_snippets.visual.theme_plotly`. O adaptador consome somente tokens que o contrato 0.1.0 atribui ao Plotly: cor/tamanho de texto, título, paleta categórica, dimensões, margens e estilo do rodapé. Alinhamento de título, legenda e template-base continuam políticas fixas do adaptador porque ainda não são tokens configuráveis.

## Compatibilidade

As APIs legadas `get_tema_eda()`, `aplicar_tema(fig, subtitulo, fonte, n)` e `registrar_template_plotly()` permanecem com as mesmas assinaturas e comportamento observado. O novo caminho é aditivo:

- `get_tema_plotly(theme)` — produz configuração Plotly sem alterar sessão;
- `aplicar_tema_resolvido(fig, theme, ...)` — aplica explicitamente à figura e devolve o mesmo objeto;
- `registrar_template_plotly_resolvido(theme, *, nome, ativar=False, substituir=False)` — registra no namespace `hub-*`; só muda o default da sessão com `ativar=True` e recusa substituir um nome já ativo quando a ativação não é explícita.

## Fail-closed

A V03 aceita somente um `ResolvedTheme` íntegro do contexto `notebook`. Dicionário cru, resultado adulterado, contexto editorial/apresentação e modos `dark`/`high_contrast` são recusados nesta sprint. Os dois últimos continuam válidos no contrato, mas ainda faltam tokens de superfície do gráfico para uma aplicação Plotly completa sem inventar defaults implícitos.

## O que não muda

Dados dos traces, títulos/ranges dos eixos e cores explicitamente definidas nos traces não são reescritos pelo adaptador. O simples import não altera `pio.templates.default`. A V03 não migra `correlation_matrix`, `distribution_grid`, curvas de ML ou qualquer consumidor existente; essas migrações precisam de decisão e testes próprios.

## Critérios de aceite técnico

A candidata só pode ser apresentada para aceite se: testes V03 e regressões V00/V01/V02 estiverem verdes; a fixture `legado_notebook` produzir exatamente o layout legado; chamadas antigas preservarem assinatura; a nova aplicação não alterar dados/eixos/cores explícitas; efeitos de sessão forem opt-in; documentação e espelho estiverem sincronizados; CI transversal passar sem relaxar guardas.

## Limites

Sem publicação Databricks, sem alteração visual automática, sem homologação de Spark/widgets/Apps/AI-BI, sem V04/V05 e sem aprovação de qualquer fixture como tema operacional.

[Checkpoint](CHECKPOINT_V03.md) · [Testes](TESTES.md) · [V02](../V02/README.md)
