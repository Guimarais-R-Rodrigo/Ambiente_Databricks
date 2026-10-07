<!-- Template: banco de analogias banking/CRM para explicações didáticas -->

# Banco de analogias — Banking, CRM, Finanças

Use estas analogias quando ajudarem o público informado a fixar um conceito técnico. São aproximações didáticas: não transferem autoridade, causalidade, certificação ou obrigações regulatórias.

## Conceitos Spark

| Conceito Spark/Delta | Analogia banking/CRM |
|----------------------|----------------------|
| Lazy evaluation | Esteira de aprovação de crédito: a análise só roda quando há decisão a tomar; até lá, só se acumulam requisitos. |
| Transformação vs. ação | Cadastrar etapas do pipeline regulatório (transformação) vs. emitir o relatório final (ação). |
| Particionamento | Carteira segmentada por agência/região; cada agência cuida do seu pedaço. |
| Shuffle | Redistribuição de carteiras entre gerentes — caro e demorado. |
| Broadcast join | Lista de feriados nacionais distribuída a toda agência; pequena, fica em todo lugar. |
| Sort merge join | Reconciliação de extratos de duas fontes que precisam ser ordenadas antes de cruzar. |
| Cache | Manter em memória os clientes da campanha do mês para consulta rápida durante o dia. |
| Window function | Rankear clientes por saldo dentro de cada segmento (`PARTITION BY segmento ORDER BY saldo`). |
| AQE | Ajuste dinâmico do plano da operação à medida que se descobre quem realmente compareceu. |
| Skew | Uma agência muito maior que as outras, gargalando o processamento. |

## Conceitos Delta Lake

| Conceito Delta | Analogia banking/CRM |
|----------------|----------------------|
| Time travel | Consultar a fotografia do cadastro no fechamento do mês passado. |
| Schema enforcement | Validação de campos obrigatórios na abertura de conta. |
| Schema evolution | Adicionar novo campo "renda recorrente" no cadastro sem quebrar o histórico. |
| MERGE | Conciliação cadastral: atualiza quem mudou, insere quem é novo, sinaliza quem saiu. |
| OPTIMIZE | Consolidação de ordens fragmentadas no fechamento. |
| Z-ORDER | Reorganizar a fila do banco por tipo de atendimento. |
| VACUUM | Descarte de documentos fora do prazo regulatório de retenção. |
| Change Data Feed | Diário de mudanças cadastrais para auditoria. |

## Conceitos MLflow / MLOps

| Conceito MLflow | Analogia banking/CRM |
|-----------------|----------------------|
| Experiment | Estudo de viabilidade de um novo produto. |
| Run | Cada simulação dentro do estudo, com parâmetros diferentes. |
| Registered model | Ficha de um modelo com versões registradas; registro não é homologação nem autorização de produção. |
| Alias / Stage | Rótulo de referência à versão segundo o mecanismo disponível; o rótulo não comprova aprovação ou execução. |
| Model serving | Esteira de scoring rodando 24/7. |
| Drift (PSI/CSI) | Mudança no perfil observado, como alteração no público que entra no funil; pede investigação, sem ordenar retreino. |
| Feature store | Repositório de features padronizadas, como um manual de produtos. |

## Conceitos Unity Catalog

| Conceito UC | Analogia banking/CRM |
|-------------|----------------------|
| Catalog | Diretoria do banco. |
| Schema | Departamento dentro da diretoria. |
| Table | Relatório oficial gerado pelo departamento. |
| Volume | Pasta física com documentos brutos do departamento. |
| Function | Rotina catalogada e reutilizável; catalogação não certifica correção nem elegibilidade. |
| Row filter / column mask | Quem pode ver quais clientes/dados, conforme política. |
| Lineage | Rastro de auditoria: quem usou aquele dado, quando, para quê. |

## Conceitos analíticos

| Conceito analítico | Analogia |
|--------------------|----------|
| Coorte / safra | Turma de clientes que entrou em janeiro vs. fevereiro. |
| Lift | Taxa de conversão da campanha vs. taxa orgânica. |
| Funil | Etapas da jornada: prospect → lead → cliente → ativo → engajado. |
| AUC | Capacidade do modelo de ordenar bons vs. maus pagadores. |
| KS | Maior distância entre as curvas de bons e maus na ordenação. |
| PSI | "Termômetro" da estabilidade da população do modelo. |
| CSI | PSI aplicado a uma variável específica (Characteristic Stability). |
| Swap rate | % de clientes que trocariam de classificação entre o modelo antigo e o novo. |

## Princípio de uso

- **Usar analogia quando o conceito for novo ou abstrato**.
- **Não forçar analogia** quando o conceito já é claro.
- **Manter precisão técnica** — analogia ilustra, não substitui a definição.

## Como adicionar novas analogias

Formato padrão para cada nova entrada:

| Conceito [categoria] | Analogia banking/CRM |
|----------------------|----------------------|
| [Nome do conceito] | [Analogia concisa: 1 a 2 linhas, conectando o conceito técnico a uma operação bancária ou de CRM reconhecível.] |

**Critérios para inclusão**:
- A analogia deve **iluminar**, não substituir a definição técnica.
- Preferir operações que o público informado reconhece no dia a dia (carteira, campanha,
  esteira de crédito, pipeline regulatório, jornada comercial, Private
  Banking, reconciliação, compliance).
- Se a analogia não ficar óbvia em 2 linhas, o conceito provavelmente não
  precisa de analogia — explique diretamente.
- Categorizar na seção correta (Spark, Delta, MLflow, UC, Analíticos) ou
  criar nova seção se o domínio for distinto.
- Evitar analogias genéricas que se aplicam a qualquer conceito (ex.:
  "é como um processo no banco" — vago demais).
