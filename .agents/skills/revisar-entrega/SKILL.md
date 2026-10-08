---
name: revisar-entrega
description: Revisa uma mudança do repositório antes de entrega, conferindo diff, contratos, documentação, evidência e pendências de transporte, sem publicar ou instalar por associação.
---
# Revisar uma entrega

Leia [colaboração](../../../docs/ai/rules/colaboracao.md) e
[gates](../../../tools/README.md). Fixe SHA/base, diff e escopo.

Confronte comportamento pedido com implementação e seus consumidores; procure
perda de conteúdo, caminhos locais, segredos, política duplicada e efeitos não
autorizados. Consulte evidência dos comandos; execute verificações locais
pertinentes quando autorizado. Priorize problemas reproduzíveis e riscos materiais.

Declare resultado por gate: PASS, FAIL, NOT_RUN ou BLOCKED. Não transforme teste
estático em runtime, descoberta nativa ou homologação corporativa. Declare
autorrevisão/contexto completo e origem efetiva; revisão na mesma sessão não
satisfaz independência A1. Entregue achados com arquivo, impacto e correção.

Casos esperados: revisar diff para PR → avaliar contratos e evidência; pedido de
publicação → procedimento específico; prova remota ausente → manter NOT_RUN,
sem preencher resultado por inferência.
