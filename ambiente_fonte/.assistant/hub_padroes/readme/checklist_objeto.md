# Revisão de README de objeto

Este é o checklist **editorial**, subordinado ao
[contrato de objeto](template_objeto.md). O processo de criação permanece no
[checklist geral](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
Uma aprovação automática confirma estrutura, não compreensão nem verdade.

## 1. Base verificável da revisão

Registre caminho do objeto, commit ou hashes dos arquivos lidos, versão do
contrato, autor e revisor efetivos. Leia implementação, fachada, notebook e
referências pertinentes. Quando só existir uma IA, registre revisão do próprio
autor (`A0_light`); não declare auditoria independente por alternar papéis.

Separe os estados: rascunho; estrutura conferida; revisão técnica; revisão
didática; aceite humano. Nenhum deles implica teste Databricks ou publicação.
Um objeto fora do escopo de execução permanece “não executado nesta rodada”.

## 2. Conferência mecânica

- [ ] `README.md` existe na pasta correta e declara a versão do contrato.
- [ ] As quinze seções estão presentes, na ordem, com conteúdo não vazio.
- [ ] A visão rápida oferece caminho para o exemplo e arquivo principal.
- [ ] Links relativos, inclusive a fachada aplicável, apontam para arquivos reais.
- [ ] Não restaram instruções de preenchimento ou marcadores editoriais.
- [ ] O notebook referencia o README sem alteração do código executável.
- [ ] Todo snippet, script ou prompt operacional possui README; não há dispensa automática.

Validação automática pode conferir cabeçalhos e ligações locais. API, significado e fontes exigem leitura; um check estrutural não executa o código do README nem certifica sua explicação.

## 3. Rubrica técnica e didática

| Dimensão | Pergunta de revisão | Evidência exigida |
|---|---|---|
| Conceito | Uma pessoa nova consegue explicar o recurso com palavras próprias? | Definição, intuição e termos introduzidos. |
| Escolha | Consegue reconhecer um uso apropriado e rejeitar outro? | Contexto positivo e contraexemplo, com motivos. |
| Fidelidade | O texto descreve este objeto, não uma versão imaginada da biblioteca? | Parâmetros, entradas, saídas e efeitos confrontados com código. |
| Interpretação | Entende o resultado e uma conclusão que ele não permite? | Unidade, direção, premissa e limite de inferência. |
| Uso seguro | Encontra o exemplo e percebe suas pré-condições? | Dependências e efeitos do helper e notebook separados. |
| Validação | Sabe o que conferir depois de executar? | Verificações específicas, não “valide os dados”. |
| Procedência | Distingue evidência, ilustração, hipótese e política? | Fontes relevantes e estado de execução explícito. |
| Clareza | O texto acolhe sem infantilizar ou intimidar? | Motivos, exemplos coerentes, ausência de jargão não explicado. |

Classifique cada dimensão como **satisfatória**, **ajuste necessário** ou
**bloqueadora**, descrevendo a evidência. Não calcule média que esconda um erro
material. Não há quota de palavras nem obrigação de inventar três alternativas.

## 4. Bloqueadores de aceite

API inexistente; capacidade ausente apresentada como implementada; inferência
causal sem fundamento; saída ilustrativa rotulada como execução; omissão de
escrita/sobrescrita material; orientação de instalação ou runtime não verificada;
contradição de código que impeça instrução de uso segura; fonte sem suporte.

Esses problemas bloqueiam o documento afetado até correção ou delimitação
explícita do escopo. Defeito do helper vai para registro de achados e não é
corrigido silenciosamente como edição documental. Um exemplar pode continuar
útil para estudar a forma e ser explicitamente inadequado para produção.

## 5. Resultado da revisão

Registre versão, documentos conferidos, achados, evidências, limites e autor/revisor reais. Alterar o contrato editorial exige avaliação de impacto; não aplicar mudança silenciosa a guias existentes.
