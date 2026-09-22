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

## 2026-09-22 — SE08: observabilidade opt-in do cleanup

### Adicionado

- (ChatGPT) cleanup_diagnostics.py: um caso por invocação, journal externo,
  eventos de cleanup explícito/finalizer, estado dos streams e consultas do Job
  Object próprio; Restart Manager opcional após WinError32, sem fechar aplicações.
- (ChatGPT) 25 regressões do observador; carga das 29 regressões corretivas pelo
  step SE08 existente. Oito métodos anteriores preservados; montagem da fixture
  em runtime portada da correção Codex em 3118e970, sem reatribuir sua autoria.
- (ChatGPT) Documento CORRETIVA_20260922 com reconciliação, resultados, limites e
  procedimento de integração à candidata local e3e67bce sem substituir sua história.

### Evidência e pendências

- (ChatGPT) Linux/Python 3.13.5: regressões corretivas 4/4 e 25/25; suíte storage
  original 9/9, que não apaga o FAIL nativo. Fixture original instrumentada mantém
  exit 130 e resíduo no oráculo; finalizer posterior não prova a causa Windows.
- (ChatGPT) Duas tentativas F-04 ficaram incompletas por interrupção externa da
  ferramenta, sem exit final observado. Logs preservados; nenhum PASS atribuído.
- (ChatGPT) Certifier, algoritmos de cleanup, writer e testes históricos de
  storage/F-04 permanecem byte-idênticos. WinError32 nativo, privilégios para
  symlink e recertificação Windows/FULL/CI continuam pendentes.
