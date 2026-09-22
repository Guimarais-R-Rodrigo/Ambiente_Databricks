# Guia de transição — Hub no Databricks do trabalho

**Rota principal: pacote mínimo com commit fixo → pasta pessoal de conferência → aceite técnico → promoção seletiva → aceite visual e da Genie.** Este é o procedimento vigente, atualizado em 11/09/2026. Foi desenhado para outro computador, **sem Databricks CLI**, com operações de instalação pela interface. Não exige clonar Git no workspace corporativo.

Mantém as decisões atuais: `.assistant_instructions.md` otimizado, READMEs/widgets/imagens já escolhidos e `MANUAL_TECNICO.md`. Não restaura pastas de rascunhos, catálogo de helpers ou glossário independentes. A instalação aqui é **pessoal**, não publicação para squad/workspace inteiro.

Use o [checklist](checklist-replicacao.md) enquanto executa e o [roteiro da Genie e das imagens](testes-genie-trabalho.md) depois da instalação técnica. Estes documentos integram o kit offline: não é necessário ler o repositório inteiro no computador do trabalho.

## 1. Por que não basta um notebook único com “Run All”

O notebook é o melhor centro de diagnóstico técnico, mas não é um instalador nem um certificado universal. Um import bem-sucedido não demonstra que o arquivo de instruções foi carregado pela Genie; um PNG íntegro não demonstra que aparece legível no README. E nenhum teste no Free comprova permissões ou políticas do trabalho.

Por isso, há quatro gates separados:

| Gate | O que prova | O que não prova |
|---|---|---|
| Pacote | identidade do commit e integridade dos arquivos transportados | autorização corporativa ou funcionamento remoto |
| Instalação | conteúdo FILE confere com o manifesto; caminhos e tipos foram revisados | que todas as chamadas da biblioteca funcionem |
| Runtime | pequenos casos sintéticos produzem os resultados esperados | cobertura dos 58 helpers, todas as dependências e todos os dados |
| Uso humano | imagens e instruções na interface; seleção e comportamento das skills | garantia universal de roteamento, segurança ou custo |

O mecanismo não marca **NAO_TESTADO**, **PENDENTE** ou dependência ausente como aprovação. Ele também separa o status do **teste** do status do **diagnóstico**: o teste de duplicidade só passa se o helper devolver `fail` para a base intencionalmente defeituosa.

Não execute o notebook antigo de smoke como primeira etapa. `tools/spark_smoke_test.py` continua como regressão avançada/histórica: percorre mais módulos, tem ramos específicos do Free e operações de tracking. O novo notebook é a entrada recomendada para esta transição. A rodada avançada precisa de escopo próprio, `target_environment=work`, experimento autorizado e revisão dos oráculos para o runtime corrente; não copie “bloqueio esperado no Free” para o trabalho.

## 2. O que preparar e baixar antes de ir para o trabalho

Na máquina de manutenção do repositório, não no Databricks do trabalho:

```powershell
python -m pip install -r tools/requirements-dev.txt
python tools/render_simulado.py --write
python tools/ci_local.py
python -m unittest discover -s tools/tests -p "test_transicao_trabalho.py" -v
```

Qualquer alteração precisa ser commitada antes de empacotar. Confirme que `git status --short` está vazio e que o commit está no remoto. Depois gere o kit em um diretório novo:

```powershell
python tools/kit_transicao_trabalho.py --output .artifacts/kit-trabalho
```

O gerador recusa checkout sujo, diretório de saída existente e fonte divergente do espelho. Usa `tools/bundle_implantacao.py`, sem conexão Databricks. Para obter outro kit, use outro diretório. Não use `--allow-dirty` para levar uma versão ao trabalho.

Também é possível gerar o mesmo kit pelo workflow **Kit de transição para o trabalho**, em GitHub Actions, no commit selecionado. Execute o workflow manualmente, confira a conclusão e baixe o artefato `kit-transicao-trabalho`. O artefato externo reúne os arquivos abaixo; ele **não** é o ZIP para importar diretamente no workspace. O workflow não publica no Databricks nem possui credenciais corporativas.

### Arquivos que você leva

| Arquivo do kit | Finalidade | Destino |
|---|---|---|
| `01_IMPORTAR_HUB_<commit>.zip` | produto e manifesto | importar em pasta vazia de staging |
| `02_IMPORTAR_ACEITE_<commit>.zip` | notebook, manifesto fixo e guias | importar na raiz da pasta do seu usuário |
| `COMECE_AQUI.md` | sequência resumida | ler no computador |
| `GUIA_TRANSICAO.md`, `CHECKLIST.md`, `TESTES_GENIE.md` | procedimento, marcação e roteiros | ler offline ou dentro da pasta de aceite |
| `01_ACEITE_TECNICO.ipynb` | cópia avulsa do notebook para inspeção | prefira usar a cópia dentro do ZIP 02 |
| `SHA256SUMS.txt` | integridade dos arquivos externos | conferir no computador autorizado |

**Não levar:** `.git`, histórico Git, `Ambiente_Antigo`, `.claude`, tokens, perfis CLI, backups corporativos de outros ambientes ou repositório completo. O README e o Manual da raiz Git não precisam de cópias extras: o produto já contém as versões adequadas em `.assistant/`.

Não confunda o ZIP externo de download com os ZIPs internos. Extraia o download no computador autorizado e importe **cada ZIP interno intacto** no local indicado. Evite recompactar manualmente: arquivos iniciados por ponto podem ser omitidos.

### Conferência do download

Compare o hash do ZIP com `SHA256SUMS.txt` usando PowerShell, sem CLI Databricks:

```powershell
Get-FileHash -Algorithm SHA256 .\01_IMPORTAR_HUB_<commit>.zip
Get-FileHash -Algorithm SHA256 .\02_IMPORTAR_ACEITE_<commit>.zip
```

Substitua o trecho `<commit>` pelo nome real do arquivo. Compare hashes sem diferenciar maiúsculas/minúsculas. A referência precisa vir de canal confiável. Um hash incluído no mesmo download detecta corrupção; **não é assinatura digital nem prova independente de autenticidade**.

Abra o ZIP 01 no computador: na raiz devem existir `.assistant_instructions.md`, `.assistant/` e `MANIFEST.json`. Não deve existir uma camada extra `Users/usuario-free` ou `ambiente_fonte`.

O manifesto v2 informa `source_commit`, `worktree_dirty=false`, paths, SHA256, tamanho e `object_type` (`FILE` ou `NOTEBOOK`). O notebook de aceite fixa o commit e o hash desse manifesto. Não misture o ZIP 01 de um commit com o ZIP 02 de outro.

## 3. Pré-condições no trabalho — conferir antes de mudar o ambiente

Confirme com a política aplicável: transporte do pacote pelo canal autorizado; acesso ao seu diretório; upload de arquivos/ZIP; suporte a Workspace Files; compute permitido; uso da Genie Code; instalação de dependências, quando necessária. A autorização para testar o Hub não é autorização para consultar dados de produção.

O caminho mostrado no navegador normalmente começa em `/Users/<username-trabalho>/`; em Python, os arquivos são acessados por `/Workspace/Users/<username-trabalho>/`. O valor real é preenchido **apenas no destino**, nunca no Git ou no pacote de origem. Abra a sua pasta pela UI e copie o caminho, sem adivinhar a partir do login de outro serviço.

Não altere configurações administrativas para contornar uma restrição. Se a importação ou Workspace Files não estiverem disponíveis, pare essa rota e solicite habilitação à equipe responsável. A alternativa manual reproduz a mesma árvore, arquivo a arquivo, mantendo o manifesto; não dispensa nenhuma conferência.

**Git folder não é a recomendação inicial.** O histórico do projeto pode conter identificadores pessoais antigos, e a ausência deles na árvore atual não limpa commits anteriores. Transporte via Git só após aprovação e auditoria do histórico. Um Git folder em local arbitrário também não substitui o caminho nativo de descoberta das skills pessoais.

## 4. Backup e inventário — antes de qualquer substituição

1. Na UI, abra `/Users/<username-trabalho>/`.
2. Localize `.assistant`, `.assistant_instructions.md` e eventual `assistant_instructions.md` sem ponto.
3. Na pasta `.assistant`, use **Download as → Zip - Source (notebook + files only)**. Exporte separadamente o arquivo de instruções, preservando seu conteúdo e o nome original.
4. Abra o backup e verifique que existem módulos `.py`, `__init__.py`, Markdown, PNGs e notebooks — não apenas notebooks. Se a exportação em lote estiver bloqueada, exporte cada escopo necessário e confirme completude antes de avançar.
5. Registre a localização do backup em um local corporativo autorizado e durável. Ele não deve ser enviado ao Git pessoal, a uma IA externa ou a outro serviço sem autorização. Pode conter `.mcp_servers.json`, caminhos e configuração sensíveis.
6. Inventarie o que pertence ao Hub e o que pertence a você/à organização. Não substitua `.assistant` ou `skills` inteiras indiscriminadamente.

**Não use DBC como único backup:** a opção DBC documentada é “notebooks only”; o Hub depende também de FILEs. ZIP de código-fonte não representa backup de ACLs, histórico, segredos, estado da sessão, experimentos MLflow ou todas as configurações de ambiente. Registre separadamente o que a política exigir e teste a recuperação dos arquivos em diretório isolado. [Fonte: formatos de exportação](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import).

Backups não devem ficar em pastas de descoberta ativa. Uma skill antiga mantida dentro de `.assistant/skills` ainda pode interferir no roteamento. Guarde o backup fora de `skills` e fora do alcance hierárquico dos notebooks utilizados pela Genie.

## 5. Importar em staging sem ativar as novas instruções

No kit, `<commit>` representa os **12 primeiros caracteres** do commit indicado em `COMECE_AQUI.md`.

1. Em **Workspace**, abra a raiz do seu usuário.
2. Use **Create → Folder** e crie `hub_staging_<commit>`.
3. Abra essa pasta vazia. Menu `⋮` ou botão direito → **Import** → selecione `01_IMPORTAR_HUB_<commit>.zip` → **Import**.
4. Abra a pasta importada. Confirme que `.assistant` e `.assistant_instructions.md` estão **diretamente** dentro de `hub_staging_<commit>`. Se a UI criou outra camada com o nome do ZIP, ajuste a organização dentro da pasta vazia ou use esse caminho real na configuração; não siga com paths presumidos.
5. Volte à raiz do usuário e importe `02_IMPORTAR_ACEITE_<commit>.zip`. O ZIP contém a pasta `aceite_hub_<commit>/` com o notebook, os guias e uma cópia fixa de `MANIFEST.json`.
6. Abra `aceite_hub_<commit>/01_ACEITE_TECNICO` (a UI pode esconder `.ipynb` no nome).

A UI documenta que ZIPs são descompactados e seus arquivos/notebooks importados. A distinção depende da extensão e do marcador de notebook. Confira no destino: não conclua sucesso apenas porque o ZIP foi aceito. [Fonte: importação de arquivos](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-basics).

Esta pasta de staging **não ativa** as skills pessoais, cujo caminho nativo é `/Users/<username>/.assistant/skills/`. Também não substitui as instruções pessoais da raiz do usuário. Não tente provar roteamento da candidata antes da promoção final. [Fonte: skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills).

### Árvore esperada nesta etapa

```text
/Users/<username-trabalho>/
├── .assistant/                         # versão anterior, ainda preservada
├── .assistant_instructions.md          # instruções anteriores, se existirem
├── hub_staging_<commit>/
│   ├── .assistant_instructions.md       # candidata ainda não ativa
│   ├── .assistant/                     # produto do kit
│   └── MANIFEST.json
└── aceite_hub_<commit>/
    ├── 01_ACEITE_TECNICO.ipynb
    ├── MANIFEST.json                   # identidade fixa que o notebook usa
    ├── GUIA_TRANSICAO.md
    ├── CHECKLIST.md
    └── TESTES_GENIE.md
```

Não importe `tools/` como pasta do produto. O código do mecanismo de teste já está embutido no notebook gerado. O pacote de aceite fica fora de `.assistant` para não poluir o Hub nem seu contexto permanente.

## 6. Executar o notebook técnico, célula por célula

### Primeira passagem: identidade e arquivos

Na célula 1 de configuração, preencha `USER_HOME`, confirme `KIT_DIR` e `STAGING_ROOT`, mantenha `PHASE="staging"`. Deixe `EXECUTAR_SPARK`, `TESTAR_MLFLOW`, `TESTAR_LEITURA_UC` e `CONSULTAR_TIPOS_VIA_API` desligados inicialmente.

Conecte ao compute permitido pela organização para executar Python. Mesmo leituras locais do notebook podem requerer uma sessão/compute com custo; “sem consultar tabelas” não significa “sem custo Databricks”. Execute as células de configuração, definições, criação da sessão, manifesto e arquivos. Se uma falhar, não promova o pacote.

A verificação SHA256 cobre **todos os FILEs do manifesto**, incluindo instruções, Manual, READMEs, módulos e imagens. Não executa os arquivos. Uma divergência de fim de linha ou edição é divergência de bytes: reimporte e investigue, não altere o hash esperado.

**Notebooks são tratados separadamente.** A plataforma pode converter SOURCE para representação de notebook; o notebook de aceite não declara igualdade dos bytes/células desses objetos. O inventário informa quantos não receberam essa comprovação. Confira tipos, abertura em células e ausência de erro ao abrir exemplos representativos. Se houver autorização, preencha `WORKSPACE_HOST` com a origem HTTPS exata do navegador e habilite `CONSULTAR_TIPOS_VIA_API`: consulta somente metadata dos notebooks do manifesto, sem escrita/CLI/token manual. Uma falha deve ser investigada, não reinterpretada como aprovação.

### Segunda passagem: imports e execução sintética

Após passar em arquivos, escolha o ambiente Python aprovado. Em notebook serverless, confira o painel **Environment**; no compute clássico, confira o runtime e as políticas de bibliotecas. Não fixe a versão do laboratório por imitação. Não instale `pyspark` dentro do serverless gerenciado, não cole todos os pins históricos e não mude NumPy/pandas especulativamente. Se faltar uma biblioteca, instale apenas o componente necessário pelo mecanismo autorizado, reinicie Python e recomece. [Fonte: dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies).

Habilite `EXECUTAR_SPARK=True` e reinicie a sessão Python antes de recomeçar. O notebook exige imports frescos para não aceitar módulos em cache de outro teste. Não apaga `sys.modules` nem faz reload silencioso.

| Teste | Resultado esperado | Significado |
|---|---|---|
| Manifesto | PASS | commit e hash do manifesto coincidem com o notebook |
| Arquivos | PASS | todos os FILEs mantêm bytes e nomes esperados |
| Imports | PASS | seis módulos públicos vieram da instalação sob teste |
| Python | `R$ 1.250.000,50`, `15,4%` | contrato básico de formatação |
| Spark | N=20, soma=190 | ação real em dados sintéticos |
| DQ aviso | teste PASS; diagnóstico `warn`, score95 | detectou 5% de nulos |
| DQ falha | teste PASS; diagnóstico `fail` | detectou duplicidade proposital |
| RFV | valor30, frequência2, recência5 | excluiu o evento futuro |
| PIT | duas linhas e valor10 | preservou multiplicidade dos fatos e atraso de publicação |
| PSI | zero | distribuições idênticas não produziram drift |
| Plotly | objeto válido + conferência visual | construção e apresentação são verificações separadas |

Os testes não usam `cache`, `persist`, RDD ou internos JVM. Utilizam DataFrames pequenos, operações suportadas pelo contrato atual e views temporárias com nomes exclusivos, removidas no `finally` de cada caso. A sessão não cria tabelas, volumes, jobs ou endpoints. [Fonte: limitações serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations).

Um teste pulado por configuração deixa o resumo **INCOMPLETO**, e pré-requisitos falhos bloqueiam os dependentes. Isso é preferível a exibir um “tudo certo” que na verdade significa “não testei”.

### Extensões que não devem bloquear a primeira instalação por ausência de autorização

**MLflow:** desligado por padrão. Para usar, crie previamente pela UI um experimento pessoal temporário autorizado, preencha `EXPERIMENTO_TEMPORARIO`, confirme `WORKSPACE_HOST` e habilite `TESTAR_MLFLOW`. O teste exige tracking no workspace atual, cria um run, grava parâmetro/métrica, lê de volta e exclui logicamente somente o próprio run. Não altera o experimento ativo da sessão, não encerra run alheio, não cria experimento, não registra modelo nem testa serving. Se a exclusão falhar, o caso reprova; consulte `aceite.mlflow_run_id` apenas no destino e resolva a limpeza do run próprio. Exclusão lógica não é expurgo físico/auditoria. [Fonte: tracking](https://learn.microsoft.com/en-us/azure/databricks/mlflow/tracking).

**Unity Catalog:** desligado por padrão. `TESTAR_LEITURA_UC` autoriza uma consulta `SELECT 1 ... LIMIT 1` na única tabela informada. Não imprime valores corporativos e não enumera catálogos. A consulta ainda pode gerar custo/leitura e não prova acesso a outras tabelas nem permissões de escrita. Não use uma tabela produtiva apenas para “ver se passa”. Uma tabela sintética governada já existente e autorizada é preferível.

**Modelos opcionais:** inventariar versões não é testar import ou `fit`. Só habilite LightGBM, XGBoost, CatBoost, SHAP, UMAP, séries temporais etc. quando sua tarefa precisar deles, em rodada dedicada com dados sintéticos, dependências mínimas, tracking conhecido e critérios próprios. O piloto básico não certifica os 58 helpers.

## 6.5. Gate SE08 antes de qualquer promoção

A transição do Hub pode ser preparada e testada em staging sem que o Skill
Enforcement Framework esteja autorizado para promoção. Antes de mover uma
candidata SEF para a instalação pessoal do trabalho, registre separadamente o
gate SE08.

Os oito requisitos canônicos são:

1. validações locais pertinentes em PASS no SHA congelado;
2. renderer sem divergência;
3. publicação no Databricks Free verificada por conteúdo;
4. casos críticos da SE06 sem escaped non-compliance;
5. zero achados críticos/altos abertos relacionados ao enforcement;
6. documentação operacional completa;
7. aceite explícito do usuário;
8. plano de rollback definido e executável.

O Gate G2 da SE06 autorizou somente a transição SE06 → SE07. Ele preservou
`behavioral_runs_observed=24/25`, `S06-A1-R4=NOT_RUN`,
`SE06_DOD=INCOMPLETE` e `FULLY_CERTIFIED=false`, e declarou
explicitamente que essa exceção **não satisfaz o gate de promoção corporativa
da SE08**. Enquanto não houver nova decisão humana específica sustentada por
evidência suficiente, registre o gate de promoção SE08 como **BLOQUEADO**; não
converta o fechamento administrativo da SE07 em autorização para o trabalho.

O residual aceito da SE07 também permanece histórico: storage cleanup FAIL 8/9
e `SE07_FULLY_CERTIFIED=false`. FULL verde, aceite humano ou ausência de nova
reprodução do WinError32 não apagam esses estados.

`tools/publicar_free.py` continua exclusivo do laboratório Free. Para o
workspace do trabalho use somente este runbook e apenas no escopo pessoal
autorizado. Não publique em `Workspace/.assistant/skills/` nem altere
instruções compartilhadas sem governança administrativa própria.

## 7. Promover seletivamente para a instalação pessoal

Só avance com backup conferido, FILEs íntegros e núcleo técnico aprovado em staging. Feche conversas e evite alterações simultâneas no escopo do Hub; a cópia manual não é uma transação atômica.

Na raiz de `.assistant`, o pacote vigente tem **cinco** diretórios `hub_`, não quatro:

```text
hub_padroes/
hub_prompts/
hub_readmes_visual_assets/
hub_scripts/
hub_snippets/
```

Além deles, há `README.md`, `MANUAL_TECNICO.md` e `skills/` com as treze skills do pacote. O manifesto é a lista de arquivos da release; o roteiro da Genie contém os nomes exatos das skills atuais. A raiz documental do Hub continua com README e Manual, sem catálogo/glossário independentes.

1. Pela UI, crie uma pasta de rollback pessoal fora de `.assistant/skills/`, se a política permitir. Não use as pastas nativas de descoberta para guardar cópias.
2. Para cada um dos cinco diretórios `hub_`, confirme propriedade e ausência de customização desconhecida. Mova a versão anterior para rollback e copie/mova a candidata correspondente de staging para `.assistant/`. Se houver conteúdo de terceiros misturado, pare e faça reconciliação; não apague a pasta inteira.
3. Em `skills/`, substitua **somente** as treze pastas atuais declaradas e retire as antigas pertencentes ao Hub após backup/identificação. Não selecione `skills/` inteira. Prefixo antigo sozinho não prova que um objeto pode ser removido; use o inventário anterior, `legacy_skill_names_for_review` no manifesto e os nomes do roteiro.
4. Substitua `README.md` e `MANUAL_TECNICO.md` pelos arquivos candidatos. Retire `CATALOGO_HELPERS.md` e `GLOSSARIO.md` somente se forem as cópias geridas pelo Hub, preservando o backup.
5. **Preserve `.assistant/.mcp_servers.json`, skills alheias, arquivos pessoais e instruções administrativas.** Não copie configuração MCP de outro ambiente.
6. Só depois de o Hub estar no lugar, atualize `.assistant_instructions.md` na raiz do seu usuário. Prefira mover/importar o FILE exato do pacote, sem alterar a redação durante a instalação. Preserve no backup qualquer conteúdo pessoal anterior; não concatene instruções conflitantes automaticamente.
7. Em **Genie Code → Settings → User instructions → Open instructions file**, confirme que abre esse arquivo, com o ponto inicial e o conteúdo “operação integrada do Hub”. Se for oferecido **Add instructions file**, use-o para localizar/criar o arquivo nativo e inserir o conteúdo aprovado, conferindo depois o hash. O arquivo sem ponto não ativa o mecanismo.

A configuração pessoal pertence à raiz do usuário, não a `hub_staging`, a `.assistant` ou à pasta de um notebook. A Databricks aplica alterações na próxima interação, com exceções Quick Fix/Autocomplete; para comparar comportamento sem histórico anterior, use chat novo. [Fonte: instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions).

Se o procedimento exigir mexer em permissões, políticas de workspace ou instruções compartilhadas, isso deixa de ser esta instalação pessoal: pare e envolva a administração.

## 8. Verificar no destino final e testar a experiência

Reinicie Python. No notebook de aceite, configure `PHASE="final"` e `PRODUCT_ROOT=USER_HOME` como definido pela configuração gerada. Mantenha `KIT_DIR` na pasta de aceite original; o manifesto não deve ser trocado pelo arquivo que acabou de ser modificado no destino. Rode os testes novamente. Um PASS de staging não cobre erros de movimentação na promoção.

Abra os READMEs reais no workspace e execute o roteiro humano. Não basta ler o Markdown cru: confirme banners, diagramas, tabelas, links e widgets selecionados. Abra também `hub_snippets/constants/format_br/format_br.py` como FILE e `hub_snippets/spark/pit_join/exemplo_pit_join.py` como NOTEBOOK. A UI pode omitir `.py` na apresentação de notebooks; não renomeie módulos para tentar forçar imports. [Fonte: tipos de arquivos e notebooks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import).

Para a Genie, use chats novos, testes pequenos, sem execução de código ou dados reais. Registre separadamente: descoberta/seleção observada, metodologia aplicada, helpers recomendados e qualidade da resposta. Um nome escrito na resposta não prova carregamento. Se a UI não expuser evidência suficiente, marque esse item como **PENDENTE**, descrevendo a limitação; não certifique por autoafirmação do agente.

Após editar skills, a documentação orienta novo chat; se o comportamento/metadata antigos persistirem, faça hard refresh. Não declare seleção determinística: `@` é seleção explícita, mas não garante qualidade perfeita do resultado. [Fonte: edição de skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills).

## 9. Interpretar o veredito consolidado

| Veredito | Ação |
|---|---|
| `BLOQUEADO` | corrigir erro/pré-condição ou rollback; não promover |
| `INCOMPLETO` | ainda faltam testes automáticos; não equivale a falha comprovada |
| `STAGING_TECNICO_APROVADO_NAO_ATIVADO` | pronto para a promoção manual, não para uso da Genie candidata |
| `TECNICO_APROVADO_ACEITE_HUMANO_PENDENTE` | arquivos/runtime passaram, faltam UI/Genie/backup |
| `BASE_OK_EXTENSAO_REPROVADA` | núcleo passou, mas extensão habilitada falhou; investigar antes de usá-la |
| `PRONTO_PARA_PILOTO_BASICO` | uso pessoal limitado ao escopo testado; não é liberação produtiva |

A célula `CONFIRMACOES` aceita CONFIRMADO, PENDENTE e REPROVADO. Não preencha antes de observar. O resultado guarda essas declarações humanas separadamente dos testes automáticos. A confirmação de tipos pela UI continua relevante mesmo com metadata via API: abra pelo menos os exemplos indicados, confira células e navegação.

## 10. Diagnóstico por sintoma

| Sintoma | Causa provável / próxima ação |
|---|---|
| `manifesto → FAIL` | ZIPs de releases diferentes, arquivo incorreto ou edição do manifesto; recupere o kit íntegro |
| FILE ausente | camada extra de pasta, upload que ignorou arquivo oculto, tipo errado ou acesso negado |
| SHA256 divergente | edição, corrupção ou mudança de representação; compare o original e reimporte, não relaxe o teste |
| `imports → FAIL` com cache | restart Python e execução desde configuração; não use reload automático |
| `ModuleNotFoundError` | confira path e dependência específica; o inventário instalado não é prova de import |
| Spark falha antes dos helpers | compute, sessão, rede ou política; não reescreva biblioteca ainda |
| DQ retorna `warn` no teste de 5% | resultado esperado, o teste deve dar PASS |
| DQ retorna `fail` na duplicidade | resultado esperado, o teste deve dar PASS |
| PIT/RFV/PSI divergem | incompatibilidade/defeito real a investigar; não aceite valor só porque a célula terminou |
| PNG íntegro não aparece no README | caminho relativo, importação/pasta, leitura ou renderização; confira no próprio README |
| Skill aparece mas comportamento antigo | chat antigo, cache, duplicata ou escopo compartilhado; compare Settings e novo chat |
| Genie não lê referência ao Manual | referência não é carregamento garantido; forneça trecho/arquivo necessário, não o manual inteiro |
| MLflow falha | confira experimento, política e run residual; bloqueio do Free não é oráculo do trabalho |
| `PERMISSION_DENIED` | não contorne ACL; peça revisão à equipe responsável |

O notebook não exporta exceções brutas automaticamente. Para diagnosticar, o objeto `aceite.errors_local` mantém a exceção na sessão. Inspecione somente no ambiente autorizado; a mensagem pode conter hostname, usuário, paths e nomes de tabelas. Não copie o objeto inteiro para Git ou IA externa.

## 11. Evidência e rollback

O JSON final é gerado sem caminho de usuário, host, tabela, experimento, token ou traceback. Registra commit, hash do manifesto, estados, contagens e declarações. **Revise antes de compartilhar**: minimização automática não substitui a política corporativa. Mantenha detalhes completos, backups e screenshots identificáveis dentro do ambiente autorizado. Não exporte o notebook preenchido com USER_HOME real para o Git pessoal.

Para rollback, interrompa a adoção, preserve o recibo e restaure somente os componentes Hub que foram substituídos, incluindo as instruções anteriores. Preserve novamente `.mcp_servers.json` e conteúdo alheio. Não restaure toda `.assistant` sobre modificações legítimas de terceiros ocorridas depois do backup. Abra chat novo, reinicie Python e confirme o funcionamento da versão restaurada. Restaurar arquivos não recria ACLs/configurações de compute nem desfaz operações externas.

Os testes básicos usam apenas views locais próprias e não deixam tabelas persistentes. Se o teste MLflow foi habilitado, confira a exclusão lógica do run próprio; uma falha de limpeza precisa de tratamento específico e não se resolve recolocando arquivos do Hub.

Ajustes descobertos no trabalho devem voltar à fonte canônica com dados de teste sintéticos. Não incorporar paths/PII do trabalho ao repositório. Uma edição emergencial no workspace deve ser reconciliada antes da próxima atualização para não ser perdida.

## 12. Limites da entrega atual

Este guia e seus testes são preparação para **medir** o ambiente do trabalho. Gate local, integridade de pacote, testes com Spark local e registros antigos do Free são evidências distintas. Não existe nesta entrega execução no workspace corporativo, autenticação corporativa, homologação conversacional ou autorização para produção.

O produto e suas imagens/README/instruções não são reescritos por este fluxo. A adoção pela squad é posterior: exige governança, responsáveis, permissões e instruções compartilhadas adequadas. Não copiar o arquivo de instruções pessoais para o workspace inteiro como atalho.

## Fontes oficiais consultadas em 11/09/2026

- [Arquivos do workspace e importação ZIP](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-basics).
- [Formatos de notebooks, marcador e exportação Source/DBC](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-export-import).
- [Workspace Files, imports e limites de acesso](https://learn.microsoft.com/en-us/azure/databricks/files/workspace).
- [Instruções pessoais/workspace e exceções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions).
- [Skills, localização, recursos e edição](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills).
- [Dependências de ambiente serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies).
- [Limitações serverless e Spark Connect](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations).
- [Tracking de modelos com MLflow](https://learn.microsoft.com/en-us/azure/databricks/mlflow/tracking).

Nomes de menus podem variar com a versão/interface. Uma permissão não disponível não é suprida pelo texto do guia; preserve o bloqueio e registre o ponto que depende da administração.
