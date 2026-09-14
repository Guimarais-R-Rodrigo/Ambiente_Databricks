# `theme_lab` — laboratório de aparência do Hub

<!-- readme-objeto: 1.0.0 -->

Este recurso permite experimentar a aparência de um notebook em uma **prévia pessoal**. A V05 candidata oferece escolha guiada de ponto de partida, edição visual, comparação, salvamento rastreável e reabertura. **Nada aqui aprova ou publica um tema; o laboratório não publica temas.**

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Laboratório de rascunhos visuais para contexto notebook. |
| Para que serve? | Escolher uma base, ajustar aparência, comparar e preservar uma sessão local. |
| Quando usar? | Para preparar e retomar uma proposta de aparência sem alterar o padrão da equipe. |
| Quando evitar? | Para aprovação, publicação, autenticação, certificação de acessibilidade ou recoloração de imagens. |
| O que exige? | Pacote completo do Hub, dependências e, para persistência, pasta explicitamente preparada. |
| O que entrega? | `ThemeLabDraft`, prévias sintéticas, JSON avulso ou sessão rastreável com base/proposta/histórico. |

Primeiro acesso: [guia operacional](GUIA_PRIMEIRO_USO.md). Demonstração: [notebook de exemplo](exemplo_theme_lab.py). Contrato executável: [implementação](theme_lab.py) e [API pública](__init__.py).

## 1. O que é?

É a superfície de experimentação do Sistema de Temas. O núcleo V02 continua responsável por validar configurações completas; o laboratório organiza autoria, prévia e persistência sem transformar um rascunho em configuração aprovada.

O import de `theme_lab` não carrega `ipywidgets`, não consulta rede, Spark, SQL ou MLflow e não altera `pio.templates.default`.

## 2. Que problema este recurso resolve?

A V05 responde a quatro necessidades: **escolher**, **ajustar**, **comparar** e **preservar uma proposta**. O operador não precisa procurar cores em vários notebooks nem escrever código para reabrir uma sessão previamente salva pelo laboratório.

## 3. Quando faz sentido usar?

Use para comparar alternativas visuais com dados sintéticos, preparar uma proposta para revisão e continuar o trabalho em outra sessão. A comparação usa os adaptadores reais V03/V04, portanto exercita o mesmo caminho técnico dos consumidores já integrados.

## 4. Quando não usar?

Não use como publicador, workflow de aprovação ou mecanismo de permissão. `Submeter` e `Publicar` permanecem fora desta entrega. Uma referência chamada “demonstração” não é tema operacional aprovado. O laboratório também não recolore PNGs nem componentes que ainda não consomem o Sistema de Temas.

## 5. Escolher um ponto de partida

`get_demo_presets()` expõe referências notebook empacotadas **explicitamente marcadas como demonstração**. `prepare_theme_lab_presets()` permite ao mantenedor fornecer outros `ResolvedTheme` notebook; todos são revalidados e um contexto incompatível é recusado.

`create_theme_lab_from_preset()` cria um rascunho a partir de uma chave conhecida. Chave inexistente não cai silenciosamente em outro preset. `build_theme_lab_launcher()` apresenta a escolha em dropdown e identifica visualmente opções de demonstração.

Escolher uma opção não a aprova e não altera o padrão da equipe.

## 6. Ajustar

`get_control_specs()` deriva tipo, descrição, unidade, limite e controle do schema canônico. Cor possui seletor + HEX; tamanhos e paletas respeitam o contrato. Todos os valores habilitados são tratados como uma proposta única: se qualquer campo falhar, o último estado válido permanece.

Campos sem consumidor correspondente na galeria ficam desabilitados e explicam o motivo. Isso evita um controle que pareça funcionar sem efeito observável.

## 7. Comparar

`build_preview()` e `compare_preview()` usam dados sintéticos fixos em seis representações por lado: cabeçalho, KPI, barras, série temporal, heatmap e tabela. Valores, nomes e ordem dos dados permanecem iguais entre base e proposta; somente a aparência pode mudar.

A galeria completa continua limitada a `mode=light`, porque o adaptador Plotly V03 ainda recusa `dark`/`high_contrast`. Isso é fail-closed, não conversão silenciosa para claro.

## 8. Rascunho e histórico em memória

`ThemeLabDraft` mantém `base`, `current`, revisão e até cem estados anteriores. `undo()` retorna ao estado válido anterior; `restore()` volta à base original. Erro de validação não cria histórico parcial.

Duas instâncias não compartilham tema ou histórico. `dirty` apenas informa diferença entre proposta atual e base; não significa que algo foi salvo.

## 9. JSON avulso versus sessão rastreável

Existem dois mecanismos diferentes:

- `export_bytes()` / `save_proposal()` produzem a configuração canônica atual; são adequados quando só o JSON da proposta é necessário;
- `save_theme_lab_session()` cria um **bundle local de sessão** para retomar a autoria com sua linhagem.

Uma sessão completa contém `base.json`, `proposal.json`, estados de histórico e `session.json`. O manifesto registra hashes de base/proposta/histórico e a revisão. Ele é escrito por último e funciona como marcador de sessão completa.

O diretório usa criação exclusiva e não sobrescreve uma sessão existente. Um diretório parcial sem `session.json` não aparece em `list_theme_lab_sessions()` e não pode ser reaberto como sessão válida.

## 10. Linhagem e reabertura

`reopen_theme_lab_session()` lê os arquivos de uma sessão completa, revalida os temas e confere os hashes registrados. Divergência de conteúdo é recusada; o código não “corrige” o hash para continuar.

A reabertura restaura a **base original, a proposta atual, o histórico e a revisão local**. Portanto, a proposta não vira silenciosamente uma nova base. `build_theme_lab_launcher()` lista sessões completas na pasta preparada e permite selecionar **Reabrir sessão** sem o operador escrever código de carregamento.

Essa linhagem é local ao laboratório. Não autentica autor, não registra aprovação de governança e não é uma assinatura digital.

## 11. Interface `ipywidgets` e fallback

`build_ipywidgets_lab()` constrói o editor para um rascunho já escolhido. `build_theme_lab_launcher()` acrescenta a entrada guiada de presets e sessões. Importar o módulo continua sem importar `ipywidgets`; a dependência é exigida somente ao construir a interface.

Sem `ipywidgets`, `install_dbutils_fallback()` e `apply_dbutils_fallback()` oferecem sete campos primários em widgets nativos de texto. É um fallback funcionalmente menor: não oferece a experiência completa de catálogo/sessões do launcher.

## 12. Salvamento e segurança operacional

As funções de gravação exigem pasta regular já existente, rejeitam nomes fora do formato e não seguem atalhos simbólicos previstos pelas guardas locais. Arquivo ou sessão existente não é sobrescrito.

Uma falha de I/O nunca gera recibo de sucesso. O salvamento de JSON avulso pode deixar resíduo parcial quando o sistema de arquivos falha; a mensagem orienta inspeção pelo mantenedor. A persistência não é sandbox contra outro processo hostil e não substitui ACL do ambiente.

`ProposalReceipt` descreve JSON avulso. `ThemeLabSessionReceipt` descreve sessão completa e inclui hashes de base/proposta e do manifesto. Nenhum recibo significa submissão, aprovação ou publicação.

## 13. Dependências e ambiente

Validar exige `jsonschema` e `referencing`; a galeria usa pandas, Plotly e Jinja2; a interface completa exige ipywidgets/IPython. O módulo não instala pacotes.

Testes em GitHub Actions comprovam o comportamento Python exercitado, não a renderização no navegador Databricks. Permanecem gates separados: runtime do workspace, callbacks no frontend, teclado/leitor de tela, contraste percebido, zoom, p95 da prévia, permissões reais da pasta e UAT por iniciante.

## 14. Como saber se faz sentido?

Teste pelo launcher: selecione uma base, abra, altere uma cor, aplique, compare os seis componentes, salve uma sessão, feche o estado em memória e reabra pelo dropdown. A base e a proposta devem conservar hashes distintos quando houver alteração; após reabertura, `undo()` deve continuar retornando ao estado anterior salvo.

Adulterar `proposal.json` deve impedir a reabertura. Uma pasta incompleta deve ficar fora da lista. Preset inexistente ou de outro contexto deve falhar sem fallback. Esses comportamentos possuem regressões automatizadas, mas ainda não substituem homologação do ambiente real.

## 15. Arquivos relacionados e referências

Leia o [guia de primeiro uso](GUIA_PRIMEIRO_USO.md), o [exemplo](exemplo_theme_lab.py), o [núcleo V02](../tema/README.md) e o [adaptador Plotly](../theme_plotly/README.md). O padrão central fica em `hub_padroes/identidade_visual/`.

Documentação oficial consultada para a camada de notebook: [Databricks — ipywidgets](https://docs.databricks.com/aws/en/notebooks/ipywidgets), [Databricks — widgets](https://docs.databricks.com/aws/en/notebooks/widgets) e [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/).

A V05 permanece candidata até revisão técnica, aceite e integração. Não houve publicação Databricks por este objeto.
