# ADR-0022 — Certificação prospectiva e evolução de contratos no Skill Enforcement Rollout

Data: 2026-09-22  
Status: Aceito  
Autor: ChatGPT  
Origem: SER00 — decisão humana explícita após revisão dos achados A01–A03.

## Contexto

O Skill Enforcement Framework (SEF) foi encerrado em SE08 e preserva perfis históricos `se01`–`se08`, evidências e resultados vinculados às respectivas árvores. A SER sucede operacionalmente o SEF para promover, skill por skill, níveis ainda abaixo do target.

A SER00 encontrou três tensões: (1) regressões históricas SE08 contêm assertions temporais sobre a árvore vigente à época — por exemplo `hub-ml-criar-objeto=L2` e a contagem de contratos — que deixarão de ser verdadeiras após promoções legítimas; (2) o vocabulário fechado do `execution_contract` 0.1 foi desenhado em torno da EDA e não representa diretamente condições como point-in-time, maturidade, materialização ou intenção de deploy; (3) o piloto L3 de criar-objeto cobre apenas `create/readme/agregador` no envelope Windows/NTFS e não prova L3 global.

O usuário aprovou em 2026-09-22 o encaminhamento arquitetural A01–A03. Esse aceite congela a direção, não implementa os mecanismos e não autoriza SER01 ou merge da SER00.

## Decisão

1. **Preservar o SEF histórico.** Perfis `se01`–`se08`, documentos, failures e estados históricos não serão reescritos para acompanhar a SER.
2. **Criar certificação SER prospectiva e aditiva.** Ela terá identidade própria, evidência SHA-bound, diretório externo, fail-closed, logs/hashes e composição explícita dos invariantes atuais. Testes históricos temporalmente pinados não serão silenciosamente transformados em assertions da árvore futura.
3. **Não mascarar falhas históricas.** Quando um comando/perfil antigo for executado numa árvore nova, seu resultado é registrado como canal histórico separado; não é removido nem reinterpretado como PASS.
4. **Evoluir condições de contrato de forma aditiva.** Contratos 0.1 permanecem válidos. Semântica específica de domínio deve preferir preflight/condição local da skill; somente conceitos transversais estáveis justificam ampliar o schema compartilhado. Condição desconhecida ou aplicabilidade não determinada bloqueia a etapa material. Expressões arbitrárias/eval continuam proibidas.
5. **Separar target de cobertura provada.** `hub-ml-criar-objeto` mantém `target_level=L3` e `scope_mode=stage_specific`, mas `current_level=L2` permanece até que a SER01 congele e prove a matriz operação × tipo × host × efeito da superfície promovida. Um piloto não autoriza overclaim global.
6. **Promoção de policy é posterior à prova.** A mudança de `current_level` continua sendo o último ato funcional da sprint e exige recertificação do SHA final e aceite humano específico.
7. **Rollout mode permanece separado do nível.** Este ADR não altera `rollout_mode` nem `execution_contract.mode`.

## Consequências

- A SER pode evoluir sem adulterar a semântica histórica da SE08.
- Será necessário implementar e testar um gate/certifier SER próprio ou uma composição equivalente com identidade distinta antes da primeira promoção.
- Novos domínios não serão forçados a reutilizar flags da EDA com significado diferente.
- Uma skill pode manter target alto e current baixo por tempo indefinido quando a superfície não puder ser provada no ambiente disponível.
- A SER00 deixa de estar bloqueada por decisão arquitetural, mas continua `SER00_NOT_READY` até o fechamento local A07, aplicação preservadora do changelog/snapshots e novo checkpoint.
- SER01 permanece `NOT_STARTED` e exige autorização separada após integração da SER00.

## Alternativas rejeitadas

- Reescrever `--profile se08` para aceitar a árvore futura: rejeitado por destruir a semântica histórica.
- Apenas criar um perfil novo mantendo assertions antigas na composição: rejeitado porque não resolve o acoplamento temporal.
- Trocar assertions históricas como `L2` por `L3` para obter verde: rejeitado por converter expectativa futura em falsa evidência passada.
- Reutilizar condições 0.1 com semântica diferente: rejeitado por tornar o contrato ambíguo.
- Promover criar-objeto com base no piloto `create/readme/agregador`: rejeitado por extrapolação de cobertura.

## Evidência e limites

Este ADR registra decisão arquitetural. Não prova execução local, Databricks Free, comportamento Genie, nem altera policy/produto. A certificação canônica da candidata SER00 continua pendente em A07.

## Referências

- `docs/sprints/skill_enforcement_rollout/PLANO_MESTRE.md`
- `docs/sprints/skill_enforcement_rollout/SER00/DESENHO_TECNICO.md`
- `docs/sprints/skill_enforcement_rollout/SER00/CHECKPOINT.md`
- `docs/sprints/skill_enforcement/REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`
- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`
