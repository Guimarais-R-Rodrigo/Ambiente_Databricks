# Manual: trechos realocados para manutenção


Baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`. Texto anterior preservado para rastreabilidade; os números de etapas e estados abaixo não são atuais. A enumeração atual de CI é `tools/ci_local.py::ETAPAS` (12 etapas verificadas nesta implementação). Rotina vigente: [ciclo de vida](../../playbooks/ciclo-de-vida.md). Links dos trechos foram fixados ao snapshot original.


## R0392 — linhas [11, 13]

**Base documental e estrutural atual:** a iniciativa R00–R13 de READMEs foi encerrada no Git em `99e01012c26621539b4379ca301e4782765f68c0`, com 75/75 objetos operacionais, 3/3 exemplares e zero pendências. A R13 auditou coerência documental e regressões locais; não recertificou toda afirmação externa da plataforma. As explicações sobre Databricks continuam apoiadas na documentação oficial consultada em **11/09/2026** e devem ser verificadas novamente quando uma capacidade, interface ou versão puder ter mudado. Exemplos com dados são sintéticos; saída esperada não prova execução no workspace de destino.

**Manutenção de uma única redação:** a versão de autoria fica em `ambiente_fonte/.assistant/MANUAL_TECNICO.md`. O arquivo homônimo da raiz do repositório é uma cópia de leitura do mesmo conteúdo; o simulado recebe a cópia produzida pelo renderer. Não mantenha redações divergentes. As referências de implementação ao final apontam para o snapshot examinado, para não transformar uma alteração futura em evidência retroativa.



## R0393 — linhas [54, 60]

A migração estrutural dos READMEs de objeto foi concluída na R11: os 75 objetos
operacionais possuem guia local, e os três exemplares permanecem contabilizados
separadamente. Para `hub_snippets`, seis índices de categoria — `constants`,
`display`, `ml`, `spark`, `testing` e `visual` — oferecem uma rota intermediária
entre este Manual, o catálogo geral e cada objeto. Novos objetos continuam
devendo incluir o guia. O molde está no caminho lógico
`hub_padroes/readme/template_objeto.md`, relativo à raiz `.assistant/`.



## R0394 — linhas [86, 117]

### 2.1. Repositório, produto, simulado e workspace

O **repositório Git** é o conjunto versionado de arquivos: produto, documentação, ferramentas e histórico. Um **commit** identifica uma versão desse conjunto. A raiz do Git é o primeiro nível do repositório, não necessariamente o local de onde um notebook importa suas bibliotecas.

`ambiente_fonte/` guarda o produto que será distribuído. Dentro dela, `.assistant_instructions.md` é irmão da pasta `.assistant/`: ele não fica dentro de `skills/`. A pasta `.assistant/` contém os componentes usados pelo Hub.

`Novo_Ambiente_Simulado/` é uma árvore de arquivos que reproduz a organização de destino. **“Simulado” aqui não significa um Databricks rodando localmente.** O diretório não fornece compute, tabelas ou uma Genie Code local. Ele facilita conferir e copiar os arquivos certos para os lugares certos.

O **workspace Databricks** é o ambiente operacional: interface, arquivos, notebooks, recursos de dados, configurações e permissões. O conteúdo publicado lá é uma cópia operacional. Uma alteração feita somente no workspace não atualiza o Git; uma mudança no Git tampouco se publica sozinha por existir um commit.

```text
Repositório Git
  ambiente_fonte/                       fonte editável do produto
    .assistant_instructions.md          instruções pessoais
    .assistant/
      README.md                         entrada do Hub
      MANUAL_TECNICO.md                  explicação técnica e consulta
      skills/                           métodos
      hub_prompts/                      briefings
      hub_snippets/                     biblioteca reutilizável
      hub_scripts/                      utilitários
      hub_micromodelos/                 contratos, execução e exemplos de domínio
      hub_padroes/                       moldes
      hub_readmes_visual_assets/        recursos visuais

  Novo_Ambiente_Simulado/                árvore gerada, não um servidor
    Users/usuario-free/
      .assistant_instructions.md
      .assistant/...
```

A organização de manutenção do Git também inclui `tools/`, `docs/` e os arquivos de instruções dos agentes. Esses arquivos de controle não são widgets nem componentes a copiar indiscriminadamente para o workspace. A consolidação deste manual não significa que o projeto inteiro deva ser reduzido a dois arquivos.



## R0395 — linhas [304, 308]

### 6.4. API pública não é descoberta automática pela IA

A ferramenta de manutenção `tools/api_publica.py` lê a árvore sintática do módulo, sem importá-lo, e identifica funções, classes e nomes definidos no topo que não começam por `_`. Ela ajuda a conferir reexportações. Não registra funções no Databricks e não chama uma API remota para instalar a biblioteca.

Há uma regra local importante: o inventário da API pública não inclui apenas funções “mais interessantes”. Constantes e outros nomes públicos também podem ser usados por outro módulo. O leitor iniciante pode começar pelos pontos de entrada recomendados; o mantenedor precisa preservar o contrato completo.



## R0396 — linhas [351, 351]

No checkout local, use o endereço da pasta `ambiente_fonte/.assistant` dentro da sua cópia. Evite criar um “bootstrap universal” que tente vários diretórios silenciosamente: ele pode encontrar uma cópia antiga e produzir sucesso aparente.



## R0397 — linhas [598, 598]

O cabeçalho CRM e o cabeçalho Squad têm papéis definidos pelo projeto. Este manual não muda essas escolhas, não substitui figuras existentes e não transforma recursos visuais em execução. A página pode permanecer visualmente idêntica enquanto a documentação técnica é consolidada.



## R0398 — linhas [1043, 1047]

### 22.4. Por que `expected-host` é importante

O publicador do projeto pode escrever centenas de objetos. A proteção `--expected-host` exige que o destino resolvido corresponda ao host pretendido. Isso reduz a chance de confundir laboratório e trabalho. Ela não transforma a operação em transação atômica, não aprova o conteúdo e não substitui um backup.

O modo de plano do publicador integral não escreve arquivos no remoto, mas resolve a identidade e o destino por ferramentas autenticadas. Não deve ser descrito como comando inteiramente offline. Já o renderer local não precisa de credencial Databricks. Essa diferença explica por que um plano de publicação pode falhar por autenticação mesmo sem `--execute`.



## R0399 — linhas [1060, 1084]

## 23. Da alteração no Git ao arquivo que aparece no Databricks

### 23.1. Commit, branch e sincronização

**Git** registra versões de arquivos. Um **commit** identifica um conjunto de alterações no histórico; seu SHA funciona como identificador. **Branch** é uma referência móvel para uma linha de trabalho. **Push** envia mudanças ao repositório remoto. **Pull request** propõe integrar uma linha de trabalho em outra. Fazer commit não publica automaticamente os arquivos no Databricks.

Um ambiente pode consumir uma pasta Git sincronizada ou receber arquivos por outra ferramenta. Este projeto possui seu próprio fluxo de renderização e publicação. Portanto, não presuma que “está na `main`” significa “está no workspace” ou que “rodei no workspace” significa “a alteração está no Git”.

### 23.2. O renderer local

O comando abaixo apenas mostra o plano:

```powershell
python tools/render_simulado.py
```

O seguinte **apaga e recria a árvore derivada local** `Novo_Ambiente_Simulado/` a partir de `ambiente_fonte/`:

```powershell
python tools/render_simulado.py --write
```

O renderer copia `.assistant_instructions.md` e a pasta `.assistant/`, excluindo caches locais conhecidos. Gera a estrutura de usuário sanitizada e o aviso `README_GERADO.md`. Não cria workspace, não envia API remota, não inicia Spark e não altera permissões. Qualquer edição manual no derivado pode ser perdida; a autoria deve permanecer na fonte.

O README de `ambiente_fonte/` e o README da raiz Git são documentos de manutenção: não entram nesse plano de cópia. O Manual Técnico de `.assistant/` entra por estar dentro da subárvore publicada. A cópia de leitura da raiz Git não é enviada separadamente.



## R0400 — linhas [1086, 1092]

### 23.3. FILE e NOTEBOOK: a extensão não basta

No workspace, um módulo Python deve permanecer importável como arquivo. Um notebook tem células e metadados de notebook. Ambos podem ser exportados com extensão `.py`, mas um notebook SOURCE possui marcadores, como `# Databricks notebook source`, `# COMMAND ----------` e `# MAGIC`.

As ferramentas do projeto usam esse marcador para classificar. Na publicação, notebooks são importados com formato SOURCE; arquivos de biblioteca precisam continuar FILE. Importar indiscriminadamente todo `.py` como notebook quebra a expectativa de importação. Renomear uma extensão não é uma conversão fiel de objeto. Os formatos de importação/exportação são contratos das operações de workspace. [S17](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/MANUAL_TECNICO.md#fonte-s17)

Também não se deve confundir `RAW` de importação com uma opção universal de exportação. O fluxo escolhido pelas ferramentas diferencia formato solicitado, tipo de objeto e bytes exportados. Leia a implementação antes de substituir comandos de publicação.



## R0401 — linhas [1094, 1123]

### 23.4. Planejar, executar e verificar

Estes comandos são documentação operacional, **não foram executados para publicar este manual**. Substituições de perfil e host só devem ocorrer no ambiente autorizado, sem salvar credenciais no Git.

```powershell
# Resolve o destino e mostra o plano, sem publicar.
python tools/publicar_free.py --profile PERFIL --expected-host https://HOST

# Escreve no laboratório explicitamente conferido.
python tools/publicar_free.py --profile PERFIL --expected-host https://HOST --execute

# Consulta/exporta e compara conteúdo; não publica uma nova versão.
python tools/publicar_free.py --profile PERFIL --expected-host https://HOST --verify --conteudo --relatorio .artifacts/verificacao.json
```

O publicador é específico do fluxo do laboratório. O modo de execução exige destino explícito e confere fonte/espelho antes de enviar. `--verify` e `--execute` não se combinam; `--rapido` é uma conferência reduzida de contagem e não pode representar comparação integral de conteúdo. O JSON de relatório registra a verificação, não a execução de cada análise.

**Exclusão no Git não implica exclusão no workspace.** Se uma publicação anterior enviou o catálogo e o glossário, removê-los da fonte e regenerar o simulado não prova que as cópias remotas desapareceram. O publicador não deve ser tratado como um sincronizador que apaga indiscriminadamente tudo o que sobrou. Qualquer retirada remota exige conferência de escopo, autorização e tratamento explícito. Este trabalho não executa essa retirada no seu workspace.

### 23.5. Manifesto, hash e pacote de implantação

Um **manifesto** relaciona o que pertence ao pacote. Um **hash SHA-256** resume bytes para comparação de integridade: mudar um byte altera o resultado esperado. Igualdade de hashes não prova que a regra de negócio esteja correta, apenas que se está comparando o mesmo conteúdo sob aquele mecanismo.

`tools/bundle_implantacao.py` produz um ZIP do produto derivado com `MANIFEST.json`. O manifesto registra caminhos, tamanhos, hashes, commit e condição do worktree. Um worktree **dirty** possui alterações ainda não commitadas; `--allow-dirty` existe para revisão, não para fingir uma versão imutável de produção.

```powershell
python tools/bundle_implantacao.py --output .artifacts/pacote-revisado.zip
```

Esse ZIP não é uma wheel Python. **Wheel**, geralmente `.whl`, é um formato de distribuição de pacote Python; o ZIP de implantação organiza arquivos do workspace. Descompactar um pacote de workspace não equivale a instalar todas as dependências de sua biblioteca.



## R0402 — linhas [1125, 1135]

### 23.6. Jobs, DAGs e Bundles

Um **job** coordena uma ou mais tarefas. Dependências entre tarefas formam um grafo; quando não há ciclos, chama-se DAG. Uma tarefa pode depender do sucesso de outra, mas retries, agendamento, identidade e políticas precisam ser configurados. Lakeflow Jobs é um recurso da plataforma; não é ativado pela criação de uma pasta `hub_scripts/`. [S31](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/MANUAL_TECNICO.md#fonte-s31)

**Declarative Automation Bundles** é a denominação atual do recurso anteriormente conhecido como Databricks Asset Bundles. Ele descreve recursos como código e apoia implantação organizada. Não confunda esse produto com o `bundle_implantacao.py` local: o nome parecido não significa que o script implemente o recurso nativo. [S32](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/MANUAL_TECNICO.md#fonte-s32)

### 23.7. Mudança segura e rollback

Antes de publicar, delimite objetos, ambiente, identidade e critérios de aceite. Mantenha evidência da versão anterior e da nova. **Rollback** é voltar deliberadamente a uma versão adequada; não é simplesmente executar outra vez um comando que falhou pela metade.

Uma operação pode gravar alguns arquivos e falhar depois. Na dúvida, inspecione o estado e o recibo antes de repetir. **Idempotência** significa que repetir uma operação sob as mesmas condições não acrescenta efeitos indesejados. Não se deve assumir essa propriedade para um job inteiro apenas porque uma das funções é determinística.



## R0403 — linhas [1140, 1167]

### 24.1. CI não é CSI e não é `sys.path`

**CI**, integração contínua, executa verificações de código e estrutura associadas a mudanças no repositório. **CSI**, discutido no capítulo 18, é uma medida de mudança de distribuição utilizada em monitoramento. **`sys.path`** é a lista de caminhos da importação Python. Nenhum é sinônimo dos outros.

**CD** pode significar entrega ou implantação contínua, conforme o processo. Um repositório ter GitHub Actions não prova que exista implantação automática. Neste snapshot, o gate local é deliberadamente separado de publicação e testes que exigem credenciais.

### 24.2. O que o gate atual executa

```powershell
python tools/ci_local.py --verbose
```

O comando usa o Python local e executa três etapas: validação de `ambiente_fonte/` com conferência das contagens do README; testes de regressão da biblioteca; e testes das ferramentas. Continua pelas etapas para apresentar mais de uma falha, em vez de esconder problemas posteriores.

As dependências desse gate estão em `tools/requirements-dev.txt`. A instalação desse arquivo é uma ação separada. Ele não prepara automaticamente o workspace Databricks nem testa todos os treinadores opcionais.

```powershell
python -m pip install -r tools/requirements-dev.txt
python tools/validate_assistant.py --conferir-readme
```

`python -m pip` vincula o instalador ao interpretador Python escolhido. Evita parte da confusão de ter vários `pip` no computador. Ainda é necessário conferir qual `python` foi resolvido pelo terminal.

### 24.3. AST: ler a estrutura do código sem executá-lo

**AST**, árvore de sintaxe abstrata, representa a estrutura de um programa: funções, argumentos, chamadas e expressões. `ast.parse` pode detectar sintaxe inválida e apoiar verificações de contratos sem iniciar Spark ou importar dependências pesadas.

A ferramenta `tools/api_publica.py` usa estrutura de código para inventariar nomes públicos e apoiar `__init__.py`. Ela não cria endpoints REST. O validador usa AST para examinar módulos e exemplos, mas uma análise estática não prova tipos em execução, acessibilidade de tabelas, correção estatística ou compatibilidade de um serviço remoto.



## R0404 — linhas [1169, 1187]

### 24.4. Teste unitário, regressão, integração e smoke

Um **teste unitário** exercita uma unidade pequena com entradas controladas. Um **teste de regressão** procura impedir que um comportamento corrigido volte a quebrar. **Integração** verifica componentes atuando juntos. **Smoke test** testa operações básicas para revelar falhas amplas de ambiente ou integração; não é validação exaustiva de todos os casos.

O projeto possui ferramentas de smoke Spark/ML e roteiros de teste conversacional. Elas não são equivalentes ao gate offline. Uma simulação ou mock de MLflow testa o código que usa a interface, não a conexão real, a autorização ou a persistência no serviço.

**Skip** indica caso não executado. “A suíte terminou sem falhas, com casos ignorados” não deve ser relatado como se todos tivessem passado em runtime. Registre o que foi executado, a versão, o ambiente e o motivo dos casos ausentes.

### 24.5. Contrato de documentação e limite da evidência

Um link válido demonstra que o destino referenciado existe na verificação; não garante que seu conteúdo esteja correto. Um PNG com hash esperado demonstra integridade; não garante legibilidade. Um bloco de saída presente em Markdown demonstra que foi escrito; não prova sozinho sua execução. Um teste de importação não exercita a função, e uma resposta bem redigida não prova carregamento da skill.

Neste projeto, resultados de validação exibidos no README são confrontados por `--conferir-readme`. Quando um documento é acrescentado ou removido, as contagens podem mudar sem que haja regressão de algoritmo. Devem ser atualizadas a partir da execução, não ajustadas por tentativa até desaparecer o erro.

### 24.6. Como registrar uma evidência útil

Uma evidência deve permitir entender versão, contexto e limite. Registre commit ou versão dos arquivos; ambiente/runtime; comando ou célula; entrada ou recorte; saída observada; critério esperado; resultado da comparação; e o que não foi coberto. Preserve o erro real quando a verificação falhar, removendo apenas informações sensíveis de modo declarado.

Separe quatro estados: **explicação hipotética**, **resultado esperado por cálculo**, **execução observada** e **execução revisada segundo critérios**. Não converta uma simulação em execução real mediante alteração da legenda.



## R0405 — linhas [1246, 1246]

| CI reprova contagens do README | Evidência documental ficou desatualizada | Reexecutar gate e conferir alteração de inventário |



## R0406 — linhas [1258, 1289]

Este inventário cobre as 52 pastas de snippets da candidata V05 e os sete scripts do snapshot examinado. A unidade contada é a pasta de objeto, não o número de funções: um objeto pode exportar várias funções, classes ou constantes. Os dois exemplares de padrões são apresentados separadamente. Nomes e assinaturas abaixo foram extraídos das definições Python, sem executar treinadores nem importar dependências opcionais.

**Como usar:** procure a finalidade, leia o tipo de entrada e de retorno, abra o exemplo específico e só então adapte a chamada. A assinatura é uma referência de consulta; os capítulos 4 a 7 explicam sua notação. Ela não substitui a docstring, os testes ou a revisão de efeitos. As dependências citadas nas fichas destacam pontos de atenção, não constituem um lockfile completo. Nenhuma ficha significa “homologado hoje no seu workspace”.

Para navegar pelos snippets antes de chegar à ficha técnica, use os seis índices de categoria pelos caminhos lógicos `hub_snippets/constants/README.md` · `hub_snippets/display/README.md` · `hub_snippets/ml/README.md` · `hub_snippets/spark/README.md` · `hub_snippets/testing/README.md` · `hub_snippets/visual/README.md`. Eles agrupam os mesmos objetos por natureza do problema e não substituem este inventário. Os caminhos são mostrados como texto porque este Manual tem cópias idênticas em diretórios diferentes; os links clicáveis ficam na entrada `.assistant/README.md` e no catálogo `hub_snippets/README.md`.

As referências de código são permalinks do snapshot, iguais nas cópias Git e workspace deste manual. Abrir esses links depende de acesso ao repositório privado. Dentro do workspace, o caminho local equivalente começa em `.assistant/` e conserva a subpasta exibida na ficha.

**Guias locais R02:** os pilotos agora possuem `README.md` na própria pasta.
Nas fichas abaixo, o caminho do guia é relativo à pasta `.assistant/`, não à
localização de uma das três cópias deste Manual. Os READMEs das coleções oferecem
links clicáveis dentro do produto. Essa convenção evita links relativos que
funcionariam na cópia canônica, mas quebrariam na cópia da raiz. A revisão é
documental e tem evidência delimitada; não representa publicação no workspace.

### 27.0. Preflight e governança de execução

#### `hub_scripts.skill_execution`

Guia conceitual e de decisão: `hub_scripts/skill_execution/README.md` (a partir de `.assistant/`).

Resolve `execution_contract.json` antes do core analítico e devolve um `PreflightResult` estruturado com `PASS` ou `BLOCKED`, decisões por recurso/template, issues bloqueantes e `writes_performed=false`. Na SE02, `run_preflight` avalia apenas pré-condições objetivas: não executa a EDA, não chama helpers analíticos e não prova aderência posterior.

A API pública inclui `run_preflight` e, desde a SE07, `get_skill_enforcement_policy`/`list_skill_enforcement_policies` para consultar a política transversal de nível por skill. O registry fica em `hub_padroes/skill_enforcement/policy.json`. `current_level` descreve somente enforcement implementado; `target_level` é roadmap e não prova existência de gates. O contrato v0.1 continua em `mode="audit"`; condição usada pelo contrato sem contexto explícito bloqueia o preflight em vez de ser tratada silenciosamente como falsa.

Desde a SE08, contratos e policy participam do validador geral do Hub e o gate
local chama o perfil cumulativo `se08` do certifier em modo parcial/read-only.
A certificação FULL permanece separada e usa
`python -B tools/skill_enforcement/certify_local.py --profile se08`: ela inclui
regressões SEF acumuladas, renderer canônico, ausência de drift no derivado e
snapshot documental. O subgate do `ci_local.py` não substitui esse FULL.




## R0407 — linhas [1302, 2157]

**Guia local do objeto (R03-A):** na pasta `hub_snippets/constants/colors/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_colors.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Reúne cores e paletas usadas na apresentação. São valores de configuração visual, não variáveis aprendidas pelo modelo nem regras de aprovação. Consumir uma constante não desenha uma figura sozinho.

Constantes exportadas: `AZUL_CAIXA`, `LARANJA`, `AZUL_CLARO`, `CINZA_ESCURO`, `VERDE`, `VERMELHO`, `ROXO`, `TEAL`, `LARANJA_ESCURO`, `CINZA_MEDIO`, `PALETA_CATEGORICA`, `PALETA_SEQUENCIAL`, `PALETA_DIVERGENTE`, `COR_POSITIVO`, `COR_NEGATIVO`, `COR_NEUTRO`, `COR_ALERTA`, `BG_SECTION`, `BG_HEADER`, `TEXTO_PRINCIPAL`, `TEXTO_SECUNDARIO`, `BORDA_CAIXA`.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/colors/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py)

#### `hub_snippets.constants.emojis`

**Guia local do objeto (R03-A):** na pasta `hub_snippets/constants/emojis/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_emojis.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Relaciona símbolos e seções da apresentação. Um emoji de alerta é um recurso de comunicação; não executa um teste e não comprova gravidade estatística.

Constantes exportadas: `SECOES_EDA`, `SEMANTICA`.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/emojis/emojis.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/emojis/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/emojis/exemplo_emojis.py)

#### `hub_snippets.constants.format_br`

Guia conceitual e de decisão: `hub_snippets/constants/format_br/README.md` (a partir de `.assistant/`).

Transforma números em texto brasileiro para apresentação: inteiro, percentual, moeda, decimal, diferença e número abreviado. Retorna strings, não números prontos para continuar o cálculo. Declare a escala de percentuais; `fmt_int` trunca entradas fracionárias. `fmt_int` e `fmt_n` não garantem precisão para inteiros muito grandes; o guia local documenta um caso de perda de unidade.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
fmt_int(n: Number) -> str
fmt_pct(v: float, casas: int=1, input_scale: Literal['ratio', 'percent']='ratio') -> str
fmt_brl(v: float) -> str
fmt_dec(v: float, casas: int=4) -> str
fmt_delta(v: float, unidade: str='pp') -> str
fmt_n(n: Number, sufixo: bool=True) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/format_br/format_br.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/format_br/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py)

#### `hub_snippets.constants.styles`

**Guia local do objeto (R03-A):** na pasta `hub_snippets/constants/styles/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_styles.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Reúne estilos visuais reutilizáveis e depende das constantes de cores do Hub. CSS controla aparência; não calcula indicadores nem altera permissões do notebook.

Constantes exportadas: `FONT_FAMILY`, `STYLE_SECTION_HEADER`, `STYLE_KPI_CARD`, `STYLE_DIVIDER_LIGHT`, `STYLE_DIVIDER_HEAVY`, `STYLE_BADGE_OK`, `STYLE_BADGE_WARN`, `STYLE_BADGE_FAIL`, `STYLE_INDEX_ITEM`.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/styles/styles.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/styles/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py)

### 27.2. Tabelas e distribuições

#### `hub_snippets.display.correlation_matrix`

**Guia local do objeto (R03-B):** na pasta `hub_snippets/display/correlation_matrix/`, abra `README.md` antes de `exemplo_correlation_matrix.py`. O guia distingue conceito, contrato, efeitos e interpretação; as referências históricas abaixo permanecem vinculadas à sua base.

Recebe um DataFrame Spark e colunas numéricas. Calcula correlações e devolve a figura Plotly e os pares fortes, não apenas uma figura isolada. Depende de APIs de `pyspark.ml`; confira suporte no compute e tratamento de nulos. Correlação não é causalidade. O corte seleciona a lista de pares, não destaca células; o descarte de nulos é conjunto nas colunas selecionadas.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_correlation(df: DataFrame, cols: Optional[Iterable[str]]=None, method: str='pearson', threshold_highlight: float=0.8)
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/correlation_matrix.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/exemplo_correlation_matrix.py)

#### `hub_snippets.display.dataframe_styled`

**Guia local do objeto (R03-B):** na pasta `hub_snippets/display/dataframe_styled/`, abra `README.md` antes de `exemplo_dataframe_styled.py`. O guia distingue conceito, contrato, efeitos e interpretação; as referências históricas abaixo permanecem vinculadas à sua base.

Recebe uma tabela pandas e devolve HTML estilizado. O consumidor escolhe onde mostrar esse texto. A operação de estilo delegada ao pandas pode exigir Jinja2 na chamada; o módulo carregar não prova essa dependência. O helper não ativa escape HTML; use conteúdo controlado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
display_styled(df_pandas, highlight_cols: Optional[Iterable[str]]=None, format_dict: Optional[Dict[str, str]]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/exemplo_dataframe_styled.py)

#### `hub_snippets.display.distribution_grid`

**Guia local do objeto (R03-B):** na pasta `hub_snippets/display/distribution_grid/`, abra `README.md` antes de `exemplo_distribution_grid.py`. O guia distingue conceito, contrato, efeitos e interpretação; as referências históricas abaixo permanecem vinculadas à sua base.

Recebe DataFrame Spark, seleciona/amostra dados numéricos e devolve uma figura Plotly com distribuições. Confirme tamanho da amostra e leitura das escalas; os histogramas não representam uma contagem integral se vieram de amostra. Valores selecionados são coletados em pandas e incorporados à figura; N conta linhas coletadas, não valores válidos por coluna.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_distributions(df: DataFrame, cols: Optional[Iterable[str]]=None, ncols: int=3, sample_n: int=10000)
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/distribution_grid.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/exemplo_distribution_grid.py)

### 27.3. Operações Spark

#### `hub_snippets.spark.date_features`

**Guia local do objeto (R04-A):** `hub_snippets/spark/date_features/README.md` explica conceito, decisão de uso, custo e limites antes do notebook.

Recebe Spark DataFrame e coluna de data; devolve atributos de calendário. A implementação embute nove feriados nacionais de data fixa em indicador próprio; isso não é calendário completo. Feriados móveis, locais, bancários ou regras do projeto entram separadamente em `holiday_dates`.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
extrair_features_data(df: DataFrame, col_data: str, prefixo: Optional[str]=None, *, holiday_dates: Optional[Sequence[str]]=None) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/date_features/date_features.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/date_features/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/date_features/exemplo_date_features.py)

#### `hub_snippets.spark.join_diagnostics`

**Guia local do objeto (R04-A):** `hub_snippets/spark/join_diagnostics/README.md` explica conceito, decisão de uso, custo e limites antes do notebook.

Recebe dois Spark DataFrames e uma chave, possivelmente composta; devolve dicionário de cardinalidade, correspondência e estimativa de expansão. Não materializa o join completo, mas executa agregações de diagnóstico. Conferir um relacionamento não cria correspondências ausentes.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
diagnosticar_join(esquerda: DataFrame, direita: DataFrame, chave: str | Sequence[str], *, amostra_orfas: int=5) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/join_diagnostics.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py)

#### `hub_snippets.spark.null_summary`

**Guia local do objeto (R04-A):** `hub_snippets/spark/null_summary/README.md` explica conceito, decisão de uso, custo e limites antes do notebook.

Recebe Spark DataFrame e devolve uma tabela por coluna com contagens, percentuais e status de `NULL`. As expressões não substituem regras de domínio para strings vazias, sentinelas ou NaN. Os limiares são política do consumidor e a implementação atual não valida sua ordem/faixa.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
null_summary(df: DataFrame, threshold_warn: float=5, threshold_fail: float=20) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/null_summary.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/exemplo_null_summary.py)

#### `hub_snippets.spark.pit_join`

Guia conceitual e de decisão: `hub_snippets/spark/pit_join/README.md` (a partir de `.assistant/`).

Recebe fatos e histórico de features Spark, chave e tempos, incluindo atraso obrigatório de publicação. Devolve `(dados, diagnostico)`. Impede usar versões indisponíveis sob o modelo temporal informado; atraso fixo não comprova a disponibilidade real se a fonte publica de forma irregular.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
pit_join(fatos: DataFrame, features: DataFrame, chave: str | Sequence[str], ts_decisao: str, ts_feature: str, *, atraso_publicacao_dias: int, janela_maxima_dias: Optional[int]=None, colunas_feature: Optional[Sequence[str]]=None, sufixo: str='', politica_empate: str='erro', devolver_disponibilidade: bool=False) -> Tuple[DataFrame, Dict[str, Any]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/pit_join.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py)

#### `hub_snippets.spark.psi_calculator`

**Guia local do objeto (R04-A):** `hub_snippets/spark/psi_calculator/README.md` explica conceito, decisão de uso, custo e limites antes do notebook.

Recebe Spark DataFrames e calcula PSI/CSI. `calcular_psi` devolve um float; `calcular_csi`, um dicionário por coluna; `interpretar_psi`, texto segundo limiares do consumidor. A guarda de cardinalidade categórica protege coleta no driver, mas não elimina todo custo distribuído.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calcular_psi(df_base: DataFrame, df_atual: DataFrame, col: str, n_bins: int=20) -> float
calcular_csi(df_base: DataFrame, df_atual: DataFrame, feature_cols: List[str], n_bins: int=20, max_categorias: int=LIMITE_CATEGORIAS_CSI) -> Dict[str, float]
interpretar_psi(psi_value: float, *, warning_threshold: Optional[float]=None, critical_threshold: Optional[float]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/psi_calculator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py)

#### `hub_snippets.spark.safe_display`

**Guia local do objeto (R04-A):** `hub_snippets/spark/safe_display/README.md` explica conceito, decisão de uso, custo e limites antes do notebook.

Mostra uma quantidade limitada de linhas sem solicitar contagem integral apenas para exibir. Retorna `None`; não é uma função de amostragem que devolve dados para treino. Passe `display_fn=display` quando o renderer estiver disponível no notebook: o módulo não herda suas variáveis globais. Em execução local simples, forneça um renderer compatível ou espere a exceção documentada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
safe_display(df: DataFrame, limit: int=1000, msg: bool=True, *, display_fn: Optional[Callable[[DataFrame], None]]=None) -> None
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/safe_display.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/exemplo_safe_display.py)

#### `hub_snippets.spark.smart_sample`

**Guia local do objeto (R04-A):** `hub_snippets/spark/smart_sample/README.md` explica conceito, decisão de uso, custo e limites antes do notebook.

Recebe Spark DataFrame e devolve amostra limitada por `n`, com opção estratificada. O modo simples usa `sample` e `limit`: `n` é teto e a saída pode ter menos linhas. No estratificado elegível, a alocação busca exatamente `n` e preserva cada estrato; uma amostra de inspeção não é automaticamente apropriada para estimação.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
smart_sample(df: DataFrame, n: int=10000, stratify_col: Optional[str]=None, seed: int=42) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/smart_sample.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/exemplo_smart_sample.py)

### 27.4. Modelagem, tempo, métricas e monitoramento

#### Guias locais R06 — como montar uma avaliação temporal sem misturar as camadas

Para um usuário começando no Hub, a ordem conceitual recomendada é: **(1) construir features sem futuro → (2) definir partições/gaps → (3) avaliar em um ou vários cortes → (4) ajustar e comparar candidatos**. Os objetos R06 não formam um pipeline automático; cada um cobre uma parte:

- `hub_snippets/ml/lgbm_temporal/README.md` — lags/rollings/calendário em pandas; não treina LightGBM;
- `hub_snippets/ml/split_temporal/README.md` — um split treino/validação/teste por períodos observados;
- `hub_snippets/ml/walk_forward/README.md` — vários folds expansivos; o callback faz o treino;
- `hub_snippets/ml/arima_wrapper/README.md` — candidato auto-ARIMA; métricas retornadas são in-sample;
- `hub_snippets/ml/prophet_wrapper/README.md` — candidato Prophet; atenção a feriados e grão agregado.

`gap` e `gap_periods` não descobrem a maturação do target. Eles contam períodos observados da base e precisam ser configurados de acordo com o processo real. Métrica in-sample, validação temporal e teste final são evidências diferentes. Todos esses helpers operam no driver.

#### `hub_snippets.ml.arima_wrapper`

Recebe série NumPy ordenada, ajusta auto-ARIMA e devolve modelo, previsões e métricas. Requer frequência e período sazonal coerentes; lacunas temporais não são inferidas pela posição do array. Pmdarima é exigido na chamada e MLflow é importado no módulo.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_arima(series: np.ndarray, m: int=12, forecast_periods: int=6, seasonal: bool=True, log_mlflow: bool=True) -> Tuple
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/arima_wrapper.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/exemplo_arima_wrapper.py)

#### Guias locais R08 — clusterização, anomalias e explicabilidade

Para um usuário novo, escolha primeiro a **pergunta**:

- `hub_snippets/ml/clustering_suite/README.md` — criar/comparar agrupamentos numéricos; `best_k` é heurística;
- `hub_snippets/ml/cluster_profiling/README.md` — descrever grupos já rotulados; `z_score` local não é teste estatístico;
- `hub_snippets/ml/umap_viz/README.md` — visualizar vizinhanças em 2D; a geometria não é medida fiel do espaço original;
- `hub_snippets/ml/autoencoder_anomaly/README.md` — priorizar anomalias por erro de reconstrução; percentil não é probabilidade;
- `hub_snippets/ml/shap_explainer/README.md` — calcular atribuições do output do modelo;
- `hub_snippets/ml/explainability_report/README.md` — transformar importâncias já calculadas em Markdown.

Use as rotas em conjunto somente quando os contratos realmente se encaixarem. A R08 documenta o estado existente; não migra `umap_viz` para a rota V04 de temas e não altera implementações.

#### `hub_snippets.ml.autoencoder_anomaly`

Recebe arrays de treino apresentados como normais e dados a avaliar. Devolve rede treinada, limiar e erros de reconstrução. PyTorch é exigido ao importar. O limiar não é uma probabilidade de fraude; o treino pode ser custoso e depende da preparação dos atributos.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
class Autoencoder
    __init__(self, input_dim: int, encoding_dim: int=16, hidden_dims: list=None) -> None
    forward(self, x: torch.Tensor) -> torch.Tensor
train_autoencoder_anomaly(X_train_normal: np.ndarray, X_test: np.ndarray, encoding_dim: int=16, epochs: int=100, batch_size: int=256, lr: float=0.001, patience: int=10, threshold_percentile: float=95.0, log_mlflow: bool=True) -> Tuple[Autoencoder, float, np.ndarray]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/autoencoder_anomaly.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py)

#### `hub_snippets.ml.cluster_profiling`

Recebe pandas com atributos e grupos já definidos. Devolve perfis tabulares e diferenças de um grupo em relação ao conjunto. Não cria os clusters; interpreta a segmentação previamente fornecida e exige cuidado com grupos pequenos.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
profile_clusters(df: pd.DataFrame, feature_cols: List[str], cluster_col: str='cluster_id') -> pd.DataFrame
top_differentiators(profiles_df: pd.DataFrame, cluster_id: int, top_n: int=5) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/cluster_profiling.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py)

#### `hub_snippets.ml.clustering_suite`

Avalia quantidades de grupos ou executa agrupamento sobre dados pandas/NumPy. Devolve dicionário com resultados, incluindo modelo e informações de agrupamento conforme a operação. Escala dos atributos muda as distâncias; métricas internas não certificam utilidade comercial. Pode registrar MLflow.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
select_k(X_scaled: np.ndarray, k_range: range=range(2, 11), method: str='both') -> Dict[str, object]
run_clustering_pipeline(df: pd.DataFrame, feature_cols: List[str], k: Optional[int]=None, k_range: range=range(2, 11), algorithm: str='kmeans', scaler: str='standard', log_mlflow: bool=True) -> Dict[str, object]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/clustering_suite.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py)

#### `hub_snippets.ml.curves_plotly`

Recebe rótulos e scores já calculados e devolve figuras ROC, Precision–Recall, lift e KS. Uma curva é um objeto Plotly, não uma implantação ou um teste causal. Preserve classe positiva, população, amostra e tratamento de empates.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_roc_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva ROC', show_auc: bool=True, n: Optional[int]=None) -> go.Figure
plot_pr_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva Precision-Recall', n: Optional[int]=None) -> go.Figure
plot_lift_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva de Lift', n_bins: int=10, n: Optional[int]=None) -> go.Figure
plot_ks_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva KS', n: Optional[int]=None) -> go.Figure
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/exemplo_curves_plotly.py)

#### `hub_snippets.ml.drift_detection`

Calcula PSI numérico, KS e estabilidade categórica sobre NumPy/pandas; também organiza relatório por feature. As referências definem bins/categorias e os limiares de classificação são política do consumidor. Não confundir o CSI escalar desta interface com o dicionário por feature da versão Spark.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calculate_psi(reference: np.ndarray, current: np.ndarray, n_bins: int=10, eps: float=1e-06) -> float
calculate_ks(reference: np.ndarray, current: np.ndarray) -> Tuple[float, float]
calculate_csi(reference: pd.Series, current: pd.Series, eps: float=1e-06) -> float
detect_drift_all_features(df_reference: pd.DataFrame, df_current: pd.DataFrame, feature_cols: List[str], numeric_cols: Optional[List[str]]=None, categorical_cols: Optional[List[str]]=None, psi_threshold: Optional[float]=None, ks_threshold: Optional[float]=None, *, severe_psi_threshold: Optional[float]=None, severe_ks_threshold: Optional[float]=None, min_non_null: int=10) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/drift_detection.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/exemplo_drift_detection.py)

#### `hub_snippets.ml.explainability_report`

Recebe evidências de importância e, quando fornecidos, valores SHAP e dados correspondentes. Devolve texto Markdown executivo ou técnico. Não calcula sozinho SHAP nem descobre significado de negócio das colunas. A geração de tabelas Markdown pode exigir `tabulate` na chamada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
generate_executive_report(shap_importance: pd.DataFrame, feature_business_names: Dict[str, str], target_description: str, model_metric: float, metric_name: str='AUC', shap_values: Optional[np.ndarray]=None, X: Optional[np.ndarray]=None, feature_names: Optional[List[str]]=None) -> str
generate_technical_summary(shap_importance: pd.DataFrame, native_importance: Optional[pd.DataFrame]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/explainability_report.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py)

#### `hub_snippets.ml.isolation_forest`

Guia conceitual e de decisão: `hub_snippets/ml/isolation_forest/README.md` (a partir de `.assistant/`).

Ajusta detector sobre pandas e devolve dicionário de modelo, scores, rótulos e estatísticas. `profile_anomalies` organiza os casos sinalizados. Requer scikit-learn e importa MLflow no módulo; contaminação é configuração, não taxa de fraude comprovada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_isolation_forest(df: pd.DataFrame, feature_cols: List[str], contamination: float=0.01, n_estimators: int=200, max_samples: str='auto', scaler: str='standard', log_mlflow: bool=True) -> Dict[str, object]
profile_anomalies(df: pd.DataFrame, feature_cols: List[str], scores: np.ndarray, labels: np.ndarray, top_n: int=50) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/isolation_forest.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py)

#### Guias locais R07 — score, maturidade e sobrevivência

Para um usuário novo no Hub, separe as perguntas antes de escolher o objeto:

- `hub_snippets/ml/score_bands/README.md` — diagnosticar como eventos se distribuem ao longo do score; `aprovacao_acum` é cobertura, não política pronta;
- `hub_snippets/ml/woe_iv_calculator/README.md` — WOE/IV de uma feature **já discretizada** em Spark;
- `hub_snippets/ml/scorecard_builder/README.md` — converter WOE + coeficientes em tabela de pontos; não aplica binning nem pontua linhas novas;
- `hub_snippets/ml/vintage_analysis/README.md` — comparar safras no mesmo MOB sem preencher maturidade ausente;
- `hub_snippets/ml/kaplan_meier/README.md` — descrever tempo até evento com censura;
- `hub_snippets/ml/survival_cox/README.md` — associações de hazard ajustadas sob riscos proporcionais.

Taxa acumulada de safra, função de sobrevivência, probabilidade de evento, hazard, odds e pontos são grandezas diferentes. Os helpers organizam cálculos; eles não escolhem política, causalidade ou aprovação regulatória.

#### `hub_snippets.ml.kaplan_meier`

Recebe pandas com duração e indicador de evento; devolve curvas Plotly ou resultado do teste log-rank. Lifelines é utilizado nas funções. Censura, duração e grupos precisam estar corretamente definidos antes da comparação.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_kaplan_meier(df: pd.DataFrame, duration_col: str, event_col: str, group_col: Optional[str]=None, title: str='Curva de Sobrevivência (Kaplan-Meier)', ci: bool=True) -> go.Figure
log_rank_test(df: pd.DataFrame, duration_col: str, event_col: str, group_col: str) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/kaplan_meier.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/exemplo_kaplan_meier.py)

#### `hub_snippets.ml.lgbm_ranker`

Recebe arrays e tamanhos dos grupos para ajustar e avaliar um ranking LightGBM. Retorna modelo e métricas no treino e dicionário na avaliação. LightGBM e MLflow integram as dependências de importação. Não trate o score de ranking como probabilidade calibrada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_lgbm_ranker(X_train: np.ndarray, y_train: np.ndarray, groups_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, groups_val: np.ndarray, params: Optional[Dict]=None, num_boost_round: int=500, early_stopping_rounds: int=50, log_mlflow: bool=True) -> Tuple[lgb.Booster, Dict[str, float]]
evaluate_ranking(model: lgb.Booster, X: np.ndarray, y: np.ndarray, groups: np.ndarray, ks: Optional[List[int]]=None) -> Dict[str, float]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/lgbm_ranker.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/exemplo_lgbm_ranker.py)

#### `hub_snippets.ml.lgbm_temporal`

Apesar do nome, cria atributos temporais em pandas; não treina LightGBM. Produz lags, janelas e atributos de calendário. Respeite entidade, formato de data e política de datas duplicadas. As primeiras linhas podem sair por falta de histórico para os atributos criados.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
create_temporal_features(df: pd.DataFrame, target_col: str, date_col: str, lags: Optional[List[int]]=None, rolling_windows: Optional[List[int]]=None, calendar_features: bool=True, entity_cols: Optional[Sequence[str]]=None, *, date_format: Optional[str]=None, on_duplicate_dates: str='raise') -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/lgbm_temporal.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py)

#### `hub_snippets.ml.metrics_report`

Recebe arrays de valores observados e previstos. Devolve dicionários de métricas. Na classificação, as chaves incluem `auc_roc`, `ks_pct`, `gini`, `auc_pr`, `brier_score`, `f1`, `precision`, `recall`, `lift_10pct` e `prevalence`. KS está em escala percentual; a maioria das demais medidas não. Na regressão, `mape` é percentual e exclui observações cujo valor real é zero.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calculate_binary_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float=0.5) -> Dict[str, float]
calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/metrics_report.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/exemplo_metrics_report.py)

#### `hub_snippets.ml.mlflow_run`

Abre contexto de registro MLflow e entrega coletor com métodos de parâmetros, métricas, modelo e artefato. MLflow ausente é detectado ao iniciar a operação. Requer destino de tracking autorizado; há escrita e possíveis resíduos de run incompleto. O capítulo 21 explica os limites do controle de completude.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
run_governado(nome: str, *, dataset: str, split: str, limitacoes: Iterable[str], experimento: Optional[str]=None, exigir_completo: bool=True) -> Iterator[_RunGovernado]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/mlflow_run.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py)

#### `hub_snippets.ml.mlp_embeddings`

Oferece classe de rede e treinador para entradas numéricas e categóricas separadas. Devolve rede e métricas. Índices de categoria e dimensões dos vocabulários precisam corresponder; categorias novas exigem política. PyTorch é uma dependência de importação, e o treino pode registrar MLflow.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
class EmbeddingMLP
    __init__(self, n_numeric: int, cat_dims: List[int], emb_dims: Optional[List[int]]=None, hidden_layers: Optional[List[int]]=None, dropout: float=0.3, task: str='binary')
    forward(self, x_num: torch.Tensor, x_cat: List[torch.Tensor]) -> torch.Tensor
train_embedding_mlp(X_num_train: np.ndarray, X_cat_train: List[np.ndarray], y_train: np.ndarray, X_num_val: np.ndarray, X_cat_val: List[np.ndarray], y_val: np.ndarray, cat_dims: List[int], epochs: int=50, batch_size: int=512, lr: float=0.001, patience: int=10, log_mlflow: bool=True) -> Tuple[EmbeddingMLP, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/mlp_embeddings.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/exemplo_mlp_embeddings.py)

#### `hub_snippets.ml.optuna_lgbm`

Recebe arrays de treino/validação e orçamento de busca. Devolve os parâmetros selecionados e o objeto Study do Optuna. Não retorna automaticamente um modelo final já aprovado. A função objetivo e a população de validação determinam o que foi otimizado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
optimize_lgbm(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', n_trials: int=50, metric: str='auc', timeout: Optional[int]=None) -> Tuple[Dict, optuna.Study]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/optuna_lgbm.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/exemplo_optuna_lgbm.py)

#### `hub_snippets.ml.performance_monitor`

Oferece extração de métricas de um relatório e uma classe para comparar desempenho com uma referência. Devolve estruturas de acompanhamento conforme o método chamado. Exige política de métricas e direção de piora; não configura por si só alerta externo, job ou retreino.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
selecionar_metricas_do_relatorio(relatorio: Dict[str, Any], politica: Optional[Dict[str, Any]]=None, *, metricas_obrigatorias: Optional[List[str]]=None) -> Dict[str, float]
class PerformanceMonitor
    __init__(self, baseline_metrics: Dict[str, float], model_name: str='model', *, policy: Optional[Dict[str, Dict[str, Any]]]=None, consecutive_alert_periods: int=3, require_complete_metrics: bool=True) -> None
    add_period(self, period: str, metrics: Dict[str, float], n_predictions: int=0) -> None
    get_current_status(self) -> str
    should_retrain(self) -> Dict[str, object]
    generate_report(self) -> str
    plot_timeline(self, metric: str) -> Any
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/performance_monitor.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/exemplo_performance_monitor.py)

#### `hub_snippets.ml.prophet_wrapper`

Recebe pandas com data e valor, ajusta Prophet e devolve modelo, DataFrame de previsão e métricas de ajuste na própria amostra. Essas métricas in-sample não substituem teste temporal fora do treino; MAPE também exige atenção a valores reais zero. A biblioteca Prophet é importada dentro da função; MLflow e outras dependências do topo continuam necessárias para carregar o módulo. Horizonte, frequência e feriados precisam representar o caso real.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_prophet(df: pd.DataFrame, ds_col: str='ds', y_col: str='y', periods: int=12, freq: str='MS', yearly: bool=True, weekly: bool=False, country_holidays: str='BR', changepoint_prior: float=0.05, log_mlflow: bool=True) -> Tuple
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/prophet_wrapper.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/exemplo_prophet_wrapper.py)

#### `hub_snippets.ml.score_bands`

Recebe scores e eventos observados e devolve pandas por faixa. Empates podem afetar grupos. `higher_score_is_better` exige uma interpretação coerente da direção do score. Decis e labels não são segmentos comerciais aprovados automaticamente.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
generate_score_bands(scores: np.ndarray, y_true: np.ndarray, n_bands: int=10, labels: Optional[Sequence[str]]=None, *, higher_score_is_better: bool=True) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/score_bands/score_bands.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/score_bands/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/score_bands/exemplo_score_bands.py)

#### `hub_snippets.ml.scorecard_builder`

Recebe coeficientes, intercepto e tabelas WOE já estimadas; devolve tabela de pontos. PDO, base de score, odds e definição de evento governam a escala. Não ajusta sozinho uma regressão nem transforma pontos em limite de crédito aprovado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
build_scorecard(coefs: np.ndarray, intercept: float, feature_names: List[str], woe_tables: Dict[str, pd.DataFrame], pdo: int=20, base_score: int=600, base_odds: int=50, event_is_bad: bool=True) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/scorecard_builder.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/exemplo_scorecard_builder.py)

#### `hub_snippets.ml.shap_explainer`

Recebe modelo e dados compatíveis, calcula atribuições, resume importância e cria visualizações. Confira tarefa, classe/saída escolhida, ordem das features e amostragem. SHAP e suas dependências são exigidos conforme a implementação; salvar gráficos pode escrever no caminho indicado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
compute_shap(model, X: np.ndarray, feature_names: List[str], model_type: str='tree', max_samples: int=5000, *, task: str='classification', output_index: Optional[int]=None) -> Tuple[np.ndarray, float]
get_feature_importance_shap(shap_values: np.ndarray, feature_names: List[str], top_n: int=20) -> pd.DataFrame
plot_shap_global(shap_values: np.ndarray, X: np.ndarray, feature_names: List[str], plot_type: str='beeswarm', max_display: int=20, save_path: Optional[str]=None)
plot_shap_local(shap_values: np.ndarray, base_value: float, X: np.ndarray, feature_names: List[str], idx: int, save_path: Optional[str]=None)
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/shap_explainer.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py)

#### `hub_snippets.ml.split_temporal`

Recebe pandas com data e devolve três DataFrames: treino, validação e teste. Opera por períodos e gaps; pode impor restrição adicional por grupo. Não aceita automaticamente um Spark DataFrame. O exemplo do capítulo 16 mostra por que percentuais não são sempre proporções finais de linhas.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
temporal_split(df: pd.DataFrame, date_col: str, train_pct: float=0.7, val_pct: float=0.15, gap_periods: int=1, period_unit: str='M', *, group_col: Optional[str]=None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/split_temporal.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/exemplo_split_temporal.py)

#### `hub_snippets.ml.survival_cox`

Recebe pandas com duração, evento e atributos; devolve modelo Cox e métricas. A função de proporcionalidade devolve tabela de diagnóstico. Lifelines é requerido na execução; o contrato pressupõe codificação coerente de evento e censura. Há registro opcional em MLflow.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_cox_ph(df: pd.DataFrame, duration_col: str, event_col: str, feature_cols: List[str], penalizer: float=0.01, l1_ratio: float=0.0, log_mlflow: bool=True) -> Tuple[object, Dict[str, float]]
validate_proportionality(model, df, duration_col, event_col) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/survival_cox.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/exemplo_survival_cox.py)

#### `hub_snippets.ml.tabnet_wrapper`

Recebe arrays e configuração de categorias, ajusta TabNet e devolve modelo, métricas e importâncias. Pytorch-tabnet é exigido na chamada; dependências de topo precisam estar presentes. Número de épocas e tamanho do lote influenciam custo e memória.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_tabnet(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', cat_idxs: Optional[List[int]]=None, cat_dims: Optional[List[int]]=None, n_d: int=32, n_a: int=32, n_steps: int=5, max_epochs: int=100, patience: int=15, batch_size: int=1024, log_mlflow: bool=True) -> Tuple[object, Dict[str, float], np.ndarray]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/tabnet_wrapper.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/exemplo_tabnet_wrapper.py)

#### `hub_snippets.ml.train_catboost`

Recebe arrays de treino/validação e devolve modelo CatBoost e métricas. Categorias devem ser identificadas conforme o parâmetro da interface; não presuma que uma string desconhecida será sempre aceita. O módulo exige a biblioteca e pode registrar tracking.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_catboost_baseline(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', cat_features: Optional[List[int]]=None, params_override: Optional[Dict[str, Any]]=None, log_mlflow: bool=True) -> Tuple[Any, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/train_catboost.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/exemplo_train_catboost.py)

#### `hub_snippets.ml.train_lgbm`

Recebe arrays de treino/validação e devolve modelo LightGBM e métricas. Permite configurações e early stopping. LightGBM/MLflow são dependências do módulo; desativar logging não remove imports. Contrato supervisionado não equivale a processamento distribuído Spark.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_lightgbm_baseline(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', params_override: Optional[Dict[str, Any]]=None, early_stopping_rounds: int=50, log_mlflow: bool=True) -> Tuple[lgb.LGBMModel, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/train_lgbm.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/exemplo_train_lgbm.py)

#### `hub_snippets.ml.train_xgboost`

Guia conceitual e de decisão: `hub_snippets/ml/train_xgboost/README.md` (a partir de `.assistant/`).

Recebe arrays de treino/validação e devolve modelo XGBoost e métricas. Exige biblioteca compatível com o ambiente. Preserve dtype, tratamento de ausentes e ordem dos atributos, sobretudo entre ajuste e inferência.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_xgboost_baseline(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', params_override: Optional[Dict[str, Any]]=None, early_stopping_rounds: int=50, log_mlflow: bool=True) -> Tuple[xgb.XGBModel, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/train_xgboost.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py)

#### `hub_snippets.ml.umap_viz`

Projeta um array em menor dimensão ou constrói figura Plotly por grupos. UMAP é exigido na chamada. Uma separação visual em duas dimensões é uma representação reduzida, não prova de grupos reais nem de efeito causal.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
compute_umap(X: np.ndarray, n_components: int=2, n_neighbors: int=15, min_dist: float=0.1) -> np.ndarray
plot_umap_clusters(X_scaled: np.ndarray, labels: np.ndarray, title: str='Clusters (UMAP 2D)', cluster_names: Optional[List[str]]=None, point_size: int=3, n: Optional[int]=None) -> go.Figure
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/umap_viz.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/exemplo_umap_viz.py)

#### `hub_snippets.ml.vintage_analysis`

Recebe painel pandas com contrato, originação, referência e target; devolve tabela de maturação. Outras funções geram curvas, heatmap ou comparação entre safras. Diferencie target de evento e target cumulativo; compare apenas maturidades observáveis e denominadores coerentes.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
build_vintage_table(df: pd.DataFrame, contract_id: str, dt_originacao: str, dt_referencia: str, target: str, safra_grain: str='month', mob_col: Optional[str]=None, target_is_cumulative: bool=False) -> pd.DataFrame
plot_vintage_curves(vintage_df: pd.DataFrame, title: str='Curvas de Maturação por Safra', max_mob: int=24, top_n_safras: Optional[int]=None) -> Any
plot_vintage_heatmap(vintage_df: pd.DataFrame, title: str='Heatmap de Safras', max_mob: int=24, metric: str='taxa_acumulada') -> Any
compare_safras(vintage_df: pd.DataFrame, mob_checkpoints: Optional[List[int]]=None) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/vintage_analysis.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/exemplo_vintage_analysis.py)

#### `hub_snippets.ml.walk_forward`

Recebe pandas temporal e uma função de avaliação passada em `model_fn`; devolve lista de resultados por janela. O callback recebe conjuntos de treino e teste de cada rodada. A função não escolhe sozinha o algoritmo; calendário, gap e critério de avaliação são parte do experimento.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
walk_forward_cv(df: pd.DataFrame, date_col: str, target_col: str, model_fn: Callable[[pd.DataFrame, pd.DataFrame], Dict[str, Any]], min_train_periods: int=12, test_periods: int=1, step: int=1, gap: int=0, *, period_unit: str='M') -> List[Dict[str, Any]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/walk_forward.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/exemplo_walk_forward.py)

#### `hub_snippets.ml.woe_iv_calculator`

Recebe Spark DataFrame com feature já discretizada e alvo binário. Devolve tabela WOE e IV total; `classify_iv` fornece uma interpretação por faixas do helper. Essas faixas não constituem regra universal de aprovação. Ajuste bins e WOE no conjunto permitido, não em todo o histórico.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calculate_woe_iv(df: DataFrame, feature_col: str, target_col: str, smoothing: float=0.5) -> Tuple[DataFrame, float]
classify_iv(iv: float) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/woe_iv_calculator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/exemplo_woe_iv_calculator.py)

### 27.5. Dados para exercícios e testes

#### `hub_snippets.testing.fixtures`

**Guia local do objeto (R03-A):** na pasta `hub_snippets/testing/fixtures/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_fixtures.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Cria Spark DataFrames sintéticos para exercícios tabulares, séries, fatos/features e safras. Alguns testes exigem uma sessão Spark ativa. As características são controladas pelo gerador; não representam estatísticas observadas de clientes reais.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
base_tabular(n: int=500, *, seed: int=42, pct_nulos_renda: float=0.04, prevalencia_alvo: float=0.25, n_entidades: Optional[int]=None) -> DataFrame
serie_temporal(n_entidades: int=20, n_periodos: int=24, *, seed: int=42, tendencia: float=0.5) -> DataFrame
fatos_e_features(n_decisoes: int=300, *, seed: int=42, atraso_real_dias: int=3, pct_feature_futura: float=0.2) -> Tuple[DataFrame, DataFrame]
safras(n_contratos: int=400, *, seed: int=42, safras_yyyymm: Sequence[str]=('202501', '202502', '202503'), mob_maximo: int=12) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/fixtures.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/exemplo_fixtures.py)

### 27.6. Componentes visuais

#### `hub_snippets.visual.badge`

**Guia local do objeto (R03-A):** na pasta `hub_snippets/visual/badge/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_badge.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Devolve pequenas marcações HTML de status, score ou texto. Cor e rótulo precisam ser alimentados por uma interpretação justificada; a função visual não certifica o dado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
badge_status(texto: str, tipo: str='ok') -> str
badge_score(valor: float, max: float=100) -> str
badge_inline(texto: str) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/badge/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/badge/exemplo_badge.py)

#### `hub_snippets.visual.divider`

**Guia local do objeto (R03-A):** na pasta `hub_snippets/visual/divider/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_divider.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Devolve separadores HTML. Controla apresentação, sem cálculo ou escrita de dados. O consumidor precisa renderizar a string na superfície adequada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
divider_light() -> str
divider_medium() -> str
divider_heavy() -> str
divider_section() -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/divider/divider.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/divider/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/divider/exemplo_divider.py)

#### `hub_snippets.visual.index_generator`

**Guia local do objeto (R03-B):** na pasta `hub_snippets/visual/index_generator/`, abra `README.md` antes de `exemplo_index_generator.py`. O guia distingue conceito, contrato, efeitos e interpretação; as referências históricas abaixo permanecem vinculadas à sua base.

Devolve um índice de etapas de EDA em HTML ou Markdown. O parâmetro `markdown` define o formato. A implementação produz lista declarada, sem links ou inspeção das células; o índice não comprova execução das etapas.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
gerar_indice_eda(etapas_ativas: Optional[Iterable[int]]=None, markdown: bool=False) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/index_generator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/exemplo_index_generator.py)

#### `hub_snippets.visual.kpi_card`

**Guia local do objeto (R03-A):** na pasta `hub_snippets/visual/kpi_card/`, abra `README.md` para entender conceito, escolhas, entradas e limites antes de `exemplo_kpi_card.py`. O guia é parte do produto; as referências históricas de implementação abaixo permanecem datadas.

Devolve cards HTML ou texto Markdown de indicadores. Recebe valores já apurados; não consulta tabela nem calcula KPI de negócio. Um card com número correto e denominador omitido ainda pode induzir erro.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
kpi_card_html(metricas: Dict[str, Any]) -> str
kpi_card_markdown(metricas: Dict[str, Any]) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/exemplo_kpi_card.py)

#### `hub_snippets.visual.section_header`

**Guia local do objeto (R03-B):** na pasta `hub_snippets/visual/section_header/`, abra `README.md` antes de `exemplo_section_header.py`. O guia distingue conceito, contrato, efeitos e interpretação; as referências históricas abaixo permanecem vinculadas à sua base.



## R0408 — linhas [2172, 2198]

#### `hub_snippets.visual.tema`

Valida uma configuração visual completa e devolve um retrato isolado dos tokens,
isto é, escolhas de aparência com nome e valor. Este núcleo não aplica cores,
não registra templates, não consulta dados e não publica. `ResolvedTheme.to_dict()` fornece
uma cópia editável, sem contaminar a configuração original. A V02 foi aceita e
integrada no Git pelo PR #14; execução local, publicação e homologação no workspace
continuam sendo estados diferentes.

**Schema** é o documento central dos campos e limites, em
`hub_padroes/identidade_visual/theme.schema.json`. **Serialização canônica** é a
forma determinística `hub-json-v1` usada para exportar os dados. **Fingerprint**
identifica conteúdo e dependências; não autentica autor ou concede aprovação.
Esses conceitos complementam este Manual, sem criar outro glossário.

A API pública contém `ThemeError`, `ResolvedTheme`, `normalize_color`,
`resolve_theme`, `load_theme`, `load_reference_theme` e `export_theme`.
As assinaturas detalhadas e exemplos ficam no README do objeto. Na pasta publicada
`.assistant`, abra `hub_snippets/visual/tema/README.md`; no Git, o caminho é
`ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md`. O exemplo só usa
referências sintéticas e memória; `export_theme` não salva um arquivo.

O import requer somente a biblioteca padrão; validar requer as bibliotecas
registradas em `hub_snippets/requirements-temas.txt`, sem instalação automática.
As referências legadas empacotadas não são temas operacionais aprovados. A cópia
completa é obrigatória; levar apenas `tema.py` perde o schema e o manifesto.
Não há configuração implícita, cache global ou fallback diante de erro.



## R0409 — linhas [2200, 2288]

#### `hub_snippets.visual.theme_lab`

**Candidata V05 — Visual Lab de aparência, sem aprovação ou publicação.** Este
objeto oferece uma prévia pessoal para escolher uma base `notebook`, ajustar
tokens, comparar a aparência e preservar uma sessão de autoria. Ele recebe temas
revalidados pelo núcleo V02 e reutiliza os consumidores V03/V04; não consulta
rede, Spark, SQL ou MLflow e não altera `plotly.io.templates.default` ao importar.

**Primeiro acesso.** Na cópia autorizada de `.assistant`, leia
`hub_snippets/visual/theme_lab/README.md`, siga
`hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md` e use
`exemplo_theme_lab.py` como demonstração. O launcher é opt-in: abrir o Hub não
muda o padrão da equipe e escolher um preset não o torna aprovado.

**Escolher e ajustar.** `get_demo_presets()` expõe referências empacotadas
marcadas como demonstração; `prepare_theme_lab_presets()` aceita bases fornecidas
pelo mantenedor e as revalida; `create_theme_lab_from_preset()` recusa chave
inexistente e contexto diferente de `notebook`, sem fallback silencioso.
`get_control_specs()` deriva tipo, unidade, limites e controle do schema. As
alterações são aplicadas atomicamente: um valor inválido preserva o último estado
válido. Campos ainda sem consumidor na galeria ficam desabilitados e explicam o
motivo, em vez de simular efeito.

**Rascunho e comparação.** `ThemeLabDraft` preserva base, proposta corrente,
revisão e histórico local limitado; `undo()` e `restore()` não publicam nada.
`build_preview()` e `compare_preview()` usam os mesmos dados sintéticos em
cabeçalho, KPI, barras, série temporal, heatmap e tabela. A galeria completa
permanece `light`, porque a rota Plotly V03 recusa `dark` e `high_contrast` até
que exista suporte explícito.

<details>
<summary>Consultar a API deste objeto: nomes e contratos</summary>

```text
ThemeLabError(code, message, *, action)
ControlSpec
ProposalReceipt
ThemeLabPreview
ThemeLabComparison
ThemeLabPreset
ThemeLabSessionReceipt
ThemeLabSessionInfo
ThemeLabDraft(base: ResolvedTheme)
ThemeLabUI
ThemeLabLauncherUI
get_control_specs(theme: ResolvedTheme) -> tuple[ControlSpec, ...]
prepare_theme_lab_presets(presets) -> tuple[ThemeLabPreset, ...]
get_demo_presets() -> tuple[ThemeLabPreset, ...]
create_theme_lab_from_preset(preset_key, presets) -> ThemeLabDraft
save_theme_lab_session(draft, root, session_name) -> ThemeLabSessionReceipt
reopen_theme_lab_session(root, session_name) -> ThemeLabDraft
list_theme_lab_sessions(root) -> tuple[ThemeLabSessionInfo, ...]
create_theme_lab(theme: ResolvedTheme) -> ThemeLabDraft
build_preview(theme: ResolvedTheme) -> ThemeLabPreview
compare_preview(draft: ThemeLabDraft) -> ThemeLabComparison
install_dbutils_fallback(draft, dbutils, *, prefix="hub_tema_") -> dict[str, str]
apply_dbutils_fallback(draft, dbutils, *, prefix="hub_tema_") -> ResolvedTheme
build_ipywidgets_lab(draft, *, save_root=None, render_initial=True) -> ThemeLabUI
build_theme_lab_launcher(*, presets=None, save_root=None) -> ThemeLabLauncherUI
```

A fachada `__init__.py` é a referência exata dos nomes públicos; o README local
documenta assinaturas, opções e exemplos com mais detalhe.

</details>

**Persistência e linhagem local.** JSON avulso e sessão são produtos diferentes.
`save_proposal()` salva apenas a configuração atual. `save_theme_lab_session()`
cria um diretório novo com `base.json`, `proposal.json`, histórico e
`session.json`; o manifesto é escrito por último e registra hashes e revisão.
Sessão incompleta não aparece na listagem nem é reaberta. A reabertura revalida
os temas, confere os hashes e restaura base original, proposta, revisão e
histórico; adulteração é recusada em vez de ter o hash “corrigido”. O bundle não
autentica autor, não assina conteúdo e não registra aprovação de governança.

**Interface e dependências.** Importar o módulo não carrega `ipywidgets`.
Validação exige `jsonschema`/`referencing`; a galeria usa pandas, Plotly e Jinja2;
a interface completa usa ipywidgets/IPython quando construída. O fallback
`dbutils.widgets` recebe `dbutils` explicitamente e é funcionalmente menor: não
tem paridade com o launcher de presets/sessões. Nenhuma função instala pacotes.

**Segurança e limites de evidência.** Persistência exige pasta regular já
existente, não sobrescreve sessão/arquivo existente e não emite recibo de sucesso
quando a escrita falha. Essas guardas não substituem ACL do ambiente nem formam
uma sandbox. Os testes Python/GitHub Actions exercitam estado, callbacks no
kernel, presets, sessões, hashes e roundtrip; não homologam navegador/runtime
Databricks, teclado/leitor de tela, contraste percebido, zoom, p95, ACL real,
reinício de sessão ou UAT por iniciante. A V05 continua candidata: sem aceite,
merge, publicação Databricks ou início da V06.



## R0410 — linhas [2290, 2312]

#### `hub_snippets.visual.theme_plotly`

**Guia local do objeto (R03-B):** na pasta `hub_snippets/visual/theme_plotly/`, abra `README.md` antes de `exemplo_theme_plotly.py`. O guia distingue conceito, contrato, efeitos e interpretação; as referências históricas abaixo permanecem vinculadas à sua base.

Mantém a rota legada de configuração/aplicação/registro e acrescenta, na V03, uma rota opt-in que consome `ResolvedTheme` de contexto notebook. `aplicar_tema_resolvido` afeta somente a figura passada; `registrar_template_plotly_resolvido` usa namespace `hub-*` e não muda o default da sessão sem `ativar=True`. Se o nome a substituir já estiver ativo, sozinho ou dentro de um default composto, `substituir=True` sem `ativar=True` é recusado para impedir mudança global implícita. Como a rota V03 revalida o tema antes do consumo, ela requer também as dependências declaradas em `hub_snippets/requirements-temas.txt` (`jsonschema` e `referencing`); nenhuma função instala pacotes. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. Dados, eixos e cores explícitas de traces permanecem fora da responsabilidade do adaptador.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
get_tema_eda() -> Dict[str, Any]
aplicar_tema(fig: go.Figure, subtitulo: Optional[str]=None, fonte: Optional[str]=None, n: Optional[int]=None) -> go.Figure
registrar_template_plotly() -> None
get_tema_plotly(theme: ResolvedTheme) -> Dict[str, Any]
aplicar_tema_resolvido(fig: go.Figure, theme: ResolvedTheme, subtitulo: Optional[str]=None, fonte: Optional[str]=None, n: Optional[int]=None) -> go.Figure
registrar_template_plotly_resolvido(theme: ResolvedTheme, *, nome: str, ativar: bool=False, substituir: bool=False) -> None
```

</details>

Para usuários novos, mantenha `aplicar_tema` se o objetivo é preservar o hábito atual. Use `aplicar_tema_resolvido` somente quando houver uma configuração notebook explicitamente resolvida pelo núcleo V02. A V03 suporta `mode=light`; `dark`/`high_contrast` falham fechados até uma sprint futura definir superfícies Plotly sem defaults ocultos. Fixtures empacotadas servem a testes/demonstrações e não são temas operacionais aprovados.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py)



## R0411 — linhas [2446, 2463]

| Skill | Pergunta atendida e contexto necessário | O que revisar na entrega |
|---|---|---|
| `hub-ml-concierge` | O que o Hub já oferece e como combinar seus recursos? Descreva objetivo, entrada conhecida e restrições. | Evidências de existência/adequação, cobertura, versão, pré-condições e repasse sem execução. |
| `hub-ml-micromodelos` | Como especificar uma característica ou descobrir oportunidades no catálogo configurado? Informe decisão, escopo e restrições. | YAML conforme contrato quando acessível, metadata observada separada da fornecida, incertezas e decisões pendentes. |
| `hub-ml-eda-profissional` | Como é uma fonte ou base consolidada? Forneça recurso, grão, chaves candidatas e período. | Perfil, qualidade, distribuições, origem integral/amostral dos números e limites. |
| `hub-ml-cross-eda-ml` | É viável combinar várias fontes? Forneça os EDAs, chaves, tempos e cobertura. | Relações, expansão dos joins, disponibilidade temporal e lacunas antes de modelar. |
| `hub-ml-feature-engineering` | Como construir atributos disponíveis no momento correto? Defina decisão, target, fontes e horizontes. | Contratos, point-in-time, preparação, testes e coerência treino/inferência. |
| `hub-ml-baseline-ml` | Qual referência de modelagem atende ao problema? Informe tarefa, base preparada, split e orçamento. | Comparabilidade, métricas pertinentes, custo, tracking e limitações. |
| `hub-ml-validacao-estatistica` | O que uma evidência sustenta sob incerteza? Defina hipótese, população e desenho. | Pressupostos, magnitude, intervalos, multiplicidade e conclusão proporcional. |
| `hub-ml-analise-safra` | Como os grupos de originação amadurecem? Informe contrato, evento, referência e MOB. | Denominador, maturidade comparável, censura/incompletude e não duplicação de eventos. |
| `hub-ml-explainability` | Como o modelo usa as entradas? Forneça modelo, preparação, dados e saída a explicar. | Coerência de features, referência explicativa, limites e distinção de causalidade. |
| `hub-ml-micromodelos` | Como especificar uma característica ou descobrir oportunidades usando metadata? Declare decisão, escopo e permissão. | Distinguir metadata observada, hipótese e aprovação; contrato L1, sem runner Databricks. |
| `hub-ml-monitoramento-modelo` | O que observar no funcionamento do modelo? Defina referência, produção, rótulos disponíveis e políticas. | Qualidade, drift, performance, custo e critérios explícitos para investigar/agir. |
| `hub-ml-pipeline-builder` | Como organizar execução recorrente? Informe fontes, destino, frequência, dependências e permissões. | Idempotência, qualidade, retries, observabilidade e aprovação de escritas. |
| `hub-ml-comentar-notebook` | Como explicar um notebook existente? Forneça o código e suas saídas. | Explicação antes/depois, interpretação dos números reais e ausência de mudanças ocultas na lógica. |
| `hub-ml-tutor-databricks` | Como entender um conceito, erro ou bloco? Forneça a dúvida e o contexto mínimo. | Progressão didática, linha a linha quando útil e exemplo compatível com a versão. |
| `hub-ml-auditoria-skills` | O método ou a entrega seguem o contrato? Forneça ambos e o critério de avaliação. | Descoberta, segurança, referências, execução observada e conclusão sustentada. |
| `hub-ml-criar-objeto` | Como criar um componente no padrão do Hub? Defina o tipo, a necessidade e os consumidores. | Molde pertinente, ausência de duplicação, API, exemplo, testes e documentação. |



## R0412 — linhas [2469, 2490]

### 28.2. Os dezesseis briefings: dar os detalhes do caso

Os arquivos ficam em `hub_prompts/<nome>/<nome>.md`, acompanhados de notebook `exemplo_<nome>.py`. No piloto R02, `hub_prompts/eda_rapida/README.md` acrescenta a explicação de escolha e alerta que o preparo de seu notebook usa overwrite de tabela persistente. Abra o briefing real para preencher todos os seus campos; esta tabela explica o ponto de entrada, não cria um formulário alternativo concorrente.

| Briefing | Use para | Informação que não deve faltar |
|---|---|---|
| `novo_projeto` | Delimitar uma iniciativa | Decisão atendida, público, escopo, fontes, riscos e critérios de sucesso. |
| `eda_rapida` | Primeiro diagnóstico limitado | Recurso, período, grão, leitura permitida e profundidade desejada. |
| `eda_completa` | Exploração desenvolvida de uma base | Regras de negócio, variáveis, população, limites de custo e entregáveis. |
| `comparar_tabelas` | Contrastar dois recursos | Qual é a referência, chaves, schemas, períodos e significado da diferença. |
| `cross_eda` | Consolidar fontes e estudos | EDAs existentes, âncora, relações de entidade, disponibilidade e cobertura. |
| `data_quality` | Diagnosticar qualidade | Chaves, campos obrigatórios, referência temporal e limiares aprovados. |
| `feature_engineering` | Planejar/construir atributos | Instante de decisão, target, fontes, transformações e janela histórica. |
| `baseline_orchestration` | Organizar um baseline | Tarefa, split, métrica, comparação e orçamento computacional. |
| `stat_check` | Planejar diagnóstico estatístico | Hipótese, unidade de observação, desenho e relevância prática. |
| `safra` | Analisar maturação de grupos | Originação, observação, evento, denominador e MOB comparável. |
| `explainability` | Explicar um modelo | Modelo/versão, features ordenadas, população e classe/saída escolhida. |
| `monitoramento_modelo` | Definir acompanhamento | Modelo em uso, referência, período corrente, rótulos e política de alerta. |
| `pipeline` | Especificar execução recorrente | Dependências, frequência, destino, qualidade, retries e escritas autorizadas. |
| `comentar_notebook` | Melhorar a explicação de um artefato | Notebook e saídas reais, público e grau de detalhe. |
| `tutor_explicar` | Aprender um ponto específico | Dúvida, bloco/erro e conhecimento prévio. |
| `auditoria_skills` | Conferir método ou resultado | Contrato, evidências e critérios; não apenas a autoavaliação do autor. |



## R0413 — linhas [2557, 2560]

**Estado da integração em 12/09/2026:** componente incorporado à fonte do produto,
com publicação e testes conversacionais pendentes. A origem histórica do código
examinado neste Manual permanece a indicada na abertura; esta seção registra a
adição posterior e não atribui o Concierge ao snapshot antigo dos helpers.



## R0414 — linhas [2648, 2674]

<a id="fontes"></a>
### Guias locais R04-B — scripts operacionais

Se a dúvida estiver em um dos seis scripts abaixo, abra primeiro o README da própria pasta. Ele explica o conceito, efeitos, custo e interpretação antes do notebook:

- `hub_scripts/data_quality_check/README.md` — chave, nulos, atualidade e score heurístico;
- `hub_scripts/doc_coverage/README.md` — adjacência Markdown-código, não qualidade textual;
- `hub_scripts/drift_detector/README.md` — PSI numérico entre coortes, sem confundir drift e performance;
- `hub_scripts/naming_checker/README.md` — convenções com origem explícita da política;
- `hub_scripts/rfv_calculator/README.md` — RFV bruto com corte temporal global;
- `hub_scripts/schema_to_yaml/README.md` — snapshot de schema, YAML/JSON e estatísticas opcionais.

Os scripts continuam sendo executados explicitamente. O README não torna o helper um gate automático e não substitui a implementação.

### Guias locais R05 — modelos tabulares

Para escolher entre os seis modelos/tabulares desta leva, abra primeiro o README da pasta. A rota recomendada é: baseline simples → baseline de árvore → somente depois tuning ou arquitetura neural, sempre sob a mesma validação.

- `hub_snippets/ml/train_lgbm/README.md` — LightGBM e métricas por tarefa;
- `hub_snippets/ml/train_catboost/README.md` — CatBoost e categóricas;
- `hub_snippets/ml/lgbm_ranker/README.md` — ranking por grupos e NDCG;
- `hub_snippets/ml/optuna_lgbm/README.md` — TPE e limites da busca;
- `hub_snippets/ml/mlp_embeddings/README.md` — embeddings e contrato binário do treinador;
- `hub_snippets/ml/tabnet_wrapper/README.md` — TabNet e importância global.

Os notebooks instalam dependências de laboratório e reiniciam o Python. Leia esses efeitos antes de executar. Métrica de validação, importância ou tuning não equivalem a homologação do modelo.




## R0415 — linhas [2728, 2765]

### 30.3. Fontes de implementação e de manutenção

O inventário do capítulo 27 aponta para cada implementação, sua API exportada e seu notebook. As referências abaixo sustentam a organização, os mecanismos de validação e o fluxo de entrega. Referenciar uma ferramenta não executa o comando nem autoriza publicação.

- [`README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/README.md)
- [`CLAUDE.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/CLAUDE.md)
- [`.claude/rules/docs-e-readmes.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/.claude/rules/docs-e-readmes.md)
- [`.claude/rules/genie-code-oficial.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/.claude/rules/genie-code-oficial.md)
- [`docs/decisions/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/docs/decisions/README.md)
- [`ambiente_fonte/.assistant_instructions.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant_instructions.md)
- [`ambiente_fonte/.assistant/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/README.md)
- [`ambiente_fonte/.assistant/skills/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/skills/README.md)
- [`ambiente_fonte/.assistant/hub_prompts/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_prompts/README.md)
- [`ambiente_fonte/.assistant/hub_padroes/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_padroes/README.md)
- [`ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt)
- [`tools/api_publica.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/api_publica.py)
- [`tools/notebook_marker.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/notebook_marker.py)
- [`tools/render_simulado.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/render_simulado.py)
- [`tools/publicar_free.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/publicar_free.py)
- [`tools/bundle_implantacao.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/bundle_implantacao.py)
- [`tools/validate_assistant.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/validate_assistant.py)
- [`tools/ci_local.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/ci_local.py)
- [`tools/project_policy.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/project_policy.py)

### 30.4. Como atualizar este manual sem criar duas redações

Edite o arquivo de autoria `ambiente_fonte/.assistant/MANUAL_TECNICO.md`. Confira os contratos no código quando acrescentar uma API ou modificar exemplos. Sincronize a cópia de leitura da raiz Git a partir desse mesmo arquivo e regenere o simulado pelo renderer, nunca por edição manual do derivado. A igualdade das cópias é parte da conferência documental.

A seguir está uma operação **local de manutenção**, a executar a partir da raiz do repositório após revisar a nova redação. Ela não publica no Databricks:

```powershell
python -c "from pathlib import Path; Path('MANUAL_TECNICO.md').write_bytes(Path('ambiente_fonte/.assistant/MANUAL_TECNICO.md').read_bytes())"
python tools/render_simulado.py --write
python tools/validate_assistant.py --conferir-readme
python tools/ci_local.py
```

Atualizar uma referência oficial exige rever a afirmação que ela sustenta; não basta trocar a data. Atualizar uma contagem exige executar sua verificação. Atualizar um teste requer preservar a distinção entre verificações locais, runtime Databricks, serviços remotos e conversa da Genie Code.



## R0416 — linhas [2771, 2806]

## Sistema de Temas — V00–V07 integradas no Git

O Sistema de Temas está integrado no repositório até a V07. Isso significa que o contrato, os adaptadores e consumidores descritos abaixo existem no produto versionado; **não** significa que um tema tenha sido publicado no workspace, aprovado visualmente ou homologado em browser/acessibilidade.

### Camadas e responsabilidade

- **V02 — núcleo:** carrega, valida e resolve configurações completas em `ResolvedTheme`. Não aplica nem aprova aparência.
- **V03 — Plotly:** `aplicar_tema_resolvido` e registro explícito de template; sem efeito global por import.
- **V04 — HTML/tabelas:** componentes `_resolvido` e estilos derivados do mesmo tema.
- **V05 — Visual Lab:** autoria/comparação opt-in em notebook, com sessão e histórico; não publica.
- **V06 — assets/geração:** renderização editorial orientada por tema em área candidata; geração não promove asset.
- **V07 — consumidores/formatos:** correlação, distribuições, curvas de ML, monitoramento, UMAP e safras recebem rotas temáticas explícitas; HTML Plotly local foi exercitado.

A fonte canônica de campos/limites está em `hub_padroes/identidade_visual/theme.schema.json`; a referência de tokens é `TOKENS.md`. Skills e templates podem orientar uso e composição, mas não devem copiar paletas para criar uma segunda política visual.

### Fluxo recomendado para notebook

1. Se você só quer o comportamento histórico, use a API legada.
2. Para escolher/editar uma proposta, use o Visual Lab ou carregue uma configuração completa pela API `hub_snippets.visual.tema`.
3. Para uma figura/componente tematizável, use a rota `_resolvido` documentada pelo objeto.
4. Revise saída, dados, unidade e limites; aparência não valida o resultado analítico.
5. Trate salvar, compartilhar, aprovar e publicar como ações diferentes.

### Limites atuais

- `dark`/`high_contrast` têm cobertura diferente entre HTML e Plotly; não trate modo válido como homologação de acessibilidade.
- SHAP/Matplotlib e o PNG do helper SHAP permanecem fora do theming V07.
- Kaplan–Meier preserva aparência legada enquanto sua ordem de cores não estiver representada pelo contrato sem remapeamento silencioso.
- PNG Plotly/Kaleido, PDF, PPTX e render real no browser Databricks não foram homologados pela V07.
- Tema não muda threshold, métrica, amostra, agregação, modelo, policy ou decisão de negócio.

### V08 — integração transversal em execução

A V08 não adiciona runtime: ela reconcilia skills, padrões e este Manual para que todos apontem às mesmas fontes de verdade e limites das V02–V07. Até aceite/merge da V08, essa reconciliação deve ser tratada como candidata de documentação transversal, não como nova capacidade publicada.

Para primeiro uso, consulte `hub_padroes/identidade_visual/GUIA_OPERACIONAL.md`. Para autoria, consulte `hub_snippets/visual/theme_lab/README.md`. Para um consumidor específico, o README local continua sendo a fonte de uso daquele objeto.

