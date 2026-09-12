# Checklist — revisão de README de objeto

**Aplica-se a:** [template_objeto.md](template_objeto.md), contrato
`objeto-v0.1-candidata`. **Estado:** checklist de revisão manual da R01-A;
não descreve um validador já implementado.

O critério de aprovação é a qualidade verificável da explicação, não número de
palavras, presença de títulos ou ausência de exceção no código. Registre cada
critério como ATENDIDO, PENDENTE, BLOQUEADO ou NÃO APLICÁVEL COM JUSTIFICATIVA,
com caminho/trecho/evidência. Não some uma nota para compensar erro material.

## 1. Escopo, origem e preservação

- [ ] Objeto identificado por pasta; implementação/formulário, fachada, exemplo
  e testes pertinentes lidos; commit/base e versão do contrato registrados.
- [ ] Leiautes aprovados, APIs, defaults, código executável, texto colável de
  prompts, ADRs aceitos e trabalhos de outros autores preservados.
- [ ] Conteúdo geral da técnica está separado das capacidades do helper real.
- [ ] Código, docstring e notebook foram confrontados; divergências materiais
  não foram escondidas nem consertadas como efeito colateral documental.
- [ ] Não há dados pessoais, identificadores corporativos, segredos ou caminhos
  reais indevidos; exemplos fictícios estão identificados.

## 2. Compreensão e adequação

- [ ] A definição pode ser compreendida sem conhecer o nome técnico; os termos
  essenciais são explicados na primeira ocorrência, sem infantilização.
- [ ] A pergunta apoiada e o resultado útil são concretos, não “otimizar análises”.
- [ ] Contextos positivos têm justificativa; existe contraexemplo pertinente com
  explicação do porquê e alternativa/ação adequada quando couber.
- [ ] O mecanismo, o cenário e a orientação operacional não repetem o mesmo texto.
- [ ] O cenário acompanha uma sequência coerente: problema, entrada, escolha,
  tipo de saída e interpretação. Ilustração não é apresentada como execução.
- [ ] Um recurso pequeno não recebeu texto de enchimento; um recurso complexo
  não perdeu premissas para cumprir limite artificial de palavras.

## 3. Contrato técnico e uso seguro

- [ ] Tipos, parâmetros, nomes públicos, defaults, retornos, chaves, unidades e
  direções de scores citados correspondem ao código/formulário lido.
- [ ] Entradas obrigatórias, dependências opcionais e recomendações estão separadas.
- [ ] Grão, chaves, período, nulos e target aparecem somente quando pertinentes,
  com definição suficiente para o caso de uso e sem schema inventado.
- [ ] Efeitos materiais foram inspecionados: escrita, coleta, sessão, tracking,
  custo e serviços externos. “Somente leitura” tem fundamento, não é pressuposto.
- [ ] Não há promessa de autoexecução, autodiscovery, deploy, paralelismo ou
  compatibilidade de plataforma que não esteja sustentada.
- [ ] Uso mínimo é coerente com a API e com preparação explícita do ambiente.
  Trecho novo não executado não está rotulado como testado; a rota ao exemplo
  existente é válida e a limitação de execução está declarada.
- [ ] Para prompts, formulário e controles originais continuam no arquivo do
  prompt; resposta esperada não é apresentada como resultado garantido.
- [ ] Limitações remanescentes e pelo menos uma verificação concreta do resultado
  são explicadas. A orientação diz o que observar e como tratar uma falha.

## 4. Fontes, estrutura e navegação

- [ ] Quinze títulos principais estão presentes e na ordem do template, com
  conteúdo específico. Subtópicos condicionais não viraram “N/A” decorativo.
- [ ] A abertura dá acesso direto ao exemplo e ao recurso para quem já conhece
  o conceito; a visão rápida não substitui explicações importantes.
- [ ] Fontes primárias sustentam afirmações externas materiais; cada referência
  tem finalidade identificável. Afirmações internas têm referência ao código.
- [ ] Evidência histórica, teste nesta rodada, ilustração e condição desconhecida
  estão separados. Revisão de texto não é homologação de runtime.
- [ ] Links locais, caixa dos nomes e âncoras foram conferidos. Verificação apenas
  no Git não é registrada como teste no workspace. Não há link para arquivo futuro.
- [ ] O texto não duplica catálogo/glossário ou capítulos do Manual. Rotas da
  coleção foram conferidas e pendências de navegação estão no relatório.

## 5. Regras de bloqueio

Bloqueiam o aceite: API inventada; saída ilustrativa vendida como executada;
capacidade inexistente; omissão de efeito material; instrução de uso insegura;
fonte que não sustenta afirmação relevante; dados sensíveis; e divergência
conceitual que leve o leitor a uma decisão errada. Boa linguagem não compensa
nenhum desses problemas.

Ausência de teste em um runtime indisponível não deve ser disfarçada. Pode
haver aceite documental delimitado quando a rota de uso está verificável, a
limitação foi explicitada e o responsável aceita esse alcance. Não declarar
aceite operacional nem aprovação global quando uma dependência material ficou
sem conferência. Critério essencial pendente impede o aceite documental.

## 6. Registro de fechamento do lote

Use o relatório/checkpoint da sprint para registrar:

| Campo | Conteúdo obrigatório |
|---|---|
| Identificação | sprint/lote, base Git, versão do contrato, objetos e caminhos |
| Autoria e revisão | autores reais, revisão técnica e didática; indicar autorrevisão |
| Alterações | READMEs novos, documentos atualizados, ferramentas e derivados separados |
| Evidências | verificações realizadas, comandos/ambientes quando houve execução, saídas e alcance |
| Pendências | falhas preexistentes, regressões, não executados e critérios bloqueados |
| Aceite | escrito, revisado e aceito como estados distintos, com responsável e data reais |
| Continuidade | próximo lote autorizado e ponto de parada; nenhuma execução presumida |

Uma segunda leitura pela mesma IA não é auditoria independente. Não marque
aceite do usuário antes de recebê-lo. Lotes paralelos só podem ter pastas
exclusivas por redator e um integrador para documentos compartilhados.

## 7. O que poderá ser automatizado

Na R01-D, propor controles para títulos/ordem, presença de arquivos, links,
placeholders remanescentes, cobertura progressiva e testes de regressão.
Essa lista é backlog, não capacidade atual. Os testes do validador devem
incluir casos negativos e evitar tratar títulos ou tamanho como prova de
qualidade. Julgamento conceitual, adequação e acolhimento continuam exigindo
revisão. O piloto R02 pode calibrar o contrato antes da versão estável.
