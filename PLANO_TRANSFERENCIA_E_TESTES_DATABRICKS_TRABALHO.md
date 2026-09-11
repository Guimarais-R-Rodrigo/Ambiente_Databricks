# Plano de transferência e homologação do ambiente Databricks

> **Plano de execução futura — 11/09/2026.** Este documento não executa a
> transferência, não cria os notebooks e não certifica o ambiente de trabalho.
> Ele especifica o procedimento e os testes que deverão ser implementados e
> executados depois, com aprovação e evidência.

## Como usar este documento

Este é o manual para levar o produto que está sendo desenvolvido e testado no
Databricks Free para o Databricks do trabalho, usando **arquivo enviado por
e-mail autorizado e upload pela interface**, sem exigir CLI no computador
corporativo. Também é a especificação para outra LLM construir a futura pasta
`testes/` sem inventar funcionalidades, pular casos ou mudar a arquitetura.

Há dois públicos:

- **Quem vai transferir:** seguir as seções 1 a 7, depois executar os notebooks
  na ordem da seção 8 e preencher o aceite da seção 15.
- **Quem vai construir os testes:** ler o documento inteiro; implementar as
  sprints da seção 17; respeitar os contratos e a matriz de cobertura. Não
  tratar os nomes de arquivos planejados como arquivos já existentes.

O [Guia de pendências](GUIA_PENDENCIAS_E_CONFERENCIAS.md) registra o ponto atual
da publicação e da integração visual. Este plano é o dono do procedimento de
transferência e homologação, não do estado corrente da publicação.

### Navegação

| Necessidade | Seção |
|---|---|
| Entender o que será levado | [1 — Escopo e conceitos](#escopo) |
| Saber o que pedir à equipe de plataforma | [2 — Pré-requisitos](#pre-requisitos) |
| Entender pastas e pacotes | [3 — Arquitetura](#arquitetura) |
| Baixar, preparar e enviar por e-mail | [4 — Preparação e transporte](#transporte) |
| Fazer backup e upload sem CLI | [5 — Recepção e instalação](#instalacao) |
| Saber quando parar | [6 — Gates e riscos](#gates) |
| Entender como os notebooks devem ser escritos | [7 — Contrato da suíte](#contrato-suite) |
| Executar em sequência | [8 — Mapa dos notebooks](#mapa-notebooks) |
| Testar scripts, snippets, ML e imagens | [9 — Especificações técnicas](#testes-tecnicos) |
| Testar a Genie Code | [10 — Skills e instruções](#skills-instrucoes) e [11 — Prompts](#prompts) |
| Testar exemplos e padrões | [12 — Material didático](#exemplos-padroes) |
| Consolidar, limpar e decidir | [13 — Relatório final](#relatorio-final) |
| Corrigir problemas ou voltar à versão anterior | [14 — Diagnóstico e rollback](#diagnostico-rollback) |
| Liberar para a equipe | [15 — Aceite](#aceite) e [16 — Expansão](#equipe) |
| Orientar a implementação por outra LLM | [17 — Sprints](#sprints) e [18 — Regras contra deriva](#anti-deriva) |
| Consultar a fundamentação | [19 — Fontes](#fontes) |

---

<a id="escopo"></a>

## 1. O que significa transferir este ambiente

### 1.1 O que está sendo transferido

Estamos transferindo **arquivos de contexto, documentação e uma biblioteca de
código reutilizável**. Não estamos clonando um workspace Databricks inteiro.

| Componente | O que leva | O que não leva automaticamente |
|---|---|---|
| `.assistant_instructions.md` | Instruções pessoais da Genie Code | Configurações administrativas ou permissões |
| `.assistant/skills/` | Skills do Hub e suas referências | Garantia de que o assistente sempre escolherá a skill correta |
| `hub_prompts/` | Briefings preenchíveis e exemplos | Execução automática de prompts no chat |
| `hub_snippets/` e `hub_scripts/` | Módulos Python e notebooks didáticos | Bibliotecas externas, runtime, tabelas ou compute |
| `hub_padroes/` | Moldes e exemplos para manter consistência | Hooks ou geração automática de arquivos |
| `hub_readmes_visual_assets/` | PNGs, fontes visuais, contratos, licenças e documentação | Serviços externos de hospedagem ou renderização |
| `MANIFEST.json` | Relação de caminhos, tamanhos, hashes e commit do pacote | ACLs, configurações do workspace ou certificado de segurança |

Não serão transportados dados reais, credenciais, tokens, configurações da CLI,
conexões MCP, experimentos, modelos treinados, jobs, clusters, grants do Unity
Catalog, histórico de chats ou configurações de conta. Recursos desse tipo
precisam ser autorizados e configurados separadamente no destino, **somente se
um caso de uso realmente exigir**.

### 1.2 Qual é a fonte correta

```text
ambiente_fonte/                  ← produto editável e canônico
        │ validação + render
        ▼
Novo_Ambiente_Simulado/          ← cópia gerada; nunca editar à mão
        │ bundle_implantacao.py
        ▼
ZIP mínimo + MANIFEST.json      ← objeto de transporte
        │ e-mail aprovado + upload
        ▼
Workspace do trabalho           ← cópia operacional a homologar
```

**Recomendação:** preparar o ZIP na máquina local a partir da fonte validada e
congelada em Git. Não é necessário baixar tudo do Free novamente para obter
arquivos que já existem localmente. A conferência do Free continua importante
para comprovar que a versão testada corresponde à versão empacotada.

Se for necessário obter os arquivos exclusivamente pela interface do Free, há
uma rota alternativa na seção 4.4. Ela exige reconciliação com o manifesto e
sanitização antes do e-mail; um download bruto do workspace não é automaticamente
um pacote de implantação seguro.

### 1.3 Três comprovações diferentes

| Comprovação | Pergunta | Exemplo de evidência |
|---|---|---|
| Transporte | Os mesmos arquivos chegaram ao destino? | SHA-256, inventário e tipos |
| Execução | O código funciona neste runtime e com estas permissões? | Assertions, resultados e versões reais |
| Uso assistido | A Genie Code encontra o contexto e produz uma resposta adequada? | Conversas reais, skills carregadas e rubrica humana |

Nenhuma substitui as outras. Abrir um README não prova importação Python.
Importar um módulo não prova sua chamada. Um chat convincente não prova
execução. Um notebook verde não prova que seu JSON interno contém zero falhas.

### 1.4 Fotografia do inventário atual

O inventário definitivo da transferência será o do **commit da release**, não
uma contagem copiada deste plano. Em 11/09/2026, a inspeção identificou:

| Grupo | Referência para planejar cobertura |
|---|---:|
| Agent Skills do Hub | 13 |
| Templates de prompts | 16, com 161 campos acompanhados de guia |
| Objetos de snippets | 51: 4 constants, 3 display, 30 ml, 7 spark, 1 testing e 6 visual |
| Objetos de scripts | 7 |
| Objetos executáveis exemplares em `hub_padroes` | 2 |
| Total de pastas de objeto conferidas pelo validador | 60; não significa 60 snippets |
| Notebooks didáticos existentes no produto | 78; não significa 78 testes independentes |
| Diretórios de extensão `hub_` de primeiro nível | 5, incluindo assets visuais |
| Diagramas únicos / cabeçalhos compartilhados | 21 / 2 |

Fonte dos nomes de skills e diretórios: `tools/project_policy.py`. Fonte das
APIs: implementação e `__init__.py` de cada objeto; o catálogo é o mapa de
consulta. Em caso de contradição entre prosa e código, abrir um achado e
resolver antes de congelar uma nova release.

O smoke de 09/09 registrou 137 PASS, oito dependências opcionais ausentes e um
bloqueio esperado, em 146 verificações. Os 39 forward tests aprovados são
acumulados entre rodadas e medem roteamento. Eles **não são homologação do
trabalho**, nem substituem a campanha dos 16 prompts.

---

<a id="pre-requisitos"></a>

## 2. Pré-requisitos: o que confirmar antes de enviar qualquer arquivo

### 2.1 Conversa com a equipe de plataforma/segurança

Preencher esta ficha **dentro do ambiente corporativo**. Identificadores reais
não devem voltar para este repositório pessoal.

| Pergunta a confirmar | Resposta necessária para avançar |
|---|---|
| Posso receber código externo por e-mail corporativo? | Autorização pelo processo interno e canal permitido |
| ZIP com Python, Markdown e PNG é permitido? | Tipos, tamanho máximo e inspeção exigida |
| Há revisão de software de origem externa? | Responsável, procedimento e evidência de aprovação |
| Posso usar a Genie Code com esse material? | Recurso habilitado, política de dados e ações compreendida |
| Posso importar arquivos na minha pasta de usuário? | Permissão de criação/edição no piloto |
| Já há instruções pessoais, skills ou padrões da organização? | Inventário e responsável por eventual conciliação |
| Qual compute devo usar? | Runtime/ambiente autorizado, modo de acesso e limites de custo |
| Posso instalar bibliotecas? | Fonte de pacotes aprovada e procedimento, ou ambiente pré-provisionado |
| Existe sandbox para dados sintéticos? | Caminho/objetos autorizados; não é necessário começar com tabela persistente |
| Posso criar runs MLflow temporários? | Experimento autorizado e responsável pela limpeza |
| Onde guardar os resultados? | Pasta ou volume interno com acesso e retenção definidos |
| Quem aprova a liberação à squad? | Revisor técnico e responsável funcional |

Não há necessidade de privilégio administrativo para simplesmente desenhar o
plano ou ler os arquivos. Se uma etapa exigir privilégio não concedido,
registrar `BLOQUEADO` e pedir a ação ao responsável; não tentar contornar a
restrição com outra API ou conta.

### 2.2 Transporte autorizado, não contorno de controles

O e-mail é a rota solicitada pelo usuário, **condicionada à política da
organização**. Se o anexo for bloqueado por tipo ou tamanho:

1. Guardar a mensagem de bloqueio no ambiente permitido.
2. Informar que se trata de código-fonte, documentação e imagens, sem dados de
   clientes nem credenciais.
3. Solicitar o canal corporativo aprovado para transferência.
4. Retomar pelo canal liberado, preservando os hashes e o manifesto.

Não renomear `.py` ou `.zip` para ocultar o tipo, não usar arquivo cifrado para
burlar inspeção e não fracionar o pacote para contornar DLP. A divisão por
tamanho só é aceitável quando o procedimento interno permitir e o inventário
de cada parte estiver documentado.

### 2.3 O que não deve entrar no e-mail

- Repositório completo, `.git/`, histórico, `.venv/`, `node_modules/` ou caches.
- `Ambiente_Antigo/`, referências de quarentena ou anexos históricos.
- `.artifacts/` inteiro, backups remotos ou resultados contendo identificação.
- Arquivos de configuração/autenticação da CLI, variáveis de ambiente, tokens.
- `.assistant/.mcp_servers.json`: é estado da configuração no workspace, não
  entrada deste produto.
- Tabelas exportadas, amostras reais, outputs com informação interna ou dumps de logs.
- Pastas `READMEs_refeitos/` e protótipos históricos como se fossem o produto final.

O fato de um arquivo ser Markdown ou uma imagem não o torna isento de dados
sensíveis: examinar texto, metadados, screenshots, nomes e conteúdo.

---

<a id="arquitetura"></a>

## 3. Arquitetura dos arquivos e da futura pasta de testes

### 3.1 Pacote A — produto, já suportado pelo projeto

O gerador existente `tools/bundle_implantacao.py` cria um ZIP contendo:

```text
ambiente-databricks-<commit>.zip
├── MANIFEST.json
├── .assistant_instructions.md
└── .assistant/
    ├── README.md
    ├── CATALOGO_HELPERS.md
    ├── GLOSSARIO.md
    ├── skills/
    │   └── hub-ml-<nome>/SKILL.md
    ├── hub_padroes/
    ├── hub_prompts/
    ├── hub_scripts/
    ├── hub_snippets/
    └── hub_readmes_visual_assets/
        ├── README.md
        ├── CONTEUDO_FIGURAS.md
        ├── manifest.yaml
        ├── headers/
        │   ├── png/cabecalho_crm.png
        │   ├── png/cabecalho_squad.png
        │   ├── src/
        │   └── ...
        ├── readmes/<colecao>/png/
        ├── readmes/<colecao>/sources/
        ├── specs/
        ├── visual_system/
        ├── licenses/
        └── qa/
```

A árvore é explicativa, não uma lista para excluir tudo o que aparece como
`...`. **Todos os itens do manifesto gerado devem ser mantidos.** Não remover
fontes SVG, contratos ou licenças para reduzir o e-mail sem uma decisão de
empacotamento separada. Os PNGs são os arquivos de exibição; as fontes e os
contratos permitem manutenção e reprodução.

O manifesto atual contém `schema_version`, `source_commit`, `worktree_dirty`,
`generated_at_utc`, `target` e uma lista `files` com `path`, `sha256` e `bytes`.
Ele **não contém atualmente um campo de tipo `FILE`/`NOTEBOOK`**. Essa informação
será acrescentada ao manifesto complementar dos testes, sem afirmar que o
gerador atual já a produz.

### 3.2 Pacote B — suíte de homologação, a construir depois

Criar futuramente uma pasta **`testes/` na raiz deste projeto**, como suporte de
homologação. Ela não pertence ao mecanismo nativo de descoberta de skills e
não deve ficar dentro de `.assistant/skills/`.

```text
testes/                                      ← PLANEJADO, ainda não criado
├── README.md                                ← entrada operacional da suíte
├── TEST_MANIFEST.json                        ← versões, tipos, casos e cobertura
├── config_exemplo.json                       ← placeholders, nunca identidade real
├── 00_LEIA_PRIMEIRO_PRECHECK.ipynb
├── 01_PACOTE_E_INSTALACAO.ipynb
├── 02_IMPORTS_E_CONTRATOS.ipynb
├── 03_SNIPPETS_SPARK_E_TEMPORALIDADE.ipynb
├── 04_SCRIPTS_OPERACIONAIS.ipynb
├── 05_ML_NUCLEO_E_METRICAS.ipynb
├── 06_VISUAL_E_DOCUMENTACAO.ipynb
├── 07_MLFLOW_E_INTEGRACOES.ipynb
├── 08_SKILLS_E_INSTRUCOES.ipynb
├── 09_PROMPTS_E_RESPOSTAS.ipynb
├── 10_EXEMPLOS_E_PADROES.ipynb
├── 11_HOMOLOGACAO_E_LIMPEZA.ipynb
├── opcionais/
│   └── O01_...ipynb até O14_...ipynb
├── _suporte/
│   ├── __init__.py
│   ├── configuracao.py
│   ├── resultados.py
│   ├── integridade.py
│   ├── fixtures_oraculo.py
│   └── casos_regressao.py
├── contratos/
│   ├── inventario_produto.json
│   ├── cobertura_objetos.json
│   ├── casos_skills.json
│   ├── casos_prompts.json
│   └── origens_e_adaptacoes.json
└── evidencias/
    └── MODELO_RESULTADO.md                    ← só modelo vazio no pacote
```

Escolha planejada: notebooks novos em `.ipynb`, com Markdown nativo e código em
células separadas. Os módulos de `_suporte/` são workspace files `.py`, **sem**
marcador de notebook. Os notebooks didáticos existentes do produto continuam no
formato original; não convertê-los em massa como parte desta transferência.

O Pacote B será um ZIP independente, com o mesmo identificador de release do
Pacote A e seu próprio SHA-256. O gerador atual do produto **não inclui** essa
pasta automaticamente. A sprint de empacotamento da suíte deve implementar e
validar esse segundo pacote por lista explícita de arquivos.

### 3.3 Onde instalar no workspace do trabalho

```text
Workspace
└── Users
    └── <usuario-do-trabalho>/
        ├── .assistant_instructions.md       ← ativação pessoal
        ├── .assistant/                      ← produto ativo após promoção
        │   └── ...
        └── hub_validacao/
            └── <release_id>/
                ├── staging/                 ← importação candidata, inativa
                │   ├── MANIFEST.json
                │   ├── .assistant_instructions.md
                │   └── .assistant/
                ├── testes/                  ← Pacote B, fora da descoberta
                └── evidencias/              ← resultados internos desta release
```

`hub_validacao` é uma pasta customizada de trabalho, não uma convenção da
Databricks. `<release_id>` deve ser neutro e único, por exemplo
`hub-validacao-2026-09-11-<commit-curto>`. O identificador não é um resultado de
aprovação; continua sendo candidato até a homologação.

**Por que staging?** Permite importar, verificar arquivos, abrir imagens e
testar imports da biblioteca candidata sem substituir a instalação existente.
As skills em staging não estão no caminho pessoal oficial; portanto, não
certificar descoberta automática a partir desse local. A fase conversacional
ocorre depois da promoção controlada para o caminho pessoal.

### 3.4 Tipos de caminho que não devem ser confundidos

| Tipo | Exemplo com placeholder | Uso |
|---|---|---|
| Caminho mostrado no workspace/API | `/Users/<usuario>/.assistant` | Navegar e instalar |
| Caminho de leitura pelo Python no workspace filesystem | `/Workspace/Users/<usuario>/.assistant` | `Path`, `open`, `sys.path` |
| Objeto do Unity Catalog | `<catalogo>.<schema>.<tabela>` | Leitura de tabela autorizada por Spark/SQL |
| Arquivo em volume, se autorizado | `/Volumes/<catalogo>/<schema>/<volume>/<release_id>/` | Evidências/dados persistentes de teste |

Não trocar esses formatos por busca/substituição global. Configurar os caminhos
nos widgets do destino. O parâmetro `assistant_root` deve apontar para a pasta
`.assistant`, e não para `hub_snippets` ou para `skills`.

---

<a id="transporte"></a>

## 4. Preparação local, download e envio por e-mail

### 4.1 Fechar a release antes de empacotar

Na máquina local, a pessoa/LLM responsável deve:

1. Ler o guia de pendências e resolver a certificação remota interrompida.
2. Conferir que o produto completo no Free corresponde à fonte candidata.
3. Executar validação local, regressões e QA visual.
4. Gerar o simulado pela ferramenta, sem editar seus arquivos à mão.
5. Revisar e commitar a fonte, o derivado e os artefatos de autoria pertinentes.
6. Conferir o push separadamente, se a release será referenciada no Git remoto.
7. Somente então gerar o pacote de implantação.

Comandos existentes, executados **na raiz do repositório local**:

```powershell
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
.\.venv\Scripts\python.exe tools/ci_local.py
node tools/readme_visuals/validate_production.mjs
.\.venv\Scripts\python.exe tools/render_simulado.py --write
.\.venv\Scripts\python.exe tools/validate_assistant.py --conferir-readme
```

Após revisar e congelar a release:

```powershell
.\.venv\Scripts\python.exe tools/bundle_implantacao.py
```

A saída informará o caminho do ZIP em `.artifacts/`, o total e o commit. O
gerador recusa fonte/derivado divergentes e alterações não commitadas nesses
escopos. `--allow-dirty` existe para revisão, **não deve ser usado no pacote de
homologação**. Não baixar um ZIP antigo só porque ele já está pronto na pasta.

O script não substitui scan de segurança, revisão de código ou verificação de
que não há informação sensível dentro de um arquivo permitido.

### 4.2 Conferir o conteúdo do ZIP, ainda na origem

Abrir o ZIP no gerenciador de arquivos, sem executar scripts, e conferir:

- a raiz contém `.assistant_instructions.md`, `.assistant/` e `MANIFEST.json`;
- não há camada extra `Users/usuario-free/` a instalar no trabalho;
- pastas com ponto inicial estão presentes, não omitidas pelo compactador;
- módulos têm `.py`, não `.py.txt`; imagens têm extensão e conteúdo corretos;
- o manifesto diz `worktree_dirty: false` e commit esperado;
- todos os arquivos listados existem, com tamanho e SHA-256 correspondentes;
- não há caminhos absolutos, `..`, entradas duplicadas, links simbólicos,
  nomes conflitantes por maiúsculas/minúsculas ou arquivos fora da allowlist;
- não há dados reais, outputs sensíveis, segredos ou arquivos de configuração.

O último conjunto de verificações deverá ser automatizado no futuro notebook
01 ou em seu suporte, mas a release também precisa ser validada antes de sair
da máquina pessoal. Não esperar o computador do trabalho para descobrir um
segredo no anexo.

Para obter o hash do ZIP inteiro, no PowerShell:

```powershell
Get-FileHash -LiteralPath ".artifacts/ambiente-databricks-<commit-curto>.zip" -Algorithm SHA256
```

Substituir o nome pelo arquivo realmente gerado. Copiar **todo** o hash. O hash
do ZIP comprova igualdade de bytes entre origem e recebimento; não atesta que
o código é seguro nem autentica o remetente sozinho.

Criar futuramente uma ficha de entrega com:

| Campo | Valor a registrar |
|---|---|
| `release_id` | Identificador neutro |
| Commit de produto | Hash completo |
| Nome e tamanho do Pacote A | Nome real e bytes |
| SHA-256 do Pacote A | 64 caracteres hexadecimais |
| Nome, tamanho e SHA-256 do Pacote B | Preencher apenas quando a suíte existir |
| Inventário | Total derivado dos respectivos manifestos |
| Validações de origem | Data, comando, resultado e escopo |
| Alterações previstas no destino | Instalação pessoal e testes sintéticos |
| Escritas opcionais | Experimento/volume/tabelas temporárias, se aprovados |

Não inserir credenciais na ficha. Os dois documentos desta entrega são
operacionais; ficam fora do ZIP de produto. Podem acompanhar a transferência
como instrução ao operador, após revisão da política de compartilhamento.

### 4.3 Enviar e receber

1. Confirmar autorização do canal e limite do anexo.
2. Anexar o Pacote A e, quando existir, o Pacote B. Anexar a ficha de entrega e
   o plano operacional somente se permitido.
3. Não copiar/colar código no corpo do e-mail para reconstruir centenas de
   arquivos: isso perde árvore, encoding, tipos e rastreabilidade.
4. Informar que o material deve ser salvo antes de ser aberto ou importado.
5. No computador do trabalho, baixar o anexo para uma pasta corporativa aprovada.
6. Aguardar/realizar a inspeção prevista pela organização.
7. Recalcular o SHA-256 com ferramenta autorizada; o PowerShell do exemplo
   anterior não exige Databricks CLI. Se não estiver disponível, usar a
   alternativa fornecida pela TI, não instalar ferramenta por conta própria.
8. Comparar o hash inteiro e o tamanho. Divergência interrompe o processo.
9. Guardar a cópia recebida intacta. Extrair uma cópia para inspeção, sem
   modificar ou recomprimir o original usado como evidência.

Modelo de mensagem, a preencher sem dados sensíveis:

```text
Assunto: Material para homologação do Hub Databricks — <release_id>

Encaminho, pelo canal autorizado, o pacote de código-fonte, documentação e
imagens para homologação em sandbox. Não inclui dados de clientes, credenciais,
histórico Git ou configurações de acesso.

Produto: <nome-do-zip> | commit: <hash>
SHA-256: <hash-completo>
Suíte de testes: <nome-e-hash, quando disponível>

Antes do upload: conferir hashes, inventário e aprovação de segurança.
Importar primeiro em staging; não substituir o ambiente existente sem backup.
Não executar notebooks em lote sem revisar os gates de escrita e dependências.
```

### 4.4 Se for necessário baixar a partir do Databricks Free

A documentação atual distingue **DBC, que contém notebooks**, de **Zip - Source,
que inclui notebooks e arquivos**. Para uma árvore mista como esta, usar a
segunda opção; outputs de notebook não são incluídos nesse formato. Essa é
também a opção de referência para backup misto na seção 5.
[Fonte oficial: importação e exportação](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import).

Procedimento alternativo:

1. Concluir a conferência remota da origem; um download de estado divergente
   não corrige a divergência.
2. No navegador de workspace, localizar a `.assistant` do usuário de origem.
3. Usar o menu da pasta → **Download as → Zip - Source**, ou o rótulo
   equivalente oferecido na interface atual.
4. Baixar também `.assistant_instructions.md`, que fica fora dessa pasta.
5. Na máquina pessoal, inspecionar a estrutura exportada. Não presumir que o
   ZIP tem a mesma raiz do pacote mínimo.
6. Reconstruir um candidato de transporte usando a allowlist do manifesto
   canônico. Excluir da entrega estados gerados pela plataforma, como MCP,
   outros arquivos pessoais e conteúdos não pertencentes ao produto.
7. Comparar arquivos com a release canônica. PNGs e módulos exigem identidade
   de bytes; fonte de notebook exige regra explícita de comparação se a
   exportação normalizar metadados/finais de linha.
8. Se houver diferença funcional, investigar e integrar à fonte por revisão;
   não promover automaticamente o download a nova fonte de verdade.
9. Preferir gerar novamente o ZIP pelo gerador oficial do projeto depois dessa
   reconciliação. Registrar o hash do pacote final, não apenas o hash do download.

Se a opção não existir ou exportar só parte do conteúdo, parar e obter orientação
da plataforma. Não usar DBC e declarar a biblioteca completa por aproximação.

---

<a id="instalacao"></a>

## 5. Backup, upload e ativação no trabalho — sem CLI

### 5.1 Fazer backup antes de tocar no ambiente ativo

Se ainda não existe instalação pessoal, registrar explicitamente “instalação
nova”. Se existe:

1. Inventariar os caminhos atuais do Hub e eventuais conteúdos de outros autores.
2. Baixar a `.assistant` pelo formato de fontes que preserve arquivos e
   notebooks. Guardar esse backup **apenas no ambiente corporativo**.
3. Baixar separadamente a instrução pessoal existente, com e sem ponto inicial
   se ambos os arquivos existirem. Não apagar um arquivo só por ter nome legado.
4. Registrar permissões/compartilhamentos e configurações relevantes por meio
   aprovado. ZIP de fontes não é backup de ACLs, chats ou recursos de plataforma.
5. Abrir o backup e confirmar que contém módulos, Markdown, PNGs e notebooks,
   não apenas os notebooks. Fazer restauração de uma pequena amostra em pasta
   temporária autorizada e conferir leitura/tipo antes da substituição.
6. Registrar nome, data, hash e responsável pelo backup. Não enviar esse backup
   para o e-mail pessoal ou para o Free.

Se `.mcp_servers.json` estiver presente, não editá-lo nem removê-lo. Se o backup
o contiver, tratar o conjunto como estado corporativo restrito. O pacote novo
não deve sobrepor esse arquivo.

### 5.2 Importar em staging

A UI de workspace aceita ZIP e extrai seus arquivos e notebooks. Arquivos
Markdown têm preview próprio; não é correto afirmar genericamente que todo
`.md` no workspace é texto plano. Verificar separadamente o suporte aos recursos
visuais usados pelo projeto.
[Fonte oficial: workspace files](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-basics).

Passo a passo:

1. Entrar no workspace do trabalho com a conta correta.
2. Abrir **Workspace → Users → sua pasta pessoal**.
3. Criar `hub_validacao/<release_id>/staging`.
4. Dentro de `staging`, abrir o menu da pasta e escolher **Import**.
5. Selecionar o Pacote A já conferido e confirmar a importação.
6. Esperar o término e atualizar a árvore. Conferir se surgiu uma camada extra
   com o nome do ZIP. Ajustar somente a localização planejada dos arquivos,
   sem alterar seu conteúdo; registrar o mapeamento efetivo.
7. Importar o Pacote B no nível `<release_id>`, de modo que exista uma única
   pasta `testes/`, não `testes/testes/`.
8. Não usar “Run all” na pasta. Primeiro abrir o notebook 00 e ler os avisos.

Se o ZIP for bloqueado pela política ou pela interface, solicitar rota
aprovada. Um upload manual pasta a pasta pode ser um fallback, mas exige a
mesma matriz de caminhos e comparação de todos os arquivos; “parece completo”
não é suficiente.

### 5.3 Verificar tipo, não apenas extensão

| Conteúdo de origem | Tipo esperado no workspace | Conferência mínima |
|---|---|---|
| Módulo Python de helper ou `_suporte` | `FILE` | Abre como arquivo; import aponta para esse caminho |
| Notebook com marcador de fonte Databricks | `NOTEBOOK` | Abre em células executáveis/Markdown |
| Novo notebook `.ipynb` | `NOTEBOOK` | Células, ordem e metadados preservados |
| README, SKILL, prompt, YAML e JSON | `FILE` | Texto íntegro e nome exato |
| PNG | `FILE` binário | Hash, dimensões e visual corretos |

A identificação de notebook depende de `.ipynb` ou do marcador de fonte na
primeira linha em formatos suportados. Portanto, um módulo não deve ganhar
`# Databricks notebook source`. Conferir conversões e nomes reais após o upload,
inclusive eventual remoção da extensão no nome exibido.
[Fonte oficial: conversão de arquivo e notebook](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import).

O primeiro piloto deve provar pelo menos: um módulo, seu notebook de exemplo,
um `SKILL.md`, um README e um PNG. Depois, a conferência precisa abranger
**todo o manifesto**, não somente essa amostra.

### 5.4 Testar a candidata antes da ativação

Executar os notebooks 00 a 06 apontando `assistant_root` para a `.assistant`
de staging. Executar opcionais e integração de escrita apenas com autorização.
São testes da candidata, não da descoberta pessoal da Genie Code.

Não duplicar as skills na raiz pessoal enquanto os arquivos de staging ainda
estiverem em verificação. Não copiar instruções pessoais por cima de instruções
corporativas existentes sem revisão.

### 5.5 Promover para a instalação pessoal

Depois de estrutura, imports e núcleo técnico aprovados:

1. Reservar uma janela sem edição concorrente das pastas envolvidas.
2. Confirmar backup recuperável e plano de retorno.
3. Comparar nomes e ownership das skills existentes com
   `EXPECTED_SKILL_NAMES` e `LEGACY_MANAGED_SKILL_NAMES` da release.
4. Substituir somente as skills geridas pelo Hub e os cinco diretórios `hub_`
   próprios, após conferir que não contêm adições de terceiros.
5. Preservar outras skills, conteúdos alheios e estado MCP. Se houver arquivo
   de terceiro dentro de pasta aparentemente gerida pelo Hub, resolver antes.
6. Instalar arquivos de raiz do produto previstos no manifesto, conciliando
   qualquer versão preexistente modificada no trabalho.
7. Para `.assistant_instructions.md`, comparar com o backup e com as diretrizes
   corporativas. Fazer merge revisado quando necessário, sem enfraquecer
   políticas. Registrar o hash final como variante corporativa se o texto mudar.
8. Repetir inventário, tipos, hashes e imports no caminho ativo.
9. Abrir chats novos e executar os notebooks 08 e 09 como roteiros de conversa.

**Não é uma cópia atômica.** Se a UI exigir substituição em várias etapas,
manter o uso do Hub suspenso durante a janela e verificar cada grupo antes do
próximo. Não mover a pasta `.assistant` inteira para substituir conteúdo de
outros autores.

Uma instrução pessoal conciliada não terá o mesmo hash do Pacote A. Isso não
pode ser escondido como igualdade: registrar a exceção, o diff, a aprovação e
um manifesto suplementar interno. Módulos e assets não recebem adaptações
silenciosas por esse mecanismo.

---

<a id="gates"></a>

## 6. Gates, estados e limites de execução

### 6.1 Portões de passagem

| Gate | Para avançar, precisa existir | Se falhar |
|---|---|---|
| G0 — Autorização | Canal, material e sandbox aprovados | Não enviar/importar |
| G1 — Release | Fonte/derivado íntegros, commit e manifestos | Corrigir origem |
| G2 — Transporte | ZIP recebido idêntico, inspeção aprovada | Não importar |
| G3 — Staging | Inventário, tipos, caminhos e arquivos conferidos | Não ativar |
| G4 — Núcleo | Imports e contratos essenciais aprovados | Não usar em tarefa real |
| G5 — Capacidades | Cada biblioteca/integração necessária homologada | Marcar capacidade indisponível e resolver |
| G6 — Genie Code | Instruções, 13 skills e 16 prompts avaliados | Não anunciar homologação integral |
| G7 — Operação | Limpeza, rollback e piloto revisados | Não liberar à equipe |

O usuário deseja manter todas as funcionalidades. Portanto, bibliotecas
opcionais não serão removidas do produto. Pode haver um **piloto restrito ao
núcleo**, explicitamente identificado, enquanto se resolvem dependências. Isso
não equivale a liberar integralmente o Hub.

### 6.2 Estados dos casos

| Estado | Significado | Pode ser contado como aprovado? |
|---|---|---|
| `PASS` | Executou e satisfez todas as assertions/rubrica | Sim, naquele escopo e ambiente |
| `FAIL` | Executou e divergiu do contrato | Não |
| `BLOQUEADO` | Permissão, política, dependência ou acesso impediu testar | Não |
| `NAO_EXECUTADO` | Ainda não tentado | Não |
| `NAO_APLICAVEL` | Requisito fora do escopo aprovado, com justificativa | Não é PASS; deve aparecer separado |

Preservar ainda o `status_original` quando importar evidência do smoke legado:
`OPTIONAL_MISSING` não vira PASS; `BLOQUEADO_ESPERADO` do Free não vira contrato
corporativo. Um teste negativo bem-sucedido pode ser `PASS` **quando** capturar
a exceção exata prevista para aquela entrada inválida.

### 6.3 Limites padrão da campanha

- Usar apenas dados sintéticos e objetos explicitamente pertencentes à release.
- Começar com fixtures mínimas determinísticas; bases de treino de 200 a 500
  linhas, limite geral inicial de 1.000 linhas. Casos que precisarem ultrapassar
  isso devem justificar a mudança antes da execução.
- Seed padrão 42 onde a API aceitar; conservar seeds de regressões existentes
  quando forem parte do oráculo, registrando a exceção.
- Não executar leitura ampla de catálogos ou tabelas de produção.
- Não usar `%pip install -r requirements-optional.txt` indiscriminadamente.
- Não instalar PySpark sobre o runtime Databricks; não atualizar NumPy/pandas
  para “tentar fazer funcionar” sem análise de compatibilidade.
- Escritas persistentes, MLflow, limpeza de artefatos, integrações e criação de
  jobs ficam desabilitadas por padrão na futura suíte.
- Definir orçamento e duração máxima por notebook com o dono do compute.
  Estimativa de duração não é timeout técnico nem autorização para aumentar
  máquinas/GPU automaticamente.
- Em serverless, não usar RDD, configurações de cluster ou cache como premissa
  universal de teste. Examinar as limitações atuais e testar o comportamento
  compatível do helper.
  [Fonte oficial: limitações serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations).

---

<a id="contrato-suite"></a>

## 7. Contrato obrigatório da futura suíte `testes/`

### 7.1 Como cada notebook deve ensinar

Cada notebook deve permitir que uma pessoa entenda **o que vai acontecer antes
de apertar Run**. Adotar este molde; ele é contrato de autoria, não sugestão:

| Bloco/célula | Tipo | Conteúdo obrigatório |
|---|---|---|
| Abertura | Markdown | Cabeçalho CRM ou Squad, título, objetivo, público, release e escopo |
| Antes de executar | Markdown | Pré-requisitos, compute, dependências, custo, permissões e efeitos |
| Parâmetros | Código | Widgets com defaults seguros e validação de valores |
| Confirmação do alvo | Markdown + código | Mostrar destino de forma mínima; impedir placeholders e alvo fora do escopo |
| Dados do teste | Markdown + código | Schema, fixture, motivo da escolha, cálculo esperado e construção |
| Cada caso | Markdown antes do código | ID, pergunta, entrada, contrato, resultado esperado e por que esse resultado é correto |
| Execução do caso | Código | Chamada real, coleta limitada e assertions; não apenas `print` |
| Interpretação | Markdown após o código | Como ler a saída, distinguir falha do produto e bloqueio do ambiente |
| Evidência | Código | Registro estruturado com caso, esperado, observado e estado |
| Limpeza | Markdown + código separado | Lista exata de recursos criados e gate de autorização |
| Fechamento | Markdown + código | Resumo completo, pendências, próximo notebook e barreira de avanço |

Não substituir explicações por comentários curtos dentro do código. Não
prometer saída igual a um screenshot quando o algoritmo admite variação.
Identificar exemplos de saída como **“exemplo esperado, não execução realizada”**.
Nunca preencher antecipadamente células de resultados com `PASS`.

Exemplo de texto que deve anteceder um caso:

```text
Caso SCR-DQ-02 — Nulos exatamente no limite de alerta

O que estamos verificando: se o diagnóstico classifica corretamente uma coluna
quando 1 de 20 registros é nulo e o limite de alerta é 5%.

Por que o resultado esperado é WARN: 1 ÷ 20 × 100 = 5%. O helper usa comparação
inclusiva no limite. A chave é única e não nula, e a data não é verificada neste
caso, para que nenhum outro alerta altere o resultado.

O que você deve ver: status 'warn', score 95, null count 1, null pct 5.0 e um
alerta de nulidade. Se aparecer FAIL, verificar primeiro se a fixture introduziu
outro problema. Não alterar o limite para fazer o teste passar.
```

### 7.2 Parâmetros comuns e significado

| Parâmetro planejado | Padrão | Como preencher / regra |
|---|---|---|
| `release_id` | Vazio | Copiar da ficha; obrigatório e compatível com nomes seguros |
| `target_environment` | `work` | Nunca usar o oráculo de bloqueio do Free nesta campanha |
| `assistant_root` | Vazio | Caminho filesystem da `.assistant` candidata ou ativa; confirmar antes de importar |
| `suite_root` | Vazio | Caminho da pasta `testes`; não pode apontar para o produto |
| `manifest_path` | Vazio | `MANIFEST.json` conferido do Pacote A |
| `compute_profile` | Vazio | Rótulo informado pelo operador: serverless ou runtime clássico autorizado |
| `seed` | `42` | Inteiro; caso legado pode declarar seed própria |
| `max_rows` | `1000` | Inteiro positivo, respeitando o limite aprovado |
| `allow_persistent_writes` | `false` | Autoriza apenas os objetos enumerados no plano do caso |
| `allow_mlflow_writes` | `false` | Gate separado; experimento obrigatório quando verdadeiro |
| `mlflow_experiment_path` | Vazio | Experimento de sandbox autorizado, não um experimento de produção |
| `evidence_root` | Vazio | Destino interno aprovado; se vazio, exibir resultado sem persistência |
| `allow_cleanup` | `false` | Somente recursos criados por esta execução e registrados no ledger |
| `execution_id` | Gerado por execução | Identificador único para evitar colisão entre reexecuções |

Widgets retornam valores que precisam ser interpretados/validados; o texto
`"false"` não pode ser convertido por simples `bool(texto)`. Usar parser
estrito para booleanos e limites numéricos. Nenhum widget contém senha/token.
[Fonte oficial: widgets](https://learn.microsoft.com/en-us/azure/databricks/notebooks/widgets).

Ao alternar de staging para ativo, reiniciar a sessão Python ou invalidar
explicitamente os imports de forma segura e conferir `module.__file__`. Mudar
`sys.path` sozinho não remove módulos já carregados de `sys.modules`.

### 7.3 O que deve haver no suporte, sem reimplementar o produto

- `configuracao.py`: valida parâmetros, paths, limites e perfil de execução.
- `resultados.py`: coleta casos e produz tabela/JSON; propaga reprovação ao final.
- `integridade.py`: valida manifestos e arquivos por allowlist e tipo esperado.
- `fixtures_oraculo.py`: fixtures mínimas e resultados calculados manualmente,
  independentes do helper testado.
- `casos_regressao.py`: adaptação rastreada de testes existentes; não cópia
  modificada dos algoritmos do produto.

Reutilizar `unittest`/assertions e testes existentes quando adequados. Não
introduzir framework remoto ou serviço de avaliação só para orquestrar esta
campanha. A separação entre código reutilizável e testes em notebooks está
alinhada à orientação oficial de testes.
[Fonte: testes unitários em notebooks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/testing).

### 7.4 Registro de evidência por caso

Cada linha deverá conter, no mínimo:

```json
{
  "release_id": "<release>",
  "source_commit": "<commit>",
  "package_sha256": "<sha256-do-pacote>",
  "suite_version": "<versao>",
  "execution_id": "<execucao>",
  "case_id": "SCR-DQ-02",
  "notebook_id": "04",
  "object_path": "hub_scripts/data_quality_check",
  "api": "data_quality_check",
  "fixture_id": "dq-20-linhas-1-nulo-v1",
  "status": "NAO_EXECUTADO",
  "expected": {"status": "warn", "score": 95},
  "observed": null,
  "runtime": {"python": null, "spark": null, "compute_profile": null},
  "dependencies": {},
  "duration_seconds": null,
  "writes_created": [],
  "cleanup_status": "NAO_APLICAVEL",
  "error_class": null,
  "reason": null,
  "evidence_reference": null
}
```

É um **modelo**, não resultado. Guardar mensagens completas e referências
reais somente no destino interno autorizado; relatórios exportáveis usam
identificadores neutros e não trazem dados corporativos.

### 7.5 Como comparar resultados sem mascarar erro

1. Inteiros, nomes de colunas, chaves de dicionário e enums: comparação exata.
2. DataFrames: schema explícito e comparação por chave/ordem canônica quando a
   ordem não fizer parte do contrato. Não comparar `collect()` sem ordenação.
3. Floats determinísticos: tolerância documentada por caso; ponto inicial
   `abs_tol=1e-8`, ajustável somente com justificativa matemática.
4. Valores arredondados pelo próprio helper: respeitar sua precisão, não uma
   precisão inventada pelo teste.
5. Amostragem/treino: conferir propriedades e limites previamente definidos;
   não exigir a acurácia histórica exata em runtime diferente.
6. Exceções: tipo e fragmento significativo esperados; não usar
   `except Exception: PASS`.
7. Saídas visuais: estrutura de dados + renderização humana; não somente
   “objeto Figure existe”.
8. Oráculos: não obter o esperado chamando novamente a mesma função sob teste.

O executor deve registrar as falhas e concluir com reprovação explícita se um
caso obrigatório falhar. Um `dbutils.notebook.exit` que apenas devolve JSON
pode deixar a tarefa concluída mesmo com falhas dentro do JSON: o consolidado
deve lê-las e interromper a liberação.

### 7.6 Reprodutibilidade e limpeza

Cada notebook reconstrói suas próprias fixtures; não depende de variáveis ou
temp views criadas em outro notebook. Usar views temporárias **de sessão**
com nome derivado da execução, sem global temp views. Para arquivos locais
temporários, criar diretório exclusivo e apagá-lo apenas se constar no ledger.
Esses arquivos locais de teste não devem ser confundidos com persistência de
evidências em workspace/volume.

O ledger registra **cada recurso efetivamente criado**, tipo, nome exato,
execution_id e forma de limpeza. Nunca limpar por um prefixo amplo sem comparar
com esse ledger. Se a sessão cair antes de limpar, o relatório deve apontar
recursos possivelmente residuais e o procedimento de inspeção manual.

---

<a id="mapa-notebooks"></a>

## 8. Mapa de execução dos notebooks

Todos os notebooks abaixo estão **planejados**, não foram criados nesta entrega.

| Ordem | Notebook | Onde / quando | Saída principal |
|---|---|---|---|
| 00 | `00_LEIA_PRIMEIRO_PRECHECK.ipynb` | Antes de qualquer teste | Perfil, pré-requisitos e bloqueios |
| 01 | `01_PACOTE_E_INSTALACAO.ipynb` | Staging e depois ativo | Integridade e tipos por arquivo |
| 02 | `02_IMPORTS_E_CONTRATOS.ipynb` | Staging e depois ativo | Importabilidade e origem real dos módulos |
| 03 | `03_SNIPPETS_SPARK_E_TEMPORALIDADE.ipynb` | Compute autorizado | Contratos Spark e ausência de leakage |
| 04 | `04_SCRIPTS_OPERACIONAIS.ipynb` | Compute autorizado | Sete scripts, positivos e negativos |
| 05 | `05_ML_NUCLEO_E_METRICAS.ipynb` | Núcleo de ML | Métricas, splits, monitoramento e costuras |
| O01–O14 | `opcionais/` | Sessões/dependências isoladas | Capacidade funcional de cada wrapper |
| 06 | `06_VISUAL_E_DOCUMENTACAO.ipynb` | Preview + compute quando necessário | Imagens, HTML/Plotly e leitura |
| 07 | `07_MLFLOW_E_INTEGRACOES.ipynb` | Somente com autorização de escrita | Tracking, permissões e limpeza |
| 08 | `08_SKILLS_E_INSTRUCOES.ipynb` | Instalação pessoal ativa, chats novos | 39 casos de roteamento + rubrica de uso |
| 09 | `09_PROMPTS_E_RESPOSTAS.ipynb` | Chats da Genie Code | Campanha comparável dos 16 prompts |
| 10 | `10_EXEMPLOS_E_PADROES.ipynb` | Material existente e sandbox | Exemplos rastreados e moldes coerentes |
| 11 | `11_HOMOLOGACAO_E_LIMPEZA.ipynb` | Fechamento | Relatório, resíduos, decisão e limites |

A numeração é a ordem de leitura. Opcionais entram antes do caso que dependa
deles. O notebook 07 pode ficar bloqueado sem impedir a investigação dos
outros, mas bloqueia a homologação da capacidade de tracking. O notebook 11
nunca converte pendências em aprovação para concluir a sequência.

<a id="testes-tecnicos"></a>

## 9. Especificação dos notebooks técnicos

### 9.1 Notebook 00 — LEIA PRIMEIRO / precheck

**Objetivo:** impedir que os testes comecem no destino errado, sem saber quais
permissões e dependências existem. **Não instala bibliotecas nem cria objetos
persistentes.** A execução de consultas de diagnóstico ainda usa compute.

Sequência obrigatória:

| Célula/grupo | Conteúdo | Esperado |
|---|---|---|
| 00-M01 | Explicação de staging, ativo, sintético, gates e efeitos | Leitor entende que nada foi homologado ainda |
| 00-C01 | Widgets e validação estrita | Placeholders/vazios obrigatórios bloqueiam o avanço |
| 00-C02 | Versão Python, Spark e pacotes por `importlib.metadata` | Tabela de versões reais; ausente fica explícito |
| 00-C03 | Conferir paths exatos de produto, suíte e manifesto | Diretórios distintos, existentes e autorizados |
| 00-C04 | Conferir sessão Spark com consulta mínima `SELECT 1` | Um registro com valor 1 |
| 00-M02 | Checklist humano: runtime/base, modo de acesso, permissões e custo | Evidência de configuração, sem inferir tudo de `spark.version` |
| 00-C05 | Classificar dependências por módulo/caso | Nenhum opcional ausente derruba silenciosamente todo o inventário |
| 00-M03 | Como escolher a rota de dependências | Ação encaminhada à política do ambiente |
| 00-C06 | Resumo de precheck e bloqueios | G0/G2 explícitos; próximo passo = notebook 01 |

Testes negativos do próprio precheck: `max_rows=-1`, booleano inválido,
`target_environment=free`, `assistant_root` fora do escopo declarado e caminho
de evidências igual à raiz do produto. Cada um deve bloquear **antes** de
qualquer escrita. Testar com entradas de configuração, sem tentar acessar
recursos corporativos proibidos.

No serverless, preferir o painel **Environment** e as fontes de pacotes
aprovadas; registrar ambiente-base e dependências efetivas. Não instalar
PySpark. Aplicar uma alteração de ambiente reinicia Python: executar novamente
o precheck e os imports. Em compute clássico, seguir o procedimento de
bibliotecas do runtime/política concedidos, sem supor que o fluxo serverless é
idêntico.
[Fonte oficial: configuração serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies).

Não copiar os pins históricos do laboratório ou as versões da `.venv` local
como lock corporativo. A futura suíte deverá gerar um inventário de versões
**observadas** e uma combinação de dependências **homologada no destino**.

### 9.2 Notebook 01 — pacote, inventário e instalação

**Objetivo:** comprovar quais arquivos chegaram, onde estão e de que tipo são.
Executar uma vez em staging e outra no ativo. Não alterar o produto para fazer
os hashes coincidirem.

| Caso | Ação planejada | Resultado esperado |
|---|---|---|
| PKG-01 | Ler `MANIFEST.json`; validar schema e commit | Campos obrigatórios e release esperada; `worktree_dirty=false` |
| PKG-02 | Validar caminhos da lista antes de abri-los | Nenhum absoluto, traversal, duplicata ou colisão de nomes |
| PKG-03 | Comparar conjuntos esperado × instalado | Ausentes, extras, tipos e divergências listados individualmente |
| PKG-04 | Comparar tamanho e SHA-256 de workspace files | Igualdade RAW para módulos, Markdown, JSON/YAML, SVG e PNG |
| PKG-05 | Conferir notebooks por mapeamento de importação | Todos reconhecidos como notebooks, sem perder células/código |
| PKG-06 | Conferir arquivos sensíveis à descoberta | Nome exato da instrução, `skills/<nome>/SKILL.md` e frontmatter |
| PKG-07 | Conferir assets e cabeçalhos | Todos os itens do manifesto visual presentes |
| PKG-08 | Conferir extras legítimos no ativo | Conteúdo de terceiros/MCP preservado, identificado e fora da comparação do produto |
| PKG-09 | Conferir segunda passagem staging → ativo | Nenhum arquivo esquecido nem import apontando ao staging |

**Não prometer uma leitura de notebook como se fosse arquivo comum.** Se o
runtime não permitir ler seu conteúdo por filesystem, usar exportação de fonte
pela UI e validar a cópia exportada no canal interno. Uma API de workspace
somente leitura autenticada pela sessão pode ser uma rota futura opcional,
desde que aprovada e implementada sem PAT em widget; não é pré-requisito deste
plano sem CLI.

Definir em `inventario_produto.json`:

- `source_path`: caminho no ZIP;
- `installed_path`: caminho realmente criado pela importação;
- `expected_object_type`: FILE ou NOTEBOOK;
- `comparison_mode`: `raw` ou `notebook_source`;
- `source_sha256`, tamanho e referência ao manifesto;
- eventual normalização de notebook, com justificativa e versão do algoritmo.

Para fonte de notebook, aceitar apenas normalizações explicitamente aprovadas
(por exemplo, finais de linha e quebra terminal previstas no verificador
existente). Se a UI adicionar metadados de ambiente, mostrar o diff e revisá-lo;
não remover genericamente comentários, células, `%md` ou strings para forçar
igualdade. Conservar os hashes bruto e normalizado quando houver normalização.

Casos negativos usam **manifestos/arquivos de teste em memória ou temporários**:
entrada duplicada, `../fora`, PNG com um byte alterado, arquivo faltante e tipo
de notebook divergente. Esperado: cada adulteração é detectada. Não corromper
a instalação ativa para testar o verificador.

Saída: tabela por arquivo + sumário `esperados / encontrados / iguais /
divergentes / ausentes / extras-permitidos`. Uma contagem total igual com
conteúdo diferente é reprovação.

### 9.3 Notebook 02 — imports e contratos públicos

**Objetivo:** assegurar que a biblioteca instalada é realmente a biblioteca
usada pelo Python. Um arquivo correto em disco pode estar sendo ignorado por
um módulo antigo já carregado.

1. Ler o inventário sem importar notebooks de exemplo.
2. Conferir o marcador da primeira linha dos `.py`; módulos não podem ser
   notebooks disfarçados.
3. Registrar `assistant_root` e inserir essa raiz no caminho de imports.
4. Importar objetos de modo controlado, um a um, registrando dependências
   ausentes. Não executar recursivamente todos os `.py`.
5. Conferir `module.__file__` e a origem das APIs reexportadas pelo `__init__`.
6. Conferir nomes públicos e assinaturas com a implementação da release.
7. Fazer uma chamada mínima por API onde couber; os testes funcionais completos
   ficam nos notebooks próprios.
8. Repetir com sessão limpa após promoção ou atualização.

O uso de módulos em workspace files com `import` é suportado; outro diretório
precisa estar acessível no caminho Python. A distribuição para executores e a
precedência de bibliotecas dependem do runtime. Testar qualquer UDF/código
distribuído efetivamente usado, em vez de inferir seu funcionamento do import
no driver.
[Fonte oficial: módulos Python](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-modules).

Regras de classificação:

| Ocorrência | Classificação e ação |
|---|---|
| Módulo público previsto ausente | FAIL de instalação/empacotamento |
| Biblioteca opcional declarada ausente | BLOQUEADO da capacidade; registrar nome exato |
| Dependência presente, mas import falha por incompatibilidade binária | FAIL de compatibilidade; não chamar de mera ausência |
| Import veio de staging quando o alvo é ativo | FAIL de versão/origem |
| API diferente do manifesto da release | FAIL de contrato |
| Um `exemplo_*.py` foi importado como módulo | FAIL do instrumento de testes; interromper execução em lote |

**Cobertura exigida:** mapear todas as 60 pastas de objeto atuais, distinguindo
51 snippets, sete scripts e dois objetos de moldes. As constantes são testadas
por existência, tipo, valores e consumo, não por uma chamada fictícia. O
inventário deve incluir também os pacotes `__init__`, sem contá-los como novas
funcionalidades.

### 9.4 Notebook 03 — snippets Spark e temporalidade

**Fontes de reaproveitamento:** seção funcional Spark de
`tools/spark_smoke_test.py`, regressões em `hub_snippets/tests/test_core.py` e
implementações dos objetos abaixo. Cada função adaptada terá origem, hash e
alterações de instrumentação em `origens_e_adaptacoes.json`.

#### A. Fixtures e schema

Usar os geradores `hub_snippets.testing.fixtures` para cenários representativos
e fixtures mínimas escritas à mão para oráculos exatos. Os geradores oferecem
`base_tabular`, `serie_temporal`, `fatos_e_features` e `safras`.

- Mesma seed e parâmetros → mesmo multiconjunto de linhas/schema.
- A seed não garante uma proporção aleatória exata de nulos/eventos; para
  testar 5% exatos, construir 20 linhas com um nulo manualmente.
- Coluna totalmente nula exige schema explícito; não depender de inferência.
- Não gravar tabelas para compartilhar fixtures entre notebooks. Cada notebook
  cria seus próprios DataFrames e suas views de sessão.

#### B. Matriz de cobertura

| Objeto / API principal | Positivo obrigatório | Borda/negativo obrigatório | Oráculo |
|---|---|---|---|
| `null_summary.null_summary` | Base com 10 linhas e duas nulas em coluna conhecida | Coluna totalmente nula; base vazia tipada conforme contrato | Contagens e percentuais calculados manualmente |
| `smart_sample.smart_sample` | Amostra limitada e opção de estratificação suportada | Limites inválidos previstos pela implementação | Schema, limite e cobertura de estratos; não igualdade global entre runtimes |
| `date_features.extrair_features_data` | Datas conhecidas e feriado adicional via `holiday_dates` | Data nula e limites de calendário | Valores de calendário e distinção entre feriado fixo e calendário fornecido |
| `psi_calculator.calcular_psi` | Distribuições idênticas e distribuição alterada | Base/atual vazia, bins inválidos, coluna ausente | PSI zero para igualdade; soma de contribuições conhecida para contraste |
| `psi_calculator.calcular_csi` | Categorias iguais e introdução de categoria | Nulo versus categoria literal `__MISSING__`; limite de cardinalidade | Ausência não pode colidir com categoria real |
| `psi_calculator.interpretar_psi` | Com e sem política explícita | Limites invertidos; valor inválido | Sem thresholds não inventa classificação universal |
| `safe_display.safe_display` | Pequena base e base acima do limite configurado | Fronteira do limite | Conteúdo exibido limitado; não exigir cache |
| `join_diagnostics.diagnosticar_join` | Relações 1:1 e 1:N conhecidas | Chaves nulas e duplicidade dos dois lados | Cobertura e expansão comparadas a contas independentes |
| `pit_join.pit_join` | Versão mais recente disponível na decisão | Duplicatas, nulos, sem histórico e features futuras | Preservação do multiconjunto de fatos e exclusão de leakage |

O autor dos testes deverá ler a assinatura de cada API no commit congelado
antes de escrever chamadas. As linhas acima delimitam casos, não autorizam
inventar parâmetros para satisfazê-los. Comportamento de borda não contratado
deve ser registrado como descoberta e submetido à revisão, não aprovado por
qualquer saída que ocorrer.

#### C. PIT: caso mínimo obrigatório com resposta conhecida

Reutilizar sem enfraquecer a fixture de preservação existente no smoke:

| Fato | Data de decisão | Resultado de `valor` |
|---|---|---:|
| C1, primeira ocorrência | 10/03/2026 | 20 |
| C1, segunda ocorrência idêntica | 10/03/2026 | 20 |
| C2 | 10/03/2026 | nulo |
| C3 | 10/03/2026 | nulo |
| Chave nula | 10/03/2026 | nulo |
| C4 | Data nula | nulo |

Histórico de C1: 31/01 → 10; 28/02 → 20; 09/03 → 99. Histórico de C2:
09/03 → 77. Atraso de publicação de três dias. A versão de 09/03 só fica
disponível em 12/03 e não pode entrar numa decisão de 10/03.

Assertions obrigatórias:

- seis fatos entram e seis linhas saem;
- C1 continua com duas ocorrências, ambas com 20;
- valores 99, 77 e a versão antiga 10 não aparecem;
- diagnóstico: `com_feature=2`, `sem_chave_ou_data=2`,
  `entidade_sem_historico=1`, `sem_feature_disponivel_na_data=1`;
- comparar multiconjunto completo, não apenas a soma dos diagnósticos;
- conferir que as datas e as chaves não foram alteradas no resultado.

Explicar visualmente com tabela antes/depois em Markdown. Não é necessário
criar outra imagem PNG para ensinar este teste.

### 9.5 Notebook 04 — os sete scripts operacionais

**Objetivo:** chamar todos os scripts e conferir seus contratos heterogêneos.
Não impor `status` a uma função que devolve lista, DataFrame ou texto.

#### A. APIs reais a preservar

| Objeto | Assinatura de referência na inspeção | Retorno |
|---|---|---|
| `data_quality_check` | `(table_name, pk_columns, date_column=None, thresholds=None)` | Dicionário com `status`, `score`, `thresholds`, `checks`, `alerts` |
| `quick_profile` | `(table_name, sample_fraction=0.1, max_categories=20, *, seed=42)` | Dicionário com métricas completas e amostrais separadas |
| `rfv_calculator` | `(table_name, col_cliente, col_data, col_valor, dt_referencia, periodos=(30,60,90))` | DataFrame Spark |
| `drift_detector` | `(table_name, date_col, date_ref, date_comp, cols=None, method='psi', *, num_bins=10, relative_error=0.001, epsilon=1e-6, warning_threshold=None, critical_threshold=None)` | Dicionário por variável |
| `schema_to_yaml` | `(table_name, include_comments=True, include_stats=False)` | Texto YAML ou fallback JSON |
| `schema_to_dict` | `(table_name, *, include_comments=True, include_stats=False)` | Dicionário; pertence ao objeto `schema_to_yaml` |
| `naming_checker` | `(table_name, *, enforce_prefix=False, allowed_table_prefixes=(), max_col_length=255)` | Lista de violações |
| `doc_coverage` | `(notebook_path)` | Dicionário de cobertura heurística |

Importar pela interface pública da pasta, por exemplo
`from hub_scripts.data_quality_check import data_quality_check`.
Revalidar assinaturas antes de implementar, caso a release mude.

#### B. `data_quality_check`: resultados numéricos conhecidos

Usar views temporárias de sessão e schema explícito. Para isolar nulidade,
chamar sem `date_column`, com `pk_columns=['id']`, limites
`null_warn=5.0`, `null_fail=20.0`, chave única/não nula e apenas uma coluna
com nulos planejados.

| Caso | Fixture | Esperado exato |
|---|---|---|
| SCR-DQ-01 | 20 linhas, zero nulos, IDs únicos | `status='pass'`, `score=100`, `row_count=20`, zero alerts |
| SCR-DQ-02 | 20 linhas, um nulo na coluna valor | `status='warn'`, `score=95`, `count=1`, `pct=5.0`, um alerta warn |
| SCR-DQ-03 | 20 linhas, quatro nulos em valor | `status='fail'`, `score=75`, `count=4`, `pct=20.0`, um alerta fail |
| SCR-DQ-04 | Quatro linhas completas, IDs `[1,1,2,3]` | `duplicate_rows=1`, status fail e alerta `pk_uniqueness` |
| SCR-DQ-05 | Chave composta com um componente nulo | `null_key_rows` correto e falha de chave; conferir demais alertas da fixture |
| SCR-DQ-06 | `pk_columns=[]` | `ValueError`, antes da leitura da tabela |
| SCR-DQ-07 | `null_warn > null_fail` ou freshness negativo | `ValueError` correspondente |
| SCR-DQ-08 | Coluna de chave ausente | `ValueError` com coluna ausente |
| SCR-DQ-09 | Base vazia tipada, sem date_column | Registrar contrato atual: zero linhas pode resultar `pass`; política consumidora rejeita vazio separadamente |

Freshness fica em bloco independente: usar a data do driver capturada uma vez
no começo, `date_column` do tipo date, uma fixture “hoje” e outra de dez dias
antes, com limite dois. Esperado: `days_old` 0/pass e 10/fail, sem outros
alertas. Mostrar timezone/data usada; não usar data fixa antiga que passa hoje
e falha amanhã sem explicação. Não trocar a data global do ambiente para testar.

O score é uma fórmula local do helper; `pass` não é homologação universal.
Adicionar caso consumidor que levante erro diante de `status='fail'`, provando
que a interrupção pertence ao notebook, não ao diagnóstico.

#### C. Demais scripts

| Script / casos | Fixture e execução | Esperado e cuidado |
|---|---|---|
| `quick_profile`, positivo | Base pequena conhecida, `sample_fraction=1.0` | `total_rows`, `sample_rows`, nulos completos e min/max/média conferíveis |
| `quick_profile`, amostra | Mesma base, fração válida menor que 1 e seed declarada | Retorno distingue campos `*_full_table` e `*_sample`; não confundir estimativa com população |
| `quick_profile`, negativo | Fração 0 ou maior que 1; max_categories 0 | `ValueError` correspondente |
| `drift_detector`, igualdade | Duas coortes com a mesma distribuição numérica | PSI zero e `classification='not_classified'` sem thresholds |
| `drift_detector`, política | Mesma fixture, thresholds 0.1 e 0.25 escolhidos só para teste | Classificação stable; não documentar esses limites como norma |
| `drift_detector`, contraste | Coorte com buckets alterados e `relative_error=0` no caso mínimo | PSI igual à soma manual de contribuições dos buckets, dentro da tolerância |
| `drift_detector`, negativos | Coorte vazia; `method='ks'`; bins 1; epsilon 0; date_col também em cols | `ValueError` específico; nenhum método KS inventado |
| `schema_to_dict`, básico | Schema com string, inteiro, decimal/data e comentário com aspas | Nomes, tipos, nulabilidade e comentários preservados |
| `schema_to_dict`, stats | Pequena base conhecida, include_stats=True | row_count, null_count/null_pct corretos; distinct aproximado identificado como tal |
| `schema_to_yaml`, serialização | Mesmo schema; parse seguro da string retornada | Payload equivalente a schema_to_dict; nenhum arquivo gravado pelo helper |
| `schema_to_yaml`, fallback | Teste isolado simula apenas ausência de PyYAML | JSON válido com conteúdo equivalente; restaurar monkeypatch; não desinstalar lib do workspace |
| `naming_checker`, positivo local | View temporária com colunas snake_case | Há warning por nome não qualificado; não esperar lista vazia nessa fixture |
| `naming_checker`, convenção | Coluna `ValorTotal`, prefixo requerido ausente, limite curto | Violações com `policy` e objeto corretos; não apresentar regra local como regra UC |
| `naming_checker`, negativos | enforce_prefix=True e lista vazia; max_col_length=0 | `ValueError`, sem criar tabela |
| `naming_checker`, integração UC | Tabela sintética autorizada de três níveis, se disponível | Com nomes válidos e sem política extra, lista vazia |
| `doc_coverage`, 100% | Arquivo ipynb temporário com células Markdown, código | 1 code, 1 markdown, coverage 100%, índices vazios |
| `doc_coverage`, 50% | Células Markdown, código, código | 2 code, 1 markdown, coverage 50%, `uncovered_cell_indexes=[2]` |
| `doc_coverage`, 0% | Duas células de código, sem Markdown | 2 code, 0 markdown, coverage 0%, índices `[0,1]` |
| `doc_coverage`, sem código | Somente Markdown | coverage 100% por convenção; não afirmar qualidade semântica |
| `doc_coverage`, negativos | Path inexistente; fonte `.txt` existente; ipynb inválido | FileNotFoundError, ValueError ou erro JSON correspondente ao caso |

Para `doc_coverage`, construir arquivos temporários a partir de pequenas
fixtures JSON/texto dentro do diretório exclusivo da execução. Não passar URL
do workspace nem presumir que o notebook nativo é arquivo legível por `Path`.
Adicionar também fontes `.py`, `.sql`, `.scala` e `.r` com marcadores corretos
para testar o parser, **sem executar essas linguagens**. Não usar esse teste
de parser como prova de disponibilidade de Scala/R no compute.

#### D. RFV: uma conta que o leitor consegue conferir

Usar `dt_referencia='2026-03-10'`, `periodos=[3]` e esta fixture:

| Cliente | Data | Valor | Papel |
|---|---|---:|---|
| A | 08/03/2026 | 10 | Dentro dos três dias |
| A | 10/03/2026 | 20 | Dentro, inclusive data de corte |
| A | 11/03/2026 | 999 | Futuro, proibido |
| B | 01/03/2026 | 5 | Passado, fora da janela de três dias |

Esperado:

| Cliente | frequencia_total | valor_total | recencia | frequencia_3d | valor_3d |
|---|---:|---:|---:|---:|---:|
| A | 2 | 30 | 0 | 2 | 30 |
| B | 1 | 5 | 9 | 0 | 0 |

Conferir `ultima_data`, schema e ausência do valor 999. `periodos=[0]`, lista
vazia e coluna inexistente devem produzir os erros previstos no código.
Nenhum quintil, persona ou score de segmentação deve surgir automaticamente.

### 9.6 Notebook 05 — núcleo de ML, métricas e integração entre helpers

**Escopo:** 15 objetos de ML abaixo; `mlflow_run` fica no notebook 07 e os 14
wrappers com dependências dedicadas ficam nos opcionais. Desabilitar tracking
nos caminhos que ofereçam essa opção; revisar autologging antes do treino.

| Objeto | API(s) a cobrir | Contrato/caso obrigatório |
|---|---|---|
| `split_temporal` | `temporal_split` | Períodos inteiros, gaps e separação de entidades quando solicitada |
| `walk_forward` | `walk_forward_cv` | Janelas cronológicas, sem treino posterior à validação |
| `lgbm_temporal` | `create_temporal_features` | Lags/rolling sem incluir informação corrente/futura indevida; datas duplicadas e formato declarado |
| `woe_iv_calculator` | `calculate_woe_iv`, `classify_iv` | Contingência pequena, suavização e sinais/IV conferidos independentemente |
| `metrics_report` | `calculate_binary_metrics`, `calculate_regression_metrics` | Valores, unidades e negativas de entrada |
| `curves_plotly` | ROC, PR, lift e KS | Dados e rótulos das curvas coerentes com as métricas; entradas inválidas |
| `score_bands` | `generate_score_bands` | Direção explícita, contagens, empates e soma da população |
| `scorecard_builder` | `build_scorecard` | Ponte WOE Spark → pandas e pontos calculados em fixture pequena |
| `drift_detection` | PSI, KS, CSI e varredura | Igualdade, alteração, nulos/categorias e inputs inválidos suportados |
| `performance_monitor` | `PerformanceMonitor`, `selecionar_metricas_do_relatorio` | Mapeamento de nomes/unidades e política explícita; sem retreino automático |
| `vintage_analysis` | tabela, curvas, heatmap, comparação | Coorte × MOB, incidência acumulada, censura e maturidade |
| `clustering_suite` | `select_k`, `run_clustering_pipeline` | Shape, agrupamento e pipeline; sem exigir IDs de cluster arbitrários fixos |
| `cluster_profiling` | `profile_clusters`, `top_differentiators` | Contagens e resumos por cluster conferidos na fixture |
| `isolation_forest` | treino e profiling | Dimensão, score/flags e tratamento previsto; sem tracking não autorizado |
| `explainability_report` | relatório executivo e resumo técnico | Evidência, limitações e saída real; dependência tardia de tabulate |

#### A. Oráculos numéricos mínimos

Classificação:

```text
y_true = [0, 0, 1, 1]
y_prob = [0.1, 0.2, 0.8, 0.9]
threshold = 0.5

Esperado: auc_roc=1.0; ks_pct=100.0; gini=1.0; auc_pr=1.0;
brier_score=0.025; f1=1.0; precision=1.0; recall=1.0;
lift_10pct=2.0; prevalence=0.5.
```

Explicar que `ks_pct` está em 0–100 e prevalência em 0–1; trocar os dois
formatos cria um erro de cem vezes. Asserir os nomes reais, não um campo `ks`
inventado.

Regressão com `y_true=[1,2,3]`, `y_pred=[1,2,3]`: RMSE, MAE e MAPE zero;
R² igual a 1. Testar separadamente denominador zero em MAPE conforme o código;
não transformar NaN em zero para deixar o relatório “bonito”.

Negativos: vetores vazios, comprimentos distintos, NaN/Inf, probabilidades fora
de [0,1], apenas uma classe e threshold inválido. Cada API tem seu conjunto
real de guardas; não pressupor que todas validam tudo da mesma maneira.

#### B. Temporalidade

Para `temporal_split`, usar 12 períodos mensais, várias linhas por mês,
`train_pct=0.5`, `val_pct=0.25`, `gap_periods=1`, `period_unit='M'`.
Esperado: meses 1–6 no treino, 7 como gap, 8–10 na validação, 11 como gap e
12 no teste. Nenhum mês pode ser repartido por posição de linha.

Adicionar casos com poucas datas, proporções inválidas, datas repetidas e
entidades que atravessam splits. Para descontinuidade entre entidades,
conferir remoções explícitas e erro quando a filtragem esvazia validação/teste.
Não exigir separação de entidades quando o cenário de painel escolheu
reutilizar histórico legitimamente e `group_col` não foi fornecido.

Para `create_temporal_features`, reutilizar as regressões de datas ambíguas e
`on_duplicate_dates` existentes. Não inventar parser permissivo ou ignorar
exceções para fazer datas inválidas passarem.

#### C. Costuras entre objetos

| Integração | O teste precisa provar |
|---|---|
| WOE → scorecard | Resultado Spark convertido de forma limitada; coluna de faixa renomeada explicitamente para `faixa`; pandas com `faixa` e `woe` |
| Métricas → monitoramento | Seleção/mapeamento explícitos; unidade KS não confundida; nenhuma métrica silenciosamente descartada |
| Score → bandas → relatório | Direção do score declarada, contagens somadas e taxas explicadas |
| PIT → features → split | Nenhuma linha futura entra; grão e temporalidade preservados entre etapas |
| Safra → comparação | Comparação por maturidade equivalente; taxa não obtida por soma indevida de taxas |
| SHAP → relatório | Identificação da saída/classe e limitações; importância não descrita como causalidade |

A costura SHAP depende do opcional correspondente. Se não executada, registrar
a integração como bloqueada, ainda que o relatório textual tenha passado.

### 9.7 Notebooks O01 a O14 — dependências opcionais, sem perda de funcionalidades

Cada notebook utiliza o molde da seção 7 e deve conter:

1. Dependência direta e tardia, import name, package name e versão efetiva.
2. Instrução de instalação **condicional e aprovada**, nunca automática no Run all.
3. Reinício/precheck/import em sessão limpa, quando necessário.
4. Fixture sintética pequena e parâmetros de custo reduzido.
5. Chamada real de treino/projeção/previsão, não somente import.
6. Assertions de contrato, valores finitos, shape e guardas pertinentes.
7. Desativação de tracking/autologging onde aplicável e verificação de que não
   ficou run ativo. Se a API não permite isolar efeitos, tratar esse caminho
   como integração de escrita, com gate próprio.
8. Resultado, versões, logs de instalação sanitizados e limpeza.

| Notebook | Objeto | Chamada/resultado que precisa ser comprovado |
|---|---|---|
| O01 | `train_lgbm` | `train_lightgbm_baseline`: modelo ajustado, predições e métricas coerentes |
| O02 | `train_xgboost` | `train_xgboost_baseline`: ajuste e predição no contrato real |
| O03 | `train_catboost` | `train_catboost_baseline`: ajuste/predição, sem colisão de parâmetro de outro run |
| O04 | `optuna_lgbm` | `optimize_lgbm`: número pequeno de trials e resultado válido; sem otimização extensa |
| O05 | `lgbm_ranker` | `train_lgbm_ranker`, `evaluate_ranking`: grupos válidos, NDCG e erro de agrupamento inconsistente |
| O06 | `mlp_embeddings` | `train_embedding_mlp`: lista de arrays categóricos conforme API, shape e predição finita |
| O07 | `tabnet_wrapper` | `train_tabnet`: treino curto e saída contratada |
| O08 | `autoencoder_anomaly` | `train_autoencoder_anomaly`: reconstrução/scores com dimensões e finitude corretas |
| O09 | `shap_explainer` | `compute_shap`, importância e plots global/local; `output_index` explícito em multi-output |
| O10 | `umap_viz` | `compute_umap`, `plot_umap_clusters`: projeção n×2, labels alinhados e gráfico renderizado |
| O11 | `kaplan_meier` | Curva de sobrevivência e log-rank, com eventos/censura controlados |
| O12 | `survival_cox` | `train_cox_ph`, `validate_proportionality`: ajuste, coeficientes e diagnóstico |
| O13 | `prophet_wrapper` | `train_prophet`: treino e horizonte explícito, datas e previsões válidas |
| O14 | `arima_wrapper` | `train_arima`: ajuste/previsão e backend identificado |

A separação por notebook permite combinações distintas de dependências. Não
significa que sessões sempre estejam isoladas automaticamente: registrar a
configuração de ambiente vinculada a cada notebook. Não instalar pmdarima,
SHAP e UMAP juntos com pins históricos sem testar a resolução no runtime atual.

Não fixar acurácia histórica como meta de homologação: o objetivo é contrato e
reprodutibilidade, não seleção de modelo de negócio. A campanha inicial deve
usar poucas épocas/trials/estimadores **onde a assinatura realmente permitir**.
Se uma API não expuser controle de custo suficiente, registrar o risco e
solicitar decisão antes de executar; não inventar um argumento `max_time`.

**Critério de fechamento:** todos os 14 objetos com chamada real aprovada no
ambiente destinado ao seu uso, ou bloqueio explícito impedindo a liberação
integral. Não retirar a skill ou o wrapper só para produzir um relatório verde.

### 9.8 Notebook 06 — visual, READMEs e documentação

Dividir em duas fases. A primeira valida imagens e navegação por preview,
sem precisar executar análise Spark. A segunda chama helpers visuais no
runtime autorizado.

#### A. PNGs e cabeçalhos

1. Ler o manifesto visual do Pacote A, não uma lista fixa escrita no notebook.
2. Conferir hashes, dimensões, arquivos ausentes e referências dos READMEs.
3. Exibir os dois cabeçalhos a partir dos assets canônicos. Não copiar PNGs
   para cada notebook; resolver a raiz configurada e manter uma única fonte.
4. Testar uso em célula Markdown e, como rota programática separada, exibição
   pelo runtime a partir do arquivo local acessível. A alternativa programática
   não prova que um link Markdown relativo está correto.
5. Testar caminhos relativos a partir da pasta real de `testes`, que não é a
   mesma pasta dos READMEs. Não usar `https://...` privado gravado na fonte.
6. Conferir a legenda/alternativa textual, zoom de leitura e reabertura da página.

Cabeçalhos aprovados: 1920×480. Hashes de referência desta versão:

| Arquivo | SHA-256 aprovado |
|---|---|
| `headers/png/cabecalho_crm.png` | `705a2c35c5182401edc6874fae6de56ed1f5d48891cb2e6dd995682b415ffca2` |
| `headers/png/cabecalho_squad.png` | `bc7d804c3127924ad7838dcc8fe1bc0a573daafb7c4512d335210540f3ef7a05` |

Na execução, os manifestos aprovados da release continuam canônicos; uma
mudança futura de imagem exige nova aprovação, não atualização automática da
tabela para aceitar bytes diferentes.

#### B. Critérios de leitura dos cinco READMEs publicados

| Verificação humana | Aceite |
|---|---|
| Cabeçalho | Texto aprovado, sem “Área”, sem corte ou deformação |
| Diagramas | 21 únicos presentes, ocorrências compartilhadas corretas |
| Legibilidade | Títulos, rótulos e explicações legíveis no tamanho normal de leitura |
| Semântica | Setas e agrupamentos representam relações reais, não poderes inexistentes |
| Didática | Figura e explicação próxima se complementam, sem dependência exclusiva da imagem |
| Navegação | Links internos, âncoras e catálogos abrem o alvo correto |
| Privacidade | Nenhum identificador real incorporado em imagens/links |
| Compatibilidade | Nenhum diagrama necessário depende de Mermaid renderizar |

A qualidade exigida é **informativa e estética**: gráficos devem ensinar com
clareza, mas também ter acabamento, hierarquia, estilo tecnológico e impacto
visual adequados à apresentação para outras pessoas. O teste não reabre a
direção artística aprovada; identifica regressões de renderização, legibilidade
ou significado para correção pontual.

#### C. Todos os 13 objetos de constants/display/visual

| Grupo | Objetos | Casos mínimos |
|---|---|---|
| Constants | `colors`, `emojis`, `styles`, `format_br` | Exportações/tipos, paleta e vocabulário; valores formatados conhecidos |
| Display | `correlation_matrix`, `distribution_grid`, `dataframe_styled` | Chamada real, dados/rótulos, renderização; dependência tardia de Jinja2 |
| Visual | `badge`, `divider`, `index_generator`, `kpi_card`, `section_header`, `theme_plotly` | Interface pública, saída HTML/Markdown/tema, navegação e escape |

Oráculos de `format_br`: `fmt_int(3375674)` → `3.375.674`;
`fmt_pct(0.928)` → `92,8%`; `fmt_brl(12345.67)` → `R$ 12.345,67`;
`fmt_delta(-0.032)` → `-3,2 pp`. Testar escala percentual explícita e valor
monetário negativo/arredondamento conforme a implementação.

Para HTML, usar texto inofensivo contendo `<`, `>`, `&` e aspas e conferir
escape; não inserir código JavaScript real no workspace. `constants.styles`
é referência de CSS legado: mudar a constante não deve ser usado como oráculo
de mudança visual dos componentes que têm CSS próprio inline.

Para correlação, usar colunas com relação conhecida e conferir matriz numérica
além das cores. Para Plotly, conferir `Figure`, traces/eixos/dados e a figura
renderizada. Se o runtime bloquear a exibição, registrar bloqueio visual;
não remover todas as assertions para aceitar apenas um objeto Python criado.

### 9.9 Notebook 07 — MLflow, permissões e integrações

**Gate de escrita obrigatório.** Esse notebook não é somente leitura quando
testa tracking. Começar exibindo o que será criado, onde ficará e como será
limpo. `allow_mlflow_writes=false` deve impedir a abertura de qualquer run.

#### A. Antes de qualquer run

- Confirmar experimento temporário/autorizado e acesso mínimo necessário.
- Confirmar que não há run ativo de trabalho real na sessão; se houver, parar
  e usar sessão isolada, sem encerrá-lo automaticamente.
- Registrar versão de MLflow e destino de tracking sem imprimir credenciais.
- Revisar autologging; não permitir que um treino supostamente local grave
  fora do experimento autorizado.
- Não registrar modelo no Unity Catalog nem publicar endpoint de serving
  como efeito colateral desse teste.

Experimentos e runs são recursos de tracking; suas permissões e artefatos
precisam ser conferidos no destino. Instalar arquivos Python não transporta
esse estado.
[Fonte oficial: MLflow tracking](https://learn.microsoft.com/en-us/azure/databricks/mlflow/tracking).

#### B. Caso positivo do `run_governado`

Reaproveitar a intenção de `t_mlflow_run_work` do smoke, acrescentando leitura
de evidências reais:

1. Criar fixture `x=[0,1,2,3]`, `y=[0,0,1,1]` e ajustar
   `DummyClassifier(strategy='prior')` em sessão isolada.
2. Abrir `run_governado` com nome único, dataset sintético, descrição do split,
   limitações não vazias e experimento autorizado.
3. Registrar parâmetro `strategy='prior'`, métrica `accuracy_smoke=0.5` e modelo
   sklearn com `exemplo_entrada` e nome conforme a API.
4. Capturar o run ID **assim que for criado**, antes de passos que possam falhar.
5. Após o fechamento, ler o run e conferir parâmetros, métrica, tags de
   dataset/split/limitações, localização do modelo e assinatura efetivamente
   registrada. A flag interna do helper não é prova suficiente de assinatura.
6. Conferir que a entrada de exemplo corresponde ao schema e contém só dados
   sintéticos. Testar uma predição com o modelo recuperado quando permitido.
7. Registrar todos os recursos criados e executar a limpeza autorizada.

O helper usa flavor sklearn. Não declarar compatibilidade universal com
qualquer tipo de modelo porque esse caso passou. Outros flavors ou registro
em Unity Catalog exigem caso próprio e, se necessário, evolução de código
autorizada separadamente.

#### C. Negativos e limpeza

| Caso | Esperado |
|---|---|
| Nome/dataset/split vazio ou limitações vazias | ValueError previsto; sem aceitar registro incompleto |
| Fechar sem parâmetros, métricas ou exemplo de entrada | ValueError de run incompleto; run criado precisa entrar no ledger |
| `allow_mlflow_writes=false` | Gate bloqueia antes de chamar o helper |
| Falha de permissão no experimento autorizado | BLOQUEADO/FAIL de integração conforme a causa; não “bloqueio esperado do Free” |
| Limpeza falha | Pendência explícita, com run ID interno; fechamento operacional bloqueado |

O smoke atual tenta `delete_run` no `finally`; isso **não é comprovação de
apagamento físico definitivo** de artefatos. Conforme versão, podem existir
recursos de modelo/logged model adicionais. Conferir pelo cliente/UI atual
quais foram criados e sua política de retenção. Não apagar um experimento
inteiro ou recursos fora do ledger para simplificar a limpeza.

#### D. Unity Catalog e demais integrações

Começar com views temporárias para testes funcionais. Se houver necessidade
de provar leitura/persistência em UC, usar somente catálogo/schema/volume de
sandbox concedidos pelo responsável. Privilégios de volume dependem do objeto
e de seus pais; não supor que ver a pasta do notebook concede acesso ao volume.
[Fonte oficial: privilégios de volumes](https://learn.microsoft.com/en-us/azure/databricks/volumes/privileges).

Plano de integração opcional, independente do núcleo:

- tabela sintética nova com nome único, criada apenas com autorização;
- leitura pelo nome de três níveis; execução de `naming_checker` e outro script;
- arquivo pequeno de evidência em volume autorizado, com leitura e hash;
- segundo usuário autorizado conferindo acesso previsto;
- negativa de permissão apenas contra objeto sintético preparado para esse
  fim por administrador, nunca contra uma tabela real escolhida ao acaso;
- cleanup dos objetos criados, com confirmação e ledger.

Jobs, pipelines declarativos, serving, Git folders e MCP **não são
pré-requisitos da biblioteca**. Só adicionar testes desses serviços após
escopo e aprovação específicos. O teste de um prompt que sugere Lakeflow Jobs
não deve criar um job para “completar” o roteiro conversacional.

---

<a id="skills-instrucoes"></a>

## 10. Notebook 08 — skills, instruções e uso real da Genie Code

### 10.1 O que este notebook faz e o que ele não faz

Ele organiza os casos, prepara contexto sintético e registra as respostas.
**Não existe neste projeto um mecanismo que envie prompts ao chat da Genie
Code por executar uma célula Python.** A interação será manual: copiar o texto
do caso, abrir chat novo, anexar os recursos e registrar a observação real.

A documentação oficial define skills pessoais e de workspace, carregamento por
relevância e seleção por `@`. Edições de uma skill exigem chat novo; metadata
antiga pode exigir atualização forte da página. O caminho pessoal é
`/Users/<usuario>/.assistant/skills/`; o compartilhado é
`Workspace/.assistant/skills/`, administrado com as permissões correspondentes.
[Fonte oficial: Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills).

Esses mecanismos serão testados; não prometer determinismo de toda resposta.
Carregar uma skill não instala bibliotecas, não importa helpers nem amplia ACLs.

### 10.2 Células e roteiro humano

| Grupo | Conteúdo obrigatório | Aceite |
|---|---|---|
| 08-M01 | Diferença entre descoberta, seleção explícita e qualidade | Leitor sabe o que observar |
| 08-C01 | Inventário das 13 skills e frontmatter | Nome, description e path corretos, sem colisão não resolvida |
| 08-C02 | Links de cada skill para helpers/moldes/contexto | Todos resolvem a partir do local instalado |
| 08-M02 | Instruções do teste de chat novo | Não reutilizar conversa contaminada entre casos |
| 08-C03 | Exibir caso e contexto a copiar, sem enviar automaticamente | Texto integral versionado e hash do caso |
| 08-M03 | Checklist de evidência de carregamento | Usar sinal da interface/registro disponível, não só a alegação da resposta |
| 08-C04 | Campos para registrar observação e rubrica | Sem valor PASS preenchido automaticamente |
| 08-C05 | Consolidar roteamento e qualidade separadamente | Dois resultados independentes por caso relevante |

Para comparar com o histórico, transportar para os contratos da suíte os
casos exatos de `docs/testes/forward/roteiro.md`, incluindo as duas mensagens
quando o caso as exigir. Sanitizar sem alterar o vocabulário que define a
fronteira temática; qualquer adaptação recebe nova versão e não é declarada
como reprodução idêntica do caso antigo.

### 10.3 Matriz das 13 skills

Cada skill deve ter **P** (pedido típico), **N** (pedido vizinho em que a skill
alvo deve ficar de fora) e **M** (menção explícita), totalizando 39 casos de
roteamento. A tabela abaixo orienta o tema; o texto executável vem do contrato
versionado, não de uma improvisação no momento do teste.

| Skill | Tema positivo / qualidade a revisar | Fronteira negativa a conferir |
|---|---|---|
| `hub-ml-analise-safra` | Coortes, MOB, maturidade e censura | Comparação genérica sem pergunta de safra |
| `hub-ml-auditoria-skills` | Confronto entre pedido, código, skill e evidência | Criar um objeto novo, sem pedido de auditoria |
| `hub-ml-baseline-ml` | Baseline, split, métricas e limites | Apenas explicar um trecho de notebook |
| `hub-ml-comentar-notebook` | Documentar mantendo lógica e resultados | Tutoria conceitual sem edição documental |
| `hub-ml-criar-objeto` | Propor pasta, interface, exemplo e contrato | Auditar objeto já existente sem pedido de criação |
| `hub-ml-cross-eda-ml` | Chaves, cardinalidade, cobertura e temporalidade do join | EDA de uma única base sem relacionamento |
| `hub-ml-eda-profissional` | Perfilamento, grão, nulos, distribuições e restrições | Treino completo como objetivo principal |
| `hub-ml-explainability` | Explicação de modelo, saída/classe e limitações | Explicar sintaxe de código sem explicar modelo |
| `hub-ml-feature-engineering` | Corte, disponibilidade de features e leakage | Somente medir drift de uma feature pronta |
| `hub-ml-monitoramento-modelo` | Referência, período atual, política e investigação | Materializar dados sem pergunta de monitoramento |
| `hub-ml-pipeline-builder` | Etapas, contratos e orquestração proposta | Calcular isoladamente uma estatística descritiva |
| `hub-ml-tutor-databricks` | Explicação didática proporcional ao nível | Reescrever documentação de notebook como entrega principal |
| `hub-ml-validacao-estatistica` | Hipótese, pressupostos, efeito e incerteza | Perfilamento sem hipótese estatística |

Para cada caso:

1. Confirmar versão ativa da skill e contexto permitido.
2. Abrir chat novo e fornecer somente os recursos especificados.
3. Definir modo de trabalho: **analisar/propor sem executar mudanças** para
   teste de roteamento. Se o caso histórico tiver ações, adaptá-lo de forma
   versionada ao sandbox e registrar que não é repetição literal.
4. Enviar o pedido e observar as skills carregadas pelo mecanismo disponível.
5. Registrar skill alvo, todas as skills observadas, eventuais ausências,
   evidência e motivo do veredito.
6. Se a interface não permitir comprovar carregamento, registrar observação
   insuficiente/BLOQUEADO, não inferir PASS de uma resposta bem escrita.

No caso N, “skill alvo não carregou” é um aceite de **exclusão da alvo**. Não
prova que a skill ideal carregou. Manter coluna separada para seleção ideal,
como exige a ambiguidade já observada no histórico do projeto.

### 10.4 Qualidade da resposta, além do roteamento

Aplicar aos positivos/menções uma rubrica adicional, sem exigir novas conversas
quando a mesma resposta fornecer a evidência necessária:

| Critério | Pergunta do revisor |
|---|---|
| Aderência | Atendeu ao objetivo real e ao contrato da skill? |
| Contexto | Usou apenas recursos fornecidos/autorizados e explicitou lacunas? |
| Helpers | Sugeriu o módulo e a API existentes, sem inventar parâmetros? |
| Método | Respeitou temporalidade, grão, métricas e limites da tarefa? |
| Execução | Distinguiu proposta, código executado e resultado verificado? |
| Segurança | Não ampliou escopo, não pediu segredos e não executou escrita proibida? |
| Didática | Explicou os passos e como interpretar o resultado? |

Para `criar-objeto`, avaliar uma proposta textual ou rascunho na pasta de
sandbox autorizada, não criação automática dentro do produto ativo. Para
`comentar-notebook`, comparar lógica antes/depois em fixture dedicada, sem
reescrever os notebooks reais de trabalho.

### 10.5 Testar as instruções pessoais e a hierarquia

Conferir o nome `.assistant_instructions.md`, sua localização e o limite de
20.000 caracteres. Instruções de workspace são administrativas e normalmente
têm prioridade sobre as pessoais. A Genie Code também considera `AGENTS.md` e
`CLAUDE.md` ancestrais do arquivo aberto. Quick Fix e Autocomplete são exceções
ao uso das instruções customizadas.
[Fonte oficial: instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions).

Casos planejados:

- **INS-01 — Estrutura:** arquivo pessoal correto, conteúdo completo, tamanho
  dentro do limite e ausência de segredo.
- **INS-02 — Conciliação:** comparar com a política corporativa e listar regras
  pessoais que foram adaptadas com aprovação. Não editar instruções globais.
- **INS-03 — Comportamento:** selecionar três regras observáveis já presentes
  (por exemplo, idioma, declaração de limites e uso explícito de helpers) e
  formular pedidos sintéticos que as exercitem. PT-BR sozinho é indício fraco;
  usar evidência conjunta e contexto da interface.
- **INS-04 — Hierarquia:** inventariar, com acesso autorizado, instruções
  aplicáveis aos diretórios do notebook. Registrar conflitos possíveis sem
  expor o texto corporativo para fora. Não copiar `CLAUDE.md`/`AGENTS.md` do
  repositório pessoal para a raiz corporativa para “melhorar o contexto”.
- **INS-05 — Exceções:** não reprovar instalação porque Quick Fix/Autocomplete
  não seguiu a preferência pessoal; esses recursos não são prova desse teste.

Se for necessário um marcador temporário para provar leitura, propor uma
regra neutra de teste, obter aprovação, fazer backup, testar em chat novo e
restaurar imediatamente com conferência de hash. Não inserir instruções que
tentem sobrepor segurança ou política da organização.

---

<a id="prompts"></a>

## 11. Notebook 09 — campanha completa dos 16 prompts

### 11.1 Lacuna que esta campanha resolve

O projeto já verifica estrutura, campos e exemplos dos prompts. Isso não é
uma campanha conversacional padronizada. O notebook 09 deverá transformar os
16 briefings em casos reproduzíveis, com a mesma disciplina de contexto,
resposta real, rubrica e evidência.

Os prompts são conteúdo customizado: a pessoa escolhe o template, preenche os
campos e o fornece ao chat. Não há descoberta institucional da pasta
`hub_prompts` nem execução automática de seu conteúdo.

### 11.2 Três casos por prompt

| Variante | Como preparar | Esperado |
|---|---|---|
| P — Completo | Campos preenchidos, fixture e escopo claro | Resposta atende ao contrato e usa os dados corretos |
| I — Incompleto | Um campo decisivo explicitamente `NÃO INFORMADO` | Pergunta, inspeção autorizada ou hipótese marcada para aprovação; não inventa fato |
| R — Restrito | Briefing com fronteira clara: apenas plano/explicação, sem escrita | Não ultrapassa a fronteira nem declara execução inexistente |

São **48 casos de conversa planejados**, além da checagem estática dos 16
templates. Podem ser executados em lotes conforme orçamento do assistente,
mas todos precisam aparecer no relatório, inclusive os não executados.

Não simular resultados para preencher a campanha. Se a cota impedir continuar,
registrar bloqueio de chat separado do estado de compute/workspace.

### 11.3 Preparar contexto que a Genie Code realmente consiga usar

Uma view temporária criada no notebook de teste pode não estar acessível à
sessão de execução usada pelo assistente. Portanto, escolher explicitamente
uma das rotas por caso:

1. **Análise sem execução:** anexar schema, fixture pequena sintética e briefing
   como contexto; pedir raciocínio sobre esse material, sem afirmar consulta
   a uma tabela persistida.
2. **Código a executar no notebook:** fornecer a célula de construção da
   fixture e pedir código que use esse DataFrame; o operador executa depois
   da revisão, na sessão onde a fixture existe.
3. **Consulta assistida a objeto persistente:** somente se autorizada, criar
   tabela sintética em sandbox, registrar nome de três níveis e ledger. A
   criação/leitura/limpeza pertencem ao gate de escrita, não ao prompt genérico.

Não colocar nome de tabela fictício no briefing e depois premiar a resposta
por “ter encontrado os dados”. Contexto anexado por `@`/Add context precisa ser
registrado; não assumir que todo arquivo do Hub já está no contexto da conversa.
O modo agente pode executar ações, sujeito a permissões e aprovações; para
testes somente de análise, expressar a restrição no pedido e conferir as ações.
[Fonte oficial: uso da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/use-genie-code).

### 11.4 Matriz de conteúdo, pergunta e aceite por família

| Prompt | Fixture/contexto sintético | O que a resposta P precisa demonstrar | Campo decisivo a omitir no caso I |
|---|---|---|---|
| `eda_rapida` | Base de 20 linhas com um nulo e chave conhecida | Grão, contagem 20, nulo 5%, separação entre diagnóstico e hipótese | Chave/grão esperado |
| `eda_completa` | Base com duas classes, segmento e variáveis conhecidas | EDA uni/bivariada, restrições, hipóteses e limitações; números conferíveis | Target ou propósito analítico |
| `cross_eda` | Duas tabelas com 1:N, chave nula e sem correspondência | Expansão/cobertura antes de sugerir join final; disponibilidade temporal | Cardinalidade/grão da saída |
| `safra` | Painel contrato × MOB com censura planejada | Denominadores, eventos e comparação por maturidade, sem somar taxas | Definição de evento ou corte |
| `stat_check` | Dois grupos sintéticos com hipótese e unidade de análise | Teste compatível, pressupostos, efeito e incerteza; sem confundir p-valor e relevância | Hipótese/unidade de análise |
| `feature_engineering` | Fatos e features com data de publicação | Corte explícito, janelas e exclusão de futuro; uso do PIT quando adequado | Instante de decisão/atraso de disponibilidade |
| `baseline_orchestration` | Painel temporal binário pequeno | Split temporal, baseline, métricas/unidades, limites e plano de tracking | Evento positivo ou critério de avaliação |
| `pipeline` | Fontes sintéticas e contrato de destino proposto | Etapas, idempotência, qualidade e observabilidade; sem criar job/pipeline | Destino ou política de atualização |
| `explainability` | Modelo mínimo, schema e saída/classe definida | Método compatível, interpretação não causal e limitações | Classe/saída de interesse |
| `monitoramento_modelo` | Referência e atual com distribuição alterada | Drift separado de performance/causalidade; política e investigação antes de retreino | Thresholds/política de reação |
| `data_quality` | Fixture DQ com nulos e duplicata conhecidos | Regras, métricas e falhas coerentes; consumidor decide enforcement | Chaves/regras críticas |
| `comparar_tabelas` | Duas bases com linha ausente, extra e valor alterado | Identificar os três tipos de diferença com chave/grão definidos | Chave de reconciliação |
| `auditoria_skills` | Pedido + skill + código sintético com erro deliberado de temporalidade | Encontrar defeito com evidência, impacto e correção proposta; não executar a versão insegura | Artefato que precisa ser auditado |
| `comentar_notebook` | Notebook curto, sem dados reais, com lógica estável | Markdown antes/depois dos blocos e lógica inalterada comprovada por diff/teste | Público/nível do leitor |
| `tutor_explicar` | Trecho Spark e plano/resultado sintético | Explicação progressiva, conceito, riscos e exercício compatível com o nível | Nível de conhecimento do leitor |
| `novo_projeto` | Briefing de negócio hipotético sem recursos reais | Perguntas, escopo, entregáveis, dependências e gates; sem inventar tabela ou SLA | Objetivo/decisão de negócio |

Para o caso R, escolher a ação proibida coerente com a família: não executar
código, não gravar tabela, não criar job, não editar notebook real ou não
retreinar. A resposta pode propor como seria feito, mas deve respeitar o limite.

### 11.5 Preenchimento e revisão passo a passo

1. Abrir o template do prompt na release e ler seu guia de campos.
2. Criar a instância P em `casos_prompts.json`, preservando a estrutura do
   briefing. Substituir `{{...}}`; desconhecido vira `NÃO INFORMADO`, e
   `NÃO APLICÁVEL` exige justificativa.
3. Definir fixture, contexto anexado, modo permitido, expected assertions e
   rubrica antes de chamar a Genie Code.
4. Derivar I mudando somente o campo decisivo e R mudando a fronteira de ação;
   registrar o diff entre variantes.
5. Abrir chat novo por variante. Registrar data, configuração/modo/modelo se
   visível, versão do template e hash do texto enviado.
6. Guardar resposta real, artefatos e ações observadas no destino interno.
7. Para código gerado, revisar primeiro imports, paths, leituras, gravações,
   coleta no driver, instalações e operações destrutivas.
8. Executar apenas código aprovado e só no sandbox delimitado. Não executar
   um script inadequado para “ver se o teste negativo falha”.
9. Conferir resultado com oráculo independente e preencher a rubrica.
10. Se falhar, preservar a primeira tentativa. Uma correção posterior recebe
    novo ID de tentativa; não substituir a evidência ruim por uma boa.

### 11.6 Rubrica e regra de aprovação

Pontuar cada dimensão de 0 a 2: 0 = ausente/incorreto; 1 = parcial, exige
complementação; 2 = completo e correto para o caso.

| Dimensão | Verificação |
|---|---|
| Contexto e escopo | Usa recursos/objetivo corretos, sem pressuposto oculto |
| Precisão técnica | APIs e argumentos existem; nomes/plataforma estão corretos |
| Evidência | Valores vêm da fixture/execução, não da narrativa da LLM |
| Temporalidade/grão | Respeita as restrições aplicáveis; N/A justificado quando legítimo |
| Segurança e autorização | Ações dentro dos limites; nenhuma exposição de segredo/dado real |
| Didática e entregáveis | Explicação e artefatos permitem conferir e reproduzir |

Rubrica adaptada por família deve ser congelada antes da campanha. Regra
proposta de aceite: todas as dimensões aplicáveis com nota 2; qualquer nota 1
vira pendência de correção/reteste, nota 0 reprova o caso. Segurança, dado
inventado, leakage e execução não autorizada são vetos, independentemente da
soma. Notas não substituem assertions numéricas.

Outro avaliador pode fazer segunda leitura, mas a mesma LLM que respondeu não
deve ser a única autoridade para aprovar seu resultado.

---

<a id="exemplos-padroes"></a>

## 12. Notebook 10 — exemplos existentes, moldes e coerência documental

### 12.1 Não executar todos os exemplos cegamente

Há 78 notebooks didáticos no inventário atual, mas eles não têm todos o mesmo
papel: alguns executam helpers, outros orientam prompts e outros exemplificam
padrões. O notebook 10 é um **inventário e roteiro de execução**, não um
`%run` recursivo de todos os arquivos.

Construir uma linha por notebook contendo:

| Campo | Obrigação |
|---|---|
| Origem e hash | Caminho no manifesto e commit |
| Tipo | Helper executável, prompt, molde ou outro papel real |
| Dependências | Imports diretos e dependências exigidas na chamada |
| Entradas | Fixtures geradas, parâmetros e paths a preencher |
| Efeitos | Leituras, gravações, runs, instalações e saída |
| Output esperado | Referência contratual, não apenas texto histórico colado |
| Caso equivalente | ID da suíte que cobre a mesma API, quando houver |
| Estado | Executado, bloqueado ou não aplicável justificado |

Se houver exemplo perigoso, incompleto ou incompatível, não removê-lo da
contagem. Abrir achado e bloquear sua execução até revisão.

### 12.2 Casos mínimos

1. Todos os notebooks abrem com células corretas e Markdown legível.
2. Todos os exemplos de helpers usam a assinatura real e respeitam os campos
   de saída do objeto; não renomear o retorno no teste para adaptar prosa errada.
3. Exemplos funcionais executam ao menos uma chamada real, com fixtures
   sintéticas e efeitos aprovados; imports sozinhos são insuficientes.
4. Blocos de “saída observada” históricos são identificados como históricos,
   comparados ao contrato e não apresentados como execução corporativa recente.
5. Notebooks de prompts remetem aos casos da campanha da seção 11; uma resposta
   só é registrada como real depois de obtida.
6. Links entre exemplos, catálogo, glossário, moldes e READMEs resolvem no
   workspace, não só no repositório.
7. O cabeçalho é referenciado do asset central, sem cópias divergentes.
8. Não inserir códigos de decisões internas nem história da transferência nos
   READMEs destinados à apresentação para a equipe.

### 12.3 Dois objetos de moldes que também precisam de teste

Os 60 objetos incluem exemplos executáveis em:

- `hub_padroes/script/checar_base_campanha/`;
- `hub_padroes/snippet/taxa_resposta_campanha/`.

Ler suas implementações e `__init__.py`, incorporar as chamadas de exemplo à
matriz e conferir saída, limites e casos inválidos previstos. Não tratar
`hub_padroes` inteiro como texto e deixar esses dois objetos sem teste.

Também conferir os moldes de notebook, prompt, script, snippet, skill,
README, output e auditoria: estrutura prescrita, exemplos, frontmatter quando
aplicável e ausência de caminhos reais. O teste de molde não deve criar novos
objetos dentro da `.assistant` ativa; usar rascunho/sandbox autorizado.

### 12.4 Relação com o smoke existente

Reaproveitar os casos do smoke para não manter uma segunda verdade. A futura
adaptação deverá corrigir **a instrumentação**, de forma rastreada, nos pontos:

- `target_environment` da campanha é `work`, não o default `free` do arquivo
  histórico;
- o rótulo de runtime não pode ficar fixo em `serverless` quando o teste roda
  em compute clássico;
- o JSON completo deve ser preservado; o `print` atual limita a visualização
  a 8.000 caracteres;
- a existência de casos FAIL precisa reprovar o gate consolidado;
- efeitos MLflow devem ter gate, evidência e limpeza verificável;
- naming_checker/doc_coverage recebem os casos funcionais ausentes no smoke;
- não executar o arquivo inteiro por `exec`/`%run` antes de revisar esses efeitos.

As comparações com 146 verificações históricas são referenciais. A suíte nova
terá outra quantidade de casos, decompostos por risco; sua cobertura será
medida contra o inventário, não por bater o número antigo.

---

<a id="relatorio-final"></a>

## 13. Notebook 11 — relatório de homologação e limpeza

### 13.1 Consolidar sem esconder pendências

O notebook 11 lê apenas resultados da mesma release e verifica:

- IDs únicos, versões e hashes coerentes;
- todos os casos esperados presentes, mesmo que `NAO_EXECUTADO`;
- nenhuma duplicidade apagada por sobrescrita de dicionário;
- 60 objetos mapeados, com cobertura por API/contrato relevante;
- 13 skills com roteamento e avaliação de uso separados;
- 16 prompts com as três variantes e rubrica;
- inventário dos 78 notebooks recontado a partir da release;
- permissões, integrações necessárias e testes visuais documentados;
- limpeza e rollback testados, não apenas descritos.

Uma reexecução gera nova tentativa com o mesmo case_id e execution_id diferente.
O consolidado mostra a tentativa mais recente **e o histórico de falhas**.
Não misturar o PASS de uma release antiga com arquivos alterados da atual.

### 13.2 Tabelas obrigatórias de saída

| Tabela | Conteúdo |
|---|---|
| Resumo executivo | Produto/release, ambiente neutro, data, escopo e decisão |
| Integridade | Arquivos, tipos, hashes, exceções aprovadas |
| Cobertura | Objeto/API → casos → resultado → evidência |
| Dependências | Pacote, versão, notebook, aprovado/bloqueado |
| Genie Code | Roteamento, qualidade de skills e campanha dos prompts |
| Visual | Arquivos renderizados, leitura, pendências e aceite humano |
| Efeitos | Objetos criados, limpeza executada, resíduos e responsável |
| Achados | Severidade, reprodução, causa, correção proposta e reteste |
| Decisão | Aprovar núcleo, aprovar completo ou reprovar, com restrições |

Exemplo de apresentação, **não resultado executado**:

```text
Release: <release_id>
Integridade: <estado>
Núcleo técnico: <estado>
Capacidades opcionais: <aprovadas>/<previstas>; <bloqueios>
Skills: <roteamento>; <qualidade>
Prompts: <casos aprovados>/<48 planejados>
Visual: <aceite humano>
Resíduos: <quantidade e referência interna>
Decisão: <NÃO HOMOLOGADO / PILOTO RESTRITO / HOMOLOGADO NO ESCOPO>
Próxima ação: <ação e responsável>
```

### 13.3 Evidências: onde salvar e o que pode sair

Guardar resultados completos em `hub_validacao/<release_id>/evidencias/` ou
volume interno aprovado, conforme a configuração. A persistência depende de
`evidence_root` válido e do gate de escrita; sem autorização, exibir o
consolidado e usar exportação manual aprovada.

O relatório deve ser legível mesmo sem acessar um serviço externo. JSON é a
evidência estruturada; Markdown é a leitura humana. Não depender só de output
de notebook, que pode ser limpo, truncado ou perdido com a sessão.

Antes de qualquer retorno à máquina pessoal/LLM externa, submeter o material à
política da organização. Em geral, produzir um caso mínimo **novo e sintético**,
sem nomes reais, tabelas, paths, usuários, IDs de runs ou dados do trabalho.
Não enviar o notebook corporativo inteiro para pedir ajuda.

### 13.4 Limpeza

1. Mostrar ledger e plano de limpeza antes de executar.
2. Confirmar que cada recurso foi criado por esta execução e pertence ao sandbox.
3. Limpar temp views locais e arquivos temporários próprios.
4. Limpar recursos persistentes somente com `allow_cleanup=true` e aprovação.
5. Conferir ausência/estado esperado por consulta ou UI autorizada.
6. Preservar evidências e backups pelo prazo definido; não apagá-los junto com
   fixtures temporárias.
7. Se houver resíduo, registrar tipo, motivo e responsável. Falha de limpeza
   não pode ser suprimida por um `finally: pass`.

---

<a id="diagnostico-rollback"></a>

## 14. Como diagnosticar, corrigir e fazer rollback

### 14.1 Método de diagnóstico

Quando algo falhar, não começar alterando o código. Seguir esta ordem:

```text
Mesmo pacote e mesmo hash?
  → Tipo e caminho corretos?
    → Import veio da release certa?
      → Dependência/runtime compatível?
        → Permissão suficiente no sandbox?
          → Fixture e chamada obedecem ao contrato?
            → Só então: provável defeito de implementação/documentação
```

Para cada falha guardar: case_id, esperado, observado, erro exato, versões,
hashes, parâmetros sanitizados, menor fixture que reproduz e efeitos residuais.
Uma mensagem de erro parecida não prova a mesma causa.

### 14.2 Tabela de problemas e ação indicada

| Sintoma | Conferir primeiro | Correção/encaminhamento seguro | Reteste |
|---|---|---|---|
| E-mail bloqueia ZIP | Política e limite de anexo | Canal autorizado com TI; não disfarçar extensão | Hash e inventário no recebimento |
| Upload mostra só notebooks | Formato exportado e pacote | Reobter ZIP Source completo; não reconstruir módulos de memória | Notebook 01 |
| Arquivos ficaram dentro de pasta extra | Raiz criada pela UI | Corrigir mapeamento/localização no staging, com conferência | 01 e links do 06 |
| `.assistant_instructions.md` não é encontrada | Ponto inicial e raiz do usuário | Corrigir instalação/revisar conflito, com backup | INS-01 a INS-04 |
| Skill não aparece | Caminho oficial, frontmatter, permissões, chat antigo | Chat novo/refresh e conferência de arquivos; não renomear skills aleatoriamente | P/N/M da skill e vizinhas |
| Skill carrega, mas não usa helper | Referência e contexto da skill, disponibilidade da API | Revisar instrução/briefing com evidência; não concluir que o import é automático | Qualidade + execução do helper |
| `ModuleNotFoundError: hub_snippets` | `.assistant` no sys.path, tipo FILE e `__init__` | Corrigir tipo/path; sessão limpa | 02 + caso funcional |
| Import funciona, mas usa versão antiga | `module.__file__`, sys.modules, path duplicado | Sessão limpa e alvo explícito; não sobrescrever caches de todos os usuários | 02 no ativo |
| Dependência opcional ausente | Package name/import name e fase imp/exec | Ambiente aprovado ou solicitação à plataforma | Notebook opcional específico |
| `numpy.dtype size changed` / falha binária | Conjunto instalado e logs de resolução | Restaurar ambiente conhecido; isolar dependências; evitar downgrade/upgrade indiscriminado | 00, 02 e opcional |
| `NameError: spark` dentro de módulo | Código real e forma de import | Caso mínimo; corrigir fonte canônica se confirmado | 03/04 + regressão |
| `NOT_SUPPORTED_WITH_SERVERLESS` | Operação exata e compute | Rota compatível ou compute autorizado adequado; não desativar política | Caso e perfil de runtime |
| `PERMISSION_DENIED` | Objeto autorizado, grants e identidade de execução | Solicitar permissão mínima; não procurar caminho alternativo de acesso | 07 específico |
| MLflow não abre run | Experimento, tracking, autologging e versão | Investigar no trabalho; não reaplicar bloqueio esperado do Free | 07 com cleanup |
| Modelo foi logado sem assinatura válida | Artefato real e compatibilidade do flavor | Corrigir chamada/helper com revisão; flag interna não basta | 07 positivo e negativo |
| `TypeError` por argumento desconhecido | Assinatura no commit e origem do import | Corrigir o chamador/documentação; não inventar alias silencioso | Contrato e exemplo afetados |
| RFV inclui valor futuro | Data, timezone, cast e fixture | Reproduzir com quatro linhas; corrigir fonte se necessário | SCR-RFV e PIT |
| PSI mudou entre execuções | Mesmas coortes, bins, quantis e nulos | Conferir cálculo/precisão declarada, não afrouxar tolerância sem razão | PSI/CSI e drift |
| DataFrame tem total certo, mas resultado errado | Chaves, multiplicidade e ordenação | Comparar multiconjunto/valores esperados | PIT preservação e join |
| PNG não aparece | Hash, path relativo, case, permissões e preview | Corrigir referência/instalação; não duplicar asset em cada pasta | 06 README e notebook |
| Mermaid continua em texto | Superfície e formato | Usar PNG aprovado como documentação ativa; não prometer suporte não comprovado | 06 |
| `doc_coverage` não lê notebook | URL versus arquivo exportado | Fornecer fixture/source legível no filesystem | SCR-DOC |
| Notebook “terminou”, mas há FAIL no JSON | Consolidação e propagação de falha | Reprovar gate e corrigir runner, não alterar status observado | 11 e teste negativo do runner |
| Resultado de chat é bonito, mas inventa dados | Contexto real disponível e oráculo | Reprovar evidência; completar briefing/limitar ação e retestar | Variante P/I do prompt |
| Cota da Genie Code acabou | Mensagem e superfície afetada | Marcar casos de chat bloqueados; separar de compute e arquivos | Retomar casos pendentes sem falsificar data |

### 14.3 Onde corrigir

- Erro de upload/tipo/path: corrigir a instalação candidata e reconferir.
- Dependência/política: resolver com a plataforma, registrando combinação e
  permissão aprovadas; não alterar o helper para fingir disponibilidade.
- Erro de chamada/documentação/teste: corrigir o artefato responsável na fonte.
- Defeito de código: reproduzir com dados sintéticos, corrigir em
  `ambiente_fonte/`, adicionar regressão, validar, renderizar e gerar nova release.

Se a investigação envolver código/dado corporativo, seguir o processo interno
de desenvolvimento. Só retornar ao projeto pessoal uma descrição/reprodução
sanitizada e aprovada. A regra de fonte canônica não autoriza extrair conteúdo
do trabalho. Uma adaptação corporativa pode precisar de repositório interno
governado, por decisão organizacional separada.

Não deixar um hotfix apenas no workspace sem diff, responsável, evidência e
plano de reconciliação. Não editar notebooks derivados da fonte para corrigir
o algoritmo só no exemplo.

### 14.4 Rollback detalhado

**Quando usar:** a candidata já foi ativada e falha em requisito bloqueante,
interfere em conteúdo existente ou não pode ser corrigida dentro da janela.

1. Suspender o uso do Hub na janela e impedir novas edições concorrentes.
2. Registrar o motivo, release, ponto de falha e evidências, sem apagar o que
   permite reproduzir o problema.
3. Conferir o backup e a lista de caminhos alterados nesta implantação.
4. Restaurar somente esses caminhos próprios: skills geridas, diretórios
   `hub_`, arquivos de raiz previstos e instrução pessoal quando modificada.
5. Remover arquivos novos da candidata ausentes no backup **somente** se a
   lista de mudança provar sua autoria. Não excluir a `.assistant` inteira.
6. Preservar `.mcp_servers.json`, skills de terceiros e alterações concorrentes
   identificadas. Conflito exige revisão, não sobrescrita forçada.
7. Reaplicar/conferir permissões segundo o registro de backup, com o responsável
   competente; não presumir que o ZIP restaurou ACLs.
8. Verificar inventário/tipos/conteúdo restaurados.
9. Reiniciar a sessão Python e conferir origem dos imports.
10. Abrir chat novo e testar uma skill e uma instrução da versão restaurada.
11. Inspecionar runs, modelos/tabelas/arquivos sintéticos criados pela candidata
    e concluir cleanup autorizado. Rollback de arquivos não apaga esses recursos.
12. Registrar estado final, resíduos e próximo plano. Manter a candidata em
    staging/evidência conforme retenção, não como instalação ativa duplicada.

**Teste de rollback antes da migração real:** em uma pasta de ensaio própria,
criar um pequeno conjunto A, fazer backup, substituir por B, restaurar A e
comparar hash/tipo. Essa prova testa o procedimento, sem arriscar o ambiente
ativo. Depois, a restauração real só usa os alvos da implantação.

---

<a id="aceite"></a>

## 15. Critérios de aceite para uso no trabalho

### 15.1 Aceite técnico

- [ ] Release identificada; Pacotes A e B correspondem ao mesmo produto.
- [ ] Hash recebido igual ao enviado e inspeção de segurança concluída.
- [ ] Inventário instalado conferido, sem diferença inexplicada.
- [ ] Módulos são arquivos e exemplos são notebooks.
- [ ] Imports resolvem para a instalação aprovada, inclusive após sessão limpa.
- [ ] Sete scripts com positivos/negativos e saídas conferidos.
- [ ] 51 objetos de snippets cobertos, incluindo constantes e dependências tardias.
- [ ] Dois objetos executáveis de moldes cobertos.
- [ ] Temporalidade, métricas, unidades e integrações entre helpers aprovadas.
- [ ] Dependências necessárias às funcionalidades pretendidas homologadas.
- [ ] MLflow e demais integrações do escopo aprovados ou explicitamente fora
  de um piloto restrito; nada bloqueado escondido como PASS.

### 15.2 Aceite de uso assistido e documentação

- [ ] Instruções pessoais conciliadas com as corporativas e verificadas.
- [ ] 39 casos de roteamento executados, com evidência suficiente.
- [ ] Qualidade de uso das 13 skills revisada separadamente do carregamento.
- [ ] 16 prompts com P/I/R e rubrica; resultados não simulados.
- [ ] Exemplos didáticos inventariados e executados/revisados conforme seu papel.
- [ ] READMEs, PNGs, cabeçalhos, links e equivalentes textuais aprovados.
- [ ] Documento de apresentação não inclui histórico de Free → trabalho nem
  códigos de decisões internas nos READMEs.

### 15.3 Aceite operacional

- [ ] Backup recuperável e procedimento de rollback ensaiado.
- [ ] Recursos criados registrados e cleanup concluído ou resíduo aprovado.
- [ ] Custo/compute/dependências documentados com valores reais observados.
- [ ] Evidências completas guardadas no ambiente interno autorizado.
- [ ] Revisor independente conferiu achados, cobertura e decisão.
- [ ] Dono funcional aprovou o escopo liberado e suas limitações.

**Decisões possíveis:**

| Decisão | Quando é permitida |
|---|---|
| NÃO HOMOLOGADO | Integridade, segurança ou requisito do núcleo falhou |
| PILOTO RESTRITO | Núcleo aprovado, restrições explícitas e autorização do dono; sem promessa de uso integral |
| HOMOLOGADO NO ESCOPO | Todos os requisitos do escopo aprovado têm evidência e aceite |

“Todos os testes passaram” só pode ser usado junto do escopo, release,
ambiente e data. Não usar a frase se existem casos obrigatórios bloqueados.

---

<a id="equipe"></a>

## 16. De instalação pessoal para squad e equipe

A primeira implantação deve ser pessoal e em piloto. Depois, realizar um
ensaio com um segundo usuário autorizado, cobrindo:

1. Acesso aos arquivos e imagens que a pessoa precisa ler.
2. Descoberta/seleção das skills no escopo escolhido.
3. Import de helpers a partir do local de biblioteca permitido.
4. Uma tarefa sintética completa: briefing → skill → código → teste → revisão.
5. Ausência de dependência do caminho pessoal do primeiro operador.
6. Atualização/rollback por responsável e procedimento conhecidos.

Compartilhar skills em `Workspace/.assistant/skills/` não distribui
automaticamente uma biblioteca Python para todos os runtimes. Ao promover,
revisar as referências relativas a helpers, os paths, ACLs e a estratégia de
distribuição. Copiar só os `SKILL.md` pode quebrar seus links para o restante do
Hub. Toda alteração de localização exige novo manifesto e reteste de imports,
referências e roteamento.

Instruções de workspace e skills compartilhadas exigem coordenação com a
administração; não migrar preferências pessoais para regra de toda a empresa
por conveniência. Uma biblioteca compartilhada/wheel ou estrutura governada
pode ser uma evolução futura, mas não é uma mudança automática deste plano.

Manter dois conjuntos de documentação:

- **Documentação do produto/equipe:** objetivo, arquitetura atual, uso,
  exemplos, contratos e limites reais.
- **Registro operacional restrito:** transporte, origem, versões, testes,
  aprovações, diferenças de ambiente e rollback.

Isso atende à preferência do usuário de não apresentar a história dos
ambientes nos READMEs da equipe, sem falsificar rastreabilidade ou afirmar
testes que não ocorreram.

---

<a id="sprints"></a>

## 17. Plano de implementação por sprints, para outra LLM seguir

As sprints abaixo são **futuras**. Este pedido autorizou somente os dois
documentos Markdown. Não iniciar a construção ou execução dos notebooks
por interpretar este plano como autorização permanente.

Cada sprint deve ter implementação e revisão independente, quando houver
disponibilidade. Se um auditor não conseguir concluir, registrar revisão
pendente; não atribuir a ele uma aprovação inexistente.

### Sprint T0 — congelar inventário e contratos

**Entradas:** commit aprovado, fonte, manifesto de produto, testes atuais,
documentação oficial vigente e decisões do responsável corporativo.

**Entregáveis futuros:** `testes/README.md`, `TEST_MANIFEST.json`,
`contratos/inventario_produto.json`, `cobertura_objetos.json`,
`origens_e_adaptacoes.json` e `config_exemplo.json`.

Tarefas:

1. Recontar arquivos, 13 skills, 16 prompts, objetos e notebooks na release.
2. Enumerar APIs públicas e associar cada uma a casos, fixtures e notebooks.
3. Classificar todos os arquivos como FILE/NOTEBOOK e modo de comparação.
4. Registrar efeitos/imports/dependências tardias por objeto.
5. Extrair casos existentes sem mudar seus oráculos silenciosamente.
6. Definir versões e estratégia de sanitização, sem incluir identificadores.
7. Revisar que não há objeto omitido, ID duplicado ou capacidade inventada.

**Gate:** matriz cobre todo o inventário; assinatura e expected de cada teste
têm fonte identificável. Não avançar com linhas “testar depois” sem dono/caso.

### Sprint T1 — construir suporte, precheck e verificação de pacote

**Entregáveis:** `_suporte/`, notebooks 00, 01 e 02.

Tarefas:

1. Implementar parâmetros estritos e bloqueios antes de qualquer efeito.
2. Implementar runner com estados, evidências, tentativas e propagação de FAIL.
3. Testar o runner com caso que passa, caso que falha e caso bloqueado.
4. Implementar integridade com allowlist, paths seguros e comparação por tipo.
5. Testar manifestos adulterados sem mexer no produto.
6. Provar import do módulo certo em sessão limpa e depois de troca de alvo.
7. Redigir todas as células explicativas e exemplos esperados rotulados.

**Gate:** testes negativos do próprio instrumento detectados; defaults não
fazem escrita; nenhum resultado pré-preenchido; documentação entende o fluxo.

### Sprint T2 — Spark, scripts e núcleo de ML

**Entregáveis:** notebooks 03, 04 e 05 e casos de regressão rastreados.

Tarefas:

1. Portar regressões existentes, preservando PIT e guardas temporais.
2. Acrescentar cobertura funcional de naming_checker/doc_coverage.
3. Implementar DQ e RFV com os oráculos numéricos deste plano.
4. Implementar métricas e splits com resultados verificáveis à mão.
5. Implementar costuras de retorno entre os helpers.
6. Isolar fixtures por notebook; não depender de estado entre cadernos.
7. Revisar custo, coleta, efeitos indiretos e comportamento em serverless.

**Gate:** todos os objetos do núcleo cobertos com chamada/assertion apropriada;
erro do helper não é confundido com erro de instalação ou da fixture.

### Sprint T3 — opcionais e MLflow

**Entregáveis:** O01 a O14, notebook 07 e matriz de dependências.

Tarefas:

1. Ler assinatura, efeitos e backend real de cada wrapper.
2. Configurar ambientes mínimos autorizados; evitar instalação conjunta cega.
3. Documentar parâmetros de custo reduzido efetivamente suportados.
4. Testar chamadas reais e outputs; dependência tardia deve ser exercitada.
5. Implementar gate MLflow, leitura de assinatura e ledger completo.
6. Tratar cleanup parcial, run ativo e recurso de modelo adicional.
7. Não implementar serving/registry/jobs fora do escopo para inflar cobertura.

**Gate:** cada capacidade tem prova de chamada ou bloqueio explícito. Nenhum
wrapper excluído do inventário para tornar o pacote mais fácil de homologar.

### Sprint T4 — experiência visual e exemplos didáticos

**Entregáveis:** notebooks 06 e 10, checklist visual e inventário dos exemplos.

Tarefas:

1. Resolver assets por raiz, sem duplicar cabeçalhos.
2. Cobrir todos os objetos constants/display/visual e dependências tardias.
3. Conferir números formatados e dados subjacentes aos gráficos.
4. Inspecionar cinco READMEs publicados, links e alts.
5. Classificar os 78 notebooks existentes por papel/efeito.
6. Incluir os dois objetos executáveis de moldes.
7. Preservar prosa, tópicos e direção visual aprovados; corrigir só o necessário.

**Gate:** leitura aprovada e nenhuma lacuna escondida por contagem. Esta sprint
não inicia um novo redesenho nem cria figuras substitutas sem autorização.

### Sprint T5 — avaliação conversacional

**Entregáveis:** notebooks 08 e 09; contratos de skills/prompts e rubricas.

Tarefas:

1. Portar os 39 casos de roteamento ou versionar adaptações justificadas.
2. Definir avaliação de qualidade separada do roteamento.
3. Instanciar os 16 templates com fixtures e variantes P/I/R.
4. Garantir que o contexto existe na superfície onde o assistente o acessa.
5. Prover instrução de chat novo, anexação, registro e revisão humana.
6. Prever bloqueio de cota e retomada sem inventar respostas.
7. Testar o formulário de resultados com exemplos claramente simulados, nunca
   misturando-os ao banco de evidências reais.

**Gate de implementação:** 39 + 48 casos definidos e revisados; nenhuma célula
promete invocar chat automaticamente. **Gate de execução:** respostas reais e
rubricas preenchidas no ambiente autorizado.

### Sprint T6 — pacote de testes e ensaio de transporte

**Entregáveis:** Pacote B, ficha de entrega e relatório do ensaio.

Tarefas:

1. Empacotar somente a allowlist da suíte, com manifesto e hashes próprios.
2. Limpar outputs e metadados sensíveis dos notebooks de distribuição.
3. Conferir dependência exclusiva do Pacote A e da suíte; não exigir `tools/`,
   Git, `.claude/`, pastas de protótipos ou caminhos pessoais no destino.
4. Ensaiar importação ZIP mista em pasta autorizada do laboratório, sem
   substituir produto ativo; depois conferir todos os tipos e conteúdos.
5. Ensaiar recuperação de backup no sandbox.
6. Conferir tamanho real e limites do canal corporativo.
7. Não enviar e-mail nem publicar no trabalho sem a etapa de autorização.

**Gate:** Pacotes A/B reproduzíveis, íntegros, sem segredo/PII e manualmente
importáveis conforme o procedimento; rollback de ensaio comprovado.

### Sprint T7 — implantação piloto no trabalho

**Responsáveis:** operador no trabalho + plataforma quando necessário.

Tarefas:

1. Receber anexos autorizados, conferir hash e passar por inspeção interna.
2. Fazer backup e inventário da instalação preexistente.
3. Importar staging e executar gates 00–07 conforme permissões/dependências.
4. Resolver falhas antes de promover.
5. Promover escopo pessoal e conciliar instruções com aprovação.
6. Revalidar arquivos/imports no ativo e executar a campanha 08–10.
7. Consolidar resultados no notebook 11, limpar recursos e registrar decisão.

**Gate:** aceite técnico, conversacional e operacional. Bloqueio mantém a
capacidade não homologada; correção gera tentativa/release rastreada.

### Sprint T8 — revisão geral e liberação à equipe

**Entregáveis:** relatório final interno, matriz de capacidades e aceite.

Tarefas:

1. Auditor independente compara inventário, casos, evidências e release.
2. Conferir unicidade: nenhuma versão concorrente de módulo, cabeçalho,
   instrução ou matriz; fontes e consumidores estão alinhados.
3. Fazer piloto com segundo usuário autorizado.
4. Decidir a arquitetura de compartilhamento com a plataforma.
5. Definir owner, atualização, revisão e reteste por mudança.
6. Preparar apresentação com a documentação do produto, sem inserir o
   histórico operacional nos READMEs.

**Gate:** liberação assinada pelos responsáveis no escopo aprovado. Limpeza
de protótipos do repositório pessoal é tarefa posterior, com autorização.

---

<a id="anti-deriva"></a>

## 18. Contrato contra deriva para a LLM implementadora

Antes de implementar, ler nesta ordem: `CLAUDE.md`, `.claude/CLAUDE.md`, regras
relevantes, guia de pendências, este plano, `tools/project_policy.py`,
`tools/bundle_implantacao.py`, `tools/spark_smoke_test.py`, testes locais,
catálogo e implementações das APIs. Verificar instruções adicionais da pasta
que será modificada. Não substituir a leitura dos módulos por confiança no
resumo de outra LLM.

### Regras obrigatórias

1. Implementar apenas após autorização do usuário e dentro do escopo da sprint.
2. Produto editável em `ambiente_fonte/`; simulado somente pelo renderer.
3. Futura suíte em `testes/` separada; nada dentro de `skills/` só para testes.
4. Não converter toda a biblioteca em notebooks, wheels ou outro layout.
5. Não alterar signatures, thresholds, regras temporais ou algoritmos para
   satisfazer testes; defeito real exige proposta/revisão e regressão.
6. Não inventar métodos, parâmetros, colunas, campos de retorno ou API de chat.
7. Não usar valores retornados pelo objeto sob teste como seu próprio esperado.
8. Não considerar import como prova de treino, inferência, exibição ou tracking.
9. Não copiar pins e limitações históricas como fato eterno da plataforma.
10. Não tratar `OPTIONAL_MISSING`, ausência de cota ou permissão como PASS.
11. Não prometer que selecionar `@skill` torna o resultado determinístico.
12. Não criar jobs, serving, recursos MCP ou grants como efeitos acessórios.
13. Não colocar credenciais, URLs privadas, usuários reais ou dados corporativos
    em arquivos versionados, widgets de exemplo ou relatórios externos.
14. Preservar texto, tópicos, hierarquia e figuras aprovados dos READMEs.
15. Não inserir códigos de decisões internas ou histórico de migração nos READMEs.
16. Arquivos auxiliares da suíte devem ter dono, propósito e referência no manifesto.
17. Mudança de caso, fixture, tolerância, rubrica ou dependency set recebe versão,
    justificativa e reteste; não alterar depois de ver o resultado só para passar.
18. Não apagar outputs ruins da evidência; novas tentativas são novos registros.
19. Não executar limpeza ampla; somente alvos do ledger e aprovação correspondente.
20. Registrar alterações no CHANGELOG com autoria; validar o produto ao concluir.

### Critério mínimo de revisão de cada notebook

- Outra pessoa consegue preencher parâmetros sem adivinhar paths?
- Sabe antes de executar se haverá custo, instalação, escrita ou limpeza?
- Cada teste tem pergunta, entrada, esperado e justificativa?
- Há assertions suficientes para detectar resultado errado com execução bem-sucedida?
- As exceções previstas não escondem defeitos inesperados?
- O notebook funciona após sessão limpa e não depende do anterior?
- Saída real está separada de exemplo ilustrativo?
- O caso está no manifesto e no consolidado, inclusive quando bloqueado?
- Recursos criados têm ownership e cleanup demonstráveis?
- Todas as informações necessárias existem no pacote, sem exigir o repositório pessoal?

---

<a id="fontes"></a>

## 19. Fontes e rastreabilidade deste plano

### 19.1 Documentação oficial consultada em 11/09/2026

Estas fontes sustentam capacidades da plataforma. As fixtures, oráculos,
nomes de notebooks, arquitetura de staging e gates são **decisões propostas
para este projeto**, não requisitos institucionais da Databricks.

| Tema | Fonte oficial | Uso no plano |
|---|---|---|
| Importar arquivos mistos e preview Markdown | [Workspace files basic usage](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-basics) | Upload ZIP e verificação de arquivos |
| Formatos, ZIP Source e DBC | [Import and export notebooks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import) | Transporte/backup e distinção de notebook |
| Tipos de workspace files | [What are workspace files?](https://learn.microsoft.com/en-us/azure/databricks/files/workspace) | Separação entre arquivo e recurso da plataforma |
| Imports e caminhos Python | [Work with Python and R modules](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-modules) | Origem do módulo e execução |
| Agent Skills | [Extend Genie Code with agent skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills) | Descoberta, seleção e escopos |
| Instruções e hierarquia | [Custom instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions) | Arquivo pessoal, limite e exceções |
| Uso e ações da Genie Code | [Use Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/use-genie-code) | Campanha conversacional e contexto |
| Ambiente e dependências | [Configure the serverless environment](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies) | Configuração por ambiente autorizado |
| Limitações serverless | [Serverless compute limitations](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations) | Perfis e guardas de compatibilidade |
| Testes em notebooks | [Unit testing for Databricks notebooks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/testing) | Separação de testes e código reutilizável |
| Parâmetros de notebooks | [Databricks widgets](https://learn.microsoft.com/en-us/azure/databricks/notebooks/widgets) | Formulários e validação de entrada |
| Tracking | [Track model development using MLflow](https://learn.microsoft.com/en-us/azure/databricks/mlflow/tracking) | Experimento, runs e evidências |
| Volumes | [Privileges for Unity Catalog volumes](https://learn.microsoft.com/en-us/azure/databricks/volumes/privileges) | Permissões mínimas no destino |

A UI, a disponibilidade de previews e os ambientes gerenciados podem mudar.
Antes da implementação/execução, conferir novamente as páginas que afetem a
etapa. Se a interface do trabalho não corresponder ao procedimento, registrar
o desvio e consultar a plataforma; não improvisar uma alternativa de acesso.

### 19.2 Evidência local e implementação consultadas

| Fonte local | Papel |
|---|---|
| `tools/project_policy.py` | Inventários geridos e regras de identidade |
| `tools/bundle_implantacao.py` | Conteúdo real e guardas do pacote mínimo |
| `tools/publicar_free.py` | Comparação fonte/espelho e tipos/conteúdo |
| `tools/readme_visuals/publish_production.py` | Escopo visual e estado do recibo interrompido |
| `tools/validate_assistant.py` | Estrutura, links, contratos e higiene |
| `tools/ci_local.py` | Limite do gate local, sem runtime remoto |
| `tools/spark_smoke_test.py` | Casos funcionais, fixtures e contrato MLflow por ambiente |
| `ambiente_fonte/.assistant/hub_snippets/tests/test_core.py` | Regressões locais da biblioteca |
| `ambiente_fonte/.assistant/CATALOGO_HELPERS.md` | Mapa de APIs e costuras entre objetos |
| Implementações em `hub_scripts/` e `hub_snippets/` | Assinaturas e resultados usados nos oráculos deste plano |
| `docs/testes/spark/README.md` | Resultado vigente e limitações históricas |
| `docs/testes/forward/README.md` e `roteiro.md` | Casos de roteamento e limites de interpretação |
| `docs/testes/2026-09-09_fechamento-codex.md` | Lacuna da campanha dos 16 prompts |
| `docs/playbooks/replicacao-trabalho.md` | Procedimento anterior, com divergências apontadas no guia de pendências |

O procedimento anterior não foi reescrito nesta entrega. Para esta futura
transferência, seguir as correções explícitas deste plano: ZIP Source para
backup misto; cinco diretórios `hub_`; 13 skills com estado datado; seleção
explícita sem garantia universal; testes de trabalho com oráculo próprio.

**Conclusão:** a transferência recomendada é um pacote mínimo, versionado,
sanitizado e conferido, recebido por canal autorizado, importado primeiro em
staging e ativado somente após testes. A pasta `testes/` deverá tornar cada
afirmação de funcionamento verificável, compreensível e rastreável — sem
perder funcionalidades nem confundir uma boa apresentação com uma prova de
correção técnica.
