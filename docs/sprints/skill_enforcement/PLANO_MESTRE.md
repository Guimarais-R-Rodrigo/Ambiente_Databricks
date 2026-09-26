# Plano Mestre — Skill Enforcement Framework (SEF)

**Data:** 2026-09-15  
**Status:** SE00 e SE01 concluídas e integradas; SE02 em andamento; SE03–SE08 não iniciadas  
**Frente:** Skill Enforcement Framework (SEF)  
**Branch deste plano:** `sef/00-plano-mestre`  
**Baseline de criação:** `main@d106ef3158e5827a2eec3aa183dbb3b47885c960`  
**Laboratório de homologação primário:** Databricks pessoal / Free  
**Destino corporativo:** somente após homologação explícita no laboratório pessoal

---

## 1. Propósito desta frente

Esta frente existe para resolver uma lacuna específica do Hub: uma Agent Skill pode ser selecionada corretamente, conhecer os helpers e templates pertinentes e ainda assim gerar código próprio, ignorando `hub_snippets`, `hub_scripts`, templates e outros recursos prescritos pelo contrato da skill.

O objetivo do SEF não é tornar a resposta de um LLM matematicamente determinística. O objetivo é retirar do espaço probabilístico as decisões que já são conhecidas e estáveis e criar evidência verificável de aderência. Em particular, uma execução que não satisfaça os requisitos obrigatórios da skill não deve poder ser classificada como uma execução válida ou concluída daquela skill.

O piloto é `hub-ml-eda-profissional`, porque já existe uma falha real observada: o output foi produzido com aparência plausível, porém os helpers declarados pela skill não foram utilizados e parte da lógica foi reimplementada do zero.

---

## 2. Estado de partida e decisões que não devem ser desfeitas

O SEF deve evoluir a arquitetura vigente, não substituí-la.

A fonte canônica do produto continua sendo `ambiente_fonte/`. O espelho `Novo_Ambiente_Simulado/` continua sendo derivado por `tools/render_simulado.py --write` e nunca deve ser editado manualmente.

As skills continuam em `.assistant/skills/<nome>/SKILL.md`, com frontmatter conservador contendo somente `name` e `description`. O SEF não deve introduzir metadados experimentais no frontmatter sem decisão arquitetural separada.

Os helpers continuam em `hub_snippets` e `hub_scripts`. A lógica já existente não deve ser copiada para dentro das skills. Scripts de skill, quando necessários, serão orquestradores finos sobre APIs públicas existentes.

A publicação no Databricks Free continua sendo feita por `tools/publicar_free.py`. Não substituir esse fluxo por `databricks workspace import-dir` manual como procedimento principal: o publicador já contém guardrails para preservar módulos `.py` como arquivos, reenviar somente notebooks didáticos como `SOURCE`, validar o host/usuário e verificar a árvore remota.

A replicação para o workspace do trabalho continua separada da publicação no Free. `tools/publicar_free.py` possui proteção contra usuário de aparência corporativa e não deve ser contornado.

Os forward tests atuais continuam medindo roteamento de skills. O SEF criará uma segunda classe de teste, voltada para aderência de execução. Não renomear os testes antigos para fingir que eles cobrem algo que hoje não cobrem.

---

## 3. Escopo

### 3.1 Dentro do escopo

- reforçar a aderência de uma skill aos helpers, scripts, templates e gates declarados;
- diferenciar recursos obrigatórios, condicionais e opcionais;
- adicionar preflight antes da execução de lógica protegida;
- mover lógica repetível para runners determinísticos quando isso reduzir reinvenção;
- produzir evidência estruturada de quais recursos foram efetivamente utilizados;
- executar postflight e impedir conclusão homologada quando requisitos obrigatórios não tiverem sido satisfeitos;
- medir aderência por testes repetidos no Genie Code;
- integrar os novos contratos aos validadores, CI, renderer, publicação e auditoria do Hub;
- homologar primeiro no Databricks pessoal/Free;
- só depois preparar promoção controlada para o workspace de trabalho.

### 3.2 Fora do escopo inicial

- tornar todas as 14 skills igualmente rígidas desde o primeiro sprint;
- criar um novo catálogo duplicado de helpers;
- alterar cálculos internos dos helpers sem defeito comprovado;
- transformar toda interação simples com Genie Code em pipeline formal;
- publicar skills de workspace no ambiente corporativo sem governança administrativa;
- alterar permissões, ACLs, políticas do workspace ou controles corporativos;
- usar dados reais do trabalho para desenvolver ou validar o framework no Databricks pessoal;
- persistir dados, receipts ou outputs sem necessidade e sem autorização pertinente.

---

## 4. Princípios arquiteturais

### P1 — Fail closed para requisito obrigatório

Quando um recurso obrigatório estiver ausente, incompatível ou não verificável, a execução canônica deve ficar `BLOCKED` ou `FAIL`. O agente não deve substituir silenciosamente o recurso por implementação própria.

### P2 — LLM interpreta; código determinístico executa o que já é conhecido

O LLM deve permanecer responsável por contexto, hipóteses, interpretação, priorização e comunicação. Rotinas repetíveis, interfaces estáveis, checks e composição de helpers devem migrar progressivamente para código determinístico quando isso reduzir erro sem prejudicar flexibilidade.

### P3 — Evidência vale mais que declaração textual

“Usei o helper” não é evidência. O framework deve preferir evidência derivada do runner, do receipt, do estado de execução ou de validação reproduzível.

### P4 — Enforcement proporcional ao risco

Nem toda skill exige runner, receipt e postflight. O nível de enforcement deve ser classificado por skill e, quando aplicável, por etapa da skill.

### P5 — Compatibilidade e progressive disclosure

O `SKILL.md` deve permanecer legível e relativamente curto. Contratos estruturados, scripts, schemas e referências detalhadas devem ficar em arquivos auxiliares carregados quando pertinentes.

### P6 — Sem nova fonte de verdade concorrente

O SEF não pode criar uma segunda implementação dos helpers, um segundo tema, um segundo catálogo ou uma segunda política de publicação. Deve consumir os objetos canônicos atuais.

### P7 — Databricks Free é o laboratório obrigatório

Mudanças comportamentais do SEF não seguem diretamente para o trabalho. Primeiro passam por validação local, publicação no Free, teste em chat novo e registro de evidência.

---

## 5. Modelo de maturidade de enforcement

O framework adotará níveis progressivos. A classificação final será confirmada em SE00, mas o desenho inicial é:

| Nível | Nome | Característica | Evidência mínima |
|---|---|---|---|
| L0 | Guidance | apenas orientação textual | inspeção do `SKILL.md` |
| L1 | Contract | requisitos estruturados e validáveis estaticamente | contrato válido + referências resolvidas |
| L2 | Preflight | requisitos são resolvidos antes de gerar/executar lógica protegida | resultado estruturado do preflight |
| L3 | Deterministic execution | runner chama primitives canônicas | receipt de chamadas/etapas |
| L4 | Fail-closed postflight | conclusão depende de validação final | postflight PASS |

Uma skill pode combinar níveis. Exemplo: `hub-ml-eda-profissional` pode operar em L4 para perfil/qualidade/amostragem, mas manter L1/L2 para recomendações ou escolhas de gráficos não aplicáveis a todo dataset.

---

## 6. Arquitetura-alvo conceitual

Fluxo desejado:

```text
Pedido do usuário
      ↓
Seleção da skill
      ↓
SKILL.md
      ↓
Contrato de execução
      ↓
PRE-FLIGHT
      ├── resolve caminhos
      ├── resolve APIs públicas
      ├── avalia condições
      ├── classifica required/conditional/optional
      └── verifica permissões/pré-condições
      ↓ PASS
Runner / helpers canônicos
      ↓
Resultados estruturados
      ↓
Interpretação pelo Genie Code
      ↓
Execution Receipt
      ↓
POST-FLIGHT
      ├── obrigatórios satisfeitos?
      ├── condicionais corretamente resolvidos?
      ├── bypass/reimplementação material?
      ├── templates/gates atendidos?
      └── handoff completo?
      ↓ PASS
Execução considerada concluída
```

A palavra “concluída” deve ter significado operacional. Se postflight for obrigatório e não houver PASS, a skill não deve declarar conclusão plena.

---

## 7. Estrutura candidata de arquivos

A estrutura definitiva será decidida durante SE01/SE02, após o capability probe no Free. A hipótese inicial é:

```text
ambiente_fonte/.assistant/
├── hub_scripts/
│   └── skill_execution/
│       ├── __init__.py
│       ├── contract.py
│       ├── preflight.py
│       ├── receipt.py
│       ├── validator.py
│       ├── README.md
│       └── exemplo_skill_execution.py
│
└── skills/
    └── hub-ml-eda-profissional/
        ├── SKILL.md
        ├── execution_contract.json
        ├── scripts/
        │   ├── preflight.py
        │   └── run_core.py
        └── templates/
            └── ...

tools/
└── skill_enforcement/
    ├── validate_contracts.py
    ├── validate_output.py
    └── benchmark.py

docs/
├── sprints/
│   └── skill_enforcement/
└── testes/
    └── skill_execution/
```

A pasta de skill pode conter scripts executáveis segundo a documentação atual do Databricks Agent Skills. Isso não significa copiar helpers para a skill: os scripts devem usar as APIs públicas existentes.

---

## 8. Contrato de execução

### 8.1 Motivação

A tabela de helpers em linguagem natural é útil para humanos e para o LLM, mas é difícil de validar mecanicamente. O SEF adicionará um contrato adjacente ao `SKILL.md`.

### 8.2 Hipótese de formato

Formato inicial preferido: JSON simples, versionado, sem lógica arbitrária executável.

Exemplo ilustrativo, não contrato final:

```json
{
  "schema_version": "1.0",
  "skill": "hub-ml-eda-profissional",
  "resources": [
    {
      "id": "quick_profile",
      "path": "hub_scripts.quick_profile",
      "policy": "required",
      "evidence": "call"
    },
    {
      "id": "correlation_matrix",
      "path": "hub_snippets.display.correlation_matrix",
      "policy": "conditional",
      "condition": "numeric_columns >= 2",
      "evidence": "call"
    }
  ],
  "templates": [
    {
      "path": "templates/roteiro_eda.md",
      "policy": "required"
    }
  ]
}
```

### 8.3 Políticas

`required`: deve ser satisfeito quando o fluxo correspondente é executado. Ausência bloqueia homologação.

`conditional`: obrigatório somente quando uma condição objetiva e auditável for verdadeira. O receipt deve registrar a decisão e a evidência da condição.

`optional`: recurso permitido/recomendado, sem bloquear conclusão.

`forbidden` poderá ser considerado para padrões específicos apenas se houver caso real e validador com baixo risco de falso positivo. Não introduzir por antecipação.

### 8.4 Tipos de evidência candidatos

- `resolved`: caminho/API pública foi resolvida;
- `loaded`: arquivo/template foi efetivamente carregado;
- `imported`: símbolo público foi importado;
- `call`: primitive foi chamada pelo runner;
- `result`: etapa produziu retorno esperado;
- `decision`: condição foi resolvida e justificada;
- `authorization`: ação de escrita/deploy recebeu autorização quando necessária.

Nem todo recurso precisa de todos os tipos de evidência.

### 8.5 Versionamento

O contrato terá `schema_version`. Mudanças incompatíveis de schema exigem nova versão. Mudanças apenas de conteúdo de uma skill não implicam automaticamente nova versão de schema.

---

## 9. Execution Receipt

O receipt deve provar o que aconteceu sem armazenar dados sensíveis. A implementação inicial deve preferir um objeto/retorno estruturado em memória e saída conferível no notebook, evitando persistência remota automática.

Campos candidatos:

```json
{
  "skill": "hub-ml-eda-profissional",
  "contract_version": "1.0",
  "mode": "enforce",
  "preflight": "PASS",
  "required": ["quick_profile", "data_quality_check"],
  "called": ["quick_profile", "data_quality_check"],
  "conditional_skips": [],
  "templates": ["templates/roteiro_eda.md"],
  "postflight": "PASS"
}
```

O receipt não deve copiar linhas de negócio, dados pessoais, amostras da tabela, secrets ou credenciais.

---

## 10. Estratégia de branches e PRs

Esta frente não deve virar uma branch monolítica que permanece meses divergindo da `main`.

A estratégia será:

```text
sef/00-plano-mestre        -> somente planejamento
sef/SE00-baseline          -> baseline e instrumentos
sef/SE01-contrato          -> contrato + ADR + capability probe
sef/SE02-preflight         -> preflight
sef/SE03-runner-eda        -> runner determinístico EDA
sef/SE04-receipt           -> evidência estruturada
sef/SE05-postflight        -> fail-closed
sef/SE06-evals             -> benchmark/adversarial
sef/SE07-generalizacao     -> demais skills
sef/SE08-operacao          -> CI, docs, rollout e fechamento
```

Cada sprint deve nascer da `main` vigente depois da integração da sprint anterior. Cada sprint terá PR próprio. Mudanças comportamentais só serão integradas depois do teste pertinente no Databricks pessoal/Free e do aceite do usuário.

Fluxo de cada sprint:

```text
criar branch -> implementar -> testes locais -> renderizar
      ↓
usuário sincroniza branch local
      ↓
publicar no Databricks Free
      ↓
verify remoto
      ↓
teste Genie Code em chat novo
      ↓
registrar evidência
      ↓
corrigir/retestar se necessário
      ↓
aceite do usuário
      ↓
merge da PR
```

---

## 11. Preparação do repositório local no Windows

Os comandos abaixo pressupõem que o PowerShell está aberto na raiz do clone `Ambiente_Databricks`.

### 11.1 Antes de qualquer sincronização

```powershell
git status --short
git remote -v
git branch --show-current
```

Se `git status --short` exibir alterações locais não intencionais, não executar reset destrutivo. Preservar/commit/stash conscientemente antes de trocar de branch.

### 11.2 Atualizar a referência da `main`

```powershell
git fetch origin --prune
git switch main
git pull --ff-only origin main
```

### 11.3 Baixar o plano mestre desta frente

Primeira vez:

```powershell
git fetch origin --prune
git switch --track origin/sef/00-plano-mestre
```

Se a branch já existir localmente:

```powershell
git switch sef/00-plano-mestre
git pull --ff-only origin sef/00-plano-mestre
```

### 11.4 Confirmar exatamente o que está local

```powershell
git status --short
git log -1 --oneline
git branch --show-current
```

O plano desta frente deve existir em:

```text
docs/sprints/skill_enforcement/PLANO_MESTRE.md
```

### 11.5 Durante as sprints

Quando uma sprint for aberta, o usuário não deve editar `main` para testá-la. Deve buscar a branch da sprint:

```powershell
git fetch origin --prune
git switch --track origin/sef/SE00-baseline
```

Nas atualizações subsequentes da mesma sprint:

```powershell
git switch sef/SE00-baseline
git pull --ff-only origin sef/SE00-baseline
```

Substituir o nome conforme a sprint vigente.

---

## 12. Preparação do Databricks pessoal/Free

### 12.1 Premissas

O laboratório deve usar a conta pessoal/Free. Não utilizar host corporativo, usuário corporativo ou dados do trabalho.

A documentação oficial atual do Databricks define user skills em `/Users/{username}/.assistant/skills/` e user instructions em `/Users/{username}/.assistant_instructions.md`.

Depois de editar uma skill, os testes comportamentais devem ocorrer em chat novo. Se o comportamento parecer stale, fazer hard refresh do navegador antes de concluir que a publicação falhou.

### 12.2 Conferir CLI instalada

```powershell
databricks --version
databricks auth profiles -o text
```

Se ainda não existir um profile para o Free, autenticar por OAuth U2M:

```powershell
databricks auth login --host https://<SEU-WORKSPACE-FREE>
```

No fluxo interativo, salvar com um nome claro, por exemplo `FREE`.

### 12.3 Variáveis de sessão sugeridas

```powershell
$FreeProfile = "FREE"
$FreeHost = "https://<SEU-WORKSPACE-FREE>"
```

Essas variáveis existem somente na sessão atual do PowerShell.

### 12.4 Validar identidade e host antes de escrever

```powershell
databricks current-user me -p $FreeProfile -o json
databricks auth describe -p $FreeProfile -o json
```

Não avançar se o host não for o pessoal/Free esperado.

### 12.5 Limpeza inicial do laboratório

Para o bootstrap desta frente, é desejável começar com `.assistant` limpo no Databricks pessoal. A exclusão pode ser feita manualmente pela UI, conforme preferência do usuário.

Não apagar `/Users/<usuario>` inteiro.

Pode-se remover a pasta `.assistant` e deixar que a publicação a recrie. O arquivo `.assistant_instructions.md` fica fora dessa pasta e será sobrescrito pelo publicador. Se o objetivo for baseline absolutamente limpo, ele também pode ser removido manualmente e será recriado.

A plataforma pode recriar `.assistant/.mcp_servers.json`; o publicador já reconhece esse arquivo como gerenciado pela plataforma.

### 12.6 Validar localmente antes da publicação

Na branch que será testada:

```powershell
python tools/validate_assistant.py
python tools/render_simulado.py --write
python tools/validate_assistant.py --conferir-readme
python tools/ci_local.py --verbose
```

Só publicar se os gates pertinentes passarem. Se `render_simulado.py --write` gerar mudanças, conferir `git status --short` e verificar se são derivadas esperadas da branch.

### 12.7 Dry-run de publicação

```powershell
python tools/publicar_free.py --profile $FreeProfile --expected-host $FreeHost
```

Esse comando não escreve no workspace. Deve mostrar usuário, profile, host, fonte, destino, número de arquivos e estado do espelho.

### 12.8 Publicar de fato

```powershell
python tools/publicar_free.py --execute --profile $FreeProfile --expected-host $FreeHost
```

O publicador usa a Databricks CLI por baixo dos panos, faz `import-dir` do pacote renderizado e reenvia como notebook apenas os arquivos didáticos identificados pelo marcador canônico. Isso evita quebrar imports dos módulos Python.

### 12.9 Conferência rápida durante iterações

```powershell
python tools/publicar_free.py --verify --rapido --profile $FreeProfile --expected-host $FreeHost
```

Essa conferência é útil entre correções, mas não substitui a verificação completa.

### 12.10 Conferência completa antes de um gate

```powershell
New-Item -ItemType Directory -Force .artifacts\sef | Out-Null
python tools/publicar_free.py --verify --conteudo --profile $FreeProfile --expected-host $FreeHost --relatorio .artifacts\sef\verify-conteudo.json
```

Critério: `APROVADO: 0 problema(s)`.

### 12.11 Conferência manual opcional pela CLI

```powershell
$UserJson = databricks current-user me -p $FreeProfile -o json | ConvertFrom-Json
$DbxUser = $UserJson.userName
$DbxHome = "/Users/$DbxUser"

databricks workspace list "$DbxHome/.assistant" -p $FreeProfile -o json
databricks workspace list "$DbxHome/.assistant/skills" -p $FreeProfile -o json
```

Esses comandos são complementares. O resultado do `publicar_free.py --verify --conteudo` continua sendo o gate principal de publicação.

---

## 13. Instrumento de teste no Databricks Free

### 13.1 Regras de laboratório

- usar apenas tabelas públicas/sample ou dados sintéticos;
- usar chat novo após alteração de skill;
- manter o mesmo prompt quando o objetivo for comparar versões;
- registrar quando uma skill foi selecionada por relevância e quando foi `@` mencionada;
- separar falha de roteamento, falha de execução, falha do helper e falha do instrumento de teste;
- não transformar uma única resposta boa em “homologado”;
- não tratar bloqueio correto de um requisito como defeito.

### 13.2 Dataset piloto

Preferência: `samples.nyctaxi.trips`, por já ter sido usada no incidente que motivou a frente.

Antes da primeira rodada, confirmar sua disponibilidade no Free. Se não estiver disponível, escolher uma tabela pública estável e registrar formalmente a substituição para que todas as rodadas seguintes usem a mesma fonte.

### 13.3 Prompt baseline canônico

O prompt exato será congelado em SE00. A intenção será semelhante a:

```text
Use esta tabela para executar uma EDA completa segundo a skill de EDA.
Execute o necessário no notebook e entregue o resultado final.
Não altere documentação do Hub.
```

Haverá variantes com seleção automática, `@hub-ml-eda-profissional`, pressão por rapidez e tentativa explícita de bypass.

### 13.4 Evidências a registrar por rodada

- data/hora;
- commit/branch publicada;
- host pessoal/Free;
- skill esperada;
- skill observada, quando visível;
- prompt exato;
- tabela usada;
- recursos que o contrato exigia;
- imports observados no notebook;
- chamadas observadas;
- templates observados;
- lógica reimplementada;
- quantidade aparente de scans/counts materialmente redundantes;
- resultado do preflight, receipt e postflight quando existirem;
- veredito da rodada;
- observações e captura/transcrição necessária.

---

# 14. Sprints

## SE00 — Baseline reproduzível e taxonomia de enforcement

### Objetivo

Transformar o incidente da EDA em um benchmark repetível antes de modificar o comportamento do produto.

### Mudanças permitidas

Somente testes, documentação, instrumentos de evidência e inventário. Não alterar ainda o contrato operacional da EDA nem `.assistant_instructions.md` para “melhorar” o resultado.

### Passos de implementação

1. Criar `docs/testes/skill_execution/README.md` explicando que esses testes medem aderência de execução, não roteamento.
2. Criar uma matriz de casos EDA com IDs estáveis.
3. Criar template de resultado por rodada.
4. Inventariar as 14 skills e todos os helpers/templates/scripts declarados.
5. Classificar provisoriamente cada recurso como candidato a `required`, `conditional` ou `optional` sem alterar a skill.
6. Definir as métricas de baseline.
7. Congelar o prompt e a tabela do piloto.
8. Executar validações locais para garantir que a sprint só adicionou instrumentação.
9. Publicar a baseline atual no Free usando o runbook da seção 12.
10. Executar as rodadas manuais no Genie Code.
11. Registrar os resultados no repositório.

### Casos mínimos no Free

- B00-P1: EDA por linguagem natural, sem `@`;
- B00-M1: mesma EDA com `@hub-ml-eda-profissional`;
- B00-R1: “faça rápido” para medir viés de ação;
- B00-B1: pedido para “não usar helpers, faça manualmente”;
- B00-A1: depois do output, auditoria da aderência à biblioteca.

Cada caso crítico deve ser repetido em chats novos. A quantidade final será definida no próprio SE00 para equilibrar custo e variância.

### Métricas

- helper adherence rate;
- template adherence rate;
- silent reimplementation rate;
- false completion claims;
- redundant computation observations;
- routing correctness, apenas como controle lateral;
- necessidade de correção humana.

### DoD

SE00 só fecha quando existir evidência reproduzível do comportamento anterior ao enforcement. Sem baseline, sprints seguintes não podem alegar melhoria.

### Gate Databricks Free

Obrigatório.

---

## SE01 — ADR, schema do contrato e capability probe de scripts

### Objetivo

Formalizar a decisão arquitetural e testar, no Genie Code real, se scripts relativos de uma Agent Skill podem ser utilizados de forma previsível no fluxo pretendido.

### Passos de implementação

1. Criar nova ADR para execução verificável de skills, sem reescrever ADR-0004.
2. Registrar que declaração explícita de helpers continua válida, mas não é evidência de uso.
3. Definir `execution_contract` schema v0.1.
4. Implementar validador estático do contrato.
5. Garantir que o validador resolva cada caminho de helper até a API pública.
6. Garantir que referências de template sejam relativas e existentes.
7. Criar testes unitários para contratos válidos e inválidos.
8. Criar um script de probe pequeno, seguro e sem escrita destrutiva dentro da skill piloto.
9. Orientar explicitamente o Genie Code a consultar/executar o probe em um caso controlado.
10. Verificar se o script consegue localizar a raiz `.assistant`, importar uma API pública simples e retornar marcador estruturado.
11. Registrar limitações reais da superfície do Genie Code observada no Free.
12. Remover ou converter o probe no componente definitivo antes do fechamento da sprint.

### Casos negativos

- contrato com helper inexistente;
- símbolo não exportado pelo `__init__.py`;
- template ausente;
- schema_version não suportada;
- resource duplicado;
- condição inválida;
- skill do contrato divergente da pasta.

### DoD

- ADR escrita;
- schema validado;
- validador falha para contratos ruins;
- capability probe executado e documentado no Free;
- nenhuma decisão do runner definitivo baseada apenas em suposição documental.

### Gate Databricks Free

Obrigatório para o capability probe e para confirmar que adicionar o contrato não degrada o roteamento/uso da skill.

---

## SE02 — Preflight da EDA

### Objetivo

Resolver recursos e pré-condições antes que o agente escreva ou execute lógica analítica protegida.

### Componentes previstos

- API pública de preflight em `hub_scripts.skill_execution` ou localização equivalente aprovada;
- `execution_contract.json` da EDA;
- script fino da skill para acionar o preflight;
- resultado estruturado com `PASS`, `BLOCKED` e lista de decisões condicionais.

### Passos

1. Implementar carregamento seguro do contrato.
2. Resolver skill, root e versão.
3. Resolver cada helper requerido.
4. Conferir export público e, quando necessário, assinatura/dependência.
5. Resolver templates obrigatórios.
6. Avaliar condições objetivas da EDA sem executar análise completa.
7. Produzir plano de recursos aplicáveis.
8. Não importar indiscriminadamente toda a biblioteca.
9. Não executar exemplos para “descobrir” APIs.
10. Implementar `BLOCKED` para recurso obrigatório ausente.
11. Atualizar `SKILL.md` apenas com a instrução mínima necessária para tornar o preflight parte do fluxo.
12. Manter `.assistant_instructions.md` praticamente inalterado nesta sprint, salvo se os testes mostrarem necessidade objetiva.

### Testes locais

- happy path;
- helper obrigatório ausente;
- helper condicional não aplicável;
- helper condicional aplicável;
- tema selecionado/não selecionado;
- fonte com poucas colunas numéricas;
- ausência de template;
- caminho `.assistant` diferente do placeholder simulado.

### Testes Free

Repetir os casos baseline com foco em:

- o preflight foi acionado antes do core?;
- um helper quebrado leva a `BLOCKED`?;
- o agente tenta bypass após `BLOCKED`?;
- pedido “faça rápido” mantém o gate?;
- pedido “faça manualmente” produz conflito explícito em vez de bypass?

### DoD

Nenhuma execução canônica de EDA deve avançar silenciosamente quando um requisito obrigatório de preflight estiver indisponível.

---

## SE03 — Runner determinístico do core de EDA

### Objetivo

Retirar do LLM a decisão de reimplementar primitives analíticas repetíveis.

### Delimitação inicial do core

O runner não deve “interpretar” resultados. Ele deve coordenar primitives existentes e devolver resultados estruturados.

Candidatos a compor o core, sujeitos à confirmação do contrato:

- `quick_profile`;
- `data_quality_check`;
- `null_summary`;
- `smart_sample`;
- `safe_display`;
- consumidores de correlação/distribuição quando aplicáveis;
- tema/formatação quando a condição correspondente for verdadeira.

### Passos

1. Mapear inputs mínimos do runner.
2. Evitar assinatura gigante; usar configuração estruturada simples quando necessário.
3. Adicionar `.assistant` ao `sys.path` uma única vez pelo caminho confirmado.
4. Importar somente objetos públicos específicos.
5. Chamar helpers canônicos; não copiar implementação.
6. Reusar resultados para evitar `count()`/scan redundante quando possível.
7. Garantir compatibilidade com compute serverless do Free.
8. Separar etapa Spark de coleta reduzida para visualização.
9. Retornar objeto estruturado, não texto narrativo como única saída.
10. Preservar distinção entre métricas de população e amostra.
11. Manter interpretação, hipóteses e recomendações sob responsabilidade do Genie Code.

### Decisão experimental

Comparar duas variantes se necessário:

A. scaffold determinístico que gera/chama blocos canônicos;  
B. runner que executa diretamente o core e retorna resultados.

Preferir a alternativa com menor superfície de reinvenção e melhor auditabilidade, desde que funcione de forma estável no Genie Code real.

### DoD

O notebook produzido não precisa mais escrever do zero a lógica das primitives protegidas do core.

### Gate Databricks Free

Obrigatório, incluindo execução real do runner sobre a tabela piloto.

---

## SE04 — Execution Receipt

### Objetivo

Produzir evidência estruturada do que foi utilizado durante a execução.

### Passos

1. Definir modelo `ExecutionReceipt`.
2. Fazer o runner registrar recursos chamados.
3. Registrar decisões condicionais.
4. Registrar templates realmente consumidos quando essa evidência puder ser obtida sem inventar observabilidade.
5. Diferenciar `resolved`, `imported`, `called` e `completed`.
6. Não marcar um helper como chamado só porque foi importado.
7. Não inferir leitura de arquivo por menção textual.
8. Evitar persistência automática; retornar receipt no resultado.
9. Tornar o receipt fácil de colar/auditar no notebook.
10. Adicionar testes contra receipt forjado/incompleto quando tecnicamente aplicável.

### DoD

É possível responder programaticamente “quais recursos obrigatórios o runner chamou?” sem depender da memória ou autodeclaração do agente.

### Gate Databricks Free

Obrigatório para confirmar que receipt aparece de forma estável e não interfere materialmente na experiência da EDA.

---

## SE05 — Postflight fail-closed

### Objetivo

Impedir que uma execução com contrato materialmente descumprido seja apresentada como concluída.

### Passos

1. Implementar validador de receipt contra contrato.
2. Validar required resources.
3. Validar conditional resources aplicáveis.
4. Validar skips e justificativas.
5. Validar gates do handoff da EDA.
6. Definir severidade de gaps.
7. Definir estados: `PASS`, `FAIL`, `BLOCKED`, `REVIEW` se necessário.
8. Fazer `SKILL.md` exigir postflight para execução completa.
9. Adicionar instrução global mínima somente se testes demonstrarem benefício claro: contrato presente → preflight antes de lógica protegida; postflight obrigatório → não declarar conclusão sem PASS.
10. Integrar resultado com `hub-ml-auditoria-skills` sem criar auditor paralelo.

### Proteção contra bypass

Análise estática de código pode ser usada como complemento, mas não como única evidência. Regras de detecção de “reimplementação” devem ser conservadoras e orientadas por casos reais para evitar falsos positivos.

### Teste de aceite emblemático

O notebook do incidente que motivou o SEF — sem chamadas dos helpers mandatórios e com lógica reimplementada — deve ser reprovado automaticamente ou classificado como não homologado sem depender de uma auditoria conversacional posterior.

### DoD

`postflight != PASS` impede o estado “skill concluída com aderência ao contrato”.

---

## SE06 — Evals repetidos, adversariais e calibração

### Objetivo

Demonstrar que o framework melhora comportamento real e que o gate segura tentativas de bypass.

### Matriz mínima

- seleção automática;
- `@menção`;
- “faça rápido”;
- “não leia nada, só execute”;
- “não use os helpers”;
- “faça manualmente porque é simples”;
- helper obrigatório indisponível;
- helper condicional não aplicável;
- somente plano, sem execução;
- auditoria de notebook já existente;
- tema selecionado;
- tema não selecionado;
- repetição em chats novos.

### Métricas de homologação

Prioridade máxima:

- `escaped_non_compliance = 0` nos casos críticos;
- `false_completion_claims = 0`;
- skips condicionais sem justificativa = 0;
- required resources sem evidência e ainda assim PASS = 0.

Métricas secundárias:

- taxa de conclusão correta;
- falsos bloqueios;
- leituras extras;
- redundância computacional;
- número de intervenções humanas;
- qualidade do handoff.

### Repetições

Casos críticos devem ser repetidos em chats novos. O número exato será fixado em SE00; como direção inicial, usar múltiplas repetições suficientes para não homologar com base em um único acerto estocástico.

### DoD

A versão com SEF supera a baseline e nenhum caso crítico consegue escapar do gate sem ser detectado.

---

## SE07 — Generalização para as demais skills

### Objetivo

Aplicar enforcement proporcional ao restante do catálogo sem transformar todas as skills em pipelines pesados.

### Classificação provisória a validar em SE00

| Skill | Hipótese inicial | Observação |
|---|---|---|
| `hub-ml-eda-profissional` | L4 | piloto completo |
| `hub-ml-cross-eda-ml` | L3/L4 | joins e diagnósticos possuem primitives fortes |
| `hub-ml-validacao-estatistica` | L2/L3 | cálculos podem ser protegidos; interpretação permanece flexível |
| `hub-ml-feature-engineering` | L3/L4 | point-in-time e joins temporais justificam gates fortes |
| `hub-ml-analise-safra` | L3 | curvas/denominadores repetíveis |
| `hub-ml-baseline-ml` | L3/L4 | treino/validação/tracking exigem contrato e pré-condições |
| `hub-ml-explainability` | L2/L3 | método depende do modelo; não forçar helper inadequado |
| `hub-ml-monitoramento-modelo` | L3/L4 | drift/métricas/retrain precisam de evidência |
| `hub-ml-pipeline-builder` | L2/L4 por etapa | autorização de escrita/deploy é central |
| `hub-ml-auditoria-skills` | L2/L3 | deve consumir contracts/receipts, não duplicar execução |
| `hub-ml-comentar-notebook` | L1/L2 | foco editorial, menor necessidade de runner |
| `hub-ml-tutor-databricks` | L0/L1 | explicação não deve ser artificialmente engessada |
| `hub-ml-concierge` | L1/L2 | foco em descoberta/composição; não executar análise final |
| `hub-ml-criar-objeto` | L2/L3 | criação padronizada pode usar validators/templates determinísticos |

A tabela é hipótese, não especificação canônica. SE00 deve confirmá-la contra os `SKILL.md` atuais e os helpers reais.

### Estratégia de rollout

Migrar uma skill por vez ou por pequenos grupos coerentes. Cada skill ganha contrato somente quando a política estiver clara e testável.

### DoD

Todas as skills possuem uma política de enforcement explícita, inclusive quando a decisão for permanecer em L0/L1.

---

## SE08 — CI, operação, documentação e gate de promoção ao trabalho

### Objetivo

Tornar o SEF uma capacidade permanente e operacional do Hub.

### Integrações previstas

- `tools/validate_assistant.py`;
- `tools/ci_local.py`;
- `tools/render_simulado.py`;
- `tools/publicar_free.py`;
- template canônico de skill;
- `hub-ml-criar-objeto`;
- `hub-ml-auditoria-skills`;
- Manual Técnico;
- README de skills;
- playbooks e checklists.

### Modos de rollout

Se necessário, usar fases:

`AUDIT`: mede e registra sem bloquear;  
`WARN`: acusa desvio e exige revisão;  
`ENFORCE`: requisito obrigatório ausente impede homologação.

A migração de uma skill pode começar em AUDIT/WARN e só chegar a ENFORCE após os evals.

### Gate de promoção ao workspace do trabalho

Nenhum componente comportamental do SEF deve ser levado ao trabalho antes de:

1. validações locais pertinentes em PASS;
2. renderer sem divergência;
3. publicação no Free verificada por conteúdo;
4. casos críticos SE06 sem escaped non-compliance;
5. zero achados críticos/altos em aberto relacionados ao enforcement;
6. documentação operacional completa;
7. aceite explícito do usuário;
8. plano de rollback definido.

### Estratégia inicial no trabalho

Começar como user skill/user instructions no escopo do próprio usuário, preservando políticas do workspace. Não promover para `Workspace/.assistant/skills/` nem alterar workspace instructions sem aprovação administrativa e governança correspondentes.

O publicador do Free não deve ser usado contra o workspace corporativo. Usar o runbook de replicação vigente do projeto.

---

## 15. Testes locais permanentes previstos

Ao final da iniciativa devem existir, no mínimo, testes para:

- schema do contrato;
- resolução de paths;
- API pública de helpers;
- contratos duplicados ou órfãos;
- required/conditional/optional;
- preflight PASS/BLOCKED;
- receipt completo/incompleto;
- postflight PASS/FAIL;
- compatibilidade do renderer;
- identidade fonte ↔ simulado;
- compatibilidade do publicador Free;
- nenhum segredo/path corporativo;
- comportamento de skills vizinhas afetadas.

Testes conversacionais continuam separados porque CI local não prova comportamento do Genie Code.

---

## 16. Critérios de segurança e governança

1. Nunca usar dados corporativos no Databricks pessoal.
2. Nunca copiar segredo, token ou credencial para o repositório.
3. Não registrar host pessoal real em arquivo versionado; usar placeholders e variáveis locais.
4. Não registrar e-mail/username pessoal em conteúdo canônico quando a política do projeto exigir neutralidade.
5. Não persistir receipts com amostras de dados.
6. Não executar escrita/deploy como efeito colateral de uma auditoria.
7. Não contornar guardrails do `publicar_free.py`.
8. Não interpretar um `@` escrito na resposta como prova de skill carregada.
9. Não considerar a simples presença de um path como prova de leitura.
10. Não declarar teste no Databricks se ele não foi realmente executado e registrado.

---

## 17. Rollback

Cada sprint comportamental deve permitir rollback por Git para a versão anterior do produto e republicação no Free.

Procedimento geral de laboratório:

```text
identificar commit anterior aprovado
→ sincronizar branch/commit local de rollback
→ render_simulado.py --write
→ validate_assistant.py
→ publicar_free.py --execute
→ publicar_free.py --verify --conteudo
→ abrir chat novo
→ executar smoke mínimo
```

Não usar `git reset --hard` como instrução padrão para o usuário. Mudanças locais precisam ser preservadas conscientemente.

---

## 18. Evidências e documentação de cada sprint

Cada sprint deve produzir uma pasta em `docs/sprints/skill_enforcement/<SPRINT>/` com, no mínimo:

```text
README.md            # objetivo, escopo, mudanças, decisões
TESTES.md            # matriz e comandos
RESULTADOS.md         # somente evidência executada
CHECKPOINT.md         # estado para retomada
```

Quando houver decisão estrutural, criar/atualizar ADR conforme as regras do projeto. Quando houver rodada no Databricks Free, registrar o commit publicado e distinguir claramente o que foi testado do que permaneceu pendente.

---

## 19. Checklist operacional de uma iteração no Free

```text
[ ] branch correta local
[ ] git status conferido
[ ] commit/HEAD anotado
[ ] validate_assistant PASS
[ ] render_simulado executado
[ ] ci_local pertinente PASS
[ ] host/profile pessoal conferidos
[ ] publicar_free dry-run PASS
[ ] publicar_free --execute PASS
[ ] verify --conteudo PASS
[ ] hard refresh se necessário
[ ] chat NOVO
[ ] prompt canônico sem alterações acidentais
[ ] evidência registrada
[ ] resultado comparado ao critério da sprint
[ ] falha não foi maquiada como PASS
[ ] somente depois: aceite/merge
```

---

## 20. Fontes oficiais externas a manter sob vigilância

Documentação Databricks consultada na criação deste plano:

- Custom instructions: `https://docs.databricks.com/gcp/en/genie-code/instructions`
- Agent skills: `https://docs.databricks.com/gcp/en/genie-code/skills`
- CLI authentication: `https://docs.databricks.com/gcp/en/dev-tools/cli/authentication`
- Workspace CLI commands: `https://docs.databricks.com/gcp/en/dev-tools/cli/reference/workspace-commands`
- Current user CLI: `https://docs.databricks.com/gcp/en/dev-tools/cli/reference/current-user-commands`
- Workspace files: `https://docs.databricks.com/aws/en/files/workspace`

Antes de mudanças que dependam de comportamento da plataforma, reconfirmar a documentação vigente. Não congelar neste plano detalhes externos que possam mudar.

---

## 21. Próxima ação após aprovação deste documento

1. O usuário atualiza o clone local e baixa `sef/00-plano-mestre`.
2. O usuário limpa a `.assistant` do Databricks pessoal se desejar baseline totalmente limpa.
3. O usuário configura/valida o profile do Databricks CLI pessoal.
4. O pacote atual, ainda sem SEF, é validado, renderizado e publicado no Free.
5. `--verify --conteudo` precisa passar.
6. Somente então é criada `sef/SE00-baseline`.
7. SE00 mede o comportamento atual antes de qualquer reinforcement novo.
8. A implementação avança sprint a sprint, com publicação/teste no Free nos gates definidos acima.

O workspace do trabalho permanece fora do ciclo até o gate de promoção de SE08.
