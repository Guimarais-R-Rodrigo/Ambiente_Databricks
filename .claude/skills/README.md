# Skills operacionais do repositório

> **CONTEXTO DE MANUTENÇÃO · NÃO PUBLICADO.** Estas skills orientam o agente que
> trabalha no Git. As skills `hub-ml-*` em `ambiente_fonte/` são o produto usado
> pelo Genie Code no Databricks.

## Não confunda as duas famílias

| | `.claude/skills/` | `ambiente_fonte/.assistant/skills/` |
|---|---|---|
| usuário | agente que mantém este repositório | usuário do Genie Code |
| atua sobre | fonte, render, publicação e gates | dados, notebooks, modelos e pipelines |
| vai ao workspace | não | sim |
| exemplo | “publique e confira o Free” | “faça uma EDA desta tabela” |

## Rotas disponíveis

| Intenção | Skill operacional | Saída esperada |
|---|---|---|
| validar o produto | `validar-assistant` | gate local com falhas acionáveis |
| gerar o espelho | `render-simulado` | `Novo_Ambiente_Simulado/` regenerado |
| publicar no laboratório | `publicar-free` | execute + verify com host/perfil explícitos |
| testar roteamento | `forward-test-skills` | registro positivo, negativo e `@menção` |
| copiar para o trabalho | `replicar-trabalho` | pré-condições, cópia e verificação no destino |

O pedido em linguagem natural aciona a rota pertinente. O `SKILL.md` explica
pré-condições, comandos, critério de sucesso e quando parar.

## Criar ou alterar uma skill operacional

1. Crie `.claude/skills/<nome>/SKILL.md`.
2. Use `name` igual ao nome da pasta e `description` com gatilho claro.
3. Mantenha automação executável em `tools/`; a skill deve orquestrá-la, não
   duplicá-la.
4. Teste sucesso e falha representativa.
5. Atualize esta tabela e o `CHANGELOG.md`.

Volte ao [README raiz](../../README.md) ou às
[ferramentas executáveis](../../tools/README.md).
