# Retificação aditiva E-01 e esclarecimento E-02 — 2026-09-21

O usuário concedeu aceite humano focalizado à F-03
`1ce5806cc04654eda88966676fe90459488553d4`, parent
`b6fb595225e139329df450edfc33158ceb1e1253`. O aceite não certifica o lote novo,
não encerra a SE07 e não aprova D2/D9, writer L3 ou SE08.

## E-01 — tentativas recuperadas

O relatório original descreveu as três primeiras campanhas Linux como
incompletas após os onze primeiros gates. Os bytes recuperados corrigem essa
narrativa: duas campanhas chegaram ao summary final e foram FAIL; a terceira
registrou falha de gate e interrupção. Nada é apagado ou reclassificado em PASS.

| Tentativa histórica | Estado observado |
|---|---|
| `linux_full` | FULL FAIL; readme_snapshot exit 1; 423 falhas; 383 linhas de status sujo |
| `linux_full_second` | FULL FAIL; readme_snapshot exit 1; 424 falhas; 383 linhas de status sujo; certifier exit 1 |
| `linux_full_third` | Sem summary final; assistant_structure registrou 240 falhas; execução interrompida |

Os registros suplementares estavam fora do manifesto original do executor.
Foram recuperados e selados na auditoria F-03; não se confundem com o bundle
original nem com reprodução própria desta continuidade. Os FULLs posteriores
Windows/Linux do executor, o FULL Windows do auditor e os testes Linux da
supervisão são campanhas distintas e não apagam esses FAILs.

Interferência de processos e reuso do mesmo clone são hipóteses compatíveis com
a evidência, não causa raiz demonstrada. F-04 trata falhas concretas do certifier;
não promete impedir todo escritor externo, suspensão ou alteração transitória
revertida entre as observações.

Referência imutável: `SEF_F03_AUDITORIA_1ce5806c.zip`, SHA256
`0c9afc3d2b38024d531697299ee8e5cdb00dc2d4b7b106faa288e8326ed7d5ad`.
Manifesto da auditoria: SHA256
`e7c0dbbb8e97fcd9e0ab5593c05244fcf271038ad33c2ec0b9bd88133508b2b5`.
No ZIP anterior, os paths abaixo têm prefixo `original_supplement/`; no novo
handoff, `e01_recovered/`. Os logs completos correspondentes são preservados.

| Path relativo | SHA256 |
|---|---|
| `linux_full/summary.json` | `aee9885d997d58d4941395c9dfc36b4f243bfa30dd7c7adb4ba7cffd47153e57` |
| `linux_full/logs/15_readme_snapshot.log` | `a0831364df0868186f5c316ae452ebda99bd06573ab79230b1e5553d766e0f86` |
| `linux_full_second/summary.json` | `126305c2be285f59bda16c0f45540c6caa28074ee47cbbab1bf22f3c4e2c772b` |
| `linux_full_second/logs/15_readme_snapshot.log` | `971deaecbb4ba1d0ab67ef95c59cdf5ce6d31cd9404c5661016dbf11f3f1fcf9` |
| `linux_full_third/logs/12_assistant_structure.log` | `3c3ff91a394c7d56c82c2d884684953a2aa34df4cc8fca2ad2e54c5b019c680e` |

## E-02 — esclarecimento textual

O campo descritivo `canonical_verifier_return.issues` passa a dizer
“lista ou tupla de strings; PASS_REVERIFIED exige coleção vazia (lista ou tupla),
normalizada para lista na saída”. Não se altera required_fields, enums, sucesso,
runner ou semântica de issues. Atualiza-se somente o fingerprint do contrato no
manifest do auditor, preservando conjunto, roles, ordem, algoritmo e versões.
O espelho é regenerado pelo renderer canônico.

Receipts históricos continuam vinculados à release de emissão; não se fabrica
compatibilidade com os novos bytes. A integração exige certificação própria no
SHA final. O handoff externo registra esse SHA e seus resultados após o freeze.

## Limites preservados

A referência R1 auditada continua NAO_APTA. SE06 permanece 24/25, A1-R4 NOT_RUN,
DoD INCOMPLETE e FULLY_CERTIFIED=false. D4/D5 permanecem limites de evidência.
Não há nova política D2, writer, R2, SE08, PR, Actions ou Free/Genie nesta rodada.
