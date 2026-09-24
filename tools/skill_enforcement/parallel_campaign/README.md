# SER Parallel Campaign — B0 foundation

Mecanismo local comum para executar **comandos já aprovados** em campanhas SER paralelas. Não cria implementação de domínio, não promove `policy.json`, não concede autoridade humana e não faz merge/publicação.

## Comandos implementados

- `lint`: valida schema, DAG, command IDs e paths.
- `inventory`: enumera métodos `test_*` por AST, sem importar as suítes.
- `diagnose`: executa campanha diagnóstica declarada.
- `certify`: executa campanha congelada declarada.
- `verify`: reconstrói o veredito a partir dos resultados persistidos.
- `qualify-host`: coleta fatos locais básicos; sandbox/modelos Codex continuam pendentes até prova do cliente.
- `package` / `verify-zip`: cria SHARE com identidade própria e rejeita ZIP traversal/symlink.

O registry usa `argv` em lista e nunca `shell=True`. Placeholders permitidos são tokens inteiros `{python}`, `{repo}`, `{evidence}` e `{task_id}`. O launcher detecta alterações Git e fingerprints de paths protegidos; isso não substitui sandbox do sistema operacional. B0.5 precisa demonstrar permissões efetivas no host local.
