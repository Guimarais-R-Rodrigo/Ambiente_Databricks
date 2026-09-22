## 2026-09-21 — SE08: complemento de I/O reconciliado

### Adicionado

- (ChatGPT) `tools/tests/test_skill_enforcement_policy_io.py`: 15 testes de I/O,
  leitura única, consistência do resumo e CLI com raiz explícita; fixtures sintéticas.

### Corrigido

- (ChatGPT) `tools/skill_enforcement/se07_policy.py`: resumo e validação reutilizam
  o mesmo parse; preservados assistant_root, API e regras da implementação concorrente.

### Notas

- (ChatGPT) Review isolada a partir de aa83e5cc, sem sobrescrever a SE08 canônica.
  Baseline ampliada: três falhas em 15 testes; correção: 15/15, zero skips, Linux/Python 3.13.5.
- (ChatGPT) Certificação integral, Windows/NTFS, integração à canônica e incorporação
  desta entrada ao changelog raiz pendentes. Não há aceite, PR, merge ou promoção.
- (ChatGPT) SE06 24/25 e A1-R4 NOT_RUN, SE07_FULLY_CERTIFIED=false, residual storage
  cleanup e criar-objeto L2 global preservados; WinError32 nativo não declarado corrigido.
