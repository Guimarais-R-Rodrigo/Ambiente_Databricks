# Glossário de leitura

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-glossario"></a>
<a id="mt-mod-glossario-h-glossário-de-leitura"></a>
### Glossário de leitura

Esta referência de consulta acompanha as explicações dos capítulos. Um termo
não substitui o contrato da função ou a decisão de negócio do seu caso. Os
capítulos apresentam o conceito antes de aprofundar sua implementação.

| Termo | Significado para a leitura | Onde aprofundar |
|---|---|---|
| API | Interface que um programa oferece: nomes, argumentos e resultados pelos quais outro programa usa sua capacidade. | [MT03](MT-parte-i.md#mt03), [MT05](MT-parte-ii.md#mt05) |
| Argumento | Valor entregue a um parâmetro numa chamada; mudar seu valor pode mudar o resultado, custo ou efeito. | [MT03](MT-parte-i.md#mt03) |
| Parâmetro | Nome declarado pela função para receber uma entrada, às vezes com valor padrão ou condição de uso. | [MT03](MT-parte-i.md#mt03) |
| Retorno | Objeto que a função entrega ao código que a chamou; não é necessariamente o mesmo que aparece na tela. | [MU06](MU-parte-ii.md#mu06) |
| Função | Operação nomeada que recebe argumentos e realiza um comportamento; seu contrato diz se retorna valor ou produz efeitos. | [MT03](MT-parte-i.md#mt03) |
| Classe | Definição de um tipo de objeto, com estado e operações; criar uma instância não garante que um modelo tenha sido treinado. | [MT03](MT-parte-i.md#mt03), [MT09](MT-parte-ii.md#mt09) |
| Módulo | Unidade de código Python carregável por importação, frequentemente um arquivo; bibliotecas e notebooks de exemplo têm papéis distintos. | [MT03](MT-parte-i.md#mt03) |
| Pacote | Organização de módulos que fornece nomes compostos, como hub_snippets.constants.format_br. | [MT03](MT-parte-i.md#mt03) |
| Fachada | Entrada pública de uma pasta de objeto; reúne reexports e nomes declarados sem obrigar o leitor a conhecer arquivos internos. | [MT05](MT-parte-ii.md#mt05) |
| Importação | Carregamento de módulo ou acesso a nomes no interpretador; não equivale a chamar a função para analisar dados. | [MT03](MT-parte-i.md#mt03), [MU06](MU-parte-ii.md#mu06) |
| Dependência | Biblioteca, serviço ou recurso de que um componente precisa; a necessidade pode aparecer no import ou somente na chamada. | [MT03](MT-parte-i.md#mt03) |
| Runtime | Ambiente efetivo de execução, incluindo versões e recursos disponíveis; o arquivo existir no repositório não instala esse ambiente. | [MT03](MT-parte-i.md#mt03) |
| DataFrame | Tabela manipulada pelo programa. pandas e Spark oferecem DataFrames com contratos e execução diferentes. | [MT06](MT-parte-ii.md#mt06), [MT07](MT-parte-ii.md#mt07) |
| Driver | Processo que coordena o programa Spark e recebe resultados trazidos para Python; sua memória impõe limites de coleta. | [MT07](MT-parte-ii.md#mt07-1) |
| Executor | Trabalhador que executa tarefas distribuídas do Spark; não é o agente autor dos manuais. | [MT07](MT-parte-ii.md#mt07-1) |
| Transformação | Operação que prepara um novo plano de dados; em Spark muitas transformações adiam o trabalho até uma ação. | [MT07](MT-parte-ii.md#mt07-1) |
| Ação Spark | Operação que pede um resultado e provoca avaliação do plano, como contar ou coletar. | [MT07](MT-parte-ii.md#mt07-1) |
| Coleta | Transporte de resultado do processamento distribuído para o driver; verificar quantidade de linhas e colunas antes de fazê-lo. | [MT07](MT-parte-ii.md#mt07-1) |
| Grão | O que uma linha representa, como uma entidade, um evento ou uma entidade numa data; define a leitura das chaves e contagens. | [MT07](MT-parte-ii.md#mt07-4), [MU09](MU-parte-iii.md#mu09) |
| Chave | Coluna ou conjunto de colunas usado para identificar ou relacionar registros; presença de chave não prova unicidade. | [MT07](MT-parte-ii.md#mt07-3) |
| Cobertura | Parcela da população definida que satisfaz um critério; seu significado depende do numerador, denominador e exclusões. | [MT07](MT-parte-ii.md#mt07-3), [MT08](MT-parte-ii.md#mt08) |
| Nulo | Ausência reconhecida pelo tipo/engine; string vazia e sentinelas textuais podem ter significado diferente. | [MU06](MU-parte-ii.md#mu06-3) |
| Amostra | Subconjunto escolhido segundo uma regra; limitar linhas, sortear e preservar estratos não respondem à mesma pergunta. | [MT07](MT-parte-ii.md#mt07-2) |
| Estrato | Grupo considerado separadamente na seleção de uma amostra; preservar grupo raro pode alterar proporções do conjunto final. | [MT07](MT-parte-ii.md#mt07-2) |
| Disponibilidade temporal | Instante a partir do qual a informação podia ser conhecida; pode ser posterior à data que o dado descreve. | [MT07](MT-parte-ii.md#mt07-3) |
| Vazamento temporal | Uso, numa decisão ou avaliação histórica, de informação que ainda não estava disponível naquela ocasião. | [MT08](MT-parte-ii.md#mt08), [MU09](MU-parte-iii.md#mu09) |
| Safra ou coorte | Grupo definido pela ocasião de entrada/originação; comparar grupos exige esclarecer maturidade e denominadores. | [MT08](MT-parte-ii.md#mt08), [MU10](MU-parte-iii.md#mu10) |
| PSI | Índice de estabilidade populacional: resume diferença de proporções entre distribuições numa régua de faixas definida. | [MT07](MT-parte-ii.md#mt07-3), [MT08](MT-parte-ii.md#mt08) |
| CSI | Índice de estabilidade de características; no helper Spark pode comparar colunas numéricas ou categorias, conforme contrato. | [MT07](MT-parte-ii.md#mt07-3) |
| Fixture | Conjunto de dados e condições preparado para um teste ou demonstração; não representa automaticamente dados reais. | [MT11](MT-parte-ii.md#mt11-4) |
| Asserção | Verificação codificada de uma expectativa, como comparar uma saída com PASS; ler a asserção não prova que foi executada. | [MT11](MT-parte-ii.md#mt11-4) |
| Schema | Descrição estrutural permitida para dados, com campos, tipos e restrições; regras semânticas podem exigir código adicional. | [MT15](MT-parte-iv.md#mt15) |
| JSON | Formato textual de dados com objetos, arrays e valores; não é, por si, programa, autorização ou configuração aceita. | [MT15](MT-parte-iv.md#mt15), [MT23](MT-parte-vi.md#mt23) |
| YAML | Formato textual de dados usado em especificações/configurações do projeto; o consumidor define validação e interpretação. | [MT15](MT-parte-iv.md#mt15), [MT21](MT-parte-v.md#mt21) |
| HTML | Marcação que organiza uma representação de conteúdo para exibição, como tabela ou cabeçalho. | [MT06](MT-parte-ii.md#mt06) |
| CSS | Regras de apresentação usadas por consumidores HTML, como cor e tipografia; aparência não substitui significado dos valores. | [MT06](MT-parte-ii.md#mt06) |
| Token visual | Nome de uma propriedade controlada do tema, como cor de texto ou tamanho; o consumidor decide como aplicá-la. | [MT23](MT-parte-vi.md#mt23), [MT24](MT-parte-vi.md#mt24) |
| Tema resolvido | Resultado validado da resolução de uma configuração no contexto indicado; não é aprovação humana nem efeito visual automático. | [MT23](MT-parte-vi.md#mt23) |
| Manifesto | Registro estruturado de elementos e identidades/integridade, conforme contrato; sua presença não atesta publicação. | [MT18](MT-parte-iv.md#mt18), [MT25](MT-parte-vi.md#mt25) |
| Hash | Resumo calculado sobre bytes ou outra preimage definida; integridade exige saber algoritmo e conteúdo resumido. | [MT18](MT-parte-iv.md#mt18) |
| Preimage | Conteúdo exato submetido ao algoritmo de hash; YAML bruto e uma projeção semântica canônica podem gerar identidades diferentes. | [MT18](MT-parte-iv.md#mt18), [MT22](MT-parte-v.md#mt22) |
| Fonte canônica | Artefato editável que o projeto trata como dono de um conteúdo; cópias derivadas e operacionais têm outros papéis. | [MT02](MT-parte-i.md#mt02) |
| Derivado | Artefato produzido a partir da fonte; sua manutenção deve respeitar o processo de geração. | [MT02](MT-parte-i.md#mt02), [MT28](MT-parte-vii.md#mt28) |
| Candidato | Conteúdo ou capacidade em avaliação no escopo declarado; existência de código não encerra aceite ou homologação. | [MT01](MT-parte-i.md#mt01), [MT29](MT-parte-vii.md#mt29) |
| Evidência | Registro que sustenta uma afirmação delimitada, com fonte, data, versão e ambiente apropriados. | [MT01](MT-parte-i.md#mt01), [MT19](MT-parte-iv.md#mt19) |
| Gate | Condição de passagem prevista no fluxo; pode exigir dados, verificação ou decisão da autoridade competente. | [MU04](MU-parte-ii.md#mu04), [MT16](MT-parte-iv.md#mt16) |
| Homologação | Verificação/aceite no escopo e ambiente declarados; teste local, integração Git e publicação são dimensões separadas. | [MT29](MT-parte-vii.md#mt29), [MU19](MU-parte-vi.md#mu19) |
| Argumento somente nomeado | Parâmetro depois de `*` na assinatura Python; a chamada precisa indicar seu nome, e uma posição adicional não é equivalente. | [MT10](MT-parte-ii.md#mt10-2) |
| Gerenciador de contexto | Objeto usado por `with` para delimitar entrada, saída e tratamento de falhas; sair do bloco não garante reversão de efeitos externos já realizados. | [MT10](MT-parte-ii.md#mt10-3) |
| Metadata-first | Descoberta que começa por metadados autorizados e aprofunda somente candidatos pertinentes; não autoriza consultar registros, contar ou perfilar dados. | [MT20](MT-parte-v.md#mt20), [MU13](MU-parte-iv.md#mu13) |
| Binding | Associação explícita entre uma referência lógica e o recurso físico do ambiente; o nome lógico não prova acesso nem autoriza gravar identificadores privados no projeto. | [MT22](MT-parte-v.md#mt22), [MU13](MU-parte-iv.md#mu13) |
| INDETERMINADO | Estado preservado quando a evidência ou condição exigida não permite concluir; não é sinônimo de FALSE, zero ou resultado negativo. | [MT20](MT-parte-v.md#mt20), [MT21](MT-parte-v.md#mt21) |
| Força de evidência | Semântica de uma pontuação heurística declarada; escala 0–100, por si só, não a transforma em probabilidade calibrada. | [MT20](MT-parte-v.md#mt20), [MT22](MT-parte-v.md#mt22) |
| Receipt | Registro produzido por uma rota executada segundo seu contrato; só sustenta os artefatos e verificações ali ligados, sem conceder aceite universal. | [MT18](MT-parte-iv.md#mt18) |
| Postflight | Verificação posterior prevista numa rota; sua disponibilidade e condição de conclusão dependem da implementação e da policy da skill. | [MT19](MT-parte-iv.md#mt19) |


<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
