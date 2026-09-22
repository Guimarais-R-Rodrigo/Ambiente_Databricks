# Fragmento de changelog — corretiva SE08 de 22/09/2026

**PENDENTE de incorporação ao CHANGELOG.md raiz na integração local.**
Este fragmento não dispensa o changelog canônico nem torna a review uma RC.
Preservar integralmente as entradas anteriores, inclusive as do Codex em
3118e970/e3e67bce, que ainda não pertencem à história remota desta review.

## 2026-09-22 — SE08: portabilidade dos instrumentos de CI

### Corrigido

- (ChatGPT) Cinco mocks de caminhos em test_temas_v02 usam Path.as_posix para
  reconhecer o mesmo alvo em Windows e POSIX. Duas sondas de ausência de
  dependências passam a usar -I junto de -S para não herdar PYTHONPATH.
- (ChatGPT) Nenhuma regra visual, asserção final, teste de symlink, dependência,
  privilégio, threshold ou timeout de produto foi relaxado.

### Adicionado

- (ChatGPT) Quatro regressões focais exercitam callbacks reais extraídos por AST
  e subprocessos reais com PYTHONPATH sintético. Baseline: sete falhas de
  subcasos; candidata: 4/4 PASS, zero skips, Linux/Python 3.13.5.

### Limites

- (ChatGPT) Evidência de instrumentos, não CI de temas completo nem Windows
  nativo. Storage cleanup, WinError32 e certificação SE08 continuam pendentes;
  SE06 24/25, A1-R4 NOT_RUN, SE07_FULLY_CERTIFIED=false e criar-objeto L2 global
  permanecem preservados. Nenhum push da canônica, PR, Actions ou workspace.
