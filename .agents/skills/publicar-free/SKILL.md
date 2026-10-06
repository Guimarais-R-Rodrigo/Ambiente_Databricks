---
name: publicar-free
description: >-
  Prepara, publica e confere o Hub no Databricks Free em fases separadas, com
  destino e autorização explícitos. Use para plano remoto, publicação ou
  verificação do laboratório; não para publicação corporativa ou análise local.
---

# Publicar no Databricks Free

## Intenção, pré-condições e autoridade

Use para sincronizar ou conferir a cópia do laboratório. O owner é
[publicar_free.py](../../../tools/publicar_free.py); o motivo do publicador
próprio está no [ADR-0005](../../../docs/decisions/ADR-0005-publicacao-propria-no-free.md).
A ferramenta não é o engine externo do Hub e não se aplica ao trabalho.

Precisa de fonte validada, espelho atual, CLI Databricks disponível/autenticada
e destino Free conhecido. Sonde o estado atual: documentação de uma máquina
não comprova que esta sessão tem CLI, credencial ou permissão. Ausência ou
ambiguidade bloqueia a fase dependente; não peça segredos em arquivos/Git.

Defina operação, perfil, origem HTTPS do host e home de destino. A autorização
para planejar ou verificar não cobre `--execute`, substituição de arquivos,
limpeza de obsoletos ou outro workspace. Carregar esta skill não concede acesso.
O gate do código compara host ativo e declarado, exige perfil/host explícitos
para escrita e recusa identidade com aparência corporativa; isso **não
substitui autorização humana nem prova sozinho que um host é Free**.

## Fases separadas

1. Rode [validar-assistant](../validar-assistant/SKILL.md).
2. Confira o espelho; se precisar regenerá-lo, cumpra o preflight e a autoridade
   de substituição de [render-simulado](../render-simulado/SKILL.md).
3. Com acesso remoto permitido, gere o plano abaixo. Substitua placeholders no
   ambiente autorizado; não versione identidades/hosts pessoais ou corporativos.

```sh
python tools/publicar_free.py --profile <free> --expected-host <url-free>
```

Mesmo sem `--execute`, o plano chama a CLI autenticada (`current-user me` e
`auth describe`) para resolver usuário/host/perfil. **Não é dry-run offline.**
Não escreve no workspace, mas consulta o remoto. Sem autorização/acesso, limite-se
à inspeção local do código, fonte e espelho; não simule um plano remoto concluído.
O código aceita `DATABRICKS_FREE_PROFILE`/`DATABRICKS_FREE_HOST` como defaults;
prefira flags explícitas para tornar o destino revisável.

4. Antes da escrita, compare inventário remoto, pacote e propriedade dos paths;
   identifique sobreposições com conteúdo alheio/MCP. O plano não é reconciliação
   completa do remoto. Pare se uma substituição sair do escopo autorizado.
5. Só com destino e escopo de escrita aprovados:

```sh
python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>
```

O execute recusa espelho divergente da fonte antes de escrever, importa o pacote
com sobrescrita e materializa notebooks conforme o owner. Não é atômico;
`import-dir --overwrite` não remove objetos que saíram da fonte.

6. Confira sempre o estado observado, mesmo após um envio aparentemente bom:

```sh
python tools/publicar_free.py --verify --profile <free> --expected-host <url-free>
python tools/publicar_free.py --verify --conteudo --profile <free> --expected-host <url-free>
```

## Alcance das verificações

- `--verify`: lê inventário e tipos, encontra ausentes, obsoletos (inclusive
  diretórios vazios), skills ausentes/inesperadas e hubs requeridos.
- `--verify --conteudo`: acrescenta exportação/comparação de conteúdo e checagem
  fonte/espelho. Normaliza CRLF/CR para LF e, só em notebooks, a quebra final.
  É igualdade segundo essa normalização, não identidade bruta remota universal.
- `--verify --conteudo --relatorio <arquivo.json>` grava evidência **local** com
  SHA de origem, escopo, hashes, arquivos comparados e erros. Revise/sanitize
  logs antes de versionar; stdout também pode mostrar identidade e host.
- `--verify --rapido` é apenas conferência parcial de diretórios; não encerra a
  publicação. `--rapido` não combina com `--conteudo` nem `--relatorio`.
  `--execute` e `--verify` são mutuamente exclusivos.

Use `EXPECTED_SKILL_NAMES` e `EXPECTED_HUB_DIRS` de
[project_policy.py](../../../tools/project_policy.py), não contagens antigas de
skills/hubs. O manifesto físico inclui assets editoriais quando declarados.
O critério centralizado segue [ADR-0008](../../../docs/decisions/ADR-0008-criterios-de-conferencia-da-publicacao.md).

## Tipos, falhas parciais e preservação

[notebook_marker.py](../../../tools/notebook_marker.py) distingue pelo conteúdo:
módulos `.py` ficam `FILE` para permitir import; `.py` didáticos com marcador
válido viram `NOTEBOOK`, normalmente sem `.py` no path remoto. Não trate todo
`.py` como FILE. O publicador reconhece materialização pelo `import-dir` e usa
fallback `SOURCE` somente quando necessário. Tipo errado exige diagnóstico do
marcador/importação, não renomeação ou republicação cega.

Se falhar no meio, não conclua “nada foi escrito”. Preserve log/recibo disponível
e SHA, liste o estado remoto e compare antes de retry. Uma verificação sem
conteúdo não prova que uma tentativa parcial deixou os bytes corretos.
Ausente pede diagnóstico de permissão/envio; espelho velho exige voltar ao render.

“Obsoleto” é diferença de inventário, **não autorização para excluir**. Confirme
propriedade, necessidade, backup e escopo explícito para qualquer limpeza;
preserve conteúdo alheio e `.assistant/.mcp_servers.json`, gerido pela plataforma.
Não apague `.assistant/` ou `skills/` inteiras, nem desative um guardrail para
fazer o verify passar. Recusa de acesso permanece bloqueio.

Somente dados sintéticos no Free. Após skills alteradas, use chat novo; se a
metadata continuar antiga, recarregue a página. Mudança de `description` requer
retestes afetados pelo [procedimento de forward](../forward-test-skills/SKILL.md).
Registre fases efetivamente executadas, SHA, exit codes, veredictos e limites no
recibo/evidência datada da publicação. A raiz recebe apenas o marco pertinente,
conforme o [critério](../../../docs/ai/templates/changelog-entry.md). Verify conclui com APROVADO/REPROVADO e
retorno 0/1. Publicar não certifica roteamento Genie nem ambiente corporativo;
para este último, use [replicar-trabalho](../replicar-trabalho/SKILL.md).

## Casos de aceitação do procedimento

- **Positivo:** “Prepare o plano no Free autorizado.” Resolver/conferir destino
  e relatar plano remoto, sem executar publicação por inferência.
- **Negativo de intenção:** “Publique no workspace do trabalho.” Recusar esta
  rota e seguir o runbook corporativo, sem chamar o publicador Free.
- **Pré-requisito ausente:** CLI/credencial, host confirmado ou autoridade de
  escrita ausente. Parar a fase afetada; mock local não equivale a operação real.
