# SE05 — guia de operação para usuário não técnico

## O que mudou

Antes da SE05, a skill podia produzir um resultado com Receipt válido, mas isso ainda não significava que todos os requisitos da entrega final tinham sido satisfeitos.

Com a SE05, existe uma etapa final chamada **postflight**.

Ela funciona como uma conferência de saída:

```text
execução
  → evidências
  → Receipt
  → postflight
  → conclusão autorizada ou recusada
```

## O que significa “concluída” agora

Para a `hub-ml-eda-profissional`, uma execução só deve ser apresentada como concluída com aderência ao contrato quando aparecer:

```text
postflight.status = PASS
completion.authorized = true
completion.status = COMPLETED
```

Qualquer outra combinação significa que ainda existe um requisito não satisfeito, uma lacuna de evidência ou algo que precisa de revisão.

## Estados possíveis

### PASS

Tudo que o gate consegue provar e que era obrigatório para aquele contexto foi satisfeito. A conclusão pode ser homologada.

### FAIL

Há um requisito material aplicável que não foi satisfeito. Exemplo: um helper obrigatório deveria ter sido chamado, mas não foi.

### BLOCKED

O gate não possui evidência confiável suficiente para decidir. Exemplo: Receipt inválido, artifacts adulterados ou configuração de postflight ausente.

### REVIEW

A execução não pode ser homologada automaticamente. Exemplo: handoff obrigatório incompleto.

`REVIEW` não é PASS.

## O que a Genie Code deve fazer

Para uma EDA completa homologada, a sequência esperada é:

1. usar `scripts/run_enforced.py`;
2. preencher o handoff final;
3. usar `scripts/postflight.py`;
4. verificar se `completion.authorized=true`;
5. somente então declarar a execução concluída com aderência ao contrato.

## O que não significa erro da análise

Se o postflight reprovar, isso não quer dizer automaticamente que todos os números da EDA estão errados.

Exemplo: uma pessoa pode calcular corretamente uma estatística manualmente. Mesmo assim, se o contrato exigia um helper canônico e não existe evidência de uso, a execução não pode ser homologada como aderente.

A SE05 separa:

```text
task correctness
≠
contract compliance
```

## Exemplos

### Exemplo A — tudo correto

- `quick_profile`, `data_quality_check` e `null_summary` executados;
- templates obrigatórios carregados;
- Receipt válido;
- handoff completo.

Resultado:

```text
Postflight = PASS
Completion = COMPLETED
```

### Exemplo B — faltou chave para qualidade

O usuário não informou `pk_columns`. O executor não inventa uma chave.

Resultado esperado:

```text
data_quality_check = sem call/completion
Postflight = FAIL
Completion = NOT_COMPLETED
```

A correção é fornecer a chave correta e executar novamente; não marcar o helper como usado manualmente.

### Exemplo C — handoff incompleto

A análise rodou, mas `quality_risks` não foi preenchido.

Resultado:

```text
Postflight = REVIEW
Completion = NOT_COMPLETED
```

## O que conferir antes de aceitar uma entrega

Procure estes quatro pontos:

```text
Receipt verifier = VALID
Postflight        = PASS
Completion        = COMPLETED
Authorized        = true
```

Se algum deles não estiver correto, a execução não está homologada no nível L4.

## O que a SE05 não faz

- não garante que toda interpretação de negócio esteja correta;
- não substitui revisão humana em decisões materiais;
- não garante que a Genie Code sempre escolherá espontaneamente a rota certa;
- não aplica L4 automaticamente às demais skills;
- não publica nada no ambiente corporativo.

## Quando pedir ajuda

Se a conclusão vier `FAIL`, `BLOCKED` ou `REVIEW`, use `postflight.issues` para identificar o item. Cada issue contém código, mensagem e, quando aplicável, o recurso/template/handoff relacionado.

Não resolva um issue apenas alterando o JSON final. A evidência precisa nascer da execução correspondente.
