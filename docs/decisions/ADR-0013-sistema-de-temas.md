# ADR-0013 — Contrato central de temas com aplicação explícita por contexto

Data: 2026-09-12
Status: Proposto — candidata V01; não autoriza publicação
Autor: Codex

## Contexto

A V00 registrou centralizações parciais: constantes Python, template Plotly,
CSS local e sistema editorial YAML. Alterar uma aparência hoje exige localizar
consumidores distintos. Precisamos permitir revisão por pessoa não técnica sem
alterar resultados analíticos, rotina legada ou ativos aprovados por engano.
O Manual Técnico continua canônico e a arquitetura mantém seus componentes.

A base desta candidata é a main `b88a9cc`, que já integra READMEs/Concierge
(PR #7) e a instrumentação V00 (PR #8). O ADR-0012 continua reservado ao
contrato de READMEs; ADR-0013 estava disponível na consulta. A entrega local
anterior foi reconciliada com essa base, sem transportar sua V00 alternativa.
Nenhuma decisão aceita foi reescrita.

## Decisão

Adotar um contrato central versionado para identidade, modo e contexto, com
documentos JSON completos e fechados. Tornar o schema a fonte única dos campos,
limites e defaults; gerar sua referência textual. Manter política de aprovação
e destino fora do tema. Nunca aceitar código, CSS arbitrário, papel autodeclarado
ou parâmetro analítico em uma configuração visual.

Começar com notebook e editorial, sem herança de runtime nem resolução de
arquivos remotos. A composição proposta será materializada em configuração
explícita. Falhar diante de tema solicitado inválido; manter legado quando
nenhuma opção nova for escolhida. Adaptar APIs existentes de forma aditiva em
sprints posteriores, com configuração por chamada em vez de mutar globais
compartilhadas por usuário.

Usar a V01 apenas como contrato verificável em `docs/sprints/sistema_temas/V01/`.
Após aceite, promover a fonte canônica para o padrão de identidade visual do
produto, sem duas versões ativas independentes. Núcleo, UI, adaptadores, assets
gerados, Apps e dashboards são entregas posteriores. O laboratório deverá
separar prévia pessoal, proposta salva, aprovação e publicação explícita.

Vincular aprovação a bytes, dependências e destino verificados por processo
confiável. Preservar histórico e permitir retorno a revisão ainda aprovada.
Não tratar hash como autenticação nem resultados de testes sintéticos como
homologação de usuários, Spark ou plataforma.

## Alternativas consideradas

Um widget de HEX em cada notebook mantém configuração dispersa e mistura
experiência com processamento. Constantes globais mutáveis falham em isolamento
e não resolvem assets publicados. JSON e YAML editáveis independentemente
recriam duas fontes de verdade. Herança dinâmica reduz repetição mas introduz
ciclos, precedência e mudanças indiretas antes de termos necessidade comprovada.
Um App primeiro aumenta dependências e não resolve consumidores que ignoram
o tema. Um editor gráfico universal excede o objetivo; layout novo continua
exigindo template específico.

## Consequências

A configuração é auditável, completa e transportável; os adaptadores podem
ser migrados gradualmente preservando a rota antiga. O custo inicial é inventariar
e adaptar consumidores e escrever documentos completos por contexto. O editor
futuro esconderá essa repetição do usuário, não omitirá valores efetivos.

A V01 não muda o visual nem certifica compatibilidade de tema aplicado. Paletas
locais e divergências entre defaults declarados e renderizados exigem decisões
explícitas. Assets raster congelados continuam protegidos. Escolhas de papéis,
infraestrutura, desempenho e homologação permanecem gates, não detalhes a
preencher com suposições.

Não supersede ADRs anteriores nesta candidata. Aceite do usuário, auditoria
independente e integração com main permanecem pendentes.

## Referências

- [Frente de temas e baseline](../sprints/sistema_temas/README.md).
- [Contrato V01](../sprints/sistema_temas/V01/CONTRATO_TEMAS.md).
- [Governança](../sprints/sistema_temas/V01/GOVERNANCA.md).
- [Fontes e dependências](../sprints/sistema_temas/V01/LEITURAS_E_DEPENDENCIAS.md).
- [ADR-0010 — Manual Técnico](ADR-0010-manual-tecnico-unificado.md).
- [ADR-0009 — identidade e pacote](ADR-0009-identidade-e-pacote-de-implantacao.md).
