# Hub Scripts

> TEMPLATE EDITORIAL — não é o README reescrito. Origem: `ambiente_fonte/.assistant/hub_scripts/README.md`.
> Aplicar as orientações comuns de `Template_READMEs/README.md`. Os campos e notas ao autor saem da versão final.

**Público:** Usuário que precisa avaliar ou transformar um recurso e ainda não domina os contratos dos sete utilitários.

**Aprendizado esperado:** Escolher o script correto, fornecer entrada válida, interpretar seu retorno específico e separar diagnóstico de decisão operacional.

**Tom específico:** Explicar o raciocínio por trás da chamada e do veredito. Evitar linguagem de aprovação absoluta, guardião infalível ou automação implícita.

**Fio condutor proposto:** Uma base de campanha precisa ser perfilada, verificada e eventualmente transformada; o leitor aprende por que ferramentas distintas respondem a perguntas distintas.

**Abertura a escrever:** {{situação reconhecível pelo leitor}} → {{dificuldade que este guia resolve}} → {{o que ele aprenderá}} → {{primeira rota de leitura}}. Preservar o cabeçalho e o título atuais; não abrir com slogan ou tempo estimado de leitura.

---

## 🧭 Neste Guia

**Função desta seção:** Oferecer trilhas de escolher utilitário, executar primeira checagem e interpretar resultado.

**Subdivisão ou aprofundamento proposto:** Apontar a diferença entre diagnóstico, transformação e serialização.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 🔍 O que é um Script neste Ecossistema?

**Função desta seção:** Definir o uso local do termo e comparar com snippet por exemplos, sem confundir arquivo executável de terminal com interface do Hub.

**Subdivisão ou aprofundamento proposto:** Ensinar execução sob demanda e responsabilidade do consumidor.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 🏛️ Arquitetura e o Padrão "Pasta de Objeto"

**Função desta seção:** Apresentar cada arquivo e o caminho público de importação com objeto real.

**Subdivisão ou aprofundamento proposto:** Explicar que o notebook de exemplo demonstra, mas não é o módulo a importar.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 📚 Catálogo Detalhado

**Função desta seção:** Preservar os três grupos e sete utilitários, explicando seus conceitos antes dos nomes de API.

**Subdivisão ou aprofundamento proposto:** Aplicar ficha de entrada, saída, uso, exemplo, interpretação, custo e quando não usar a cada um.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### 🩺 1. Qualidade e Perfilamento de Dados (Data Health)

**Questão de desenvolvimento:** o que o leitor precisa compreender em “🩺 1. Qualidade e Perfilamento de Dados (Data Health)” para avançar na seção “📚 Catálogo Detalhado”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

#### `data_quality_check` — Inspeção Sanitária Pré-Modelagem

**Orientação específica:** Explicar chave candidata, nulidade, freshness e limiares. Ensinar os campos checks/alerts/score e o alcance de pass; não inventar metrics nem argumentos ausentes. Inserir caso pequeno com proporção de nulos conhecida.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

#### `quick_profile` — Raio-X de Schema e Distribuição

**Orientação específica:** Explicar perfilamento e distinguir medidas da tabela inteira de medidas da amostra. Fornecer um exemplo com amostra completa antes da variação amostral; interpretar os nomes *_sample e *_full_table.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

#### `rfv_calculator` — Recência, Frequência e Valor

**Orientação específica:** Definir recência, frequência e valor com quatro transações e data de corte. Mostrar uma transação futura excluída. Explicar que a saída é DataFrame, não diagnóstico de aprovação.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

### 📉 2. Estabilidade e Monitoramento de Distribuição

**Questão de desenvolvimento:** o que o leitor precisa compreender em “📉 2. Estabilidade e Monitoramento de Distribuição” para avançar na seção “📚 Catálogo Detalhado”? Preencher {{explicação do conceito/relação}}, {{aplicação ao exemplo da seção}} e {{consequência prática}}. Acrescentar definição dos termos novos; não repetir apenas o título em uma frase.

#### `drift_detector` — Detecção de Desvios de Distribuição

**Orientação específica:** Definir referência, comparação e distribuição. Mostrar duas coortes iguais e uma alterada. Explicar ausência de classificação sem política e por que drift não demonstra causalidade ou perda de performance.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

### 📐 3. Governança, Contratos e Boas Práticas de Código

**Desenvolvimento da família:** explicar qual objetivo reúne os itens, apresentar uma situação concreta e compará-la com uma família vizinha. Manter cada item e sua ordem de referência; aprofundar os detalhes nas fichas, sem duplicar toda a ficha nesta introdução.

#### `schema_to_yaml` — Contratos de Dados em YAML

**Orientação específica:** Definir schema e serialização com um exemplo de coluna/tipo/nulabilidade. Mostrar texto de saída, escape e persistência como ação separada.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

#### `naming_checker` — Guardião de Nomenclatura

**Orientação específica:** Explicar convenção local versus regra de plataforma. Comparar nome válido e violação, e ensinar a ler a lista retornada.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

#### `doc_coverage` — Auditoria Estrutural de Documentação

**Orientação específica:** Explicar células Markdown próximas do código e o significado heurístico da cobertura. Mostrar exemplo com bloco descoberto; distinguir arquivo exportado de URL de notebook.

**Preencher:** {{entrada}} → {{chamada real}} → {{saída}} → {{interpretação}} → {{limite}}. Não deixar a demonstração restrita ao nome da ferramenta.

## 🛠️ Passo a Passo Operacional: Como Usar um Script

**Função desta seção:** Transformar o exemplo DQ em tutorial autocontido. Explicar tabela/view, chave candidata, nulos e thresholds antes do código.

**Subdivisão ou aprofundamento proposto:** Acrescentar um caso pass, um warn e um fail com conta pequena; separar parâmetros do usuário e nomes fixos da API.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### Exemplo Prático de Código

**Transformar em exemplo acompanhado:** cenário, preparo, dados/artefatos, pedido ou código, resultado esperado e leitura do resultado. Explicar o que pode ser substituído. Se houver resposta ilustrativa de IA, rotular como ilustração e não como execução certificada.

### Como interpretar o retorno

**Ensinar a interpretar:** mostrar campos reais, tipos, unidades e uma saída pequena. Associar o valor a uma conclusão permitida e a uma conclusão que não se pode tirar. Separar diagnóstico e decisão.

### Leitura visual do veredito

**Ensinar a interpretar:** mostrar campos reais, tipos, unidades e uma saída pequena. Associar o valor a uma conclusão permitida e a uma conclusão que não se pode tirar. Separar diagnóstico e decisão.

## ⚙️ O que Acontece Durante a Execução?

**Função desta seção:** Traduzir scan, aggregate, shuffle e sample com operações do exemplo.

**Subdivisão ou aprofundamento proposto:** Ensinar que amostragem em parte do perfil não torna todas as leituras amostrais.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## 🧭 Diagnóstico não é Enforcement

**Função desta seção:** Definir enforcement e mostrar como uma política explícita consome o diagnóstico.

**Subdivisão ou aprofundamento proposto:** Comparar chamar e imprimir, registrar alerta e interromper execução; não criar job ou pipeline como efeito do tutorial.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

## ❓ Perguntas Frequentes (FAQ)

**Função desta seção:** Manter perguntas e dar exemplos concretos de retorno/erro/ação.

**Subdivisão ou aprofundamento proposto:** Acrescentar por que nem todo script tem status e por que pass não é aprovação para qualquer uso.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

### 1. Se o script retornar `status="fail"`, meus dados serão apagados ou modificados?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 2. Os scripts funcionam com tabelas do Unity Catalog?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 3. Preciso rodar esses scripts pelo terminal ou dentro de um notebook?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 4. Os scripts causam lentidão em tabelas volumosas?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 5. Posso usar os scripts em pipelines automatizados?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

### 6. A Genie Code executa estes scripts automaticamente?

**Molde da resposta:** {{resposta direta à pergunta}}. Em seguida, {{explicação do motivo}}, {{exemplo ou sinal observável}} e {{ação recomendada ou seção exata para continuar}}. Manter a pergunta; desenvolver a resposta sem remeter tudo a outro guia.

## 🔗 Continue Explorando

**Função desta seção:** Ligar a preparação de dados, interpretação e próximos testes.

**Subdivisão ou aprofundamento proposto:** A referência ao próximo documento deve explicar qual lacuna ele resolve.

**Espaço de desenvolvimento:** {{explicação em prosa}} · {{conceito definido}} · {{exemplo específico}} · {{o que o leitor consegue fazer depois}}.

---

## Orientações adicionais para desenvolver este README

### Subdivisões propostas, sem apagar as atuais

No exemplo principal: Preparação do conjunto, Critérios escolhidos, Chamada comentada, Retorno campo a campo e Decisão do consumidor. Dentro de cada utilitário, incluir “Quando não usar” e “Erros comuns”.

### Exemplo central obrigatório

20 registros, IDs únicos, uma coluna com 1 nulo: explicação de 5%, limiar inclusivo de alerta e score no contrato real. Contrastar com um RFV de quatro transações, que devolve DataFrame e não pass/warn/fail. Inserir tabela de entrada e saída para ambos.

O exemplo final deve conter pré-requisitos, local de uso, entrada completa, passos, chamada/pedido, resultado e interpretação. Código só é copiável quando os recursos e variáveis necessários foram apresentados. Acrescentar uma variação comentada para ensinar adaptação.

### Como integrar as figuras aprovadas

Manter catálogo, anatomia, panorama de retornos, veredito e camadas de política. O texto precisa explicar por que os retornos não são intercambiáveis.

As imagens ficam nos mesmos assets canônicos. Os caminhos devem ser calculados a partir do README final, não desta pasta de templates. Não inserir a informação essencial apenas no PNG.

### Conferência específica antes de apresentar a versão

- Todos os títulos e subtítulos acima foram preservados ou têm correção pontual justificada?
- Cada conceito usado nos procedimentos foi explicado antes?
- O exemplo central pode ser acompanhado sem adivinhar dados, paths ou etapas?
- O resultado é interpretado, e não apenas exibido?
- Cada recomendação técnica foi conferida no código e, para recursos da plataforma, na documentação oficial vigente?
- Não há códigos de decisões, história de migração, promessas em segundos/minutos ou capacidades inventadas?
- As notas ao autor e placeholders foram removidos da versão pronta?

**Critério final:** Escolher o script correto, fornecer entrada válida, interpretar seu retorno específico e separar diagnóstico de decisão operacional. A versão precisa demonstrar esse aprendizado; quantidade de texto sozinha não é aceite.

