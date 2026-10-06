# Template de auditoria

## Uso

Pasta: `docs/auditoria/YYYY-MM-DD_<tema>/`. O contrato necessário está na
[regra local](../rules/colaboracao.md#auditoria); não requer repositório irmão.
Use A0_light (1 origem), A1_standard (2 independentes), A2_strict (3 independentes)
ou A3_incident (3+ independentes), com justificativa. Auxiliares da mesma sessão
não satisfazem sozinhos independência. Não baixar rigor quando houver dados
sensíveis, produção, publicação externa ou decisão para squad/missão.

Modelo não executável: `launchable=false`, `execution_authorized=false`.
Executar teste/consulta fora da revisão somente com autorização específica;
preencher formulário não é aprovação. Resultados ausentes ficam NOT_RUN;
evidência que o ambiente não permite observar fica NOT_OBSERVABLE.

## Modelo

```markdown
# 01_contexto — <tema>

Data: <YYYY-MM-DD> · Branch: <branch> · Base/head SHA: <hashes>
Nível: <A0_light/A1_standard/A2_strict/A3_incident>
Motivo e gatilhos: <por que esse nível; A1+ quando aplicável>
Modo: <contexto completo ou cego com prova de sessão inicial>
launchable=false
execution_authorized=false
Estado inicial dos testes: NOT_RUN
Observabilidade não demonstrada: NOT_OBSERVABLE

## Escopo e autoridade
<Arquivos/efeitos permitidos; fora do escopo; origem da autorização e limites.>
<Não incluir credenciais, dados/paths/identificadores corporativos ou PII.>

## Corpus e independência
Permitido: <manifesto com paths, SHA/hash e versão por auditor>
Proibido: <histórico, conclusões ou arquivos excluídos>
Recebido efetivamente: <contexto/diagnóstico de cada sessão>
Autores/revisores: <identidades reais e quem escreveu cada lote>
Origens independentes: <prova; se ausente, requisito BLOCKED>
<Cegueira inválida se corpus proibido já recebido; registrar contexto completo.>

## Rodadas
02_<auditor1>.md, 03_<auditor2>.md, 04_<auditor3>.md conforme nível.
Cada rodada: achado/ID, severidade, arquivo/linhas, prova, impacto, correção,
teste esperado/observado, versão/ambiente e estado. Não herdar PASS alheio.

# 99_consenso
<Consensos, divergências, decisão/autoridade e riscos residuais.>
Ações priorizadas: <owner, escopo, gate e evidência para verificar cada ação>.
Divergência sem solução: PENDENTE/DECISAO, <owner e condição de retomada>.
Limites: <BLOCKED/NOT_RUN; sem converter cobertura parcial em aceite total>.
```
