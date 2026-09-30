# Consolidação da validação B1 na Genie — 2026-09-30

(Codex) Esta é a síntese decisória das coletas manuais proporcionais, não
uma reclassificação das tentativas históricas. Fontes: [registro por caso](GENIE_SKILLS_RESULTADOS_2026-09-28.md),
[reconciliação SD × FG](RECONCILIACAO_SD_FG_2026-09-29.md),
[triagem pós-UI](TRIAGEM_POS_UI_2026-09-30.md),
[provas locais](ENTREGA_LOCAL_2026-09-28.md) e
[provas Free R2](CONTINUACAO_LOCAL_FREE_2026-09-28.md).

## Decisão atual

As **37/37 primeiras tentativas SD** foram coletadas. O lote proporcional
adicional foi concluído: seis checagens dirigidas das skills sem cobertura
atual suficiente e seis diagnósticos em cinco frentes (Cross-EDA,
Pipeline Builder, Baseline, Feature Engineering e Safra), incluindo dois de
Pipeline Builder para separar chat sem @ de seleção @. O lote não equivale
a 42/42 prompts FG; os literais não enviados continuam NOT_RUN. Os
**39/39 forward históricos** e as provas locais/Free são reaproveitados
somente no objetivo e versão que demonstraram.

**Nenhuma das 14 skills está homologada integralmente por esta campanha.**
Os perfis candidatos declarados tiveram testes locais e provas Free R2
registrados, mas isso é separado da seleção/aderência pela Genie. Um chat
conceitual sem output de runner/Receipt não certifica execução canônica;
uma falha textual em chat não apaga uma prova Free anterior. MM04 é a 15ª
skill no pacote remoto e tem frente/gates próprios.

| Skill B1 | O que a coleta Genie demonstrou | Lacuna material que permanece |
|---|---|---|
| Safra | @ e indicador; estados MOB0–MOB3 corretos com corte e taxa final recusada em [D01](genie_evidencias/SD-VF-STATUS-D01.md) | Sugestão de denominador provisório 1 contra roster 2; falhas históricas de maturidade/ausência não são apagadas; última rodada NOT_RUN |
| Explainability | @ e respostas conceituais corretas em retestes; fronteira de `valid=true` corrigida | Prova conversacional é limitada ao exemplo; nenhum SHAP/Receipt novo nesta rodada |
| Validação Estatística | KS sintético com execução observada no [SD-ST-P-D01](genie_evidencias/SD-ST-P_D01.md); @ observado | Ressalvas históricas de potência/procedência e multiplicidade permanecem por caso |
| Cross-EDA | Seleção espontânea no [D01](genie_evidencias/SD-CE-P-D01.md) e cálculo 2/3 correto | Fontes/contexto preenchidos sem prova e preflight/Receipt alegados sem outputs observáveis; SER05 conversacional não homologado |
| Feature Engineering | @ e regra PIT observados; em [D01](genie_evidencias/SD-FE-MAT-D01.md), `UNKNOWN` e entrypoints corretos | Somente Baseline apareceu no indicador espontâneo D01; readback e causa do bloqueio extrapolados; efeito não executado nesse chat |
| Baseline ML | Indicador espontâneo confirmado; [D01](genie_evidencias/SD-BL-P-D01.md) reservou holdout e não inventou treino/MLflow | Datas de maturidade e “gap natural” presumidos; plano não é treino executado |
| Monitoramento | @ e indicador; recusa de ação automática por AUC crítico; D04 exploratório corrigiu PSI/KS | Casos anteriores com interpretação/roteamento falho preservados; SER12 não foi certificado pelo chat conceitual |
| Pipeline Builder | @ e indicador; [D02](genie_evidencias/SD-PB-DELTA-D02.md) conservou estado `UNKNOWN` após DROP incerto | Roteamento espontâneo ausente em D01; detalhes de tabela gerenciada/arquivos presumidos; efeito não executado no chat |
| EDA Profissional | @ e indicador confirmados | Resposta recente presumiu tipos/grão sem schema; falha parcial de contexto |
| Tutor Databricks | @ e indicador confirmados | Resposta afirmou estado/execução anteriores sem evidência suficiente |
| Comentar Notebook | @ e indicador; resultado `df.count()` mantido pendente | Ressalva de frase que amplia ausência de execução além da sessão; sem novo runner aplicável |
| Auditoria Skills | @ e indicador; reconheceu número `42` sem prova | Score incoerente e preflight/runner só narrados, sem output observável; não homologar SE07 pelo texto |
| Criar Objeto | Cobertura forward histórica no nome atual e regressão local proporcional | Nenhum novo chat B1 específico; não inferir homologação da policy vigente apenas do histórico |
| Concierge | Positivo espontâneo e seleção @ com indicador passaram nos casos coletados | Matriz literal FG completa e gates próprios não foram executados; não pedir 42 chats só para preenchê-la |

## Versão e fronteira da evidência remota

Após as conversas, o verificador read-only do Free comparou **657/657**
arquivos gerenciados sem divergência de conteúdo e encontrou **15/15**
skills. O inventário geral retornou **FAIL** pelos 30 objetos extras sob
`.assistant/hub_micromodelos/`, de propriedade da frente paralela; todos
foram preservados. Hash normalizado da fonte gerenciada:
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
Relatório bruto: `.artifacts/skills-delivery-evidence/genie-20260930-final-remote-verify.json`
(SHA-256 `45844d944d741c24556f7a7ea0331def4b55c60a0e080e16a6a98faaa887d674`).
O readback posterior reduz a hipótese de bytes B1 divergentes, mas não
prova qual arquivo a Genie leu em cada chat nem neutraliza possível efeito
de roteamento dos objetos extras. Não houve limpeza/publicação.

## Fila proporcional após a consolidação

1. **Roteamento:** manter o FAIL espontâneo FE D01 e os casos sem indicador
   como observações específicas. Já existe @ FE positivo; não alterar
   `description` ou instrução global por um caso isolado sem hipótese causal
   reproduzível. O indicador de Baseline D01 e o @ de Safra foram confirmados.
2. **Precisão:** preservar os FAILs materiais de denominador Safra,
   proveniência/Receipt Cross-EDA, dados ausentes em EDA/Tutor e score de
   Auditoria. O contrato local já cobre as fronteiras principais; revisão
   textual duplicada não é uma correção causal demonstrada. Reabrir produto
   somente com lacuna concreta de contrato ou falha reproduzível do runner.
3. **Execução canônica:** usar os relatórios locais/Free existentes para os
   perfis que já rodaram. Uma nova rodada Genie só é necessária se o gate
   específico exigir observar a Genie escolher/chamar a rota e seus outputs;
   não converter alegação textual em Receipt verificado.
4. **Integração:** manter os 30 objetos `hub_micromodelos` sob responsabilidade
   da frente MM. Não apagar, sobrescrever, publicar policy, fazer merge nem
   inferir readiness. A eventual integração do inventário remoto com a fonte
   B1 exige reconciliação de ownership e escopo com a frente MM.

## Revisão focal do contrato vigente

A leitura dos `SKILL.md` da fonte confirma guardas já explícitas nos
achados centrais: Safra exige denominador fixo e distingue
`NO_OBSERVATIONS`/`INCOMPLETE`; Cross-EDA exige fontes, chaves e outputs
de preflight/Receipt antes de afirmar cobertura medida; Feature Engineering
nomeia `effect_request`/`execute` e bloqueia retry em `UNKNOWN`; Baseline
exige corte/split e reserva avaliação do holdout; EDA/Tutor vedam preencher
schema ou resultado sem saída; Auditoria exige preflight/runner e separa
alegação de reverificação. [Triagens anteriores](TRIAGEM_POS_SD_2026-09-29.md)
e [pós-UI](TRIAGEM_POS_UI_2026-09-30.md) sustentam o mesmo limite.

**Decisão de consolidação:** estes chats não demonstraram lacuna nova de
contrato ou defeito reproduzível do runner que justifique editar a fonte,
renderizar/publicar de novo ou repetir todos os prompts. As respostas
incorretas permanecem FAIL de comportamento por caso. O roteamento
espontâneo FE é uma falha observada nesta rodada, mas a `description` já
inclui materialização e há carregamento FE espontâneo em T01; não há causa
isolada para mudar o gatilho global.

O pacote B1 fica como **candidato verificado nos perfis locais/Free declarados,
com homologação Genie parcial**. O próximo gate não é mais uma rodada manual
automática: qualquer expansão de escopo, correção de produto ou aceite
integral deve indicar critério específico e evidência adicional. Policy,
merge e workspace corporativo continuam em seus gates próprios.

O [fechamento técnico por diferença](FECHAMENTO_TECNICO_B1_2026-09-30.md)
vincula snapshot, mudanças após R2, testes reaproveitados, validador atual
e limites do worktree compartilhado para revisão antes de qualquer merge.
