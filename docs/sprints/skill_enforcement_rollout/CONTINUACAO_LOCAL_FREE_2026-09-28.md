# Continuação local e Free — 2026-09-28

(Codex) O usuário autorizou continuar a implementação, testes/auditoria e levar os candidatos ao Databricks quando necessário. Destino resolvido: perfil pessoal FREE; dados exclusivamente sintéticos. Esta autorização não é promoção de policy nem merge. A configuração humana e os componentes de controller/B0 permanecem preservados.

A entrega inicial está em [Entrega local](ENTREGA_LOCAL_2026-09-28.md). Este registro é aditivo e não reescreve a evidência anterior.

## Escopo por skill

| Skill | Capacidade candidata / próxima fronteira |
|---|---|
| EDA | Piloto existente; regressão proporcional. |
| Criar Objeto | Escopos existentes de geração/validação/escrita, sem expansão nesta rodada. |
| Auditoria | Verificação existente; regressão proporcional. |
| Tutor | Escopo explicativo L0, sem runner artificial. |
| Concierge | Descoberta/handoff L1; não executa outras skills por conta própria. |
| Comentar Notebook | Contrato editorial L1, sem runner artificial. |
| Safra | Mensal binária EVENT e CUMULATIVE com maturidade/denominador observáveis. Trimestre e estimando monetário não suportados nesta candidata. |
| Explainability | SHAP linear escalar com background, features, modelo e amostra vinculados. Outros métodos exigem perfil próprio; interpretação causal/fairness não é inferida. |
| Estatística | KS bilateral contínuo sem empates, hipótese e comparação únicas declaradas. Oráculos combinatórios cobrem fixtures; outras famílias não são reivindicadas. |
| Cross-EDA | Contexto L2, diagnóstico estático e novo PIT sintético com janela, atraso constante, UTC e limite inclusivo; Receipt, oráculo e Postflight/finalizer. |
| Features | Lag observado dentro da janela elegível e composição de feature view com PIT verificado. Materialização Delta sintética implementada, com tipagem, proveniência, identidade/versionamento da tabela e limpeza; prova Free R2 PASS, com MERGE/replay/readback e DROP conferidos. |
| Baseline | Treino binário temporal e fit restrito ao treino; adapter de tracking registra o mesmo modelo, parâmetros, métricas e assinatura, verifica artefato remoto e soft-delete. Execução Free R2 PASS; prova live antes da limpeza, run/experimento com soft-delete verificado. Probe anterior de helper permanece evidência distinta. |
| Monitoramento | Drift numérico e performance com labels maduros, política AUC explícita e finalização limitada ao diagnóstico. Precisão de AUC/KS/Brier conferida contra oráculos independentes; nenhuma ação automática. |
| Pipeline | Especificação L2 e MERGE Spark em memória preservados; executor Delta sintético exige autorização externa, tabela nova marcada, retorno, replay e DROP somente com propriedade conferida. Não é deploy de job permanente. |

## Evidência desta rodada

Evidência detalhada local, não versionada: `.artifacts/skills-delivery-evidence/continuation/`.

- Backup/leitura dos 590 arquivos gerenciados existentes no Free: 579 iguais à candidata inicial e 11 iguais à base Git, nenhum conflito remoto encontrado. Notebooks foram exportados por SOURCE e comparados com normalização do publicador; arquivos de configuração de plataforma não foram copiados.
- `feature-pit-tests.log`: 5 testes PASS (composição PIT e lag).
- `performance-precision-tests.log`: 15 testes PASS (performance, fronteiras numéricas e drift).
- `baseline-tracking-tests.log`: 12 testes PASS (treino, verificação e controles MLflow simulados).
- `delta-controls-tests.log`: 15 testes PASS (6 controles Delta simulados e 9 regressões de execução/spec). Primeiro ensaio bloqueou pelo hash de um contrato convertido de CRLF para LF; equivalência normalizada conferida e somente esse hash corrigido.
- `pit-pipeline-tests.log`: 18 testes PASS em Spark local, incluindo os novos perfis e regressões dos preflights/diagnóstico estático.
- Auditoria independente: duplicidade temporal por representações Z/+00:00 corrigida; serialização UTC não depende do timezone do driver; manifesto PIT corrigido para bytes LF. Pipeline fecha retorno e falha de limpeza antes de emitir Receipt.
- `tracking-output.json`: helper `run_governado` executado no Free, com readback de parâmetros, métrica, tags, assinatura e predições do modelo. Run e experimento criados pelo probe tiveram soft-delete conferido; isso não declara remoção física nem Baseline L4.
- A primeira importação de notebook falhou no transporte HTTP/2; readback confirmou ausência. A repetição usou HTTP/1 somente no processo CLI e passou, sem mudança de configuração/controller/firewall.
- Auditoria independente encerrou os achados de precisão, autolog antes de fit/refit, timeout com resultado desconhecido e snapshots de autorização/pedido antes de callbacks. Nenhum achado aberto na candidata integrada.
- `validate-final.log`: APROVADO, 0 falhas; 155 entradas de manifestos conferidas. O único aviso é cache Python local, excluído pelo renderer. Link de README ao teste externo ao pacote e mojibake no probe corrigidos na fonte; derivado regenerado, sem edição manual.
- Notebook de runtime: `tools/skills_delivery_free_probe.py`. Notebook separado de capacidade MLflow: `tools/skills_tracking_free_probe.py`. Resultados remotos e publicação são discriminados por tentativa abaixo.

## Limites que não podem virar PASS por redação

Receipt V1 e Postflight existentes são usados conforme seus contratos. A rota de cálculo não ganha autorização de escrita persistente por produzir um Receipt. Em particular, um MERGE sobre DataFrames em memória não comprova MERGE Delta, e um helper MLflow exercitado isoladamente não certifica Baseline L4.

A conclusão do perfil PIT refere-se apenas ao join sintético validado. Readiness de negócio, dados reais, bitemporalidade e atraso variável permanecem fora dele. UNKNOWN ou falta de evidência bloqueiam o perfil aplicável.

O teste via Jobs executa código no runtime Free. Descoberta/@menção e resistência a bypass precisam de conversa real com Genie Code; um notebook não substitui essa observação. Roteiro: [forward tests](../../testes/forward/roteiro.md).

## Referências de runtime consultadas

- [Ambientes serverless](https://docs.databricks.com/aws/en/release-notes/serverless/environment-version/): ambiente 2 oferece Python 3.11; seleção explícita para testar a dependência SHAP desta candidata.
- [Dependências serverless](https://docs.databricks.com/aws/en/compute/serverless/dependencies): dependências por ambiente de tarefa; PySpark não é instalado no Free.
- [MLflow Client](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html): readback e soft-delete. Limpeza lógica não é alegada como remoção física de artefatos.


## Publicação conferida

O publicador canônico executou plano, envio e `--verify --conteudo`: **PASS**,
652/652 arquivos exportados e comparados, 14/14 skills, zero ausentes/obsoletos
ou divergências. O arquivo de configuração gerenciado pela plataforma foi
preservado. Fonte: checkout com mudanças locais sobre `d6cd9fd39f3e82ccf9db6f9e0c61db526fe3a143-dirty`;
isso não representa commit ou merge da candidata.

Hash normalizado do pacote: `e07850d3508aacf6d6bf286bb2e35f78fbf9dceaff5ea2f596342e90ba9e053b`.
Evidência: `publish-final-verify.json` e `publish-final-verify.log`.
Os três notebooks R1 foram importados em pasta pessoal nova e tiveram
readback antes da submissão única. Resultados R1 estão registrados abaixo.

## Primeira execução Free dos perfis

Job concluído; os relatórios internos, e não o estado SUCCESS do job, determinam
o resultado. `suite-runtime-report.json`: **12/12 PASS**, incluindo Receipt,
verificação, rejeição de replay/adulteração e hashes do pacote sem mudança.
Versões observadas: Python 3.11.10, NumPy 1.23.5, pandas 1.5.3, SciPy 1.11.1, scikit-learn 1.3.0 e SHAP 0.44.1. Na R1, o campo de versões dizia `MISSING` para distribuições `mlflow`/`pyspark`, embora os módulos estivessem ativos; R2 distingue falta de metadata da disponibilidade de import.
`suite-delta-report.json`: **PASS**, MERGE real e replay com hashes iguais ao
esperado, duas verificações de propriedade, DROP e ausência confirmada.

`suite-tracking-report.json`: **FAIL** no verificador, embora o adapter tenha
retornado PASS. O modelo e seus metadados foram lidos e os recursos tiveram
soft-delete. A reconciliação confirmou que a exclusão do experimento muda seu
nome para Trash e a consulta posterior ao run exige experimento ativo.
A ordem da verificação independente era incompatível com esse ciclo de vida.
Esta tentativa permanece FAIL, sem restauração nem repetição automática.
Protocolo corrigido na R2: verificador independente lê o modelo antes da limpeza; run tem soft-delete e readback antes da exclusão do experimento. Verificação final declara somente consistência do registro e limpeza do experimento, sem alegar nova leitura do modelo excluído. A nova prova isolada R2 passou, conforme a seção seguinte.

## Candidata R2

- `baseline-tracking-v2-tests.log`: 13 PASS; `tracking-standalone-tests.log`: 7 PASS. Baterias sobrepostas, não somadas. Autolog desabilitado antes de fit/refit, autorização congelada antes de callbacks e verificação live independente antes do soft-delete.
- `fe-materialization-integrated-tests.log`: 28 PASS, incluindo 7 controles FE, 6 Delta, 5 execução Pipeline, 4 spec, 1 composição PIT, 4 lag e 1 Cross PIT.
- FE reutiliza o ciclo Delta de Pipeline. Confere Receipt/Postflight externos, projeção exata e proveniência; leitura rejeita coerção float/bool, identidade da tabela é estável e versão Delta não retrocede. Perfil PIT permanece inteiro entre -1.000.000 e 1.000.000.
- Auditoria independente encerrou achados da candidata. `validate-r2-before-render.log` e `validate-r2-final.log`: PASS; derivado regenerado. Configuração humana e policy preservadas.
- Antes de publicar R2, 652 arquivos remotos R1 foram exportados e comparados: nenhum conflito (`r2-remote-preservation.json`).
- R2 publicada e conferida integralmente: **654/654 arquivos, 14/14 skills, zero divergências**, `publish-r2-verify.json`. Hash normalizado `513e2ef9536833d6784d0d464f824392d0559f7dcc39eee1185d434a2c5446f9`. Arquivo da plataforma preservado.
- Quatro notebooks importados sem sobrescrita em pasta pessoal nova, com readback e hashes conferidos; submissão única `766771719629464`. Quatro relatórios internos PASS; detalhes abaixo.

## Provas Free R2 concluídas

O job `766771719629464` terminou, e **cada relatório interno** foi conferido:

| Prova | Resultado e evidência |
|---|---|
| Runtime | **12/12 PASS**, `suite-r2-runtime-report.json`; 103 hashes observados antes/depois iguais aos arquivos fonte, sem mutação do pacote. |
| Baseline MLflow | **PASS**, `suite-r2-tracking-report.json`; mesmo modelo treinado registrado, parâmetros/métricas/tags/assinatura e predições lidos; verificação independente enquanto ativo; run e experimento com soft-delete conferido. |
| Pipeline Delta | **PASS**, `suite-r2-delta-report.json`; criação autorizada, MERGE real, readback, replay idempotente e DROP com ausência conferida. |
| Materialização FE | **PASS**, `suite-r2-feature_materialization-report.json`; view PIT vinculada a Receipt/Postflight, tipos e valores preservados, três linhas esperadas, identidade estável, versões Delta 1 → 2, replay e DROP com ausência conferida. Timezone restaurado. |

A conferência raiz `r2-independent-check.json` passou, incluindo o oráculo FE
manual: d1 recebe 1.000.000 disponível exatamente no corte de microssegundos;
d2 e d3 permanecem nulos. Digest esperado, primeira escrita e replay iguais:
`69bfe597aa47b9bff9ae831dca00f6c3723703ae9d0e1d24c9ad8a2241214a48`.

Runtime observado: Python 3.11.10, NumPy 1.23.5, pandas 1.5.3, SciPy 1.11.1,
scikit-learn 1.3.0, SHAP 0.44.1, MLflow 2.11.4 e PySpark 3.5.0. Os dois últimos
foram identificados pelo módulo; a metadata de distribuição estava ausente.

O verificador final de tracking declara `model_rechecked_after_cleanup=false`:
a prova do modelo ocorreu antes da limpeza. Soft-delete é limpeza lógica, sem
alegação de remoção física. Os notebooks de prova e metadados dos jobs ficam na
pasta pessoal para inspeção; não foi criado job recorrente. A tentativa R1 de
tracking continua **FAIL**, sem alteração retroativa de resultado.

Auditoria independente final: **sem achados materiais**. Reproduziu os 654
hashes individuais e os dois agregados da publicação, os 103 hashes do runtime,
os vínculos live/cleanup de tracking e os oráculos/replay/proveniência/limpeza
FE e Delta. Auditoria feita sobre artefatos locais; não reivindica nova consulta
a recursos excluídos nem observação da UI. Índice de evidências:
`r2-evidence-index.json`.

## Fechamento

As oito skills prioritárias têm os perfis candidatos da matriz implementados,
testados localmente e exercitados no Free; as demais seis preservam o escopo e
as regressões proporcionais descritas na entrega local. Isso não certifica todas
as famílias de algoritmos, dados corporativos ou prontidão de negócio.

Publicação R2 e provas sintéticas: **PASS**. Homologação conversacional Genie:
**NOT_RUN**. Não houve promoção de policy, merge ou publicação no trabalho.
Configuração humana e policy mantiveram seus hashes; controller/B0 não recebeu
manutenção. Validação final: `validate-r2-closure.log`, zero falhas e zero avisos.

A próxima atuação humana é abrir chats novos no Genie Code do Free e coletar
seleção/carregamento/@menção e comportamento nos [37 casos preparados](GENIE_SKILLS_CANDIDATAS_2026-09-28.md).
O [registro preenchível](GENIE_SKILLS_RESULTADOS_2026-09-28.md) vincula a campanha
ao hash R2 e inicia todos os casos em NOT_RUN. Os casos congelados VF/CE e o
roteiro geral permanecem distintos. O playbook
[forward-test-skills](../../../.claude/skills/forward-test-skills/SKILL.md) exige
“Observar qual skill o Genie Code carrega (indicador na UI)”; esta sessão não
dispõe de ferramenta para observar/controlar essa interface. Um resultado de
Jobs não substitui essa evidência. Após a coleta, podem ser corrigidos e
retestados somente os casos afetados, preservando os primeiros resultados.

