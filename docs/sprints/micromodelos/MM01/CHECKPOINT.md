# MM01 — Checkpoint

Status: **CANDIDATA TÉCNICA PRONTA PARA A1; NÃO ACEITA; NÃO INTEGRADA**

## Base e superfície

- `main` inicial: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- base reconciliada após integração/fechamento da V10: `a9480391c78e2402986885db0ce08b10e0619a1a`;
- branch: `micromodelos/mm01-contrato-canonico`;
- PR: `#51`;
- MM00: encerrada e integrada;
- MM02: bloqueada até A1, aceite e merge desta sprint.

## O que a candidata entrega

1. schema formal `1.0.0` para `micromodelo.yaml`;
2. template YAML inicial válido e sanitizado;
3. máquina de fases com rework explícito e `PUBLICADO` terminal por versão;
4. condições operacionais ortogonais (`ATIVO`, `BLOQUEADO`, `SUSPENSO`, `DEPRECATED`);
5. proveniência `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO`, `MEDIDO` com gates próprios;
6. proteção explícita de `FALSE` versus `INDETERMINADO`, inclusive contra equivalência apenas cosmeticamente diferente;
7. score 0–100 com semântica/normalização e calibração medida antes de linguagem probabilística;
8. gates humanos para limiares, pesos, validação, regras materiais e política de publicação;
9. escopo de fontes fail-closed em `CATALOGO_PRODUTO`, sem override de CLI;
10. recusa de chaves duplicadas em YAML/JSON e de IDs duplicados em coleções controladas;
11. conteúdo material mínimo obrigatório ao entrar em `EM_VALIDACAO`;
12. coerência entre fase e status da interface de publicação, com caminhos positivos testados até `PUBLICADO`;
13. fronteira de tracking preservada para MM06;
14. validador de referência/CI, fixtures sintéticos e suíte com 17 métodos de teste;
15. gate permanente `.github/workflows/micromodelos-mm01-ci.yml`, read-only e sem acesso a ambiente corporativo;
16. pacote neutro para auditoria A1 independente.

## O que não foi feito

- não foi criada `hub-ml-micromodelos`;
- não foi alterada a lista de skills roteáveis;
- não foi criado sétimo tipo em `hub_padroes`;
- não foi criado fingerprint;
- não houve descoberta de metadata;
- não houve leitura de dados;
- não houve alteração de `mlflow_run`;
- não houve integração visual específica da MM01; V10 foi somente absorvida como base;
- não houve handoff/publicação real;
- não houve migração de legado.

## Evidência técnica pré-A1

- materialização validada: run `34899617125`, `success`;
- reconciliação fail-closed com `main@a9480391c78e2402986885db0ce08b10e0619a1a`: run `34900062786`, `success`;
- gate permanente após endurecimento adversarial: run `34903052597`, `success`;
- gate permanente após teste do caminho positivo de publicação: run `34903285176`, `success`;
- V00, V01 e V02 também ficaram verdes no mesmo head técnico;
- failure histórico de transporte `34899029039` preservado como failure e separado de resultado funcional.

A descrição da PR #51 registra os checks da **árvore final** após a última mudança documental. Não se fará commit apenas para copiar o SHA/run ID do próprio commit para este arquivo.

## Gate independente pendente

A única etapa de qualidade que deve ocorrer fora desta sessão antes do contraditório final é a **auditoria A1 independente** preparada em:

```text
docs/auditoria/2026-09-14_micromodelos-mm01/
├── 01_contexto.md
└── 02_prompt_auditoria.md
```

O contexto A1 foi conferido contra os nomes reais dos ADRs versionados. O auditor deve executar a candidata e criar casos adversariais próprios; não deve implementar correções.

## Gates restantes

1. confirmar checks da árvore documental final e estabilidade da `main`;
2. executar A1 em sessão independente;
3. confrontar cada achado com a árvore;
4. corrigir/retestar apenas achados procedentes;
5. apresentar checkpoint final para aceite explícito;
6. integrar a PR #51 somente após o aceite.

Enquanto qualquer item acima estiver pendente, **MM02 permanece bloqueada**.
