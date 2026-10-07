# Catálogo das ferramentas de manutenção

Esta pasta acompanha o clone Git e sustenta a manutenção do `.assistant`.
Use este catálogo para escolher o comando e compreender seus efeitos antes de
executá-lo no computador do trabalho. O produto instalado no Databricks recebe
somente a fonte sanitizada, pelos procedimentos de kit/publicação.

**Critério de retenção:** conservar gates, testes, geração e transporte usados
pelo projeto; manter instrumentos históricos com sua linhagem explícita. Uma
ferramenta histórica não deve ser usada para certificar o HEAD atual por analogia.
Este catálogo orienta a manutenção e não substitui o catálogo de helpers do Manual.

O [índice individual da raiz](INDICE_ARQUIVOS.md) complementa as famílias abaixo.
A classificação documental não implica que os módulos já foram movidos para subpastas.

## Próxima ação

| Objetivo | Entrada | Efeito e condição |
|---|---|---|
| Conferir a fonte | `python -B tools/validate_assistant.py` | Leitura local; estrutura, links, contratos e higiene |
| Escolher testes | `python -B tools/ci_local.py --help` | Mostra a composição executável vigente; execução pode exigir dependências |
| Examinar espelho | `python -B tools/render_simulado.py` | Plano local sem escrita; `--check` confere derivado existente |
| Gerar espelho | `render_simulado.py --write` | Substitui o destino gerido; inventariar extras e preservar conflitos antes |
| Conferir automação de CI | `python -B tools/ci_workflows.py --check` | Leitura local; receitas e DAG; ver [workflows](../.github/workflows/README.md) |
| Conferir instruções IA | `python -B tools/ai_controls.py --check` | Leitura local; `--generate` escreve somente adaptadores geridos |
| Preparar transferência | [kit de trabalho](kit_transicao_trabalho.py) e [runbook](../docs/playbooks/replicacao-trabalho.md) | Preparação local é distinta de importação/promoção no destino |
| Recuperar prova do protótipo retirado | `python -B tools/verify_concierge_history.py` | Confere blobs no histórico Git completo, sem restaurar arquivos |

As dependências de desenvolvimento são declaradas em `requirements-dev.txt` e
`requirements-temas-dev.txt`; a cadeia visual tem `readme_visuals/package.json`.
Instalação exige escopo próprio. Ausência de dependência é BLOCKED, não dispensa
nem autorização para substituir um gate por um diagnóstico superficial.

## Gates atuais e apoio compartilhado

| Arquivos ou família | Função | Estado e execução |
|---|---|---|
| [validate_assistant.py](validate_assistant.py) | Validação integrada da fonte e rotas do Git | Atual; primeira conferência da mudança |
| [ci_local.py](ci_local.py), [run_core_tests.py](run_core_tests.py) | Orquestração local e regressões do núcleo | Atual; os IDs pertencem a `ETAPAS`, não a uma contagem histórica |
| [ci_workflows.py](ci_workflows.py) | Compõe receitas dos workflows em CI permanente | Atual; manuais também são inputs, não apagar sem migrar compiler |
| [ai_controls.py](ai_controls.py), [task_context.py](task_context.py) | Contratos das instruções IA, adaptadores e contexto por tarefa | Atual; leitura normal, geração explícita separada |
| [readme_objeto_contract.py](readme_objeto_contract.py) | Contrato editorial e ratchet de READMEs de objeto | Atual; depende de identidades e evidência histórica, não recriar baseline |
| [markdown_links.py](markdown_links.py), [markdown_contract.py](markdown_contract.py) | Análise estática de Markdown e links | Apoio atual; não confere comportamento de conversa nem conteúdo remoto |
| [project_policy.py](project_policy.py), [repo_inventory.py](repo_inventory.py) | Identidades geridas e inventário Git | Apoio atual; índice, extras e worktree são estados distintos |
| [package_boundary.py](package_boundary.py), [notebook_marker.py](notebook_marker.py) | Fronteira do payload e classificação FILE/NOTEBOOK | Apoio atual; evita transportar caches e classificar todo `.py` como notebook |
| [api_publica.py](api_publica.py) | Descobre API por AST e gera fachada | Atual; modo de geração escreve, inspecionar interface antes |
| [verify_concierge_history.py](verify_concierge_history.py) | Prova hashes e tamanhos dos blobs do protótipo retirado | Atual; requer histórico completo; não depende da pasta eliminada |
| [historical_links.py](historical_links.py) | Prova estrita de hrefs congelados por fonte/hash/commit/objeto | Atual; separada da navegação local, sem dispensa para links vivos |
| [tests/](tests/) | Regressões de contratos, integração e casos negativos | Atual; transportar com o clone, sem publicar como produto |

## Geração, transporte e aceites

| Arquivos ou família | Função | Limite de uso |
|---|---|---|
| [render_simulado.py](render_simulado.py), [simulado.py](simulado.py) | Plano, materialização e equivalência do espelho local | Atual; escrita é efeito explícito e a saída é derivada |
| [bundle_implantacao.py](bundle_implantacao.py) | ZIP sanitizado com manifesto para implantação | Atual; não equivale a instalação, exige fonte e derivado consistentes |
| [bundle_para_auditoria.py](bundle_para_auditoria.py) | Corpus canônico, segurança, completo ou recorte de tarefa | Atual; mover docs para histórico não as exclui dos modos integrais |
| [kit_transicao_trabalho.py](kit_transicao_trabalho.py) | Kit local de replicação no trabalho | Atual; não promove workspace automaticamente |
| [publicar_free.py](publicar_free.py) | Publicação protegida e conferência remota | Atual, remoto; exige destino Free e escopo; plano também consulta CLI |
| [aceite_trabalho.py](aceite_trabalho.py), [aceite_micromodelos_trabalho.py](aceite_micromodelos_trabalho.py) | Roteiros de aceite no destino autorizado | Atual, runtime; execução local não comprova trabalho, ACL ou aceite humano |
| [spark_smoke_test.py](spark_smoke_test.py) | Chamadas funcionais no runtime Databricks | Atual, runtime; dados/credenciais dependem do ambiente autorizado |
| [micromodelo_free_kit.py](micromodelo_free_kit.py), [free_kit/](free_kit/) | Preparação e notebooks de demonstração Free | Atual; somente sintéticos; transporte e execução são etapas diferentes |

## Micromodelos e temas

| Arquivos ou família | Função | Owner e condição |
|---|---|---|
| `micromodelo_mm01_contract.py`, `micromodelo_mm02_fingerprint.py`, `micromodelo_mm03_metadata.py`, `micromodelo_mm04_flow.py` | Contratos, fingerprint, metadados e fluxo dos Micromodelos | Apoio atual; conferir [kit/guia](micromodelo_free_kit.py) e testes correspondentes |
| `micromodelo_mm06_artifacts.py`, `micromodelo_mm06_e0_tracking.py`, `micromodelo_mm07_databricks.py` | Artefatos, tracking E0 e integração Databricks | Atual; operações remotas/runtime dependem de autorização e configuração |
| `micromodelo_mm09_lab.py`, `micromodelo_mm10_handoff.py`, `micromodelo_mm12_migration_lab.py`, `micromodelo_mm13_catalog.py` | Laboratórios, handoff, migração e catálogo | Atual; leitura, escrita local e promoção dependem do modo específico |
| `temas_v01_contract.py`, `temas_v02_check.py` | Schema/contrato e núcleo dos temas | Atual; requer dependências declaradas, sem instalação implícita |
| `temas_v09_transicao.py`, `temas_v10_app.py`, `temas_v12_homologacao.py` | Transição, app e roteiro de homologação | Atual; ensaio local não prova aparência/aceite no destino |
| `temas_v13_preflight.py`, `temas_v13_operacional.py`, `temas_v13_release.py`, `temas_v13_compatibilidade.py`, `temas_v13_diagnostico.py`, `temas_v13_ensaios.py`, `temas_v14_ownership.py` | Preflight, operação, release, compatibilidade, diagnóstico, ensaios e ownership | Consultar [frente de temas](../docs/sprints/sistema_temas/README.md); estado do script não certifica conclusão da sprint |

## Skills, campanhas e probes

| Arquivos ou família | Função | Estado e limite |
|---|---|---|
| [skill_enforcement/](skill_enforcement/README.md) | Schemas, policies, contratos, avaliação e certificadores de campanha | Composição mista; distinguir gate vigente e plano congelado pelo owner |
| `skill_enforcement/parallel/` | Cobertura B0, identidade, lease, sandbox, preflight, scheduler, launcher e evidência | Apoio da coordenação atual; inventário de cobertura não comprova execução nem independência de origem |
| `skill_enforcement/ser_promotion_certify.py` | Certificação da promoção SER | Pós-promoção; seguir rota específica, não o corpus pré-promoção |
| `skill_enforcement/ser_certify.py`, `skill_enforcement/certify_local.py` | Certificação SER/SE com linhagem histórica | Consulte [certificadores congelados](../docs/manutencao/certificadores-congelados.md) antes; não certificar HEAD com baseline antiga |
| `skills_*_free_probe.py`, `skill_enforcement/se0*_free_probe.py`, `skill_enforcement/ser01_free_probe.py` | Probes de tracking, Delta, materialização, delivery e roteamento em Free | Opt-in, remoto/runtime; precisam de alvo autorizado e dados sintéticos; não são startup do VS Code |
| [mm01_local_certify.py](mm01_local_certify.py) | MM01 Local Certification v1 e diagnóstico de compatibilidade | Histórico; `--describe` e `--diagnose` não emitem certificação PASS do HEAD |

## Recursos visuais atuais e históricos

| Arquivos ou família | Função | Estado e limite |
|---|---|---|
| [readme_visuals/](readme_visuals/README.md) | Cadeia visual Node/Python, fontes, assets e QA | Produção v2 é a rota recomendada; scripts internos não são CLIs intercambiáveis |
| [inventario_visual.py](inventario_visual.py), [executar_baseline_visual.py](executar_baseline_visual.py) | Inventário e baseline visual V00 em `.artifacts/` | Diagnóstico atual com contexto V00; não concede homologação visual |
| [render_readme_visuals.mjs](render_readme_visuals.mjs) e `readme_visuals/publish_sprint0.py` | Fluxo visual anterior/sprint 0 | Histórico; manter para linhagem e consumidores até migração específica, evitar em nova produção |
| `readme_visuals/qa/`, `readme_visuals/assets/` | Evidências, fontes visuais e amostras | Nem toda imagem é descartável; conferir geração, consumo e hashes antes de remover |

## Como manter o catálogo

Ao acrescentar ou retirar uma ferramenta, registre função, efeitos, owner e rota
vigente neste catálogo ou no README da coleção correspondente. Os detalhes de
argumentos pertencem ao `--help` e ao código; uma tabela não autoriza um comando.
Novas famílias exigem classificação, revisão dos consumidores e testes pertinentes.
Preserve snapshots e ADRs aceitos; sucessão exige decisão nova, não reescrita.

Em 07/10/2026, esta organização reteve ferramentas úteis e retirou somente o
protótipo duplicado `novas_funcionalidades/`. A evidência executada está em
[retirada do protótipo](../docs/manutencao/retirada-prototipo-2026-10-07.md).

[Voltar aos comandos e gates](README.md)
