# `theme_lab` — laboratório de aparência do Hub

<!-- readme-objeto: 1.0.0 -->

O `theme_lab` é o snippet de autoria assistida do Sistema de Temas para contexto `notebook`: ele permite escolher um ponto de partida, experimentar ajustes, comparar a aparência e preservar uma sessão de trabalho rastreável. **Nada aqui aprova ou publica um tema; o laboratório não publica temas.**

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Laboratório de rascunhos visuais que consome o tema validado pelo núcleo e os adaptadores Plotly/HTML. |
| Para que serve? | Escolher uma base, ajustar tokens, comparar a aparência e salvar/reabrir uma sessão local sem mudar o padrão da equipe. |
| Quando usar? | Para preparar, revisar e retomar uma proposta de aparência de notebook com dados sintéticos. |
| Quando evitar? | Para aprovação, publicação, autenticação, certificação de acessibilidade ou alteração de dados analíticos. |
| O que exige? | Pacote completo do Hub; dependências de tema; pandas, Plotly e Jinja2 para a prévia; ipywidgets/IPython para a interface completa; pasta preparada para persistência. |
| O que entrega? | Rascunho validado, prévias/comparações, JSON avulso ou sessão rastreável com base, proposta e histórico. |

Comece pelo [guia de primeiro uso](GUIA_PRIMEIRO_USO.md). Veja uma execução orientada no [exemplo](exemplo_theme_lab.py). O contrato executável está na [implementação](theme_lab.py) e na [fachada pública](__init__.py).

## 1. O que é?

É a superfície de experimentação do Sistema de Temas. O núcleo [`visual.tema`](../tema/README.md) continua sendo responsável por carregar, validar e resolver uma configuração completa; o laboratório recebe um `ResolvedTheme` de contexto `notebook`, mantém uma proposta isolada e usa os consumidores Plotly/HTML para mostrar como a aparência chegaria aos componentes suportados.

O laboratório não é um gerenciador de configuração global. Importar `hub_snippets.visual.theme_lab` não carrega `ipywidgets`, não consulta rede, Spark, SQL ou MLflow e não altera `plotly.io.templates.default`. A interface opcional só é importada quando sua construção é solicitada.

## 2. Que problema este recurso resolve?

Ele responde à pergunta: **“Como posso experimentar uma aparência do notebook, comparar com o ponto de partida e voltar depois ao mesmo rascunho sem transformar a experiência em tema aprovado?”**

Sem essa camada, a pessoa teria de editar JSON manualmente, montar prévias por conta própria e reconstruir o contexto da sessão. O `theme_lab` organiza escolha, edição, comparação e persistência, mas mantém separadas autoria, aprovação e publicação.

## 3. Quando faz sentido usar?

Use o laboratório quando a decisão é visual e o contexto é `notebook`: por exemplo, comparar cor principal, tipografia, dimensões ou paletas antes de propor uma mudança. Ele é especialmente útil quando é importante preservar a base original, registrar um histórico de estados válidos e reabrir a sessão em outro momento.

Também faz sentido para demonstrações controladas. `get_demo_presets()` fornece referências empacotadas explicitamente marcadas como demonstração, e `prepare_theme_lab_presets()` permite ao mantenedor fornecer outros `ResolvedTheme` notebook, todos revalidados antes de entrar no catálogo.

## 4. Quando não usar?

Não use como workflow de submissão, aprovação, publicação ou controle de acesso. Os botões de publicar/submeter não transformam o laboratório em mecanismo de governança, e um recibo de salvamento não comprova aceite. Uma referência chamada “demonstração” também não se torna tema operacional aprovado.

Não use para alterar métricas, dados, regras analíticas ou cores explicitamente gravadas em traces que os adaptadores não controlam. Também não use a galeria completa para afirmar suporte a `dark` ou `high_contrast`: a prévia Plotly permanece `light` e falha fechada nos modos ainda não suportados.

Contraexemplo: o código pode carregar um tema válido e produzir uma prévia bonita, mas isso não responde se o contraste é acessível no navegador Databricks. Acessibilidade percebida exige outro gate.

## 5. Como funciona, intuitivamente?

O fluxo é: **escolher uma base validada → criar um rascunho isolado → editar tokens permitidos → revalidar a proposta inteira → gerar uma galeria com os mesmos dados sintéticos → comparar → salvar ou reabrir a sessão**.

`get_control_specs()` deriva unidade, limites e tipo de controle do schema canônico. Rótulos amigáveis podem vir do mapa local `_LABELS`; na ausência dele, usam descrição ou nome do token. A atualização é atômica: se um dos valores propostos for inválido, o último estado válido continua sendo o rascunho corrente. Campos que ainda não possuem consumidor correspondente na galeria ficam desabilitados e informam o motivo, em vez de aparentar efeito inexistente.

`ThemeLabDraft` mantém `base`, `current`, revisão e histórico de até cem estados. `undo()` retorna ao estado válido anterior; `restore()` volta à base original. Instâncias diferentes não compartilham tema ou histórico. O atributo `dirty` informa diferença entre proposta e base, não que a proposta foi salva.

Na visualização, `build_preview()` e `compare_preview()` usam o mesmo conjunto sintético em seis representações por lado: cabeçalho, KPI, barras, série temporal, heatmap e tabela. Os valores e a ordem dos dados permanecem fixos; a comparação pretende isolar a aparência.

## 6. Exemplo de situação

Uma pessoa quer avaliar se outra cor principal e outro tamanho de título melhoram a leitura de notebooks. Ela abre o launcher, escolhe uma referência de demonstração, altera os dois controles e aplica a proposta à prévia. O laboratório revalida a configuração e mostra lado a lado a base e a proposta com os mesmos dados sintéticos.

Depois da revisão, a pessoa salva a sessão em uma pasta preparada. Ao reabrir pelo launcher, o laboratório restaura a base original, a proposta atual, a revisão e o histórico. Ela pode executar `undo()` e voltar ao estado anterior preservado. Essa continuidade é evidência de linhagem local da sessão; não é aprovação da aparência.

## 7. O que você precisa antes de usar?

Você precisa do pacote completo `.assistant`, porque o laboratório depende do núcleo, do schema e dos consumidores visuais. A configuração de entrada precisa ser um `ResolvedTheme` válido de contexto `notebook`; dicionário cru ou contexto incompatível é recusado.

Para validar temas, o pacote usa `jsonschema` e `referencing`. A galeria usa pandas, Plotly e Jinja2. A interface completa usa ipywidgets e IPython quando construída. O módulo não instala dependências automaticamente.

Para salvar JSON ou sessões, prepare explicitamente uma pasta regular existente e com permissões adequadas. O laboratório valida o formato do nome, evita sobrescrita e aplica guardas locais de caminho/symlink, mas não cria uma sandbox contra outro processo e não substitui ACLs do workspace.

Antes de confiar no resultado, confirme ainda que o ambiente Databricks real renderiza os widgets e os componentes como esperado; um teste Python não comprova o frontend do workspace.

## 8. O que este recurso entrega?

A fachada pública expõe tipos de rascunho, controle, prévia, comparação, preset, recibos e informações de sessão, além das funções de criação, catálogo, persistência, galeria e interface.

`ThemeLabDraft` representa a proposta em memória. `ThemeLabPreview` contém cabeçalho, KPI, tabela e três figuras Plotly; `ThemeLabComparison` reúne as duas prévias. `ProposalReceipt` descreve um JSON avulso salvo. `ThemeLabSessionReceipt` descreve uma sessão completa; `ThemeLabSessionInfo` expõe metadados seguros para listagem.

Há dois produtos persistentes diferentes:

- `export_bytes()` / `save_proposal()` geram somente a configuração canônica atual;
- `save_theme_lab_session()` cria um bundle de sessão com `base.json`, `proposal.json`, estados de histórico e `session.json`.

O manifesto `session.json` é escrito por último e registra hashes da base, da proposta e do histórico, além da revisão. Uma pasta parcial sem esse marcador não aparece em `list_theme_lab_sessions()` e não é aceita por `reopen_theme_lab_session()`. A listagem valida apenas o manifesto; a reabertura lê `base.json`, `proposal.json` e `history_000.json`, `history_001.json` etc. e confere cada hash. Listagem não comprova integridade atual de todos os payloads.

Nenhum desses retornos significa submissão, aprovação, publicação, autenticação de autor ou assinatura digital.

## 9. Como usar este recurso no Hub?

A rota mais simples é seguir o [guia de primeiro uso](GUIA_PRIMEIRO_USO.md) e depois executar o [exemplo](exemplo_theme_lab.py) em um ambiente de teste. O exemplo demonstra o fluxo sem substituir a leitura do contrato.

A fachada pública permite iniciar pelo launcher:

```python
from hub_snippets.visual.theme_lab import build_theme_lab_launcher

ui = build_theme_lab_launcher()
display(ui.root)
```

Essa rota permite experimentar sem persistência. Para habilitar salvamento/reabertura, forneça explicitamente `save_root=PASTA_AUTORIZADA`, uma pasta regular existente preparada pelo responsável. O launcher lista sessões com manifesto válido; aparecer na lista não verifica todos os payloads e hashes. A conferência completa ocorre na reabertura. Para integrar uma base escolhida pelo mantenedor, prepare o catálogo com `prepare_theme_lab_presets()` e forneça-o explicitamente ao launcher conforme o exemplo.

Quando ipywidgets não estiver disponível, `install_dbutils_fallback()` e `apply_dbutils_fallback()` oferecem um fallback menor baseado em sete campos primários de texto. Esse caminho não reproduz toda a experiência de catálogo e sessões do launcher.

## 10. Decisões e configurações que mais importam

A primeira decisão é a **base**. `create_theme_lab_from_preset()` aceita somente uma chave conhecida; chave inexistente não cai silenciosamente em outro preset. Presets fornecidos pelo mantenedor são revalidados e contexto incompatível é recusado.

A segunda é **aplicar versus apenas editar os controles**. Na interface, campos pendentes ainda não aplicados bloqueiam salvamento/exportação, evitando persistir uma proposta diferente do que a pessoa acabou de visualizar.

A terceira é **JSON avulso versus sessão rastreável**. Salve apenas a proposta quando você só precisa da configuração canônica. Use sessão quando precisa retomar a autoria preservando base original, proposta, histórico e revisão.

A quarta é o **modo visual**. A galeria completa permanece `light` porque o adaptador Plotly ainda recusa `dark` e `high_contrast`. O laboratório não converte silenciosamente esses modos para claro.

## 11. Limitações, riscos e armadilhas

A persistência é local ao caminho fornecido. O diretório de sessão é criado de forma exclusiva e não sobrescreve uma sessão existente. Se houver falha de I/O, o código não emite recibo de sucesso. No salvamento de JSON avulso, uma falha posterior à criação pode deixar arquivo parcial; a pessoa deve inspecionar o resíduo antes de tentar novamente.

`reopen_theme_lab_session()` relê os arquivos, revalida os temas e confere os hashes registrados. Conteúdo adulterado é recusado; o código não “repara” o hash para continuar. A reabertura restaura a base original em vez de transformar silenciosamente a proposta em nova base.

A galeria usa dados sintéticos e não certifica a aparência de todos os notebooks. Campos sem componente correspondente na galeria permanecem preservados, mas não são fingidos como visualizados.

Os testes Python exercitam o estado dos widgets e callbacks no kernel, mas não comprovam renderização no navegador Databricks, teclado/leitor de tela, contraste percebido, zoom, p95 da interação, permissões reais da pasta ou uso por pessoa iniciante. Esses gates continuam separados.

## 12. Quais são as alternativas?

Se você só precisa carregar, validar, resolver ou serializar uma configuração, use [`visual.tema`](../tema/README.md) diretamente; o Visual Lab acrescentaria uma interface que não é necessária.

Se já possui um `ResolvedTheme` e quer apenas aplicá-lo a uma figura Plotly existente, use [`visual.theme_plotly`](../theme_plotly/README.md). Para componentes HTML e tabela pandas, use as rotas `_resolvido` dos respectivos objetos sem abrir o laboratório.

Também é possível editar o JSON de configuração fora da interface e validá-lo pelo núcleo. Essa alternativa é mais direta para automação ou revisão por arquivo, mas não oferece a comparação guiada, o histórico do rascunho e a reabertura de sessão do laboratório.

Nenhuma dessas alternativas, por si só, publica ou aprova temas.

## 13. Como saber se o resultado faz sentido?

Faça uma verificação funcional controlada: abra o launcher, selecione uma base conhecida, altere uma cor, aplique, compare os seis componentes, salve uma sessão, descarte o estado em memória e reabra a sessão. Quando houve alteração, base e proposta devem manter hashes distintos; após reabertura, `undo()` deve continuar retornando ao estado anterior salvo.

Depois teste as recusas: adulterar `proposal.json` deve impedir a reabertura; uma pasta incompleta sem manifesto deve ficar fora da lista; preset inexistente e contexto diferente de `notebook` devem falhar sem fallback.

Essas verificações demonstram contratos do helper. A etapa seguinte é conferir a aparência no runtime autorizado, com navegador e permissões reais, e executar a revisão humana de legibilidade/acessibilidade prevista para a iniciativa.

## 14. Arquivos relacionados e próximos passos

- [Implementação `theme_lab.py`](theme_lab.py): contrato executável e guardas.
- [Fachada `__init__.py`](__init__.py): nomes públicos importáveis.
- [Exemplo `exemplo_theme_lab.py`](exemplo_theme_lab.py): demonstração sintética do fluxo.
- [Guia de primeiro uso](GUIA_PRIMEIRO_USO.md): operação passo a passo para quem nunca usou o laboratório.
- [Núcleo `visual.tema`](../tema/README.md): validação e resolução.
- [Adaptador `visual.theme_plotly`](../theme_plotly/README.md): consumidor Plotly.
- [Padrão de identidade visual](../../../hub_padroes/identidade_visual/README.md): contrato central do Sistema de Temas.

Use a instalação fornecida pelo responsável. Confirme renderização, acessibilidade, desempenho e permissões do destino antes de adotar a interface; a existência do código não certifica essas condições nem autoriza publicação.

## 15. Referências

O comportamento descrito é sustentado pela [implementação](theme_lab.py), pela [fachada pública](__init__.py), pelo [exemplo](exemplo_theme_lab.py). A documentação local do núcleo e dos adaptadores delimita o que cada camada consome; o Visual Lab não redefine esses contratos.

Para a superfície de notebook, consulte a documentação oficial do [Databricks — ipywidgets](https://docs.databricks.com/aws/en/notebooks/ipywidgets) e [Databricks — widgets](https://docs.databricks.com/aws/en/notebooks/widgets), além da documentação do [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/).

Conferência do contrato Python não equivale a publicação nem homologação de frontend/runtime Databricks, acessibilidade ou uso autônomo.
