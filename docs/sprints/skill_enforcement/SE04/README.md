# SE04 — Execution Receipt formal

## Estado

**BOOTSTRAP ARQUITETURAL — implementação ainda não concluída.**

Branch: `sef/SE04-execution-receipt`  
Baseline: `main@216df1544c2b21a8ff94bb5ce51fd84b8a444057`  
Skill piloto: `hub-ml-eda-profissional`  
Contrato vigente: v0.1, `mode="audit"`.

## Objetivo

Transformar a evidência estrutural da SE03 em um `ExecutionReceiptV1` formal, versionado, verificável e auditável, emitido somente a partir de uma execução canônica válida do runner.

A SE04 deve tornar verificável a pergunta:

> existe um receipt formal válido que vincula este resultado à execução canônica específica esperada?

Isso não equivale a bloquear a apresentação de resultado sem receipt. O bloqueio de conclusão/homologação continua reservado à SE05.

## Precedência e reconciliação

O Plano Mestre original descreve SE04 como produção de evidência estruturada e coloca a validação final de contrato no postflight da SE05. A revisão pós-SE03 transfere à SE04 a responsabilidade de formalizar o receipt e tornar distinguível a rota canônica da rota manual.

Nesta sprint, portanto:

- SE04 implementa **verificação do receipt como objeto/evidência**;
- SE04 não conecta essa verificação a um gate obrigatório de conclusão;
- SE05 continuará responsável pelo **postflight fail-closed de produção**.

Essa separação preserva a fronteira canônica sem deixar o receipt impossível de testar deterministicamente.

## Invariantes herdados

- `scripts/run.py::run` continua sendo o único entrypoint canônico do core protegido;
- primitive protegida permanece somente `hub_scripts.quick_profile.quick_profile`;
- `ExecutionTraceV0` continua precursor técnico e não é substituído pelo receipt;
- `numeric_columns` permanece `runtime_derived` e conflito declarado continua `BLOCKED`;
- `fallback_used=false` permanece requisito;
- `mode="audit"` não muda nesta sprint;
- E02 histórico permanece `FAIL_OBSERVED` e `GENIE_BEHAVIORAL_SCREENING=MIXED`;
- nenhum dado corporativo é usado;
- fonte editável é `ambiente_fonte/`; `Novo_Ambiente_Simulado/` continua derivado do renderer canônico.

## Resultado funcional esperado

Uma execução bem-sucedida deve produzir:

```text
runner canônico
+ release íntegra
+ contexto/provenance válido
+ preflight PASS
+ quick_profile chamada
+ trace PASS
+ output correspondente
→ ExecutionReceiptV1
```

Rotas manuais, chamadas diretas, output adulterado, receipt adulterado, receipt stale/reutilizado, skill/release divergentes, conflito de provenance e falha/fallback não devem verificar como receipt canônico válido.

## O que fica fora

- postflight obrigatório;
- bloqueio da resposta final por ausência de receipt;
- generalização para todas as skills;
- mudança para `mode="enforce"`;
- assinatura com segredo/HMAC/PKI;
- defesa contra atacante com capacidade de alterar arbitrariamente código e recalcular todas as evidências;
- promoção corporativa;
- merge sem aceite humano explícito.

## Documentos desta sprint

- `DESENHO_TECNICO.md` — contrato técnico e decisões de serialização/binding;
- `THREAT_MODEL.md` — cenários R01+ e limites de segurança;
- `TESTES.md` — matriz local/Free e classificação de resultados;
- `RUNBOOK_FREE.md` — será congelado antes da homologação Free;
- `CHECKPOINT.md` — será atualizado a cada gate relevante.
