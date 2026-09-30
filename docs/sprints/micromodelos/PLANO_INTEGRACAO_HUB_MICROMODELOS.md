# Integração de Micromodelos ao Hub

**Atualização:** 2026-09-30. **Estado:** candidata revisada, validada localmente e publicada seletivamente no Free para análise; composição com a outra frente pendente.

**Checkpoint local:** commit `66e22192`, fonte e espelho do mesmo conteúdo. Gate local completo aprovado em checkout limpo: 12 etapas, incluindo validador com 0 falhas e 0 avisos, SE08, Micromodelos e aceite do pacote extraído. O exemplo de recência conferiu sete linhas sintéticas. O módulo `hub_micromodelos/` foi enviado pela CLI ao Free e teve readback de 25/25 arquivos, nenhum ausente/extra, Python como `FILE`, hash normalizado `457f0931ffd1978a9a15103fcb7d67d08b1e664aa7e30e199f9dfe0b6b4c240e`. Caches gerados pelo Python no primeiro envio foram removidos antes do readback final. Documentos compartilhados e a skill preexistente não foram sobrescritos no Free, pois a outra frente possui diferenças ainda não compostas. Esta publicação permite examinar o módulo e o exemplo; não representa a entrega conjunta ao trabalho.

**Checkpoint da revisão documental:** commit `25d30e7fe5880429eeaf232b50d6547b3d41eb9d`, com `guias/`, README de contrato e handoff no exemplo. Gate local completo aprovado em checkout limpo nas 12 etapas, validador 0 falhas/0 avisos. ZIP 01 com 610 arquivos de produto, manifesto SHA-256 `f8f9434f52821ca6f361947d11108236174d65a0e70e0ffab18d3d5c6708349e`; aceite do ZIP extraído passou nas dez etapas e o novo comando do caso de recência foi executado a partir desse ZIP. Envio seletivo do módulo ao Free e readback exato 28/28, sem arquivos ausentes ou extras, SHA-256 agregado `5b6fa7d2d1270d30ad688af4978a9a32c6352b0d7316360c7a184f6bbabeffb2`. Documentos compartilhados da outra frente não foram sobrescritos.

## Objetivo

Colocar o que já foi desenvolvido em `ambiente_fonte/.assistant/hub_micromodelos/`, seguindo os padrões atuais do Hub. Entregar o ambiente completo, consolidado com a outra frente, para testar no trabalho.

Este plano substitui a organização mais subdividida proposta anteriormente e a distribuição separada prevista no [plano de entrega local](PLANO_ENTREGA_LOCAL.md). O kit anterior conserva seus resultados de teste, mas a entrega final terá Micromodelos dentro do pacote do Hub.

### Completude e simplicidade

A orientação do responsável é simplificar a organização sem reduzir a entrega. Preservar todas as capacidades, pastas, atributos e conteúdos previstos na documentação vigente da frente. Recursos necessários, didáticos ou que concretizem boas práticas permanecem. Antes da migração, conferir o inventário dos READMEs e contratos e registrar, neste documento, onde cada item será entregue e como será demonstrado. Uma reorganização deve ter correspondência explícita entre origem e destino; retirar duplicação não pode eliminar conteúdo ou comportamento.

A árvore abaixo é uma proposta de navegação, não um limite de três pastas. Manter ou acrescentar divisões quando ajudarem a entender, usar ou manter o projeto. Evitar camadas sem finalidade concreta e documentação repetida. Itens históricos ou expressamente futuros continuam identificados como tais; funcionalidades prometidas para esta entrega devem existir e ser verificadas.

## Estrutura necessária

```text
.assistant/
├── hub_micromodelos/
│   ├── README.md
│   ├── __init__.py
│   ├── guias/
│   │   └── README.md
│   ├── contratos/
│   │   ├── README.md
│   │   ├── micromodelo.schema.json
│   │   └── micromodelo.template.yaml
│   ├── execucao/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── execucao.py
│   │   ├── exemplo_execucao.py
│   │   └── [módulos de apoio existentes]
│   └── exemplos/
│       ├── README.md
│       ├── migracao_simulada.py
│       └── recencia_contato/
│           ├── README.md
│           ├── micromodelo.yaml
│           ├── dados_sinteticos.json
│           ├── executar_exemplo.py
│           ├── conferir_entrega.py
│           └── resultado_esperado.json
└── skills/hub-ml-micromodelos/
```

A navegação agrupa jornada, contrato, execução e exemplos. `guias/` foi acrescentada após a avaliação do responsável porque a sequência e os limites de cada etapa não cabiam no resumo inicial. As funções já separadas em arquivos continuam separadas quando isso facilita a manutenção; cada arquivo de apoio não precisa virar uma pasta ou um objeto público independente. `execucao` segue o padrão existente de objeto do Hub, inclusive seu README e exemplo. `contratos/` ganhou um README para explicar estados e atributos condicionais.

Os exemplos utilizam dados sintéticos e deixam esse limite explícito. Testes de desenvolvimento continuam em `tools/tests/`. Projetos e dados reais permanecem no ambiente corporativo autorizado.

### Nomes em português

Usar português sem acentos nos novos nomes de arquivos e funções que forem realmente necessários. Para os módulos de apoio, usar `especificacao`, `assinatura`, `metadados`, `fluxo`, `artefatos`, `databricks`, `entrega` e `catalogo`, conforme a responsabilidade do código existente. Na documentação, explicar assinatura como o hash da especificação.

Preservar convenções do projeto e das ferramentas: `.assistant`, `hub_`, `skills`, `README.md`, `SKILL.md`, `__init__.py`, JSON Schema, MLflow e Databricks. Preservar também os campos dos contratos e as funções públicas existentes; traduzir essas interfaces só por estética geraria mudanças desnecessárias.

## O que será adaptado

### 1. Aproveitar a implementação existente

- Mover a implementação reutilizável de `tools/micromodelo_mm*.py` para `execucao/`, mantendo seu comportamento e aproveitando os testes existentes.
- Colocar schema e modelo YAML em `contratos/`; levar os exemplos de laboratório e os dados sintéticos necessários para `exemplos/`.
- Ajustar imports e caminhos para funcionar a partir da instalação `.assistant`, sem depender de `tools/` ou `docs/sprints/`.
- Manter um encaminhamento nos comandos antigos somente quando houver consumidor que precise dele. A implementação terá uma única fonte.
- Reutilizar o acompanhamento MLflow já existente no Hub e declarar as dependências pelo mecanismo de instalação atual. Importar o módulo não inicia serviços nem consultas.

Essa etapa aproveita o código existente e completa os recursos necessários à entrega e à demonstração. Acrescentar uma divisão ou recurso quando houver benefício concreto para uso, explicação ou manutenção; evitar mecanismos genéricos destinados apenas a necessidades hipotéticas.

### Micromodelo fictício completo para avaliação

Entregar um exemplo de **recência de contato**, com pessoas e contatos inteiramente sintéticos. Ele será a referência navegável para o responsável avaliar como o framework funciona, além dos testes automatizados.

- `micromodelo.yaml` preenchido conforme o contrato vigente: identidade e estado; negócio e usos vedados; entidade, grão e tempo de referência; fontes; evidências e contraevidências; classificação, ausência de evidência e limiares; score, escala, normalização, componentes e calibração; experimentos; validação; saídas; tracking; governança; publicação e proveniência, incluindo seus atributos internos.
- README com a explicação de cada atributo, valor escolhido, motivo e ponto em que é consumido. Conferir a cobertura com o schema completo, incluindo propriedades opcionais e condicionais, em vez de usar somente o template inicial como inventário.
- Dados e regras reproduzíveis que demonstrem TRUE, FALSE e INDETERMINADO, informação ausente e contraditória, limites temporais e cálculo do score. Explicar o score como força de evidência quando essa for a semântica adotada.
- Execução usando a biblioteca instalada no Hub, com resultado esperado conferível, assinatura da especificação, evidências de validação e exemplo de entrega/reconciliação. Explicar onde ficam os registros de execução e demonstrar a integração MLflow no ambiente em que for efetivamente testada.
- Campos condicionais incompatíveis entre si serão explicados e demonstrados em variantes sintéticas quando necessário. Usar `null` ou estado pendente apenas quando semanticamente correto, com motivo e condição para preenchimento; o exemplo não pode ser um template com lacunas sem explicação.
- Aprovações, publicação e referências institucionais serão explicitamente simuladas em exemplos documentais separados quando necessário. Não registrar aprovação fictícia como evidência real nem alterar o contrato para fazer uma simulação passar por homologação. Distinguir resultados calculados, medições realizadas e ilustrações.

O README principal e o Manual Técnico apontarão diretamente para esse exemplo. O roteiro de avaliação será: ler o caso → conferir os atributos → executar → comparar as saídas → alterar um parâmetro documentado e observar o efeito. Preservar as demais demonstrações úteis da frente.

### 2. Documentar no padrão do Hub

- **README de Micromodelos:** finalidade, estrutura, início de uso, exemplo e limites, seguindo o modelo de coleção existente.
- **README de execução:** entradas, saídas, uso e erros no modelo de objeto já adotado pelo projeto.
- **README de exemplos:** como executar a demonstração sintética e interpretar o resultado.
- **Manual Técnico:** seção integrada sobre Micromodelos, localização e uso; atualizar sumário e inventário e sincronizar a cópia da raiz.
- **README do Hub, skill e Concierge:** incluir os links e ajustar referências aos arquivos movidos. Os prompts permanecem nas pastas atuais.

Registrar a mudança de localização em uma ADR curta, conforme a regra do projeto, e atualizar os planos vivos que apontem para a organização anterior. Preservar registros históricos. Corrigir diagramas somente quando ficarem incorretos com a mudança; usar o padrão visual existente.

### 3. Incluir no transporte e na validação atuais

Acrescentar `hub_micromodelos` ao inventário de pastas geridas e ajustar os validadores existentes para reconhecer seus objetos e links. Alterar restrições de caminhos somente onde o uso real exigir, sem ampliar permissões da skill.

Usar o renderizador, gerador de pacote e roteiro de aceite que o Hub já possui. O pacote principal passa a conter contratos, código e exemplos de Micromodelos; o aceite passa a consumir essa instalação. A execução deixa de exigir o ZIP técnico separado. Ajustar o kit Free para usar a mesma fonte e incluir os testes afetados no CI existente.

### 4. Consolidar e conferir a entrega

Combinar as versões aceitas desta frente e da outra em uma área isolada, preservando alterações alheias. Conferir os arquivos compartilhados, especialmente instruções, policy, Manual e instalação, antes de gerar um único pacote do ambiente completo.

Validação necessária:

1. Rodar os testes existentes afetados pela movimentação e o validador do Hub.
2. Gerar o ambiente simulado pelo renderizador e conferir sua correspondência com a fonte.
3. Extrair o pacote fora do repositório e executar o exemplo sintético e o aceite existente a partir da instalação entregue. Manter as verificações atuais de integridade e dependências.
4. Conferir no Free o novo caminho de instalação e execução; repetir casos conversacionais apenas quando o roteamento ou contrato tiver mudado.
5. Fazer uma revisão separada da autoria, resolver os problemas encontrados e executar os gates exigidos do conjunto consolidado. Enviar ao CI em lote para economizar crédito.

Os resultados pertencem à versão efetivamente testada. A entrega local não comprova permissões, dados reais ou homologação no trabalho. A skill permanece L1/audit e as decisões corporativas já previstas continuam no [plano E2](PLANO_PREPARACAO_E2.md).

## Organização do trabalho

Começar pela mudança dos arquivos e definição dos caminhos. Depois, documentação pode avançar em paralelo aos ajustes de instalação e testes. Um agente pode cuidar de cada parte, com o integrador responsável pelos arquivos compartilhados e pela revisão final. Usar essa divisão apenas onde houver trabalho independente suficiente; não criar frentes ou relatórios adicionais só para preencher papéis.

## Conferência de cobertura após a revisão do responsável

| Item prometido | Destino atual | Estado e limite |
|---|---|---|
| Contrato MM01, template, estados, proveniência e fingerprint MM02 | `contratos/`; `execucao/especificacao.py`, `assinatura.py`; guia do contrato | Presente. O exemplo cobre os blocos do YAML e explica os condicionais que exigiriam aprovação ou medição. Não os preenche ficticiamente. |
| Dois modos conversacionais e descoberta MM03 metadata-only | `skills/hub-ml-micromodelos/`; `hub_prompts/`; `execucao/metadados.py`, `fluxo.py`, `databricks.py` | Presente. O adapter depende de sessão e binding autorizados; metadata não comprova SELECT nem viabilidade. |
| Artefatos de estudo e política de runs | `execucao/artefatos.py`; `hub_snippets/ml/mlflow_run`; guia de jornada | Presente. Scaffold é `NOT_RUN`. Runs E0/E1 do laboratório anterior estão nos relatórios; o novo caso de recência não foi executado em MLflow. |
| Piloto greenfield, classificação, score e indeterminado | `execucao/execucao.py`; `exemplos/recencia_contato/` | Presente em ensaios sintéticos distintos. Não há executor genérico que transforme qualquer YAML em scoring produtivo. |
| Exemplo preenchido, dados, resultado e handoff | `exemplos/recencia_contato/` | Sete casos, oráculo e `conferir_entrega.py` reproduzidos localmente. O handoff é rascunho com agregado `SUPPLIED_UNVERIFIED`. |
| Catálogo, impacto e migração conservadora | `execucao/catalogo.py`; `exemplos/migracao_simulada.py` | Presente como ensaio fictício. Migração real depende do piloto institucional e de equivalência medida. |
| Aprovação, publicação, visual/monitoramento e V1 | YAML e guia indicam autoridades e estados; plano E2 define portas | Não implementados como automação deste módulo. Dependem de governança e do ambiente corporativo; pastas vazias não trariam essas capacidades. |
| Manual, navegação, pacote e aceite | README do módulo, `guias/`, `contratos/`, `execucao/`, `exemplos/`, Manual; pacote ZIP 01 e aceite ZIP 02 | Revisão validada, pacote extraído conferido e readback Free 28/28 no commit de produto acima. |

**Concluído localmente quando:** Micromodelos estiver na pasta do Hub, com os itens acima presentes e documentados, funcionando pelo pacote extraído; o exemplo tiver resultados e rascunho de entrega reproduzidos; e os gates da versão exata estiverem registrados. Esses critérios foram cumpridos para a candidata de produto `25d30e7f`. **Próxima ação operacional:** revisão do responsável no Free e composição posterior com a outra frente antes de transportar o ambiente inteiro. O teste institucional continua separado.
