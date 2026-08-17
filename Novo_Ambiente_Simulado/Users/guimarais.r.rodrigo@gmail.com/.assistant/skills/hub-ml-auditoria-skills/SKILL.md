---
name: hub-ml-auditoria-skills
description: Audita implementações de skills do Databricks Genie Code e também outputs produzidos por uma skill contra o contrato de seu SKILL.md. Verifica descoberta, frontmatter, gatilhos, referências, segurança, executabilidade, coerência cruzada, completude e reprodutibilidade. Usar quando pedirem revisão, auditoria, QA, score, validação, inconsistências ou melhoria de uma pasta em `.assistant/skills`, ou quando quiserem validar notebook, relatório, código ou artefato gerado por outra skill.
---

# Auditar skills e seus outputs

## Basear a auditoria em evidências

Tratar como requisito nativo somente o que estiver sustentado pela documentação oficial atual do Databricks Genie Code ou pela especificação Agent Skills adotada. Identificar políticas internas, preferências e heurísticas com o rótulo **customizado**.

Não aprovar uma skill apenas por conter palavras-chave. Ler o contrato, testar referências e avaliar se um agente consegue executar o fluxo sem adivinhar detalhes críticos.

## Selecionar o modo

- **Modo IMPLEMENTAÇÃO**: auditar uma ou várias pastas em `.assistant/skills`.
- **Modo OUTPUT**: auditar notebook, relatório, código ou outro artefato gerado,
  comparando-o com o `SKILL.md` da skill produtora e com o pedido original.
- Se as entradas forem ambíguas, perguntar qual modo usar. Não avaliar o output como
  se fosse a implementação, nem o inverso.

## Executar auditoria de implementação

1. Inventariar cada pasta direta de `.assistant/skills`.
2. Confirmar um `SKILL.md` por pasta e nome idêntico ao diretório.
3. Validar os campos obrigatórios `name` e `description`; registrar campos opcionais
   e confirmar suporte. Este pacote adota apenas os dois obrigatórios como política
   conservadora local.
4. Verificar nome em minúsculas, hífens, até 64 caracteres e descrição com função mais gatilhos concretos.
5. Medir tamanho do corpo; recomendar menos de 500 linhas e 5.000 tokens.
6. Confirmar instruções no imperativo/infinitivo e ausência de seção redundante de gatilhos no corpo.
7. Resolver cada link relativo a partir da raiz da skill e registrar referências ausentes.
8. Inspecionar scripts: sintaxe, argumentos, dependências, efeitos colaterais, dados sensíveis e ao menos um teste representativo.
9. Procurar APIs inexistentes, comandos apresentados como nativos sem serem, paths pessoais, segredos e alegações regulatórias sem fonte.
10. Comparar skills entre si para detectar sobreposição, contradições, ciclos e contratos de handoff incompatíveis.
11. Conferir a seção de helpers da skill contra [CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md): módulos citados existem, caminhos de import conferem, dependências opcionais estão sinalizadas e nenhum helper aplicável ao fluxo ficou de fora.
12. Executar o validador disponível e registrar comando, saída e data.
13. Produzir achados priorizados e uma conclusão independente para cada skill e para o conjunto.

## Executar auditoria de output

1. Ler o pedido original, o output e o `SKILL.md` da skill produtora.
2. Extrair o contrato de entrada, as etapas obrigatórias, o contrato de saída, os
   limites de segurança e os gates de validação.
3. Mapear cada requisito para evidência concreta no output. Marcar como ausente o que
   não estiver demonstrado; não inferir execução por intenção textual.
4. Verificar resultados, código, fórmulas, amostragem, leakage, efeitos de escrita,
   caminhos, dependências e reprodutibilidade proporcionalmente ao risco.
5. Avaliar completude, reprodutibilidade, rigor, documentação, rastreabilidade,
   governança, acionabilidade, apresentação, robustez e integração do ecossistema.
6. Verificar aderência à biblioteca: quando o output reimplementa lógica já disponível
   em `hub_snippets`/`hub_scripts` — PSI, split temporal, WOE/IV, métricas, bandas de score,
   curvas de safra — registrar achado, indicar o módulo do catálogo e avaliar se a
   versão reescrita diverge da implementação auditada. Reescrita justificada é
   aceitável; reescrita silenciosa não.
7. Separar defeito do output, limitação da skill produtora e falta de entrada do
   usuário. Não atribuir um problema à camada errada.
8. Produzir score/rubrica somente depois dos vetos críticos; média alta não neutraliza
   erro material, leakage, dado corrompido ou claim regulatório indevido.
9. Entregar correções propostas ou, quando autorizado, corrigir o output e repetir a
   auditoria. Não modificar a skill produtora sem autorização explícita.

## Classificar achados

Usar severidade baseada em impacto:

- **Crítico**: impede descoberta/execução, expõe segredo, corrompe dados ou induz decisão material errada.
- **Alto**: API quebrada, leakage, cálculo incorreto, alegação regulatória indevida ou contradição central.
- **Médio**: baixa clareza, documentação desatualizada, referência frágil ou custo excessivo de contexto.
- **Baixo**: consistência editorial ou oportunidade de melhoria sem impacto operacional imediato.

Para cada achado, registrar:

- evidência com arquivo e linha;
- impacto observável;
- requisito oficial ou princípio aplicável;
- correção mínima;
- validação de aceite.

## Avaliar dimensões

Pontuar de 0 a 10, sem esconder vetos, nestas dimensões:

1. descoberta e estrutura;
2. executabilidade;
3. rigor técnico;
4. segurança e privacidade;
5. reprodutibilidade;
6. uso eficiente de contexto;
7. integração Databricks;
8. coerência cruzada;
9. qualidade dos recursos;
10. aderência à biblioteca de helpers;
11. clareza da entrega.

Uma média alta não compensa achado crítico. Separar conformidade verificável de julgamento editorial.

## Usar recursos

- Usar [CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md) como referência de aderência: é a lista dos módulos disponíveis, com API e dependências opcionais.
- Para auditar a própria documentação e nomenclatura, `hub_scripts.doc_coverage` e `hub_scripts.naming_checker` estão disponíveis; o segundo aplica política do projeto, não requisito da Databricks.
- Usar [templates/rubrica_universal.md](templates/rubrica_universal.md) como ponto de partida, ajustando pesos ao risco real.
- Usar [templates/relatorio_auditoria.md](templates/relatorio_auditoria.md) para a saída.
- Consultar [templates/checkpoints_por_skill.md](templates/checkpoints_por_skill.md) somente como histórico customizado. Não tratá-lo como documentação oficial nem como lista fixa de aceite; conferir o `SKILL.md` atual de cada skill.

## Verificar o resultado

Antes de concluir:

- reexecutar validações após as correções;
- garantir zero links internos quebrados;
- no modo implementação, confirmar campos YAML suportados e a política local;
- confirmar que exemplos não dependem de paths do autor;
- distinguir “funciona por convenção local” de “é descoberto automaticamente pelo Genie Code”;
- no modo output, anexar a matriz contrato → evidência → status e listar testes
  executados/não executados;
- listar riscos remanescentes e testes não executados.
