# Workflows — verificações automáticas e receitas manuais

Esta pasta define as verificações executadas pelo GitHub Actions. É documentação
para quem mantém o repositório. Copiar os YAMLs para um computador não executa CI;
os eventos configurados precisam ocorrer num repositório GitHub com Actions
habilitado. A pasta não integra o produto instalado no Databricks.

Inventário conferido em 07/10/2026, na base `8dd8da57`: **20 workflows, oito com
eventos automáticos e 12 somente manuais**. Os YAMLs são a fonte de verdade dos
comandos, versões, filtros e condições. Este README explica o propósito de cada um.

## O que fazer conforme sua necessidade

| Necessidade | Rota |
|---|---|
| Entender uma falha no PR | abrir o job que falhou, identificar o primeiro comando com erro e consultar a tabela abaixo |
| Validar uma alteração local | seguir [tools](../../tools/README.md) e executar os gates afetados |
| Entender geração e dependências do CI | consultar [CI por ambiente](../../docs/manutencao/saida-gerada.md#ci-por-ambiente) |
| Gerar pacote de instalação | workflow de kit ou [runbook](../../docs/playbooks/replicacao-trabalho.md), com o alcance autorizado |
| Avaliar redução do CI | consultar a [análise de manutenção](../../docs/manutencao/analise-faxina-2026-10-07.md) antes de retirar verificações |

Um workflow é uma receita; um job é uma execução dentro dela; um check é o
resultado apresentado ao PR. Um único workflow pode produzir vários checks.
`push` reage a envio de commits, `pull_request` a eventos de PR e
`workflow_dispatch` oferece execução manual. Branches, paths e condições de job
podem limitar o disparo ou a execução. Referência: [GitHub Actions — workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).

## Nomes humanos e compatibilidade

Os rótulos em negrito abaixo explicam o propósito para leitura deste índice.
Os nomes técnicos dos arquivos e checks continuam os mesmos. São identidades
consumidas pelo compilador, testes e certificadores históricos; não são apenas
nomes de apresentação. "Vxx" identifica a campanha de origem, não uma versão
obrigatória do runtime ou o único alcance do teste.

A cobertura documental foi reconferida contra os 20 YAMLs nesta revisão: cada
arquivo tem finalidade, disparos e alcance, complementados por perfis/efeitos.
Renomear arquivos ou títulos YAML é uma migração própria, descrita no
[plano de organização](../../docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md).

## Os oito workflows automáticos

| Arquivo e check principal | Quando roda | O que protege e por que manter |
|---|---|---|
| **CI integrado** — [ci.yml](ci.yml): `validar` e jobs de Temas | todos os PRs; push em `main` e `codex/temas-v*` | gate local agregado, instruções IA, estrutura e regressões; cinco perfis comuns e 12 jobs derivados. É o ponto central da manutenção |
| **Pacote para o trabalho** — [kit-transicao-trabalho.yml](kit-transicao-trabalho.yml): `preparar` | manual; PR com filtros; push em `main` com filtros | prepara e testa o pacote extraído, contratos Spark local e integração temática do ZIP. Manter enquanto houver distribuição |
| **Regressões de Micromodelos** — [micromodelos-mm01-ci.yml](micromodelos-mm01-ci.yml): `validar-mm01` | todos os PRs; push em `main` e `micromodelos/mm01-*` | descobre `test_micromodelo*.py` e aceite do pacote de Micromodelos. O nome MM01 é histórico: o alcance atual é maior |
| **Contratos de skills** — [skill-enforcement-se01.yml](skill-enforcement-se01.yml): `se01` | PR e push em `main`, com filtros | contratos estruturados, regressão SE01, render e snapshot README; publica artifact da skill renderizada |
| **Certificação local de skills** — [skill-enforcement-se02.yml](skill-enforcement-se02.yml): `se02` | PR com filtros nos eventos opened/reopened/synchronize/ready_for_review; push em `main` com filtros | certificação reproduzível do perfil SE02 e artifacts de evidência/preflight. Em PR draft o job é pulado pela condição explícita |
| **Schema e contrato temático** — [temas-v01-ci.yml](temas-v01-ci.yml): `contrato` | todos os PRs; push em `main` e `codex/temas-v01` | schema e contrato central de temas, documentação derivada e testes negativos |
| **Núcleo da biblioteca temática** — [temas-v02-ci.yml](temas-v02-ci.yml): `nucleo` | todos os PRs; push em `main` e `codex/temas-v02` | resolução e API do núcleo, compatibilidade com contrato V01 e exemplo sintético |
| **Gráficos Plotly** — [temas-v03-ci.yml](temas-v03-ci.yml): `plotly-v03` | PR com filtros; push em `main` e `codex/temas-v03` | adaptador Plotly, compatibilidade visual e regressões dos contratos anteriores |

Os filtros de kit/SE01/SE02/V03 abrangem, entre outros, `tools/**`,
`ambiente_databricks/**`, `.github/workflows/**` e `docs/ai/**`. Alguns repetem paths
específicos já abrangidos pelos globs; isso pode ser simplificado mantendo a
mesma seleção de eventos. Consulte o YAML para a lista completa.

SE01/SE02 usam Python 3.11. Micromodelos e Temas usam Python 3.12. O kit usa
Python 3.11 e 3.12 em PR; push/manual usam 3.11. Seu perfil inclui Spark 4.0.1
e Java 17. Esses ambientes têm finalidades distintas: aprovação num perfil não
substitui automaticamente o outro.

## As 12 receitas manuais de Temas

Todos os arquivos abaixo possuem apenas `workflow_dispatch` como trigger próprio.
**Continuam sendo consumidos pelo CI automático**: `tools/ci_workflows.py` lê suas
receitas para compor jobs em `ci.yml`. Excluí-los hoje quebra essa geração.

| Receita / check preservado | Cobertura específica | Comando focal ou resultado |
|---|---|---|
| **Baseline e preservação visual** — [temas-v00-ci.yml](temas-v00-ci.yml) / `testar-v00` | inventário visual, proteção do legado e confiabilidade da baseline | `test_inventario_visual.py`, `test_visual_legado_v00.py`, `test_baseline_visual_runner.py` |
| **HTML e tabelas** — [temas-v04-ci.yml](temas-v04-ci.yml) / `html-v04` | componentes HTML e tabelas | `tools/tests/test_temas_v04.py` |
| **Laboratório de temas em notebook** — [temas-v05-ci.yml](temas-v05-ci.yml) / `visual-lab-v05` | Visual Lab, sessões e widgets | `test_temas_v05.py --require-ipywidgets` e `test_temas_v05_sessions.py`; exige widgets |
| **Geração determinística de assets** — [temas-v06-ci.yml](temas-v06-ci.yml) / `assets-v06` | compositor visual, assets e determinismo | `tools/tests/test_temas_v06.py`; Node/pnpm e seed fixo |
| **Consumidores e formatos** — [temas-v07-ci.yml](temas-v07-ci.yml) / `consumidores-v07` | consumidores, formatos e invariância dos dados | descoberta `test_temas_v07*.py` |
| **Integração entre coleções** — [temas-v08-ci.yml](temas-v08-ci.yml) / `transversal-v08` | alinhamento entre skills, padrões, Manual e Temas | `test_temas_v08.py`; guarda de proibição de delta runtime apenas nas condições da campanha V08 |
| **Temas no pacote de distribuição** — [temas-v09-ci.yml](temas-v09-ci.yml) / `kit-temas-v09` | integridade do contrato temático na distribuição | testes V09/transição; gera `.artifacts/v09-kit` e confere o ZIP |
| **App de gestão visual** — [temas-v10-ci.yml](temas-v10-ci.yml) / `databricks-app-v10` | autoria visual, identidade, persistência e bundle do App | testes V10, sintaxe Python e build/verify em `.artifacts/v10-app`; não faz deploy |
| **Tema nativo AI/BI** — [temas-v11-ci.yml](temas-v11-ci.yml) / `aibi-v11` | projeção de tema para AI/BI e suas limitações | testes V11 e sintaxe de `aibi_theme.py`; sem chamadas ao Databricks |
| **Contrato de homologação** — [temas-v12-ci.yml](temas-v12-ci.yml) / `homologacao-v12` | protocolo de evidência e guardas de jornadas | testes V12 e evidência versionada; escopo estrito/higiene conforme condições do YAML |
| **Operação, release e rollback** — [temas-v13-ci.yml](temas-v13-ci.yml) / `contrato-operacional-v13` | preflight, release/rollback simulados, diagnóstico, compatibilidade, ensaios e handoff | testes S1–S7 e validador operacional; runner Ubuntu 24.04 |
| **Ownership e readiness** — [temas-v14-ci.yml](temas-v14-ci.yml) / `readiness-v14` | freeze histórico, ownership e autoridade operacional | testes S0/S1 e `temas_v14_ownership.py --check`; não decide go-live |

Além do teste focal, essas receitas incluem preparação, validação e regressões
cumulativas. Rodar apenas o comando da última coluna ajuda no diagnóstico, mas
não reproduz o workflow inteiro. Nomes de etapas como “V01–V06” podem ser
históricos: o glob `test_temas*.py` alcança os testes presentes no checkout atual.

## Como o CI central reaproveita as receitas

O grafo de dependências de jobs é chamado de DAG. No desenho vigente, cinco
perfis executam as suítes comuns e os jobs derivados exigem sucesso do perfil
correspondente antes de verificar sua receita específica:

| Perfil comum em ci.yml | Ambiente | Jobs que dependem dele |
|---|---|---|
| `validar` | Python 3.12, sem Spark, Node/pnpm; `ci_local.py` | V00, V04 |
| `temas-widgets` | widgets obrigatórios, sem seed configurado | V05 |
| `temas-widgets-seeded` | widgets e `SOURCE_DATE_EPOCH=1700000000` | V06, V07, V08, V09 |
| `temas-widgets-app` | widgets, dependências App, seed; `ubuntu-latest` | V10, V11, V12 |
| `temas-widgets-app-24` | widgets, dependências App, seed; `ubuntu-24.04` | V13, V14 |

Os 12 jobs derivados usam `always()` e um teste explícito do resultado upstream.
Assim, falha, cancelamento ou skip da suíte comum não vira aprovação silenciosa.
O gerador conserva os nomes dos checks e remove uma receita cumulativa duplicada
por job. O contrato e os negativos estão em
[ci_workflows.py](../../tools/ci_workflows.py) e
[test_ai_ci_workflows.py](../../tools/tests/test_ai_ci_workflows.py).

O trecho de `ci.yml` após `BEGIN GENERATED CAMPAIGN JOBS` é gerado. Para uma
mudança autorizada nas receitas, regenere pelo comando `python tools/ci_workflows.py --write`
e confira com `python tools/ci_workflows.py --check`. Não mantenha uma
segunda versão manual do trecho compilado.

## Artefatos, efeitos e limites

- O kit sobe um artifact de teste por versão Python em PR e o artifact
  `kit-transicao-trabalho` em push/manual. Produzir o ZIP não o instala no destino.
- SE01 sobe `se01-skill-renderizado`; SE02 sobe `se02-certification-evidence`
  (retenção de 14 dias) e `se02-preflight-renderizado` (7 dias).
- V09 e V10 geram e verificam pacotes no runner. A geração local não equivale a
  upload de artifact; seus YAMLs não contêm `upload-artifact` próprio.
- Os workflows declaram `contents: read`. Instalam dependências e gravam saídas
  temporárias no runner; não contêm etapa de publicação do Hub no Databricks.
- Echo de um resultado histórico, como validação humana, não executa uma nova
  sessão humana. Teste de evidência versionada prova somente seu contrato.
- A reprodução local depende de Python, Node/pnpm e, conforme o perfil,
  widgets/App ou Spark/Java. Comandos Bash de CI não são scripts PowerShell.

## Manter, reduzir ou remover

**Recomendação:** manter a cobertura de regressão e distribuição; simplificar a
orquestração em uma mudança própria. Uma funcionalidade concluída ainda pode
quebrar depois de atualização de dependências, refatoração ou geração de pacote.

No computador do trabalho, um checkout de manutenção pode conservar esta pasta;
o payload Databricks já a exclui. Um pacote reduzido para uso precisa de manifesto
e verificações próprias, porque as ferramentas atuais pressupõem checkout completo.

Antes de consolidar/remover um workflow:

1. Mapear comandos, ambientes, artifacts e condição de sucesso para um sucessor.
2. Consultar required checks/rulesets do repositório que receberá a mudança.
3. Atualizar gerador, seus testes e chamadas de certificadores atuais; preservar
   pins históricos e a rota de reprodução na revisão original.
4. Demonstrar que falhas dos testes afetados continuam reprovando o sucessor.
5. Comparar custo e duração em PR estreito e mudança de produto; só então ajustar
   filtros. Não confundir redução de arquivos YAML com redução de trabalho executado.

Em 07/10/2026, a consulta ao repositório de origem retornou `main.protected=false`,
lista vazia de rulesets e HTTP 404 `Branch not protected` para required status
checks. Isso descreve a consulta desta data, não a política do repositório corporativo.

Para recuperar uma remoção, reverta a mudança junto com gerador/testes e confira
novamente o grafo. Detalhes da proposta estão no
[plano por sprints](../../docs/manutencao/plano-faxina-2026-10-07.md).
