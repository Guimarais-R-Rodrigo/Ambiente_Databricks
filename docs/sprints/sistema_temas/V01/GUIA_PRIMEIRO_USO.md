# Primeiro uso: como você escolherá a aparência do Hub

## Antes de começar: o que está disponível hoje

Este documento acompanha a **V01, que ainda não instala o painel**. Você pode
ler e avaliar o fluxo sem abrir o Databricks. Não procure um botão novo no Hub,
não copie os arquivos de `tools/` para o workspace e não execute todos os
notebooks para tentar ativar cores. Continue usando sua rotina atual.

O Hub reúne recursos de apoio ao trabalho com dados e modelos. Um **tema** é um
conjunto de escolhas de aparência: cores, letras, espaços e variantes de
componentes. Ele não altera os números ou a regra do modelo. Uma **prévia** é
uma experiência isolada. Uma **proposta** é algo salvo para avaliação. Uma
**publicação** torna uma versão aprovada disponível em um destino definido.

A leitura abaixo descreve a experiência a entregar na V05. A equipe deverá
complementá-la com o caminho real de entrada, capturas e permissões do ambiente
homologado. Isso evita instruções de clique para telas que ainda não existem.

## Exemplo: sua chefia pediu uma apresentação mais sóbria

Você deverá abrir a entrada “Aparência do Hub” indicada no README operacional.
O painel deve mostrar “Prévia pessoal”, a versão carregada e o contexto. Se
não houver acesso ou o link estiver ausente, use o canal de suporte autorizado
no seu ambiente. Não procure permissões administrativas por conta própria.

Escolha o contexto da entrega. Para gráficos dentro de notebook, escolha
notebook; para imagens de documentação, escolha README; apresentação é outro
contexto. Uma mudança pode funcionar em um e exigir regenerar imagens no outro.
O painel explicará essa diferença antes de salvar.

Escolha “Atual preservado” para começar do que conhece, ou um preset aprovado
adequado à apresentação. Faça uma alteração pequena, como o tom do título.
Use o seletor visual ou informe o código fornecido pela equipe de comunicação,
por exemplo `#005CA9`. O campo deve exibir amostra e orientação sobre erros.

Veja a comparação entre atual e proposta. Leia um título longo, uma legenda,
um número negativo e o texto menor. Confira se a alteração ajuda a leitura,
se as categorias continuam identificáveis e se os números são os mesmos.
Nada disso deverá consultar bases corporativas ou treinar um modelo.

Se não gostar, use “Desfazer”. Para abandonar as mudanças e recomeçar, use
“Restaurar ponto de partida”; o painel deverá proteger mudanças não salvas.
Fechar a sessão sem salvar pode perder o rascunho: a prévia não é um arquivo.

Quando estiver satisfeito, use “Salvar/exportar proposta”. Confira o nome,
a revisão e o destino informado na confirmação. Ausência de confirmação
significa que você ainda não deve considerar o arquivo salvo. Salvar não
muda o padrão da equipe.

Para pedir revisão, submeta a versão salva ao destino adequado. O responsável
avaliará a proposta. **Aprovação não é instalação**: uma pessoa autorizada a
publicar fará uma ação separada. O painel deverá dizer onde a versão foi
adotada e onde ainda não foi. Não se presume que todo notebook, imagem antiga,
App e dashboard mudarão ao mesmo tempo.

## Como escolher sem conhecer códigos de cor

Comece de um preset e altere poucas coisas por vez. Priorize texto legível em
seu fundo. Não use somente verde/vermelho para transmitir o significado:
legendas, ícones ou rótulos devem ajudar. Texto pequeno sobre cor clara pode
ser difícil de ler mesmo quando fica bonito no seletor.

Há diferenças entre a cor da marca e as cores dos dados. “Aumentou” não quer
dizer sempre “melhorou”. A regra analítica não pode ser alterada pelo painel.
Uma ilustração ou assinatura já aprovada pode exigir uma nova variante em vez
de uma troca instantânea de cor.

## Dúvidas e recuperação

**Não encontro o painel:** na V01 ele realmente não existe. Na versão operacional,
confira primeiro se a versão instalada inclui o laboratório e se seu acesso foi
liberado. Você não precisa alterar código para corrigir essa dúvida.

**O código de cor foi recusado:** confira `#` seguido de seis caracteres entre
0–9 e A–F. Não cole instruções CSS. A prévia anterior deverá continuar válida.

**O gráfico mudou, mas a imagem do README não:** a imagem é um arquivo já
gerado. Consulte o impacto da proposta; a equipe precisará regenerá-la ou
selecionar uma variante aprovada. Não sobrescreva o arquivo manualmente.

**Salvei e nada mudou para outra pessoa:** isso é esperado; salvar proposta não
é publicar. Confira o estado e o destino antes de solicitar suporte.

**Não posso publicar:** o papel pode não permitir. Encaminhe a proposta pelo
fluxo de revisão. Não tente mudar `approved` ou `role` no arquivo: isso não
concede autorização e o contrato recusa esses campos.

**Perdi a sessão:** abra a última proposta que tenha confirmação de gravação.
O rascunho volátil pode não existir mais. O guia definitivo deverá indicar
onde procurar arquivos e por quanto tempo o destino os mantém.

**A versão publicada precisa voltar:** peça o retorno controlado ao responsável.
Isso exige revisão e registro; não apague imagens ou configurações sozinho.

## O que informar ao suporte

Informe objetivo, versão exibida, nome/revisão da proposta, contexto, ação
realizada e código de erro. Captura deve excluir dados de clientes, nomes
corporativos restritos, tokens e segredos. Não envie uma tabela real apenas
para demonstrar problema de cor. Use o exemplo sintético do laboratório.

## Revisão deste guia

Uma pessoa que nunca entrou no Hub deverá ler este documento e explicar, sem
ajuda verbal, onde começa, como experimenta, como desfaz e por que salvar não
altera o padrão compartilhado. Essa avaliação humana está **PENDENTE**; nenhum
participante ou tempo de conclusão foi inventado nesta entrega.

[Voltar à V01](README.md) · [Operação atual: Manual Técnico](../../../../MANUAL_TECNICO.md)
