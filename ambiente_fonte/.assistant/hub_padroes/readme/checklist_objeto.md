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
- [ ] O objeto foi retirado da dispensa temporária quando ganhou README.

Os comandos `tools/readme_objeto_contract.py`, `tools/validate_assistant.py` e
`tools/ci_local.py` pertencem ao repositório, não ao pacote no workspace. Eles
não executam código do README para decidir se a explicação é correta. O gate
confere cabeçalhos, ligações locais e migração; API e fontes exigem leitura.

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
corrigido silenciosamente em sprint documental. Um exemplar pode continuar
útil para estudar a forma e ser explicitamente inadequado para produção.

## 5. Fechamento por sprint

Entregue relações separadas de: READMEs criados/revisados; outras documentações
alteradas, com seção e motivo; ferramentas/testes; cópias geradas; arquivos
apenas inspecionados. Extraia a relação do diff real. Registre baseline,
regressões, testes pulados e ambiente. Salve o checkpoint antes de pausar.

O padrão é parar no fim da sprint autorizada. Após o piloto R02 e o aceite
editorial de 2026-09-12, o contrato vigente é **1.0.0**. Os textos de cada novo
lote continuam sujeitos a revisão e aceite próprios. Uma alteração posterior
no contrato exige revisão de impacto sobre documentos já entregues, não
aplicação silenciosa em um lote. R03-A termina antes da R03-B.
