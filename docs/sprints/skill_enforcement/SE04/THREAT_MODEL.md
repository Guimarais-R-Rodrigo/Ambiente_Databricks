# SE04 — modelo de ameaça do Execution Receipt

## Objetivo

O Receipt V1 fornece tamper evidence, binding determinístico e rastreabilidade da execução canônica. Ele não é uma assinatura criptográfica nem uma prova contra atacante administrativo/root.

## Cenários mínimos

| ID | Cenário | Resultado esperado |
|---|---|---|
| R01 | runner canônico + receipt correspondente | `VALID` |
| R02 | output manual correto sem runner | `ABSENT`; canonical compliance FAIL |
| R03 | chamada direta ao helper | `ABSENT`; canonical compliance FAIL |
| R04 | output/trace existe, receipt ausente | `ABSENT` |
| R05 | campo protegido do receipt alterado | `INVALID` |
| R06 | output alterado depois da emissão | `INCOMPATIBLE` |
| R07 | receipt de run anterior contra run atual esperado | `STALE_REPLAYED` |
| R08 | receipt de outra skill | `INCOMPATIBLE` |
| R09 | contract/runner/manifest divergente | `INCOMPATIBLE` |
| R10 | provenance contraditória | emissão recusada ou verificação inválida |
| R11 | primitive protegida ausente/adulterada | nenhum receipt válido emitido |
| R12 | primitive falha + fallback manual | nenhum receipt válido emitido |
| R13 | receipt copiado + output recriado incompatível | `INCOMPATIBLE` |
| R14 | receipt parcial/schema incompleto | `MALFORMED` |
| R15 | versão desconhecida | `UNSUPPORTED_VERSION` |

## Vetores adicionais

### R16 — trace adulterado depois da emissão

`trace_sha256` deve divergir e a verificação falha.

### R17 — receipt íntegro de release anterior

Mesmo que o `receipt_id` seja internamente consistente, a comparação com expectativas da release atual deve resultar `INCOMPATIBLE`.

### R18 — ordenação JSON diferente

Dicionários semanticamente iguais, com outra ordem de inserção, devem gerar os mesmos digests canônicos.

### R19 — tentativa de legitimar conflito por agent-declared

Alterar apenas metadados declarados não pode substituir provenance runtime. O verifier exige o estado runtime-derived refletido no trace vinculado.

## Limite criptográfico explícito

SHA-256 puro detecta alteração quando existe uma referência/expectativa independente, mas não autentica a origem contra um atacante que consiga:

1. executar código arbitrário;
2. fabricar trace e receipt completos;
3. recalcular todos os hashes;
4. substituir os artefatos verificadores/runner ou controlar a release.

Resolver esse vetor exigiria uma âncora de confiança externa (por exemplo assinatura/HMAC com segredo protegido, serviço de attestation ou armazenamento imutável). Isso não é introduzido na SE04 porque excede o objetivo atual e criaria infraestrutura criptográfica prematura.

## Propriedade garantida no alcance SE04

Rotas paralelas testadas não conseguem **reutilizar** receipt canônico válido para outro run/output/release sem gerar incompatibilidade detectável, e uma rota manual comum não recebe receipt pela API canônica do runner.
