---
name: evoluir-hub
description: Planeja e implementa incrementos na fonte do Hub, localizando padrões, contratos, consumidores e verificações adequadas. Use para mudanças no projeto, não para executar análise de dados de usuário.
---
# Evoluir a fonte do Hub

Comece por [fontes e derivados](../../../docs/ai/rules/fontes-e-derivados.md),
[documentação](../../../docs/ai/rules/documentacao.md) e
[padrões do produto](../../../ambiente_databricks/.assistant/hub_padroes/README.md).

Localize owner, padrão existente e consumidores antes de criar objeto. Para
mudança de arquitetura, registre ADR; preserve decisões e evidências fechadas.
Edite produto em `ambiente_databricks/`; use parâmetros e caminhos relativos.
Destinos pessoais vêm da configuração local, nunca de valores fixados na fonte.

Implemente no escopo pedido, incluindo README de objeto quando aplicável.
Valide fonte e contratos afetados. Se o produto mudou, trate o render com o
preflight da skill correspondente; publicação e instalação têm escopo próprio.
Registre comportamento, arquivos, evidência e limites no owner da tarefa.

Casos esperados: adicionar helper ao Hub → localizar contrato e implementar;
treinar modelo com dados corporativos → fluxo de produto autorizado;
dependência ausente → registrar bloqueio, sem enfraquecer o gate.
