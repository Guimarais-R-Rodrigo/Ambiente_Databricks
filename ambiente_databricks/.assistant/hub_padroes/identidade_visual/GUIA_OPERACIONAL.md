# Primeiro uso — conferir uma proposta sem alterar o Hub

## Antes de começar

Escolha sua tarefa: validar uma proposta no núcleo, aplicar em um consumidor, experimentar no laboratório, usar o App autorizado ou preparar um candidato AI/BI. Carregar uma configuração não troca o caminho legado nem modifica um notebook automaticamente.

Use somente o pacote instalado pelo procedimento autorizado e conferido no destino. Não publique arquivos por conta própria para experimentar uma cor. A ponte AI/BI trabalha localmente, não chama Databricks, não publica dashboard e não torna `context="aibi"` válido.

Quem vai executar precisa de Python, do pacote completo `.assistant` e das bibliotecas
indicadas em [requirements-temas.txt](../../hub_snippets/requirements-temas.txt). A política do seu ambiente é
que determina se uma instalação é permitida; uma mensagem de biblioteca ausente
não autoriza instalar por fora dela.

## Abrir e executar o exemplo

1. Na pasta do Hub recebida do mantenedor, abra
   `hub_snippets/visual/tema/exemplo_tema.py` como notebook ou arquivo Python.
2. Leia a célula de preparação. Se a localização não for descoberta, preencha
   `HUB_ROOT` com o caminho da própria pasta `.assistant`, copiado da interface
   do seu ambiente. Não informe o caminho de uma tabela ou de um arquivo JSON.
3. Execute somente a preparação. Se houver erro, pare e consulte
   [Erros e recuperação](ERROS.md). Não execute células seguintes fora da ordem.
4. Execute “Referência”: deve aparecer contexto `notebook`, 48 tokens e azul
   `#005CA9`, além dos avisos de que nada foi aprovado ou aplicado.
5. Execute “Cópia e exportação”: a proposta passa a usar `#112233`; o original
   continua azul. A comparação “Mesmo conteúdo” deve ser verdadeira. Tudo fica
   em memória.
6. Execute “Erro esperado”: a retirada de `brand.primary` produz `SCHEMA_REQUIRED`.
   Esse erro é intencional; demonstra a proteção, não uma falha de instalação.

O exemplo não consulta dados, não treina modelos, não cria tabelas, não grava
arquivos, não registra templates e não publica. A preparação altera apenas o
caminho de importação do processo Python para localizar o pacote escolhido.

## Interpretar a saída

`tokens` são escolhas com nome e valor. `origins` registra qual documento forneceu
cada escolha. `warnings` lembra os limites: validar não aplica e não aprova.
`fingerprint` identifica a configuração efetiva e suas dependências. Ele não diz
se a paleta é bonita, acessível ou autorizada. Compare-o somente entre versões
compatíveis do protocolo descrito no [contrato](README.md).

Não confunda `export_theme` com salvar: ele devolve bytes em memória. Salvar em
uma pasta, compartilhar, aprovar e publicar são ações distintas. O laboratório pode persistir sessão/proposta em pasta autorizada e a geração editorial pode produzir variantes candidatas, mas nenhuma dessas ações equivale a aprovar ou publicar um tema. Publicação e homologação no workspace continuam gates separados.

## Carregar um arquivo da sua pasta autorizada

O mantenedor pode usar `load_theme(root, "proposta.json", expected_sha256=...)`.
A raiz é escolhida pelo código confiável, não pelo JSON. O nome é relativo à raiz;
URLs, `..`, atalhos simbólicos e arquivos especiais são recusados. Use a revisão
exata recebida; retirar a checagem de hash para fazer uma proposta diferente
passar elimina a verificação pretendida.

Para desistir da experiência, descarte as variáveis ou reinicie a sessão conforme
a rotina do seu ambiente. Nenhum resultado analítico nem padrão compartilhado
precisa ser restaurado, porque este núcleo não os modifica. Uma cópia editável
é obtida com `to_dict()`, não alterando os dados internos do resultado.

## Aplicar tema em um componente HTML

A aplicação é opt-in. Resolva/carregue primeiro um tema notebook íntegro; depois passe-o à função `_resolvido` do componente. Exemplo:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.section_header import section_header_html_resolvido

tema = load_reference_theme("notebook")
html = section_header_html_resolvido(
    tema,
    titulo="Resumo",
    descricao="Base sintética.",
)
```

A referência mantém a aparência histórica. Outras configurações completas podem mudar somente propriedades cobertas pelo contrato. Não passe dicionário cru, não edite `_values` e não use a função como folha de estilo global. `dark` e `high_contrast` são materializáveis no HTML quando válidos, porém isso não constitui homologação visual ou de acessibilidade.

Para voltar ao comportamento anterior, use a função sem `_resolvido`; não é necessário limpar um tema global porque essa rota não cria um.

## Experimentar no Visual Lab

Para editar/comparar uma proposta sem mudar o padrão da equipe, abra `hub_snippets.visual.theme_lab`. Ele parte de configuração notebook validada, aplica alterações de forma atômica e compara Atual/Proposta com dados sintéticos. Salvar uma sessão preserva trabalho; não publica nem aprova o tema.

## Aplicar nos consumidores disponíveis

Quando um consumidor documentar uma rota `_resolvido`, carregue primeiro um `ResolvedTheme` íntegro e passe-o explicitamente. Exemplos incluem `plot_correlation_resolvido`, `plot_distributions_resolvido`, curvas de ML, timeline de monitoramento, UMAP e safras. A rota temática muda somente propriedades visuais cobertas; dados, agregações, amostragem, métricas e thresholds permanecem os mesmos.

SHAP/Matplotlib e Kaplan–Meier continuam exceções explícitas ao theming atual. Não assuma suporte apenas porque outras figuras do notebook usam um tema.

## Material editorial

A geração orientada por tema recebe um derivado controlado do `ResolvedTheme` e produz candidatos fora do pacote visual ativo. Gerar um asset não o promove. Preserve hashes/recursos congelados e siga o fluxo de revisão antes de qualquer substituição.

## Usar o App de autoria

O [guia de primeiro uso do App](databricks_app/GUIA_PRIMEIRO_USO.md) explica a interface. Ela reaproveita o Visual Lab para escolher uma base, ajustar, comparar, salvar e reabrir a própria sessão.

A superfície é `authoring_only`: não existe botão para aprovar, publicar, promover ou apagar histórico. O modo de desenvolvimento local não substitui autenticação Databricks. Um deploy real continua exigindo autorização separada, recurso `theme_storage` apontando para Unity Catalog Volume e permissões reais no workspace.

Antes de usar, o responsável precisa confirmar identidade encaminhada, acesso ao Volume e funcionamento da interface nesse destino. A presença dos arquivos não comprova essas condições.

## Preparar um candidato AI/BI

Para entender o fluxo de AI/BI, abra o [guia de primeiro uso AI/BI](aibi/GUIA_PRIMEIRO_USO.md). A ponte recebe somente um `ResolvedTheme` `notebook` íntegro e produz uma projeção auditável dos 48 tokens: traduzidos, aproximados ou não suportados.

A projeção `hub-aibi-theme-projection` **não é** o JSON nativo aceito pelo botão `Import theme`. Como o schema completo desse arquivo não está publicado nas fontes oficiais verificadas, a ponte não inventa campos. Um candidato nativo só pode ser criado sobre um export real, com SHA-256 fixado e JSON Pointers revisados para campos já existentes; aproximações nunca são aplicadas automaticamente.

O tema do workspace e o tema local do dashboard também não são intercambiáveis. Gerenciar o tema do workspace exige administrador; um dashboard existente recebe snapshot ao aplicar o workspace theme e mudanças futuras não se propagam automaticamente. Publicar dashboard permanece ação separada e não é implementada pela ponte.

## Para pedir ajuda

Informe ao mantenedor o código do erro, a etapa executada e a versão do pacote.
Não envie dados de clientes, credenciais, paths corporativos ou conteúdo integral
sensível. O guia de erros indica o significado sem repetir o valor recebido.
Testes Python não comprovam interface Databricks, acessibilidade ou experiência de uso no seu ambiente; registre a condição efetivamente observada.

[Voltar ao padrão](README.md) · [Abrir o exemplo](../../hub_snippets/visual/tema/exemplo_tema.py)
