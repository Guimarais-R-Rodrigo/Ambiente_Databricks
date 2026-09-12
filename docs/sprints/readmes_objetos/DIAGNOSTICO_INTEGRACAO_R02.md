# Diagnóstico de integração — R01/R02 e Concierge

Data: 12/09/2026. Autor: ChatGPT. Revisão própria (`A0_light`).
**Diagnóstico executado; integração não executada.** Nenhuma branch recebeu merge,
rebase, force-push, alteração de base de PR ou publicação Databricks nesta revisão.

## Bases observadas, não presumidas

| Papel | Commit |
|---|---|
| Ancestral comum | `f748c144dbb6909c7437b53498b25dd4f4854ab7` |
| R01, PR 5, `codex/readmes-r01` | `af1efd14f2a688d3d3cc816ef85f5f1755e8afec` |
| R02 antes do fechamento, PR 6 | `0c76bce9f3fa0f52b4312b60c3059e0fd27a2733` |
| `main` observada com Concierge integrado | `8744157fe9c3e0603f689fb2bcad52445e96cb41` |

O commit novo da main é filho do ancestral comum e altera 59 caminhos.
A consulta ao PR 5 retornou `mergeable: false`; a consulta ao PR 6 retornou
`mergeable: true` contra a R01. O campo `base_sha` do PR 5 ainda mostrava o
ancestral antigo. Por isso a referência da main foi consultada diretamente,
e o diagnóstico local usou o commit real observado, não esse campo defasado.
Esses estados são retratos desta consulta e devem ser reconfirmados antes de integrar.

## Simulação reproduzível

Com histórico completo e árvores originais, foram executados:

```bash
git merge-base af1efd14f2a688d3d3cc816ef85f5f1755e8afec 8744157fe9c3e0603f689fb2bcad52445e96cb41
git merge-tree --write-tree --name-only af1efd14f2a688d3d3cc816ef85f5f1755e8afec 8744157fe9c3e0603f689fb2bcad52445e96cb41
git merge-tree --write-tree --name-only 0c76bce9f3fa0f52b4312b60c3059e0fd27a2733 8744157fe9c3e0603f689fb2bcad52445e96cb41
```

As duas simulações retornaram 1 por conflitos. Esse comando criou objetos
locais de simulação; não alterou arquivos de trabalho nem integrou referências.
Os logs estão em [simulação R01](evidencias_fechamento_r02/diagnostico_merge_r01.txt)
e [simulação R02](evidencias_fechamento_r02/diagnostico_merge_r02.txt).

## Quatro conflitos textuais em ambas as simulações

| Arquivo | Motivo observado e resolução a preparar em etapa autorizada |
|---|---|
| `CHANGELOG.md` | Inserções concorrentes no início. Conservar ambas as entradas históricas e acrescentar a entrada da integração, sem escolher uma história em detrimento da outra. |
| `CLAUDE.md` | Ambas as iniciativas acrescentaram decisões e rotas. Conservar o Concierge integrado e a proposta dos READMEs, com identificadores não ambíguos. |
| `README.md` | Contagens e descrição do gate diferem. Compor conteúdo, executar a árvore resultante e só então atualizar as contagens; não copiar números de uma das branches. |
| `tools/ci_local.py` | A R01 acrescentou a etapa `readmes`; a main acrescentou três etapas do Concierge. Preservar a união, não substituir cinco etapas por sete ou vice-versa. |

A união esperada preserva oito etapas: as quatro comuns, `readmes`,
`concierge-pacote`, `concierge-regressoes` e `concierge-integracao`. Esse número
é derivado da leitura dos dois arquivos. **O gate combinado não foi executado
nem aprovado nesta rodada**, pois nenhuma árvore integrada foi adotada.

## Colisão semântica que o Git não resolve

Existem duas decisões diferentes com número 0011:

- Main: `docs/decisions/ADR-0011-concierge-hub.md`, aceito para integração.
- R01/R02: `docs/decisions/ADR-0011-readmes-de-objeto.md`, ainda proposto.

Os nomes dos arquivos diferem. Por isso, podem coexistir após uma junção textual
sem conflito e continuar ambíguos para pessoas e agentes. Preservar o ADR já
integrado do Concierge e renumerar a proposta dos READMEs é o encaminhamento
recomendado. O número 0012 estava livre na main consultada, **não foi reservado**;
reconfirmar disponibilidade no momento da integração. Não renumerar somente na
R02 enquanto a R01 continua apontando ao número antigo.

Ao renumerar, ajustar título, índice decisório e referências ativas do fluxo.
Registros históricos devem conservar o relato datado, com errata/ponte de
rastreabilidade quando necessário. Não reescrever corpos de ADRs aceitos nem
fazer substituição textual indiscriminada de todo `ADR-0011`, pois isso afetaria
o Concierge legítimo.

## Mesclagem textual automática não é validação semântica

O Git conseguiu combinar automaticamente instruções do produto, READMEs de
entrada, Manual e índices. Esses resultados exigem revisão: manter o Concierge
opcional para descoberta solicitada; manter consulta seletiva aos READMEs;
não transformar descoberta em execução analítica autorizada. O Manual continua
canônico, com três cópias idênticas após sincronização/renderização.

Os derivados devem ser descartados/regenerados pelo renderer a partir da fonte
já reconciliada. A guarda de migração precisa continuar avaliando o histórico
completo e as dispensas apenas decrescentes. Nenhum dos 68 objetos pendentes
pode ser tratado como já documentado por causa da integração do Concierge.

## Encaminhamento, sem execução implícita

Após aceite/autorização de integração: reconfirmar refs; compor a R01 com a main
em uma branch de integração; resolver os quatro conflitos e a colisão do ADR;
revisar os arquivos combinados automaticamente; renderizar; executar todos os
gates preservados; reaplicar/conferir o delta da R02; repetir validações.
Não usar force-push ou apagar PRs anteriores como atalho sem decisão explícita.

A ordem lógica continua R01 antes de R02. Os PRs 5 e 6 continuam rascunhos;
essa revisão não afirma ter tornado o PR 5 mesclável. A CI da R02 contra a R01,
mesmo aprovada, não certifica integração com a main atual.
