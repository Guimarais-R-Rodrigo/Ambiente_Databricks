# V02 — relatório da implementação candidata

Data: 12/09/2026. Autor: Codex. Base do produto:
`836f23684cf76ee1f3d7898d44acb70d32a7ff59` (V01 e correção documental integradas).
O manifesto externo da entrega informa o commit e a árvore finais, evitando
atribuir a este arquivo um hash autorreferente. Nenhuma publicação Databricks.

## Implementação observada

Núcleo com import apenas da biblioteca padrão; validação explícita usa
jsonschema 4.26.0 e referencing 0.37.0. Schema 0.1.0 promovido sem mudar bytes,
referência gerada, exemplos congelados, manifesto relativo, dados imutáveis,
origens, hashes de bytes e conteúdo, fingerprint e exportação somente em memória.

V01 passa a usar as mesmas funções de validação. Seus 138 testes conservam as
asserções; só as duas referências ao arquivo de schema foram atualizadas. O
CI conserva as oito etapas anteriores e acrescenta a etapa de temas. O exemplo,
README de quinze seções, guia de erros e Manual explicam o alcance real.

## Rodadas e alcance

O baseline remoto `34711683992` executou a versão anterior em Python 3.12.
O segundo baseline `34712744652` acrescentou um bundle de leitura do histórico
Git para reprodução local. Nenhum desses runs, sozinho, comprova a V02.

O primeiro snapshot local permitiu testar o núcleo, mas o gate de READMEs
recusou a ausência de histórico. O histórico real foi recuperado do próprio
repositório, sem inventar commits nem relaxar a guarda. A validação integral
passou depois de a candidata ser vinculada à base real e seus contadores serem
reconciliados com a medição. As rodadas reprovadas permanecem nos logs da entrega.

O ambiente local é Linux, Python 3.13.5. Foram observados: 105 testes V02,
138 V01, 48 V00 e 29 do publicador aprovados. O CI tem nove etapas; seus casos
incluem V01 e V02, portanto não somar esses dois conjuntos novamente. Os sete
SKIPs de testes que exigem Spark permanecem explicitamente não executados.
O pacote externo registra a repetição final depois da documentação e a
reimportação independente do bundle em outra pasta pelo mesmo autor.

Execuções remotas da candidata, se realizadas, devem aparecer com seu próprio
commit materializado, árvore e logs; o sucesso de um baseline não é transferido
para outra árvore. Revisão própria ou reprodução em outra pasta não equivale
a auditoria independente.

## Preservação

Dos 441 arquivos anteriores do produto, 438 permanecem idênticos; mudam somente
o Manual e os READMEs das coleções de padrões e snippets. Quinze arquivos novos
são adicionados ao produto; o espelho é gerado, não editado à mão. Os 211 arquivos
Python anteriores do produto e todos os ativos gráficos anteriores permanecem
iguais. O schema foi movido da V01 para o padrão; a cópia antiga não fica ativa.
As três cópias do Manual são iguais e o trecho anterior é preservado.

## Limites que não se tornam aprovação

Databricks, Windows, Spark, widgets, Apps, AI/BI, avaliação com iniciante,
acessibilidade perceptual e auditoria independente não foram homologados.
A validação editorial global Node não foi executada para esta mudança; sua
pendência preexistente continua aberta. Nenhuma credencial de workspace ou dado
corporativo foi usado. Não foi criado painel, adaptador novo nem regra analítica.

## Próxima ação e recuperação

Revisar a candidata completa, seu diff e seu bundle em branch própria. A execução
V02 não autoriza merge nem V03 automaticamente. Após aceite, a integração precisa
conferir a main atual, repetir os gates e verificar a árvore realmente integrada.
Sem merge, o descarte da candidata não exige restaurar um tema no Databricks.

[Guia de reprodução](../../../sprints/sistema_temas/V02/TESTES.md)
