# R03-A — contrato estável e sete guias de apoio

**Data:** 2026-09-12. **Autor/revisor:** ChatGPT (A0_light).
**Base:** main integrada `5493f7db68f397ad7040485cb09bad53eb79be74`.
**Branch de trabalho:** `codex/readmes-r03a`. **Parada:** antes da R03-B.

## 1. Aceite e integração anteriores

Rodrigo aprovou explicitamente a candidata R02-I e a continuidade. O PR nº 7
foi integrado após reconferência de base, head e CI. O [registro de aceite](ACEITE_V1.md)
contém a decisão humana e o SHA retornado pelo GitHub. As branches antigas não
foram reescritas; os PRs nº 5/#6 não devem ser mesclados novamente como trabalhos
independentes. Nenhum workspace foi publicado.

## 2. Contrato 1.0.0

O template mantém o conteúdo das quinze seções. Sua abertura e o checklist
passam a registrar a versão estável, e o ADR-0012 recebe ratificação anexada.
Os três exemplares e os seis pilotos anteriores mudam **somente no marcador**
de versão; não foram reescritos nem recertificados operacionalmente. O controle
de migração mantém seu baseline e retira apenas as sete dispensas do lote.

O aceite prévio não aprova estes sete textos novos. Esta entrega é revisada
pelo próprio autor e submetida em branch própria; não é auditoria independente.

## 3. READMEs novos

| Objeto | Papel da explicação |
|---|---|
| constants/colors | Cor semântica, três paletas, escolha de escala, cópias locais e contraste. |
| constants/emojis | Vocabulário e roteiro consultáveis, sem executar ou impor a EDA. |
| constants/styles | HTML/CSS e uso explícito, sem prometer reestilização global. |
| testing/fixtures | Quatro geradores, grão, seed, probabilidades, memória e limites da simulação. |
| visual/badge | Estado, cortes, arredondamento, validações ausentes e acessibilidade. |
| visual/divider | Hierarquia visual complementar a títulos; quatro strings HTML. |
| visual/kpi_card | Resumo de métricas já calculadas, duas saídas e limites de formatação/escape. |

Os sete possuem conceito, escolha, contraexemplo, intuição, cenário, requisitos,
retornos, rota operacional, configurações, riscos, alternativas, verificação,
arquivos e referências. Foram lidos módulos, fachadas e notebooks. A rubrica
por objeto não usa médias que escondam problemas materiais.

**Cobertura estrutural esperada e conferida pelo gate:** 13/74 operacionais,
3/3 exemplares, 61 pendentes. Aceite editorial dos novos guias permanece separado.

## 4. Outras documentações efetivamente alteradas

A [matriz nominal](MATRIZ_ALTERACOES_R03A.md) vem do diff contra a base integrada.
Distingue sete READMEs novos, nove marcadores anteriores, sete notebooks com
mudança documental, documentos de governança/navegação, evidências e espelhos.

Foram atualizados template e checklist, regra editorial, CLAUDE, índice e
ratificação do ADR, índice/checkpoint da iniciativa, PLANO_HUB, índice de sprints,
README da raiz, coleção de snippets, Manual canônico/cópia e CHANGELOG. Os
sete exemplos ganharam backlink e correções pontuais de prosa; saídas históricas,
AST e magics executáveis foram preservados. O Manual apresenta a rota local por
pasta, sem acrescentar links relativos que quebrem sua cópia idêntica na raiz.

**Sem alteração:** helpers, fachadas, APIs, dependências, código dos gates,
workflows permanentes, formulários de prompts, skills operacionais, imagens e
Concierge. Nenhum README de categoria foi antecipado. [Achados](ACHADOS_R03A.md)
registram limites que exigiriam tarefas funcionais ou visuais separadas.

## 5. Verificação e alcance

O baseline local foi executado antes das edições: oito etapas aprovadas, 195
casos aprovados e sete testes opcionais Spark pulados. O fechamento reexecutou e aprovou
as mesmas oito etapas; reexecuções não são novos casos. Logs integrais de
baseline, gate final e preservação acompanham esta entrega.

O suplemento `verificar_r03a.py` contém **26 casos**: 17 portáteis e nove de
Spark. Localmente os 17 portáteis passaram, incluindo execução dos seis blocos
Python dos respectivos READMEs; os nove Spark foram pulados por ausência de
PySpark. A tentativa de instalação local falhou por resolução de rede, não por
incompatibilidade comprovada. `--require-spark` impede classificar uma execução
sem Spark como validação completa.

O runner isolado executará o suplemento com Spark real; seu resultado só deve
ser considerado após ler logs/artefato. Resultados remotos posteriores a este
registro ficam no comentário de fechamento do PR e no pacote da conversa,
sem reescrever uma execução local como remota. O workflow temporário não faz
merge nem publica dados; a árvore final precisa coincidir com a testada.

Uma validação da string HTML e um cálculo de contraste não são homologação
visual do Databricks, teste de leitor de tela ou impressão. Não foi executado
notebook no workspace, tracking, treino ou teste conversacional da Genie Code.

## 6. Critérios de revisão e achados

O objetivo didático é autonomia para escolher, não ensinar todos os detalhes
do ecossistema a cada arquivo. As palavras de uso menos familiar são definidas;
quantidade de palavras não aprova o documento. Alertas sobre CSS, precisão,
probabilidades e limites das fixtures se referem à implementação real.

Não foi necessário mudar a estrutura do template depois do piloto. A revisão
é A0_light; a necessidade de A1+ antes de distribuir à squad/trabalho permanece.
O aceite recebido refere-se ao padrão/pilotos/integração anteriores, não a uma
leitura humana já realizada dos textos novos.

## 7. Checkpoint e próxima autorização

R03-A termina com sete guias em branch separada. Não fazer merge automático do
novo lote só porque o PR nº 7 foi aprovado: são conteúdos diferentes. Reconfirmar
main/CI antes de uma integração autorizada. A próxima leva **R03-B** contém
correlation_matrix, dataframe_styled, distribution_grid, index_generator,
section_header e theme_plotly e **não foi iniciada**. Nenhum deles ganhou README
nesta rodada. [Controle de migração](CONTROLE_MIGRACAO.json).
