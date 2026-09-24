# B0 — mecanismo comum da execução paralela SER

Estado de autoria: **CORRECTED_CANDIDATE / FULL_CHECKOUT_REVALIDATION_PENDING / LOCAL_QUALIFICATION_PENDING**.

B0 implementa apenas a infraestrutura local comum. Não promove skill, não altera `policy.json`, não publica no Databricks e não autoriza SER02–SER14. O executor B0 opera o repositório em `READ_ONLY`; preparação mecânica de renderer/snapshot permanece serial e fora dos workers.

Pacotes: B0.1 governança, B0.2 cobertura/contratos, B0.3 executor, B0.4 verifier/bundle, B0.5 host qualification, B0.6 dois pilotos sintéticos e B0.7 revisão de liberação.

## Corretiva pós-revisão adversarial

A revisão independente da primeira candidata encontrou sete grupos bloqueantes no verificador, gate dos pilotos, allowlist do registry e protocolo de evidência. A candidata corrigida fecha esses grupos antes de qualquer freeze local:

- o registry B0 aceita somente os seis `command_id` e argv exatos versionados; expansão é mudança repo-side;
- o verificador rederiva DAG, ondas, dependências, stop global, first failure, limites de paralelismo/auditoria/recurso, exclusividade, bindings de task/SHA/effect e binding de cada command record ao registry e aos bytes persistidos;
- resultados de campanha são terminais; `PASS` com issue pendente, comando não vinculado ou evidência inconsistente é inválido;
- os pilotos selective/global têm topologia, waves, roles, blockers e `exit_code=1` deliberado verificados independentemente;
- stdout/stderr RAW são persistidos e hasheados como bytes exatos, sem normalização de newline;
- o envelope probatório V3 usa `RAW/` e `SHARE/` com manifestos internos fechados e `RAW_SHARE_BINDING.json` externo aos dois manifestos, evitando circularidade;
- somente o `MANIFEST.json` raiz de cada bundle é autoexcluído; manifestos aninhados e symlinks entram na regra de integridade;
- conteúdo SHARE não decodificável não pode produzir secret-scan PASS;
- cobertura vazia só é `MAPPED` quando há classificação explícita como `COMMAND_INVARIANT`; exceções stale são bloqueantes.

A suíte B0 passa a conter **69 metatestes**. Nesta autoria corretiva, 65 testes funcionais/negativos puderam ser executados de forma isolada e passaram; os quatro testes documentais dependem do checkout completo e permanecem para a revalidação no SHA publicado. Esse resultado de autoria não é qualificação Windows.

## Próximo gate

Antes do freeze, revalidar a suíte completa de 69 testes e o coverage inventory no checkout real do novo SHA. Se verdes e sem finding funcional novo, executar `python -B -m tools.skill_enforcement.parallel.freeze_prepare --apply`: ela mede o snapshot pelo validador e pode alterar somente `README.md`; depois o operador revisa o diff e cria o commit de freeze.

Somente então a qualificação local executa `python -B -m tools.skill_enforcement.parallel.b0_release --output-dir <DIR_EXTERNO_NOVO>`. O qualificador cria um envelope V3 com `RAW/`, `SHARE/`, binding externo e manifesto do envelope. Um PASS funcional com `release_status=PENDING_HOST_QUALIFICATION` não é `LOCAL_QUALIFIED`; Windows/NTFS e sandbox/host continuam precisando de prova efetiva.
