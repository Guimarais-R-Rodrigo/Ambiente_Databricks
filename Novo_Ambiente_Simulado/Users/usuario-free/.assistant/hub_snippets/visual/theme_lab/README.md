# `theme_lab` — laboratório de aparência do Hub

<!-- readme-objeto: 1.0.0 -->

Este recurso permite experimentar a aparência de uma proposta de notebook em uma
prévia pessoal. **Não aprova e não publica temas.** A candidata V05 ainda depende
de revisão e homologação; ela não muda o padrão da equipe nem os notebooks existentes.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Editor de rascunho visual, com comparação sintética. |
| Para que serve? | Experimentar cores, tamanhos e paletas sem consultar dados reais. |
| Quando usar? | Para preparar uma proposta de aparência de notebook. |
| Quando evitar? | Para publicar, aprovar ou certificar acessibilidade. |
| O que exige? | Pacote completo do Hub e dependências preparadas pelo mantenedor. |
| O que entrega? | Rascunho validado, prévia e JSON; gravação somente em pasta explícita. |

Primeiro acesso: [guia operacional](GUIA_PRIMEIRO_USO.md). Demonstração:
[notebook de exemplo](exemplo_theme_lab.py). Contrato executável:
[implementação](theme_lab.py) e [API pública](__init__.py).

## 1. O que é?

É a superfície de experimentação do Sistema de Temas. Um tema é um conjunto
completo de escolhas de aparência; cada escolha tem um nome técnico, chamado
token. A interface apresenta também nomes em português, como Cor principal.
O rascunho é uma cópia de trabalho em memória, não o padrão publicado do Hub.

## 2. Que problema este recurso resolve?

Permite responder “como esta proposta ficará em gráficos e tabelas?” sem editar
vários notebooks. O laboratório usa o mesmo núcleo de validação V02 e os mesmos
adaptadores Plotly/HTML V03/V04. Não recalcula indicadores de negócio.

## 3. Quando faz sentido usar?

Use para comparar a aparência de uma proposta com seu ponto de partida, preparar
uma apresentação interna ou identificar ajustes de legibilidade. As comparações
usam dados sintéticos fixos; não dependem de acesso a tabelas corporativas.

## 4. Quando não usar?

Não use como publicador, gerenciador de permissões ou aprovador de marca. Um botão
desabilitado não implementa autorização. O laboratório não oferece esses serviços.
Não interprete uma tabela sintética como análise real, nem uma paleta denominada
alto contraste como certificação de acessibilidade.

## 5. Como funciona, intuitivamente?

O laboratório recebe um `ResolvedTheme` notebook, isto é, configuração revalidada
pelo núcleo V02. Os campos da tela formam uma proposta. Aplicar valida o conjunto
completo e prepara os dois lados da galeria antes de substituir o rascunho e a saída.
Um erro nessa preparação conserva o estado anterior. Salvar/exportar é uma ação
separada e recusa campos que ainda não tenham sido aplicados.

O schema canônico fornece tipos, descrições, unidades e limites. A cobertura da
galeria é informada separadamente: controles sem demonstração correspondente ficam
desabilitados. Isso não cria outro schema nem transforma metadados em autorização.

## 6. Exemplo de situação

Para apresentar uma alternativa ao gestor, abra o laboratório preparado, escolha
outra Cor principal e clique Aplicar na prévia. Compare cabeçalhos e tabelas dos
dois lados. Para mudar cores de séries, use Paleta categórica, não Cor principal:
são escolhas diferentes. Os dados, nomes e posições das séries permanecem iguais.

## 7. O que você precisa antes de usar?

O mantenedor prepara o caminho da pasta `.assistant` e as dependências. Validar
exige `jsonschema`/`referencing`; a galeria exige pandas, Plotly e Jinja2; o painel
exige ipywidgets/IPython. Importar este módulo não instala bibliotecas nem importa
ipywidgets. A versão e a renderização no workspace precisam ser homologadas.

Para salvar, a pasta deve existir, ser explicitamente autorizada e ter permissões
controladas, inclusive nos diretórios pais. O laboratório não cria a pasta nem
descobre quem pode vê-la. Os dados usados pela galeria não precisam ser fornecidos.

## 8. O que este recurso entrega?

`ThemeLabDraft` guarda base, proposta atual, revisão local e até cem estados para
Desfazer. `dirty` compara a proposta com a base: não comprova gravação em disco.
`ControlSpec` descreve cada controle e sua cobertura. `ThemeLabPreview` contém
cabeçalho, KPI, tabela e três figuras; `ThemeLabComparison` reúne base/proposta.
`ThemeLabUI` reúne painel, controles, status e saída, sem persistir a sessão.

`export_bytes()` devolve JSON canônico. `save_proposal()` cria arquivo novo e,
somente após conferir os bytes, devolve `ProposalReceipt` com destino, nome,
SHA-256, tamanho e revisão. Esse recibo não significa submissão ou publicação.

## 9. Como usar este recurso no Hub?

Siga o [guia de primeiro uso](GUIA_PRIMEIRO_USO.md) e abra o
[exemplo](exemplo_theme_lab.py). O mantenedor preenche o caminho; a pessoa que
ajusta a aparência opera os controles. Não precisa editar os valores do código.

O exemplo demonstra criação, alteração e restauração em memória, depois abre a
interface e oferece comparação fora do painel. Não define pasta de salvamento.
Não use Executar tudo depois de começar a editar: a célula de criação reinicia
o rascunho. Nenhuma célula consulta Spark/SQL ou grava tabela.

## 10. Decisões e configurações que mais importam

A galeria completa usa contexto notebook e modo `light`. Temas `dark` e
`high_contrast` continuam sem suporte Plotly completo; não são substituídos
silenciosamente pelo tema claro. A seleção de outro ponto de partida é feita
pelo mantenedor ao construir o rascunho, não por um catálogo de presets aprovado.

A paleta categórica aparece em quatro séries fixas. A divergente chega ao mapa
de calor com escala de -1 a 1 e centro zero. Paletas e propriedades sem consumidor
nesta galeria ficam desabilitadas, com motivo. A API programática pode preparar
outros tokens válidos, mas isso não cria uma prévia deles.

Sem `save_root`, Salvar permanece desabilitado. Informar uma pasta não concede
permissão. Alterar o formulário não altera o rascunho até Aplicar. Restaurar a
base com mudanças exige confirmação, e restaurar um campo só ajusta o formulário.

## 11. Limitações, riscos e armadilhas

Não há recuperação automática da sessão, autenticação de papéis, aprovação ou
publicação. A interface não recolore PNGs nem consumidores externos. O layout e
a fonte fixa da tabela podem ter limites diferentes dos componentes HTML.

Salvar não é transação de filesystem. Falta de espaço, escrita curta ou erro de
sincronização podem deixar arquivo parcial: a operação retorna erro, não recibo,
e não apaga arquivos para tentar corrigir. O mantenedor inspeciona o destino antes
de reutilizar qualquer resíduo. A raiz precisa ser confiável; não é uma sandbox
contra outro processo que altera diretórios durante a operação.

A saída do painel usa mensagens HTML e Plotly, sem JavaScript/CDN injetado pelo
laboratório. O frontend precisa suportar esses formatos. Preparar as mensagens
em Python não comprova que o navegador as desenhou. Use a comparação fora do
painel quando necessário e registre a limitação.

## 12. Quais são as alternativas?

A [API V02](../tema/README.md) atende quem prefere manipulação programática de uma
cópia completa do tema. O fallback nativo descrito no guia fornece sete campos
primários e aplicação por reexecução de célula; não tem paridade de interface com
ipywidgets. Um App futuro não está instalado por esta entrega.

## 13. Como saber se o resultado faz sentido?

Compare os mesmos seis componentes dos dois lados, não só o gráfico de barras.
Nomes, ordem e valores precisam continuar iguais; títulos e cores podem mudar.
O exemplo informa os hashes para conferir restauração, sem tratá-los como assinatura.

Teste uma cor inválida: não deve substituir a última proposta válida. Tente salvar
sem aplicar campos novos: o laboratório deve recusar. Após salvar, confira destino,
revisão e hash. Sem mensagem de sucesso, não considere o arquivo confirmado.
Contraste, zoom, teclado, leitor de tela e uso por iniciante exigem avaliação própria.

## 14. Arquivos relacionados e próximos passos

O [guia](GUIA_PRIMEIRO_USO.md) explica acesso, botões, erros e reabertura. O
[exemplo](exemplo_theme_lab.py) demonstra operações; a [implementação](theme_lab.py)
e a [fachada](__init__.py) definem a API. O [adaptador Plotly](../theme_plotly/README.md)
e o [componente de cabeçalho](../section_header/README.md) explicam consumidores.
O [padrão de identidade visual](../../../hub_padroes/identidade_visual/README.md)
é a entrada do contrato. Todos esses links permanecem dentro do produto.

O Manual Técnico da raiz `.assistant` continua sendo o catálogo integrado.
Revisão técnica, aceite, merge e homologação do workspace são etapas distintas.

## 15. Referências

Comportamento desta candidata: [código](theme_lab.py), [API](__init__.py) e
[exemplo](exemplo_theme_lab.py). A saída registrada no exemplo é local e delimitada,
não captura de interface Databricks nem aprovação de usuário iniciante.

Documentação oficial consultada em 13/09/2026:
[ipywidgets — Output](https://ipywidgets.readthedocs.io/en/latest/reference/ipywidgets.html),
[Databricks — ipywidgets](https://docs.databricks.com/aws/en/notebooks/ipywidgets) e
[Databricks — limitações de notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-limitations).
As limitações de estado entre sessões e de frontend precisam ser verificadas no
destino; testes no GitHub Actions não as eliminam.
