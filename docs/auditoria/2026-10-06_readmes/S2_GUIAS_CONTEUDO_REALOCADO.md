# Guias e padrões: conteúdo anterior realocado

Baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`. Excertos anteriores para auditoria; não são contratos de uso atuais. Links relativos foram fixados ao snapshot.

## R0066 · ambiente_fonte/.assistant/README.md

### 🎨 Sistema de Temas — V00–V07 integradas no Git

O Sistema de Temas possui um núcleo validado (`ResolvedTheme`), adaptadores opt-in para Plotly e HTML, Visual Lab de autoria em notebook, geração editorial orientada por tema e consumidores runtime integrados em `display`/`ml`. **Nada disso troca automaticamente o padrão da equipe nem publica um tema.**

Para autoria e comparação, comece pelo [Visual Lab](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md). Para contrato, tokens, primeiro uso e limites, consulte o [padrão de identidade visual](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md). Para um consumidor concreto, abra o README local e use a rota `_resolvido` quando ela existir.

A V07 integrou, entre outros, correlação, distribuições, curvas de ML, timeline de monitoramento, UMAP e safras. `dataframe_styled` já era coberto pela V04. SHAP/Matplotlib e Kaplan–Meier permanecem exceções explícitas ao theming atual; selecionar um tema não autoriza afirmar que seus plots foram recoloridos.

Integração Git não equivale a publicação no workspace, aprovação visual, acessibilidade, ACL real ou UAT. A V08 organiza transversalmente essas orientações em skills, padrões e Manual sem criar uma segunda fonte de verdade.

## R0066 · ambiente_fonte/.assistant/README.md

## Entender um objeto antes de executar

Nos objetos já documentados, comece pelo `README.md` da própria pasta. Ele
explica conceito, escolha e limites, e aponta para o notebook. A migração é
gradual; o [Manual](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/MANUAL_TECNICO.md#readmes-objeto) mantém a visão integrada.
A inclusão do guia não instala dependências nem executa código.

## R0073 · ambiente_fonte/.assistant/hub_padroes/README.md

## Sistema de Temas

O [padrão de identidade visual](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/identidade_visual/README.md) é o contrato transversal; não é um sétimo tipo de objeto. `ResolvedTheme` é a representação validada. V03/V04 integram consumidores Plotly/HTML, V05 fornece o Visual Lab opt-in, V06 conecta geração editorial e V07 amplia os consumidores runtime e formatos exercitados.

Templates e skills podem orientar composição, mas não redeclaram tokens ou paletas. Para um objeto visual configurável novo, use o contrato central e a rota `_resolvido` aplicável. Não há tema global automático, migração silenciosa de notebooks ou publicação implícita.

## R0073 · ambiente_fonte/.assistant/hub_padroes/README.md

## README de objeto — contrato vigente 1.0.0

O template genérico `readme/template.md` atende guias agregadores. Para pastas
operacionais de snippet, script ou prompt, use o
[molde de objeto](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) e o
[checklist editorial](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md). A transição terminou com
75/75 objetos operacionais, 3/3 exemplares e zero pendências.

Todo novo objeto desses três tipos deve nascer com README local no mesmo
contrato. O guia explica conceito, adequação, requisitos, efeitos e
interpretação; código, fachada ou briefing continuam definindo o comportamento
técnico. Não reabra dispensas nem replique o catálogo integrado do Manual.

## R0077 · ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/README.md

No formulário, ela informa a tabela confirmada, o período da campanha e `5000`
como orçamento de contatos. O resultado desejado é uma priorização justificada,
com limites explícitos. Não há aqui uma resposta simulada da IA apresentada
como captura real, nem indicação de que alguma tabela foi consultada nesta R01.

## R0077 · ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/README.md

R01: leitura estática e revisão pelo próprio autor. Não houve envio do prompt
à Genie Code, acesso a dados, geração de resposta observada nem teste de
roteamento. Auditoria independente e aceite humano estão pendentes.

## R0078 · ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/README.md

**`pct_nulo_alerta` aparece nos padrões, mas não é usado para decidir os alertas.**
Qualquer quantidade de respostas nulas gera `fail` no código atual, mesmo
mudando aquele valor. Essa limitação foi registrada na R01, sem alteração da
implementação. O argumento `limites` também não valida nomes desconhecidos
ou todos os tipos/intervalos recebidos.

## R0078 · ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/README.md

R01: leitura estática e revisão do próprio autor; PySpark não estava instalado
nesta sessão local. Nenhuma tabela foi acessada, criada ou removida e nenhum
teste de workspace foi realizado. Revisão independente e aceite humano estão
pendentes; as limitações foram documentadas, não corrigidas silenciosamente.

## R0079 · ambiente_fonte/.assistant/hub_padroes/skill_enforcement/README.md

A SE07 começou com 14/14 skills. A reconciliação posterior de Micromodelos
amplia o catálogo corrente para 15/15 com L1 estático; o baseline histórico
permanece registrado na campanha SE07. Migração de uma skill para L1–L4 só ocorre quando os artefatos correspondentes existem e os testes pertinentes passam.

## Operação permanente a partir da SE08

A policy deixa de ser apenas artefato da sprint SE07 e passa a integrar os gates
permanentes do Hub:

- o validador geral confere contratos e policy contra a mesma raiz analisada;
- o gate local usa o perfil cumulativo SE08 em modo parcial/read-only;
- a certificação FULL SE08 inclui regressões anteriores, policy, I/O, renderer,
  diff do derivado e snapshot documental;
- publicação/verify no Free e comportamento do Genie Code continuam evidências
  separadas, nunca inferidas do gate local.

A promoção para o workspace do trabalho exige gate próprio. Ela não é autorizada
por `target_level`, por uma rodada verde de CI ou pelo aceite humano de uma
dívida histórica. O publicador do Free continua proibido como rota de escrita no
workspace corporativo.

## R0079 · ambiente_fonte/.assistant/hub_padroes/skill_enforcement/README.md

## Dívida da auditoria

A política da `hub-ml-auditoria-skills` carrega explicitamente os achados da SE06:

- `AUDIT_FALSE_REASSURANCE`;
- `AUDIT_STATE_LADDER`;
- `AUDIT_CONDITIONAL_APPLICABILITY`.

A auditoria não pode chamar de “reverificado” um PASS apenas persistido no notebook.

## R0080 · ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md

Com o mínimo padrão de 100 contatos, a marca `decidivel` seria verdadeira no
primeiro grupo e falsa no segundo. Esse é um exemplo aritmético e uma leitura
da condição implementada, **não uma transcrição de execução PySpark nesta
sprint**. O próximo passo é examinar os intervalos e o contexto, não transferir
a decisão inteira para a marca booleana.

## R0080 · ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md

Ela também não fornece um ajuste para populações finitas ou contatos
correlacionados. Os requisitos sobre dados devem ser revistos antes de usar o
intervalo para generalizar resultados. No notebook histórico há interpretações
mais fortes que o retorno sustenta; a nota R01 delimita esse problema sem
alterar o código ou fabricar uma nova execução.

## R0080 · ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md

Revisão R01: leitura estática do módulo, fachada e notebook; revisão do próprio
autor, sem auditor independente. Fórmula ilustrativa não é execução do helper.
Teste Spark/Databricks e aceite humano permanecem separados e pendentes.

## R0066 · ambiente_fonte/.assistant/README.md

![CRM — Missão Modelos Analíticos CRM](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Um ambiente integrado de instruções, habilidades, bibliotecas e briefings que ajuda a transformar a Genie Code em uma parceira contextualizada para a rotina analítica.

> **LEGENDA DE PROCEDÊNCIA.** Agent Skills e instruções são mecanismos nativos suportados pela Genie Code. Os componentes `hub_prompts`, `hub_snippets`, `hub_scripts`, `hub_padroes`, `hub_micromodelos` e o conteúdo das skills `hub-ml-*` foram criados neste projeto e possuem ativação própria.

---


## R0066 · ambiente_fonte/.assistant/README.md

Sua homologação conversacional permanece pendente.

## R0066 · ambiente_fonte/.assistant/README.md

Consulte o Hub Padrões em `.assistant/hub_padroes/README.md`.

## R0073 · ambiente_fonte/.assistant/hub_padroes/README.md

Crie um {{TIPO}} para {{OBJETIVO}} usando @hub_padroes/{{TIPO}}/template.

## R0073 · ambiente_fonte/.assistant/hub_padroes/README.md

| executa diagnóstico orientado a um recurso | script |

## R0077 · ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/README.md

# `analisar_campanha` — formular a pergunta antes de pedir uma análise

<!-- readme-objeto: 1.0.0 -->

Este exemplar ajuda a transformar “mostre a taxa por segmento” em um pedido
com dados, período e uma decisão explícita. É **material dos padrões do Hub**;
o texto orienta uma interação, não executa uma análise sozinho.


## R0078 · ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/README.md

# `checar_base_campanha` — verificar a base antes de medir a campanha

<!-- readme-objeto: 1.0.0 -->

Este exemplar mostra como transformar problemas de uma tabela em um diagnóstico
legível, sem tentar corrigir os dados automaticamente. É **referência dos
padrões do Hub**, não um script de produção homologado.


## R0080 · ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md

# `taxa_resposta_campanha` — uma taxa acompanhada de sua incerteza

<!-- readme-objeto: 1.0.0 -->

Este exemplar mostra como apresentar a proporção de respostas de uma campanha
junto da precisão da estimativa, em vez de decidir olhando apenas a maior taxa.
É **material dos padrões do Hub**, não um novo helper operacional nem uma
implementação homologada para produção.


## R0184 · ambiente_fonte/.assistant/hub_padroes/auditoria/template.md

# Template — prompt de auditoria de sprint

Toda sprint fecha com uma rodada em **aba nova**, sem o contexto de quem
executou. Este arquivo monta o prompt.

## Por que em sessão sem contexto

Quatro rodadas neste projeto, quatro resultados: 13 achados na biblioteca, 22 e
25 na documentação, 25 no plano — todos em material que o autor já havia
revisado. A taxa não cai. Autorrevisão não encontra pressuposto do autor, porque
o pressuposto é invisível para quem o tem.

## As três invariantes

Presentes em todo prompt, e é o que fez as quatro rodadas funcionarem:

1. **Acesso ao disco e à CLI.** Auditor que só lê julga o texto; auditor que
   executa encontra o que quebra.
2. **Instrução para executar, não ler.** "Refaça o que a sprint fez, sobre um
   objeto, numa cópia temporária" produz achados que leitura nenhuma produz.
3. **Bloqueio de `CHANGELOG.md`, `docs/auditoria/`, `docs/sprints/` e do
   histórico do git.** Todos contêm o raciocínio de quem executou. `git log`
   sozinho entrega a sprint inteira.

## Profundidade por tipo de sprint

| Tipo de sprint | Profundidade | Foco do prompt |
|---|---|---|
| Fundação (ferramentas) | completa | o que a ferramenta deixa passar |
| Padrões | completa + leitura humana | ambiguidade que faria dois executores divergirem |
| Renomeação mecânica | de execução | o que quebrou sem ninguém ver; referência órfã; remoto sujo |
| Portão de formato | completa | se o formato aguenta os extremos do que virá |
| Conteúdo repetido | por amostragem | o auditor escolhe os objetos; 3 a fundo, varredura rasa no resto |
| README de topo | completa | percurso do leitor que chega sem contexto |
| Skill nova | completa + forward test | colisão de roteamento com as existentes |

## O esqueleto

```text
Você vai auditar o resultado de uma sprint de reestruturação. O objetivo não é
julgar o texto: é descobrir o que quebra quando alguém usar isto.

CONTEXTO
- Repositório: <caminho>
- O que a sprint entregou: <uma frase, sem justificativas>
- Arquivos no escopo: <lista ou pasta>

O QUE VOCÊ PODE LER
<pastas liberadas>

O QUE VOCÊ NÃO DEVE LER
CHANGELOG.md, docs/auditoria/, docs/sprints/, e o histórico do git
(git log, git show, git diff de commits). Contêm o raciocínio de quem executou.
git status e git ls-files são permitidos.

SOMENTE LEITURA
Não edite arquivo do repositório, não faça commit, não rode --execute. Para
experimentos, use pasta temporária fora do repositório e diga onde.

OS TESTES
T1 — EXECUTE, não leia. <a tarefa concreta de refazer/usar o que a sprint fez>
T2 — Reproduza todo número afirmado, com o comando que usou.
T3 — Teste toda afirmação técnica; confirmada, contradita ou não testável.
T4 — Divergência: onde dois executores competentes produziriam resultados
     diferentes? Cite o trecho, as duas leituras e a diferença no arquivo final.
T5 — O que a sprint não menciona e vai atingir.
T6 — Confronte com as regras do projeto em .claude/rules/.
<T7+ específicos da sprint>

FORMATO
Comece pelo T1, em prosa. Depois três listas ordenadas por custo de descobrir
tarde: QUEBRA (não funciona / falta algo sem o qual para), DIVERGE (ambiguidade
entre executores), MELHORÁVEL (só entra se disser o que se perde mantendo).
Termine com: o maior risco; a pergunta que você faria antes de continuar; o que
acertou e deve sobreviver; o que não conseguiu avaliar.

REGRAS
- Não elogie, não resuma de volta, não abra com apreciação geral.
- Achado sem evidência que você produziu não vale: descarte.
- Distinga "não funciona" de "eu faria diferente"; a segunda só entra com o
  custo concreto de manter.
- Trate justificativa como afirmação a verificar, não como explicação a aceitar.
- Priorize o defeito que só apareceria depois de dezenas de arquivos escritos.
```

## O que fazer com o resultado

Verifique **cada achado contra o disco** antes de aceitar. Nas quatro rodadas
deste projeto todos procederam, o que não é garantia para a próxima — e um
achado aceito sem verificação vira correção que quebra outra coisa.

Registre em `docs/auditoria/<data>_<tema>/`, com o que foi confirmado e o que a
correção não precisou tocar. A segunda lista delimita o escopo tanto quanto a
primeira.


## R0497 · ambiente_fonte/.assistant_instructions.md

- Mantenha o Hub em `ambiente_fonte/` canônico; gere `Novo_Ambiente_Simulado/` pelo renderer. Workspace é cópia operacional. Não altere instruções/skills/helpers compartilhados nem publique como efeito colateral de análise.

## R0192 · ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/analisar_campanha.md

Ele descreve o que aconteceu; não isola o efeito da oferta, do canal ou do
momento. Para atribuir causa, o desenho precisa ser experimental, e nenhum
formulário conserta uma campanha que já rodou sem grupo de controle.

## R0193 · ambiente_fonte/.assistant/hub_padroes/prompt/template.md

A lista abaixo era a antiga, preservada porque um item dela não estava no
canônico — os demais foram absorvidos:

## R0200 · ambiente_fonte/.assistant/hub_padroes/skill/template.md

A lista abaixo era a antiga, preservada porque um item dela não estava no
canônico — os demais foram absorvidos:

## R0193 · ambiente_fonte/.assistant/hub_padroes/prompt/template.md

rotas possíveis e peça `@` determinístico quando uma delas for escolhida.
Depender do roteamento automático para um pedido ambíguo é apostar: em teste
real, um pedido de análise direta levou o assistente a preterir a skill do Hub
em favor de uma nativa da plataforma — com argumento defensável. O prompt existe
para remover essa aposta.

## R0193 · ambiente_fonte/.assistant/hub_padroes/prompt/template.md

## O notebook, que não executa

## R0193 · ambiente_fonte/.assistant/hub_padroes/prompt/template.md

Prompt não roda: a resposta vem de uma interação que notebook nenhum reproduz.

## R0194 · ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md

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


## R0194 · ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md

- [ ] O objeto foi retirado da dispensa temporária quando ganhou README.

## R0194 · ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md

Os comandos `tools/readme_objeto_contract.py`, `tools/validate_assistant.py` e
`tools/ci_local.py` pertencem ao repositório, não ao pacote no workspace. Eles
não executam código do README para decidir se a explicação é correta. O gate
confere cabeçalhos, ligações locais e migração; API e fontes exigem leitura.

## R0194 · ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md

corrigido silenciosamente em sprint documental.

## R0195 · ambiente_fonte/.assistant/hub_padroes/readme/exemplo.md

## Como usar

## R0195 · ambiente_fonte/.assistant/hub_padroes/readme/exemplo.md

- **Significância não é relevância.** O segmento de 28 contatos tem intervalo que
  não se sobrepõe a nenhum outro: a diferença é real. E é irrelevante — são 28
  pessoas, e o teto absoluto são 17 respostas.

## R0196 · ambiente_fonte/.assistant/hub_padroes/readme/template.md

**Conte pastas de objeto, não arquivos.** `hub_snippets/display/` tem 3 objetos
(curta); `hub_snippets/spark/` tem 7 (padrão); `hub_padroes/` tem 7 subpastas
(padrão). A dúvida é real e produz READMEs de tamanhos diferentes para a mesma
pasta.

## R0196 · ambiente_fonte/.assistant/hub_padroes/readme/template.md

Depois da reestruturação, quase tudo que tem README é do Hub. Repetir "isto é
customizado" em vinte pastas é ruído. 

## R0197 · ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md

Versão **1.0.0**, estabilizada em 2026-09-12 após o piloto R02 e o aceite
editorial de Rodrigo. O PR nº 7 foi integrado antes da R03-A. O aceite do
padrão não aprova antecipadamente novos textos nem homologa runtimes.

## R0197 · ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md

Não transfira um “executado” antigo para esta sprint sem execução nova.

## R0198 · ambiente_fonte/.assistant/hub_padroes/script/template.md

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Se o seu objeto
> recebe **DataFrame** e devolve dado para o fluxo seguir, ele é snippet e não
> script — veja [`../snippet/template.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/script/../snippet/template.md). O que estiver
> em `checar_base_campanha/` é referência de forma, **não biblioteca**.

Use quando o objeto for **diagnóstico**: algo que se aponta a uma tabela do
workspace e que devolve um veredito legível, tipicamente antes de alguém confiar
naquele objeto.

## Script ou snippet?

A diferença é de papel, não de tamanho, e ela decide a assinatura da função:

| | Snippet | Script |
|---|---|---|
| Papel | peça de cálculo dentro de um fluxo | diagnóstico que roda sozinho |
| Entrada | `DataFrame` | **nome de tabela** (`catalogo.schema.tabela`) |
| Saída | `DataFrame` | dicionário com `status`, `checagens` e `alertas` |
| Quem chama | outro código, ou o notebook do analista | uma pessoa, antes de decidir |

Script recebe nome de tabela porque existe para ser apontado a algo que já está
publicado. Snippet recebe DataFrame porque entra no meio de uma transformação.



## R0198 · ambiente_fonte/.assistant/hub_padroes/script/template.md

# gerado por tools/api_publica.py

## R0198 · ambiente_fonte/.assistant/hub_padroes/script/template.md

## O contrato de saída

## R0198 · ambiente_fonte/.assistant/hub_padroes/script/template.md

A lista abaixo era a antiga, preservada porque um item dela não estava no
canônico — os demais foram absorvidos:

```text
[ ] a função recebe nome de tabela, não DataFrame
[ ] não escreve nada, e a docstring diz isso
[ ] a docstring diz quantas varreduras faz, para quem avalia custo
[ ] o notebook demonstra um caso pass/warn E um caso fail
[ ] __init__.py saiu da ferramenta
[ ] o README da seção lista este script
```



## R0199 · ambiente_fonte/.assistant/hub_padroes/skill/exemplo/SKILL.md

O Genie Code **não** descobre estes módulos sozinho. Importe-os explicitamente no
notebook, depois de acrescentar `.assistant` ao `sys.path`.

## R0200 · ambiente_fonte/.assistant/hub_padroes/skill/template.md

A skill recomenda o módulo no texto que injeta,
e quem importa é a pessoa, no notebook (ADR-0004).

## R0201 · ambiente_fonte/.assistant/hub_padroes/snippet/template.md

## 4. Converter um snippet que já existe

**A maior parte do trabalho do Hub não é criar: é converter.** São 51 snippets e
7 scripts que já rodam, que o smoke test já importa e que as skills já recomendam
por caminho de import. As seções acima descrevem o objeto pronto; esta descreve
como chegar nele sem quebrar o que funciona.

### A regra: mover, e só então melhorar

Converter é **mover**. A conversão não muda comportamento. Se o módulo antigo
devolve 0% em base vazia, o convertido devolve 0% em base vazia — mesmo que o
template peça "falhe cedo".

Duas etapas, em commits separados:

| Etapa | O que entra | O que **não** entra |
|---|---|---|
| **1. Mover** | pasta, `__init__.py` gerado, notebook novo, docstring traduzida e ampliada | nenhuma mudança de assinatura, de valor devolvido ou de comportamento em caso de borda |
| **2. Melhorar** | validação de entrada, constante de política, recusa em caso ambíguo | — |

A etapa 2 é **opcional e por objeto**, e exige registrar no notebook o que mudou.
Sem essa separação, cada executor decide sozinho quanto do módulo antigo
sobrevive, e a diferença só aparece quando algo que funcionava para de funcionar.

### O que a conversão não pode alterar

| Item | Por quê |
|---|---|
| Nome e ordem dos parâmetros | há código chamando; renomear `threshold_warn` quebra em silêncio |
| Nome das colunas devolvidas | quem consome o DataFrame quebra sem erro de import |
| Comportamento em base vazia, nulo e caso limite | é o que o smoke test e os testes de regressão fixam |
| `print()` de progresso, se houver | é ruído em biblioteca, mas removê-lo é mudança de comportamento — registre e faça na etapa 2 |

### Idioma

**Não traduza identificador na conversão.** Parâmetro, coluna devolvida e nome de
função ficam como estão — traduzir é quebra silenciosa. Docstring, comentário e
notebook são prosa e vão em português. Um módulo com `threshold_warn` e docstring
em português é inconsistente e correto; um com `limite_alerta` é consistente e
quebrado.

### Antes de mover, olhe para fora da pasta

| Verifique | Onde |
|---|---|
| Quem importa este módulo | `grep -rn "<secao>.<modulo>" ambiente_fonte tools` |
| Se o smoke test o cita nominalmente | `tools/spark_smoke_test.py` tem casos funcionais por nome |
| Se alguma skill o recomenda | as `SKILL.md` de `skills/` declaram helpers por caminho de import |
| Se ele redeclara constante de outro módulo | ver a regra abaixo — é o único caso em que a conversão **não** é só mover |

### Constante duplicada: a exceção que precisa de decisão

Quatro módulos de `ml/` redeclaram a paleta em vez de importá-la de
`constants.colors`. E os valores **divergem**:

| Nome | Onde | Valor |
|---|---|---|
| `PALETA_CATEGORICA` | `constants.colors` | 10 cores |
| `PALETA_CATEGORICA` | `ml.curves_plotly` | **6 cores** |
| `PALETA_CATEGORICA` | `ml.umap_viz`, `ml.vintage_analysis` | 10 cores, idênticas |

Duas das três cópias são iguais à original, o que torna a terceira invisível numa
inspeção rápida.

A regra exaustiva do `__init__.py` publica cada uma como API pública oficial. Ao
fim da conversão haverá dois caminhos de import para `PALETA_CATEGORICA` com
valores diferentes, ambos "corretos" pela regra.

**A conversão não resolve isso, e não deve tentar.** Trocar a redeclaração por
import muda o comportamento — `curves_plotly` passaria de 6 para 10 cores nos
gráficos —, e a etapa 1 proíbe mudança de comportamento. A instrução anterior,
"converta o import antes", pedia exatamente o que a regra veta.

**O que fazer:** converta como está, na etapa 1, e **registre a duplicação no
notebook do objeto**, na seção "quando não usar" — dizendo qual valor aquele
módulo usa e que ele difere de `constants.colors`. A unificação é decisão de
produto, vai para a etapa 2, e precisa de alguém olhando os gráficos para dizer
se seis ou dez cores é o certo ali.

Duplicação de constante com valor idêntico (`umap_viz`, `vintage_analysis`) é
dívida menor: registre no notebook e siga.



## R0201 · ambiente_fonte/.assistant/hub_padroes/snippet/template.md

## 1. `__init__.py` — não escreva à mão

```bash
python tools/api_publica.py <caminho>/<nome>.py > <caminho>/__init__.py
```

A ferramenta lê o módulo por AST e reexporta **todos** os nomes públicos de nível
superior. A regra é exaustiva, não curada, e isso não é preferência:
`constants/colors` tem 22 nomes públicos, e `visual/section_header` e
`visual/theme_plotly` importam nomes específicos dele. Uma curadoria plausível exporta cinco e quebra o import de
quem depende — e o sintoma aparece sprints depois da causa.

Resultado esperado:

```python
from .taxa_resposta_campanha import MINIMO_PARA_DECISAO, taxa_resposta_campanha

__all__ = [
    "MINIMO_PARA_DECISAO",
    "taxa_resposta_campanha",
]
```

Com isso o import fica limpo, sem repetir o nome:

```python
from hub_snippets.spark.pit_join import pit_join
```

### O `__init__.py` de **seção** não reexporta nada

`spark/__init__.py`, `ml/__init__.py` e os outros de nível de seção continuam
com docstring e mais nada. Só a pasta do **objeto** reexporta.

Não é preguiça: é o que mantém a seção importável. Um `__init__.py` de seção que
reexportasse os objetos importaria todos eles de uma vez — e **sete** módulos de
`ml/` importam biblioteca ausente no laboratório já no topo do arquivo. A seção
inteira deixaria de importar por causa deles, **e os irmãos junto**: um
`ml/score_bands`, sem dependência nenhuma, falharia com `exc.name='lightgbm'`,
porque importar qualquer submódulo executa o `__init__` do pacote pai.

(São 14 os módulos com dependência opcional; os outros 7 importam dentro da
função e por isso importam sem erro. A distinção importa na hora de decidir o
que testar.)

Verificado com um pacote de teste:

```text
pkg.ml.train_lgbm              -> OPTIONAL_MISSING  (exc.name = 'lightgbm')
pkg.ml.train_lgbm.train_lgbm   -> OPTIONAL_MISSING  (exc.name = 'lightgbm')
pkg.ml                         -> PASS
```

A última linha só é `PASS` porque a seção não reexporta.

### Objeto que depende de biblioteca ausente: nada muda

As duas primeiras linhas acima respondem à outra dúvida. O `__init__.py` eager
**preserva o `exc.name`** da dependência que faltou, então o smoke test continua
classificando como `OPTIONAL_MISSING` e não como `FAIL`.

E não há regressão: `train_lgbm.py` já tem `import lightgbm` no topo, de modo que
importar o módulo já falhava antes da conversão. A pasta falha do mesmo jeito,
pelo mesmo motivo, com o mesmo diagnóstico.

**Consequência para quem escreve o notebook:** o objeto não pode ser importado no
laboratório de forma alguma, nem para alcançar uma constante. É o caso do BLOCO
CANÔNICO de não executado, e o motivo se enquadra em "a dependência não existe e
não há versão compatível conhecida".



## R0201 · ambiente_fonte/.assistant/hub_padroes/snippet/template.md

Três listas divergentes conviveram neste projeto até uma auditoria apontar: uma
pedia smoke test e não pedia catálogo, outra o inverso. Uma lista só, com um
dono, é o conserto.

Os dois primeiros itens de verificação automática estão marcados: o validador
confere nome de pasta, os artefatos executáveis e se o `__init__.py` bate com a
API pública do módulo. A guarda de README confere a quarta peça segundo o
contrato de objeto e as dispensas transitórias de legados. Os demais são manuais — e o item do smoke test só é
alcançável depois que a seção inteira estiver convertida.



## R0201 · ambiente_fonte/.assistant/hub_padroes/snippet/template.md

A dispensa de legados é transitória e controlada no repositório;
converter a documentação não autoriza alterar a implementação.

## R0201 · ambiente_fonte/.assistant/hub_padroes/snippet/template.md

> recebe **nome de tabela** e devolve um veredito, ele é script e não snippet —
> a distinção está em [`../script/template.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_padroes/snippet/../script/template.md) e muda a
> assinatura da função.
