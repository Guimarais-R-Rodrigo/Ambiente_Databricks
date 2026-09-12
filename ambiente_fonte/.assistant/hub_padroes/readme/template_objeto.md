# Template — README de objeto

<!-- readme-objeto: 0.1.0-candidata -->

Versão candidata da R01. O piloto R02 e o aceite humano precedem o congelamento
em 1.0. Este arquivo é o dono das seções: regras, skill e validador o referenciam,
sem manter outro esqueleto concorrente. É a escala **Objeto** do
[template geral](template.md), não um sétimo tipo do Hub.

## Como aplicar o molde

Crie `README.md` na pasta de cada snippet, script ou prompt. Não aplique este
molde a `__init__.py`, testes, índices de categoria nem `SKILL.md`. Os três
[exemplares](#exemplares) abaixo ensinam a forma; não são bibliotecas operacionais.

A abertura do documento final contém: título com nome público e descrição
humana; frase de identidade; o marcador de versão acima; aviso de exemplar,
quando for esse o caso; `## Visão rápida`; e acesso direto ao exemplo e à
implementação ou briefing. A tabela rápida responde o que é, para que serve,
quando usar/evitar, o que exige e o que entrega. Não transforme a tabela em
seis parágrafos longos. Quem já conhece o assunto encontra o notebook aqui.

Depois da abertura, mantenha **exatamente os quinze títulos numerados abaixo**,
na mesma ordem. Subtítulos de nível três são livres quando ajudam; não imponha
vocabulário de modelos a um recurso de apresentação. As instruções de autoria
deste molde não são conteúdo a copiar para o README preenchido.

Explique em PT-BR, preservando todos os identificadores existentes, inclusive
os que já são portugueses. Apresente a intuição antes da terminologia e defina
o termo no primeiro uso. Escreva recomendações acompanhadas do motivo. Evite
“basta”, “óbvio” e “trivial” para uma etapa que pode ser nova ao leitor.

Não há quota de palavras, número mínimo de alternativas ou obrigação de usar
uma analogia. O critério é responder à pergunta da seção sem repetição. Recursos
pequenos podem ter parágrafos curtos; conceitos difíceis precisam de espaço.
Não preencha seções com “N/A”: explique a limitação realmente pertinente.

## 1. O que é?

Explique o conceito com uma definição compreensível sem conhecimento prévio.
Depois delimite a implementação desta pasta: um wrapper não implementa todas
as capacidades da biblioteca subjacente. Para uma constante ou componente
visual, explique seu papel sem inventar teoria estatística.

## 2. Que problema este recurso resolve?

Formule uma pergunta concreta da pessoa que usaria o recurso e a decisão que
ela pretende apoiar. Diferencie calcular um indicador, diagnosticar uma base,
produzir uma visualização e orientar uma IA. Não apresente uma sugestão de
negócio como decisão automática tomada pelo helper.

## 3. Quando faz sentido usar?

Descreva contextos positivos realmente distintos e por que são adequados.
Considere características dos dados, objetivo e etapa do trabalho, sem repetir
o mesmo caso com nomes de departamentos diferentes. Informe quais condições
precisam valer para a recomendação ser útil.

## 4. Quando não usar?

Explique quando rejeitar a escolha **antes** de executar: problema diferente,
premissa essencial ausente ou alternativa claramente mais simples. Inclua um
contraexemplo específico e explique por que o código poderia rodar, mas
responder à pergunta errada. Evite proibições universais sem fundamento.

## 5. Como funciona, intuitivamente?

Conte a transformação: o que entra, quais etapas importam, a lógica central e
o que sai. Uma analogia é opcional e precisa ter seus limites. Fórmula ou
exemplo numérico só entra quando ensina algo que a prosa não torna claro.
Não substitua a explicação por uma lista de funções internas.

## 6. Exemplo de situação

Use um cenário sintético coerente: situação, informação disponível, pergunta,
motivo da escolha e tipo de resposta esperada. Diferencie um cálculo didático
que você fez de uma saída efetivamente obtida pelo helper. Não invente logs,
resultados de treinamento nem métricas de desempenho.

## 7. O que você precisa antes de usar?

Explique as entradas humanas e técnicas: dados/contexto, unidade de cada linha
(grão), chaves, período, colunas, tipos, unidades, permissões e dependências
realmente exigidas. Target e separação treino/teste só aparecem quando cabem.
Diga também o que o código **não verifica**, mas o leitor precisa conferir.
Não trate uma anotação de tipo como validação executada.

## 8. O que este recurso entrega?

Descreva o retorno real: estrutura, campos relevantes, unidades, direção dos
scores, arredondamento e significado. Para um prompt, distinga entrega
solicitada de resposta garantida. Explique uma interpretação que a saída não
sustenta. Tabelas ajudam a consultar campos, não substituem a interpretação.

## 9. Como usar este recurso no Hub?

Ofereça a rota mínima correta e um link relativo real para a demonstração.
Não replique o notebook. Um exemplo mínimo de código é opcional: a rota
explícita para o exemplo existente satisfaz esta seção quando é mais segura.
Se incluir código, confira a fachada pública, a assinatura e as dependências;
registre o que foi ou não executado. Não use `%run` nem copie a implementação.

**Separe efeitos do helper e efeitos do exemplo.** Um helper somente de leitura
pode ter notebook que cria ou sobrescreve tabelas sintéticas. Avise antes do
link de execução, com destino e modo quando conhecidos. Não instrua o leitor
a executar o notebook inteiro sem conferir os efeitos.

## 10. Decisões e configurações que mais importam

Explique escolhas que mudam resultado, interpretação, custo ou risco. Preserve
nomes e defaults reais. Um limiar local não vira lei estatística nem regra da
plataforma. Parâmetro declarado mas não utilizado deve ser identificado, não
explicado como se controlasse algo. Em prompts, explique os placeholders
relevantes sem duplicar seu formulário completo.

## 11. Limitações, riscos e armadilhas

Trate dos cuidados que permanecem **mesmo quando a escolha é adequada**.
Inclua limitações de método, implementação, volume, memória e efeitos de sessão
quando pertinentes. Não repita a seção 4. Uma divergência entre docstring,
notebook e código deve ser sinalizada e registrada; não mude comportamento
para fazer a documentação parecer consistente.

## 12. Quais são as alternativas?

Compare opções plausíveis por contexto, sem declarar vencedor universal.
Prefira recurso existente do Hub quando ele realmente atender à necessidade.
Uma referência à implementação ou pasta existente é melhor que um link para
README futuro. Não invente alternativas para atingir um número de linhas.

## 13. Como saber se o resultado faz sentido?

Dê verificações concretas que o leitor consiga executar: recontagem, unidade,
sinal, conjunto de referência, estabilidade, caso conhecido ou revisão humana.
Diferencie execução sem erro, correção de cálculo e adequação da decisão.
Para componentes visuais, conferência de formatação e legibilidade pode ser
mais importante que qualquer métrica estatística.

## 14. Arquivos relacionados e próximos passos

Ligue o arquivo principal e o `exemplo_<nome>.py`, explicando seus papéis.
Inclua `__init__.py` para snippets/scripts e o briefing para prompts. Aponte
para a coleção ou padrão pertinente. Não crie rotas concorrentes ao catálogo
integrado do Manual nem dependa de ferramenta de manutenção no workspace.

## 15. Referências

Sustente afirmações de comportamento com a implementação e a fachada locais;
use o notebook como evidência delimitada, não como prova universal. Para teoria,
consulte documentação primária, literatura pertinente ou documentação oficial.
Para plataforma, identifique serviço, ambiente/versão e data consultada.
Referência histórica por commit e instrução vigente têm funções diferentes.

Não exija fonte externa para a simples descrição de uma constante local. Não
use bibliografia decorativa. Registre o estado desta revisão: leitura estática,
testes locais, teste de runtime e revisão independente são coisas diferentes.
Não transfira um “executado” antigo para esta sprint sem execução nova.

## Exemplares

- [Snippet: taxa de resposta](../snippet/taxa_resposta_campanha/README.md).
- [Script: checagem de base](../script/checar_base_campanha/README.md).
- [Prompt: análise de campanha](../prompt/analisar_campanha/README.md).

Antes de fechar, use o [checklist editorial](checklist_objeto.md). O checklist
[geral de objeto novo](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md)
continua sendo a entrada do processo; ele remete ao editorial sem duplicá-lo.
