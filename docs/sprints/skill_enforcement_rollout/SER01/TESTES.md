# SER01 — testes A1 e execução delegada

## Desenvolvimento já realizado

A suíte `tools/tests/test_ser01_object_validation.py` contém 24 métodos de envelope/integridade e sete métodos de integração opt-in. Os primeiros não carregam nem simulam aprovação do catálogo completo. Os sete últimos precisam do checkout real e da autorização de evidência externa.

No Linux/Python 3.13.5 desta autoria: 24 PASS, sete SKIP explícitos por indisponibilidade do clone integral. O ensaio externo de orquestração exercitou três cenários com Git/processos reais e validators/supervisor sintéticos; confirmou fluxo positivo, reprovação da candidata inválida e reprovação de preflight malformado. Isso não é validação canônica.

Uma primeira execução de desenvolvimento encontrou duas falhas de expectativa no teste da allowlist: inserir um quinto arquivo acionava antes o limite de quatro. O teste foi corrigido para substituir um dos quatro arquivos e isolar a allowlist. O FAIL original e os logs posteriores permanecem no bundle externo. Não houve campanha certificadora congelada nem retry-until-green.

## Integrações discriminantes planejadas

1. Pacote snippet a partir de réplica sintética isolada do objeto `format_br`.
2. Pacote script a partir de réplica sintética isolada de `data_quality_check`.
3. Pacote prompt a partir de réplica sintética isolada de `eda_rapida`.
4. Notebook adicional de fixture na pasta do prompt existente.
5. README agregador de fixture na pasta scripts do piloto.
6. Notebook com sintaxe inválida: a base deve passar e a candidata deve reprovar.
7. Fachada pública incorreta: recusar, sem regenerar bytes para fazer o teste passar.

As cópias existem apenas no overlay externo. Não entram em `ambiente_fonte/` do checkout original, não são publicação, não executam os exemplos e não fabricam novas saídas analíticas.

## Preparação anterior ao freeze

O conector permitiu publicação dos novos arquivos, mas este ambiente não conseguiu clonar o Git por DNS. A aplicação preservadora da entrada em `CHANGELOG.md` e a atualização **medida** do snapshot raiz serão operações mecânicas delegadas, antes da campanha formal. Não se considera a candidata pronta enquanto isso faltar.

O executor deve usar uma worktree dedicada, preservar as worktrees A07 antigas, ler `CLAUDE.md` e regras aplicáveis, confirmar a base e preparar dependências pelos arquivos existentes. Não escolher outra arquitetura, não editar a primitive/testes, não mudar policy ou ampliar escopo.

Aplicar `ENTRADA_CHANGELOG.md` integralmente como nova seção após `# Changelog`, apenas se o título ainda não existir. Estagiar os arquivos documentais antes de medir o censo: o validator usa inventário Git. Executar o validator normal; só com aprovação estrutural medir as duas linhas `repo (identidade)`/`repo (links)` e atualizá-las no bloco do README. Não alterar outras expectativas para obter verde. Um único commit de preparação pode modificar **somente** `CHANGELOG.md` e `README.md`.

Confirmar HEAD, tree, base, merge-base, behind=0, diff permitido e worktree limpa. Esse SHA posterior à preparação é o freeze real; o SHA de autoria recebido não herda sua certificação.

## Campanha A1-LAB

Diretório externo novo, sem logs/ZIPs dentro do repo. UTF-8 explícito para o Python pai e subprocessos. Detectar host; não pressupor Linux nem Windows. Instalações e probes ambientais acontecem antes do freeze, sem alteração dos manifests/lockfiles.

Executar uma vez os testes novos, com `SER01_RUN_REPO_INTEGRATION=1` e `SER01_EVIDENCE_ROOT` externo. Comandos de referência, a resolver no host:

```text
python -B -m unittest tools.tests.test_ser01_object_validation -v -f
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/se07_policy.py
python -B tools/validate_assistant.py
python -B tools/render_simulado.py --write
python -B tools/validate_assistant.py --conferir-readme
python -B tools/ci_local.py --verbose
python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <novo-diretorio-externo>
```

Remover a flag de integração do ambiente após a execução explícita da suíte SER01, para não dispará-la implicitamente em outras campanhas. Não omitir os testes SER01 por não constarem do perfil histórico SE08.

Após renderer, exigir zero drift rastreado/não rastreado. FULL só após todos os gates prévios passarem. O stderr de um teste negativo esperado pode conter FAIL da candidata sintética; quem define sucesso desse caso é seu oráculo unittest, nunca uma busca cega pela palavra FAIL. Falha do teste ou comando obrigatório encerra a campanha, preservando o restante como NOT_RUN.

## Entrega do laboratório

Identidade antes/depois; hashes dos arquivos declarativos; versões; comandos, exit codes e logs completos; registros `validation.json`; candidatos sintéticos; checksums; diff de preparação; log de commits; resultado de testes unitários versus integração; CI/FULL por canal e hash do ZIP.

Preservar bruto local. Para transporte, pode-se excluir o conteúdo volumoso `.git` dos overlays somente com inventário explícito: conservar os candidatos, base/tree, registros e logs necessários à reprodução. Não apagar ou reescrever o bruto para sanitizar.

O agente externo pode devolver `A1_LAB_PASS` ou um bloqueio/falha observado. Não pode declarar SER01 encerrada, promover L3, publicar no Free, fazer merge ou iniciar SER02.

## Corretiva pós-R1 (2026-09-23)

A R1 reprovou em `test_real_script_validation`: a réplica do script herdou o README legado sem LF terminal e a primitive recusou corretamente com `CONTENT_REQUIRES_UTF8_LF`. A corretiva altera só `replica()`, que acrescenta o LF terminal ausente à fixture positiva. Não há método novo: a suíte continua com 31 métodos (24 unitários, sete integrações). O caso negativo `"sem newline"` de `test_encoding_and_size_restrictions` permanece e deve continuar bloqueando. A R2 repete a campanha inteira, uma vez, sobre o novo SHA congelado; push só depois de todos os gates verdes.
