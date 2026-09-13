# `theme_lab` — laboratório visual de propostas em notebook

<!-- readme-objeto: 1.0.0 -->

O Visual Lab permite experimentar uma configuração notebook já validada, comparar a proposta com o ponto de partida e exportar ou salvar um **rascunho**. Ele não publica temas, não aprova revisões e não altera o padrão da equipe.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um adaptador V05 sobre o núcleo de temas V02 e os renderizadores V03/V04. |
| Para que serve? | Editar tokens de forma explícita, pré-visualizar dados sintéticos e manter histórico local da sessão. |
| Use quando... | Quiser avaliar aparência de notebook sem mudar chamadas legadas nem consultar dados reais. |
| Evite quando... | Precisar publicar tema, aprovar revisão, homologar acessibilidade ou usar dados corporativos. |
| Precisa de... | Núcleo de temas e dependências da prévia; `ipywidgets` apenas para a UI interativa. |
| Entrega... | `ThemeLabDraft`, metadados de controles, prévia sintética, comparação e UI/fallback opcionais. |

Consulte a [implementação](theme_lab.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_theme_lab.py).

## 1. O que é?

É a camada de experiência em notebook do Sistema de Temas. O estado do rascunho fica em uma instância `ThemeLabDraft`: base, proposta atual, histórico e revisão local. Não existe tema global do laboratório.

A UI `ipywidgets` é construída somente quando `build_ipywidgets_lab` é chamada. Importar `hub_snippets.visual.theme_lab` não importa `ipywidgets`, não cria widget e não escreve arquivo.

## 2. Que problema este recurso resolve?

Até V04, o Hub já consegue validar um tema e aplicá-lo explicitamente a Plotly, HTML e tabelas, mas a pessoa precisa editar a configuração por código. A V05 cria uma superfície guiada para experimentar esses mesmos adaptadores, mantendo a configuração completa e revalidada a cada aplicação.

Isso reduz edição manual de JSON sem transformar a UI em fonte de verdade. O schema continua decidindo tipos, limites e campos válidos.

## 3. Quando faz sentido usar?

Use para comparar uma proposta de aparência notebook com a referência atual, validar rapidamente cores, tipografia, dimensões e paletas e produzir um JSON de rascunho que possa ser revisado depois.

O laboratório é especialmente útil quando a pergunta é visual — “como esta combinação fica em gráficos, KPI, tabela e cabeçalho?” — e os dados reais não são necessários para responder.

## 4. Quando não usar?

Não use como mecanismo de publicação, aprovação, autenticação ou persistência corporativa. Os botões de submissão/publicação da UI V05 ficam desabilitados por desenho.

Não use a galeria completa para `dark` ou `high_contrast` enquanto o adaptador Plotly V03 continuar limitado a `light`. O nome do modo também não certifica contraste ou acessibilidade.

Não use para avaliar significado analítico: os dados são pequenos e sintéticos e não treinam nem consultam tabelas.

## 5. Como funciona, intuitivamente?

`create_theme_lab(theme)` revalida o `ResolvedTheme` notebook e cria um rascunho isolado. `apply_updates` copia a configuração atual, converte os valores da UI, chama novamente `resolve_theme` e só troca a proposta se **todas** as alterações forem válidas. Erro preserva a última prévia válida.

`undo` retorna ao estado anterior. `restore` retorna ao ponto de partida. `export_bytes` devolve o JSON canônico em memória. `save_proposal` grava apenas um novo arquivo `.json` numa pasta explicitamente informada e se recusa a sobrescrever nomes existentes.

`build_preview` gera barras, série, mapa de calor, KPI, tabela e cabeçalho com dados sintéticos usando `aplicar_tema_resolvido`, `kpi_card_html_resolvido`, `display_styled_resolvido` e `section_header_html_resolvido`.

## 6. Exemplo de situação

Você quer experimentar uma cor principal diferente e aumentar o título de seção sem mudar o padrão da equipe:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_lab import create_theme_lab, compare_preview

rascunho = create_theme_lab(load_reference_theme("notebook"))
rascunho.apply_updates({
    "brand.primary": "#0066CC",
    "section.title_px": 20,
})
comparacao = compare_preview(rascunho)
```

A referência permanece intacta. A proposta passa por todo o contrato V02 antes de aparecer como estado válido.

## 7. O que você precisa antes de usar?

Prepare o caminho do Hub e as dependências declaradas para o Sistema de Temas. A validação continua exigindo `jsonschema` e `referencing`. A galeria requer pandas e Plotly.

Para a UI interativa em notebook Python, o Databricks recomenda `ipywidgets` em runtimes compatíveis. A versão disponível depende do runtime; o Hub não instala ou fixa `ipywidgets` automaticamente. A documentação oficial também registra que o estado de ipywidgets não é preservado entre sessões e que widgets podem renderizar de forma diferente no modo escuro do notebook.

Se `ipywidgets` não estiver disponível, `install_dbutils_fallback` cria controles nativos de texto para o conjunto primário. Esses widgets retornam strings e exigem reexecução explícita da célula que chama `apply_dbutils_fallback`.

## 8. O que este recurso entrega?

- `ThemeLabDraft`: estado e histórico isolados;
- `ControlSpec`: metadados de controle lidos do schema canônico;
- `ThemeLabPreview` e `ThemeLabComparison`: galeria sintética;
- `ProposalReceipt`: recibo local de um arquivo novo de rascunho;
- `ThemeLabUI`: referências da interface ipywidgets;
- `get_control_specs`, `create_theme_lab`, `build_preview`, `compare_preview`;
- `install_dbutils_fallback` e `apply_dbutils_fallback`;
- `build_ipywidgets_lab`.

Nenhum desses retornos equivale a aprovação ou publicação.

## 9. Como usar este recurso no Hub?

### Rota ipywidgets

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_lab import create_theme_lab, build_ipywidgets_lab

rascunho = create_theme_lab(load_reference_theme("notebook"))
ui = build_ipywidgets_lab(rascunho)
display(ui.root)
```

A aba **Escolher e ajustar** contém controles, desfazer/restaurar e exportação. A aba **Comparar** mostra Atual/Proposta. A UI não se exibe sozinha: o notebook decide quando chamar `display`.

### Fallback nativo

```python
from hub_snippets.visual.theme_lab import install_dbutils_fallback, apply_dbutils_fallback

install_dbutils_fallback(rascunho, dbutils)
# ajuste os widgets no topo e reexecute a próxima linha
apply_dbutils_fallback(rascunho, dbutils)
```

### Salvar rascunho

Só habilite gravação se houver pasta explicitamente autorizada:

```python
ui = build_ipywidgets_lab(rascunho, save_root="/caminho/autorizado/rascunhos")
```

A V05 não cria essa pasta, não sobrescreve arquivo existente e não trata o destino como publicação.

## 10. Decisões e configurações que mais importam

**Ponto de partida.** Deve ser um `ResolvedTheme` notebook. Fixtures são úteis para demonstração, não são identidade aprovada.

**Atomicidade do rascunho.** Um clique pode alterar vários campos, mas o commit local só ocorre depois que a configuração completa passa no núcleo V02.

**Controles do schema.** Unidade, descrição, tipo e limites vêm de `theme.schema.json`; a UI não altera o contrato.

**Modo.** A galeria completa V05 exige `light` porque Plotly V03 ainda é fail-closed para `dark/high_contrast`.

**Persistência.** `save_root=None` deixa Salvar desabilitado. Informar uma pasta habilita apenas criação de novo rascunho.

## 11. Limitações, riscos e armadilhas

- ipywidgets exige ambiente compatível e estado precisa ser recriado ao reabrir a sessão;
- não há autenticação de papel nem aprovação real;
- `save_proposal` é escrita de arquivo Python no destino informado, não transação Databricks nem publicação;
- a galeria não comprova responsividade, leitor de tela, zoom ou contraste percebido;
- paleta categórica alterada muda somente consumidores que efetivamente a usam;
- imagens raster e assets congelados não são recoloridos;
- o fallback dbutils não possui callbacks: mudança só entra após reexecutar a aplicação;
- `export_bytes` imprime/transporta o JSON da proposta, não um segredo nem um recibo de deploy.

## 12. Quais são as alternativas?

Para uso programático sem interface, edite uma cópia de `ResolvedTheme.to_dict()` e chame `resolve_theme` diretamente. Para parametrização simples de notebook ou jobs, use `dbutils.widgets`; para controles interativos em notebooks Python, a documentação Databricks recomenda ipywidgets.

O Databricks App planejado para sprint posterior poderá oferecer uma experiência mais estável de administração, mas não substitui o contrato central nem torna V05 uma interface de publicação.

## 13. Como saber se o resultado faz sentido?

Confira separadamente:

1. `rascunho.current` é um `ResolvedTheme` válido;
2. `dirty` muda somente após alteração válida;
3. dados dos gráficos/tabela são idênticos em Atual e Proposta;
4. erro de campo não muda `content_sha256` da última proposta válida;
5. desfazer/restaurar retorna aos hashes esperados;
6. exportação em memória não cria arquivo;
7. gravação retorna nome, SHA-256 e quantidade de bytes somente depois de fechar o arquivo;
8. `pio.templates.default` não é modificado pela galeria;
9. nenhuma ação da UI chama publicação, rede ou fonte de dados externa.

Homologação visual Databricks e teste com iniciante continuam gates humanos posteriores.

## 14. Arquivos relacionados e próximos passos

- [Núcleo `visual.tema`](../tema/README.md)
- [Adaptador Plotly V03](../theme_plotly/README.md)
- [Componentes V04](../section_header/README.md)
- [Contrato da experiência V01](../../../../../docs/sprints/sistema_temas/V01/EXPERIENCIA_LABORATORIO.md)
- [Governança V01](../../../../../docs/sprints/sistema_temas/V01/GOVERNANCA.md)
- [Checkpoint V05](../../../../../docs/sprints/sistema_temas/V05/CHECKPOINT_V05.md)

A V05 entrega laboratório em notebook. Publicação, App e AI/BI permanecem em sprints próprias.

## 15. Referências

- Databricks, **Use ipywidgets in Databricks notebooks** — documentação oficial sobre requisitos, uso e escolha entre ipywidgets e Databricks widgets.
- Databricks, **Databricks widgets** — tipos, strings, permissões e comportamento de reexecução.
- Databricks, **Known limitations of Databricks notebooks** — persistência de estado, compute e limitações de ipywidgets.
- `docs/decisions/ADR-0013-sistema-de-temas.md` — contrato central e aplicação explícita por contexto.
- `docs/sprints/sistema_temas/V01/EXPERIENCIA_LABORATORIO.md` — experiência aprovada para a futura V05.
