# Arquivos na raiz de tools

Inventário de 07/10/2026: 62 arquivos de primeiro nível na baseline `09ecdc1e`;
este índice acrescenta uma entrada documental. Não inclui caches/dependências
locais nem substitui inventário de todo o diretório. Os nomes atuais são mantidos
por compatibilidade; função e domínio aparecem abaixo para facilitar a leitura.

Descrições resumem a docstring e a função do owner; nas fachadas de
compatibilidade, indicam o domínio da implementação encaminhada.
Classificação é editorial: "atual" não significa runtime homologado, e um arquivo
histórico pode ter diagnóstico ainda utilizado. Efeitos, pré-condições e próxima
ação estão no [catálogo](CATALOGO.md); a proposta de migração está no
[plano](../docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md).

| Arquivo | Domínio / estado | Descrição do owner |
|---|---|---|
| [CATALOGO.md](CATALOGO.md) | Documentação | Famílias, efeitos e rotas atuais/históricas. |
| [INDICE_ARQUIVOS.md](INDICE_ARQUIVOS.md) | Documentação | Inventário individual da raiz. |
| [README.md](README.md) | Documentação | Entrada de manutenção e comandos por objetivo. |
| [aceite_micromodelos_trabalho.py](aceite_micromodelos_trabalho.py) | Destino/runtime — escopo próprio | Aceite E0 sintético do pacote técnico de Micromodelos extraído. |
| [aceite_trabalho.py](aceite_trabalho.py) | Destino/runtime — escopo próprio | Núcleo do notebook de aceite: verificações locais e testes sintéticos opt-in. |
| [ai_controls.py](ai_controls.py) | Instruções e contexto IA | Valida instruções de manutenção, rastreabilidade e adaptadores; sem rede ou instalação. |
| [api_publica.py](api_publica.py) | Apoio compartilhado | Extrai a API pública de um módulo por AST, sem importá-lo. |
| [bundle_implantacao.py](bundle_implantacao.py) | Geração/distribuição local | Gera um ZIP mínimo e sanitizado para implantação manual no Databricks. |
| [bundle_para_auditoria.py](bundle_para_auditoria.py) | Geração/distribuição local | Empacota texto UTF-8 para leitura: canonical (padrão), security, full ou task. |
| [ci_local.py](ci_local.py) | CI e regressões | Gate local do repositório: roda sem credencial do Databricks. |
| [ci_workflows.py](ci_workflows.py) | CI e regressões | Compila receitas em um grafo de CI, preservando identidades dos checks. |
| [executar_baseline_visual.py](executar_baseline_visual.py) | Diagnóstico visual com linhagem V00 | Executa V00 em dois checkouts limpos e salva evidências em .artifacts/. |
| [historical_links.py](historical_links.py) | Apoio compartilhado | Confere referências congeladas no Git, separadas dos links locais vivos. |
| [inventario_visual.py](inventario_visual.py) | Diagnóstico visual com linhagem V00 | Inventário V00: leitura de checkout Git limpo, sem importar o produto. |
| [kit_transicao_trabalho.py](kit_transicao_trabalho.py) | Geração/distribuição local | Monta kit offline para a UI corporativa, sem publicar ou usar credenciais. |
| [markdown_contract.py](markdown_contract.py) | Apoio compartilhado | Leitura conservadora de links Markdown sem interpretar exemplos como links. |
| [markdown_links.py](markdown_links.py) | Apoio compartilhado | Destinos Markdown locais, sem dependências ou interpretação de HTML arbitrário. |
| [micromodelo_free_kit.py](micromodelo_free_kit.py) | Geração/distribuição local | Empacota fontes E0 sintéticas para transporte concreto ao Databricks Free. |
| [micromodelo_mm01_contract.py](micromodelo_mm01_contract.py) | Micromodelos — contratos atuais | Fachada para o contrato canônico e validação das especificações dos Micromodelos. |
| [micromodelo_mm02_fingerprint.py](micromodelo_mm02_fingerprint.py) | Micromodelos — contratos atuais | Fachada para fingerprint e identidade determinística da especificação. |
| [micromodelo_mm03_metadata.py](micromodelo_mm03_metadata.py) | Micromodelos — contratos atuais | Fachada para o contrato de metadados e catálogo de fontes. |
| [micromodelo_mm04_flow.py](micromodelo_mm04_flow.py) | Micromodelos — contratos atuais | Fachada para fluxo de execução e composição dos Micromodelos. |
| [micromodelo_mm06_artifacts.py](micromodelo_mm06_artifacts.py) | Micromodelos — contratos atuais | Fachada para artefatos de execução e suas referências. |
| [micromodelo_mm06_e0_tracking.py](micromodelo_mm06_e0_tracking.py) | Micromodelos — contratos atuais | Reproduz três runs MLflow E0 com a fixture MM09; usa backend local ignorado. |
| [micromodelo_mm07_databricks.py](micromodelo_mm07_databricks.py) | Micromodelos — contratos atuais | Fachada para integração e preparação de execução no Databricks. |
| [micromodelo_mm09_lab.py](micromodelo_mm09_lab.py) | Micromodelos — contratos atuais | Fachada para laboratório sintético dos Micromodelos. |
| [micromodelo_mm10_handoff.py](micromodelo_mm10_handoff.py) | Micromodelos — contratos atuais | Fachada para handoff e transferência das informações de execução. |
| [micromodelo_mm12_migration_lab.py](micromodelo_mm12_migration_lab.py) | Micromodelos — contratos atuais | Fachada para laboratório de migração, com implementação no produto. |
| [micromodelo_mm13_catalog.py](micromodelo_mm13_catalog.py) | Micromodelos — contratos atuais | Fachada para catálogo e seleção das especificações de Micromodelos. |
| [mm01_local_certify.py](mm01_local_certify.py) | Certificador histórico + diagnóstico | Preserva certificação MM01 v1 congelada e oferece diagnóstico de compatibilidade atual. |
| [notebook_marker.py](notebook_marker.py) | Apoio compartilhado | Detecção canônica de notebook Databricks a partir do arquivo .py. |
| [package_boundary.py](package_boundary.py) | Validação de contratos | Contrato da extração de QA/autoria: recursos runtime nunca são dispensados. |
| [project_policy.py](project_policy.py) | Apoio compartilhado | Políticas compartilhadas pelas ferramentas locais do projeto. |
| [publicar_free.py](publicar_free.py) | Destino/runtime — escopo próprio | Publica o ecossistema no Databricks Free e confere o resultado. |
| [readme_objeto_contract.py](readme_objeto_contract.py) | Validação de contratos | Contrato estrutural dos READMEs e migração monotônica, sem importar helpers. |
| [render_readme_visuals.mjs](render_readme_visuals.mjs) | Renderer histórico v1 | Renderer v1; recusa manifesto v2 e não é a rota atual de produção. |
| [render_simulado.py](render_simulado.py) | Geração/distribuição local | Renderiza .artifacts/simulado/ como espelho da árvore do workspace. |
| [repo_inventory.py](repo_inventory.py) | Apoio compartilhado | Inventário Git certificável, separado da higiene da árvore de trabalho. |
| [requirements-dev.txt](requirements-dev.txt) | Dependências | Dependências do gate local. |
| [requirements-temas-dev.txt](requirements-temas-dev.txt) | Dependências | Dependências adicionais dos contratos temáticos. |
| [run_core_tests.py](run_core_tests.py) | CI e regressões | Executa os casos do núcleo e exige sucesso de cada identidade esperada uma vez. |
| [simulado.py](simulado.py) | Apoio compartilhado | Inventário exato do derivado: paths, bytes, hashes e tipos, sem git diff. |
| [skills_baseline_tracking_free_probe.py](skills_baseline_tracking_free_probe.py) | Probes remotos opt-in | Tentativa sintética autorizada de tracking SER10, sem retry nem registro de modelo. |
| [skills_delivery_free_probe.py](skills_delivery_free_probe.py) | Probes remotos opt-in | Probe sintético de runtime das oito candidatas de skills; destino autorizado. |
| [skills_delta_free_probe.py](skills_delta_free_probe.py) | Probes remotos opt-in | Tentativa sintética de MERGE Delta no workspace Free do chamador. |
| [skills_feature_materialization_free_probe.py](skills_feature_materialization_free_probe.py) | Probes remotos opt-in | Probe Delta de materialização de uma feature view Cross PIT sintética verificada. |
| [skills_tracking_free_probe.py](skills_tracking_free_probe.py) | Probes remotos opt-in | Probe sintético do helper MLflow; não certifica Baseline L4. |
| [spark_smoke_test.py](spark_smoke_test.py) | Destino/runtime — escopo próprio | Notebook de smoke com dados sintéticos; exercita helpers no runtime Databricks real. |
| [task_context.py](task_context.py) | Instruções e contexto IA | Rotas explícitas e limitadas para o contexto de tarefa, sem busca recursiva. |
| [temas_v01_contract.py](temas_v01_contract.py) | Temas — contratos/integração atuais | Verificação LOCAL do contrato candidato V01, sem resolver ou aplicar temas. |
| [temas_v02_check.py](temas_v02_check.py) | Temas — contratos/integração atuais | Guarda estrutural V02; não publica nem importa dependências gráficas. |
| [temas_v09_transicao.py](temas_v09_transicao.py) | Temas — contratos/integração atuais | Contrato V09 do Sistema de Temas para o kit de transição. |
| [temas_v10_app.py](temas_v10_app.py) | Temas — contratos/integração atuais | Monta/verifica o bundle local do Databricks App de gestão visual V10. |
| [temas_v12_homologacao.py](temas_v12_homologacao.py) | Temas — contratos/integração atuais | V12 — validação fail-closed de evidências de homologação do Sistema de Temas. |
| [temas_v13_compatibilidade.py](temas_v13_compatibilidade.py) | Temas — contratos/integração atuais | Compatibilidade e acessibilidade operacional V13-S5. |
| [temas_v13_diagnostico.py](temas_v13_diagnostico.py) | Temas — contratos/integração atuais | Observabilidade e diagnóstico local V13-S4. |
| [temas_v13_ensaios.py](temas_v13_ensaios.py) | Temas — contratos/integração atuais | V13-S6: ensaios operacionais locais/simulados por superfície. |
| [temas_v13_operacional.py](temas_v13_operacional.py) | Temas — contratos/integração atuais | Validador read-only do inventário operacional V13-S1. |
| [temas_v13_preflight.py](temas_v13_preflight.py) | Temas — contratos/integração atuais | Preflight operacional unificado V13-S2. |
| [temas_v13_release.py](temas_v13_release.py) | Temas — contratos/integração atuais | Ciclo operacional local V13-S3 para release, update e rollback dry-run. |
| [temas_v14_ownership.py](temas_v14_ownership.py) | Temas — contratos/integração atuais | Valida matriz de ownership, responsabilidades e autoridade operacional por superfície. |
| [validate_assistant.py](validate_assistant.py) | Validação de contratos | Bateria de validação local do ambiente_databricks/. |
| [verify_concierge_history.py](verify_concierge_history.py) | Validação de contratos | Confere recuperação do protótipo retirado usando blobs Git e manifesto congelado. |
