# Guia de leitura do Manual do Usuário

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MU-indice.md#sumario-mu) · [Livro completo](../../MANUAL_DO_USUARIO.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mu-mod-guia-leitura-usuario"></a>
<a id="mu-mod-guia-leitura-usuario-h-guia-de-leitura-do-manual-do-usuário"></a>
## Guia de leitura do Manual do Usuário


<a id="mu-mod-guia-leitura-usuario-h-comece-pela-decisão-que-precisa-tomar"></a>
### Comece pela decisão que precisa tomar

Este manual pode acompanhar uma primeira experiência completa ou uma consulta
durante o trabalho. Para escolher um ponto de entrada, transforme sua necessidade
numa frase que termine com uma decisão: conhecer uma base para decidir se ela
serve ao estudo; comparar fontes para decidir se o cruzamento é confiável; montar
um visual para comunicar uma conclusão. Essa pequena preparação ajuda a escolher
o capítulo e a reconhecer quando a tarefa terminou. “Quero usar Python” descreve
uma ferramenta; “quero descobrir quais campos têm ausência e como isso afeta a
análise” descreve uma pergunta que o livro consegue encaminhar.

Se ainda não conhece o ambiente, percorra os capítulos iniciais na ordem. Eles
ensinam a localizar recursos, separar arquivos de dados e preparar o primeiro
uso. Nas consultas seguintes, entre pela pergunta do sumário. Você pode ler uma
receita específica sem repetir o livro inteiro, desde que confira os seus
pré-requisitos. Uma indicação de leitura anterior significa que aquela decisão
ou preparação será usada no procedimento; não significa executar novamente
todas as análises anteriores numa mesma sessão.

Ao abrir um capítulo, procure primeiro a pergunta, a rota indicada e o resultado
esperado. Depois leia a explicação dos termos necessários e a receita completa.
Reserve os detalhes de exceção para a etapa em que eles se aplicam, mas leia os
efeitos antes de executar código: um exemplo pode criar dados de demonstração,
instalar uma dependência ou iniciar um registro de execução. A explicação desses
efeitos faz parte da receita. O fato de um comando aparecer num manual não
define, sozinho, o destino adequado para o seu ambiente.

<a id="mu-mod-guia-leitura-usuario-h-escolha-quanto-do-procedimento-precisa-usar"></a>
### Escolha quanto do procedimento precisa usar

Algumas perguntas cabem numa função auxiliar isolada. Outras exigem um roteiro
com escolhas de população, tempo, qualidade e forma de entrega. Os capítulos
mostram essas duas possibilidades. Quando você já conhece a pergunta, os dados e
a interface de um recurso, siga a receita de uso isolado. Quando precisa de
ajuda para organizar decisões e produzir uma análise revisável, siga a receita
da skill pertinente. Uma skill é um conjunto de orientações e recursos para um
tipo de trabalho; sua seleção não demonstra que os dados já foram analisados.

Descreva também o tipo de ajuda desejado. Pedir uma explicação, um plano, código
para revisar ou execução produz expectativas diferentes. Se quer aprender sem
acionar cálculo, diga isso no pedido. Se quer executar, informe os recursos
autorizados e os limites conhecidos. Ao conferir a resposta, veja se ela ficou
no modo solicitado e se apresenta as evidências correspondentes. Um plano pode
ser uma boa entrega de planejamento; uma célula escrita pode ser uma boa entrega
de código. Para reconhecer uma análise executada, você precisa dos resultados e
das verificações que pertencem àquela rota.

Um briefing pronto ajuda a organizar o pedido, mas ainda precisa dos seus
valores. Leia cada campo antes de substituir um marcador. Uma tabela identificada
por catálogo, schema e nome é diferente de uma view temporária da sessão; uma
data de ocorrência é diferente da data em que o dado ficou disponível. Se não
souber uma informação necessária, registre a pendência e explique quem pode
resolvê-la. Preencher um campo com um valor inventado cria um pedido aparentemente
completo e uma análise que responde a outra pergunta.

<a id="mu-mod-guia-leitura-usuario-h-leia-exemplos-como-exercícios-verificáveis"></a>
### Leia exemplos como exercícios verificáveis

Os exemplos pequenos permitem acompanhar o raciocínio antes de usar uma base
grande. Observe os valores de entrada, a chamada e a interpretação da saída.
Faça a conta simples quando houver números: qual é o denominador de uma taxa,
quantas entidades foram incluídas, qual data limita o histórico e em qual escala
está o percentual? Essa leitura transforma o exemplo numa ferramenta de
aprendizado. Copiar apenas a chamada elimina justamente as decisões que tornam
o resultado compreensível.

Considere uma tabela de três decisões que você pretende cruzar com outra fonte.
Uma decisão encontra duas versões, outra não encontra correspondência e a
terceira não tem chave. O total depois de um cruzamento pode parecer próximo do
total original, mas ainda existe multiplicação e perda de fatos. O exemplo de
joins ensina a examinar essas causas separadamente. Ao transportar a receita
para o trabalho, preserve a pergunta sobre a unidade de cada linha. Uma tabela
que ficou maior não demonstra, por si, que você obteve mais informação válida.

O mesmo cuidado vale para gráficos. Veja primeiro o que foi calculado e depois
como foi apresentado. Alterar cor, título ou tema não deve mudar amostra, unidade
ou denominador. Se uma figura parece comunicar outra conclusão após uma mudança
visual, confira escala, seleção de dados, legenda e destaque. Os capítulos
visuais apresentam uma sequência de planejamento, construção, comparação e
revisão; você pode usar essa sequência mesmo quando escolhe manter a aparência
existente.

Resultados ilustrativos explicam o comportamento esperado sob condições
declaradas. Resultados observados registram uma execução identificável. Mantenha
essa diferença ao escrever suas próprias notas. Se executou apenas o exemplo
local, descreva esse alcance. Se adaptou o código e ainda não rodou, registre a
adaptação como proposta. Outra pessoa precisa conseguir reconhecer o que pode
reutilizar como evidência e o que ainda depende de verificação.

<a id="mu-mod-guia-leitura-usuario-h-volte-à-etapa-em-que-apareceu-a-dificuldade"></a>
### Volte à etapa em que apareceu a dificuldade

Quando o procedimento falhar, localize a etapa antes de trocar de recurso.
Arquivo não encontrado pede conferir caminho e cópia instalada. Importação que
falha pede conferir a raiz da biblioteca e a dependência pertinente. Argumento
recusado pede conferir a assinatura e o valor fornecido. Uma saída inesperada
pede revisar população, filtros, unidades e hipóteses. Essas situações têm
recuperações diferentes; o quadro de erros de cada capítulo ajuda a escolher a
próxima ação sem repetir trabalho desnecessário.

Se estiver usando uma skill com mecanismo obrigatório de verificação, leia o
estado retornado e a recuperação indicada. Um bloqueio identifica uma condição
que precisa ser resolvida na mesma rota. A ausência de finalização significa que
o trabalho ainda não recebeu autorização de conclusão por aquele mecanismo.
Uma mensagem bem escrita ou um gráfico plausível não substitui essa etapa. Em
contrapartida, uma função de diagnóstico pode apenas devolver alertas para você
interpretar. O manual identifica o alcance de cada recurso para evitar tratar
todo aviso como bloqueio ou todo resultado como aprovação.

Você também pode encontrar um recurso descrito como candidato ou uma superfície
que depende de instalação e autorização. Leia a condição antes de tentar o
procedimento. Use as alternativas documentadas que atendam à sua tarefa e
registre o limite encontrado. Se uma funcionalidade ainda não está disponível,
o livro pode ensinar a preparar uma proposta ou interpretar seus arquivos; isso
não torna aquela funcionalidade operacional no seu workspace.

<a id="mu-mod-guia-leitura-usuario-h-prepare-uma-entrega-que-outra-pessoa-consiga-continuar"></a>
### Prepare uma entrega que outra pessoa consiga continuar

Ao terminar, faça uma leitura breve como se estivesse recebendo seu próprio
trabalho. A pergunta foi respondida? As entradas e os recortes estão claros? Os
números têm unidade e denominador? A pessoa consegue distinguir dados completos,
amostra, ausência e resultado negativo? Os limites que podem mudar a decisão
ficaram próximos da conclusão? Essa revisão é útil para uma tabela pequena,
um notebook longo e uma entrega visual.

Registre também a próxima ação. Ela pode ser usar o resultado, corrigir uma
entrada, resolver uma decisão de domínio ou pedir revisão especializada. Quando
houver escrita ou compartilhamento, confira destino, modo e alcance antes da
ação. Para consultas futuras, guarde a identificação dos recursos e a versão da
entrega. O objetivo é permitir que alguém continue o trabalho sem reconstruir
intenções a partir de células soltas ou de uma conversa esquecida.

O Manual Técnico V2 serve como complemento quando você precisar entender a
construção de um recurso, seu contrato e suas limitações internas. Continue pelo
Manual do Usuário enquanto a pergunta principal for como realizar a tarefa. As
pontes entre os livros permitem aprofundar um ponto específico sem transformar
toda consulta prática numa investigação da arquitetura.

<!-- editorial:exclude:start -->
<a id="mu-mod-guia-leitura-usuario-h-rotas-de-consulta"></a>
### Rotas de consulta

| Necessidade | Capítulos |
|---|---|
| Conhecer, preparar acesso e escolher recursos | [MU01](MU-parte-i.md#mu01), [MU02](MU-parte-i.md#mu02), [MU03](MU-parte-i.md#mu03) |
| Usar uma skill ou preencher briefing | [MU04](MU-parte-ii.md#mu04), [MU05](MU-parte-ii.md#mu05) |
| Usar uma função ou um script isoladamente | [MU06](MU-parte-ii.md#mu06), [MU07](MU-parte-ii.md#mu07) |
| Conhecer dados e cruzar fontes | [MU08](MU-parte-iii.md#mu08), [MU09](MU-parte-iii.md#mu09) |
| Preparar features, estudos e modelos | [MU10](MU-parte-iii.md#mu10), [MU11](MU-parte-iii.md#mu11), [MU12](MU-parte-iii.md#mu12) |
| Trabalhar com micromodelos | [MU13](MU-parte-iv.md#mu13) |
| Planejar e construir uma entrega visual | [MU14](MU-parte-v.md#mu14), [MU15](MU-parte-v.md#mu15), [MU16](MU-parte-v.md#mu16), [MU17](MU-parte-v.md#mu17) |
| Criar, documentar e compartilhar | [MU18](MU-parte-vi.md#mu18), [MU19](MU-parte-vi.md#mu19) |
| Resolver problemas e percorrer o fluxo completo | [MU20](MU-parte-vi.md#mu20) |

[Índice completo](MU-indice.md#sumario-mu) · [Referência técnica](MT-indice.md#sumario-mt).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [Outro manual](MT-indice.md#sumario-mt)
<!-- editorial:exclude:end -->
