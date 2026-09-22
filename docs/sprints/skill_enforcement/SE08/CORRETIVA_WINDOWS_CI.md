# SE08 — corretiva Windows/CI após candidata local e3e67bce

**Estado:** implementação repo-side corretiva; exige aplicação/reconciliação sobre
a candidata local e execução Windows antes de qualquer conclusão.

## Evidência de origem

A campanha local da candidata `e3e67bced219bfb1d78ac80b0c5a8d29f86678fc`
reportou:

- materialização concluída e snapshot correto;
- testes específicos SE08 em PASS;
- storage cleanup 8/9, preservando o residual histórico;
- FULL SE08 FAIL, 17/18 gates, com WinError32 nativo em
  `test_never_ready_has_finite_diagnostic_and_cleanup`;
- CI geral 7/10, com Temas, Transição e READMEs vermelhos;
- WinError1314 em testes que tentavam criar symlinks no Windows sem privilégio;
- cinco mocks de layout que não dispararam o ValueError esperado;
- probe de dependência ausente contaminado pelo ambiente Python;
- writer 32/35 via venv e 35/35 via Python base.

Nenhum vermelho é reclassificado por este documento.

## Frente A — WinError32

Não há correção causal do cleanup nesta branch.

O certifier ganhou somente telemetria observacional imediatamente antes de
`TemporaryDirectory.__exit__`. O snapshot registra:

- existência e entradas do diretório;
- result/process_cleanup;
- pid e launcher_pid;
- observed_exit_code e exit_after_cleanup;
- command_started;
- metadata_error/start_error;
- utf8_valid.

A função não dorme, não mata processo, não fecha handle, não remove arquivo e
não repete cleanup. O veredito continua fail-closed.

Objetivo da próxima reprodução Windows: correlacionar esse snapshot com o
WinError32 e, se possível, observar externamente quem mantém o handle do
`stderr` no instante da falha. Sem essa observação não introduzir sleep,
retry, ignore_errors ou aumento arbitrário de timeout.

## Frente B — CI Windows

### Layout

Mocks de `test_temas_v02.py` usavam
`str(path).endswith("diretorio/arquivo")`. Em Windows a representação usa
separador diferente e o mutante podia não ser aplicado. A corretiva compara
`Path.parts` e inclui controle com `PureWindowsPath`.

### Dependência ausente

Os subprocessos `python -S` podiam continuar recebendo dependências por
`PYTHONPATH`. A corretiva remove essa variável do ambiente e usa `-E -S`,
mantendo o próprio produto inserido explicitamente em `sys.path`.

Isso testa o cenário declarado — ausência de dependências de terceiros — sem
trocar versões de pacotes.

### Symlinks

Testes de segurança que precisam de symlink agora capturam
`OSError/NotImplementedError` e registram `skipTest` quando o ambiente não
permite criar o link. Isso não é PASS da barreira: é evidência explícita de que
o ambiente não conseguiu montar a fixture.

Junction não foi usada como substituto geral porque os validadores envolvidos
checavam `Path.is_symlink()`; trocar a fixture por junction mudaria a
propriedade testada.

## Aplicação sobre a candidata local

Esta branch parte de `25013c53db37be0984604df3c463e98cb42949e2`, enquanto a
candidata Windows possui dois commits locais adicionais:

- `3118e9707fadd9bd37b3fea3d9504aba2be0a0b9`;
- `e3e67bced219bfb1d78ac80b0c5a8d29f86678fc`.

Não fazer reset/force. O operador local deve primeiro preservar/publicar ou
referenciar esses commits e então aplicar a corretiva por cherry-pick/rebase
controlado, auditando conflitos. A materialização já existente não deve ser
recriada manualmente.

## Gates da próxima rodada

No novo SHA, executar primeiro:

```powershell
python -B tools/tests/test_se08_windows_corrective.py -v
python -B tools/tests/test_temas_v02.py -v
python -B tools/tests/test_transicao_trabalho.py -v
python -B tools/tests/test_readme_objeto_contract.py -v
python -B tools/tests/test_certify_local.py -v
```

Depois, conforme resultado:

```powershell
python tools/ci_local.py --verbose
python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <NOVO_DIRETORIO>
```

A reprodução de `test_never_ready_has_finite_diagnostic_and_cleanup` deve
preservar `temporary_cleanup_pre_remove` e a evidência externa de handles.
Não fazer retry-until-green.

## Estados preservados

- SE06 = 24/25; A1-R4 NOT_RUN; DoD incompleto; FULLY_CERTIFIED=false;
- SE07_FULLY_CERTIFIED=false;
- storage cleanup histórico = FAIL 8/9;
- WinError32 antigo não reproduzido continua fato histórico daquela rodada;
- WinError32 nativo foi observado na campanha SE08 e não está declarado corrigido;
- hub-ml-criar-objeto continua L2 global;
- PROMOCAO_TRABALHO=BLOQUEADA;
- Free/Genie/PR permanecem posteriores à recertificação local.
