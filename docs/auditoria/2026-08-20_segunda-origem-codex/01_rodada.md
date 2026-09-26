# Auditoria A2 — segunda origem com execução (Codex)

> **REGISTRO DO BASELINE.** As severidades e o veredito abaixo preservam o
> diagnóstico emitido antes do contraditório. A posição final, as correções e os
> testes pós-correção estão em
> [02_treplica-e-execucao.md](02_treplica-e-execucao.md). Não use os rótulos
> desta página como estado atual.

- **Data:** 2026-08-20
- **Baseline auditado:** `9c17008`
- **Escopo:** 894 arquivos versionados; produto, biblioteca, ferramentas,
  documentação viva, decisões, segurança e replicação
- **Método:** cinco frentes especializadas em subagentes, probes de valor
  conhecido, mutation tests, execução local e job real no Databricks Free
- **Natureza desta rodada:** diagnóstico; nenhuma correção foi aplicada ao
  produto, aos runbooks ou aos ADRs

## 1. Veredito em uma frase

O projeto passa os quatro gates atuais, mas **não está seguro para replicação no
workspace de trabalho**: há operações destrutivas nos runbooks, proteção
insuficiente contra publicação no destino errado, PII versionada, falsos verdes
nos validadores e erros matemáticos confirmados na biblioteca.

## 2. Reprodução dos quatro gates

Os gates foram executados **antes** dos probes e da criação deste relatório.

| Gate | Comando/evidência | Resultado reproduzido | Limite revelado pela auditoria |
|---|---|---|---|
| Estrutura local | `python tools/validate_assistant.py` | **APROVADO**, 0 falhas, 0 avisos; 23 checks | mutation tests encontraram falsos negativos semânticos |
| Saídas do README | `python tools/validate_assistant.py --conferir-readme` | **APROVADO**, 14 linhas | não confere todo número que o README apresenta |
| Publicação remota | `python tools/publicar_free.py --verify` | **APROVADO**, 0 problemas; 314 esperados; 13/13 skills | compara quantidades, não a identidade/validade das skills |
| Runtime real | import do notebook + `databricks jobs submit` | **SUCCESS**; 145 total, 136 PASS, 0 FAIL, 8 `OPTIONAL_MISSING`, 1 `BLOQUEADO_ESPERADO`; Spark 4.1.0 | o oráculo de bloqueio aceita qualquer exceção |

Evidência do quarto gate: run `421891787481190`, task
`1036929425660395`, 56 s de execução e 60,7 s totais. O único bloqueio desta
execução foi inspecionado e trazia a assinatura esperada de configuração MLflow
indisponível no Spark Connect. Isso valida **esta execução**, mas não elimina a
falha de desenho do oráculo.

O teste unitário local `hub_snippets/tests/test_core.py` não iniciou porque este
host não possui `scikit-learn`. O fato foi registrado como limite; os testes não
foram declarados aprovados.

## 3. Achados, ordenados pelo custo

### 🔴 F01 — o publicador não prova que o destino é o laboratório Free

- **Onde:** `tools/publicar_free.py:32,68-79`.
- **Diz:** “Esta ferramenta publica no laboratório Free; o workspace do
  trabalho usa o runbook manual”.
- **É:** a ferramenta olha apenas uma regex reduzida sobre o username e não
  confere host ou perfil. Dois usernames corporativos sintéticos que a regex do
  validador bloqueia foram aceitos pelo publicador em mock; somente o padrão
  estreito do próprio publicador foi recusado.
- **Custo:** com a CLI apontada para outro perfil, `--execute` pode escrever o
  pacote pessoal no workspace errado.
- **Correção específica:** exigir allowlist explícita do host/profile do Free,
  mostrar o destino e pedir confirmação consciente no modo de escrita; usar uma
  única política de identidade compartilhada pelas ferramentas.

### 🔴 F02 — PII pessoal está versionada e é tratada como exceção informal

- **Onde:** `CLAUDE.md:55-59`; `README.md:335-349`;
  `tools/render_simulado.py:27`; `docs/testes/forward/roteiro.md`;
  `.claude/context/perfil-usuario.md:9`; um template congelado em
  `Ajustes_Codex/`; paths de `Novo_Ambiente_Simulado/Users/<e-mail-pessoal>/`.
- **Diz:** o canônico exige placeholders e proíbe PII em arquivo versionado; o
  README e o código aceitam o username pessoal do laboratório.
- **É:** a varredura encontrou 45 linhas com e-mail pessoal (44 no roteiro e
  uma no renderer), 314 paths rastreados contendo o e-mail e dois paths locais
  pessoais adicionais. A varredura global usa a regex corporativa, não a de
  PII pessoal.
- **Custo:** Git, ZIP, bundle e clone para máquina corporativa transportam PII;
  o gate verde promete alcance maior que o implementado.
- **Correção específica:** render versionado com `Users/usuario-free/`; roteiro
  com `<username>` e cópia personalizada local-only; redação dos paths; scanner
  de conteúdo **e path** sobre todo arquivo rastreado; novo ADR para resolver a
  exceção, sem reescrever o ADR-0003.

### 🔴 F03 — o runbook manda apagar configuração MCP e todas as skills

- **Onde:** `docs/playbooks/replicacao-trabalho.md:87-95` e
  `docs/playbooks/checklist-replicacao.md:76-83`.
- **Diz:** o problema são skills antigas “com o mesmo nome”, mas a ação manda
  remover `skills/` inteira; também manda remover `.mcp_servers.json`.
- **É:** `.claude/rules/genie-code-oficial.md:25-29` e
  `tools/publicar_free.py:38-42` classificam o JSON como estado gerido pela
  plataforma que não deve ser removido. A deleção de `skills/` inclui qualquer
  skill pessoal ou organizacional não pertencente ao Hub.
- **Custo:** perda de conectores e funcionalidades externas no workspace do
  trabalho. Backup permite rollback total, mas não preserva coexistência nem
  evita merge manual.
- **Correção específica:** inventariar filhos e remover somente uma allowlist de
  nomes gerenciados pelo Hub; preservar MCP e skills alheias; conferir o diff
  antes de qualquer deleção.

### 🔴 F04 — o smoke do trabalho pode criar run MLflow e chamar erro interno de bloqueio

- **Onde:** `docs/playbooks/replicacao-trabalho.md:150-167,179-183`;
  `tools/spark_smoke_test.py:71-92,568-579`;
  `hub_snippets/ml/mlflow_run/mlflow_run.py:137-159`.
- **Diz:** executar a mesma bateria no trabalho; qualquer exceção do caso MLflow
  vira `BLOQUEADO_ESPERADO`; o rollback não deixa resíduo.
- **É:** mock confirmou `start_run`, tags e `end_run`, seguido de `ValueError`
  por execução incompleta. O caso passa `limitacoes` como string e não registra
  parâmetros, métricas, assinatura ou modelo. O wrapper do smoke classifica
  qualquer exceção como bloqueio da plataforma.
- **Custo:** falso aceite e run residual no tracking server corporativo.
- **Correção específica:** oráculo por classe + assinatura da mensagem; casos
  distintos para Free e trabalho; run temporário completo, identificado e com
  limpeza explícita no trabalho; `limitacoes` como lista.

### 🟠 F05 — fonte e remoto podem aprovar apenas 12 skills reais

- **Onde:** `tools/validate_assistant.py:110-135`;
  `tools/publicar_free.py:34-35,226-231`.
- **Diz:** 13/13 skills e frontmatter YAML válido.
- **É:** sandbox com 12 skills válidas e uma pasta lixo retornou `RC=0` no
  validador (`12/12`) e no verify remoto (`13/13`). Frontmatter com
  `description` vazia, YAML inválido ou sem delimitador final também passou;
  YAML válido com nome entre aspas gerou falso positivo.
- **Custo:** uma skill some da descoberta do Genie Code enquanto os dois gates
  continuam verdes.
- **Correção específica:** conjunto canônico de nomes esperados; comparação de
  nomes no fonte e remoto; parser YAML real; strings não vazias e validação
  completa da especificação Agent Skills.

### 🟠 F06 — checks de contrato analisam ocorrências lexicais, não o contrato operacional

- **Onde:** `tools/validate_assistant.py:193-252,833-976`.
- **Diz:** confere o que o notebook consome e “toda chamada” à API pública.
- **É:** `df.select("ghost")` passa; um literal incidental `"ghost"` no módulo
  mascara um acesso inválido; consumo no primeiro bloco não é tratado
  corretamente. `f(bad=1)` é pego, mas `mod.f(bad=1)` passa. Nove referências
  abreviadas a helpers atuais não entram nos 72 caminhos contados.
- **Custo:** notebooks e skills podem continuar apontando para colunas,
  parâmetros ou helpers inexistentes com validação verde.
- **Correção específica:** AST com resolução de aliases, `ast.Attribute`,
  contexto de célula e chaves efetivamente retornadas/criadas; expandir os nove
  caminhos ou ensinar herança de prefixo.

### 🟠 F07 — guardas de normas e sincronização validam proxies frágeis

- **Onde:** `tools/validate_assistant.py:611-721,1021-1046` e check de seções.
- **Diz:** quatro normas do molde, sincronização do detector de notebook e cinco
  seções completas.
- **É:** `cache()` em `else/finally`, `toPandas()` com a palavra `limit` em
  comentário e `spark` ligado em outro escopo passam; `Memo.cache()` legítimo
  reprova. Implementações opostas do detector, com as mesmas constantes,
  passam. Títulos vazios/infinitivos arbitrários simulam fluxo e “nunca fazer”.
- **Custo:** o selo de conformidade não conserva a propriedade que o texto diz
  testar.
- **Correção específica:** AST sensível a fluxo/escopo/tipo; tabela executável
  de casos do detector ou implementação única; separar presença estrutural de
  evidência comportamental.

### 🟠 F08 — o renderer permite path traversal e usa política de identidade divergente

- **Onde:** `tools/render_simulado.py:27-32,54,62-97`.
- **Diz:** `--username` apenas sobrepõe o usuário do simulado.
- **É:** dry-run com `..\..\escape` resolveu o destino fora de
  `Novo_Ambiente_Simulado`. As regexes de renderer, publicador e validador
  aceitam conjuntos diferentes.
- **Custo:** `--write` pode criar/copiar a árvore fora do destino pretendido;
  uma identidade bloqueada pelo primeiro gate pode nascer no render seguinte.
- **Correção específica:** aceitar um único componente de path; provar por
  `resolve()` que o destino permanece sob `TARGET_ROOT/Users`; módulo único de
  identidade com mutation tests.

### 🟠 F09 — o bundle pode entregar corpus vazio e omite superfícies de segurança

- **Onde:** `tools/bundle_para_auditoria.py:3-10,27,38-66`.
- **Diz:** empacota o corpus inteiro; derivado e congelado não acrescentam
  informação.
- **É:** mock de `git ls-files` com RC 128 gerou bundle de zero arquivos e
  retorno 0. Por padrão, 489/894 paths são excluídos. Os bytes derivados podem
  ser iguais, mas o path contém informação de segurança/PII.
- **Custo:** auditoria externa recebe corpus vazio ou perde metadados relevantes
  sem falha explícita.
- **Correção específica:** falhar em RC não zero/lista vazia; cabeçalho com
  commit, manifest, hashes e exclusões; modos `canonical`, `security` e `full`;
  preflight/redação de PII.

### 🟠 F10 — as instruções automáticas se contradizem sobre dependências e contexto

- **Onde:** `ambiente_fonte/.assistant_instructions.md:8,12,24,35` e
  `hub_snippets/requirements-optional.txt:26-48`.
- **Diz:** fixar NumPy/pandas em qualquer instalação; usar como contexto apenas
  o que entrou por `@`/Add context; arquivo do projeto vence inclusive diante de
  limites chamados inegociáveis.
- **É:** o inventário medido proíbe pin preventivo e limita pins a três casos.
  Genie Code também recebe instruções, `AGENTS.md`/`CLAUDE.md` e metadados de
  tabela, conforme documentação oficial.
- **Custo:** a instrução carregada na maioria das interações pode quebrar o
  runtime ou mandar ignorar contexto legítimo; conflito de precedência não tem
  resolução segura.
- **Correção específica:** remeter ao inventário datado; proibir pin preventivo;
  separar limites de segurança de preferências; dizer quais **recursos de
  dados** precisam ser anexados sem negar contexto automático.

### 🟠 F11 — os 16 prompts não cumprem o molde publicado

- **Onde:** norma em `hub_padroes/prompt/template.md:23-51`; corpus em
  `hub_prompts/*/*.md`.
- **Diz:** explicar por que cada placeholder importa; incluir “O que conferir
  na resposta” e “Limites”.
- **É:** 161 campos únicos; somente três são explicados nominalmente antes do
  bloco; 0/16 têm as duas seções normativas; 16/16 substituem por
  `Follow-ups úteis`. Dois prompts sem skill recomendada mantêm boilerplate que
  fala “na skill recomendada”. Três notebooks dizem que criam tabela, mas não
  executam escrita. `hub-ml-criar-objeto` exige “três arquivos” para tipos cujo
  molde define um ou dois.
- **Custo:** prompt detalhado para o modelo, mas pouco didático para o usuário;
  contratos de efeito lateral e entrega são falsos.
- **Correção específica:** tabela `campo → como preencher → por que importa →
  exemplo`; QA humano e limites; remover boilerplate sem rota; matriz de
  artefatos obrigatórios por tipo.

### 🟠 F12 — outputs duráveis não carregam proveniência para a auditoria prometida

- **Onde:** requisito em `hub-ml-auditoria-skills/SKILL.md:50-67`; exemplos em
  templates de EDA, monitoramento, pipeline e na própria auditoria.
- **Diz:** auditar pedido original contra o `SKILL.md` produtor.
- **É:** templates normalmente não registram prompt, skill produtora,
  versão/commit do contrato, recursos/snapshots e data de execução.
- **Custo:** fora da conversa, o artefato não é reprodutível nem auditável contra
  o contrato exato.
- **Correção específica:** bloco comum de proveniência em todo output durável;
  restringir a description ampla de auditoria a um `SKILL.md` explicitamente
  nomeado.

### 🟠 F13 — KS muda de unidade entre helpers acoplados

- **Onde:** `metrics_report.py:48-50,88-94`;
  `performance_monitor.py:21-24`; `curves_plotly.py:246-249`.
- **Diz:** `metrics_report` é padronizado; o monitor usa limiar absoluto 0,03/
  0,05; curvas trabalham em 0–1.
- **É:** KS estatístico 0,5 vira 50,0. Baseline 40 → 39 gera delta 1,0 e status
  crítico; baseline 0,40 → 0,39 gera delta 0,01 e status saudável.
- **Custo:** alerta crítico falso e governança acionada por unidade, não por
  degradação.
- **Correção específica:** unidade canônica 0–1 ou nome `ks_pct`; teste de
  composição `metrics_report → PerformanceMonitor`.

### 🟠 F14 — vintage fabrica observações e viola monotonicidade acumulada

- **Onde:** `vintage_analysis.py:80-105,122-133`.
- **Diz:** lacunas imaturas ficam de fora e `taxa_acumulada` é acumulada.
- **É:** contrato com target cumulativo 1 em MOB 0 e 2, sem MOB 1, produziu
  `50% → 0% → 50%`, com cobertura 100% nos três. Contrato cuja primeira foto é
  MOB 1 é fabricado em MOB 0. Target nulo é aceito e convertido em não-evento.
- **Custo:** maturidade superestimada e comparação de safras incorreta.
- **Correção específica:** coluna de observação real; lacuna permanece `NaN`;
  rejeitar target nulo salvo política; invariantes de monotonicidade e cobertura
  baseados somente em snapshots existentes.

### 🟠 F15 — o diagnóstico do `pit_join` não reconcilia causas

- **Onde:** `pit_join.py:137,203-225`.
- **Diz:** separa chave nula, entidade sem histórico e histórico indisponível.
- **É:** `validos_totais` já exclui `sem_chave`, mas a fórmula subtrai
  `sem_chave` outra vez. “Entidade sem histórico” usa pares distintos, enquanto
  os outros contadores usam linhas.
- **Custo:** o join pode estar certo e a causa operacional atribuída errada.
- **Correção específica:** indicadores mutuamente exclusivos por linha de fato;
  assert de soma igual a `linhas_fato`.

### 🟠 F16 — features temporais removem dados alheios e aceitam janela que zera a base

- **Onde:** `lgbm_temporal.py:63-78,93-96`.
- **Diz:** remove “NaN de lags”; toda janela positiva é aceita.
- **É:** janela 1 gera `rolling_std` todo nulo (`ddof=1`) e devolve zero linhas.
  `dropna()` global também remove missing preexistente de coluna alheia.
- **Custo:** seleção silenciosa, viés antes da imputação e base vazia para
  parâmetro formalmente válido.
- **Correção específica:** `dropna(subset=generated_required_columns)` ou
  preservação por padrão; rejeitar janela <2 para desvio amostral ou documentar
  `ddof=0`.

### 🟠 F17 — scorecard, bandas e lift publicam estados indefinidos como válidos

- **Onde:** `scorecard_builder.py:50-85`; `score_bands.py:37-71`;
  `curves_plotly.py:175-199`.
- **É:** coeficiente/WOE não finito produz pontos `NaN/Inf`; scores todos
  empatados devolvem DataFrame 0×0 sem schema; target de classe única recebe
  gráfico “Lift top-10% = 1,00x”.
- **Custo:** artefatos inválidos seguem para decisão e apresentação sem erro.
- **Correção específica:** finitude obrigatória; contrato explícito para score
  sem variação; exigir duas classes como `metrics_report` já faz.

### 🟠 F18 — três utilitários distribuídos têm defaults que negam seu propósito

- **Onde:** `data_quality_check.py:52-78,111-115`;
  `smart_sample.py:31-49`; `drift_detector.py:102-106`.
- **É:** PK com uma chave nula pode receber status global pass; arredondamento +
  `limit(n)` pode eliminar o estrato raro; `date_col` numérica entra na seleção
  automática e mede drift da própria coluna usada para separar coortes.
- **Custo:** sinal verde de integridade, amostra sem minoria e falso drift
  tautológico.
- **Correção específica:** nulidade zero para PK; alocação inteira que soma `n`
  e preserva estratos quando possível; excluir `date_col` da seleção automática.

### 🟠 F19 — instruções vivas ainda mandam usar o engine supersedido

- **Onde:** `.claude/rules/free-vs-trabalho.md:11` e
  `.claude/context/ambiente-free.md:6-7` contra `CLAUDE.md` e ADR-0005.
- **Diz:** publicar pelo engine `databricks-genie`/ADR-0002.
- **É:** ADR-0005 rejeitou esse engine porque transforma módulos em notebooks e
  quebra imports; o caminho vigente é `tools/publicar_free.py`.
- **Custo:** um agente que siga a regra específica escolhe exatamente o
  publicador já rejeitado.
- **Correção específica:** atualizar os dois documentos vivos para ADR-0005 e
  critério do ADR-0008.

### 🟠 F20 — a atualização no trabalho não remove helpers obsoletos

- **Onde:** `replicacao-trabalho.md:87-95,185-189` e checklist correspondente.
- **Diz:** recopiar arquivos alterados e conferir presença amostral.
- **É:** nenhum passo remove antigos `hub_snippets`, `hub_scripts`,
  `hub_prompts` ou `hub_padroes`; o publicador Free reconhece explicitamente que
  overwrite não apaga obsoletos.
- **Custo:** helper removido da fonte continua importável no trabalho.
- **Correção específica:** substituir atomicamente somente os quatro diretórios
  Hub-owned e conferir manifesto/hashes; preservar MCP e skills alheias.

### 🟡 F21 — o gate de README cria um “halo verde” sobre conteúdo não conferido

- **Onde:** `README.md:195-197,219,387`;
  `tools/validate_assistant.py:354-360,395-401`;
  `.assistant/README.md:232-235`; `tools/README.md:16-69`.
- **Diz:** “reprova se algum número colado divergir”.
- **É:** só 14 rótulos entram na allowlist; rótulo ausente é ignorado. O gate
  passou com `instrucoes=7085` no README e 7260 na execução, sem a linha de
  normas no bloco. O README raiz/runbooks ainda usam 64/71/7, enquanto o estado
  é 145/136/0/8/1. O README publicado ainda diz 11 notebooks sem Leitura; são
  77/0. `tools/README` ainda descreve 20 checks, 2/13 e 11 avisos.
- **Custo:** a documentação viva mais consultada parece certificada quando não é.
- **Correção específica:** uma estrutura de dados gera resumo, bloco do README e
  docs de status; falhar para toda linha numérica não coberta; um único dono do
  estado corrente.

### 🟡 F22 — os READMEs misturam guia estável, status e glossário em múltiplos donos

- **Onde:** `README.md` (425 linhas), `ambiente_fonte/.assistant/README.md`
  (522), `tools/README.md` (109) e READMEs de seção.
- **É:** os índices ajudam a navegar, mas fatos como contagens, gates,
  descoberta e limites são repetidos. O README de skills afirma que só skills
  são automáticas e que “uma skill não executa nada”, embora instruções e
  arquivos hierárquicos também sejam automáticos e o padrão admita scripts.
- **Custo:** alto custo de manutenção e onboarding; a deriva observada é efeito
  do desenho, não de uma frase isolada.
- **Correção específica:** landing page curta por tarefa; separar manual do
  contribuidor, manual do usuário, glossário e status gerado; referências em vez
  de repetir estado.

### 🟡 F23 — governança documental tem exceções não normatizadas

- **Onde:** `.claude/rules/docs-e-readmes.md`; ADR-0003, 0007 e 0008;
  `docs/auditoria/README.md`; `PLANO_HUB.md`; `CHANGELOG.md`.
- **É:** cadeia de supersessão está íntegra, mas a regra exige novo ADR para toda
  mudança enquanto 0007/0008 usam errata append-only; ADR-0003 é “Aceito” e
  “pendente de ratificação”; regra absoluta de README foi recusada sem ser
  atualizada; índice de auditorias diz que a rodada de leitura abriu o gate,
  contrariando PLANO e CHANGELOG. O PLANO ainda diz 22 checks/74 notebooks e
  mistura dívida fechada com decisão aberta.
- **Custo:** agentes honestos chegam a ações diferentes seguindo normas vivas.
- **Correção específica:** normatizar errata factual versus nova decisão;
  ratificar/superseder ADR-0003; regra “arquivo de entrada” com exceções; status
  corrente gerado.

### 🟡 F24 — pré-requisito da CLI está abaixo do mínimo oficial atual

- **Onde:** `README.md`, seção “Antes de começar”.
- **Diz:** CLI v0.200+.
- **É:** a documentação oficial atual trata 0.18 e inferiores como legada e
  orienta a CLI nova em **0.205+**.
- **Custo:** uma versão entre 0.200 e 0.204 pode ser apresentada como suportada
  sem estar no intervalo documentado.
- **Correção específica:** usar 0.205+ ou, melhor, linkar a página de instalação
  e testar os comandos necessários, não apenas a versão.

## 4. S1 — biblioteca: matriz e testes

| Grupo | Objetos | Revisão estática | Execução nesta rodada |
|---|---:|---|---|
| `constants` | 4 | API, formatação, dependências | indireta |
| `visual` | 6 | HTML, tema, escaping | backend visual ausente localmente |
| `display` | 3 | custo Spark/serverless | PySpark/Plotly ausentes localmente |
| `spark` | 7 | ações, cardinalidade, leakage | PSI puro + smoke real; probes Spark específicos não locais |
| `ml` | 30 | matemática, temporalidade, risco, integrações | temporal, vintage, scorecard, bandas, monitor e métricas puras |
| `testing.fixtures` | 1 | determinismo/semântica | estática |
| `hub_scripts` | 7 | DQ, drift, RFV, perfil, schema/docs | helper PSI/doc coverage; Spark específico por prova algébrica |
| **Total** | **58** | **58/58** | limites declarados, sem inventar execução |

`ast.parse` percorreu 182 arquivos Python dessa frente: zero erro. A execução
real do smoke cobriu imports e 136 casos; não substitui os known-answer tests.

| Prova de valor conhecido | Resultado |
|---|---|
| KS 0,5 no relatório | devolveu 50,0 |
| Monitor KS 40→39 | crítico; 0,40→0,39 saudável |
| Vintage cumulativo com MOB ausente | 50%→0%→50%, cobertura 100% |
| Temporal rolling window 1 | 0 linhas |
| Scorecard com não finito | pontos `NaN/Inf` |
| Score todo empatado | DataFrame 0×0 |
| Target todo zero no lift | figura “1,00x” |
| PSI em distribuições idênticas | 0,0 nos caminhos puros testados |
| Scorecard válido, evento=bad | direção de pontos e base preservadas |

Não foram contadas como achado suspeitas que exigiriam execução ausente de
SHAP, lifelines ou backend gráfico. A correção de Holm e os shapes SHAP atuais
foram inspecionados sem novo defeito confirmado.

## 5. S2 — ferramentas: matriz dos 23 checks

Todos os checks foram chamados diretamente em sandboxes temporários com uma
violação simples e um vizinho legítimo.

| # | Check | Violação simples | Limite comprovado |
|---:|---|---|---|
| 1 | frontmatter | detecta ausência de campo | vazio/YAML inválido/sem fechamento passa |
| 2 | tamanho de skill | 501 linhas → aviso | aviso deliberado |
| 3 | pycache | cache → aviso | adequado |
| 4 | Markdown | fence/link quebrado | não valida âncora |
| 5 | links de notebook | alvo ausente | apenas comentários/Markdown |
| 6 | AST Python | sintaxe inválida | adequado |
| 7 | tamanho das instruções | 20.001 → falha | adequado |
| 8 | higiene de texto | path pessoal no produto | só `.md`/`.py` e escopo parcial |
| 9 | higiene de path | identidade proibida | regex contextual, não exaustiva |
| 10 | pasta de objeto | `__init__` divergente | arquivo extra passa |
| 11 | pasta malformada | módulo errado com init | pasta sem init é invisível |
| 12 | contrato de dados | `out["ghost"]` | `select`, literal incidental e primeira célula passam |
| 13 | contrato de entrada | `f(bad=1)` | `mod.f(bad=1)` passa |
| 14 | saída colada | bloco curto | qualquer dígito/prosa longa parece “real” |
| 15 | sync do smoke | constante divergente | lógica oposta com constantes iguais passa |
| 16 | helpers de skill | path completo ausente | nove abreviados não entram |
| 17 | seções de skill | seção ausente | título vazio/infinitivo simula conteúdo |
| 18 | docstring PT-BR | frase inglesa típica | formulação inglesa alternativa passa |
| 19 | normas do molde | cache simples fora de try | 3 FNs e 1 FP confirmados |
| 20 | notebook exercita | só importa | homônimo `other.f()` passa |
| 21 | saída do README | rótulo divergente | linha/rótulo não allowlisted é ignorado |
| 22 | repo corporativo | sentinela conhecida | exclui congelado; não procura segredo/PII global |
| 23 | links do repo | alvo ausente | varredura vazia reprova corretamente |

Resultado do harness: 22/23 violações simples foram acusadas de primeira; a 23ª
só apareceu após mover o consumo para depois do primeiro marcador de célula.
Casos legítimos básicos passaram, com falsos positivos adicionais descritos em
F05–F07.

Outras ferramentas:

- render autorizado: `OK: 315`; SHA-256 sem divergência nos 314 publicáveis;
- rename remoto: obsoleto em arquivo e diretório foi detectado;
- API atual: 51 módulos/166 nomes em snippets + 7/10 em scripts, coerentes com o
  gerador atual; a alegação futura de API “exaustiva” não cobre tuple/block;
- tempo: validação local ~1,2–2 s; verify remoto ~30 s nesta rodada; otimizar a
  reexecução local economizaria pouco frente à rede.

## 6. S3 — produto/UX, colisões e forward tests

### Percurso real do analista

```text
pedido
  → instruções pessoais + contexto hierárquico
  → roteamento por descriptions das skills
  → corpo da skill e templates referenciados
  → helper importado manualmente no runtime
  → output durável
  → auditoria contra pedido + contrato produtor
```

Rupturas confirmadas: instruções conflitantes na entrada; prompts fora do molde;
helpers apenas recomendados, não executados automaticamente; output sem
proveniência suficiente no fim.

### Colisões de description

| Par | Ambiguidade | Estado |
|---|---|---|
| auditoria × tutor/comentar | revisão de notebook/relatório/código ampla demais | sem negativo específico |
| validação × monitoramento | drift, KS e distribuições | 04N/07N já passaram |
| monitoramento × safra | PSI/alerta versus “safra” | 13N pendente |
| baseline × feature engineering | scorecard versus WOE/IV | sem caso específico |
| pipeline × feature engineering | feature/scoring pipeline/materialização | 08N passou |
| auditoria × EDA | validar output versus produzir DQ/EDA | 12N passou |

### Três casos pendentes da Skill 13 — transcrição e previsão

1. **13P:** “Quero criar um snippet novo no Hub para calcular taxa de resposta
   de campanha. Qual é o formato e o que preciso entregar junto?”
   - Previsão: `hub-ml-criar-objeto`, alta confiança.
2. **13N:** “Como calculo o PSI entre a safra de janeiro e a de junho, e a
   partir de que valor devo me preocupar?”
   - Previsão: não criar-objeto; `monitoramento-modelo` > `analise-safra` >
     `validacao-estatistica`. Ideal declarado: monitoramento; safra é aceitável.
3. **13M:** “@hub-ml-criar-objeto qual template eu uso para um utilitário que
   recebe o nome de uma tabela e devolve um diagnóstico de qualidade?”
   - Previsão: criar-objeto, determinística pela menção.

Não foram executados: o orçamento do chat está documentado como bloqueado até
1º de setembro. As 16 partes 3 dos notebooks de prompt continuam sem resposta
real, de forma honestamente declarada; partes 1 e 2 em job não provam a qualidade
da resposta do Genie Code.

## 7. S4 — documentação, ADRs, CHANGELOG e dívida

### Cadeia de supersessão

| Relação | Origem avisa | Destino aponta de volta | Canônico roteia | Veredito |
|---|---:|---:|---:|---|
| ADR-0002 → 0005 | sim | sim | sim | íntegra |
| ADR-0004 → 0007 (local/forma) | sim | sim | sim | íntegra |
| ADR-0005 → 0008 (critério) | sim | sim | sim | íntegra |
| ADR-0006 complementa 0001/0004 | explícito | aplicável | sim | íntegra |

### Claims de 17–19/08

- confirmados por diff/execução: 50 blocos, 77/0, 15 docstrings, 13/13 skills,
  quatro normas instrumentadas e JSON 145/136/0/8/1;
- confirmado: WOE→scorecard foi documentado/exercitado, mas a ponte segue
  manual;
- o claim de 17/08 sobre banners dos ADRs foi falso no próprio commit e
  corrigido depois; o CHANGELOG admite a correção;
- claim residual falso: os 72 caminhos não eram todos snippets; eram 59
  snippets + 13 scripts;
- “60 de biblioteca” foi corrigido posteriormente para 58 + 2 exemplares.

### §12.1–§12.3

| Dívida | Estado auditado |
|---|---|
| §12.1 saídas coladas | fechada: 77/0 e 50 blocos |
| §12.2 cores/CSS | higiene fechada; paleta divergente e espelho morto seguem como decisão/dívida declarada |
| §12.3 cinco funções PT-BR | contagem coerente; compatibilidade explica não renomear, mas aliases ingleses preservariam API |

## 8. S5 — segurança e replicação

### Superfícies

| Camada | Rastreada | Bundle padrão | Publicada no Genie | Transportada por Git/ZIP |
|---|---:|---:|---:|---:|
| `Ambiente_Antigo/` | não | não | não | não |
| `Ajustes_Codex/` | 174 | não | não | sim |
| `ambiente_fonte/` | 315 | sim | via espelho | sim |
| `Novo_Ambiente_Simulado/` | 315 | não | conteúdo, sem path local | sim |
| `docs/testes/forward/` | sim | sim | não | sim |
| `.claude/context/` | sim | sim | não | sim |

A quarentena de `Ambiente_Antigo/` funciona: zero path rastreado, sem symlink ou
submódulo apontando para fora. Busca dirigida no tree atual encontrou zero token
ou chave privada comum. Isso não substitui secret scanner: sentinelas inofensivas
de formatos conhecidos passaram pela regex atual, e não há Gitleaks/TruffleHog.

### Gaps Free → trabalho

| Dimensão | Free | Trabalho/runbook | Lacuna |
|---|---|---|---|
| Completude | verify de arquivo/tipo/obsoleto | presença amostral | faltantes/obsoletos passam |
| MCP | preservado | removido | perda de configuração |
| Skills alheias | não geridas | pasta inteira removida | perda funcional |
| MLflow | bloqueio esperado | mesmo oráculo | falso positivo/run residual |
| Transporte | só subárvore publicada | clone/ZIP do repo | PII e congelado chegam |
| Roteamento | 36/39 | exemplos avulsos | sem gate equivalente |
| Rollback | — | backup de arquivos | não cobre run criado pelo teste |

## 9. As 12 decisões contestáveis

| # | Decisão | Juízo desta rodada |
|---:|---|---|
| 1 | regra de idioma alterada | **aprovar** constante de domínio; reflete a API real |
| 2 | cinco funções PT-BR não renomeadas | **aprovar parcialmente**: não quebrar; criar aliases ingleses/depreciação |
| 3 | sem guarda de idioma de identificadores | **rejeitar**: allowlist das cinco legadas evita uma sexta sem classificador linguístico |
| 4 | `styles` como espelho morto | **aprovar só como transição**: deprecar/remover após mapear consumidor externo |
| 5 | três guardas promovidas sem observação | **rejeitar a confiança atual**: mutation tests mostram proxies fracos |
| 6 | `check_normas` cobre quatro | **rejeitar o rótulo**: endurecer as quatro e dizer “4 automatizadas” antes de ampliar |
| 7 | WOE→scorecard documentado, não integrado | **rejeitar como fechamento**: adapter limitado e teste de composição |
| 8 | detector estrutural de fluxo | **rejeitar** como evidência de completude; infinitivos arbitrários passam |
| 9 | “O que nunca fazer” sem teste | **rejeitar**: presença de título não prova obediência |
| 10 | username forward não parametrizado | **rejeitar**: 44 PII + não portável |
| 11 | errata append-only em ADR-7/8 | **aprovar para fato**, mas normatizar; mudança de decisão exige ADR novo |
| 12 | bundle exclui derivado/congelado | **aprovar só no modo canônico**; segurança/forense exigem paths completos |

## 10. Classe nova de defeito

### Gate de propriedade substituída

O instrumento mede uma representação conveniente, mas que **não preserva a
propriedade operacional prometida**:

- número de diretórios em vez de identidade/validade das skills;
- ocorrência de string em vez de coluna/chave realmente produzida;
- qualquer exceção em vez da assinatura do bloqueio esperado;
- constantes iguais em vez de implementação igual;
- bytes iguais em vez de superfície de path/metadata igual.

Ela difere de “contradição entre artefatos”: cada lado pode concordar e ainda
assim medir a coisa errada. O antídoto é escrever primeiro o invariante em forma
de propriedade — nomes esperados, categorias que reconciliam, erro com classe e
mensagem, path contido — e só depois escolher o proxy.

O efeito secundário é o **halo verde**: um gate parcial aprovado transfere
credibilidade para números e frases adjacentes que nunca entraram na medição.

## 11. Três ações primeiro

1. **Conter risco externo antes de qualquer replicação.** Bloquear host/profile
   errado; corrigir runbook para preservar MCP e skills alheias; separar smoke
   Free/trabalho; parametrizar/sanitizar PII.
2. **Corrigir as três falhas analíticas de maior impacto e testar costuras.**
   Vintage com invariantes de cobertura/monotonicidade; unidade canônica de KS;
   diagnóstico reconciliável do `pit_join`. Em seguida, known-answer tests para
   scorecard/bandas/lift/temporal.
3. **Trocar selos por contratos executáveis e reduzir donos documentais.** YAML
   real e nomes exatos de skills; AST semântico; oráculos por assinatura;
   manifesto/hash; PII/secret scan; status/contagens gerados; prompts alinhados
   ao molde e outputs com proveniência.

Até essas três frentes, a recomendação é: **não replicar no workspace do
trabalho e não usar o selo verde como evidência de corretude matemática**.

## Fontes oficiais conferidas em 2026-08-20

- [Agent Skills no Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções customizadas do Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Contexto e prompts no Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [MCP no Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp)
- [Databricks CLI](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/)
- [Agent Skills specification](https://agentskills.io/specification)
