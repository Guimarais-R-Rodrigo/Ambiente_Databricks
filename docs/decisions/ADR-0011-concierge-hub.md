# ADR-0011 — Concierge para descoberta e composição do Hub

- **Status:** Aceito para integração Git por solicitação do usuário em 12/09/2026.
- **Data:** 2026-09-12.
- **Alcance:** modifica a rejeição de descoberta em chat do ADR-0004 apenas para
  a demanda explícita de descoberta e composição. Declaração de helpers nas
  skills, pasta de objeto e inventário integrado ao Manual permanecem.

## Contexto

O usuário aprovou implementar a proposta após a criação e explicação do protótipo
em `novas_funcionalidades/skills/hub-ml-concierge/`. O objetivo é melhorar o uso do
Hub, não operar outro agente nem substituir as especialidades analíticas.

## Decisão

Manter o procedimento em `ambiente_fonte/.assistant/skills/hub-ml-concierge/`.
A cópia experimental fica congelada como histórico, com um ponteiro na coleção.
A skill usa o mapa semântico existente e ferramentas de leitura disponíveis,
verifica finalistas e produz recomendação/handoff. Nenhum acesso é criado por texto.

A ativação é limitada à descoberta solicitada ou menção explícita. Não é porta
obrigatória de todas as tarefas e não intercepta especialista já selecionado.
A leitura é progressiva: índices das cinco famílias, shortlist e contratos dos
finalistas. Registra versão, cobertura e acesso parcial, sem inventar inexistência.
A declaração explícita dos helpers nas demais skills continua sem alterações.

Não criar catálogo autoral paralelo, indexador, servidor MCP, agente independente
ou execução analítica no Concierge. Futuras ferramentas de busca requerem evidência
de necessidade e devem derivar suas informações das fontes existentes.

## Controles e integração

Atualizar política central de skills, mapa das instruções, READMEs e Manual;
manter cópia do Manual da raiz idêntica. O renderer é o único autor do simulado.
Adicionar o verificador e as regressões da skill ao CI, com testes de integração
que conferem referências, inventário, instruções e igualdade fonte/derivado.

O antigo 39/39 de forward tests é evidência histórica, não aprovação da skill nova
nem do conjunto ampliado. Preparar 14P/14N/14M e manter a matriz detalhada do pacote.
Antes de compartilhar, executar no destino os casos da nova skill e das vizinhas,
com revisão independente conforme o fluxo multi-IA.

## Consequências e limites

Usuários podem começar pela necessidade, inclusive reutilizando somente uma função
pública. Há mais conteúdo e risco de colisão de descriptions; testes conversacionais
continuam necessários. Validação estática não assegura a qualidade da recomendação.

Integração no Git não autoriza instalação, consultas de dados, publicação no Free
ou trabalho, alterações de ACL ou homologação. O pacote não realiza essas ações.

## Referências

- [ADR-0004](ADR-0004-declaracao-explicita-de-helpers.md).
- [ADR-0010](ADR-0010-manual-tecnico-unificado.md).
- [Skill integrada](../../ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md).
- [Forward tests](../testes/forward/README.md).
