# Handoff — correções Codex prontas para baixar

Data: 09/09/2026 · De: Codex · Para: Rodrigo / sessão local.

## Estado atual

Implementação sobre a branch `claude/plano-consolidado-2026-09-08`, a partir de
`771dbf2`. A branch continua separada da `main`; não houve merge nem publicação
Databricks nesta sessão.

- R01/R06: seleção de métricas recusa valor inválido, detecta aliases conflitantes
  e aceita lista explícita de métricas obrigatórias; migração KS documentada sem
  alterar sua escala histórica 0–100.
- R02: nomes auxiliares temporais não sobrescrevem colunas do chamador.
- R03: caches/extras ignorados presentes no espelho impedem upload; o bundle usa
  a mesma guarda fonte–espelho. Links simbólicos no espelho são recusados.
- R04: teste PIT compara o multiconjunto completo de chave, data e feature;
  mutantes fora de C1 e alteração de data são detectados localmente.
- R05: limite CSI exige inteiro positivo antes de acesso ao DataFrame/Spark.
- T3: contagem do versionado usa Git; extras locais, inclusive ignorados no
  escopo ativo, têm higiene separada. A conferência local do README não chama
  Databricks; a remota tem flag própria.
- Publicador: origem Git é ancorada no repositório, erros não viram estado limpo,
  hashes completos e `--relatorio` permitem evidência JSON por arquivo.
- Exemplos atualizados; espelho regenerado exclusivamente pelo renderer.

Validação local: 40 testes de biblioteca e 32 de ferramentas aprovados, incluindo
parsing de exportação e relatório JSON remoto simulado. O teste CSI valida a
pré-condição em isolamento; não é execução Spark. Contagens estruturais ficam
no README, conferidas contra Git. Nenhuma dependência de dados corporativos.

## Atualizar a pasta do PC

No terminal dentro do clone existente:

```powershell
git status --short
git fetch origin
```

Se houver alterações locais, preserve-as e revise antes de trocar de branch ou
integrar o remoto; não use reset destrutivo. Com a árvore em condição de integrar:

```powershell
git switch claude/plano-consolidado-2026-09-08
git pull --ff-only origin claude/plano-consolidado-2026-09-08
python -m pip install -r tools/requirements-dev.txt
python tools/ci_local.py
```

Se a branch não existir localmente, use
`git switch --track origin/claude/plano-consolidado-2026-09-08` no lugar do switch
anterior. Verifique o commit recebido com `git log -1 --oneline`.

O gate de inventário agora requer um checkout Git. Download de ZIP sem `.git`
não equivale a um clone para essa certificação; Git ausente ou índice vazio
reprova explicitamente. Arquivos novos precisam ser adicionados ao índice para
participar da contagem versionada; antes disso continuam na higiene de extras.

## Em andamento / bloqueado

Não foi acessado o workspace Free nem o corporativo. Falta executar:

1. pacote limpo e publicação Free da versão final;
2. exportação real FILE/NOTEBOOK e comparação de conteúdo;
3. smoke no runtime Free, incluindo PIT e cenários CSI de cardinalidade;
4. 3 cenários da skill e 16 famílias de prompts em chats novos;
5. aceite de runtime, permissões e MLflow no trabalho.

`ci_local.py` automatiza execução local; não instala workflow no GitHub. A
configuração de CI hospedada continua uma entrega opcional posterior.

## Publicação e evidência no Free

Usar os valores locais do perfil e host; não persistir identificadores reais em
Git. Primeiro confira `git status` e os gates. Então:

```powershell
python tools/render_simulado.py --write
git status --short
python tools/bundle_implantacao.py
python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>
python tools/publicar_free.py --verify --conteudo --profile <free> --expected-host <url-free> --relatorio .artifacts/verify-conteudo.json
```

Se o renderer produzir alterações inesperadas, interrompa a publicação e revise.
O JSON contém hashes completos do conjunto local comparado e status da leitura
remota. Esses hashes agregados não são o hash do arquivo ZIP. Uma execução com
origem dirty fica explicitamente identificada, sem equivaler a release limpa.

A conferência remota do bloco histórico do README é separada:
`python tools/validate_assistant.py --conferir-readme-remoto` (use as variáveis
DATABRICKS_FREE_PROFILE e DATABRICKS_FREE_HOST configuradas localmente).
Esse comando não substitui `--verify --conteudo`.

## Armadilhas conhecidas

- Uma política genérica tem métricas de várias tarefas: declare as obrigatórias
  da sua tarefa; não exija todas indiscriminadamente.
- Métrica inválida selecionada deve ser corrigida na origem ou excluída por
  política deliberada, nunca desaparecer sem decisão.
- O índice Git define os nomes versionados; as verificações leem seu conteúdo
  atual na worktree, incluindo alterações ainda não commitadas. Isso é validação
  de desenvolvimento, não atestado de correspondência com HEAD limpo.
- Higiene não autoriza publicar extras. Re-renderize se o espelho tiver caches.
- Testes com CLI simulada não provam o protocolo real da versão instalada.
- Abrir sessão adequada após publicação evita usar módulos antigos em memória.

## Fechamento posterior — Codex, 09/09/2026

O estado pendente acima foi superado no Free. O produto do commit `8187fac` foi
publicado e conferido em conteúdo (316/316); o smoke final no Spark 4.2.0 fechou
com 137 PASS e 0 FAIL; e os três casos da skill 13 fecharam o roteamento em
39/39. A evidência canônica é
[`docs/testes/2026-09-09_fechamento-codex.md`](../testes/2026-09-09_fechamento-codex.md).
Continuam fora do aceite: as respostas conversacionais das 16 famílias de
prompts e a replicação no workspace de trabalho.
