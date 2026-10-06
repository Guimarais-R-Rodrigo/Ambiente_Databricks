# Proveniência documental — snippets e temas

Registro de manutenção de 06/10/2026. Os trechos abaixo foram preservados da baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040` ao separar o percurso de uso da história de construção. São transcrições históricas, não instruções vigentes nem reexecuções. Estados de falha, restrições e resultados continuam limitados ao contexto original. O código, policy, schema e células executáveis não foram alterados por esta revisão textual. A referência operacional de tokens possui mudança documental e testes próprios.

O procedimento administrativo atual do App está em [Deploy e rollback](../../guias/temas/DEPLOY_ROLLBACK_APP.md). O ponteiro curto no pacote preserva compatibilidade do bundle; não autoriza deploy.

## 1. ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md

Origem: [R0074, linha 3](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md#L3). Conteúdo original:

````text
> **PADRÃO TRANSVERSAL DO HUB · V02–V10 INTEGRADAS NO GIT; V11 EM CANDIDATA.** Não é um novo tipo de objeto,
> configuração ativa de todos os notebooks nem autorização para alterar temas no workspace. Consumo, autoria e projeção continuam opt-in; nada muda silenciosamente na rotina legada.

Para começar, abra o [guia operacional](GUIA_OPERACIONAL.md). Para corrigir uma
mensagem, consulte [Erros e recuperação](ERROS.md). Para implementar um consumidor,
leia o [objeto `visual.tema`](../../hub_snippets/visual/tema/README.md). Para a ponte AI/BI V11 candidata, use o [guia AI/BI](aibi/GUIA_PRIMEIRO_USO.md).

**Estado vigente no Git:** V02 integrou o núcleo de carga/validação/resolução; V03 o adaptador Plotly; V04 componentes HTML/tabela; V05 o Visual Lab de autoria; V06 a geração editorial orientada por tema; V07 consumidores runtime e formatos exercitados; V08 alinhou as superfícies transversais; V09 integrou o contrato mínimo de temas ao kit de transição; V10 integrou a superfície Databricks App `authoring_only`. `ResolvedTheme` permanece a fonte efetiva para consumo configurável e as APIs legadas continuam o default. A V11 está sendo desenvolvida separadamente como ponte fail-closed para capacidades de temas nativos AI/BI, sem alterar o schema central, sem aceite/merge e sem operação no workspace. Integração Git não equivale a publicação, homologação visual/runtime, acessibilidade ou aprovação de uma identidade.
````

## 2. ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md

Origem: [R0074, linha 14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md#L14). Conteúdo original:

````text
`theme.schema.json` é a fonte ativa dos campos e limites. Seus bytes foram
movidos da candidata V01 sem alterar o contrato 0.1.0; o título histórico dentro
do JSON foi preservado deliberadamente. O arquivo anterior foi removido da V01,
e o verificador de manutenção aponta a esta fonte, em vez de manter dois schemas.
A [referência de tokens](TOKENS.md) é gerada, nunca editada manualmente.

Os quatro arquivos em `exemplos/` são cópias derivadas das fixtures históricas
V01, verificadas por testes. Não devem ser editados independentemente nem usados
como sinal de aprovação de uma marca. Preservam o legado e exemplos contratuais;
para uma proposta, use uma cópia em memória ou em sua pasta autorizada.
````

## 3. ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md

Origem: [R0074, linha 59](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md#L59). Conteúdo original:

````text
A V10 integrada possui dependências próprias de interface em `databricks_app/requirements.txt`; isso não altera as dependências do núcleo nem faz Streamlit virar requisito de quem apenas importa `hub_snippets.visual.tema`. A V11 não adiciona Databricks SDK/REST/CLI: a projeção e o binder trabalham somente com objetos/bytes locais e recusam inventar o schema nativo de `Import theme`.

Leia o [guia operacional](GUIA_OPERACIONAL.md) antes de executar o exemplo.
A [coleção de padrões](../README.md) e o [Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers)
continuam sendo as entradas gerais. A publicação e sua homologação são gates
separados; V00–V10 integradas no Git e a existência de uma candidata V11 não oferecem, por si só, comando ou autorização para alterar tema de workspace, importar tema ou publicar dashboard.
````

## 4. ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/README.md

Origem: [R0075, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/README.md#L1). Conteúdo original:

````text
# AI/BI theme bridge — V11

## O que é

Esta pasta contém a ponte V11 entre o Sistema de Temas do Hub e os temas nativos de dashboards Databricks AI/BI.

A fonte de verdade **continua sendo `ResolvedTheme`**. A V11 não cria um segundo tema canônico, não transforma `context="aibi"` em contexto suportado pelo schema V01/V02 e não altera o núcleo de resolução. Em vez disso, uma configuração `notebook` íntegra é projetada para uma matriz explícita de capacidades AI/BI.
````

## 5. ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/README.md

Origem: [R0075, linha 44](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/README.md#L44). Conteúdo original:

````text
A homologação em workspace, browser, permissões reais, acessibilidade e UAT permanecem gates posteriores.
````

## 6. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md

Origem: [R0076, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md#L1). Conteúdo original:

````text
# Databricks App V10 — gestão visual do Hub

Este diretório contém a superfície **Databricks App** da V10 do Sistema de Temas. Ela reutiliza o núcleo V02 e o Visual Lab V05 para experimentar e persistir sessões de autoria de temas de contexto `notebook`. **O App não aprova, promove nem publica temas.**
````

## 7. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md

Origem: [R0076, linha 62](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md#L62). Conteúdo original:

````text
## 6. Identidade e papéis

O App não possui seletor de papel. A política canônica continua em `docs/sprints/sistema_temas/V01/politica_workflow.json` com `leitor`, `proponente`, `aprovador`, `publicador` e `mantenedor`.

Nesta V10, a instância de autoria deve ser disponibilizada pelo administrador somente aos grupos reais mapeados para `proponente` e/ou `mantenedor`. A interface não consulta nem grava grupos corporativos, não aceita `role=...` do navegador e não transforma acesso ao App em aprovação.

A ausência de identidade encaminhada bloqueia o App. O fallback de identidade só existe quando `HUB_THEME_LOCAL_DEV=true` e exige `HUB_THEME_LOCAL_USER_ID`, exclusivamente para desenvolvimento/teste local.
````

## 8. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md

Origem: [R0076, linha 136](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md#L136). Conteúdo original:

````text
## 12. Execução local

A execução local é apenas desenvolvimento. Prepare uma pasta temporária e use um usuário sintético:

```powershell
$env:HUB_THEME_LOCAL_DEV = "true"
$env:HUB_THEME_LOCAL_USER_ID = "usuario-teste"
$env:HUB_THEME_VOLUME = "C:\temp\hub-theme-v10"
streamlit run app.py
```

A pasta precisa existir. Nunca use esse modo como evidência de autenticação Databricks ou de persistência em Unity Catalog.
````

## 9. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md

Origem: [R0076, linha 164](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/README.md#L164). Conteúdo original:

````text
## 14. Implantação e retorno

O repositório não envia este App ao workspace automaticamente. `tools/temas_v10_app.py` gera um bundle derivado em `.artifacts/`, contendo App + dependências canônicas necessárias. O procedimento autorizado está em [DEPLOY_ROLLBACK.md](DEPLOY_ROLLBACK.md).

Rollback do **App** significa voltar a uma versão anterior do código/bundle validado. Isso não apaga sessões do Volume. Rollback de **tema publicado** não pertence a esta V10 porque o App não publica temas.

## 15. Referências e próximos gates

- [Guia de primeiro uso](GUIA_PRIMEIRO_USO.md)
- [Deploy e rollback](DEPLOY_ROLLBACK.md)
- [`app.py`](app.py)
- [`app_service.py`](app_service.py)
- [`app.yaml`](app.yaml)
- [Visual Lab V05](../../../hub_snippets/visual/theme_lab/README.md)
- [Contrato de identidade visual](../README.md)
- Matriz de papéis V10: `docs/sprints/sistema_temas/V10/MATRIZ_PAPEIS.json` no repositório.

A V10 candidata não equivale a deploy, UAT, acessibilidade ou publicação. V11/AI-BI não é iniciada por este diretório.
````

## 10. ambiente_fonte/.assistant/hub_snippets/README.md

Origem: [R0124, linha 59](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/README.md#L59). Conteúdo original:

````text
Cada snippet mantém o núcleo executável de três componentes abaixo. Cada objeto operacional inclui também `README.md`, a camada humana de conceito e escolha. A migração estrutural foi encerrada na R13:
````

## 11. ambiente_fonte/.assistant/hub_snippets/README.md

Origem: [R0124, linha 110](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/README.md#L110). Conteúdo original:

````text
**Núcleo de temas integrado no Git:** [`visual.tema`](visual/tema/README.md) confere configurações completas e isoladas. V03 conecta Plotly por opt-in e V04 estende a rota explícita a HTML/estilos/tabela pandas; consumidores legados permanecem o default e nenhuma dessas integrações publica ou homologa aparência no Databricks.
````

## 12. ambiente_fonte/.assistant/hub_snippets/README.md

Origem: [R0124, linha 131](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/README.md#L131). Conteúdo original:

````text
Antes de modelar uma série, separe as camadas: features, partição/backtest e modelo. Os guias locais R06 documentam os contratos atuais:
````

## 13. ambiente_fonte/.assistant/hub_snippets/README.md

Origem: [R0124, linha 167](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/README.md#L167). Conteúdo original:

````text
A R08 separa quatro tarefas que costumam ser misturadas: **criar clusters**, **descrevê-los**, **projetá-los para visualização** e **explicar modelos/pontuar anomalias**:
````

## 14. ambiente_fonte/.assistant/hub_snippets/README.md

Origem: [R0124, linha 501](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/README.md#L501). Conteúdo original:

````text
A migração estrutural está concluída: os 52 snippets operacionais possuem README local. Para descobrir recursos, use os seis índices de categoria: [constants](constants/README.md), [display](display/README.md), [ml](ml/README.md), [spark](spark/README.md), [testing](testing/README.md) e [visual](visual/README.md). Cada índice enumera os filhos reais da categoria e aponta para o guia do objeto.
````

## 15. ambiente_fonte/.assistant/hub_snippets/constants/colors/README.md

Origem: [R0126, linha 76](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/colors/README.md#L76). Conteúdo original:

````text
Saída do trecho portátil conferido nesta sprint: `#005CA9 10`. Para preparar a importação, siga a [coleção](../../README.md); não presuma um caminho de usuário diferente do ambiente confirmado.
````

## 16. ambiente_fonte/.assistant/hub_snippets/constants/colors/README.md

Origem: [R0126, linha 88](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/colors/README.md#L88). Conteúdo original:

````text
Pelo cálculo de contraste da WCAG, texto branco sobre `COR_ALERTA` apresenta aproximadamente **1,73:1** e sobre `COR_POSITIVO`, **2,04:1**, abaixo de 4,5:1 para texto comum. A conferência foi numérica, não uma auditoria visual completa. Os valores não foram alterados nesta sprint. A [WCAG 2.2](https://www.w3.org/TR/WCAG22/#contrast-minimum) contém o critério e suas exceções; [uso da cor](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) exige que informação não dependa apenas dela.
````

## 17. ambiente_fonte/.assistant/hub_snippets/constants/colors/README.md

Origem: [R0126, linha 110](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/colors/README.md#L110). Conteúdo original:

````text
Revisão R03-A: leitura de implementação, fachada e exemplo; testes portáteis e cálculo de contraste. O notebook Databricks não foi reexecutado, e não houve auditoria independente ou alteração de paleta.
````

## 18. ambiente_fonte/.assistant/hub_snippets/constants/emojis/README.md

Origem: [R0127, linha 77](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/emojis/README.md#L77). Conteúdo original:

````text
O trecho portátil foi conferido nesta sprint. Imprimir o aviso não executa a revisão sugerida.
````

## 19. ambiente_fonte/.assistant/hub_snippets/constants/emojis/README.md

Origem: [R0127, linha 109](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/emojis/README.md#L109). Conteúdo original:

````text
Revisão R03-A: código, fachada, notebook e testes portáteis. A leitura dos mapas foi exercitada; não houve execução de EDA, homologação Databricks ou auditoria independente.
````

## 20. ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md

Origem: [R0128, linha 73](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md#L73). Conteúdo original:

````text
Esses casos são verificáveis pelo código mínimo e pelos testes locais da R02. São saídas textuais, não valores destinados a nova aritmética. Pontos-base (*basis points*, `bps`) representam centésimos de ponto percentual; um ponto percentual corresponde a 0.01 na escala de fração.
````

## 21. ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md

Origem: [R0128, linha 94](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md#L94). Conteúdo original:

````text
O bloco foi executado localmente nesta sprint, com a raiz do Hub adicionada ao caminho Python. O [notebook](exemplo_format_br.py) expande a explicação das escalas; sua execução no Databricks não foi presumida a partir desse teste local. Não é necessário alterar `locale` nem escrever tabela para usar o helper.
````

## 22. ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md

Origem: [R0128, linha 108](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md#L108). Conteúdo original:

````text
Na execução local da R02, `fmt_int(9007199254740993)` produziu `9.007.199.254.740.992`, perdendo uma unidade. `fmt_n` sem sufixo teve o mesmo resultado. Esse limite foi documentado, não corrigido no código nesta sprint. Para precisão integral, preserve o inteiro e use uma representação sem conversão para ponto flutuante. A [especificação de formatação do Python](https://docs.python.org/3/library/string.html#format-specification-mini-language) explica os tipos de apresentação.
````

## 23. ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md

Origem: [R0128, linha 128](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md#L128). Conteúdo original:

````text
Contrato e exemplos conferidos no código da base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. A referência externa pertinente é a [documentação oficial de Decimal](https://docs.python.org/3/library/decimal.html), consultada em 12/09/2026, para `quantize` e `ROUND_HALF_UP`. As convenções de saída do Hub são definidas pelo próprio módulo.

Revisão R02 pelo próprio autor, com execução do bloco Python acima e casos de borda em Python 3.13.5. Isso não é uma execução do notebook Databricks. Revisão independente e aceite humano do piloto têm estados próprios no relatório da sprint.
````

## 24. ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md

Origem: [R0129, linha 5](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md#L5). Conteúdo original:

````text
> CSS descreve como um elemento aparece. O módulo preserva as constantes legadas e, na V04, também materializa estilos a partir de um `ResolvedTheme` recebido explicitamente; ele continua sem reestilizar o Hub de forma global.
````

## 25. ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md

Origem: [R0129, linha 24](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md#L24). Conteúdo original:

````text
O módulo também fornece `FONT_FAMILY`. Não contém um arquivo de fonte nem instala tipografia. Na V04, badges, divisores, KPI cards, cabeçalhos, índice e tabela pandas consomem este módulo **somente nas novas rotas `_resolvido`**. As rotas legadas continuam usando constantes compatíveis e não são reestilizadas por carregar um tema.
````

## 26. ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md

Origem: [R0129, linha 80](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md#L80). Conteúdo original:

````text
### Caminho V04 — tema explícito
````

## 27. ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md

Origem: [R0129, linha 101](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md#L101). Conteúdo original:

````text
A V04 elimina a duplicação no **caminho resolvido** dos componentes cobertos, que passam a pedir estilos a `get_styles_resolvidos`. O caminho legado permanece congelado por compatibilidade e não deve ser confundido com um tema global ou folha de estilo de aplicação.
````

## 28. ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md

Origem: [R0129, linha 125](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md#L125). Conteúdo original:

````text
Revisão R03-A: análise estática dos consumidores, testes portáteis e contraste numérico. Não houve mudança de CSS, homologação no workspace ou auditoria independente.
````

## 29. ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/README.md

Origem: [R0131, linha 5](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/README.md#L5). Conteúdo original:

````text
> **Atualização V07 — estado atual.** `plot_correlation` e
> `plot_correlation_matrix` continuam sendo as rotas legadas. Para aplicar um
> `ResolvedTheme` notebook/light de forma opt-in, use
> `plot_correlation_resolvido` ou `plot_correlation_matrix_resolvido`. A rota
> temática usa `palette.diverging` somente na escala de cor; seleção de colunas,
> descarte de faltantes, cálculo Spark, método e `strong_pairs` permanecem na
> mesma implementação. Um tema inválido falha antes do cálculo.
````

## 30. ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/README.md

Origem: [R0131, linha 94](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/README.md#L94). Conteúdo original:

````text
Para explorar a figura no notebook, use `fig.show()`. O [notebook didático](exemplo_correlation_matrix.py) configura o import pelo usuário da sessão e preserva uma falha histórica de execução no laboratório. Essa transcrição não é resultado novo nem prova de incompatibilidade em todo ambiente. O helper lê os dados e coleta a matriz; não grava tabelas.
````

## 31. ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/README.md

Origem: [R0131, linha 130](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/README.md#L130). Conteúdo original:

````text
A procedência do comportamento específico é a [implementação local](correlation_matrix.py), lida na base `c60f1e5`. Os casos reproduzíveis desta sprint ficam nas evidências R03-B do repositório. Conferência de cálculo e geração de figura não equivalem a teste visual no workspace. Revisão própria de ChatGPT; não houve auditoria independente.
````

## 32. ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md

Origem: [R0132, linha 90](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md#L90). Conteúdo original:

````text
### Caminho V04 — tabela com tema explícito
````

## 33. ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md

Origem: [R0132, linha 100](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md#L100). Conteúdo original:

````text
A rota V04 usa `brand.primary` no cabeçalho, `table.header_text` no texto do cabeçalho e `semantic.negative` no realce de negativos. O DataFrame, `highlight_cols` e `format_dict` mantêm o contrato histórico. A fonte da tabela permanece fixa porque o contrato V01 não atribui `font.family` a esse consumidor.
````

## 34. ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md

Origem: [R0132, linha 134](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md#L134). Conteúdo original:

````text
O comportamento do Hub foi confrontado com [código](dataframe_styled.py), [API](__init__.py) e exemplo na base `c60f1e5`. Testes R03-B verificam conteúdo HTML e preservação dos dados; isso não homologa a renderização visual no Databricks. Autorrevisão de ChatGPT, sem auditoria independente.
````

## 35. ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/README.md

Origem: [R0133, linha 5](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/README.md#L5). Conteúdo original:

````text
> **Atualização V07 — estado atual.** As rotas legadas `plot_distributions` e
> `plot_distribution_grid` permanecem disponíveis. Para aparência derivada de um
> `ResolvedTheme`, use `plot_distributions_resolvido` ou
> `plot_distribution_grid_resolvido`. O tema é validado antes da amostragem;
> `smart_sample`, conversão para pandas, colunas e valores dos histogramas não têm
> uma segunda implementação. A V07 não transforma a amostra em evidência da
> população inteira nem homologa a renderização no browser Databricks.
````

## 36. ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/README.md

Origem: [R0133, linha 133](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/README.md#L133). Conteúdo original:

````text
A interpretação do contrato local se apoia em [distribution_grid.py](distribution_grid.py) e [smart_sample.py](../../spark/smart_sample/smart_sample.py), lidos na base `c60f1e5`. Evidências R03-B distinguem construção/cálculo de homologação visual e Databricks. Revisão própria, sem auditoria independente.
````

## 37. ambiente_fonte/.assistant/hub_snippets/spark/date_features/README.md

Origem: [R0166, linha 139](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/date_features/README.md#L139). Conteúdo original:

````text
O comportamento descrito foi conferido em `date_features.py`, `__init__.py` e no notebook desta pasta, sobre a base integrada da R04-A. As funções de calendário são APIs PySpark; o contrato local, os nomes e a lista fixa são definidos pelo Hub. A documentação atual do Databricks para `to_date` registra que entrada malformada levanta erro com ANSI habilitado e recomenda `try_cast(... AS DATE)` quando a intenção é retornar `NULL` em vez de falhar.

Nesta revisão houve leitura estática e testes sintéticos próprios da sprint. Teste local sem PySpark e teste de runtime Spark são registrados separadamente no relatório R04-A; não há publicação Databricks nem auditoria independente implícita.
````

## 38. ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/README.md

Origem: [R0167, linha 140](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/README.md#L140). Conteúdo original:

````text
A R04-A registra testes sintéticos com Spark separadamente do gate estrutural. Não há benchmark de escala, publicação Databricks ou auditoria independente nesta entrega.
````

## 39. ambiente_fonte/.assistant/hub_snippets/spark/null_summary/README.md

Origem: [R0168, linha 125](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/README.md#L125). Conteúdo original:

````text
A R04-A caracteriza casos de limiar e execução Spark em testes próprios. Isso não converte os defaults em política de negócio nem implica publicação no Databricks ou revisão independente.
````

## 40. ambiente_fonte/.assistant/hub_snippets/spark/pit_join/README.md

Origem: [R0169, linha 123](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/README.md#L123). Conteúdo original:

````text
Contrato conferido na base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. A [documentação de point-in-time joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series), consultada em 12/09/2026, sustenta o conceito, não a equivalência deste helper ao serviço. A [referência de limitações serverless](https://docs.databricks.com/aws/en/compute/serverless/limitations), na mesma data, delimita o ambiente; não é uma homologação do código.

A redação inicial e a revisão de fechamento R02 são técnicas e didáticas pelo próprio autor. A [execução suplementar da R02 em 12/09/2026](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982) exercitou este helper com PySpark 4.0.1 real, incluindo elegibilidade temporal, empate, janela e preservação de fatos repetidos. O ambiente local do fechamento não possui PySpark; essa evidência anterior não foi apresentada como reexecução local. Ela não equivale a execução do notebook no Databricks, teste de escala, Spark Connect ou auditoria independente.
````

## 41. ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/README.md

Origem: [R0170, linha 127](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/README.md#L127). Conteúdo original:

````text
Os índices e limiares apresentados são mecanismos de monitoramento, não padrões Databricks. A R04-A registra execução sintética Spark em evidência própria; sem publicação, dados reais ou auditoria independente.
````

## 42. ambiente_fonte/.assistant/hub_snippets/spark/safe_display/README.md

Origem: [R0171, linha 122](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/README.md#L122). Conteúdo original:

````text
A R04-A testa o helper com renderer injetado e Spark local no runner. Isso não é benchmark nem homologação da interface Databricks.
````

## 43. ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/README.md

Origem: [R0172, linha 126](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/README.md#L126). Conteúdo original:

````text
A R04-A executa casos sintéticos com Spark no runner e registra skips locais separadamente. Não há inferência de representatividade estatística, benchmark ou homologação Databricks.
````

## 44. ambiente_fonte/.assistant/hub_snippets/testing/fixtures/README.md

Origem: [R0174, linha 125](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/README.md#L125). Conteúdo original:

````text
Revisão R03-A: leitura completa do módulo, fachada e notebook. Os testes da sprint distinguem geração em Spark real de inspeção estática; versões e resultados ficam nas evidências. Não foi executado o notebook no Databricks nem validada uma carteira real.
````

## 45. ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md

Origem: [R0176, linha 24](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md#L24). Conteúdo original:

````text
O caminho legado fornece `badge_status`, `badge_score` e `badge_inline`. A V04 acrescenta as variantes `_resolvido`, que mudam somente a apresentação quando recebem um tema explícito. O módulo não é um motor de qualidade de dados: `badge_status` recebe o estado escolhido e `badge_score` continua usando os mesmos limites fixos.
````

## 46. ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md

Origem: [R0176, linha 78](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md#L78). Conteúdo original:

````text
### Caminho V04 — badge com tema explícito
````

## 47. ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md

Origem: [R0176, linha 88](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md#L88). Conteúdo original:

````text
Os cortes de `badge_score` não viram tokens e não mudam na V04. Apenas `status.*`, superfície informativa e dimensões do badge são materializados pelo tema. Um tipo desconhecido continua caindo no estilo informativo.
````

## 48. ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md

Origem: [R0176, linha 100](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md#L100). Conteúdo original:

````text
O estilo `warn` usa texto `#B26A00` sobre `#FFF8E1`, com contraste calculado próximo de **3,99:1**, inferior a 4,5:1 para texto comum; a fonte declarada é de 11px. A [WCAG](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) orienta a avaliação. Não declare o componente plenamente acessível; as cores permaneceram intactas nesta migração.

Na rota V04, cores e dimensões de estado vêm de `constants.styles` materializado a partir do tema; a rota legada preserva os valores históricos. O escape de HTML não anonimiza conteúdo: mensagens ainda podem expor dados se o autor os inserir.
````

## 49. ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md

Origem: [R0176, linha 122](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md#L122). Conteúdo original:

````text
Revisão R03-A: testes portáteis de cortes, arredondamento, fallback, escape e contraste. Não houve alteração de CSS ou política, execução do notebook no Databricks ou auditoria independente.
````

## 50. ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md

Origem: [R0177, linha 84](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md#L84). Conteúdo original:

````text
### Caminho V04 — divisória com tema explícito
````

## 51. ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md

Origem: [R0177, linha 98](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md#L98). Conteúdo original:

````text
As funções legadas preservam seus estilos históricos. Na V04, as variantes `_resolvido` usam `constants.styles`: `divider.light`, `divider.medium` e `brand.primary` chegam do tema validado. Nenhuma delas cria mecanismo de atualização global. Mantenha os títulos mesmo quando a linha parecer suficiente.

## 12. Quais são as alternativas?

Títulos e espaço em branco podem resolver a organização sem separadores. `---` atende a uma rota Markdown. [section_header](../section_header/section_header.py) oferece cabeçalho renderizado quando é necessário nomear a seção; [styles](../../constants/styles/README.md) concentra a materialização da rota V04, sempre por chamada explícita.
````

## 52. ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md

Origem: [R0177, linha 118](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md#L118). Conteúdo original:

````text
Revisão R03-A: leitura do módulo, fachada e exemplo; testes portáteis de conteúdo e determinismo. Sem alteração de layout, execução do notebook no Databricks ou auditoria independente.
````

## 53. ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md

Origem: [R0178, linha 48](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md#L48). Conteúdo original:

````text
O parâmetro `markdown` muda apenas o formato da string. Não há varredura de células, ordenação automática, deduplicação ou acompanhamento de progresso. A rota legada usa estilos históricos; `gerar_indice_eda_resolvido` obtém os estilos HTML da materialização V04. Em `markdown=True`, o tema é validado, mas nenhum CSS é inserido no texto.
````

## 54. ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md

Origem: [R0178, linha 83](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md#L83). Conteúdo original:

````text
### Caminho V04 — índice HTML com tema explícito
````

## 55. ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md

Origem: [R0178, linha 117](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md#L117). Conteúdo original:

````text
O contrato específico é verificado em [index_generator.py](index_generator.py) e no [mapa](../../constants/emojis/emojis.py), base `c60f1e5`. A documentação oficial [Organize Databricks notebook cells](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-cells) descreve o sumário nativo e seus títulos; consultada em 2026-09-12.

Os testes R03-B conferem ordem, repetições, formato e recusa de chave inexistente. Isso não é teste de navegação no workspace nem auditoria de um notebook real. Revisão própria de ChatGPT, sem auditoria independente.
````

## 56. ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md

Origem: [R0179, linha 80](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md#L80). Conteúdo original:

````text
### Caminho V04 — KPI HTML com tema explícito
````

## 57. ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md

Origem: [R0179, linha 90](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md#L90). Conteúdo original:

````text
A V04 não tematiza `kpi_card_markdown`: Markdown permanece textual. O tema controla somente a apresentação HTML do card; valores, ordem, unidades e contexto continuam responsabilidade do chamador.
````

## 58. ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md

Origem: [R0179, linha 102](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md#L102). Conteúdo original:

````text
A conversão de chaves para string pode descartar uma entrada Markdown se, por exemplo, o dicionário tiver as chaves `1` e `"1"`. Essa limitação foi reproduzida; a recomendação é usar rótulos textuais únicos desde a entrada. Na V04, `kpi_card_html_resolvido` obtém o CSS de `constants.styles`; `kpi_card_html` continua no caminho legado e não muda por carregar um tema.
````

## 59. ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md

Origem: [R0179, linha 124](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md#L124). Conteúdo original:

````text
Revisão R03-A: testes portáteis de texto, ordem, escape, entrada vazia e colisão de chaves. Não houve alteração de CSS, cálculo de indicadores reais, execução no Databricks ou auditoria independente.
````

## 60. ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md

Origem: [R0180, linha 48](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md#L48). Conteúdo original:

````text
Antes de montar o HTML, o código converte os campos para texto e aplica `html.escape`, que representa sinais como `<` e `>` de modo que apareçam como conteúdo, não como marcação. A rota legada usa as constantes históricas; `section_header_html_resolvido` obtém container, título e descrição da materialização central da V04.
````

## 61. ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md

Origem: [R0180, linha 86](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md#L86). Conteúdo original:

````text
### Caminho V04 — cabeçalho com tema explícito
````

## 62. ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md

Origem: [R0180, linha 120](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md#L120). Conteúdo original:

````text
O comportamento foi confrontado com [section_header.py](section_header.py) na base `c60f1e5`. A documentação [html.escape](https://docs.python.org/3/library/html.html) sustenta o tratamento dos caracteres. A [organização de células Databricks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-cells) explica a navegação por títulos. Consulta em 2026-09-12.

Os testes R03-B verificam preenchimento, sobrescrita, fallback e escape. Não são homologação visual ou de acessibilidade no workspace. Autorrevisão de ChatGPT, sem auditoria independente.
````

## 63. ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md

Origem: [R0181, linha 3](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md#L3). Conteúdo original:

````text
> **CUSTOMIZADO PELO HUB · V02 INTEGRADA · O NÚCLEO NÃO APLICA CORES SOZINHO.** O núcleo valida
> uma proposta; a V03 permite consumo Plotly por opt-in, sem instalar painel, aprovar identidade ou publicar arquivos.
````

## 64. ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md

Origem: [R0181, linha 38](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md#L38). Conteúdo original:

````text
Na preparação de uma proposta e nos adaptadores de gráficos, cabeçalhos
e materiais editoriais. A V03 já conecta explicitamente este núcleo ao `theme_plotly`
por uma rota opt-in; outros consumidores continuam em suas rotas atuais até a sprint
específica de cada um. Também permite testar uma configuração em Python sem
````

## 65. ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md

Origem: [R0181, linha 49](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md#L49). Conteúdo original:

````text
Para Plotly, a V03 mantém a rota legada e acrescenta uma integração opt-in com
[`theme_plotly`](../theme_plotly/): somente um `ResolvedTheme` explícito é consumido
pela API nova. Isso não migra gráficos existentes nem transforma a validação em aprovação.
````

## 66. ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md

Origem: [R0181, linha 138](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md#L138). Conteúdo original:

````text
O verificador de manutenção V01 cobre política e documentação; ele reutiliza as
mesmas funções de validação deste núcleo e não deve ser copiado para o workspace.
````

## 67. ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md

Origem: [R0181, linha 157](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md#L157). Conteúdo original:

````text
continua sendo o catálogo integrado. A adaptação Plotly virá na V03.
````

## 68. ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md

Origem: [R0181, linha 165](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md#L165). Conteúdo original:

````text
Testes desta candidata são locais e no CI conforme o checkpoint; não há alegação
de execução no Databricks, revisão independente ou usabilidade com iniciante.
````

## 69. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 11](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L11). Conteúdo original:

````text
| O que é? | Laboratório de rascunhos visuais que consome o tema validado pelo núcleo V02 e os adaptadores V03/V04. |
````

## 70. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L22). Conteúdo original:

````text
É a superfície de experimentação da V05 do Sistema de Temas. O núcleo [`visual.tema`](../tema/README.md) continua sendo responsável por carregar, validar e resolver uma configuração completa; o laboratório recebe um `ResolvedTheme` de contexto `notebook`, mantém uma proposta isolada e usa os consumidores V03/V04 para mostrar como a aparência chegaria aos componentes suportados.
````

## 71. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 40](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L40). Conteúdo original:

````text
Não use como workflow de submissão, aprovação, publicação ou controle de acesso. Os botões de publicar/submeter não transformam a V05 em mecanismo de governança, e um recibo de salvamento não comprova aceite. Uma referência chamada “demonstração” também não se torna tema operacional aprovado.

Não use para alterar métricas, dados, regras analíticas ou cores explicitamente gravadas em traces que os adaptadores não controlam. Também não use a galeria completa para afirmar suporte a `dark` ou `high_contrast`: a prévia Plotly V03 permanece `light` e falha fechada nos modos ainda não suportados.
````

## 72. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 64](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L64). Conteúdo original:

````text
Você precisa do pacote completo `.assistant`, porque o laboratório depende do núcleo V02, do schema e dos consumidores visuais V03/V04. A configuração de entrada precisa ser um `ResolvedTheme` válido de contexto `notebook`; dicionário cru ou contexto incompatível é recusado.
````

## 73. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 112](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L112). Conteúdo original:

````text
A quarta é o **modo visual**. A galeria completa permanece `light` porque o adaptador Plotly V03 ainda recusa `dark` e `high_contrast`. O laboratório não converte silenciosamente esses modos para claro.
````

## 74. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 128](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L128). Conteúdo original:

````text
Se já possui um `ResolvedTheme` e quer apenas aplicá-lo a uma figura Plotly existente, use [`visual.theme_plotly`](../theme_plotly/README.md). Para componentes HTML e tabela pandas integrados na V04, use as rotas `_resolvido` dos respectivos objetos sem abrir o laboratório.

Também é possível editar o JSON de configuração fora da interface e validá-lo pelo núcleo V02. Essa alternativa é mais direta para automação ou revisão por arquivo, mas não oferece a comparação guiada, o histórico do rascunho e a reabertura de sessão da V05.
````

## 75. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 148](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L148). Conteúdo original:

````text
- [Núcleo `visual.tema`](../tema/README.md): validação e resolução V02.
- [Adaptador `visual.theme_plotly`](../theme_plotly/README.md): consumidor Plotly V03.
- [Padrão de identidade visual](../../../hub_padroes/identidade_visual/README.md): contrato central do Sistema de Temas.

A V05 permanece candidata até revisão técnica e aceite explícito. Os próximos passos operacionais são validar no Databricks autorizado, acessibilidade, desempenho percebido/p95 quando aplicável, permissões reais de persistência e UAT por pessoa iniciante. Integração Git e publicação no workspace são gates distintos.
````

## 76. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md

Origem: [R0182, linha 156](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md#L156). Conteúdo original:

````text
O comportamento descrito é sustentado pela [implementação](theme_lab.py), pela [fachada pública](__init__.py), pelo [exemplo](exemplo_theme_lab.py) e pelas regressões V05 do repositório. A documentação local do núcleo e dos adaptadores delimita o que cada camada consome; o Visual Lab não redefine esses contratos.

Para a superfície de notebook, consulte a documentação oficial do [Databricks — ipywidgets](https://docs.databricks.com/aws/en/notebooks/ipywidgets) e [Databricks — widgets](https://docs.databricks.com/aws/en/notebooks/widgets), além da documentação do [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/).

Estado desta revisão: leitura do código e testes Git/Python da candidata; isso não equivale a publicação nem homologação de frontend/runtime Databricks, acessibilidade ou UAT.
````

## 77. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 5](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L5). Conteúdo original:

````text
> **Atualização V07 — estado atual.** Além das rotas V03, `theme_plotly` agora
> expõe `get_tokens_plotly(theme)`: ele revalida o `ResolvedTheme` pelas mesmas
> guardas de `notebook/light` e devolve uma **cópia** dos tokens para consumidores
> que precisam de semânticas específicas, como `palette.curves_legacy`,
> `palette.sequential` ou `semantic.warning`. A função não registra template nem
> altera `pio.templates.default`. A V07 também migrou explicitamente
> `correlation_matrix` e `distribution_grid`; referências abaixo que os descrevem
> como consumidores apenas legados registram o estado histórico da V03.
````

## 78. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 20](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L20). Conteúdo original:

````text
| O que é? | Funções legadas de tema Plotly mais um adaptador V03 opt-in para `ResolvedTheme`. |
````

## 79. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 33](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L33). Conteúdo original:

````text
As três operações legadas continuam iguais: `get_tema_eda` consulta a configuração histórica, `aplicar_tema` modifica uma figura e `registrar_template_plotly` registra o padrão `caixa` na sessão. A V03 acrescenta, sem substituir essas chamadas, `get_tema_plotly`, `aplicar_tema_resolvido` e `registrar_template_plotly_resolvido` para consumir explicitamente um `ResolvedTheme` validado pela V02. Plotly continua sendo apenas um consumidor; HTML e outros componentes têm sprints próprias.
````

## 80. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 61](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L61). Conteúdo original:

````text
Na rota V03, `get_tema_plotly(theme)` traduz somente os tokens notebook atribuídos ao Plotly e não altera a sessão. `aplicar_tema_resolvido` aplica essa tradução explicitamente a uma figura. `registrar_template_plotly_resolvido` usa um nome `hub-*`, não ativa o template por padrão e só muda `pio.templates.default` com `ativar=True`. A configuração é revalidada pelo núcleo antes de ser consumida.
````

## 81. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 71](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L71). Conteúdo original:

````text
Tenha Plotly instalado e o caminho de importação preparado. `aplicar_tema` recebe uma `go.Figure`, não uma tabela de dados. Para a rota V03, tenha também um `ResolvedTheme` produzido pelo núcleo V02 para o contexto `notebook`; não passe dicionário cru ao adaptador. Como a V03 revalida esse resultado antes de consumi-lo, `jsonschema` e `referencing` também precisam estar disponíveis conforme `hub_snippets/requirements-temas.txt`. O helper não instala dependências automaticamente. Fonte e subtítulo devem ser textos controlados e apropriados ao compartilhamento.
````

## 82. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 79](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L79). Conteúdo original:

````text
`get_tema_eda()` retorna o dicionário legado. `aplicar_tema(...)` retorna a própria figura modificada, preservando os dados dos traces. `registrar_template_plotly()` retorna `None` e deixa o template legado ativo na sessão. Na rota V03, `get_tema_plotly(theme)` retorna um novo dicionário de layout derivado do `ResolvedTheme`; `aplicar_tema_resolvido(...)` retorna a mesma figura modificada sem trocar o template default; e `registrar_template_plotly_resolvido(...)` retorna `None`, registra um nome `hub-*` e só altera o default quando `ativar=True`.
````

## 83. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 100](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L100). Conteúdo original:

````text
### V03: aplicar uma proposta resolvida sem mudar o legado
````

## 84. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 128](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L128). Conteúdo original:

````text
Escolha conscientemente entre aplicação explícita e registro global. Para propostas V03, prefira `aplicar_tema_resolvido`; `registrar_template_plotly_resolvido` exige namespace `hub-*`, recusa colisão por padrão e só ativa o template com `ativar=True`. `substituir=True` permite trocar um nome já registrado, mas não permite substituir silenciosamente um nome que já participa do default da sessão: nesse caso, a chamada falha e exige também `ativar=True`, pois trocar o objeto ativo já seria uma mudança global. Para recuperar o padrão da sessão depois de uma experiência de registro, guarde o valor anterior de `pio.templates.default` e restaure-o; não suponha que uma nova célula comece uma sessão vazia.
````

## 85. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 136](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L136). Conteúdo original:

````text
A paleta categórica não substitui escalas explicitamente definidas em heatmaps nem cores já fixadas nos traces. O registro global afeta outras figuras que usem o padrão da mesma sessão, e não outras sessões independentes. Um default Plotly pode ser composto, por exemplo `plotly+hub-alguma-coisa`; a V03 considera cada nome desse composto como ativo e recusa sua substituição com `ativar=False`. A V03 aplica somente `mode=light`: `dark` e `high_contrast` são válidos no contrato, mas falham fechados no adaptador Plotly até existirem tokens de superfície suficientes para não inventar backgrounds implícitos.
````

## 86. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md

Origem: [R0183, linha 154](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md#L154). Conteúdo original:

````text
A [implementação](theme_plotly.py) mantém as três operações legadas e acrescenta as três operações V03; a [fachada](__init__.py) exporta os seis nomes. O [notebook](exemplo_theme_plotly.py) demonstra o legado e a rota opt-in usando uma referência resolvida sem customização inline. [Correlation matrix](../../display/correlation_matrix/README.md) e [distribution grid](../../display/distribution_grid/README.md) continuam consumidores do caminho legado nesta sprint: não foram migrados implicitamente. O estado da V03 está em `docs/sprints/sistema_temas/V03/`.

## 15. Referências

O guia oficial [Theming and templates](https://plotly.com/python/templates/) descreve o registro e o alcance por sessão, assim como a distinção entre template e propriedades da figura. Consulta em 2026-09-12. As decisões particulares vigentes do Hub são verificáveis em [theme_plotly.py](theme_plotly.py). O estado desta sprint está em `docs/sprints/sistema_temas/V03/CHECKPOINT_V03.md`; a base `c60f1e5` permanece apenas como referência histórica da R03-B.

Os testes R03-B conferem identidade do objeto, dados preservados, precedência, anotações e registro com restauração do estado. Não homologam o aspecto no Databricks nem verificam a origem declarada pelo usuário. Revisão própria de ChatGPT; auditoria independente não realizada.

A V03 acrescenta testes de equivalência do layout legado, tradução de tokens, integridade do `ResolvedTheme`, ausência de efeitos globais na aplicação por figura, namespace/colisão de templates e falha fechada de contextos/modos ainda não suportados. Esses testes também não substituem inspeção visual no Databricks.
````

## 87. ambiente_fonte/.assistant/hub_padroes/identidade_visual/ERROS.md

Origem: [R0185, linha 26](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/ERROS.md#L26). Conteúdo original:

````text
| `RESOURCE_HASH`, `ASSET_HASH`, `ASSET_UNKNOWN` | Pacote ou recurso divergente | Restaure a versão compatível com o mantenedor; não altere hashes para esconder erro. |
| `DEPENDENCY_MISSING` | Validador indisponível | Mantenedor prepara requirements-temas.txt em ambiente autorizado; nada é instalado automaticamente. |
| `RESULT_TYPE`, `RESULT_INTEGRITY` | Objeto de saída incorreto ou adulterado | Gere novo resultado usando resolve_theme/load_theme; não monte a classe manualmente. |
| `SCHEMA_DIALECT`, `SCHEMA_INVALID`, `SCHEMA_REMOTE_REF`, `SCHEMA_LOCAL_REF`, `SCHEMA_NESTED_ID`, `SCHEMA_DYNAMIC_REF`, `SCHEMA_CYCLE` | Defeito do schema/pacote, não de uma escolha visual comum | Encaminhe ao mantenedor; nenhuma referência remota será consultada. |
````

## 88. ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md

Origem: [R0186, linha 4](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md#L4). Conteúdo original:

````text

O núcleo V02 está integrado no Git como verificador/resolvedor. V03/V04 acrescentam consumidores Plotly/HTML opt-in; V05 oferece o Visual Lab; V06 integra geração editorial; V07 amplia consumidores runtime e formatos exercitados; V08 alinha orientação transversal; V09 protege o transporte no kit; e V10 integra a superfície Databricks App `authoring_only`. Nenhuma dessas camadas troca o caminho legado por padrão.
Seu notebook atual continua igual. Para usar o pacote no workspace de trabalho, a revisão integrada ainda precisa ser instalada/publicada pelo procedimento autorizado e homologada no destino. Não publique arquivos por conta própria para experimentar uma cor.
````

## 89. ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md

Origem: [R0186, linha 7](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md#L7). Conteúdo original:

````text

A V11 está em candidata separada. Ela acrescenta uma ponte local/fail-closed entre um `ResolvedTheme` notebook e capacidades de tema de dashboards AI/BI. A ponte não altera `theme.schema.json`, não torna `context="aibi"` válido, não chama Databricks e não publica dashboard.

Quem só precisa acompanhar a entrega pode ler a seção “Interpretar a saída” abaixo.
````

## 90. ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md

Origem: [R0186, linha 116](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md#L116). Conteúdo original:

````text
sensível. O guia de erros indica o significado sem repetir o valor recebido.
A execução da demonstração foi verificada em Python/CI conforme o checkpoint;
Databricks, Windows, acessibilidade e teste com iniciante precisam de evidência
própria antes de serem declarados homologados.
````

## 91. ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md

Origem: [R0187, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md#L1). Conteúdo original:

````text
# Guia de primeiro uso — AI/BI V11

Este guia separa o que o projeto consegue preparar no Git do que precisa ser feito em um workspace Databricks autorizado.
````

## 92. ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md

Origem: [R0187, linha 2](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md#L2). Conteúdo original:

````text

Este guia separa o que o projeto consegue preparar no Git do que precisa ser feito em um workspace Databricks autorizado.

## 1. Entenda os dois níveis de tema
````

## 93. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md

Origem: [R0188, linha 6](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md#L6). Conteúdo original:

````text

Mantenedor/publicador técnico autorizado a criar ou atualizar Databricks Apps e a configurar recursos e permissões. Usuário final não precisa executar estas etapas.

## Pré-requisitos verificáveis
````

## 94. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md

Origem: [R0188, linha 2](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md#L2). Conteúdo original:

````text

> Este procedimento **não autoriza deploy**. Use somente depois de autorização explícita no ambiente de destino. O GitHub Actions da V10 nunca cria, atualiza ou publica Databricks Apps.

## Público
````

## 95. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md

Origem: [R0189, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md#L1). Conteúdo original:

````text
# Guia de primeiro uso — App de Gestão Visual V10

Este guia é para quem nunca usou o Sistema de Temas. Ele descreve o que a interface faz sem pressupor conhecimento de Python.
````

## 96. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md

Origem: [R0189, linha 11](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md#L11). Conteúdo original:

````text
3. você está no ambiente correto;
4. ninguém pediu que você publique ou altere o padrão da equipe — a V10 não faz isso.

Se o App exibir erro de identidade ou armazenamento, não tente contornar o bloqueio. Copie somente o código da mensagem e procure o mantenedor; não envie tokens nem dados internos.
````

## 97. ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py

Origem: [R0336, linha 146](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py#L146). Conteúdo original:

````text
# MAGIC **E há uma decisão de design que faltava neste notebook: contraste.**
# MAGIC Duas das quatro cores **reprovam** o mínimo AA (4,5:1) com texto branco —
# MAGIC `COR_ALERTA` em 1,73:1 e `COR_POSITIVO` em 2,04:1. São amarelo e verde
# MAGIC claros; branco em cima deles é praticamente ilegível.
# MAGIC
# MAGIC A regra que decorre disso: **`COR_ALERTA` e `COR_POSITIVO` são cores de
# MAGIC preenchimento — barra, ponto, borda —, nunca fundo para texto branco.**
# MAGIC Para selo ou chip com essas duas, o texto vai em `TEXTO_PRINCIPAL`. A
# MAGIC célula acima faz essa escolha sozinha, medindo antes de pintar.
# MAGIC
# MAGIC Isso é diferente de daltonismo, que o "quando não usar" menciona: contraste
# MAGIC é aferível no valor, e portanto não tem desculpa para ficar sem verificação.
````

## 98. ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py

Origem: [R0336, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py#L22). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |
````

## 99. ambiente_fonte/.assistant/hub_snippets/constants/emojis/exemplo_emojis.py

Origem: [R0337, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/emojis/exemplo_emojis.py#L22). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |
````

## 100. ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py

Origem: [R0338, linha 9](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py#L9). Conteúdo original:

````text
# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
````

## 101. ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py

Origem: [R0338, linha 129](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py#L129). Conteúdo original:

````text
# MAGIC base é um centésimo de ponto percentual) e é mais uma escala para errar. A
# MAGIC docstring do módulo chegou a documentar esse caso com um exemplo errado por
# MAGIC um fator de dez; foi corrigida, e a célula acima existe para que a próxima
# MAGIC divergência apareça na execução em vez de ficar no comentário.
````

## 102. ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py

Origem: [R0339, linha 5](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py#L5). Conteúdo original:

````text
# MAGIC **O problema.** Cada bloco de HTML num notebook pode carregar seu próprio `style="..."` inline, e uma mudança de identidade visual passa a exigir edição dispersa. A V04 mantém as constantes legadas e acrescenta uma materialização opt-in a partir do Sistema de Temas.
````

## 103. ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py

Origem: [R0339, linha 72](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py#L72). Conteúdo original:

````text
# MAGIC **Como ler.** As constantes continuam strings de CSS e preservam o caminho existente. A V04 não as transforma em estado global nem reestiliza HTML já exibido.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Caminho V04 — tema explícito, sem estado global
````

## 104. ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py

Origem: [R0339, linha 99](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py#L99). Conteúdo original:

````text
# MAGIC Na V04, `visual/badge`, `visual/divider`, `visual/kpi_card`, `visual/section_header`, `visual/index_generator` e `display/dataframe_styled` passam a consumir essa materialização **somente nas novas funções `_resolvido`**. As funções antigas continuam usando as constantes legadas e não mudam de aparência por efeito implícito.
# MAGIC
# MAGIC A configuração de referência reproduz os estilos legados dos componentes HTML. `dark` e `high_contrast` podem ser materializados quando a configuração completa é válida, mas isso não constitui certificação de acessibilidade ou homologação visual no Databricks.
# MAGIC
# MAGIC O contraste do badge de atenção da referência histórica continua uma limitação conhecida; confira a medição e a referência no [README](README.md).

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem conferir o destino.** A exibição no notebook não comprova suporte de outro renderizador; teste o documento final antes de distribuí-lo.
# MAGIC - **Como folha de estilo global.** A função devolve um dicionário para uso explícito; não injeta CSS na sessão.
# MAGIC - **Passando dicionário cru.** Os componentes V04 aceitam somente `ResolvedTheme` íntegro produzido pelo núcleo V02.
````

## 105. ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py

Origem: [R0339, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py#L22). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |
````

## 106. ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/exemplo_correlation_matrix.py

Origem: [R0340, linha 68](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/exemplo_correlation_matrix.py#L68). Conteúdo original:

````text
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC linhas: 3000 | colunas: 4
# MAGIC não executou neste runtime:
# MAGIC   Py4JError: An error occurred while calling
# MAGIC   None.org.apache.spark.ml.feature.VectorAssembler
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A base foi construída com `limite_credito` valendo três vezes a
# MAGIC `renda` mais um ruído pequeno. O comentário numérico na célula de geração
# MAGIC foi preservado como histórico, mas o coeficiente deve ser calculado, não
# MAGIC inferido daquela anotação. Em um ambiente compatível, esse par deve mostrar
# MAGIC associação positiva forte; a lista de pares e o mapa são saídas distintas.
# MAGIC A transcrição acima registra uma execução antiga, não o teste da R03-B.
````

## 107. ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/exemplo_dataframe_styled.py

Origem: [R0341, linha 95](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/exemplo_dataframe_styled.py#L95). Conteúdo original:

````text
# MAGIC É por isso que esta demonstração precisou de uma coluna com negativos.
# MAGIC Uma versão anterior deste notebook passava `highlight_cols=["nulos_pct",
# MAGIC "psi"]` — colunas sem nenhum valor negativo — e afirmava que as duas
# MAGIC ficavam destacadas. **Zero células eram pintadas**, e o HTML devolvido não
# MAGIC continha uma única ocorrência da cor de destaque.
````

## 108. ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt

Origem: [R0373, linha 8](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt#L8). Conteúdo original:

````text
# VERIFICADO EM 2026-08-17 — serverless, Spark 4.1.0, Python 3.11.10
# ===========================================================================
#
# O runtime traz numpy 1.23.5, pandas, matplotlib 3.7.2, mlflow 2.11.4,
# plotly 5.9.0 e scikit-learn 1.3.0. Todo o resto e ausente e precisa de
# instalacao explicita.
#
# `%pip install` FUNCIONA em notebook serverless, na primeira celula, seguido
# de `%restart_python`. As 12 bibliotecas abaixo foram instaladas e exercitadas
# com chamada real (ajuste de modelo, projecao, previsao) — nao so importadas.
#
# CUSTO MEDIDO nos 14 notebooks, em dois grupos bem distintos:
#   - torch e derivados (pytorch-tabnet)  : 270 a 310 s por job
#   - as outras nove bibliotecas          :  33 a  70 s por job
# Os 14 juntos levam ~25 minutos, nao a hora que uma estimativa unica de "3 min
# por notebook" sugeria. A diferenca importa: estimativa alta demais faz alguem
# nao reexecutar antes de replicar no trabalho.
````

## 109. ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt

Origem: [R0373, linha 26](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt#L26). Conteúdo original:

````text
# TRES REGRAS QUE CUSTARAM UM AMBIENTE QUEBRADO:
#
# 1. Instale por notebook, so o que aquele objeto usa. Instalar pmdarima, shap
#    e umap-learn na MESMA sessao derruba o `import numpy` do proprio notebook
#    ("numpy.dtype size changed... Expected 96 from C header, got 88").
#    Isoladas, as tres funcionam.
# 2. Tres exigem pin; as outras nove resolvem sozinhas. Sem o pin, `shap` arrasta
#    numpy 2.4.6 por cima do 1.23.5 do runtime, e o que quebra sao as extensoes C
#    ja compiladas contra o numpy antigo:
#      ValueError: numpy.dtype size changed, may indicate binary incompatibility.
#      Expected 96 from C header, got 88 from PyObject
#    Verificado em sessao limpa, com `%pip install shap` e mais nada.
#    As regras 1 e 2 compartilham o SINTOMA; o que as separa e a causa — ali sao
#    tres pacotes brigando entre si, aqui e um pacote trocando o numpy do
#    ambiente. O diagnostico pela mensagem sozinha nao distingue os dois.
# 3. Nao fixe numpy/pandas por precaucao. O aviso anterior deste arquivo mandava
#    fixar numpy==1.26.4 sempre; o runtime hoje traz 1.23.5, e o pin gera
#    conflito em vez de evitar. A excecao esta anotada no pmdarima.
#
# Registro anterior, de 2026-08-14, dizia que instalar sem fixar versao derrubava
# o kernel e que `%pip` antes do primeiro comando Spark abortava a execucao.
# Nenhuma das duas coisas se reproduziu hoje. O registro nao estava errado:
# descrevia o runtime daquele dia. Reexecute antes de confiar neste arquivo —
# ver `.claude/rules/free-vs-trabalho.md`.
````

## 110. ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt

Origem: [R0373, linha 51](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt#L51). Conteúdo original:

````text
# --- resolvem sozinhas: instale sem pin -------------------------------------
# versao que o pip escolheu em 2026-08-17, e a prova que rodou
catboost          # 1.2.10  — ajustou classificador, acuracia 0,885
lifelines         # 0.30.3  — Kaplan-Meier mediana 19,5; Cox coef 0,0903
lightgbm          # 4.7.0   — ajustou classificador, acuracia 0,897
optuna            # 4.9.0   — 8 trials, convergiu para x=2,30
prophet           # ver nota abaixo — previu 127 pontos, yhat final 88,6
pytorch-tabnet    # ajustou 2 epocas, acuracia 0,743
tabulate          # 0.10.0  — DataFrame.to_markdown() funcionando
torch             # 2.13.0+cu130 — tensor ok; cuda indisponivel (esperado)
xgboost           # 3.2.0   — ajustou classificador, acuracia 0,887

# --- EXIGEM pin: sem ele, quebram --------------------------------------------
pmdarima==2.0.4   # exige tambem numpy==1.23.5 na mesma linha de instalacao;
                  # sem os dois pins, envenena o ambiente. auto_arima devolveu
                  # ordem (0,1,0)
shap==0.44.1      # sem o pin, arrasta numpy 2.4.6 e quebra as extensoes C do
                  # runtime; ver a regra 2 no topo. TreeExplainer devolveu
                  # shap_values como lista de 2
umap-learn==0.5.5 # projecao (300, 2) confirmada
````

## 111. ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt

Origem: [R0373, linha 74](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt#L74). Conteúdo original:

````text
# que delegam a biblioteca opcional NO MOMENTO DA CHAMADA. Nenhuma analise de
# import de topo encontra isso, e o smoke test importa os dois modulos com PASS.
#
#   ml/explainability_report -> DataFrame.to_markdown() exige tabulate
#   display/dataframe_styled -> DataFrame.style       exige jinja2
#
# (o tabulate esta na lista de cima)
jinja2

# ml/mlflow_run chama mlflow.sklearn.log_model. `import mlflow` NAO traz o
# scikit-learn: o flavor e um submodulo resolvido na hora da chamada. Presente no
# runtime do Free (1.3.0), mas nao garantido em ambiente minimo. Efeito colateral
# conhecido: o flavor esta fixo em sklearn, entao um Booster LightGBM sai
# registrado pelo flavor errado.
scikit-learn>=1.3

# --- ja presentes no runtime; nao reinstale sem necessidade -----------------
matplotlib        # 3.7.2
mlflow            # 2.11.4 — mas nenhum run abre no serverless; ver a regra
plotly            # 5.9.0
scipy

# ===========================================================================
# NOTA SOBRE O PROPHET
# ===========================================================================
````

## 112. ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt

Origem: [R0373, linha 99](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt#L99). Conteúdo original:

````text
# Ate 2026-08-16 este arquivo classificava prophet como "sem combinacao
# funcional conhecida", por falhar com
# "'Prophet' object has no attribute 'stan_backend'" em serverless. Em
# 2026-08-17, `%pip install prophet` sem pin instalou e ajustou um modelo
# completo, com previsao de 7 dias a frente. O impedimento nao existe mais no
# runtime atual do Free.
````

## 113. ambiente_fonte/.assistant/hub_snippets/requirements-temas.txt

Origem: [R0374, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-temas.txt#L1). Conteúdo original:

````text
# Validação explícita V02. Não instalar no import; respeitar política do ambiente.
````

## 114. ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py

Origem: [R0376, linha 202](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py#L202). Conteúdo original:

````text
# MAGIC linhas na esquerda      : 500
# MAGIC com chave nula          : 48  <- nunca casam
# MAGIC cobertura sobre o total : 100.0%
# MAGIC ```
# MAGIC
# MAGIC O rótulo impresso “sobre o total” é histórico e impreciso: o campo
# MAGIC `cobertura_pct_chaves_validas` **exclui** as 48 linhas de chave nula do
# MAGIC denominador. Por isso pode mostrar 100% mesmo quando a esquerda contém nulos.
````

## 115. ambiente_fonte/.assistant/hub_snippets/spark/null_summary/exemplo_null_summary.py

Origem: [R0377, linha 148](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/exemplo_null_summary.py#L148). Conteúdo original:

````text
# MAGIC **O filtro merece atenção.** O status é emoji, não texto. Escrever
# MAGIC `status != 'ok'` parece natural, casa todas as linhas, e o `count` sai 5 de
# MAGIC 5 sem que nada acuse. Foi exatamente o erro que este notebook teve na
# MAGIC primeira versão — e a validação do projeto ganhou uma guarda por causa
# MAGIC dele: hoje ela reprova comparação com literal que o módulo não produz.
````

## 116. ambiente_fonte/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py

Origem: [R0378, linha 15](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py#L15). Conteúdo original:

````text
# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
````

## 117. ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py

Origem: [R0379, linha 11](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py#L11). Conteúdo original:

````text
# MAGIC ## Por que este notebook existe
# MAGIC
# MAGIC O ambiente anterior a este continha um cálculo de PSI **incorreto**:
# MAGIC comparava média e desvio padrão entre dois períodos. Parecia razoável,
# MAGIC produzia um número, e esse número não era PSI.
# MAGIC
# MAGIC O erro é fácil de cometer e difícil de perceber, porque o resultado
# MAGIC errado também "funciona": sobe quando a média muda, desce quando não
# MAGIC muda. Só que ele é cego para o tipo de mudança que mais importa.
````

## 118. ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py

Origem: [R0379, linha 232](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py#L232). Conteúdo original:

````text
# MAGIC ### Contrato atualizado em 09/09/2026
# MAGIC max_categorias deve ser inteiro positivo: bool, NaN e infinito são recusados antes de ações Spark. O limite vale por população e controla quantidade de categorias, não bytes totais ou custo do shuffle.
````

## 119. ambiente_fonte/.assistant/hub_snippets/spark/safe_display/exemplo_safe_display.py

Origem: [R0380, linha 66](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/exemplo_safe_display.py#L66). Conteúdo original:

````text
# MAGIC É a mesma família do `NameError: name 'spark' is not defined` que derrubou
# MAGIC seis módulos deste projeto no primeiro teste de runtime: **o notebook tem
# MAGIC globais que o módulo não herda**. Vale como regra ao escrever helper — se
# MAGIC ele precisa de algo que só existe no notebook, esse algo é parâmetro.
````

## 120. ambiente_fonte/.assistant/hub_snippets/testing/fixtures/exemplo_fixtures.py

Origem: [R0382, linha 28](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/exemplo_fixtures.py#L28). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | execução deste notebook no destino não revalidada na R03-A |
````

## 121. ambiente_fonte/.assistant/hub_snippets/visual/badge/exemplo_badge.py

Origem: [R0383, linha 112](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/exemplo_badge.py#L112). Conteúdo original:

````text
# MAGIC O contraste do estilo de atenção é uma limitação documentada no README,
# MAGIC não corrigida por esta sprint documental.
# MAGIC
# MAGIC ## Dívida registrada: as cores não vêm de `constants`
# MAGIC
# MAGIC O verde daqui é `#2E7D32`; o `VERDE` de `constants.colors` é `#8DC63F`.
# MAGIC São **três sítios de declaração e dois valores**: `constants.styles`
# MAGIC (`STYLE_BADGE_OK`) tem estilos de mesma finalidade, escritos separadamente, e
# MAGIC nenhum dos dois usa o `VERDE` oficial.
# MAGIC
# MAGIC A distinção importa para quem for unificar: uma unificação de `styles` e `badge` precisa
# MAGIC conferir contratos e apresentação; alinhar os dois ao `VERDE` de `colors`
# MAGIC **troca as cores dos estados alinhados**. Ambas exigem revisão de produto.
# MAGIC
# MAGIC O inventário dos doze módulos com cor redeclarada está em
# MAGIC `PLANO_HUB.md` §12.2.
````

## 122. ambiente_fonte/.assistant/hub_snippets/visual/badge/exemplo_badge.py

Origem: [R0383, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/badge/exemplo_badge.py#L22). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |
````

## 123. ambiente_fonte/.assistant/hub_snippets/visual/divider/exemplo_divider.py

Origem: [R0384, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/divider/exemplo_divider.py#L22). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |
````

## 124. ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/exemplo_kpi_card.py

Origem: [R0386, linha 22](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/exemplo_kpi_card.py#L22). Conteúdo original:

````text
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |
````

## 125. ambiente_fonte/.assistant/hub_snippets/visual/section_header/exemplo_section_header.py

Origem: [R0387, linha 51](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/section_header/exemplo_section_header.py#L51). Conteúdo original:

````text
# MAGIC O acoplamento é intencional e vale registrar: este módulo **importa** de
# MAGIC `constants.emojis` e de `constants.colors`. Novas chamadas usam o mapa
# MAGIC disponível no processo. Uma string já produzida ou saída já exibida não
# MAGIC se atualiza sozinha; reinicie/recarregue e execute conscientemente após
# MAGIC mudanças de biblioteca. Valores explícitos podem sobrescrever o mapa.
````

## 126. ambiente_fonte/.assistant/hub_snippets/visual/section_header/exemplo_section_header.py

Origem: [R0387, linha 86](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/section_header/exemplo_section_header.py#L86). Conteúdo original:

````text
# MAGIC A saída é HTML puro — e aqui uma correção importante, porque é
# MAGIC contraintuitivo: **o CSS está inline neste módulo**, montado a partir das
# MAGIC cores importadas. `constants.styles.STYLE_SECTION_HEADER` existe, mas
# MAGIC não é consumido por esta função. Essa constatação local não afirma
# MAGIC identidade integral de CSS nem ausência de uso em todo outro código.
# MAGIC
# MAGIC Ou seja: editar `STYLE_SECTION_HEADER` não muda a saída desta função. A
# MAGIC dívida está registrada no notebook de `constants.styles` e no inventário
# MAGIC de duplicação em `PLANO_HUB.md` §12.2.
````

## 127. ambiente_fonte/.assistant/hub_snippets/visual/tema/exemplo_tema.py

Origem: [R0388, linha 3](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/tema/exemplo_tema.py#L3). Conteúdo original:

````text
# MAGIC # Conferir temas — exemplo sintético V02
# MAGIC Leia o [guia do objeto](README.md) antes de executar. Sem instalação,
# MAGIC consultas, tabelas, gráficos ou arquivos gravados. Validação exige as
# MAGIC bibliotecas declaradas. Esta candidata não é homologação de Databricks.
````

## 128. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md

Origem: [R0389, linha 3](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md#L3). Conteúdo original:

````text
**Estado:** guia da candidata V05. Não representa instalação ou homologação no seu Databricks. O mantenedor entrega o pacote e as dependências preparados. O operador não precisa de Git, Node ou CLI para usar o painel.
````

## 129. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md

Origem: [R0389, linha 46](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md#L46). Conteúdo original:

````text
A galeria completa usa `mode=light`. Tema escuro e alto contraste não são simulados como se estivessem homologados, porque o adaptador Plotly V03 ainda os recusa.
````

## 130. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md

Origem: [R0389, linha 116](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md#L116). Conteúdo original:

````text
## 13. O que continua fora da V05

A V05 não implementa submissão, aprovação ou publicação compartilhada. Não recolore PNGs, não migra notebooks antigos, não configura Databricks App e não altera dashboards AI/BI.

Também permanecem pendentes como homologação separada: frontend Databricks real, teclado/leitor de tela, zoom, contraste percebido, p95 da prévia, permissões reais do destino e teste por usuário iniciante sem ajuda.
````

## 131. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md

Origem: [R0389, linha 122](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md#L122). Conteúdo original:

````text
## 14. Teste de primeiro uso — pendente

O UAT deve entregar este guia e o notebook preparado, sem ajuda verbal inicial. Registrar se a pessoa consegue escolher uma base, alterar e comparar, salvar sessão, encerrar/reabrir, explicar qual era a base original e dizer corretamente quem foi afetado pela mudança.

Teste Python automatizado não substitui esse UAT.
````

## 132. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py

Origem: [R0390, linha 3](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py#L3). Conteúdo original:

````text
# MAGIC # Aparência do Hub — prévia pessoal V05
````

## 133. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py

Origem: [R0390, linha 67](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py#L67). Conteúdo original:

````text
# MAGIC Saída da célula acima, executada com a candidata V05; é evidência Python,
# MAGIC não captura da interface Databricks:
````

## 134. ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py

Origem: [R0390, linha 147](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py#L147). Conteúdo original:

````text
# MAGIC ## 7. O que este notebook não comprova
# MAGIC
# MAGIC O [guia](GUIA_PRIMEIRO_USO.md) descreve fallback `dbutils.widgets`,
# MAGIC salvamento, reabertura e erros. GitHub Actions testa os objetos Python,
# MAGIC mas não homologa navegador Databricks, acessibilidade, p95, ACL da pasta
# MAGIC ou uso autônomo por pessoa iniciante. Submeter/aprovar/publicar continuam
# MAGIC fora da V05, assim como recoloração de PNGs e consumidores não integrados.
````

## 135. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py

Origem: [R0391, linha 19](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py#L19). Conteúdo original:

````text
# MAGIC | Bibliotecas | Plotly e NumPy disponíveis; para a seção V03, `jsonschema` e `referencing` preparados conforme `hub_snippets/requirements-temas.txt`; o notebook não instala pacotes |
````

## 136. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py

Origem: [R0391, linha 64](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py#L64). Conteúdo original:

````text
# MAGIC **Como ler.** As duas figuras mostram os mesmos dados. A diferença que importa
# MAGIC não é a cor — é o **rodapé**: a versão com tema declara a fonte dos dados e
# MAGIC quantos pontos foram declarados. Nesta célula, o rótulo de fonte menciona
# MAGIC fixtures, mas a série foi gerada por NumPy acima. A chamada original foi
# MAGIC preservada; não use esse rótulo ilustrativo como procedência comprovada.
````

## 137. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py

Origem: [R0391, linha 116](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py#L116). Conteúdo original:

````text
# MAGIC Este módulo **importa** a paleta de `constants.colors` em vez de copiá-la,
# MAGIC e também importa `CINZA_ESCURO` para a fonte. O hexadecimal exibido na
# MAGIC saída é o valor resolvido dessa constante, não prova de duplicação no
# MAGIC código atual. O inventário histórico de estilos não substitui essa leitura
# MAGIC da implementação. O tema também não substitui cores explícitas de traces.
````

## 138. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py

Origem: [R0391, linha 139](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py#L139). Conteúdo original:

````text
# MAGIC ## 3. V03 — referência resolvida, aplicação explícita
# MAGIC
# MAGIC Esta seção usa a referência notebook empacotada para provar a nova rota sem
# MAGIC editar a configuração dentro do notebook irmão. A referência é uma fixture
# MAGIC de teste, não um tema operacional aprovado.
````

## 139. ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py

Origem: [R0391, linha 166](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py#L166). Conteúdo original:

````text
# MAGIC **Como ler.** A igualdade entre as duas configurações prova que a referência
# MAGIC `legado_notebook` preserva o layout atual pela nova rota. A aplicação afeta
# MAGIC somente `figura3` e não muda `pio.templates.default`. Para aprender a criar
# MAGIC uma proposta com tokens diferentes, use o exemplo comentado no README do
# MAGIC objeto; o notebook executável mantém um contrato local simples e auditável.
# MAGIC `dark` e `high_contrast` continuam fora do adaptador Plotly desta sprint.
````

## 140. ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt

Origem: [arquivo integral, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt#L1). Conteúdo original:

````text
# Dependencias opcionais dos modulos de hub_snippets/ml.
#
# Instale apenas o subconjunto que o workflow exigir. Este arquivo e inventario
# com referencia de versao, nao lockfile: o projeto consumidor deve fixar o
# conjunto que testou.
#
# ===========================================================================
# VERIFICADO EM 2026-08-17 — serverless, Spark 4.1.0, Python 3.11.10
# ===========================================================================
#
# O runtime traz numpy 1.23.5, pandas, matplotlib 3.7.2, mlflow 2.11.4,
# plotly 5.9.0 e scikit-learn 1.3.0. Todo o resto e ausente e precisa de
# instalacao explicita.
#
# `%pip install` FUNCIONA em notebook serverless, na primeira celula, seguido
# de `%restart_python`. As 12 bibliotecas abaixo foram instaladas e exercitadas
# com chamada real (ajuste de modelo, projecao, previsao) — nao so importadas.
#
# CUSTO MEDIDO nos 14 notebooks, em dois grupos bem distintos:
#   - torch e derivados (pytorch-tabnet)  : 270 a 310 s por job
#   - as outras nove bibliotecas          :  33 a  70 s por job
# Os 14 juntos levam ~25 minutos, nao a hora que uma estimativa unica de "3 min
# por notebook" sugeria. A diferenca importa: estimativa alta demais faz alguem
# nao reexecutar antes de replicar no trabalho.
#
# TRES REGRAS QUE CUSTARAM UM AMBIENTE QUEBRADO:
#
# 1. Instale por notebook, so o que aquele objeto usa. Instalar pmdarima, shap
#    e umap-learn na MESMA sessao derruba o `import numpy` do proprio notebook
#    ("numpy.dtype size changed... Expected 96 from C header, got 88").
#    Isoladas, as tres funcionam.
# 2. Tres exigem pin; as outras nove resolvem sozinhas. Sem o pin, `shap` arrasta
#    numpy 2.4.6 por cima do 1.23.5 do runtime, e o que quebra sao as extensoes C
#    ja compiladas contra o numpy antigo:
#      ValueError: numpy.dtype size changed, may indicate binary incompatibility.
#      Expected 96 from C header, got 88 from PyObject
#    Verificado em sessao limpa, com `%pip install shap` e mais nada.
#    As regras 1 e 2 compartilham o SINTOMA; o que as separa e a causa — ali sao
#    tres pacotes brigando entre si, aqui e um pacote trocando o numpy do
#    ambiente. O diagnostico pela mensagem sozinha nao distingue os dois.
# 3. Nao fixe numpy/pandas por precaucao. O aviso anterior deste arquivo mandava
#    fixar numpy==1.26.4 sempre; o runtime hoje traz 1.23.5, e o pin gera
#    conflito em vez de evitar. A excecao esta anotada no pmdarima.
#
# Registro anterior, de 2026-08-14, dizia que instalar sem fixar versao derrubava
# o kernel e que `%pip` antes do primeiro comando Spark abortava a execucao.
# Nenhuma das duas coisas se reproduziu hoje. O registro nao estava errado:
# descrevia o runtime daquele dia. Reexecute antes de confiar neste arquivo —
# ver `.claude/rules/free-vs-trabalho.md`.

# --- resolvem sozinhas: instale sem pin -------------------------------------
# versao que o pip escolheu em 2026-08-17, e a prova que rodou
catboost          # 1.2.10  — ajustou classificador, acuracia 0,885
lifelines         # 0.30.3  — Kaplan-Meier mediana 19,5; Cox coef 0,0903
lightgbm          # 4.7.0   — ajustou classificador, acuracia 0,897
optuna            # 4.9.0   — 8 trials, convergiu para x=2,30
prophet           # ver nota abaixo — previu 127 pontos, yhat final 88,6
pytorch-tabnet    # ajustou 2 epocas, acuracia 0,743
tabulate          # 0.10.0  — DataFrame.to_markdown() funcionando
torch             # 2.13.0+cu130 — tensor ok; cuda indisponivel (esperado)
xgboost           # 3.2.0   — ajustou classificador, acuracia 0,887

# --- EXIGEM pin: sem ele, quebram --------------------------------------------
pmdarima==2.0.4   # exige tambem numpy==1.23.5 na mesma linha de instalacao;
                  # sem os dois pins, envenena o ambiente. auto_arima devolveu
                  # ordem (0,1,0)
shap==0.44.1      # sem o pin, arrasta numpy 2.4.6 e quebra as extensoes C do
                  # runtime; ver a regra 2 no topo. TreeExplainer devolveu
                  # shap_values como lista de 2
umap-learn==0.5.5 # projecao (300, 2) confirmada

# --- dependencia ESCONDIDA: nao aparece como import no topo do modulo --------
# SAO DOIS CASOS, e o padrao vale mais que cada um: o pandas tem varias funcoes
# que delegam a biblioteca opcional NO MOMENTO DA CHAMADA. Nenhuma analise de
# import de topo encontra isso, e o smoke test importa os dois modulos com PASS.
#
#   ml/explainability_report -> DataFrame.to_markdown() exige tabulate
#   display/dataframe_styled -> DataFrame.style       exige jinja2
#
# (o tabulate esta na lista de cima)
jinja2

# ml/mlflow_run chama mlflow.sklearn.log_model. `import mlflow` NAO traz o
# scikit-learn: o flavor e um submodulo resolvido na hora da chamada. Presente no
# runtime do Free (1.3.0), mas nao garantido em ambiente minimo. Efeito colateral
# conhecido: o flavor esta fixo em sklearn, entao um Booster LightGBM sai
# registrado pelo flavor errado.
scikit-learn>=1.3

# --- ja presentes no runtime; nao reinstale sem necessidade -----------------
matplotlib        # 3.7.2
mlflow            # 2.11.4 — mas nenhum run abre no serverless; ver a regra
plotly            # 5.9.0
scipy

# ===========================================================================
# NOTA SOBRE O PROPHET
# ===========================================================================
# Ate 2026-08-16 este arquivo classificava prophet como "sem combinacao
# funcional conhecida", por falhar com
# "'Prophet' object has no attribute 'stan_backend'" em serverless. Em
# 2026-08-17, `%pip install prophet` sem pin instalou e ajustou um modelo
# completo, com previsao de 7 dias a frente. O impedimento nao existe mais no
# runtime atual do Free.
````

## 141. ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md

Origem: [arquivo integral, linha 1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md#L1). Conteúdo original:

````text
# Deploy e rollback — Databricks App de Gestão Visual V10

> Este procedimento **não autoriza deploy**. Use somente depois de autorização explícita no ambiente de destino. O GitHub Actions da V10 nunca cria, atualiza ou publica Databricks Apps.

## Público

Mantenedor/publicador técnico autorizado a criar ou atualizar Databricks Apps e a configurar recursos e permissões. Usuário final não precisa executar estas etapas.

## Pré-requisitos verificáveis

- V10 integrada no Git em commit identificado e com CI verde;
- Databricks Apps habilitado no workspace;
- Unity Catalog Volume já existente para sessões;
- pessoa executora com permissão para gerenciar o App e associar o Volume;
- grupos reais de proponentes/mantenedores definidos pelo proprietário do ambiente;
- backup/conferência das sessões existentes quando houver atualização de App;
- nenhum segredo, PAT ou caminho corporativo gravado no repositório.

## 1. Gerar a fonte implantável

Em checkout limpo do commit aprovado:

```powershell
python -B tools/temas_v10_app.py --output .artifacts/v10-app
```

O comando cria uma pasta nova e falha se o destino já existir. O bundle contém os arquivos do App, `hub_snippets`, o contrato de identidade visual necessário e `V10_APP_MANIFEST.json` com SHA-256. Ele não executa Databricks CLI e não faz upload.

Execute em seguida:

```powershell
python -B tools/temas_v10_app.py --verify .artifacts/v10-app
```

Somente continue se a verificação terminar em `OK`.

## 2. Criar/configurar o App no workspace autorizado

Na interface Databricks Apps:

1. crie ou selecione o App destinado à gestão visual;
2. em **App resources**, adicione o Unity Catalog Volume de sessões;
3. use a resource key exatamente `theme_storage`;
4. conceda leitura e gravação ao service principal do App, porque a V10 persiste sessões;
5. restrinja **CAN USE** aos grupos que o proprietário do ambiente mapeou para autoria/manutenção;
6. não adicione SQL warehouse, Model Serving, Lakebase, Job, Genie ou segredo se não houver outra demanda aprovada;
7. não altere `app.yaml` para incorporar IDs ou caminhos corporativos.

O `app.yaml` recebe o caminho do Volume via `valueFrom: theme_storage`.

## 3. Implantar a pasta gerada

Use o mecanismo oficial autorizado pelo workspace para enviar o conteúdo de `.artifacts/v10-app/` como fonte do App. O arquivo `app.yaml` precisa ficar na raiz do projeto implantado.

A V10 não prescreve um nome corporativo de App, catálogo, schema ou Volume. Esses identificadores pertencem ao ambiente e não devem ser inventados no Git.

## 4. Smoke pós-deploy

Com usuário de teste autorizado:

1. abra o App e confirme que a identidade aparece sem pedir login adicional no próprio App;
2. abra um preset de demonstração;
3. faça uma alteração simples e valide;
4. compare base × proposta;
5. salve uma sessão de teste;
6. recarregue a página e reabra a sessão;
7. confirme revisão e histórico;
8. com uma segunda identidade autorizada, confirme que a sessão da primeira não aparece;
9. confirme visualmente que não existem ações de aprovar/publicar/promover;
10. registre somente evidência sanitizada no Git.

Esse smoke comprova operação do App/Volume naquele ambiente. Ele não substitui V12 (jornadas humanas, acessibilidade e usabilidade).

## 5. Falha durante deploy

Se o App não iniciar:

- confira logs do App;
- confirme que `theme_storage` existe e foi associado;
- confirme que o service principal tem privilégios de leitura/gravação no Volume;
- não troque o caminho para DBFS ou `/tmp` para contornar o erro;
- não habilite `HUB_THEME_LOCAL_DEV` em produção;
- não adicione PAT.

Se uma sessão não salvar, considere a operação falha até existir confirmação do App. Não invente recibo e não ajuste hash manualmente.

## 6. Rollback do App

Rollback da V10 significa voltar o **código do App** para um commit anterior ainda aprovado:

1. identifique o commit anterior e gere novamente seu bundle V10;
2. verifique `V10_APP_MANIFEST.json`;
3. mantenha o mesmo Volume; não apague sessões;
4. implante o bundle anterior pelo mesmo canal autorizado;
5. repita o smoke mínimo de abertura/listagem/reabertura;
6. registre commit anterior, commit revertido, motivo e resultado.

Não use force-push, limpeza recursiva ou exclusão do Volume como rollback.

## 7. O que este rollback não faz

O App V10 não publica temas. Portanto, retornar o App não significa retornar um tema compartilhado. O rollback de tema publicado continua sujeito à política V01: nova publicação de revisão anterior ainda aprovada, com guardas e histórico preservados.

## 8. Retenção e limpeza

A V10 não apaga automaticamente sessões e não oferece botão de exclusão. Se o ambiente exigir retenção, o administrador deve estabelecer política explícita para o Volume antes de executar qualquer limpeza. A ausência de política não autoriza descarte ad hoc.
````
