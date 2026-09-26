# Codex Autonomous Controller — runtime qualification

Versão: 1.0  
Decisões donas: ADR-0024 + ADR-0025

Esta qualificação prova a configuração **efetiva** do cliente Codex. Ler TOML no
Git não prova que a camada project-scoped foi carregada nem que overrides do
usuário/CLI/managed policy preservaram as permissões esperadas.

## Gate CQ0 — project root e trust

A sessão deve começar na raiz Git do repositório. A configuração project-scoped
só é válida se o projeto estiver trusted.

Quando disponível no cliente, usar:

```text
/status
/debug-config
```

Registrar sem segredos:

- project root;
- fonte da camada `.codex/config.toml`;
- modelo/effort efetivos;
- approval policy;
- sandbox/permission mode;
- writable roots;
- overrides de maior precedência.

Se a camada project-scoped estiver ignorada, parar:

`BLOCKED_CONTROLLER_PROJECT_TRUST`.

## Gate CQ1 — strict config

Quando o CLI estiver disponível, executar uma validação de configuração em modo
strict antes do primeiro trabalho material. O objetivo é reprovar chave
desconhecida, não abrir outra sessão autônoma.

Se o cliente não expuser uma forma não destrutiva de strict-config, registrar
`STRICT_CONFIG_NOT_OBSERVABLE` e confiar apenas nos demais gates; não inventar
PASS.

## Gate CQ2 — roles

Confirmar que os cinco custom agents estão discoverable:

- explorer;
- executor;
- domain-auditor;
- evidence-auditor;
- architecture-auditor.

Cada arquivo project-scoped precisa de `name`, `description` e
`developer_instructions`.

## Gate CQ3 — effective permissions

Esperado para o root:

```text
model = gpt-6-astra
reasoning = high
sandbox = workspace-write
approval = on-request
reviewer = user
```

Esperado para subagentes:

- explorer/auditors: read-only;
- executor: workspace-write;
- nesting: disabled.

O sandbox padrão do Codex protege `.git`, `.codex` e `.agents` dentro do
workspace, mas isso não prova todo o `repo_scope` do envelope. Os hooks e o
delta checker são defesa adicional.

## Gate CQ4 — hooks

Confirmar que a camada trusted carregou `.codex/hooks.json`.

Prova mínima:

1. patch sintético em path permitido deve ser aceito apenas em clone/scratch
   descartável ou por inspeção do hook; não alterar produto para “testar”;
2. tentativa de patch em path `HUMAN_GATE_REQUIRED` deve ser negada antes da
   escrita;
3. o post-hook deve detectar worktree fora de A1 se uma escrita indireta for
   simulada em fixture descartável.

Hooks são guardrail, não uma fronteira de segurança completa. Resultado do hook
não substitui sandbox nem revisão do delta.

## Gate CQ5 — controller validators

Executar no ambiente de manutenção já preparado:

```text
python -B tools/validate_codex_autonomy.py --json
python -B -m unittest tools.tests.test_codex_autonomy -v
```

Se qualquer gate CQ0–CQ5 material falhar, parar antes de assumir B1. Defeito em
governança do controller exige `CONTROLLER_MAINTENANCE`; não é reparado pelo
próprio A1 executor.

## Saída

Emitir um resumo:

```text
CONTROLLER_RUNTIME_QUALIFICATION = PASS | BLOCKED | FAIL
PROJECT_CONFIG_LOADED = true|false|NOT_OBSERVABLE
STRICT_CONFIG = PASS|FAIL|NOT_OBSERVABLE
CUSTOM_AGENTS = 5/5 | ...
EFFECTIVE_ROOT_PERMISSIONS = PASS|FAIL|NOT_OBSERVABLE
HOOKS = PASS|FAIL|NOT_OBSERVABLE
VALIDATOR = PASS|FAIL
METATESTS = PASS|FAIL
```

Nenhum desses gates concede A2.
