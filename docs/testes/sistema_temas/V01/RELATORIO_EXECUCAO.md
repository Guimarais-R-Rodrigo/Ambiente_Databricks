# Execução da candidata V01 sobre a main integrada

**Data: 12/09/2026 · autoria: Codex · estado: candidata de revisão.**

O seletor de cores ainda não existe. Esta entrega cria contrato, documentação e
verificações de manutenção; não aplica temas nem muda a rotina de quem usa o Hub.
Para entender a proposta sem executar código, leia o
[guia de primeiro uso](../../../sprints/sistema_temas/V01/GUIA_PRIMEIRO_USO.md).

## Base e o que foi reconciliado

Base efetivamente consultada: `b88a9ccdde6e61892bc25eb7cf4f4b2577badb23`, árvore
`e339983237bd21b2127248f38705c685b03da0f0`, já com os PRs #7 e #8 integrados.
A candidata local anterior `aa70abcf` foi insumo, não uma prova sobre esta base.
Não foi transportada a alternativa antiga de V00. A rota única agora é
`docs/sprints/sistema_temas/V01/`, vinculada à instrumentação integrada.

O ADR-0013 continua **proposto**. A V01 fornece schema 0.1.0, 48 definições para
notebook e 32 editoriais, quatro fixtures completas, governança especificada,
guias, referência gerada e verificadores. Nenhum campo foi ligado ao runtime.

A suíte de integração acrescenta 24 testes aos 114 da candidata anterior.
Reaproveita o parser Markdown e as guardas dos gates já existentes. Confere que
o registro candidato contém exatamente os 12 ativos dos manifestos oficiais,
sem permitir omitir um item para aceitar uma imagem alterada. Valida também
âncoras, navegação, documentação gerada e rastreabilidade dos métodos de teste.

## Resultados locais efetivamente observados

| Verificação | Resultado |
|---|---|
| Contrato local | PASS; quatro fixtures, 80 definições, 12 ativos, 52 links locais e suas âncoras. |
| Testes V01 | 138 métodos aprovados, sem skip. Subtestes não contados separadamente. |
| CI vigente | Oito etapas aprovadas; 202 métodos, 195 aprovados e sete skips Spark. |
| Instrumentação V00 | 48 métodos aprovados: 27 de inventário, 12 de legado, nove de relatórios. |
| Publicador visual | 29 métodos aprovados, com mocks; nenhuma publicação real. |
| Arquivos do produto e espelho | 441 + 441 preservados byte a byte contra a base. |
| Manual da raiz, gate e dois workflows existentes | Quatro arquivos preservados byte a byte. |
| Capturas sintéticas legadas | JSON idêntico antes/depois, mesmo ambiente e código V00. |
| Validação editorial Node | BLOQUEADA por ausência de sharp; sem homologação editorial. |

As versões, comandos, códigos de saída e hashes de logs estão no
[registro estruturado](EVIDENCIAS_LOCAIS.json). Logs brutos, capturas e tentativas
intermediárias acompanham o pacote de evidências desta entrega. O CI remoto,
quando executado, identifica seu commit no PR; não se confunde com esta medição local.
Os comandos de reprodução ficam no
[guia do mantenedor](../../../sprints/sistema_temas/V01/GUIA_MANTENEDOR.md).

As repetições próprias não são auditoria independente. O teste de biblioteca
não equivale a treinamento, consulta ou validação de negócio. A inspeção de
bytes não equivale a análise visual e os links válidos não provam compreensão.

## Tentativas malsucedidas e correções

A primeira cópia tinha histórico raso: o gate de READMEs a recusou. Foi obtido
histórico completo e o CI da base passou nas oito etapas, sem relaxar a guarda.
O transporte inicial bem-sucedido não foi anunciado como teste de software.

Na primeira validação da candidata faltava registrar a remoção do workflow
transitório e atualizar as contagens locais do README. O índice foi preparado
e os números foram reconciliados com o validador, sem alterar saídas históricas
de publicação remota. O gate completo então passou.

Uma tentativa de localizar os testes do publicador em `tools/` retornou zero
casos, com código 5. Não foi considerada aprovação; foi repetida na pasta
`tools/readme_visuals/tests/`, com os 29 métodos reais aprovados.

O Node foi tentado em uma cópia descartável da base, retornando
`ERR_MODULE_NOT_FOUND` para sharp antes de validar assets. Nenhum QA antigo
foi aproveitado como resultado novo. A falha global anterior relacionada ao
catálogo removido continua dívida registrada na V00, não corrigida aqui.

## Preservação, publicação e aceite

Não foram editados `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, `MANUAL_TECNICO.md`,
`tools/ci_local.py` ou os workflows permanentes anteriores. Não foi necessário
renderizar o espelho nem transportar arquivos ao Databricks. As oito etapas do
CI convivem com o workflow separado V01, que tem apenas permissão de leitura.
Artefatos temporários de preparação/transporte não integram a árvore final.

Nesta etapa, a publicação é somente uma candidata Git em `codex/temas-v01`.
O registro do PR é a referência para o commit remoto e os checks. Não há merge
presumido, aprovação arquitetural automática nem publicação no workspace.

Continuam pendentes o aceite do ADR, a revisão independente, a avaliação do guia
com iniciante e a homologação nos ambientes pertinentes. Papéis e transições são
oráculos sintéticos: não há autenticação ou persistência operacional instalada.
O tema legado continua intacto. A V02 não foi iniciada.

[Voltar à V01](../../../sprints/sistema_temas/V01/README.md) ·
[Checkpoint](../../../sprints/sistema_temas/V01/CHECKPOINT_V01.md)
