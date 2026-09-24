# B0 — mecanismo comum da execução paralela SER

Estado de autoria: **CORRECTED_CANDIDATE / FULL_CHECKOUT_METATESTS_PENDING / LOCAL_QUALIFICATION_PENDING**.

B0 implementa apenas a infraestrutura local comum. Não promove skill, não altera `policy.json`, não publica no Databricks e não autoriza SER02–SER14. O executor B0 opera o repositório em `READ_ONLY`; preparação mecânica de renderer/snapshot permanece serial e fora dos workers.

Pacotes: B0.1 governança, B0.2 cobertura/contratos, B0.3 executor, B0.4 verifier/bundle, B0.5 host qualification, B0.6 dois pilotos sintéticos e B0.7 revisão de liberação. A corretiva pós-revisão fecha RV-01–RV-07 com allowlist exata, verificação independente de DAG/ondas/limites/bindings, logs byte-bound, RAW/SHARE não circular e secret scan fail-closed. A suíte versionada contém 52 métodos; o PASS histórico de 39/39 não vale para o SHA corretivo.

Antes do freeze, o checkout real deve passar `python -B -m unittest tools.tests.test_ser_parallel_b0 -v` e `python -B -m tools.skill_enforcement.parallel.coverage`. Depois, a preparação mecânica executa `python -B -m tools.skill_enforcement.parallel.freeze_prepare --apply`: ela mede o snapshot pelo validador e pode alterar somente `README.md`; depois o operador revisa o diff e cria o commit de freeze. Em seguida, a qualificação local executa `python -B -m tools.skill_enforcement.parallel.b0_release --output-dir <DIR_EXTERNO_NOVO>`. Um PASS funcional com `release_status=PENDING_HOST_QUALIFICATION` não é `LOCAL_QUALIFIED`; sandbox/host ainda precisam de prova efetiva.
