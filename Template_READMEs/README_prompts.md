# Hub Prompts — Briefings Técnicos Estruturados para Genie Code

> TEMPLATE EDITORIAL — não é o README reescrito. Origem: `ambiente_fonte/.assistant/hub_prompts/README.md`.
> Aplicar as orientações comuns de `Template_READMEs/README.md`. Os campos e notas ao autor saem da versão final.

**Público:** Pessoa que conhece a demanda de negócio, mas não sabe transformá-la em pedido técnico claro para a Genie Code.

**Aprendizado esperado:** Escolher o briefing, compreender cada campo, preenchê-lo sem inventar dados e revisar o resultado contra o pedido.

**Tom específico:** Orientador, não burocrático: explicar para que cada campo serve, o erro que evita e como preencher quando falta informação.

**Fio condutor proposto:** Um pedido vago sobre campanha se transforma gradualmente num briefing completo; o leitor entende a razão de cada informação acrescentada.

**Abertura a escrever:** {{situação reconhecível pelo leitor}} → {{dificuldade que este guia resolve}} → {{o que ele aprenderá}} → {{primeira rota de leitura}}. Preservar o cabeçalho e o título atuais; não abrir com slogan ou tempo estimado de leitura.

---

## 🧭 Neste Guia

**Função desta seção:** Organizar a jornada escolher → preencher → fornecer contexto → revisar → validar.

**Subdivisão ou aprofundamento proposto:** Oferecer também consulta por família sem substituir a primeira jornada didática.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 🎯 O que é um Prompt Estruturado?

**Função desta seção:** Ensinar briefing como definição compartilhada do trabalho, não fórmula mágica de prompting.

**Subdivisão ou aprofundamento proposto:** Mostrar pedido vago e versão melhorada, anotando o motivo de cada acréscimo.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 🏗️ A Anatomia de uma Pasta de Prompt

**Função desta seção:** Explicar template, notebook e exemplo preenchido como três papéis, não três formas equivalentes de executar.

**Subdivisão ou aprofundamento proposto:** Separar texto que será copiado para o chat e orientações que são apenas para o leitor.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### 1. O Arquivo Markdown (`<nome>.md`)

**Leitura guiada:** mostrar o que o leitor encontrará dentro do arquivo, por que ele existe e se deve ler, copiar, importar ou executar. Apontar o que não acontece só por abrir o arquivo.

### 2. O Notebook de Acompanhamento (`exemplo_<nome>.py`)

**Leitura guiada:** mostrar o que o leitor encontrará dentro do arquivo, por que ele existe e se deve ler, copiar, importar ou executar. Apontar o que não acontece só por abrir o arquivo.

### 3. Exemplo de briefing completamente preenchido

**Transformar em exemplo acompanhado:** cenário, preparo, dados/artefatos, pedido ou código, resultado esperado e leitura do resultado. Explicar o que pode ser substituído. Se houver resposta ilustrativa de IA, rotular como ilustração e não como execução certificada.

## 🧩 A Disciplina dos Parâmetros: Evitando Alucinações

**Função desta seção:** Ensinar todos os tipos de informação: objetivo, recurso, grão, chave, tempo, restrição, saída e aceite.

**Subdivisão ou aprofundamento proposto:** Dar exemplos de valor concreto, NÃO INFORMADO e NÃO APLICÁVEL; não dizer que essas expressões são travas de sistema.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### O contexto mínimo que evita retrabalho

**Questão de desenvolvimento:** o que o leitor precisa compreender em “O contexto mínimo que evita retrabalho” para avançar na seção “🧩 A Disciplina dos Parâmetros: Evitando Alucinações”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

## 🔄 A Sinergia Triangular: Prompts, Skills e Helpers

**Função desta seção:** Aplicar prompt, skill e helper ao mesmo caso; explicar interfaces e ação humana.

**Subdivisão ou aprofundamento proposto:** Não repetir a introdução do ecossistema: mostrar a passagem concreta de briefing para método e chamada.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 📂 Famílias Funcionais de Prompts

**Função desta seção:** Preservar os quatro grupos conceituais e deixar clara a estrutura física.

**Subdivisão ou aprofundamento proposto:** Mostrar como decidir entre dois briefings próximos com o mesmo conjunto de dados.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### Matriz rápida de seleção

**Questão de desenvolvimento:** o que o leitor precisa compreender em “Matriz rápida de seleção” para avançar na seção “📂 Famílias Funcionais de Prompts”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

### Legenda dos campos de cada briefing

**Questão de desenvolvimento:** o que o leitor precisa compreender em “Legenda dos campos de cada briefing” para avançar na seção “📂 Famílias Funcionais de Prompts”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

### 1. Exploração & Perfilamento

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

### 2. Modelagem, Safras & Estatística

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

### 3. Qualidade, Reconciliação & Auditoria

**Questão de desenvolvimento:** o que o leitor precisa compreender em “3. Qualidade, Reconciliação & Auditoria” para avançar na seção “📂 Famílias Funcionais de Prompts”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

### 4. Documentação, Tutoria & Onboarding

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

## 📖 Catálogo Detalhado de Prompts

**Função desta seção:** Preservar os 16 prompts e todos os grupos; dar uma ficha de preenchimento e validação por prompt.

**Subdivisão ou aprofundamento proposto:** Não reduzir catálogo a skill recomendada: o usuário precisa aprender que informação ele próprio fornece.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### 🔍 Exploração & Perfilamento

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

#### `eda_rapida` — Perfil Preliminar de Dados

**Orientação específica:** Desenvolver uma primeira inspeção de base de campanha; explicar grão, chave e nulos. Exigir um microbriefing preenchido e uma conta conhecida.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `eda_completa` — Análise Exploratória Profunda

**Orientação específica:** Explicar o que o aprofundamento acrescenta à inspeção inicial: distribuições, relações, segmentos e limites. Comparar quando basta EDA rápida.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `cross_eda` — Exploração Cruzada Multi-Tabelas

**Orientação específica:** Usar duas tabelas e mostrar cardinalidade, cobertura e multiplicação de linhas antes da junção. Explicar chave e grão de saída.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

### 📈 Modelagem, Safras & Estatística

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

#### `safra` — Análise de Coortes e Maturação Temporal

**Orientação específica:** Definir coorte/safra, MOB e maturidade antes de pedir a análise. Usar poucos contratos e explicitar censura e denominador.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `stat_check` — Validação Estatística de Hipóteses

**Orientação específica:** Partir de uma pergunta sobre diferença entre grupos. Explicar hipótese, pressuposto, efeito e incerteza antes dos nomes dos testes.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `feature_engineering` — Engenharia de Atributos Temporais

**Orientação específica:** Mostrar uma feature que só pode usar informação disponível até a decisão; diferenciar data do evento e disponibilidade.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `baseline_orchestration` — Modelo Baseline Ponta a Ponta

**Orientação específica:** Definir baseline e por que começar por ele. Explicar split, população, métrica e tracking, sem transformar o pedido em treino indiscriminado.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `pipeline` — Construção de Pipelines Modulares

**Orientação específica:** Explicar etapa, dependência, contrato e idempotência com uma rotina concreta. Diferenciar planejar automação e criar recursos.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `explainability` — Explicabilidade de Modelos de ML

**Orientação específica:** Distinguir explicação global/local e saída/classe de interesse. Ensinar o limite entre associação do modelo e causalidade.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `monitoramento_modelo` — Acompanhamento de Performance e Drift

**Orientação específica:** Comparar população de referência e atual; separar drift, performance e regra de ação. Explicar o que investigar antes de sugerir retreino.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

### 🛡️ Qualidade, Reconciliação & Auditoria

**Questão de desenvolvimento:** o que o leitor precisa compreender em “🛡️ Qualidade, Reconciliação & Auditoria” para avançar na seção “📖 Catálogo Detalhado de Prompts”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

#### `data_quality` — Varredura e Regras de Integridade

**Orientação específica:** Transformar regra de negócio em verificação mensurável e critério explícito. Mostrar que aprovação depende do escopo das regras.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `comparar_tabelas` — Reconciliação entre Bases de Dados

**Orientação específica:** Demonstrar linha ausente, linha extra e valor divergente em duas bases pequenas. Explicar chave da reconciliação.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `auditoria_skills` — Auditoria de Código Gerado por IA

**Orientação específica:** Mostrar pedido, método, código e evidência sendo confrontados. Incluir um erro sintético que a revisão deveria localizar.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

### 📚 Documentação, Tutoria & Onboarding

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

#### `comentar_notebook` — Refatoração e Documentação Didática

**Orientação específica:** Demonstrar documentação antes/depois preservando a lógica; explicar qual público precisa compreender a etapa.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `tutor_explicar` — Mentoria Técnica e Explicabilidade de Código

**Orientação específica:** Mostrar como declarar nível de conhecimento e objetivo de aprendizado; incluir conceito, leitura de código e exercício guiado.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

#### `novo_projeto` — Kick-off Estruturado de Projetos de Dados

**Orientação específica:** Ensinar como delimitar objetivo, perguntas em aberto, entregáveis e restrições antes de propor arquitetura ou criar arquivos.

**Preencher:** {{quando usar}} → {{campo essencial e explicação}} → {{microexemplo preenchido}} → {{contexto a fornecer}} → {{critério de aceite}}.

## 🛠️ Passo a Passo Operacional: Do Briefing ao Resultado

**Função desta seção:** Expandir os cinco passos com exemplo preenchido, contexto fornecido, revisão e conferência.

**Subdivisão ou aprofundamento proposto:** Mostrar primeira resposta, pedido de ajuste e critério de encerramento como ilustração, nunca como teste real.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### 1. Selecione o Briefing Adequado

**Molde do passo:** {{o que você fará}} → {{onde fará}} → {{por que isso é necessário}} → {{entrada/trecho completo}} → {{o que observar ao terminar}}. Acrescentar uma nota de adaptação e um erro comum desse passo. Não depender de variável, tabela ou contexto que ainda não foi apresentado.

### 2. Preencha os Metadados com Rigor

**Molde do passo:** {{o que você fará}} → {{onde fará}} → {{por que isso é necessário}} → {{entrada/trecho completo}} → {{o que observar ao terminar}}. Acrescentar uma nota de adaptação e um erro comum desse passo. Não depender de variável, tabela ou contexto que ainda não foi apresentado.

### 3. Anexe os Recursos e Defina o Modo de Trabalho

**Molde do passo:** {{o que você fará}} → {{onde fará}} → {{por que isso é necessário}} → {{entrada/trecho completo}} → {{o que observar ao terminar}}. Acrescentar uma nota de adaptação e um erro comum desse passo. Não depender de variável, tabela ou contexto que ainda não foi apresentado.

### 4. Revise o Plano antes de Executar

**Molde do passo:** {{o que você fará}} → {{onde fará}} → {{por que isso é necessário}} → {{entrada/trecho completo}} → {{o que observar ao terminar}}. Acrescentar uma nota de adaptação e um erro comum desse passo. Não depender de variável, tabela ou contexto que ainda não foi apresentado.

### 5. Valide a Entrega contra o Contrato de Saída

**Molde do passo:** {{o que você fará}} → {{onde fará}} → {{por que isso é necessário}} → {{entrada/trecho completo}} → {{o que observar ao terminar}}. Acrescentar uma nota de adaptação e um erro comum desse passo. Não depender de variável, tabela ou contexto que ainda não foi apresentado.

## ❓ Perguntas Frequentes (FAQ)

**Função desta seção:** Manter perguntas e explicar como lidar com incerteza, contexto e fases da conversa.

**Subdivisão ou aprofundamento proposto:** Acrescentar o que não copiar do template, quando dividir a demanda e como contestar dado inventado.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### 1. Por que preencher um briefing estruturado em vez de apenas fazer uma pergunta livre?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 2. O que preencher quando eu não souber a chave primária ou a granularidade?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 3. Por que o notebook `exemplo_*.py` não executa o prompt automaticamente?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 4. Quando abrir uma conversa nova?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 5. Minha equipe pode criar novos modelos de briefing?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 6. O prompt carrega a skill e os helpers automaticamente?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

## 🔗 Continue Explorando

**Função desta seção:** Encaminhar ao template real, ao notebook e à skill pertinente, conforme objetivo.

**Subdivisão ou aprofundamento proposto:** Explicar o próximo artefato que o usuário deverá produzir.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

---

## Orientações adicionais para desenvolver este README

### Subdivisões propostas, sem apagar as atuais

Sob disciplina dos parâmetros: “Como descobrir o que ainda falta”, “O que copiar para o chat” e “Como revisar antes de enviar”. Cada ficha do catálogo deve conter microexemplo preenchido; o tutorial central deve conter um briefing integral.

### Exemplo central obrigatório

Usar eda_rapida com fixture de 20 linhas e nulidade conhecida para mostrar contexto e aceite verificáveis. Explicar cada campo do briefing completo em tabela campo → significado → valor escolhido → motivo. Depois mostrar como o mesmo caso pede comparar_tabelas ou feature_engineering quando o objetivo muda.

O exemplo final deve conter pré-requisitos, local de uso, entrada completa, passos, chamada/pedido, resultado e interpretação. Código só é copiável quando os recursos e variáveis necessários foram apresentados. Acrescentar uma variação comentada para ensinar adaptação.

### Como integrar as figuras aprovadas

Manter blueprint, roteador de famílias e storyboard. O blueprint orienta preenchimento, o roteador escolha, o storyboard interação; a prosa não deve repetir a mesma lista três vezes.

As imagens ficam nos mesmos assets canônicos. Os caminhos devem ser calculados a partir do README final, não desta pasta de templates. Não inserir a informação essencial apenas no PNG.

### Conferência específica antes de apresentar a versão

- Todos os títulos e subtítulos acima foram preservados ou têm correção pontual justificada?
- Cada conceito usado nos procedimentos foi explicado antes?
- O exemplo central pode ser acompanhado sem adivinhar dados, paths ou etapas?
- O resultado é interpretado, e não apenas exibido?
- Cada recomendação técnica foi conferida no código e, para recursos da plataforma, na documentação oficial vigente?
- Não há códigos de decisões, história de migração, promessas em segundos/minutos ou capacidades inventadas?
- As notas ao autor e placeholders foram removidos da versão pronta?

**Critério final:** Escolher o briefing, compreender cada campo, preenchê-lo sem inventar dados e revisar o resultado contra o pedido. A versão precisa demonstrar esse aprendizado; quantidade de texto sozinha não é aceite.

