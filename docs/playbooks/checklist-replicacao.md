# Checklist de replicação no trabalho

> **Os números deste documento saem de comando, não de memória.** Onde antes
> havia uma contagem fixa, hoje há a linha que a produz — porque toda contagem
> escrita à mão neste projeto envelheceu, sem exceção. Rode antes de replicar:
>
> ```powershell
> python tools/validate_assistant.py     # skills, objetos, contratos
> python tools/publicar_free.py --verify # arquivos, skills, extensões, obsoletos
> ```

Documento de acompanhamento, para marcar enquanto executa. O procedimento
completo, com o porquê de cada passo, está em
[replicacao-trabalho.md](replicacao-trabalho.md).

**Versão a replicar:** o commit que passou nos dois comandos do aviso acima.
Anote aqui o hash e a saída de `--verify`, para que quem conferir depois saiba
exatamente o que foi copiado:

```text
commit    : ________________
arquivos  : ________ (linha `remotos` do --verify)
skills    : ________ (linha `skills`)
extensões : ________ (linha `extensões`)
```

Preencha ao final: data \_\_\_\_\_\_\_\_ · executado por \_\_\_\_\_\_\_\_

---

## Fase 0 — antes de sair desta máquina

- [ ] `git status` limpo e sincronizado com o remoto
- [ ] `python tools/validate_assistant.py` aprovado
- [ ] `python tools/publicar_free.py --verify` aprovado
- [ ] Anotar o commit que está sendo replicado: `________`
- [ ] `python tools/render_simulado.py --write`
- [ ] `python tools/bundle_implantacao.py`
- [ ] Guardar o ZIP mínimo e anotar o commit do `MANIFEST.json`

## Fase 1 — backup, antes de tocar em qualquer coisa

Sem CLI no trabalho, este é o único caminho de volta.

- [ ] Abrir `/Users/<username-trabalho>/` no workspace
- [ ] Exportar a pasta `.assistant` inteira (menu de contexto → Export)
- [ ] Exportar o arquivo de instruções existente — no ambiente anterior ele
      costuma estar como `assistant_instructions.md`, **sem o ponto inicial**
- [ ] Guardar os dois fora do Databricks, em local que sobreviva à sessão
- [ ] Anotar data e conteúdo do backup: `________`

> Se o menu não oferecer exportação de pasta, exporte subpasta por subpasta.
> Não avance sem backup completo.

## Fase 2 — levar os arquivos

Escolha a rota que a política permitir. Descubra isso **antes** da fase 3.

### Rota A — ZIP mínimo (preferível)

- [ ] Levar somente `.artifacts/ambiente-databricks-<commit>.zip`
- [ ] Conferir commit e paths no `MANIFEST.json`

### Rota B — Git folder, se aprovada

- [ ] Confirmar autorização para transportar o repositório completo
- [ ] Confirmar que a história Git foi sanitizada/auditada; **a rota está
      bloqueada enquanto commits antigos contiverem o path pessoal do simulado**
- [ ] Copiar para o destino somente os paths listados no manifesto

### Rota C — criação manual

- [ ] Recriar a estrutura de pastas e subir arquivo a arquivo

Rota usada: `________`

## Fase 3 — limpar o ambiente antigo

Só depois do backup confirmado.

- [ ] Inventariar skills atuais e preservar todas as que não pertencem ao Hub
- [ ] Remover somente skills Hub atuais/legadas listadas em `tools/project_policy.py`
- [ ] Preservar `.assistant/.mcp_servers.json`
- [ ] Remover/substituir somente `hub_padroes`, `hub_prompts`, `hub_scripts` e
      `hub_snippets`, para que helpers obsoletos não sobrevivam
- [ ] Remover `assistant_instructions.md` (sem ponto), que nunca foi lido
- [ ] Conferir que nenhuma pasta pessoal não relacionada foi afetada

## Fase 4 — instalar

O destino é a pasta do **seu usuário do trabalho**. Copie o **conteúdo** da
subárvore, não a pasta de usuário do laboratório.

- [ ] `.assistant_instructions.md` na raiz de `/Users/<username-trabalho>/`
- [ ] `.assistant/` completa no mesmo nível
- [ ] Conferir que o arquivo de instruções tem o **ponto inicial** e o nome exato

## Fase 5 — verificar a estrutura

- [ ] `.assistant/skills/` tem o número de pastas `hub-ml-*` que o `--verify`
      reportou, cada uma com `SKILL.md`
- [ ] `.assistant/` tem os diretórios `hub_` que a linha `extensões` do `--verify` reportou mais `README.md`
- [ ] `.assistant_instructions.md` presente na raiz do usuário
- [ ] Abrir um `.py` de `hub_snippets`: precisa ser **arquivo**, não notebook
- [ ] Abrir `hub_snippets/spark/pit_join/exemplo_pit_join.py`: precisa ser **notebook**
- [ ] `CATALOGO_HELPERS.md` e `GLOSSARIO.md` presentes

> `.py` como notebook quebra `from hub_snippets...`. Notebook como arquivo não tem
> células para executar. Os dois tipos importam.

## Fase 6 — testes de aceitação

O roteamento foi certificado em **36/36 nas 12 skills originais**; a
`hub-ml-criar-objeto`, da Sprint 11, **ainda não foi testada** — inclua-a nos
testes desta fase. O resultado depende só das
descriptions, que são as mesmas. O que **só o trabalho valida** é runtime,
permissão e integração.

- [ ] **Chat novo**: pedir "Faça uma EDA completa da tabela X: granularidade,
      chaves, qualidade e relatório executivo" → deve carregar
      `hub-ml-eda-profissional`
- [ ] **Chat novo**: pedir com `@hub-ml-baseline-ml` → seleção determinística
- [ ] Confirmar que as respostas saem em PT-BR e seguem as preferências
- [ ] Importar `tools/spark_smoke_test.py` como notebook
- [ ] Definir `target_environment=work` e um `mlflow_experiment_path` temporário
- [ ] Executar e confirmar que o run temporário foi excluído
- [ ] Registrar o resultado do smoke test: `________ aprovações / ________ falhas`

Consultar a referência corrente em `docs/testes/spark/README.md`. Módulos de ML
podem parar de acusar dependência ausente, e limitações de `cache()` podem mudar
em compute clássico.

## Fase 7 — registrar

- [ ] Entrada no `CHANGELOG.md` com o commit replicado e o resultado dos testes,
      **sem identificadores corporativos**
- [ ] Divergência entre laboratório e trabalho anotada na matriz de
      `.claude/rules/free-vs-trabalho.md`
- [ ] Qualquer correção necessária feita no `ambiente_fonte/`, nunca só no
      workspace

## Se algo der errado

Restaurar o backup da fase 1 no mesmo caminho e abrir um chat novo. Conferir
também se o run temporário do smoke foi excluído; se não, removê-lo antes de
encerrar o rollback.

## Ressalva sobre os módulos novos

`pit_join`, `join_diagnostics`, `fixtures` e `mlflow_run` têm auditoria de uma
rodada apenas, com o mesmo modelo que os implementou. Essa rodada encontrou treze
defeitos, o que sugere que uma segunda origem encontraria mais. Eles são opt-in:
ninguém os usa sem importar. **Evite `pit_join` em decisão que importe até a
segunda auditoria.**
