# Template de handoff

## Uso

Arquivo: `docs/handoffs/YYYY-MM-DD_<tema>.md`. Escreva para alguém que chega sem
conversa anterior. Dados sanitizados, branch/SHA conferíveis, links/arquivos e
critérios explícitos tornam a retomada independente da memória do executor.

Modelo não executável: `launchable=false`, `execution_authorized=false`.
A autorização deve ser reobtida da fonte aplicável quando ausente; o handoff ou
a sugestão de próximo passo não a concede. Não preencher PASS por expectativa.

## Modelo

```markdown
# Handoff — <tema>

Data: <YYYY-MM-DD> · De: <pessoa/agente/sessão reais> · Para: <responsável>
Repositório/branch: <identificação sanitizada>
Base/head SHA e árvore: <hashes verificáveis>
launchable=false
execution_authorized=false

## Escopo e autoridade
<Pergunta/objetivo; arquivos permitidos; efeitos autorizados e referência da
aprovação original; efeitos que ainda dependem de decisão.>

## Estado atual e evidência
<Arquivos/diff, testes com comandos/versões/ambiente/exit code, resultado real,
links sanitizados e limitações. Ausente: NOT_RUN; não observável: NOT_OBSERVABLE.>

## Em andamento ou bloqueado
<Item, motivo, owner, impacto e condição precisa para retomar.>

## Decisões tomadas
- <Decisão e referência a ADR/changelog; não confundir proposta com aceite>.

## Próximos passos recomendados
1. <Passo verificável, pré-condição, gate e quem decide/autoriza>.

## Armadilhas e reversão
<O que não fazer; alterações alheias a preservar; rollback seletivo e prova
necessária. Não presumir credenciais/acesso/sessão nem usar reset destrutivo.>
```
