# SE04 — guia para usuário não técnico

## Três ideias simples

**ExecutionTraceV0** é o registro técnico do que aconteceu durante a execução.

**ExecutionReceiptV1** é o comprovante formal que liga aquele registro ao resultado e à versão esperada da execução canônica.

**SE05** será, no futuro, a regra que impedirá uma conclusão homologada quando esse comprovante não for válido. A SE04 ainda não faz esse bloqueio automático.

## Resultado correto não é a mesma coisa que execução homologada

Um código manual pode produzir números corretos. Isso prova, no máximo, que a tarefa foi resolvida tecnicamente. Não prova que o caminho canônico da skill foi usado.

Na SE04, a evidência formal é um Receipt válido. Uma solução manual não deve receber um Receipt retroativo só porque o resultado parece igual.

## Como ler os estados

- `VALID`: o comprovante corresponde ao run, trace, resultado e release verificados;
- `ABSENT`: não há comprovante;
- `MALFORMED`: o comprovante está incompleto ou com formato inválido;
- `INVALID`: o próprio comprovante foi alterado ou não fecha internamente;
- `INCOMPATIBLE`: o comprovante não corresponde ao trace, resultado ou release apresentados;
- `STALE_REPLAYED`: o comprovante pertence a outro run quando comparado ao run atual esperado;
- `UNSUPPORTED_VERSION`: a versão do comprovante não é suportada.

Somente `VALID` representa canonical compliance formal da SE04.

## O que fazer quando não for `VALID`

1. não fabricar nem editar o Receipt;
2. não copiar Receipt de execução anterior;
3. conferir se `scripts/run.py` foi realmente usado;
4. verificar se integridade, provenance e preflight passaram;
5. verificar se a primitive protegida concluiu sem fallback;
6. executar novamente pela rota canônica quando apropriado;
7. se o problema persistir, entregar o estado e os códigos de erro ao responsável técnico.

## Onde está a evidência

O payload do runner contém três partes:

```text
trace   = registro técnico
receipt = comprovante formal ou null
result  = resultado de negócio
```

O Receipt não copia os dados/resultados completos; ele usa digests para vincular o comprovante ao conteúdo correspondente.

## O que a SE04 ainda não faz

A ausência de Receipt `VALID` ainda não dispara, sozinha, um bloqueio universal da resposta final. Essa política será implementada exclusivamente na SE05. Portanto, a SE04 deve ser usada para **verificar e classificar a evidência**, não para alegar que o postflight final já existe.
