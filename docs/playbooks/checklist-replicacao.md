# Checklist de replicação no trabalho

> **Números desatualizados pela reestruturação do Hub (Sprint 2, 16/08/2026).**
> As contagens de arquivos, diretórios e nomes de skill neste documento
> referem-se à estrutura anterior. O procedimento continua válido; os
> números serão refeitos na Sprint 12, após a conversão terminar. Confira o
> estado real com `python tools/publicar_free.py --verify`.

Documento de acompanhamento, para marcar enquanto executa. O procedimento
completo, com o porquê de cada passo, está em
[replicacao-trabalho.md](replicacao-trabalho.md).

**Versão a replicar:** commit `ac9a782` · 174 arquivos · 12 skills · 6 diretórios
de extensão · 4 notebooks didáticos.

Preencha ao final: data \_\_\_\_\_\_\_\_ · executado por \_\_\_\_\_\_\_\_

---

## Fase 0 — antes de sair desta máquina

- [ ] `git status` limpo e sincronizado com o remoto
- [ ] `python tools/validate_assistant.py` aprovado
- [ ] `python tools/publicar_free.py --verify` aprovado
- [ ] Anotar o commit que está sendo replicado: `________`
- [ ] Confirmar que o repositório está acessível pelo GitHub a partir do outro
      computador (login e permissão)

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

### Rota A — Git folder (preferível)

- [ ] Workspace → Repos/Git folders → Add → URL do repositório
- [ ] Autenticar (token pessoal do GitHub, se exigido)
- [ ] Confirmar que o clone trouxe `Novo_Ambiente_Simulado/`

### Rota B — download e importação manual

- [ ] Baixar o ZIP do repositório no computador do trabalho
- [ ] Extrair e localizar `Novo_Ambiente_Simulado/Users/<qualquer>/`
- [ ] Importar pela UI do workspace

### Rota C — criação manual

- [ ] Recriar a estrutura de pastas e subir arquivo a arquivo

Rota usada: `________`

## Fase 3 — limpar o ambiente antigo

Só depois do backup confirmado.

- [ ] Remover `/Users/<username-trabalho>/.assistant/skills/` inteira
- [ ] Remover `.mcp_servers.json`, se existir
- [ ] Remover `assistant_instructions.md` (sem ponto), que nunca foi lido
- [ ] Conferir que nenhuma pasta pessoal não relacionada foi afetada

## Fase 4 — instalar

O destino é a pasta do **seu usuário do trabalho**. Copie o **conteúdo** da
subárvore, não a pasta de usuário do laboratório.

- [ ] `.assistant_instructions.md` na raiz de `/Users/<username-trabalho>/`
- [ ] `.assistant/` completa no mesmo nível
- [ ] Conferir que o arquivo de instruções tem o **ponto inicial** e o nome exato

## Fase 5 — verificar a estrutura

- [ ] `.assistant/skills/` tem 12 pastas `rodrigo-*`, cada uma com `SKILL.md`
- [ ] `.assistant/` tem os 4 diretórios `hub_` mais `README.md`
- [ ] `.assistant_instructions.md` presente na raiz do usuário
- [ ] Abrir um `.py` de `hub_snippets`: precisa ser **arquivo**, não notebook
- [ ] Abrir um notebook de `hub_snippets/_notebooks_a_migrar/`: precisa ser **notebook**
- [ ] `CATALOGO_HELPERS.md` e `GLOSSARIO.md` presentes

> `.py` como notebook quebra `from hub_snippets...`. Notebook como arquivo não tem
> células para executar. Os dois tipos importam.

## Fase 6 — testes de aceitação

O roteamento já foi certificado no laboratório (36/36) e depende só das
descriptions, que são as mesmas. O que **só o trabalho valida** é runtime,
permissão e integração.

- [ ] **Chat novo**: pedir "Faça uma EDA completa da tabela X: granularidade,
      chaves, qualidade e relatório executivo" → deve carregar
      `rodrigo-eda-profissional`
- [ ] **Chat novo**: pedir com `@rodrigo-baseline-ml` → seleção determinística
- [ ] Confirmar que as respostas saem em PT-BR e seguem as preferências
- [ ] Importar `tools/spark_smoke_test.py` como notebook e executar
- [ ] Registrar o resultado do smoke test: `________ aprovações / ________ falhas`

Resultado de referência no laboratório: 64 aprovações, nenhuma falha. Diferenças
esperadas no trabalho: módulos de ML podem parar de acusar dependência ausente,
e falhas ligadas a `cache()` desaparecem em compute clássico.

## Fase 7 — registrar

- [ ] Entrada no `CHANGELOG.md` com o commit replicado e o resultado dos testes,
      **sem identificadores corporativos**
- [ ] Divergência entre laboratório e trabalho anotada na matriz de
      `.claude/rules/free-vs-trabalho.md`
- [ ] Qualquer correção necessária feita no `ambiente_fonte/`, nunca só no
      workspace

## Se algo der errado

Restaurar o backup da fase 1 no mesmo caminho e abrir um chat novo. Como o
ecossistema é conteúdo estático — sem job, sem serving, sem escrita em dados —
o rollback não deixa efeito residual.

## Ressalva sobre os módulos novos

`pit_join`, `join_diagnostics`, `fixtures` e `mlflow_run` têm auditoria de uma
rodada apenas, com o mesmo modelo que os implementou. Essa rodada encontrou treze
defeitos, o que sugere que uma segunda origem encontraria mais. Eles são opt-in:
ninguém os usa sem importar. **Evite `pit_join` em decisão que importe até a
segunda auditoria.**
