# Decisões arquiteturais (ADRs)

Um ADR (*Architecture Decision Record*) registra uma decisão estrutural junto com
o contexto que a motivou e as alternativas descartadas. A prática existe porque a
decisão em si é a parte fácil de recuperar depois — o difícil é lembrar **por
que** ela foi tomada, e sem isso alguém refaz o mesmo debate ou reverte por
engano algo que resolvia um problema real.

Estes arquivos são **imutáveis depois de aceitos**. Mudar de ideia não apaga o
ADR antigo: escreve-se um novo que o supersede, e o antigo recebe um aviso
apontando para o substituto. O ADR-0005 deste projeto é exatamente isso — ele
reverte a decisão do ADR-0002 depois que uma medição mostrou que a escolha
original quebraria a biblioteca. Os dois continuam no repositório, e a leitura
em sequência mostra o raciocínio completo, inclusive o erro.

Escreva um ADR quando a decisão for difícil de reverter, afetar a estrutura do
projeto, ou quando alguém provavelmente perguntará "por que fizeram assim?".
Preferência de estilo e ajuste pontual não pedem ADR — pedem entrada no
changelog. Template em `.claude/templates/adr.md`.

| ADR | Decisão | Status |
|---|---|---|
| [ADR-0001](ADR-0001-arquitetura-multi-ia.md) | Arquitetura multi-IA: repo canônico + camadas derivadas | Aceito |
| [ADR-0002](ADR-0002-engine-databricks-genie-hub.md) | Reutilizar engine `databricks-genie` do Hub | ~~Aceito~~ supersedido por ADR-0005 |
| [ADR-0003](ADR-0003-quarentena-ambiente-antigo.md) | `Ambiente_Antigo/` local-only (fora do git) | Aceito |
| [ADR-0004](ADR-0004-declaracao-explicita-de-helpers.md) | Helpers declarados nas skills, não descobertos em chat | Aceito; localização e forma supersedidas por ADR-0007 |
| [ADR-0005](ADR-0005-publicacao-propria-no-free.md) | Publicação própria no Free, herdando o padrão do Hub | Aceito; critério de conferência supersedido por ADR-0008 |
| [ADR-0006](ADR-0006-identidade-hub.md) | De ambiente pessoal a Hub de equipe: `x_`→`hub_`, `rodrigo-`→`hub-ml-`, com tabela de correspondência | Aceito |
| [ADR-0007](ADR-0007-catalogo-e-pasta-de-objeto.md) | O catálogo depois da pasta de objeto: onde vive, o que cobre, e a coluna `exec` | Aceito |
| [ADR-0008](ADR-0008-criterios-de-conferencia-da-publicacao.md) | O critério de conferência sai do ADR e vai para constante de código | Aceito |

Ao adicionar um ADR, atualize esta tabela e registre no `CHANGELOG.md`.
