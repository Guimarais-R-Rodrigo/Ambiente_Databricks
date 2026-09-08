# Execução das etapas 1 a 5 — 2026-08-29

Registro do fechamento técnico solicitado após a auditoria A2. Identidades e
URLs reais do laboratório não são persistidas; os comandos resolveram o usuário
em runtime e exigiram perfil e host explícitos.

## Resultado executivo

| Etapa | Evidência | Estado |
|---|---|---|
| 1. Checkpoint Git | branch `codex/auditoria-a2-correcoes`, commit `02a5ad3` | PASS |
| 2. Pacote limpo | 315 arquivos + `MANIFEST.json`; hashes internos reconciliados | PASS |
| 3. Publicação Free | 315 esperados; 316 remotos incluindo o MCP da plataforma; 0 ausente/obsoleto | PASS |
| 4. Smoke real | 145 total; 136 PASS; 0 FAIL; 8 opcionais; 1 bloqueio esperado | PASS |
| 5a. 16 famílias de prompts | contrato estático 16/16; envio no chat desabilitado pela cota | BLOQUEADO |
| 5b. 3 forward tests pendentes | `hub-ml-criar-objeto`: positivo, negativo e `@menção` | BLOQUEADO |

## Pacote e publicação

O pacote limpo gerado após o checkpoint foi
`.artifacts/ambiente-databricks-02a5ad328736.zip`, com SHA-256
`DBA1C38940BA82E060FCA27C083C9BDE3F01D8C317D4FE93E1E4319208202E0D`.
O manifesto contém 315 arquivos, declara árvore limpa e teve cada hash conferido
contra o conteúdo do ZIP.

O publicador executou plano, escrita e `--verify` com o mesmo perfil/host Free.
O remoto contém as 13 skills e os 4 diretórios `hub_`; o único arquivo além do
produto é `.assistant/.mcp_servers.json`, gerenciado pela própria plataforma e
preservado conforme a política do projeto.

## Smoke test no runtime

- run do job: `996607251657906`;
- run da tarefa: `657506000110053`;
- estado: `TERMINATED/SUCCESS`;
- runtime: Spark 4.2.0 serverless;
- resultado integral: [2026-08-29_smoke_a2.json](spark/resultados/2026-08-29_smoke_a2.json).

Os oito `OPTIONAL_MISSING` correspondem a bibliotecas declaradas como opcionais.
O caso MLflow recebeu `BLOQUEADO_ESPERADO` apenas porque classe e assinatura da
mensagem coincidiram com o bloqueio conhecido de Spark Connect.

## Bloqueio conversacional

Ao abrir um chat novo no Genie Code depois da publicação, a interface mostrou
`Budget reached. Contact your admin to resume. Resets Sep 1.` e manteve o botão
de envio desabilitado. Portanto nenhuma resposta das 16 famílias e nenhum dos
três forward tests pendentes foi produzido nesta data.

Esse estado não é falha das skills nem dos prompts. Também não é aprovação: a
validação estrutural de 16 prompts/161 campos não substitui uma resposta do
modelo. A retomada deve ocorrer após a renovação da cota, sempre em chat novo:

1. executar os três casos da `hub-ml-criar-objeto` no
   [roteiro de forward tests](forward/roteiro.md);
2. executar uma tarefa autocontida de cada uma das 16 famílias de
   `hub_prompts`, observando contrato, limites e artefato devolvido;
3. registrar PASS/FAIL e qualquer colisão sem reaproveitar conversa.
