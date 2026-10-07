# `visual.tema` — conferir uma configuração antes de mudar a aparência

> **CUSTOMIZADO PELO HUB · O NÚCLEO NÃO APLICA CORES SOZINHO.** Valida uma proposta; consumidores aplicam explicitamente, sem aprovar identidade ou publicar arquivos.

<!-- readme-objeto: 1.0.0 -->

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Leitor e verificador de configurações visuais completas. |
| Para que serve? | Conferir se uma proposta pode ser interpretada com segurança. |
| Quando usar? | Preparação de tema e integração explícita de consumidores. |
| Quando evitar? | Para mudar um gráfico agora ou autorizar uma publicação. |
| O que exige? | Pacote completo, Python compatível e dependências de validação. |
| O que entrega? | Configuração isolada, identificadores de integridade e avisos. |

Comece pelo [exemplo guiado](exemplo_tema.py). Ele só lê referências sintéticas,
trabalha em memória e imprime resultados. A [implementação](tema.py) não consulta
Spark nem grava arquivos. Uma execução local não certifica o Databricks.

## 1. O que é?

Um tema descreve escolhas de apresentação, como uma cor e o tamanho de um título.
Este recurso verifica uma dessas descrições antes de outro componente utilizá-la.
“Resolver” significa produzir um retrato completo e isolado desses valores;
não significa desenhar uma figura ou aplicar a escolha em toda a equipe.

## 2. Que problema este recurso resolve?

“Esta proposta está completa, usa opções permitidas e continua correspondendo
à versão que recebi?” O núcleo recusa erros explícitos e permite identificar
qual conteúdo foi conferido. Um erro não aciona outro tema silenciosamente.

## 3. Quando faz sentido usar?

Use na preparação de uma proposta para gráficos, cabeçalhos e materiais editoriais. O núcleo permite conferir uma configuração em Python sem compute Spark ou dados de clientes. Escolha o próximo componente pelo efeito:

| Necessidade | Componente | Efeito |
|---|---|---|
| Validar/serializar | `visual.tema` | configuração isolada/bytes em memória |
| Aplicar em figura | [theme_plotly](../theme_plotly/README.md) | altera a figura recebida; registro é outra chamada |
| Aplicar em HTML/tabela | rotas `_resolvido` dos componentes | retorna string com tema explícito |
| Experimentar/comparar | [theme_lab](../theme_lab/README.md) | rascunho e prévia; persistência apenas quando solicitada em pasta autorizada |

## 4. Quando não usar?

Não use para publicar uma identidade, conceder acesso ou modificar um dashboard.
Um tema válido pode não ser legível ou adequado à marca. Por exemplo, chamar
uma configuração de “alto contraste” não certifica que ela seja acessível.
Para Plotly, há rota legada e integração opt-in com
[`theme_plotly`](../theme_plotly/): somente um `ResolvedTheme` explícito é consumido
pela API nova. Isso não migra gráficos existentes nem transforma a validação em aprovação.

## 5. Como funciona, intuitivamente?

O núcleo lê dados JSON, uma notação textual de campos e valores. Verifica tamanho,
formato, campos, contexto, compatibilidade e integridade dos recursos empacotados.
Depois devolve uma configuração imutável: a cópia de uma pessoa não muda a de outra.
Todos os valores vêm do documento; não existe herança, precedência entre arquivos,
preenchimento oculto ou busca de “latest”. O schema é a lista central das regras.

## 6. Exemplo de situação

Na preparação de uma reunião, você recebe uma proposta que troca o azul principal.
A demonstração carrega uma referência sintética, cria uma cópia e troca uma cor.
As duas configurações podem ser conferidas separadamente, sem treinar um modelo
ou mudar um gráfico. Um terceiro caso remove um campo e mostra a recusa esperada.
O aviso de não aprovação acompanha inclusive a proposta que passou na validação.

## 7. O que você precisa antes de usar?

Leia o [roteiro operacional](../../../hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).
É necessário que o pacote completo esteja disponível, não só o arquivo `tema.py`.
Para validar, o mantenedor prepara as dependências de
[`requirements-temas.txt`](../../requirements-temas.txt). O import e a função
`normalize_color` usam somente a biblioteca padrão; a validação importa
`jsonschema` e `referencing` na chamada. Nenhuma função instala bibliotecas.

Os arquivos devem estar em uma pasta com permissão de leitura e controle de
escrita. Não são necessários tabelas, credenciais, target ou dados bancários.
O mantenedor deve confirmar Python e bibliotecas no workspace antes de homologá-lo.

## 8. O que este recurso entrega?

`ResolvedTheme` contém `tokens` e `origins` somente de leitura, `warnings`, `source`
e hashes de conteúdo, origem e dependências. `to_dict()` produz uma cópia editável.
Listas dentro de `tokens` são tuplas imutáveis. `content_sha256` identifica o JSON
normalizado; `raw_sha256` identifica os bytes recebidos. Em entrada por dicionário,
o segundo identifica sua serialização, pois não existiram bytes de arquivo.

`fingerprint` combina conteúdo, schema, manifesto e protocolo de serialização.
Nenhum hash autentica o autor, concede permissão ou aprova uma publicação.
`export_theme` retorna bytes em memória; salvar esses bytes é outra ação.

## 9. Como usar este recurso no Hub?

Abra o [notebook de exemplo](exemplo_tema.py) e leia a primeira célula. Confira
onde o pacote está instalado; não use `%run` ou copie o código interno. Execute
as células na ordem descrita. O exemplo não instala dependências nem cria dados.
Em Python com `.assistant` já no caminho de importação:

```python
from hub_snippets.visual.tema import load_reference_theme, export_theme
referencia = load_reference_theme("notebook")
print(referencia.tokens["brand.primary"])
proposta_em_memoria = export_theme(referencia)
```

O azul esperado nessa referência é `#005CA9`. Isso confere um valor de exemplo,
não a aparência de uma tela. Instruções de instalação do Hub continuam no
[README do produto](../../../README.md).

Assinaturas de consulta, carga e serialização:

- `resolve_theme(value: bytes | dict[str, Any], *, expected_context: str | None=None)`
- `load_theme(root: str | Path, relative_path: str, *, expected_sha256: str | None=None, expected_context: str | None=None)`
- `load_reference_theme(context: str='notebook')`
- `export_theme(theme: ResolvedTheme)`

`resolve_theme` recebe bytes JSON estritos ou `dict` já construído; `load_theme` lê `.json` sob raiz explícita; `export_theme` devolve bytes `hub-json-v1`, sem salvar. Contextos aceitos: `notebook`, `readme`, `presentation`. Aceitação pelo schema não garante suporte de um consumidor. Consulte os [erros e recuperação](../../../hub_padroes/identidade_visual/ERROS.md).

## 10. Decisões e configurações que mais importam

`expected_context` impede usar uma configuração de notebook onde se espera material
editorial. `load_theme(root, relative_path)` exige uma raiz escolhida explicitamente
e um nome relativo `.json`. Seu `expected_sha256` compara os bytes da revisão,
sem substituí-los por outra versão. O [contrato central](../../../hub_padroes/identidade_visual/README.md)
explica a serialização e os limites. `normalize_color` é uma ajuda explícita de
autoria; a importação não corrige uma cor inválida em silêncio.

## 11. Limitações, riscos e armadilhas

Este núcleo não contém UI, adapter, banco de propostas, aprovação ou publicação. [theme_lab](../theme_lab/README.md) e [theme_plotly](../theme_plotly/README.md) são componentes separados. As referências
são testes, não presets aprovados para produção. A checagem de arquivos recusa
atalhos simbólicos e arquivos especiais, mas não é sandbox contra um processo
hostil capaz de substituir pastas pais simultaneamente; use permissões controladas.
O fingerprint não é um mecanismo criptográfico de assinatura de autor.

Não há cache: cada chamada relê os recursos para não reutilizar conteúdo alterado.
Isso privilegia previsibilidade nesta versão; não há meta de latência homologada.
A serialização `hub-json-v1` não declara implementação do RFC 8785 nem garantia
interlinguagens. PNGs continuam estáticos e nenhum recurso é recolorido.

## 12. Quais são as alternativas?

As [constantes atuais](../../constants/colors/) e o helper
[`theme_plotly`](../theme_plotly/) atendem aos usos legados e seguem preservados.
Para autoria assistida, use [theme_lab](../theme_lab/README.md). O [App](../../../hub_padroes/identidade_visual/databricks_app/README.md) prepara propostas e a [ponte AI/BI](../../../hub_padroes/identidade_visual/aibi/README.md) prepara candidatos locais; não concedem aprovação ou publicação.

## 13. Como saber se o resultado faz sentido?

Confira o contexto, o valor de referência, os avisos e a quantidade de tokens.
Exporte, reimporte e compare `fingerprint`: a exportação canônica deve conservar
os valores. Altere a cópia retornada por `to_dict()` e veja que o original não
muda. Remova `brand.primary`: a recusa deve indicar `SCHEMA_REQUIRED`, sem completar
o campo. A demonstração percorre essas verificações, mas não substitui revisão
visual, teste com iniciante ou homologação de runtime.

## 14. Arquivos relacionados e próximos passos

[Implementação](tema.py), [fachada pública](__init__.py) e
[exemplo](exemplo_tema.py) compõem este objeto. O [padrão central](../../../hub_padroes/identidade_visual/README.md)
é o dono das regras; o [guia de erros](../../../hub_padroes/identidade_visual/ERROS.md)
orienta correções. O [Manual Técnico](../../../MANUAL_TECNICO_V2.md#catalogo-helpers)
continua sendo o catálogo integrado. Para aplicar, siga [theme_plotly](../theme_plotly/README.md); para experimentar, siga [theme_lab](../theme_lab/README.md).

## 15. Referências

As assinaturas e efeitos são definidos pela implementação e fachada acima.
A referência dos parâmetros deriva do schema, não de uma segunda lista manual.
Consulta técnica em 12/09/2026: [JSON em Python](https://docs.python.org/3/library/json.html)
e [resolução de schemas](https://python-jsonschema.readthedocs.io/en/stable/referencing/).
Validação de contrato não certifica renderização, acessibilidade ou usabilidade no Databricks; cada consumidor e destino exigem conferência própria.
