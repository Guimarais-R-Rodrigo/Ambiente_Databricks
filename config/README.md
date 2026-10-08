# Configuração individual

Copie `workspace.example.json` para `workspace.local.json` nesta pasta e preencha
os valores somente no computador autorizado. O arquivo local é ignorado pelo Git.
Cada colega mantém seu perfil e suas pastas; exemplos versionados são sintéticos.

| Campo | Significado |
|---|---|
| `schema_version` | versão do contrato; atualmente `1` |
| `profile` | nome do perfil nativo na CLI Databricks |
| `expected_host` | URL HTTPS esperada; deve coincidir com o host do perfil |
| `development_root` | pasta remota de desenvolvimento usada pela extensão |
| `installation_root` | pasta pessoal que receberá `.assistant/` e a instrução irmã |

As duas raízes devem ser distintas, sem sobreposição, abaixo de uma pasta pessoal
`/Users/<usuario>/`. O leitor recusa raízes amplas, caminhos não normalizados,
campos desconhecidos e exemplos não preenchidos. Não acrescente token, senha,
compute ou catálogo a este contrato. Credenciais ficam na autenticação nativa;
outros parâmetros poderão ser acrescentados com versão e necessidade demonstrada.

Da raiz do clone:

```powershell
Copy-Item config/workspace.example.json config/workspace.local.json
python -m tools.trabalho.workspace --check
python -m tools.trabalho.workspace --plan
```

`--check` compara o host com o perfil local, sem conexão e sem mostrar seus valores.
Respeita `DATABRICKS_CONFIG_FILE` e recusa `DATABRICKS_HOST` divergente; a
autenticação efetiva ainda precisa ser conferida na CLI instalada.
`--plan` informa inventário e SHA da fonte. Ambos leem arquivos locais e não
instalam, sincronizam nem publicam. `--show-paths` mostra caminhos apenas no
terminal local; não compartilhe essa saída. O arquivo precisa estar ignorado e
não versionado; a ferramenta recusa configuração adicionada ao índice Git.

Ignorar no Git não impede leitura por uma IA com acesso ao filesystem. Evite
anexar o arquivo ao chat e use apenas os metadados necessários, nunca credenciais.
Configuração pessoal não entra no produto, no kit nem no espelho gerado.

Continue pelo [guia do trabalho](../docs/playbooks/copilot-trabalho.md).
