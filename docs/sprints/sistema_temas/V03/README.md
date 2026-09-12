# V03 — integração explícita do núcleo com Plotly

> **ACEITA POR RODRIGO · INTEGRAÇÃO GIT AUTORIZADA · 12/09/2026.** A V02 está aceita e integrada. A V03 acrescenta uma rota opt-in para Plotly e preserva os gráficos existentes por padrão. O PR #16 registra a efetivação do merge; este texto, isoladamente, não prova integração nem publicação.

## Para quem nunca entrou no Hub

Se você já usa `aplicar_tema(fig, ...)`, continue usando exatamente como hoje. A V03 não exige trocar código antigo nem escolher um novo tema. A nova rota existe para quando você quiser testar conscientemente uma configuração completa validada pelo núcleo V02.

A ordem segura é: obter/resolver uma configuração de notebook → aplicar à figura com a nova função → conferir visualmente → fazer ajustes específicos depois. Não registre template global para experimentar uma única figura.

O aceite desta sprint não publica nada no Databricks. Se a rota V03 vier a ser usada em um ambiente publicado no futuro, Plotly e as dependências de validação declaradas em `hub_snippets/requirements-temas.txt` precisam estar disponíveis; nenhuma função instala pacotes automaticamente.

## Escopo

A V03 conecta `hub_snippets.visual.tema.ResolvedTheme` ao helper `hub_snippets.visual.theme_plotly`. O adaptador consome somente tokens que o contrato 0.1.0 atribui ao Plotly: cor/tamanho de texto, título, paleta categórica, dimensões, margens e estilo do rodapé. Alinhamento de título, legenda e template-base continuam políticas fixas do adaptador porque ainda não são tokens configuráveis.

## Compatibilidade

As APIs legadas `get_tema_eda()`, `aplicar_tema(fig, subtitulo, fonte, n)` e `registrar_template_plotly()` permanecem com as mesmas assinaturas e comportamento observado. O novo caminho é aditivo:

- `get_tema_plotly(theme)` — produz configuração Plotly sem alterar sessão;
- `aplicar_tema_resolvido(fig, theme, ...)` — aplica explicitamente à figura e devolve o mesmo objeto;
- `registrar_template_plotly_resolvido(theme, *, nome, ativar=False, substituir=False)` — registra no namespace `hub-*`; só muda o default da sessão com `ativar=True` e recusa substituir um nome já ativo quando a ativação não é explícita.

## Fail-closed

A V03 aceita somente um `ResolvedTheme` íntegro do contexto `notebook`. Dicionário cru, resultado adulterado, contexto editorial/apresentação e modos `dark`/`high_contrast` são recusados nesta sprint. Os dois últimos continuam válidos no contrato, mas ainda faltam tokens de superfície do gráfico para uma aplicação Plotly completa sem inventar defaults implícitos.

Se um template `hub-*` já participa do default ativo, sozinho ou dentro de uma composição como `plotly+hub-*`, `substituir=True` com `ativar=False` é recusado antes da troca do objeto. Substituir esse nome exige assumir explicitamente o efeito global com `ativar=True`.

## O que não muda

Dados dos traces, títulos/ranges dos eixos e cores explicitamente definidas nos traces não são reescritos pelo adaptador. O simples import não altera `pio.templates.default`. A V03 não migra `correlation_matrix`, `distribution_grid`, curvas de ML ou qualquer consumidor existente; essas migrações precisam de decisão e testes próprios.

## Aceite técnico

Os critérios técnicos da candidata foram satisfeitos antes do aceite de Rodrigo: testes V03 e regressões V00/V01/V02 verdes; fixture `legado_notebook` equivalente ao layout legado; assinaturas antigas preservadas; aplicação nova sem alteração de dados/eixos/cores explícitas; efeitos de sessão opt-in; documentação/espelho sincronizados; CI transversal verde; code review final sem novo achado.

A ratificação do aceite é revalidada novamente antes do merge. O estado efetivo de integração e os SHAs finais pertencem ao PR #16 e à `main`, não a uma afirmação antecipada deste README.

## Limites

Sem publicação Databricks, sem alteração visual automática, sem homologação de Spark/widgets/Apps/AI-BI, sem V04/V05 e sem aprovação de qualquer fixture como tema operacional. Auditoria independente e avaliação com usuário iniciante continuam gates separados.

[Checkpoint](CHECKPOINT_V03.md) · [Testes](TESTES.md) · [V02](../V02/README.md)
