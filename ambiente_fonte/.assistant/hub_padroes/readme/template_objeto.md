# Template — README de objeto do Hub

**Contrato:** `objeto-v0.1-candidata` · **Estado:** proposta da R01-A, ainda não
congelada pelo piloto R02.

Este é o contrato de autoria para `README.md` na pasta de um snippet, script ou
prompt. [O template geral](template.md) seleciona a escala; este arquivo define
as perguntas; [o checklist](checklist_objeto.md) orienta o aceite. Não aplique
este molde a `SKILL.md`, testes, cada arquivo físico ou índices de coleção.

## Como preparar a redação

Leia a implementação inteira, a fachada pública, o notebook e os testes
pertinentes; para prompts, leia o formulário e o bloco colável completos.
Registre no relatório do lote o commit/base e os caminhos consultados. Não
importe módulos nem execute exemplos para descobrir a API por tentativa.

Explique primeiro o conceito e depois o recorte implementado. O nome de uma
biblioteca não comprova que o helper ofereça todas as suas capacidades. Quando
código e explicação divergem, registre o achado: comportamento existente não é
prova de correção científica e não deve ser corrigido nesta migração por efeito
colateral. Um defeito material pode bloquear o aceite do README.

Defina os termos essenciais no primeiro uso e explique por que cada indicação
faz sentido. Use PT-BR respeitoso, sem infantilização, promessas de facilidade
ou jargão não explicado. Preserve os identificadores reais, inclusive os em
português. Exemplos sintéticos não devem conter dados de clientes ou caminhos
corporativos. Quantidade de palavras não aprova nem reprova o texto.

## Estrutura e divisão de responsabilidades

Mantenha o título, a abertura e as quinze seções principais do esqueleto abaixo.
Subtópicos são condicionais: não crie treino para um utilitário visual ou risco
estatístico para um prompt que não calcula estatísticas. Para recurso simples,
um parágrafo breve pode responder a uma seção. Quando o tema não se aplicar,
explique a razão pertinente; não deixe apenas “N/A”.

Evite repetir parágrafos. A seção 3 justifica a escolha; a 4 rejeita escolhas
inadequadas; a 11 explica riscos remanescentes mesmo numa escolha adequada.
A seção 5 explica o mecanismo sem código; a 6 o coloca num cenário; a 9 oferece
a rota operacional. A seção 8 interpreta a saída; a 13 mostra como verificá-la.
A seção 12 compara alternativas, não repete os casos de uso.

A síntese conceitual deve permitir leitura autônoma, sem copiar capítulos do
Manual. O catálogo integrado continua no Manual. O README não substitui as
instruções de preenchimento do prompt nem a demonstração do notebook. Recursos
humanos são consultados conforme a tarefa, não carregados em massa por uma IA.

## Esqueleto para preencher

Copie apenas o conteúdo do bloco. Substitua os placeholders e as orientações
entre colchetes. Os caminhos são marcadores, não links existentes nem API
proposta. Converta-os em links relativos conferidos na pasta de destino. Não
publique as instruções editoriais como se fossem explicações do objeto.

````markdown
# `{{NOME_DO_OBJETO}}` — {{DESCRICAO_HUMANA}}

> **Em uma frase:** {{conceito acessível e problema principal}}.

**Comece por aqui:** {{link conferido para o exemplo}} ·
{{link conferido para o recurso principal}} · {{link para a coleção}}.

**Sobre esta documentação:** contrato `objeto-v0.1-candidata`;
revisão em {{DATA_REAL}}; implementação de referência {{COMMIT_OU_EVIDENCIA}}.
Demonstração: {{EXECUTADA_NESTE_CONTEXTO / EVIDENCIA_HISTORICA / NAO_EXECUTADA}},
com {{ambiente, data, evidência e limitações conhecidas}}.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | {{definição curta}} |
| Para que serve? | {{problema ou decisão}} |
| Use quando... | {{condição principal}} |
| Evite quando... | {{contraindicação principal}} |
| Precisa de... | {{entrada e requisito principal}} |
| Entrega... | {{saída e efeito relevante}} |

## 1. O que é?

[Apresente a ideia em linguagem comum, depois a definição técnica necessária.
Diferencie técnica/biblioteca e recurso do Hub. Explique termos como feature,
score ou wrapper quando realmente aparecerem. Não comece pelo import.]

## 2. Que problema este recurso resolve?

[Formule uma pergunta reconhecível pelo usuário e a decisão apoiada. Mostre o
que o recurso mede, transforma ou orienta, sem prometer a decisão completa.
Diferencie descrição, previsão e explicação causal quando isso for pertinente.]

## 3. Quando faz sentido usar?

[Explique os contextos adequados e os motivos. Relacione características dos
dados/contexto, objetivo e etapa do fluxo. Inclua aplicações distintas quando
existirem; não invente casos para atingir uma quantidade mínima.]

## 4. Quando não usar?

[Apresente pelo menos um contraexemplo real e pertinente. Explique por que a
escolha seria errada, insuficiente ou exigiria outro recurso. Diferencie
premissa não atendida de preferência por alternativa mais simples. Não
transforme heurística em proibição universal.]

## 5. Como funciona, intuitivamente?

[Explique a sequência entrada → lógica principal → saída, sem começar pela
sintaxe. Analogia, esquema ou pequeno exemplo numérico são opcionais e devem
preservar o mecanismo. Para prompt, explique como o contexto orienta a tarefa,
sem sugerir execução determinística ou garantia de obediência da IA.]

## 6. Exemplo de situação

[Apresente situação, contexto disponível, pergunta, justificativa da escolha e
tipo de resultado esperado. Prefira um único cenário coerente. Identifique os
dados fictícios. Valores ilustrativos não são saídas executadas nem benchmarks.
Mantenha o cenário compatível com o que o recurso realmente implementa.]

## 7. O que você precisa antes de usar?

[Explique as entradas reais: tipos, colunas, grão, período, unidades, nulos,
chaves e target somente quando aplicáveis. Para prompt, explique contexto e
aponte ao guia de preenchimento original. Separe requisitos obrigatórios,
dependências opcionais e preparação recomendada.]

[Declare condições de ambiente necessárias e evidência disponível: bibliotecas,
compute, localização da execução, permissões e memória quando materiais.
“Usa pandas” não comprova compatibilidade irrestrita com todo Databricks.
Não presuma recursos, tabelas, versões ou permissões não confirmados.]

## 8. O que este recurso entrega?

[Descreva a saída real e como lê-la. Preserve nomes de chaves/colunas, tipo,
unidades, direção de scores e denominadores. Explique interpretações indevidas
prováveis. Para prompt, diferencie contrato de resposta esperado e resposta
real que ainda precisa ser conferida.]

[Quando útil, use uma tabela curta: saída | significado | como interpretar.]

## 9. Como usar este recurso no Hub?

[Forneça o caminho mínimo correto e link direto para o notebook/recurso
existente. Explique a preparação sem presumir usuário, diretório ou sessão.
Não copie o notebook inteiro, invente assinaturas nem altere implementação.]

[Um trecho executável novo só pode ser chamado de testado se realmente foi
executado nesse contexto. Registre comando, ambiente e evidência no relatório.
Sem execução segura, use a rota explícita para o exemplo e declare a limitação;
não apresente pseudocódigo como solução copiável validada.]

[Para prompt, a rota é preencher e usar o formulário original. Não duplique o
bloco colável nem remova seus limites, instruções ou campos de conferência.]

## 10. Decisões e configurações que mais importam

[Explique escolhas que mudam resultado, interpretação, custo ou efeito.
Separe default implementado, parâmetro fornecido e recomendação. Não transforme
um default em regra de negócio. Cite valores exatos apenas após ler o código.
Se não houver parâmetros, explique a escolha relevante de contexto/entrada,
ou a ausência de configuração, sem inventar opções.]

## 11. Limitações, riscos e armadilhas

[Documente cuidados que permanecem mesmo quando o recurso é apropriado.
Considere limitações conceituais, estatísticas, técnicas e operacionais apenas
quando pertinentes. Declare escrita, coleta, estado de sessão, tracking,
custo ou envio externo quando existirem; não rotule tudo como “somente leitura”.]

[Distinga limitação inerente da técnica, limitação do wrapper e defeito conhecido.
Um teste sintético ou local não homologa produção. Não reproduza uma afirmação
do notebook como verdade universal sem verificar seu alcance.]

## 12. Quais são as alternativas?

[Compare alternativas plausíveis pela decisão que interessa: quando preferir,
o que muda e qual o trade-off. A alternativa pode ser um método simples,
recurso existente ou não executar a operação. Não invente concorrentes para
constantes/estilos nem imponha um ranking universal. Verifique os links.]

## 13. Como saber se o resultado faz sentido?

[Indique verificações concretas proporcionais ao risco e à natureza do objeto:
um teste de sanidade, referência conhecida, invariância, diagnóstico de entrada
ou revisão de conteúdo, por exemplo. Explique o resultado esperado da checagem
e o que fazer se ela falhar. Código sem exceção não equivale a análise correta;
resposta plausível de IA não equivale a evidência.]

## 14. Arquivos relacionados e próximos passos

[Relacione recurso principal, exemplo, fachada quando existir, coleção e
recursos úteis reais. Use links relativos conferidos, com uma frase sobre o
papel de cada destino. Não crie links para READMEs ainda planejados; use a
pasta/implementação existente até a entrega ou registre a pendência no lote.]

[Para o Manual, use a rota disponível no produto. Não pressuponha acesso ao
GitHub privado no workspace. Links que funcionam no Git precisam de conferência
no destino de publicação; essa conferência não deve ser declarada sem execução.]

## 15. Referências

[Associe afirmações técnicas materiais às fontes pertinentes, por link junto ao
trecho ou identificador resolvido aqui. Priorize documentação oficial, artigo
original e código de referência. Cite fonte do comportamento da plataforma
quando fizer essa afirmação. Não inclua bibliografia decorativa.]

[Para cada fonte, informe o que ela sustenta e, quando relevante, versão/data
consultada. Diferencie referência histórica de verificação atual. Para um
utilitário puramente interno, código e convenção do Hub podem ser suficientes.
Sem evidência de uma afirmação material, registre a lacuna, não invente fonte.]
````

## Estado e manutenção

O bloco de metadados deve ser curto; autoria, revisão técnica, revisão didática,
execuções e aceite completo ficam no relatório de sprint. Atualize o README
quando o contrato do objeto mudar. Uma data de revisão não comprova teste.

A R01-A não entrega exemplares preenchidos, novos validadores, README dos
objetos operacionais ou publicação. O status editorial só muda para aceito com
as evidências do [checklist](checklist_objeto.md); um arquivo presente não
representa cobertura aceita. Alterações deste contrato são registradas antes
de autorizar o lote seguinte. Não congele a versão 1.0 antes do piloto.
