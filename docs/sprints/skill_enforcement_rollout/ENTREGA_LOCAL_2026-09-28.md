# Entrega local das skills — 2026-09-28

(Codex) Implementação direta autorizada, integrada centralmente com autoria e auditoria por subagentes. Dados exclusivamente sintéticos. Esta entrega é candidata local: não altera níveis na policy, não homologa Genie e não publica nem faz merge. A configuração humana do Codex foi preservada; não houve manutenção de controller, firewall ou B0.

## Escopo verificável

| Skill | Execução local e limite |
|---|---|
| Safra | SKILL exige runner e verificador existentes, Receipt e contexto externo; perfil mensal binário sintético. |
| Explainability | SHAP real para regressão linear escalar, referência declarada, modelo e arrays vinculados; oráculo analítico por feature. Cópias float64, bloqueio de inteiros não representáveis e de ordem divergente das features. |
| Validação Estatística | KS bilateral para duas amostras contínuas independentes, sem empates e com uma comparação declarada; não representa todos os testes estatísticos da skill. |
| Cross-EDA | Preflight L2 preservado; diagnóstico Spark real de duas fontes estáticas sintéticas, PIT NOT_APPLICABLE, cardinalidade sem expansão. Não produz join de negócio nem PIT temporal. |
| Feature Engineering | Lag1 por entidade dentro da janela elegível, disponibilidade fixa de um dia, fronteiras inclusivas; warm-up explícito, sem fit ou materialização. |
| Baseline | Split temporal, scaler ajustado apenas no treino, regressão logística e helpers reais. Saída restrita a AUC/Brier verificadas; sem registro ou persistência de modelo. |
| Monitoramento | PSI por quantis da referência e KS em janelas disjuntas, tratamento explícito de nulos; sem alertas operacionais, performance com rótulos ou retreino. |
| Pipeline Builder | Validação L2 de especificação sintética com template real, sem Receipt de execução. Deploy, escrita, agendamento e conclusão operacional permanecem NOT_RUN/não autorizados. |

As rotas reutilizam os contratos, fachadas SEF, Receipt V1 e integridade existentes. Pipeline usa preflight sem fingir execução de pipeline. A mudança no helper SHAP adiciona `background` opcional e preserva o comportamento anterior quando omitido. Os SKILL.md mantêm suas orientações anteriores e acrescentam a rota candidata.

## Evidência local

Evidência não versionada em `.artifacts/skills-delivery-evidence/`:

- `integration-tests.log`: seleção de 224 testes de domínio, piloto EDA, candidatos, policy, auditoria e criação de objeto. A primeira execução em Python 3.11 teve falhas de compatibilidade Windows (junction e PID do launcher), preservadas no log.
- `windows-regression-py312.log`: repetição integral dos dois grupos afetados no Python 3.12.10, 53 testes, 52 PASS e um skip POSIX. Todos os erros/falhas anteriores desses grupos foram resolvidos pela escolha do runtime, sem alterar seus testes ou o produto.
- Considerando a repetição, a seleção integrada tem 216 PASS e oito skips: sete integrações SER01 em clone integral exigem opt-in/evidência externa e um caso exige symlink POSIX. Esses casos não são alegados como executados.
- `baseline-monitor-final.log`: 11 PASS após fechamento de partições/janelas, incluindo dois casos novos com Receipt reconstruído. `explainability-final.log`: nove PASS após alinhamento SER02. Sem contar repetições, são 275 casos aprovados e dez não executados nesta seleção.
- `helpers-tests.log`: 45 PASS nos helpers; `concierge-tests.log`: 12 PASS e dois skips por permissão de symlink Windows.
- `environment.json`: versões completas. Runtime dos candidatos: Python 3.11.15, SHAP 0.44.1, NumPy 1.26.4, pandas 2.2.3, SciPy 1.14.1, scikit-learn 1.5.2, Spark 3.5.3 e Java 17. Dependências isoladas em `.artifacts/`, sem alteração global.
- `validate-assistant.log` e `render.log`: gate final APROVADO com zero falhas/avisos e geração de 634 arquivos (incluindo marcador). Os 633 arquivos da fonte foram conferidos byte a byte no espelho; todos os manifests conferem. A auditoria estrutural encerrou ambos os achados, com 38/38 hashes conferidos independentemente nos três perfis finais.

Para repetir uma rota, usar `python -B -m unittest tools.tests.test_ser04_candidate` (Estatística), `test_ser05_diagnostic` (Cross-EDA), `test_ser07_feature_engineering`, `test_skill_enforcement_explainability`, `test_ser09_baseline_candidate`, `test_ser11_monitor_candidate` ou `test_ser13_pipeline_spec`, sempre com o prefixo `tools.tests.`. Safra/EDA permanecem cobertas por `test_ser_b1_domains`, `test_skill_enforcement_se04_runner` e `test_skill_enforcement_se05_runner`. Spark requer JAVA_HOME para Java 17, PYSPARK_PYTHON para o Python isolado e SPARK_LOCAL_IP=127.0.0.1.

## Auditoria e limites

A auditoria independente encerrou os achados de representação float64, ordem das features, métricas adulteradas, sigmoid extremo e replay. A regressão adversarial altera payloads e recalcula Receipt para exigir conferência semântica, além de detectar hashes obsoletos, mutações e falhas de helpers.

Receipt e hashes comprovam consistência dos artefatos sob os inputs externos esperados; não autenticam usuário nem constituem atestado remoto. A conferência do p-valor KS reutiliza SciPy e não é um oráculo estatístico independente. Diagnóstico local não equivale a aceitação do domínio corporativo. Warnings de timezone, parsing, Hadoop nativo/winutils e sockets Spark foram observados sem falha dos testes sintéticos.

A auditoria estrutural também identificou campos extras não verificados em partições/janelas e a identificação de Explainability como SER05. A correção fecha as coleções esperadas e alinha Explainability à frente canônica SER02, com regressão do contrato.

O gate documental identificou falsos positivos em duas referências Git abreviadas já existentes; foram expandidas para seus hashes completos, preservando a referência histórica e a regra de privacidade.

Próximas etapas que exigem autorização específica: promoção de policy, homologação Genie/Databricks, publicação, execução com dados/workspaces reais ou merge. A implementação ampla de PIT, pipelines com efeitos e demais perfis fora dos contratos acima não é declarada concluída.
