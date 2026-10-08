# Preparação pessoal no trabalho

`workspace.py` lê a [configuração individual](../../config/README.md), compara
o host do perfil nativo e calcula destinos do payload canônico. Não usa rede,
não escreve configuração nativa e não instala arquivos no workspace.

```powershell
python -m tools.trabalho.workspace --check
python -m tools.trabalho.workspace --plan
```

A fonte do plano é `ambiente_databricks/`, nunca a raiz inteira do clone.
Configuração, `.git`, docs, skills de manutenção e tools ficam fora do payload.
O SHA é a base Git; `working_tree_dirty` registra mudanças locais e os hashes
identificam os bytes efetivamente planejados. Plano sujo não é release aprovada.

Consulte o [guia operacional](../../docs/playbooks/copilot-trabalho.md) antes de
qualquer integração remota. O publicador Free mantém seu contrato próprio.
