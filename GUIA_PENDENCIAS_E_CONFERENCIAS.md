# Guia de pendências e conferências do projeto

> Ponto de retomada em **11/09/2026**. Este documento registra o que já existe,
> o que ainda falta comprovar e a ordem recomendada de fechamento. Não é um
> certificado de publicação nem de homologação no ambiente de trabalho.

O procedimento completo de transferência e a especificação dos futuros
notebooks estão no [Plano de transferência e testes](PLANO_TRANSFERENCIA_E_TESTES_DATABRICKS_TRABALHO.md).
Este guia é a lista de trabalho; o outro documento explica como executar cada
etapa com segurança.

## 1. Onde o trabalho parou

As novas figuras e os cabeçalhos aprovados foram integrados à arquitetura local.
O usuário assumirá a continuação da publicação por outra LLM/modelo. **Não é
necessário redesenhar os READMEs nem gerar novamente as imagens para retomar.**

| Frente | Situação observada | O que falta |
|---|---|---|
| Evolução visual v2 | Integrada localmente; 21 diagramas e 2 cabeçalhos compartilhados | Conferência visual final na interface do Databricks |
| Arquitetura visual | Fontes, PNGs, contratos, licenças, transcrição e QA em `hub_readmes_visual_assets/` | Confirmar a mesma estrutura no destino |
| Preservação editorial | Seis READMEs físicos mantêm sua hierarquia; 23 ocorrências de diagramas | Aceite de leitura do usuário no destino |
| Cabeçalho CRM | Integrado aos seis READMEs físicos | Conferir renderização, tamanho e legibilidade |
| Cabeçalho Squad | Disponível no pacote, sem aplicação em massa a notebooks | Testar seu uso em notebook dedicado |
| Integridade local | QA visual e regressões locais aprovados na rodada de integração | Repetir os gates sobre a versão que será congelada |
| Publicação visual | Log chegou a 103/103 envios com conferência RAW individual | Nova verificação final do conjunto; recibo anterior não concluiu |
| Git | Há alterações staged, unstaged e arquivos novos; sem commit/push desta integração | Revisar, versionar o escopo aprovado e conferir o remoto Git |
| Homologação corporativa | Não realizada | Executar o plano no workspace de trabalho |
| Futura suíte `testes/` | Especificada no documento complementar | Implementar somente em uma próxima etapa autorizada |

**Cinco sprints documentais não significam cinco arquivos físicos:** a frente
superior inclui o README do repositório e o README do `.assistant`; as outras
quatro cobrem snippets, scripts, skills e prompts. Na publicação visual entram
cinco READMEs de uso no workspace, além de toda a árvore de assets. O README do
repositório não é um sexto README a instalar na raiz do usuário.

### 1.1 O estado exato da publicação interrompida

O processo foi interrompido por solicitação de mudança de escopo do usuário.
O terminal registrou:

```text
envio e verificação RAW: 103/103
aposentadoria: conferência individual dos legados com backup
verificação final: inventário e bytes do escopo completo
```

O recibo local permaneceu com `status: started`. Portanto:

- houve envio dos 103 arquivos e conferência individual de seus bytes;
- a rotina alcançou a fase de conferência final;
- **não existe nesse recibo uma certificação final `verified`**;
- a situação dos 12 assets legados deve ser reconferida; não inferir sua
  ausência apenas pelo log de entrada da fase;
- não afirmar que a publicação não começou, nem que terminou certificada.

Evidência local privada, ignorada pelo Git:

```text
.artifacts/visual-v2/publication/
└── 20260911T111747.590144Z_execute_92804/
    ├── receipt.json
    └── remote-backup/
        ├── manifest.json
        └── blobs/
```

O recibo registra baseline `f5461d866fd6dd19fc921674ca059e8ccc9ae78f`,
`scope_dirty: true` e hash RAW do escopo
`a548b02cd66758fd4963318fdbf2aca75d163c57fa503926111b2a67b8d99e41`.
Esse hash identifica o escopo daquela execução, **não o ZIP completo de implantação**.
Não transportar o backup remoto ou credenciais com o pacote do produto.

## 2. Ordem de fechamento recomendada

```text
Conferir estado local e remoto
             ↓
Fechar o aceite visual e documental
             ↓
Revisar mudanças e congelar uma versão Git
             ↓
Preparar e testar o pacote mínimo de transporte
             ↓
Implementar a suíte de testes planejada
             ↓
Transferir, instalar em piloto e homologar no trabalho
             ↓
Liberar para a equipe e, depois, avaliar remoção dos protótipos
```

### P1 — Encerrar a conferência da publicação visual

**Responsável:** pessoa/LLM que assumirá a CLI na máquina de origem.

1. Ler `tools/readme_visuals/README.md` e o recibo citado acima.
2. Confirmar profile e host do laboratório, sem copiá-los para documentos
   versionados. Não usar o destino de trabalho por engano.
3. Começar por **verificação**, não por nova publicação:

```powershell
.\.venv\Scripts\python.exe tools/readme_visuals/publish_production.py --verify --profile "PERFIL_FREE" --expected-host "https://HOST_FREE"
```

Substituir os dois valores em maiúsculas pelos valores locais corretos. O
comando não modifica o workspace, mas reexecuta QA e grava evidência local.
Se a CLI não estiver no `PATH`, resolver a instalação/caminho existente; não
reconfigurar credenciais nem instalar outra CLI indiscriminadamente.

4. Exigir novo recibo com `status: verified`, inventário completo, ausência dos
   legados conhecidos e comparação RAW de todos os arquivos do escopo.
5. Se houver divergência, identificar primeiro se é arquivo ausente, conteúdo
   alterado, tipo incorreto ou edição concorrente. Preservar evidência antes de
   decidir reenviar. O publicador não faz rollback automático.
6. Somente quando a divergência for compreendida, retomar o procedimento de
   execução documentado no publicador, com o escopo já autorizado pelo usuário.
   Não usar exclusão recursiva da pasta `.assistant`.

**Aceite:** recibo final válido e nenhuma divergência inexplicada. Os 103
arquivos são o escopo visual observado nesta rodada, não o total do produto.

### P2 — Conferir o produto inteiro, não apenas as figuras

O publicador visual não certifica skills, instruções, módulos ou notebooks fora
de seu escopo. Para fechar a origem, usar também o verificador completo:

```powershell
.\.venv\Scripts\python.exe tools/publicar_free.py --verify --conteudo --profile "PERFIL_FREE" --expected-host "https://HOST_FREE" --relatorio ".artifacts/verify-produto-fechamento.json"
```

Conferir contagens, nomes, tipos `FILE`/`NOTEBOOK`, conteúdo e obsoletos. A
normalização de fonte de notebook prevista nesse verificador é diferente da
comparação RAW das imagens. Um verificador rápido de contagens não substitui
essa conferência aprofundada.

**Aceite:** todos os itens do manifesto corrente cobertos. Não reutilizar o
total histórico de 316 arquivos: ele antecede a integração visual atual.

### P3 — Fazer o aceite visual dentro do Databricks

- [ ] Abrir `.assistant/README.md`, `hub_snippets/README.md`,
  `hub_scripts/README.md`, `skills/README.md` e `hub_prompts/README.md`.
- [ ] Confirmar preview Markdown, imagens carregadas e links navegáveis.
- [ ] Verificar os 21 diagramas únicos e as ocorrências compartilhadas.
- [ ] Ler sem zoom extremo: textos não podem ficar cortados ou pequenos demais.
- [ ] Conferir que setas, legendas e agrupamentos não sugerem execução automática
  dos helpers ou descoberta nativa das pastas `hub_`.
- [ ] Verificar CRM com o texto aprovado e sem a palavra “Área”.
- [ ] Conferir o cabeçalho Squad no futuro notebook de validação visual.
- [ ] Confirmar equivalentes textuais e ausência de dependência de Mermaid.
- [ ] Registrar eventuais ajustes pontuais; preservar didática, títulos e
  subtítulos aprovados. Não iniciar outro redesenho global.

**Aceite:** aprovação humana da renderização. Hash correto comprova transporte,
mas não comprova legibilidade na interface.

### P4 — Fechar Git e uma versão de entrega reproduzível

Há mudanças de sessões anteriores no worktree. Antes de versionar:

```powershell
git status --short
git diff --stat
git diff --cached --stat
git diff --check
```

Revisar alterações staged e unstaged separadamente. Incluir explicitamente os
arquivos novos de autoria, manifestos, fontes e ativos aprovados. Não usar
`git add .` sem inventário e revisão. Não limpar alterações de outras LLMs.

Reexecutar os gates locais na versão candidata:

```powershell
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
.\.venv\Scripts\python.exe tools/ci_local.py
.\.venv\Scripts\python.exe tools/readme_visuals/tests/test_publish_production.py
node tools/readme_visuals/validate_production.mjs
.\.venv\Scripts\python.exe tools/render_simulado.py --write
.\.venv\Scripts\python.exe tools/validate_assistant.py --conferir-readme
```

O renderer é a única forma permitida de atualizar o simulado. O validador
visual gera/atualiza seus relatórios locais; revisar também essas saídas antes
do commit. Se uma contagem documental mudar, usar o diagnóstico do gate para
atualizar sua fonte, não alterar um número apenas para obter aprovação.

Após revisão, commit e push do escopo aprovado devem ser conferidos de forma
explícita. Registrar o hash final e comparar `HEAD` com a branch remota após
atualizá-la por `git fetch`. “Commitado”, “enviado ao Git” e “publicado no
Databricks” são três estados distintos.

**Aceite:** fonte e derivado sem alterações pendentes relativas à release,
artefatos novos incluídos e commit remoto confirmado. Não usar
`bundle_implantacao.py --allow-dirty` como entrega homologada.

### P5 — Resolver pendências documentais operacionais

Estas correções são backlog identificado; os documentos antigos não foram
reescritos nesta entrega:

| Documento/ponto | Ajuste a realizar |
|---|---|
| Bloco de saída de validação no `README.md` raiz | A inclusão destes documentos altera a contagem de links do repositório. Recolher a saída real e atualizar o bloco ao consolidar a release; nesta entrega o README foi preservado |
| `docs/playbooks/replicacao-trabalho.md` | Backup misto por ZIP Source, não DBC; cinco diretórios `hub_`; atualizar estado dos 13 forward tests; retirar promessa de seleção determinística |
| `docs/playbooks/checklist-replicacao.md` | Alinhar ao novo plano e ao manifesto da release antes da execução |
| `docs/handoffs/2026-09-10_evolucao-visual-v2.md` | Acrescentar fechamento futuro da publicação e aceite; não apagar relato histórico |
| `ambiente_fonte/.assistant/CATALOGO_HELPERS.md` | Conferir resumo de runtime: há referência histórica de 145 verificações, anterior ao resultado de 09/09 |
| `requirements-optional.txt` e notas de ambiente | Tratar pins e limitações antigas como observações datadas; produzir combinação homologada no trabalho |
| `tools/spark_smoke_test.py` | Na futura adaptação, revisar rótulo fixo `serverless`, saída visual truncada e propagação de falha; não supor que execução verde do notebook = todos os casos aprovados |
| Retomada do publicador visual | Melhorar futuramente o registro de interrupção: `KeyboardInterrupt` deixou o recibo `started`; não corrigir recibo antigo à mão para simular conclusão |

As correções de transporte deste guia e do plano complementar prevalecem sobre
as instruções operacionais antigas conflitantes. Registros históricos de
execução devem continuar datados, sem serem reescritos como resultado atual.

### P6 — Implementar e executar os testes que ainda faltam

O [plano complementar](PLANO_TRANSFERENCIA_E_TESTES_DATABRICKS_TRABALHO.md)
define notebooks, fixtures, gates, saídas esperadas e sprints de implementação.
As prioridades são:

1. Integridade do ZIP, importação mista e instalação com tipos corretos.
2. Cobertura funcional dos sete scripts, incluindo `naming_checker` e
   `doc_coverage`, não chamados funcionalmente no smoke corrente.
3. Cobertura explícita dos objetos de snippets; import não basta para certificar
   função, dependência tardia, treino ou resultado visual.
4. Nova execução do smoke no runtime escolhido para o trabalho; MLflow com
   contrato de trabalho e autorização de escrita, não com bloqueio esperado do Free.
5. Roteamento das 13 skills no destino, mais avaliação da qualidade das respostas.
6. Rodada comparável dos 16 prompts, hoje sem certificação conversacional comum.
7. Permissões, limpeza, rollback e piloto com um segundo usuário autorizado.

**Aceite:** evidências do destino e nenhum item obrigatório sem resultado. Não
contar `OPTIONAL_MISSING`, `BLOQUEADO` ou “não executado” como `PASS`.

### P7 — Limpeza das pastas temporárias, somente depois

`READMEs_refeitos/` e suas subpastas guardam propostas e aprovações históricas.
O usuário pretende excluí-las no futuro, mas a limpeza não faz parte desta
entrega. Antes de removê-las:

- provar que a geração normal depende apenas das fontes canônicas;
- conferir que imagens, fontes, licenças e aprovações foram preservadas;
- garantir que há versão Git recuperável;
- obter aceite de publicação e de apresentação;
- remover apenas os alvos explicitamente aprovados e atualizar referências.

Não remover `.artifacts/` indiscriminadamente: o backup da publicação
interrompida pode ser necessário até o fechamento remoto.

## 3. O que já foi comprovado — e o limite da comprovação

| Evidência | Resultado registrado | Não comprova |
|---|---|---|
| QA visual local da integração | 8.154 verificações; zero falhas | Renderização final no navegador do usuário |
| Dois renders independentes | 44 SVG/PNG comparados byte a byte | Configuração ou permissões do workspace |
| Assinaturas e cabeçalhos aprovados | Cinco diagramas e dois cabeçalhos com hashes preservados | Aceite de todas as páginas publicadas |
| Auditoria global local | 312 arquivos de produto fora dos READMEs/assets iguais ao baseline; links e hierarquia conferidos | Funcionamento no runtime corporativo |
| Regressões locais | 45 testes da biblioteca, 35 das ferramentas existentes, 29 do publicador visual | Spark/Genie Code no trabalho |
| Smoke de 09/09 no Free | 146 casos: 137 PASS, zero FAIL, oito opcionais ausentes, um bloqueio esperado | 146 helpers; aprovação integral de todas as dependências |
| Forward tests acumulados | 39/39 casos de roteamento das 13 skills | Qualidade de toda resposta ou teste dos 16 prompts |

Fontes locais: [smoke vigente](docs/testes/spark/README.md),
[forward tests](docs/testes/forward/README.md),
[fechamento de 09/09](docs/testes/2026-09-09_fechamento-codex.md),
[plano visual](docs/sprints/2026-09-10-evolucao-visual-v2.md) e
[changelog](CHANGELOG.md).

## 4. Checklist de encerramento para a próxima pessoa/LLM

- [ ] Conferi o estado real, sem assumir que o resumo antigo continua atual.
- [ ] Preservei alterações preexistentes e não editei o simulado à mão.
- [ ] Obtive recibo final da publicação visual e conferência completa do produto.
- [ ] Registrei o aceite visual na interface.
- [ ] Fechei a release em commit e conferi o push, sem incluir dados privados.
- [ ] Atualizei as instruções operacionais conflitantes antes de segui-las.
- [ ] Gerei ZIP mínimo íntegro e aprovado para transporte corporativo.
- [ ] Implementei os notebooks somente após autorização, seguindo o plano.
- [ ] Registrei resultados reais do destino e pendências por capacidade.
- [ ] Mantive histórico de migração fora dos READMEs de apresentação da equipe.
- [ ] Não apaguei protótipos ou backups antes do aceite e da autorização.

**Fechamento desta entrega documental:** foram pedidos dois documentos Markdown.
Não foi solicitado criar notebooks, enviar e-mail, fazer upload, publicar,
commitar ou executar testes no ambiente do trabalho nesta etapa.

Validação desta entrega: `tools/validate_assistant.py` aprovado, com zero
falhas e zero avisos. A conferência adicional `--conferir-readme` exige atualizar
a contagem colada no README raiz, que mudou pela inclusão dos documentos;
isso ficou registrado como pendência editorial, sem alterar o README nesta etapa.
