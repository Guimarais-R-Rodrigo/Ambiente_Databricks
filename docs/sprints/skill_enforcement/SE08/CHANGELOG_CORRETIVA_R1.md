## 2026-09-22 — SE08: portabilidade e diagnóstico opt-in R1

### Corrigido

- (ChatGPT) Cinco mocks V02 passaram a normalizar separadores com `as_posix()`;
  dois subprocessos sem dependências usam `-I -S`. As 78 asserções/skips
  identificadas por AST foram preservadas; nenhum novo skip contorna permissões.

### Adicionado

- (ChatGPT) Oito testes dos seletores reais e do isolamento contra PYTHONPATH/cwd.
- (ChatGPT) Observador opt-in de cleanup/finalização automática, consulta opcional
  de usuários do arquivo pelo Restart Manager e diagnóstico de capacidade de
  symlinks. Sem shutdown/restart, alteração de nível ou correção especulativa do cleanup.
- (ChatGPT) Dezessete testes do observador, com proteção da exceção original,
  identidade Git e evidência externa. Conferência final: 8/8 e 17/17 em
  Linux/Python 3.13.5; componentes, NÃO FULL ou Windows. Vermelhos preservados.

### Estado

- (ChatGPT) Revisão isolada sobre c99174cf, preservando telemetria encontrada.
  Integração com os dois commits locais e3e67bce/3118e970, incorporação deste
  fragmento ao changelog raiz, snapshot e certificação Windows continuam pendentes.
- (ChatGPT) Sem PR, Actions, merge em main, Free/Genie ou promoção. SE06 24/25,
  A1-R4 NOT_RUN, SE07_FULLY_CERTIFIED=false, storage histórico FAIL 8/9 e
  criar-objeto L2 global preservados. WinError32 nativo não declarado corrigido.
