# Bloco de proveniência para output durável

> **PADRÃO CUSTOMIZADO DO HUB.** Não é metadata automática do Genie Code. Copie
> este bloco para relatórios, notebooks e especificações que precisem sobreviver
> ao chat; preencha somente o que foi observado.

```yaml
proveniencia:
  gerado_em_utc: "AAAA-MM-DDTHH:MM:SSZ"
  skill_produtora: "hub-ml-..."
  contrato: ".assistant/skills/hub-ml-.../SKILL.md"
  versao_contrato: "commit, tag ou NÃO INFORMADO"
  pedido_original: "link, caminho ou resumo literal"
  recursos:
    - nome: "catalog.schema.table, notebook ou arquivo"
      snapshot_ou_periodo: "versão, timestamp, filtro ou NÃO INFORMADO"
  ambiente: "workspace/runtime/compute ou NÃO INFORMADO"
  execucao: "executado | proposto | parcialmente executado"
  validacoes_executadas: []
  escritas_realizadas: []
  limitacoes: []
```

## Regras

- Não invente commit, timestamp, snapshot, execução ou validação.
- `pedido_original` deve permitir reconstruir a intenção; resumo não substitui o
  texto quando uma decisão depender da formulação exata.
- Liste escrita somente com evidência. Se nada foi escrito, use `[]`.
- Para output sem execução, `recursos` identifica contexto, não prova leitura.
- Se o contrato mudou depois, a auditoria usa `versao_contrato`; sem versão,
  registre a lacuna em vez de presumir o contrato atual.
