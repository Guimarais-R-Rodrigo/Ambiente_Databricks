# Micromodelos — contrato L1

Esta pasta contém a skill conversacional L1/audit, sem runner protegido L3. O [módulo de domínio](../../hub_micromodelos/README.md) contém validação, adapter metadata-only e exemplos; seu uso exige chamada explícita e permissões próprias. [Jornada](../../hub_micromodelos/guias/README.md): em `OBJETIVO_CONHECIDO`, informe decisão, entidade e tempo; em `DESCOBRIR_OPORTUNIDADES`, forneça catálogo/escopo autorizado para hipóteses com origem e incerteza.

A skill [hub-ml-micromodelos](SKILL.md) orienta a especificação progressiva de
`micromodelo.yaml` e a descoberta de oportunidades a partir de metadata. O
[contrato estático](execution_contract.json) declara L1 em modo audit. L2/L3
são direção de evolução; esta pasta não contém preflight, runner, Receipt nem
adapter Databricks para descoberta executável.

Para usá-la, declare decisão ou área, ambiente, fonte lógica e permissões. Peça
primeiro um plano ou rascunho com lacunas explícitas. Exemplo sintético:

```text
@hub-ml-micromodelos Quero especificar uma característica de recência para um
micromodelo de resposta. Tenho apenas uma descrição de catálogo sintético; ainda
não conheço chave, instante de decisão ou disponibilidade da fonte. Entregue um
rascunho de requisitos e pendências sem consultar registros ou afirmar medição.
```

Esta skill orienta planejamento e especificação. A biblioteca de domínio e os exemplos têm chamadas explícitas; sua disponibilidade não aprova dados, modelos ou publicação.
