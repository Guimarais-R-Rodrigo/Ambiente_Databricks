# SE08 — matriz de testes e gates

Este documento define o que deve ser executado; `RESULTADOS.md` registra apenas
o que foi realmente observado. Comando listado aqui não é evidência de PASS.

## Camada A — regressões específicas

Executar serialmente no mesmo SHA, preservando toda tentativa:

```powershell
python -B tools/tests/test_skill_enforcement_policy_io.py -v
python -B tools/tests/test_skill_enforcement_se08.py -v
```

Critérios: exit 0, zero failures/errors/skips inesperados e nenhuma alteração de
policy/níveis como efeito colateral.

## Camada B — dívidas e regressões SE07 relacionadas

```powershell
python -B tools/tests/test_certify_storage_cleanup.py -v
python -B tools/tests/test_certify_local.py -v
python -B tools/tests/test_validate_create_readme.py -v
python -B tools/tests/test_skill_enforcement_se07_create_l3.py -v
python -B tools/tests/test_skill_enforcement_se07.py -v
```

O storage cleanup é gate separado. Um FULL verde não converte eventual FAIL
dessa suíte em PASS.

## Camada C — estrutura, renderer e snapshot

```powershell
python tools/validate_assistant.py
python tools/render_simulado.py --write
git status --short
python tools/validate_assistant.py --conferir-readme
```

Depois do renderer, revisar somente mudanças derivadas esperadas. Não editar o
simulado à mão. Se o snapshot do README raiz divergir, atualizá-lo a partir da
saída real do validador e repetir o gate no novo SHA.

## Camada D — certificação FULL SE08

Em worktree limpa e diretório externo novo:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <DIRETORIO_EXTERNO_NOVO>
```

Não usar `--allow-dirty`, `--skip-render` ou `--no-evidence` no FULL.

Registrar SHA, tree, branch, merge-base, plataforma, Python, filesystem,
comandos, exits, duração, testes/falhas/skips, logs, `summary.json`,
`commands.json`, `processes.json` e limitações.

## Camada E — gate geral do repositório

Preparar as dependências declaradas pelo projeto e executar:

```powershell
python tools/ci_local.py --verbose
```

O subgate SEF interno é parcial/read-only e não substitui o FULL da camada D.

## Windows/NTFS

Quando a campanha final for executada no Windows nativo/NTFS, registrar a versão
do Python e executar as suítes sensíveis a processos/cleanup no mesmo SHA. Não
inferir evidência Windows a partir de Linux/WSL.

O residual histórico storage cleanup 8/9 e o WinError32 histórico permanecem
como fatos anteriores. Nova rodada só altera a classificação se produzir nova
evidência no escopo explicitamente testado.

## Free e Genie

Não executar automaticamente nesta fase local. Primeiro concluir a certificação
repo-side e decidir, com base no Plano Mestre, quais probes/homologações da SE08
são obrigatórios para a candidata.

Publicação Free exige `publicar_free.py --verify --conteudo` e evidência do SHA
publicado. Genie exige chat novo e registro separado de roteamento, execução e
aderência. Mock não substitui workspace.

## Actions e PR

GitHub Actions só entram depois de release candidate/Ready-for-review. Não usar
rerun-until-green. Falha gera investigação causal e, se houver novo SHA, nova
rodada aplicável.

## Gate de promoção ao trabalho

Mesmo após todos os testes acima, promoção continua bloqueada enquanto os oito
requisitos do gate SE08 não estiverem satisfeitos. Em particular, G2 não
transformou SE06 24/25 em certificação suficiente para promoção corporativa.


## Estado observado da candidata técnica R5

No SHA `ee1cf04b031497bb5b7ddfa47ce28b8015d15668`, Windows 11/NTFS/Python 3.12.14:

- Windows corrective: 10/10 PASS;
- storage cleanup: 9/9 PASS;
- certifier regression: 51 métodos, 0 failures/errors, 1 skip de escopo, exit 0;
- CI local: 10/10 etapas PASS;
- FULL SE08 local: 21/21 gates PASS;
- `release_clean_certification=true`;
- nenhuma ocorrência nativa WinError32 observada nessa campanha.

Esses resultados não apagam as tentativas vermelhas anteriores e não demonstram root cause do WinError32 intermitente.

## Recertificação do delta documental final

Depois de atualizar CHECKPOINT/RESULTADOS/README/TESTES/RUNBOOK/CHANGELOG sem alterar código, o novo SHA deve executar somente:

1. precheck de identidade/worktree;
2. `python -B tools/ci_local.py`;
3. FULL `python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <NOVO_DIRETORIO>`;
4. identidade final.

O FULL contém storage, corretivas Windows, cleanup diagnostics e certifier regression. Não há necessidade de repetir separadamente os mesmos gates apenas por causa de alterações documentais, salvo finding novo.
