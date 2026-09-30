# ADR-0024 — Módulo de Micromodelos no Hub

Data: 2026-09-30
Status: Aceito por orientação do responsável em 2026-09-29 e 2026-09-30
Autor: Codex

## Contexto

O framework de Micromodelos cresceu em `tools/` e em documentos de sprint, enquanto a skill e os prompts já fazem parte do produto `.assistant`. Isso exige um pacote técnico separado para transportar a execução. O responsável pediu que todo o ambiente seja levado junto ao trabalho e que Micromodelos tenha uma pasta própria no Hub, com exemplo fictício completo para avaliação.

## Decisão

Distribuir contratos, código reutilizável e exemplos de Micromodelos em `ambiente_fonte/.assistant/hub_micromodelos/`. Manter a skill em `skills/` e os prompts nas pastas existentes. A pasta é um módulo de domínio, não um novo tipo de objeto na taxonomia do Hub. Organizar subpastas conforme a necessidade concreta de navegação e manutenção, preservando o conteúdo e as capacidades já previstos.

O produto instalado será a fonte de execução; `tools/` conserva apenas desenvolvimento, testes e comandos compatíveis que deleguem à biblioteca. O pacote padrão do Hub transporta o módulo completo.

## Alternativas consideradas

- Continuar com o runtime apenas no ZIP técnico separado: dificulta a avaliação e instalação do ambiente como um conjunto.
- Tratar cada micromodelo como uma skill: mistura artefato analítico com o mecanismo de instruções do Genie Code.

## Consequências

- READMEs e Manual Técnico passam a orientar o uso do módulo e de um exemplo sintético preenchido.
- Inventário, validador, renderização, publicação Free e kit corporativo precisam reconhecer a nova pasta.
- A migração de localização não certifica comportamento no Genie Code nem autoriza publicação institucional.

## Referências

- [ADR-0014](ADR-0014-micromodelo-artefato-de-dominio.md)
- [ADR-0015](ADR-0015-micromodelo-yaml-canonico.md)
- [plano de integração](../sprints/micromodelos/PLANO_INTEGRACAO_HUB_MICROMODELOS.md)
