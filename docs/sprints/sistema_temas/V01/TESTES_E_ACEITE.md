# Testes e aceite da V01

A [matriz estruturada](matriz_testes.json) liga os 17 cenários do plano à sua
verificação. CON-01 a CON-12 são verificáveis como contrato local; DOC-02,
DOC-03, A11-01, SEC-01 e UAT-01 incluem revisão humana ou de ambiente que ainda
não ocorreu. Os métodos listados na matriz são âncoras de rastreabilidade,
não uma contagem de execuções: resultados pertencem ao relatório e aos logs.

## Camadas de evidência

O schema define formato. O parser verifica ambiguidades e limites que JSON
Schema sozinho não resolve ao receber um objeto já carregado. A suíte de
mutantes exige códigos específicos, não considera “qualquer exceção” um sucesso.
O modelo de workflow exige guardas sintéticas; não autentica pessoas.
A acessibilidade matemática de pares opacos não prova a leitura de todos os
componentes. A documentação com links válidos não prova compreensão humana.

Não somar subTest como se fossem casos independentes de unittest. Relatar
métodos executados, falhas, erros e skips, mais o número de cenários do plano
separadamente. PASS significa verificação efetivamente observada naquele
ambiente; PENDENTE, BLOQUEADO, NÃO TESTADO e SKIP não equivalem a aprovação.

## Contrato: casos positivos e adversariais

CON-01 valida fixtures completas por contexto e confirma que defaults não são
injetados. CON-02/03 testam cor, tipo e campo desconhecido; CON-04 testa chaves
duplicadas antes do schema. CON-05 cobre extremos e não finitos. CON-06 cobre
quantidade, repetição e centro, mas não prova adequação estatística da paleta.

CON-07 rejeita versões não suportadas. CON-08 rejeita herança/autorreferência
em vez de tentar resolver ciclos no runtime inexistente. CON-09 cobre conjunto
e caminhos de assets, comparando bytes protegidos. CON-10 distingue grupos e
unidades. CON-11 limita entrada e evita falso positivo com colchetes em strings.
CON-12 recusa aprovação e papéis autodeclarados, além de exigir guardas no modelo.

Toda guarda nova deve receber mutante que a exercite. A fixture é aprovada
**como entrada do contrato**, nunca aprovada como identidade corporativa final.
O pacote deve falhar se houver conjunto vazio/incompleto de exemplos, tabela
derivada divergente, consumidor declarado inexistente ou recurso congelado alterado.

## Regressões de base e preservação

Executar as oito etapas do CI, as três suítes V00 e o publicador visual antes e
depois. A base de composição é `b88a9cc`, já com READMEs e Concierge. Comparar
produto, espelho, Manual, gate e históricos da V00 sem alterar as referências
para obter aprovação. As capturas sintéticas legadas usam o mesmo código da V00.

Os 114 métodos da candidata anterior são reaproveitados; a suíte de integração
adiciona mutantes para referências documentais, registros oficiais de assets e
convivência com os gates existentes. Resultado executado e contagens ficam no
[relatório](RELATORIO_V01.md), não são inferidos da existência dos testes.
A primeira tentativa local com histórico raso foi recusada; o ambiente foi
corrigido, sem enfraquecer a guarda. Não atribuir essa recusa a uma regressão do Hub.

## Acessibilidade e rubrica

O cálculo sRGB testa preto/branco 21:1, cor idêntica 1:1, simetria e ausência de
arredondamento favorável. Pares de uma fixture executiva passam pelo limite
4,5:1 em seus fundos declarados. Isto não certifica todas as 80 definições.
Cores legadas positivas/de alerta sobre branco têm dívida se usadas como texto
comum; registrar a condição, não trocar automaticamente o padrão nem concluir
que todo uso gráfico dessas cores viola o mesmo critério.

A revisão real deve verificar conteúdo não baseado só em cor, foco, teclado,
nome acessível, escala/zoom, títulos/legendas e contexto de uso. Texto grande
só usa 3:1 quando classificado de acordo com o critério pertinente. A rubrica
não usa média para compensar falha crítica de legibilidade ou interpretação.

## Revisão com iniciante: roteiro e formulário

Entregar apenas o README e o guia. Pedir que a pessoa explique onde começa,
qual o efeito de trocar uma cor, como desfaz, como salva e quem publica.
Não explicar os termos durante a tarefa; registrar toda intervenção como achado.
A pessoa deve saber que **a V01 não oferece interface instalada**. O teste de
operação real será repetido quando houver laboratório.

| Registro | Estado desta entrega |
|---|---|
| Participante autorizado | Não designado; não preencher com pessoa fictícia. |
| Documento/versão entregue | Registrar na sessão de teste futura. |
| Data, duração observada e dispositivo | Não medidos. |
| Ajuda verbal | Não observada porque a sessão não ocorreu. |
| Encontrou próxima ação sem ajuda | PENDENTE. |
| Distinguiu salvar/aprovar/publicar | PENDENTE. |
| Problemas e revisão do documento | Registrar após sessão; sem selo de usabilidade agora. |

Meta candidata para achar a próxima ação: 60 segundos, a ratificar; não inferir
cumprimento pelo tamanho do README. Na V12, usar a amostra formativa prevista
no plano, sem alegar representatividade estatística. Revisão do autor e
reexecução própria dos testes não são auditoria independente.

## Critérios de fechamento e de transferência

A candidata local exige schema consistente, fixtures válidas, mutantes que
reprovam, documentos navegáveis, preservação do produto, logs e procedimento
de retorno. O encerramento formal também requer revisão de arquitetura,
aceite do desenho documental e auditoria independente, além da decisão sobre
integração com a main. Esses aceites continuam pendentes; o pedido “Siga para
a V01” autoriza trabalhar, não altera a história da V00.

Para V02: revisar o contrato antes de implementá-lo em runtime; decidir promoção
da fonte candidata para padrão do produto; manter defaults legados explícitos;
aplicar o template vigente aos novos objetos; trazer as decisões de versão,
segurança e persistência sem transformar o oráculo de manutenção em autorização
real. V02 não foi iniciada aqui.

[Voltar à V01](README.md) · [Reprodução](GUIA_MANTENEDOR.md)
