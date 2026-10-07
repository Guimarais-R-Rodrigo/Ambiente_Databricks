# Prompt: auditoria de implementação ou output de skill

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe a pasta/arquivos da skill com
> **Add context**/`@`. Skill: `@hub-ml-auditoria-skills`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-auditoria-skills/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO_V2.md#catalogo-helpers) é o catálogo integrado.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{IMPLEMENTACAO_OU_OUTPUT}}` | Escolha exatamente um modo. | Evita auditar artefato como contrato. | OUTPUT |
| `{{SKILL_ALVO}}` | Anexe a pasta ou nomeie o `SKILL.md` produtor. | Fixa o contrato auditado. | `@hub-ml-baseline-ml` |
| `{{OUTPUT_ALVO_OU_NAO_APLICAVEL}}` | Anexe o artefato no modo OUTPUT. | Fornece a evidência a comparar. | `@relatorio_baseline.md` |
| `{{PEDIDO_ORIGINAL_OU_NAO_APLICAVEL}}` | Anexe ou transcreva o pedido original. | Permite medir aderência real. | link do chat ou texto literal |
| `{{CASOS_DE_USO}}` | Liste fluxos que a skill precisa cobrir. | Define cobertura funcional. | baseline binário e regressão |
| `{{PROMPTS_TESTE}}` | Forneça casos positivos e negativos. | Testa roteamento e limites. | pedido direto e pedido ambíguo |
| `{{TIPO_E_LOCAL}}` | Informe user/workspace e caminho. | Determina descoberta e precedência. | user skill em `/Users/...` |
| `{{DEPENDENCIAS}}` | Liste scripts, helpers e runtimes. | Permite testar executabilidade. | PySpark; `hub_snippets.ml` |
| `{{FOCO}}` | Priorize risco, segurança ou completude. | Controla profundidade. | leakage e efeitos de escrita |
| `{{AUDITORIA_PLANO_DE_CORRECAO_OU_CORRIGIR_AUTORIZADO}}` | Escolha relatório, plano ou correção autorizada. | Não transforma revisão em edição implícita. | auditoria + plano |

## Prompt pronto para colar

```text
Use @hub-ml-auditoria-skills no modo {{IMPLEMENTACAO_OU_OUTPUT}}. No modo
IMPLEMENTAÇÃO, audite a pasta da skill contra a documentação oficial atual da
Databricks e o padrão Agent Skills. No modo OUTPUT, audite o artefato anexado contra
o pedido original e o contrato no SKILL.md da skill produtora. Não edite no modo
AUDITORIA.

CONTEXTO
- Skill/pasta alvo: {{SKILL_ALVO}}
- Output alvo (modo OUTPUT): {{OUTPUT_ALVO_OU_NAO_APLICAVEL}}
- Pedido original (modo OUTPUT): {{PEDIDO_ORIGINAL_OU_NAO_APLICAVEL}}
- Casos de uso esperados: {{CASOS_DE_USO}}
- Exemplos de prompts: {{PROMPTS_TESTE}}
- Ambiente user/workspace: {{TIPO_E_LOCAL}}
- Dependências/scripts: {{DEPENDENCIAS}}
- Riscos prioritários: {{FOCO}}
- Modo: {{AUDITORIA_PLANO_DE_CORRECAO_OU_CORRIGIR_AUTORIZADO}}

CHECKLIST
1. Estrutura: `.assistant/skills/<skill>/SKILL.md`, pasta dedicada e referências
   relativas à raiz da skill.
2. Frontmatter: `name` e `description` obrigatórios; nome válido, descrição que
   explique o que faz e quando usar, e campos opcionais somente se suportados.
3. Descoberta: escopo focal, gatilhos inequívocos e possibilidade de `@` mention.
4. Conteúdo: passos claros, exemplos, casos de borda e contexto mínimo necessário.
5. Recursos: scripts executáveis, documentação separada, links/caminhos válidos e
   ausência de imports/APIs fantasma.
6. Segurança: sem segredos, PII, paths pessoais ou ações mutáveis sem limites.
7. Correção: APIs atuais, claims suportados e distinção entre recurso Databricks e
   convenção customizada.
8. Testes: validação estrutural, parsing, execução segura de scripts e prompts
   representativos. Registre o que não pôde ser executado.
9. No modo OUTPUT: contrato da skill produtora, matriz requisito→evidência, correção
   técnica dos resultados, reprodutibilidade, rastreabilidade e adequação ao pedido.

CONTRATO DE SAÍDA
- Inventário e veredito de descobribilidade.
- No modo OUTPUT, veredito do artefato e separação entre defeito do output,
  limitação da skill e entrada ausente.
- Achados P0/P1/P2/P3 com arquivo, evidência, impacto e correção proposta.
- Matriz requisito→evidência→status.
- Plano de testes e prompts de forward test.
- No modo CORRIGIR, diff e validações; preserve funcionalidade e não altere outras
  skills sem autorização.

VALIDAÇÃO FINAL
- Não declare sucesso apenas porque o Markdown abre.
- Verifique referências e scripts de ponta a ponta quando seguro.
- Cite a documentação oficial usada e sinalize inferências.
```

## Exemplo mínimo

Skill alvo = `@hub-ml-eda-profissional`; modo = AUDITORIA; foco = descoberta,
referências relativas, segurança em alto volume e testes representativos.

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Gere o plano de correção sem editar arquivos.”
- “Corrija apenas P0/P1 e valide novamente.”
- “Faça forward test com três prompts positivos e dois negativos.”
