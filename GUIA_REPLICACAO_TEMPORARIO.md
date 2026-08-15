# Guia de replicação — explicado passo a passo

> **Arquivo temporário.** Não está versionado no git. Apague quando terminar a
> replicação: `rm GUIA_REPLICACAO_TEMPORARIO.md`

Este guia assume que você está com **duas telas**: este arquivo aberto no
computador de casa, e o workspace do Databricks do trabalho no navegador do
outro computador. Ele explica cada passo, o que você deve ver na tela, e o que
fazer quando algo não sair como descrito.

---

## Parte 1 — Entender o que vai acontecer

### O que existe hoje no seu workspace do trabalho

Um ecossistema `.assistant` montado antes deste projeto. Ele tem problemas que a
auditoria documentou:

- seis das doze skills sem o cabeçalho de identificação, o que impede a Genie
  Code de encontrá-las;
- o arquivo de instruções salvo como `assistant_instructions.md`, **sem o ponto
  inicial** — nesse formato a Genie Code nunca o leu, então suas preferências
  nunca valeram;
- um cálculo de PSI incorreto, baseado em média e desvio;
- identificadores corporativos espalhados por vários arquivos.

### O que vai entrar no lugar

O ambiente reconstruído: doze skills com roteamento testado, biblioteca de
helpers verificada no runtime, instruções reformuladas, glossário, catálogo e
quatro notebooks didáticos.

### A ideia central da operação

Você **não** vai editar nada dentro do Databricks. Vai copiar para lá uma
subárvore de pastas já pronta, que este repositório gerou. Se algum dia precisar
mudar alguma coisa, muda aqui e repete a cópia — nunca o contrário.

Isso importa por um motivo prático: se você editar direto no workspace, a
alteração vive até a próxima cópia e depois desaparece sem aviso.

### Quanto tempo reservar

Entre uma e duas horas, contando os testes. A parte imprevisível é a Parte 4
(transporte), que depende do que a política do banco permite.

---

## Parte 2 — Preparação, aqui no computador de casa

### O que já está pronto

Conferi antes de escrever este guia:

- a versão a replicar é o commit **`ac9a782`**;
- são **174 arquivos**: 12 skills, 6 diretórios de extensão, 4 notebooks;
- a validação passou sem falhas e a publicação no laboratório está conferida.

### Onde ficam os arquivos que você vai copiar

```
C:\Users\Rodrigo\Projetos_IA\Projetos_Diversos\Ambiente_Databricks\
└── Novo_Ambiente_Simulado\
    └── Users\
        └── guimarais.r.rodrigo@gmail.com\     ← o nome desta pasta NÃO importa
            ├── .assistant_instructions.md      ← copiar este
            └── .assistant\                     ← e esta pasta inteira
```

**Ponto que confunde todo mundo na primeira vez:** o nome da pasta
`guimarais.r.rodrigo@gmail.com` é do laboratório e não deve ser recriado no
trabalho. O que você copia é o **conteúdo** dela — os dois itens marcados — para
dentro da sua pasta de usuário do trabalho.

Pense assim: essa pasta é uma caixa de mudança. Você leva o que está dentro, não
a caixa.

### Anote antes de começar

Deixe à mão, em um bloco de notas:

```
commit replicado: ac9a782
data da replicação: ____________
```

---

## Parte 3 — Backup (o passo que não pode ser pulado)

### Por que este passo existe

No trabalho você não tem a CLI do Databricks. Sem ela, **não há como desfazer
nada por comando**. Se algo der errado depois de apagar o ambiente antigo, o
backup é literalmente o único caminho de volta.

### O que fazer

1. Abra o workspace do Databricks do trabalho.
2. No navegador de arquivos à esquerda, vá até `Workspace` → `Users` → e clique
   na sua pasta de usuário.
3. Você deve ver, entre outras coisas, uma pasta chamada **`.assistant`** e um
   arquivo **`assistant_instructions.md`**.

> Se a pasta `.assistant` não aparecer, procure a opção de mostrar arquivos
> ocultos — pastas iniciadas com ponto às vezes ficam escondidas na interface.

4. Clique com o botão direito na pasta `.assistant` → procure a opção
   **Export**. O formato oferecido varia conforme a versão do workspace; aceite
   o que aparecer (costuma ser *DBC Archive* ou *Source file*).
5. Salve o arquivo baixado em uma pasta do computador do trabalho, fora do
   Databricks. Sugestão de nome: `backup_assistant_ANTES_da_replicacao.dbc`.
6. Repita para o arquivo `assistant_instructions.md`.

### Se a exportação de pasta não estiver disponível

Algumas versões só exportam arquivo por arquivo. Nesse caso, exporte cada
subpasta de `.assistant` separadamente. É chato, mas é mais rápido do que
reconstruir tudo se der problema.

### Como saber que o backup está bom

Abra o arquivo baixado. Se for `.dbc`, ele é um zip — renomeie para `.zip` e
abra para conferir que tem conteúdo dentro. Não avance sem essa conferência.

---

## Parte 4 — Levar os arquivos até o workspace

Aqui é onde a política do banco decide o caminho. Descubra qual funciona
**antes** de apagar qualquer coisa.

### Rota A — conectar o workspace ao GitHub (a melhor, se permitirem)

**Por que é a melhor:** depois de configurada, atualizar o ambiente vira um
`pull`. Nas outras rotas, toda atualização futura repete o procedimento inteiro.

1. No workspace, procure no menu lateral por **Repos** ou **Git folders**.
2. Clique em **Add** → **Git folder** (ou *Add Repo*).
3. Cole a URL do repositório:
   `https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks`
4. Se pedir autenticação, será necessário um token pessoal do GitHub.
   Gere em github.com → Settings → Developer settings → Personal access tokens,
   com permissão de leitura de repositórios.
5. Confirme. Deve aparecer uma pasta com todo o conteúdo do repositório.

**Se falhar:** anote a mensagem de erro. Se disser algo sobre bloqueio de rede
ou domínio não permitido, a política corporativa não libera GitHub e você vai
para a rota B.

**Depois do clone, atenção:** a Git folder é uma cópia do repositório, **não** é
onde a Genie Code procura as skills. Ela procura em
`/Users/<seu-usuário>/.assistant/`. Ou seja, ainda falta copiar de um lugar para
o outro — é o que a Parte 6 faz.

### Rota B — baixar e subir manualmente

1. No navegador do computador do trabalho, abra o repositório no GitHub.
2. Botão **Code** → **Download ZIP**.
3. Extraia em uma pasta local.
4. Navegue até `Novo_Ambiente_Simulado\Users\guimarais.r.rodrigo@gmail.com\`.
5. No workspace, use **Import** para subir os arquivos.

**O problema desta rota:** a importação pela interface costuma aceitar arquivos
individuais, e nem toda versão aceita pasta inteira. Se aceitar só arquivo,
serão muitas operações.

### Rota C — recriar à mão

Último recurso: criar cada pasta pela interface e subir os arquivos um a um.
São 174. Funciona, mas reserve bastante tempo.

**Anote qual rota funcionou:** ______________

---

## Parte 5 — Apagar o ambiente antigo

### Por que apagar em vez de sobrescrever

As skills novas têm os mesmos nomes das antigas. Se as duas versões convivem, a
Genie Code pode carregar a errada, e você não terá como saber qual foi.

### O que remover

Dentro de `/Users/<seu-usuário>/`:

1. A pasta **`.assistant/skills/`** inteira.
2. O arquivo **`.mcp_servers.json`**, se existir. É um arquivo herdado que não
   configura nada — contém só uma lista vazia.
3. O arquivo **`assistant_instructions.md`** (sem ponto). É o que a Genie Code
   nunca leu.

### O que NÃO remover

Qualquer notebook, pasta de projeto ou arquivo seu que esteja no diretório de
usuário e não faça parte do `.assistant`. Olhe antes de apagar.

---

## Parte 6 — Instalar

### O destino exato

```
/Users/<seu-usuário-do-trabalho>/
├── .assistant_instructions.md      ← arquivo, na raiz da sua pasta
└── .assistant/
    ├── README.md
    ├── skills/                     ← 12 pastas rodrigo-*
    ├── x_config/
    ├── x_docs/
    ├── x_projects/
    ├── x_prompts/
    ├── x_scripts/
    └── x_snippets/
```

### Como copiar, vindo da Git folder (rota A)

1. Navegue na Git folder até
   `Novo_Ambiente_Simulado/Users/guimarais.r.rodrigo@gmail.com/`.
2. Clique com o botão direito na pasta `.assistant` → procure **Copy** ou
   **Clone**.
3. Cole em `/Users/<seu-usuário>/`.
4. Repita para o arquivo `.assistant_instructions.md`.

### O erro mais comum

Copiar a pasta `guimarais.r.rodrigo@gmail.com` inteira, resultando em:

```
/Users/<seu-usuário>/guimarais.r.rodrigo@gmail.com/.assistant/    ← ERRADO
```

A Genie Code não procura aí. O certo é:

```
/Users/<seu-usuário>/.assistant/                                   ← CERTO
```

### O nome do arquivo de instruções

Confira caractere por caractere: **`.assistant_instructions.md`**, começando com
ponto. Um arquivo chamado `assistant_instructions.md` é ignorado — foi
exatamente o que aconteceu no ambiente antigo, e por isso suas preferências
nunca tiveram efeito.

---

## Parte 7 — Verificar se ficou certo

Cinco conferências. As duas últimas são as que ninguém faz e são as que mais
quebram.

### 1. As doze skills

Abra `/Users/<seu-usuário>/.assistant/skills/`. Devem aparecer doze pastas
começando com `rodrigo-`, e dentro de cada uma um arquivo `SKILL.md`.

### 2. Os seis diretórios de extensão

Em `.assistant/`, além de `skills/` e `README.md`, devem estar: `x_config`,
`x_docs`, `x_projects`, `x_prompts`, `x_scripts`, `x_snippets`.

### 3. O arquivo de instruções

Na raiz da sua pasta de usuário, com o ponto inicial.

### 4. Os `.py` da biblioteca devem ser ARQUIVO

Abra `.assistant/x_snippets/spark/pit_join.py`.

**O que você deve ver:** o código, como um arquivo de texto comum.

**O que NÃO pode aparecer:** a interface de notebook, com células e botão de
executar.

**Por que importa:** se o Databricks entender esses arquivos como notebook,
`from x_snippets...` para de funcionar e a biblioteca inteira fica inacessível.

**Se aparecer como notebook:** apague e suba de novo escolhendo a opção de
arquivo, não de notebook.

### 5. Os notebooks didáticos devem ser NOTEBOOK

Abra `.assistant/x_docs/notebooks/01_vazamento_temporal.py`.

**O que você deve ver:** a interface de notebook, com células e texto formatado.

**Por que importa:** é o oposto do item anterior. Como arquivo simples, não há
células para executar nem texto formatado para ler.

> Esses dois tipos conviverem foi um defeito que encontrei na minha própria
> ferramenta de publicação: ela mandava tudo como arquivo, e os notebooks
> ficavam inúteis.

---

## Parte 8 — Testar

O roteamento das skills já foi testado 36 vezes no laboratório e depende só do
texto de descrição, que é idêntico. O que **só o trabalho valida** é o runtime
real, as permissões e o acesso aos dados.

### Teste 1 — a skill certa é escolhida sozinha

Abra um **chat novo** na Genie Code (chat novo importa: skills não recarregam em
conversa já aberta) e cole:

```
Faça uma EDA completa da tabela catalogo.crm.clientes_pf: granularidade,
chaves, qualidade de dados, distribuições e um relatório executivo ao final.
```

**Esperado:** a interface indica que carregou `rodrigo-eda-profissional`.

A tabela não precisa existir — o teste é sobre qual skill foi escolhida, não
sobre executar. Se responder "não encontrei essa tabela", ótimo: significa que
não está inventando dados.

### Teste 2 — a menção direta funciona

Chat novo, e:

```
@rodrigo-baseline-ml rode a suite de baseline para o target inadimplencia_90d.
```

**Esperado:** carrega exatamente essa skill.

### Teste 3 — as instruções estão valendo

Em qualquer chat, faça uma pergunta técnica simples. A resposta deve vir em
português. Se vier em inglês, o arquivo de instruções não está sendo lido —
volte à Parte 6 e confira o nome.

> Detalhe oficial: instruções pessoais **não** se aplicam ao Quick Fix nem ao
> Autocomplete. Não estranhe se essas duas funções ignorarem suas preferências.

### Teste 4 — a biblioteca funciona no runtime

1. Importe o arquivo `tools/spark_smoke_test.py` (está na Git folder, ou baixe
   do repositório) **como notebook**.
2. Execute todas as células.
3. Ao final ele imprime um resumo em JSON.

**Referência do laboratório:** 64 aprovações, nenhuma falha, e sete módulos
acusando biblioteca de ML ausente.

**Diferenças esperadas no trabalho — são boas notícias, não problemas:**

| O que pode mudar | O que significa |
|---|---|
| Os sete módulos de ML param de acusar ausência | O ambiente corporativo já tem as bibliotecas |
| Somem as falhas ligadas a `cache()` | Compute clássico permite persistência; a restrição era do serverless |
| Aparece falha de permissão | Restrição do Unity Catalog, não defeito da biblioteca |

**Anote o resultado:** ______ aprovações / ______ falhas

---

## Parte 9 — Registrar

De volta ao computador de casa, me mande:

- qual rota de transporte funcionou;
- o resultado do smoke test;
- qualquer diferença que você notou em relação ao descrito aqui.

Eu registro no changelog e atualizo a matriz de diferenças entre laboratório e
trabalho — é assim que esse conhecimento fica guardado em vez de se perder.

**Importante:** nada do que for registrado pode conter seu usuário corporativo,
nome de tabela real ou caminho do banco. Se precisar mencionar, use
`<username-trabalho>`.

---

## Se algo der errado

### Rollback

Restaure o backup da Parte 3 no mesmo caminho e abra um chat novo. Como o
ecossistema é conteúdo estático — sem job agendado, sem serviço, sem escrita em
dados —, voltar atrás não deixa efeito nenhum.

### Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Nenhuma skill é carregada | Caminho errado ou pasta no lugar errado | Conferir se é `/Users/<você>/.assistant/skills/` |
| Skill aparece mas com comportamento antigo | Metadata em cache | Chat novo; se persistir, recarregar a página |
| Respostas em inglês | Instruções não estão sendo lidas | Conferir o ponto inicial no nome do arquivo |
| `ModuleNotFoundError: x_snippets` | Caminho adicionado errado | Adicionar a pasta `.assistant`, não `x_snippets` |
| `.py` abrindo como notebook | Formato errado na importação | Reimportar escolhendo arquivo |
| Não consigo exportar pasta | Versão do workspace | Exportar subpasta por subpasta |
| GitHub bloqueado | Política corporativa | Ir para a rota B |

---

## Uma ressalva honesta

Quatro módulos vão junto e são novos: `pit_join`, `join_diagnostics`,
`fixtures` e `mlflow_run`. Eles passaram por uma rodada de auditoria, que
encontrou **treze defeitos** — todos corrigidos. Mas foi uma rodada só, feita
pelo mesmo modelo que os escreveu, então é razoável supor que uma segunda
opinião encontraria mais.

Eles são opt-in: ninguém os usa sem importar explicitamente. **Evite usar o
`pit_join` em decisão que valha dinheiro até a segunda auditoria.** O resto do
ambiente — as skills, as instruções, a documentação — está bem mais testado.

---

## Ao terminar

```powershell
# de volta no computador de casa, na pasta do projeto
Remove-Item GUIA_REPLICACAO_TEMPORARIO.md
```
