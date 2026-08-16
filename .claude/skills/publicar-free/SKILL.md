---
name: publicar-free
description: >-
  Publica o ecossistema no workspace Databricks Free em três fases (plano,
  publicação com gate, verificação) e interpreta o resultado. Use após validar e
  renderizar, sempre que o laboratório precisar refletir o estado do repositório.
---

# Publicar no Databricks Free

## Sequência obrigatória

```powershell
python tools/validate_assistant.py       # 1. fonte válida
python tools/render_simulado.py --write  # 2. simulado atualizado
python tools/publicar_free.py            # 3. plano (dry-run)
python tools/publicar_free.py --execute  # 4. publicação
python tools/publicar_free.py --verify   # 5. conferência independente
```

Nunca pular o passo 5: a publicação relata o que enviou, o `verify` confere o
que existe. São coisas diferentes.

## O que o verify cobre

| Verificação | Por que importa |
|---|---|
| Arquivos ausentes | envio parcial passa despercebido no log de publicação |
| **Arquivos obsoletos** | `import-dir --overwrite` sobrescreve mas nunca apaga: arquivo removido da fonte continua ativo no workspace |
| `.py` como `FILE` | como `NOTEBOOK`, `from hub_snippets...` deixa de funcionar |
| 12 pastas de skill | descoberta incompleta é silenciosa |
| 4 diretórios `hub_` | extensões ausentes só aparecem no uso |

## Interpretar e agir

- **obsoleto no remoto**: remover à mão (`databricks workspace delete <path>`) e
  reexecutar o verify. Avaliar se o arquivo deveria ter sido removido da fonte
  em algum momento e se isso está registrado.
- **importado como NOTEBOOK**: republicar; se persistir, conferir o formato de
  importação. O correto para `.py` é `AUTO`.
- **ausente**: republicar e verificar permissão de escrita no caminho.

## Guardrails

- A ferramenta recusa usuário com aparência corporativa: ela publica no
  laboratório. O workspace do trabalho usa o runbook manual
  ([replicacao-trabalho.md](../../../docs/playbooks/replicacao-trabalho.md)).
- Somente dados sintéticos no Free; nenhum identificador do trabalho.
- Após publicar skills alteradas, abrir **chat novo** no Genie Code; havendo
  cache de metadata, recarregar a página.
- Alteração de `description` invalida a certificação de roteamento: reexecutar
  os forward tests afetados ([roteiro](../../../docs/testes/forward/roteiro.md)).

O padrão de três fases vem do engine `databricks-genie` do Verg_Alchemy_Hub; o
ADR-0005 registra por que o código não é consumido diretamente.
