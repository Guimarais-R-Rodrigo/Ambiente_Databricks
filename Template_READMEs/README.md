# Como desenvolver os READMEs a partir destes templates

> Material de orientação editorial. Não é uma nova versão dos READMEs e não deve ser publicado como documentação pronta.

Rascunhos preenchidos (um por sprint, ainda **fora** de `ambiente_fonte/` e **não** publicados no Databricks): [`sprints_preenchidos/PLANO.md`](sprints_preenchidos/PLANO.md).

## O que esta proposta pretende resolver

O leitor precisa aprender a pensar sobre a tarefa, escolher uma funcionalidade e usá-la com segurança. Uma imagem bonita ajuda a construir o mapa mental, mas não explica sozinha quais dados preparar, onde executar um comando ou como interpretar uma saída.

A orientação é **aprofundar a estrutura existente**, não substituí-la por um resumo novo. Os templates preservam os títulos e subtítulos dos documentos de referência; as ampliações estão identificadas como propostas. Nenhum README atual foi reescrito nesta entrega.

## Escopo dos arquivos

As cinco frentes trabalhadas têm seis READMEs físicos: a frente superior contém o guia do repositório e o guia do ambiente publicado. Há um template específico para cada um, além de quatro guias auxiliares do produto.

| Template | Documento a orientar |
|---|---|
| `README_raiz.md` | `README.md` do repositório |
| `README_assistant.md` | `ambiente_fonte/.assistant/README.md` |
| `README_snippets.md` | `ambiente_fonte/.assistant/hub_snippets/README.md` |
| `README_scripts.md` | `ambiente_fonte/.assistant/hub_scripts/README.md` |
| `README_skills.md` | `ambiente_fonte/.assistant/skills/README.md` |
| `README_prompts.md` | `ambiente_fonte/.assistant/hub_prompts/README.md` |
| `README_ambiente_fonte.md` | `ambiente_fonte/README.md` |
| `README_padroes.md` | `ambiente_fonte/.assistant/hub_padroes/README.md` |
| `README_visual_assets.md` | `ambiente_fonte/.assistant/hub_readmes_visual_assets/README.md` |
| `README_cabecalhos.md` | `ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/README.md` |

Índices históricos de auditoria, playbooks e ferramentas de manutenção não são as páginas de experiência do produto discutidas aqui; não foram redesenhados nem confundidos com essas dez entradas. O simulado e as propostas antigas não recebem versões paralelas dos templates.

## Como preencher sem transformar o template em texto final

1. Abrir o README de origem e seu template lado a lado.
2. Ler a intenção, o público e o exemplo central descritos no início do template.
3. Preservar títulos, subtítulos, âncoras e imagens atuais, salvo correção explicitamente justificada.
4. Desenvolver cada seção a partir da pergunta que ela precisa responder.
5. Acrescentar as subdivisões propostas dentro da seção correspondente, sem apagar os tópicos existentes.
6. Consultar código, exemplos e documentação oficial antes de afirmar assinatura, comportamento ou recurso.
7. Remover instruções ao autor, campos `{{...}}` e observações editoriais da futura versão pronta.
8. Conferir a leitura humana e os exemplos, depois os links e a consistência entre documentos.
9. Apresentar a versão para aprovação antes de substituir ou publicar.

Os títulos do molde são referência de continuidade, não autorização para perpetuar um erro. Exceções necessárias devem ser localizadas: por exemplo, um título que promete leitura em segundos deve ser substituído por um título descritivo, mantendo o conteúdo útil da seção.

## Tom: um colega experiente ensinando com paciência

Escrever em PT-BR, dirigindo-se ao leitor como “você” nos procedimentos. Explicar sem infantilizar. Preferir frases concretas: sujeito, ação, motivo e resultado observável.

- Introduzir o problema antes do nome técnico.
- Definir o termo no primeiro uso e reutilizar a mesma definição.
- Explicar por que uma etapa existe, especialmente quando parece burocrática.
- Não chamar tarefa de “simples”, “óbvia” ou “basta fazer”.
- Não prometer aprendizado ou execução em minutos/segundos.
- Evitar superlativos, slogans e metáforas que atribuam poderes ao sistema.
- Usar analogia curta e depois traduzi-la para os arquivos e ações reais.
- Distinguir orientação do Hub, funcionalidade da plataforma e responsabilidade do usuário.
- Não repetir alertas genéricos em todas as seções: colocar cada risco junto da ação correspondente.
- Não aumentar o documento com paráfrases. Acrescentar explicação, exemplo, interpretação ou decisão nova.

### Modelo de mudança de tom — explicação conceitual

**Frase insuficiente:** “Importe o helper e execute.”

**Modelo de explicação a desenvolver:** “O helper está salvo como um módulo Python. Para utilizá-lo, o notebook precisa localizar a pasta da biblioteca e importar a função desejada. Localizar a pasta não executa a análise: essa execução só acontece quando você chama a função com seus dados. Nos próximos passos, vamos separar essas duas ações e conferir o resultado de cada uma.”

É uma amostra de voz editorial, não texto para repetir em todos os documentos.

### Modelo de mudança de tom — interpretação

**Frase insuficiente:** “O resultado foi WARN.”

**Modelo de explicação a desenvolver:** “O aviso indica que uma das verificações atingiu o limite de atenção escolhido para este exemplo. Antes de decidir o que fazer, observe qual coluna gerou o alerta e qual foi a proporção medida. Um aviso não determina sozinho que você deve descartar a base; essa decisão depende da regra de uso que você está aplicando.”

Na versão final, acrescentar os números da fixture e o contrato real da função escolhida.

## Estrutura pedagógica de uma seção

Uma seção de conceito deve percorrer:

1. A situação que o leitor reconhece.
2. O conceito em linguagem comum.
3. O nome técnico e sua definição.
4. Um exemplo pequeno.
5. Como isso muda a próxima ação do leitor.
6. Limite ou confusão comum, quando relevante.

Uma seção operacional deve percorrer:

1. Objetivo da tarefa.
2. Antes de começar: acesso, dados, dependências e efeitos.
3. Onde fazer: chat, célula de notebook, arquivo ou repositório local.
4. Entrada completa e identificada.
5. Passos numerados com uma ação verificável por passo.
6. Código ou briefing integral.
7. Saída esperada, rotulada como exemplo até ser executada.
8. Leitura da saída, campo a campo quando necessário.
9. O que adaptar e o que preservar.
10. O que fazer se não funcionar e para onde seguir.

Não impor esse molde inteiro a uma seção de navegação; aplicar a profundidade conforme a função do trecho.

## Ficha de catálogo para código

Usar em snippets e scripts, adaptando ao tipo do objeto:

- **Qual problema resolve:** situação concreta, sem apenas traduzir o nome.
- **Conceito necessário:** explicação breve de PSI, RFV, split, schema ou outro termo.
- **Quando usar / quando não usar:** fronteiras com objetos próximos.
- **Entrada:** tipo, colunas, unidade, grão, tempo e pré-condições.
- **Interface:** import e assinatura conferidos na implementação.
- **Exemplo:** entrada pequena e chamada completa.
- **Saída:** tipo e campos, com uma interpretação.
- **Efeitos e custo:** leitura, coleta, gravação ou dependência pertinente.
- **Como adaptar:** parâmetros substituíveis e decisões que dependem do usuário.
- **Onde aprofundar:** link para o exemplo específico, não apenas para a raiz da coleção.

A ficha serve à compreensão; não precisa virar dez subtítulos minúsculos para uma constante. Para funções complexas, as subdivisões devem ser visíveis.

## Ficha de catálogo para skill

- Demanda e conceitos.
- Quando escolher esta skill e quando escolher outra.
- Informações e artefatos que o usuário fornece.
- Pedido completo de exemplo.
- Método e entregáveis esperados.
- Relação possível com helpers reais.
- Como revisar a resposta.
- Limites, aprovações e recuperação quando faltou contexto.

## Ficha de catálogo para prompt

- Pergunta que o briefing ajuda a formular.
- Cenário apropriado e cenário inadequado.
- Campos essenciais explicados.
- Microexemplo preenchido, não só placeholders.
- Contexto a fornecer e modo de trabalho permitido.
- Saída solicitada e critérios de aceite.
- Tratamento de informação desconhecida.
- Exemplo completo de acompanhamento.

## Requisitos de um exemplo realmente didático

Não deixar `df`, `spark_table`, `resultado` ou um modelo treinado aparecerem sem preparação. Se a preparação estiver fora do trecho, apontar exatamente onde ela está e o que deve produzir.

| Elemento | O que o exemplo precisa conter |
|---|---|
| Dados | Fixture sintética ou instrução precisa de preparo; schema e significado |
| Local | Onde colar o código ou pedido e pré-requisitos |
| Parâmetros | O que substituir, por quê e com qual tipo de valor |
| Execução | Chamada real de API existente; nenhuma instalação/escrita implícita |
| Resultado | Valores conferíveis ou propriedades esperadas |
| Interpretação | O que o número/campo permite concluir e o que não permite |
| Adaptação | Pequena variação resolvida e proposta de exercício |
| Recuperação | Erro comum, causa provável e próximo passo seguro |

Para funções numéricas, usar ao menos um caso calculável à mão. Para prompts, usar pedido completo e checklist de revisão. Para skills, distinguir evidência de carregamento de qualidade da resposta. Para imagens, distinguir arquivo presente de renderização legível.

## Imagens e escrita trabalhando juntas

Preservar as imagens aprovadas e a arquitetura de assets. Não pedir nova arte nesta etapa.

**Antes da figura:** explicar a pergunta que ela responde.

**Depois da figura:** orientar a leitura de duas ou três relações relevantes e aplicar uma delas ao exemplo.

**Equivalente textual:** preservar a informação essencial para quem não vê o PNG e para leitura de contexto pela IA.

Não escrever apenas “conforme a figura acima”. Não reproduzir todos os rótulos em um parágrafo. O texto deve aprofundar a relação, não transcrever a imagem inteira.

Usar tabelas para comparação, código para instrução executável, listas numeradas para ação e prosa para explicação. Evitar transformar todo o README numa coleção de tabelas compactas. Emojis são marcadores de navegação, não substitutos de títulos precisos.

## Uma história coerente, sem duplicação entre guias

O exemplo de campanha é uma proposta didática, não um cenário real da organização:

- Raiz: apresenta as peças e a arquitetura.
- Assistant: conduz uma tarefa completa.
- Snippets: ensina a reutilizar a implementação.
- Scripts: ensina a avaliar e interpretar um recurso.
- Skills: ensina a aplicar um método.
- Prompts: ensina a formular a demanda.

O caso pode ser compartilhado, mas cada guia responde a outra pergunta. O usuário que abre somente um deles deve encontrar o pré-requisito necessário, não uma obrigação de ler todos os demais.

## Cuidados editoriais que não podem ser perdidos

Não inserir códigos de decisões internas, nem referências a essas decisões, nos READMEs destinados ao leitor. Não narrar a passagem entre ambientes no material de apresentação. Preservar limites reais de uso, sem atribuir uma homologação que não existe.

Contagens, versões, assinaturas e afirmações de plataforma devem vir das fontes atuais. Não chamar recursos customizados de funcionalidades institucionais. Não dizer que uma imagem explica tudo, que um prompt garante correção ou que uma skill executa todos os helpers automaticamente.

Os templates não atualizam os estados históricos de publicação. Consultar a evidência corrente separadamente: outro agente pode já ter encerrado uma pendência documentada em uma rodada anterior.

## Critério de aprovação editorial

- Um leitor iniciante no Hub consegue explicar o conceito com suas próprias palavras?
- Consegue escolher entre ferramentas próximas e justificar a escolha?
- Sabe onde executar cada ação e quais dados preparar?
- Existe ao menos um percurso completo, sem variável ou recurso implícito?
- Consegue interpretar o resultado e identificar algo que deu errado?
- Sabe adaptar o exemplo a outra situação sem copiar decisões de negócio?
- A imagem foi preservada e a prosa acrescenta informação?
- Os títulos e subtítulos originais continuam reconhecíveis?
- As adições criam profundidade em vez de repetição?
- Os limites estão junto do procedimento, sem slogans ou promessas temporais?

O README está didaticamente completo quando essas perguntas têm respostas demonstráveis — não quando atinge um número arbitrário de páginas.

