# Playbook — ciclo de vida de uma mudança

A mudança começa localmente. Editar documentação não autoriza publicar, executar um notebook, iniciar compute ou promover uma policy. O [guia de ferramentas](../../tools/README.md) é dono dos comandos; a [certificação SEF/SER](../../tools/skill_enforcement/README.md#ser--certificação-prospectiva) prevalece nas superfícies que governa.

## 1. Definir escopo e preparar

Confirme HEAD, worktree, arquivos permitidos e efeitos autorizados. Leia `AGENTS.md`, `CLAUDE.md` e as regras pertinentes. Use as [dependências de manutenção](../../tools/README.md#pré-requisitos-e-efeitos). Registre baseline e falhas preexistentes.

## 2. Editar e validar a fonte

Edite o produto em `ambiente_fonte/`; nunca repare o espelho à mão. Manual é autorado na fonte e sua cópia de leitura na raiz precisa continuar idêntica. Rode `python tools/validate_assistant.py`, checks focais e `python tools/ci_local.py --verbose` quando aplicável. Diferencie PASS, FAIL, bloqueado e não executado. Não use saída sob teste como seu próprio oráculo.

## 3. Gerar em árvore isolada

`python tools/render_simulado.py` mostra o plano. Antes de `python tools/render_simulado.py --write`, inventarie extras e confirme que toda a árvore `Novo_Ambiente_Simulado/` pode ser substituída. Compare todo o pacote e repita os gates após integração. Recursos visuais seguem exclusivamente a [produção v2](../../tools/readme_visuals/README.md#produção-v2--caminho-recomendado).

## 4. Revisar, registrar e integrar

Revise o diff contra os contratos e execute verificações proporcionais. Registre o que de fato passou no `CHANGELOG.md` com atribuição, sem declarar validação de ambiente não executada. Commit e push exigem escopo autorizado; merge e publicação são decisões distintas. ADR aceito mantém corpo imutável; mudança arquitetural exige o processo próprio.

## 5. Validar ambiente somente quando necessário e autorizado

| Mudança | Evidência adicional pertinente |
|---|---|
| prosa/navegação | links, contratos, público e derivados locais |
| API, Spark, ML ou execução | testes focais e runtime alvo autorizado |
| roteamento de skill | positivo, negativo e seleção explícita observados |
| briefing | resposta observada com versão/ambiente e limites próprios |
| autorização/efeitos | certificação do perfil e oráculo independente |

Um contrato de enforcement pode exigir gates adicionais. Não inferir autorização remota de um teste local, nem registrar NOT_RUN como PASS.

## 6. Publicação separada

Depois de autorizados destino, versão e efeito, siga a [skill de publicação](../../.claude/skills/publicar-free/SKILL.md). O modo de plano (`python tools/publicar_free.py`) não escreve remotamente, mas consulta identidade e destino pela CLI autenticada; não é inteiramente offline. `--execute` escreve. `--verify` compara inventário/tipos; `--verify --conteudo` também compara conteúdo. Confira recibos, ausentes e obsoletos; em falha parcial, inspecione a tentativa anterior antes de qualquer retry. A conferência não homologa comportamento Genie.

## 7. Trabalho corporativo

A [replicação no trabalho](replicacao-trabalho.md), seu [checklist](checklist-replicacao.md) e o aceite no destino exigem autorização e evidência próprias. Free não comprova runtime, permissões ou governança corporativa.

## Fontes

- [Entrada e ciclo de contribuição](../../README.md#ciclo-de-contribuição)
- [Fonte do produto](../../ambiente_fonte/README.md)
- [Publicação e conferência](../decisions/ADR-0005-publicacao-propria-no-free.md) / [critério de conteúdo](../decisions/ADR-0008-criterios-de-conferencia-da-publicacao.md)
