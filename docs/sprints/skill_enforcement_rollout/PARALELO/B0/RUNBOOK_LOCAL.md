# B0 — runbook de qualificação local

Este runbook é execução, não autoria. Não editar arquivos funcionais durante a campanha.

1. Reconfirmar `origin/main`, branch B0, merge-base, ahead/behind, shallow=false e worktree clean.
2. Instalar apenas dependências já declaradas em `tools/requirements-dev.txt`; não instalar no meio da certificação.
3. Rodar `python -B -m unittest tools.tests.test_parallel_campaign_b0 -v`.
4. Rodar os gates estruturais existentes (`validate_assistant`, contracts, policy) e regressões do certifier/SE08 em canal definido pela campanha B0.
5. Gerar method inventory a partir de `coverage_patterns.json`; nenhum pattern obrigatório pode ficar sem classificação por razão conhecida.
6. Executar `qualify-host` e completar client/model/sandbox probes do formulário.
7. Materializar `pilot_campaign.template.json` com HEAD/tree reais em arquivo de evidência externo, sem editar o template versionado.
8. Executar o piloto sintético uma vez. Esperado: `independent_pass=PASS`, `deliberate_fail=FAIL`, `dependent_blocked=BLOCKED_DEPENDENCY`, `independent_after_fail=PASS`; a campanha global é FAIL deliberado, mas o isolamento é PASS quando somente a cadeia dependente é bloqueada.
9. Auditar locks, mistura de evidência, repo mutation, first failure, RAW/SHARE e ZIP adversarial.
10. B0.7 somente após relatório independente. Não iniciar SER03/SER05 antes do aceite humano do B0.
