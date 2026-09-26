# Cabeçalhos CRM e Squad

Cabeçalhos editoriais aprovados, compartilhados entre guias e notebooks.
São identidade visual do projeto, não logotipos nem recursos nativos da Databricks.

## CRM — guias e notebooks gerais

![CRM — Missão Modelos Analíticos CRM](png/cabecalho_crm.png)

Texto: **CRM** · **Missão Modelos Analíticos CRM**.

Um único PNG atende aos dois usos. O formato de 1920 × 480 px cria uma faixa
horizontal: preserva espaço para o conteúdo e permite leitura a partir de
720 px de largura sem reduzir o menor texto abaixo de 18 px.

## Squad — notebooks específicos

![Squad Modelos Analíticos e Preditivos](png/cabecalho_squad.png)

Texto: **Squad Modelos Analíticos e Preditivos**. As quebras de linha mantêm a
frase exata e o tamanho da tipografia. Este banner substitui o de CRM quando
a identificação específica da Squad é a apropriada; não empilhe os dois.

## Uso no Markdown e em notebooks

O [suporte oficial a imagens de workspace](https://docs.databricks.com/aws/en/notebooks/notebook-media)
permite caminhos relativos ou absolutos em células Markdown. Não é necessário
iniciar compute, usar Mermaid ou executar `displayHTML` para exibir o PNG.

Em um documento localizado nesta pasta, o cabeçalho CRM usa:

```markdown
![CRM — Missão Modelos Analíticos CRM](./png/cabecalho_crm.png)

# Título do documento
```

Em uma célula Markdown de notebook localizado nesta pasta:

```markdown
%md
![Squad Modelos Analíticos e Preditivos](./png/cabecalho_squad.png)

# Título do notebook
```

Em outro diretório, ajuste o caminho a partir do documento consumidor, mantendo
o arquivo central. Publique a árvore de assets junto do documento. Imagens
embutidas não são importações Python, nem usam o prefixo de links entre notebooks.

### Acessibilidade e contexto textual

- Mantenha título, finalidade, instruções e exemplos em Markdown normal. A
  identificação nunca deve ser a única informação legível fora dos pixels.
- Preserve alt descritivo; se toda a identificação estiver imediatamente
  repetida em texto, pode usar alt vazio para tratar o banner como decorativo.
- Não dependa de leitura de imagens pela IA para regras, paths ou critérios de
  aceite. A Genie Code pode usar contexto visual, mas o texto continua explícito.
- As conexões da arte são decorativas: não representam execução, permissões,
  disponibilidade de serviços ou automação do Hub.

## Manutenção sem cópias concorrentes

| Local | Papel | Como alterar |
|---|---|---|
| `src/fundo_tecnologico_original.png` | arte raster original sem texto | nova proposta visual, preservando a referência aprovada |
| `src/copy.json` | textos, pesos, cores e posicionamento | editar o texto exato e regenerar |
| `src/*_tipografia.svg` | camada tipográfica gerada | não editar manualmente |
| `png/` | dois arquivos finais usados pelos documentos | regenerar, conferir e publicar |
| `manifest.json` e `qa/` | hashes e verificações | gerados pelo compositor |

Comando de autoria, na raiz do repositório:

```powershell
node tools/readme_visuals/headers.mjs
```

O fundo foi gerado pela ferramenta nativa de imagem e congelado como entrada;
a composição e a tipografia Inter são determinísticas. Não existe um SVG da
ilustração completa. A [proveniência](src/PROMPT_FUNDO.md) e a
[licença Inter](../licenses/Inter-OFL.txt) acompanham os arquivos.
