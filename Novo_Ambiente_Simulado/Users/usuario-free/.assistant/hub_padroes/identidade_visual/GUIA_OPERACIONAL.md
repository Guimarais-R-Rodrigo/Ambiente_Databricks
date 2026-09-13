# Primeiro uso — conferir uma proposta sem alterar o Hub

## Antes de começar

O que existe nesta V02 é um verificador com exemplo guiado, não um painel de cores.
Seu notebook atual continua igual. A candidata precisa ser instalada e homologada
pelo mantenedor antes de ser usada no workspace de trabalho. Não publique arquivos
por conta própria para experimentar uma cor.

Quem só precisa acompanhar a entrega pode ler a seção “Interpretar a saída” abaixo.
Quem vai executar precisa de Python, do pacote completo `.assistant` e das bibliotecas
indicadas em `hub_snippets/requirements-temas.txt`. A política do seu ambiente é
que determina se uma instalação é permitida; uma mensagem de biblioteca ausente
não autoriza instalar por fora dela.

## Abrir e executar o exemplo

1. Na pasta do Hub recebida do mantenedor, abra
   `hub_snippets/visual/tema/exemplo_tema.py` como notebook ou arquivo Python.
   No repositório, essa pasta fica sob `ambiente_fonte/.assistant/`.
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
uma pasta, compartilhar, aprovar e publicar são ações distintas. O laboratório
e a gestão dessas ações serão entregues em sprints posteriores.

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

## Usar a rota V04 em um componente HTML

A V04 é opt-in. Resolva/carregue primeiro um tema notebook íntegro; depois passe-o à função `_resolvido` do componente. Exemplo:

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

Para voltar ao comportamento anterior, use a função sem `_resolvido`; não é necessário limpar um tema global porque a V04 não cria um.

## Para pedir ajuda

Informe ao mantenedor o código do erro, a etapa executada e a versão do pacote.
Não envie dados de clientes, credenciais, paths corporativos ou conteúdo integral
sensível. O guia de erros indica o significado sem repetir o valor recebido.
A execução da demonstração foi verificada em Python/CI conforme o checkpoint;
Databricks, Windows, acessibilidade e teste com iniciante precisam de evidência
própria antes de serem declarados homologados.

[Voltar ao padrão](README.md) · [Abrir o exemplo](../../hub_snippets/visual/tema/exemplo_tema.py)
