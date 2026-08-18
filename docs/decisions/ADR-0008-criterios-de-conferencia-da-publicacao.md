# ADR-0008 — O que a conferência da publicação verifica

- **Status:** Aceito
- **Data:** 2026-08-17
- **Supersede:** o ADR-0005 no **critério de conferência**. A decisão de fundo —
  publicar com ferramenta própria, em três fases — continua valendo.

## Contexto

O ADR-0005 decidiu, em 2026-08-15, publicar no Free com ferramenta própria em vez
do engine do Hub, em três fases: plano, publicação com gate, conferência
independente. A decisão está certa e não muda.

O que envelheceu foi a lista do que a conferência verifica. O ADR-0005 fecha
declarando que ela valida *"`.py` como `FILE`, 12 skills, 6 diretórios de
extensão, ausência de obsoletos"*. Dois dos quatro deixaram de descrever o
repositório:

| ADR-0005 dizia | Hoje |
|---|---|
| 12 skills | **13** — a `hub-ml-criar-objeto` entrou na Sprint 11 |
| 6 diretórios de extensão | **4**: `hub_padroes`, `hub_prompts`, `hub_scripts`, `hub_snippets` |

O "6" vinha da época de `x_config/`, `x_docs/`, `x_projects/` e afins, removidos
na Sprint 2. O ADR é imutável e descreve corretamente o repositório de 15/08.

E há uma verificação que o ADR-0005 não previa, porque o problema não existia:
**o tipo de cada objeto**. Depois da conversão para pasta de objeto, cada pasta
tem um `.py` que precisa ser `FILE` e um `exemplo_*.py` que precisa ser
`NOTEBOOK`. Trocar os dois quebra o import sem erro visível.

## Decisão

**1. O critério de conferência deixa de citar números no corpo dos ADRs.** Ele
passa a ser declarado no código, onde é conferível:

| O que | Onde vive |
|---|---|
| contagem de skills | `EXPECTED_SKILLS` em `tools/publicar_free.py` |
| diretórios de extensão | `EXPECTED_HUB_DIRS` no mesmo arquivo |
| tipo de cada objeto | a conferência de `FILE` × `NOTEBOOK` do `--verify` |
| obsoletos no remoto | comparação entre esperados e remotos, arquivos **e** diretórios |
| arquivos geridos pela plataforma | `GERENCIADOS_PELA_PLATAFORMA`, hoje só `.mcp_servers.json` |

Número em ADR envelhece sem que nada acuse; número em constante de código reprova
a execução quando diverge. Foi o que aconteceu na Sprint 11: subir
`EXPECTED_SKILLS` para 13 foi parte da mudança, não uma correção posterior.

**2. A conferência de obsoletos é obrigatória e não é opcional.** `import-dir
--overwrite` sobrescreve e **nunca apaga**. Toda sprint que renomeia, converte ou
remove precisa de remoção explícita antes do `--verify`.

Isso não é teoria: a conferência pegou 121 arquivos obsoletos na Sprint 2, 12
pastas de skill órfãs na 3, 16 arquivos planos na 5, e — o caso que ninguém
previu — dez arquivos de log que o CatBoost escreveu dentro de `.assistant`
durante a Sprint 8.

**3. O arquivo gerido pela plataforma é separado dos obsoletos.** Abrir o painel
de MCP em Genie Code → Settings **escreve** `.assistant/.mcp_servers.json`. Ele
não vem da fonte e não deve ser apagado; a conferência o lista à parte.

## Consequências

**Positivas.** O `--verify` virou o portão que mais pegou defeito nesta fase, e
pegou classes que a validação local não vê por construção — ela olha o disco, ele
olha o workspace. Os quatro casos citados acima são todos dele.

**Negativas.** A remoção de obsoleto continua manual, com `databricks workspace
delete`. Automatizá-la exigiria dar à ferramenta permissão de apagar no
workspace, e a assimetria atual — publica sozinho, apaga com a pessoa no comando
— é deliberada.

## Alternativas descartadas

**Fazer o `--execute` apagar o que sobrou.** Seria conveniente e perigoso: um bug
na lista de esperados apagaria trabalho de outra pessoa no mesmo workspace. A
conferência que **relata** e a remoção que **você executa** custam um comando a
mais e não têm esse modo de falha.

**Manter os números no ADR e atualizá-los.** ADR aceito é imutável. Números vivem
em código.

## Referências

- ADR-0005, superseded no critério de conferência
- Ferramenta: `tools/publicar_free.py`; skill: `.claude/skills/publicar-free/`
- `PLANO_HUB.md` §7.3, limpeza remota obrigatória
