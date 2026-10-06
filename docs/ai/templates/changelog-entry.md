# Template de changelog

## Uso

Adicione sob a data real da sessão; crie `## YYYY-MM-DD` se necessário. Subseções
na ordem Adicionado, Atualizado, Corrigido, Removido, Notas, omitindo vazias.
Cada item identifica autor efetivo entre parênteses, sem fornecedor fixo.
Itens curtos, de uma a três linhas, citam arquivos e evidência/limites. Não incluir
identificadores corporativos, PII ou segredos; não reescrever datas passadas.

Modelo não executável: `launchable=false`, `execution_authorized=false`.
Um registro de plano não afirma execução e não autoriza a próxima ação.

## Modelo

```markdown
## <YYYY-MM-DD>

### Adicionado
1. (<autor real>) <arquivo>: <mudança efetiva e finalidade>.

### Atualizado
1. (<autor real>) <arquivo>: <delta e escopo preservado>.

### Corrigido
1. (<autor real>) <arquivo>: <defeito e prova da correção>.

### Removido
1. (<autor real>) <arquivo>: <remoção autorizada e rota substituta>.

### Notas
- (<autor real>) <comando/ação, SHA, resultado observado e limite>.
- (<autor real>) <teste ainda não executado>: NOT_RUN; <destino sem prova>: NOT_OBSERVABLE.
- (<autor real>) <bloqueio, owner e próxima condição, sem concessão de execução>.
```
