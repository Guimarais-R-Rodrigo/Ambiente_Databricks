# Template de changelog

## Uso

`CHANGELOG.md` da raiz reúne marcos que alteram uso, arquitetura, compatibilidade,
contrato, distribuição ou risco material. Use a data real e a autoria efetiva,
sem fornecedor fixo; cada marco resume efeito e limite em uma a três linhas,
com links para decisão, owner e prova quando necessários.

Toda sessão com alteração continua rastreável, mas comandos, contagens, tentativas,
rebase e recibos pertencem ao owner da execução: teste/auditoria datados, handoff
quando há trabalho aberto, ou commit/PR para manutenção trivial. Não criar outro
diário obrigatório nem duplicar a mesma evidência em vários índices.

A entrada consolidada também contém uma síntese da trajetória do plano,
conforme o ADR-0030. Atualize essa síntese somente ao consolidar uma nova etapa;
não acrescente diário, inventário ou comandos nela.

Metas editoriais da entrada consolidada: até 12 marcos recentes, 200 linhas e
16 KiB no total, contando a síntese. Ao exceder, preserve a trajetória e faça
outro snapshot verificável dos marcos, com índice, commit e hashes, antes de
curar a raiz. São metas de leitura, não limites de modelo nem permissão para
excluir fatos. [Arquivo preservado](../../historico/changelog/README.md).

Não incluir identificadores corporativos, PII ou segredos. Não reescrever datas,
autoria, ADR aceito ou provas congeladas. Erratas entram com nova data e referência.
Um resultado PASS vale apenas para o SHA, ambiente e escopo observado; conserve
FAIL, NOT_RUN, BLOCKED e NOT_AUTHORIZED quando aplicáveis.

Modelo não executável: `launchable=false`, `execution_authorized=false`.
Um registro de plano não afirma execução e não autoriza a próxima ação.

## Modelo

```markdown
## <YYYY-MM-DD>

- (<autor real>) <mudança efetiva e impacto de uso/contrato>. <Limite material>.
  [Decisão](<ADR>) · [Estado e prova](<owner da frente ou evidência datada>).
```

Para detalhar uma execução, use o template de teste/auditoria da frente ou o
[handoff](handoff.md), informando SHA, arquivos, comandos, esperado, observado,
exit code, ambiente, bloqueios e condição de retomada. Atualizar um registro não
concede autorização para executar suas próximas ações.
