# Saída gerada e CI da release atual

`ambiente_fonte/` continua fonte canônica. O output-root compartilhado de renderer,
publicador e pacote é `.artifacts/simulado/`, definido em `tools/project_policy.py`.
O nome `Novo_Ambiente_Simulado/` permanece apenas em evidências, snapshots e aliases
históricos de proteção. Esses registros não instruem uma release atual a ler a
árvore antiga.

## Preparar e conferir

Após validar a fonte e autorizar a substituição da árvore gerida, em checkout
isolado sem extras alheios:

```sh
python tools/validate_assistant.py --conferir-readme
python tools/render_simulado.py --write
python tools/render_simulado.py --check
python tools/ci_local.py --verbose
```

`--write` continua destrutivo no destino escolhido. Inventarie toda a árvore,
inclusive arquivos ocultos e diretórios vazios, e preserve conteúdo desconhecido
antes. `--check` é read-only: exige fonte não vazia, paths exatos, bytes brutos,
SHA-256 e tipos FILE/NOTEBOOK/diretório; recusa extras e symlinks. Não depende de
`git diff`, de symlinks para o path antigo nem de saída rastreada. Caches de fonte
são ignorados; caches ou extras no destino reprovam.

Renderer, `publicar_free.py` e `bundle_implantacao.py` aceitam `--output-root` para
um subdiretório próprio de `.artifacts/`. O mesmo valor deve acompanhar todas as
etapas. A raiz `.artifacts/` em si, traversal, origem do produto, escape e symlinks
são recusados. O nome do usuário continua placeholder neutro, por padrão
`usuario-free`.

O ZIP segue com os mesmos paths de produto, bytes e classificação FILE/NOTEBOOK;
a localização do diretório de build não viaja no payload. Empacotar não publica.
Publicação e verificação remota continuam exigindo escopo próprio.

## CI por ambiente

[ci.yml](../../.github/workflows/ci.yml) é o DAG automático comum para todo PR,
`main` e branches de campanha `codex/temas-v*`. Os checks antigos V00/V04–V14
mantêm exatamente seus nomes, receitas específicas e uma dependência que exige
sucesso da suíte cumulativa correspondente. Falha, cancelamento, skip ou resultado
ausente do upstream reprovam o check, em vez de deixá-lo passar por skip.

- `validar`: agregado Python 3.12, Spark ausente, widgets opcionais.
- `temas-widgets`: descoberta completa Python 3.12 com ipywidgets obrigatório, sem seed de ambiente (V05).
- `temas-widgets-seeded`: mesmo perfil com `SOURCE_DATE_EPOCH=1700000000` (V06–V09).
- `temas-widgets-app`: widgets + App, seed fixo e `ubuntu-latest` (V10–V12).
- `temas-widgets-app-24`: mesmo conjunto de dependências/seed, `ubuntu-24.04` (V13–V14).
- `preparar`, no workflow de kit: agregado separado Python 3.11 + Spark 4.0.1/Java 17.

V00 preserva suas três suítes fora do prefixo `test_temas`; V05 preserva
`--require-ipywidgets`; V09/V10 mantêm build/verificação de artefatos; V08/V12
mantêm escopo e higiene; V13/V14 mantêm controles e limites da campanha. A
certificação FULL SEF permanece separada do subgate parcial de `ci_local.py`.

Os YAMLs antigos V00/V04–V14 são receitas manuais completas de compatibilidade.
O sufixo do DAG comum é compilado dessas receitas por `tools/ci_workflows.py`:

```sh
python tools/ci_workflows.py --write
python tools/ci_workflows.py --check
```

A checagem detecta drift do conteúdo gerado, dependências e triggers duplicados.
Os testes `test_ai_ci_workflows.py` preservam a matriz de nomes/comandos/artifacts
observada e os negativos de propagação. Cache pip inclui o requirements externo
e o arquivo de Temas incluído por ele; o perfil App inclui seu requirements.
Nenhum cache de resultado de teste concede aprovação.

A escolha conservadora deixa todos os checks comuns sem filtros. Num push amplo
em main, as rotas configuradas de suíte completa caem de 13 para 6, incluindo o
kit Python 3.11/Spark quando seu filtro se aplica. Num PR estreito de documentação,
as rotas podem aumentar de 1 para 5. Isso preserva reporte e dependências dos
checks enquanto required checks não podem ser auditados; não é uma promessa de
redução universal nem de duração. Tempo remoto ainda não foi medido. Runners
`ubuntu-latest` e `ubuntu-24.04`, seed presente/ausente e dependências diferentes
continuam separados; não se presume equivalência entre labels de imagem.

## Limites e retenção

Os check names atuais foram observados no GitHub como nomes simples de jobs do
app GitHub Actions. Rulesets visíveis retornaram lista vazia; a consulta de branch
protection retornou 403. Configuração de required checks segue **BLOCKED por
acesso**, e check-runs do SHA candidato são **NOT_RUN até publicação autorizada**.
Prova estática e testes locais não afirmam equivalência remota já homologada.

As matrizes vivas V08/V13 migram somente o path do derivado. Checkpoints, provas
brutas, snapshots, baseline B0 e baseline da campanha IA continuam históricos.
`ai_controls --check` confere o payload corrente; `--migration-freeze` continua
ligado à baseline imutável anterior e deve reprovar uma mudança autorizada que
não pertença àquela campanha. Não recalcule a baseline para esconder esse delta.
