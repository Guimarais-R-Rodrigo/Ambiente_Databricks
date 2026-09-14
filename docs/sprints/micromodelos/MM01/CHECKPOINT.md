# MM01 — Checkpoint

Status: **CANDIDATA; NÃO ACEITA; NÃO INTEGRADA**

## Base

- `main` congelada no início: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- branch: `micromodelos/mm01-contrato-canonico`;
- MM00: encerrada e integrada;
- MM02: bloqueada até aceite e merge desta sprint.

## O que a candidata entrega

1. schema formal `1.0.0` para `micromodelo.yaml`;
2. template YAML inicial válido;
3. máquina de fases com rework explícito e `PUBLICADO` terminal por versão;
4. condições operacionais ortogonais (`ATIVO`, `BLOQUEADO`, `SUSPENSO`, `DEPRECATED`);
5. proveniência `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO`, `MEDIDO` com gates próprios;
6. proteção explícita de `FALSE` versus `INDETERMINADO`;
7. score 0–100 com semântica/normalização e calibração obrigatória antes de chamar de probabilidade;
8. gates humanos para limiares, pesos, validação e política de publicação;
9. fronteira de tracking preservada para MM06;
10. validador de referência/CI e fixtures sintéticos.

## O que não foi feito

- não foi criada `hub-ml-micromodelos`;
- não foi alterada a lista de skills roteáveis;
- não foi criado sétimo tipo em `hub_padroes`;
- não foi criado fingerprint;
- não houve descoberta de metadata;
- não houve leitura de dados;
- não houve alteração de `mlflow_run`;
- não houve integração visual;
- não houve handoff/publicação real;
- não houve migração de legado.

## Gates ainda pendentes

- CI permanente sobre o head final da branch;
- auditoria A1 independente;
- verificação dos achados da A1;
- correções/reteste, se houver;
- atualização final de `TESTES.md`/checkpoint;
- aceite explícito do usuário;
- merge.

Enquanto qualquer item acima estiver pendente, a MM02 permanece bloqueada.
