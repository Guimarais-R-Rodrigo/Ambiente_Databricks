# Organização da raiz, workflows e ferramentas — 07/10/2026

Owner: Codex. Baseline `09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd`, após merge
PR #128. Branch `codex/organizacao-tools-20261007`. Pedido: executar documentação
clara e preparar plano para decisões de estrutura/nomenclatura. Este lote não
move executáveis, modifica YAMLs, troca hashes históricos ou altera o produto.

## Conclusão e decisão por arquivo da raiz

| Arquivo | Necessário hoje? | Evidência e consequência | Encaminhamento |
|---|---|---|---|
| [PLANO_HUB.md](../../PLANO_HUB.md) | Sim, como referência histórica e registro da decisão da paleta | AGENTS cita §2.2; validador explica essa exceção; índices de sprints/auditoria e documentos fechados têm referências | Manter por ora. Seu localizador já distingue história de estado atual. Planejar extração da decisão vigente e arquivamento do corpo; não apagar |
| [.gitattributes](../../.gitattributes) | Sim | `git check-attr` confirmou texto/LF nos arquivos de manutenção e `-text/-diff` no PNG; histórico registra divergência CRLF/LF entre plataformas | Manter na raiz, onde a política alcança o checkout; remoção pode alterar bytes, hashes e diffs |
| [.gitignore](../../.gitignore) | Sim | `git check-ignore --no-index` reconheceu nomes sintéticos de `.env`, `.artifacts`, venv, dependências Node e quarentena | Manter. Evita adicionar esses arquivos por rotina; não protege arquivos já rastreados, não é criptografia/ACL e não substitui filtros do renderer/bundle |

A inspeção da quarentena restringiu-se à regra Git e a um nome sintético; nenhum
conteúdo privado foi lido ou exposto. Estes arquivos não são lixo de construção.
O plano não importa o estado antigo do Hub como instrução de trabalho atual.

## Workflows: documentação e nomes

O [README](../../.github/workflows/README.md) já documentava os 20 YAMLs:
oito com eventos automáticos e 12 receitas com trigger próprio manual, também
consumidas pelo compilador do CI automático. A conferência nesta revisão abrangeu
`name`, eventos e jobs dos 20 arquivos. O índice explica propósito, condições,
perfis, artefatos, comandos focais, retenção e limites. Não encontrei um workflow
sem entrada. Melhorado agora com rótulos humanos na primeira coluna e explicação
do significado de V00–V14.

Não seria seguro renomear os arquivos por busca/substituição genérica:
[ci_workflows.py](../../tools/ci_workflows.py) constrói caminhos
`temas-v{campaign:02d}-ci.yml`; testes conferem receitas/checks;
[mm01_local_certify.py](../../tools/mm01_local_certify.py) tem paths e pins de
workflow históricos. Alterar `name` no YAML não muda só documentação: muda os
bytes desses inputs e o título exibido pelo GitHub. A migração precisa separar
identidade do check, path da receita e rótulo de interface.

**Proposta, ainda não executada:** conservar `ci.yml` e identidades dos checks;
usar nomes por função nas receitas. Exemplo: `temas-v06-ci.yml` poderia virar
`temas-assets-determinismo.yml`, V13 `temas-operacao-release.yml`,
`micromodelos-mm01-ci.yml` `micromodelos-regressoes.yml`, SE01
`skills-contratos.yml` e SE02 `skills-certificacao-local.yml`.
A associação da campanha deve ficar explícita em um mapa, não desaparecer.
Escolher se vale renomear o arquivo ou apenas seu título é a decisão desta sprint.

## Tools: o que foi feito e o que faltava

A entrega anterior criou [CATALOGO.md](../../tools/CATALOGO.md) com famílias,
efeitos e distinção de gates/probes/história. **Não reorganizou os executáveis
fisicamente.** Na baseline há 284 arquivos versionados em `tools`, 62 deles
na raiz; as subárvores são tests (108), readme_visuals (61), skill_enforcement
(51) e free_kit (2). Contagens são fotografia dessa revisão, não guardas futuras.

Vários `micromodelo_mm*.py` da raiz já são fachadas de compatibilidade: a
implementação é encaminhada para `hub_micromodelos` no produto. A quantidade de
nomes não representa a mesma quantidade de implementações duplicadas. O índice
agora identifica a finalidade de cada fachada.

O catálogo é útil, mas agrupa muitos nomes por campanha e não dá uma entrada
individual para cada arquivo. Faltavam READMEs em oito subpastas de primeiro/segundo
nível efetivamente usadas. Esse déficit de navegação foi corrigido neste lote.

### Executado agora

- [Índice individual](../../tools/INDICE_ARQUIVOS.md) de todos os arquivos da raiz,
  agrupando domínio e estado, com descrições do próprio módulo.
- [README tools](../../tools/README.md) com mapa de subpastas e descrição explícita
  do estado da arrumação; catálogo aponta ao índice individual.
- READMEs em [free_kit](../../tools/free_kit/README.md),
  [tests](../../tools/tests/README.md), [fixtures](../../tools/tests/fixtures/README.md),
  [runtime dos testes](../../tools/tests/runtime/README.md),
  [parallel](../../tools/skill_enforcement/parallel/README.md),
  [archetypes](../../tools/readme_visuals/archetypes/README.md),
  [QA visual](../../tools/readme_visuals/qa/README.md) e
  [testes visuais](../../tools/readme_visuals/tests/README.md).
- Rótulos humanos no catálogo dos workflows, sem mudar execução/checks.

As entradas explicam finalidade, owner, execução aplicável, efeitos e limites.
Não criam pastas vazias para simular uma organização ainda não realizada.

### Tools deve ficar dentro de docs?

**Recomendação: manter separadas.** Tools contém código executável/importável;
docs contém documentação, decisões, planos e evidência. Workflows chamam paths
`tools/...`, scripts calculam raiz por `__file__.parents`, testes usam imports
com esse diretório no `sys.path`, registries guardam módulos/argv e manifestos
preservam proveniência. Mover para docs exigiria a mesma migração técnica e ainda
misturaria responsabilidades. README perto do código e orientação longa em
`docs/manutencao` resolvem a navegação sem criar essa mistura.

### Estado não deve ser o primeiro nível de pacotes

Não recomendo dividir tudo em `atuais/`, `legado/` e `historico/`. Os módulos de
uma família misturam código reutilizado, diagnósticos e campanhas datadas.
`mm01_local_certify.py`, por exemplo, preserva plano congelado e fornece diagnóstico
atual; `temas_v01_contract.py` emite referência histórica e contrato operacional.
Mudar estado não deveria mudar imports/CLI. Use domínio para código e estado no
README/manifesto. Só arquivos comprovadamente sem consumidores ativos vão para
legado/histórico numa migração específica. Evidência documental antiga cabe em docs.

## Plano proposto por sprints

### Sprint 1 — navegação e diagnóstico (executada neste lote)

Escopo: READMEs, índice por arquivo, rótulos humanos de workflows e este relatório.
Aceite: cobertura dos oito diretórios identificados, 20 workflows indexados,
links locais válidos, arquivos Git conservados e zero mudança de código/produto/YAML.
Gates: validação integrada, snapshot README, compilador CI, controles IA e fronteira.

### Sprint 2 — contrato da estrutura e mapa de dependências (proposta)

1. Aprovar ADR com organização por domínio, retenção e compatibilidade das CLIs.
2. Inventariar por arquivo imports/exportações, `parents[n]`, comandos de subprocesso,
   YAMLs, skills, registries, manifests, testes e documentação que o consomem.
3. Classificar cada arquivo: vigente, biblioteca, probe opt-in, diagnóstico histórico
   ou congelado. "Não encontrei uso" não basta para classificar como removível.
4. Decidir política de fachadas na raiz: manter os comandos públicos existentes
   durante a migração ou migrar todos os consumidores num corte controlado.
5. Separar localização da raiz de cálculo pela profundidade do módulo. Definir um
   owner comum; provar que resolver raiz não aceita symlinks/escape nem outro projeto.

Entregáveis: ADR, mapa `origem → destino → consumidores → teste` e lista dos paths
históricos que ficam imutáveis. Aceite: nenhum arquivo sem classificação e nenhum
comando/import afetado sem sucessor. Ainda não mover arquivos nesta sprint.

### Sprint 3 — migrar uma família piloto (proposta)

Proposta de estrutura, a confirmar na Sprint 2:

```text
tools/
  validacao/        # gates editoriais, pacote, links e instruções
  ci/              # orquestração e compilador das receitas
  distribuicao/    # render, ZIP e kits
  temas/           # contratos e integração temática
  micromodelos/    # contratos, laboratório e migração
  probes/          # chamadas opt-in a destinos autorizados
  comum/           # identidade, paths e utilitários compartilhados
  skill_enforcement/  # domínio existente, com seus submódulos
  readme_visuals/     # domínio existente Node/Python
  tests/             # suítes existentes; reorganização própria se necessária
  free_kit/          # fontes de notebooks
```

Pilotar primeiro uma família pequena com poucos consumidores, escolhida pelo mapa.
Mover implementação, corrigir imports e raiz; manter façade quando aprovada.
Não usar symlinks nem duplicar implementações. README da família define CLIs,
bibliotecas, efeito e suporte. Testar comando antigo/novo quando ambos forem mantidos,
execução de checkout com espaços no caminho e falhas reais dos gates negativos.
Aceite: mesma API/efeitos/códigos de saída e produto byte a byte preservado.

### Sprint 4 — migrar demais famílias e aposentar legado comprovado (proposta)

Migrar um domínio por lote, com seus testes, CI e documentação. Conferir coleta
por identidade, núcleo/assertions e fronteira de pacote. Manifests de origem não
mudam junto com paths ativos; adicionar sucessão estrita quando necessária.
Certificadores congelados mantêm revisão original recuperável e diagnóstico
explícito. Só mover/remover ferramenta legada após verificar consumidores e rota
de reprodução; não excluir provas, fontes visuais ou fixtures pela idade.
Aceite por lote: não perder testes/negativos nem modificar payload por associação.

### Sprint 5 — nomes e simplificação dos workflows (proposta independente)

Escolher títulos humanos apenas ou filenames por função. Fazer mapa dos 20 nomes,
distinguir check de job/workflow e verificar rulesets/required checks do destino.
Se mudar arquivos, substituir a fórmula de paths do compilador por mapa explícito,
migrar consumidores atuais e preservar pins/corpus de certificadores históricos.
Regenerar apenas a seção gerida de `ci.yml`; executar regressões de CI e demonstrar
que falha/skip/cancelamento upstream continuam reprovando o sucessor.
Aceite: triggers, filtros, ambientes, dependências, artifacts, efeitos e check IDs
preservados, ou diferenças deliberadas documentadas no ADR. CI remoto deve comprovar
a revisão antes de integrar; esta revisão documental não é essa migração.

### Sprint 6 — reduzir PLANO_HUB na raiz e preparar handoff (proposta)

Extrair a decisão vigente da paleta para owner atual aprovado; registrar sucessão
sem reescrever a decisão histórica. Arquivar o corpo do plano com sua revisão;
migrar rotas vivas e conservar links históricos recuperáveis. Decidir se a raiz
mantém um localizador curto ou remove a entrada depois de migrar seus consumidores.
Não editar AGENTS/control-map/proveniência com substituição indiscriminada.
Fechar com guia de manutenção para VS Code, dependências por perfil, dry-runs,
rotas de teste e relato de compatibilidade; não presumir homologação no trabalho.

## Evidência e limites desta execução

Conferência do checkout baseado na baseline acima, com diff documental deste lote:

| Comando / conferência | Resultado observado |
|---|---|
| `python -B tools/validate_assistant.py --conferir-readme` | **PASS**, exit 0, zero falhas e zero avisos; snapshot atualizado: 1.768 arquivos e 2.108 links no repo |
| `python -B tools/ai_controls.py --check` | **PASS**, cinco skills/cópias, 215 requisitos e 708 pares de produto |
| `python -B tools/ci_workflows.py --check` | **PASS**, receitas, nomes de checks e dependências preservados |
| `python -B tools/package_boundary.py` | **PASS**, zero erros; pins e contratos de preservação intactos |
| Diff e inventário | **PASS**, somente Markdown; 20 YAMLs e três arquivos da raiz idênticos à baseline; oito READMEs presentes |
| Varredura de links novos | **PASS**, nenhum problema; 30 referências históricas recuperáveis permanecem separadas |

Logs locais: `.artifacts/organizacao-tools/validacao.log`, `ai-controls.json`,
`contagens.json` e `escopo.json`, ignorados no Git. A revisão editorial final
melhorou descrições do índice sem mudar caminhos, links ou código. Não houve
reexecução do CI completo: a mudança é documental e o compilador verificou o
mesmo conjunto executável de receitas.
A classificação é análise do checkout, não certificação de ambiente remoto.
Nenhum teste de runtime, instalação, publicação, push ou merge está incluído
neste lote. Alterações documentais não corrigem o bloqueio de Python isolado
registrado na faxina anterior. Reversão: retirar somente os READMEs/índice novos
e reverter as alterações editoriais deste lote; não tocar implementações ou pins.
