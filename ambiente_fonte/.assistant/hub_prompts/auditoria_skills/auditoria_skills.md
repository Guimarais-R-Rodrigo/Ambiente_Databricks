# Prompt: auditoria de implementação ou output de skill

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe a pasta/arquivos da skill com
> **Add context**/`@`. Skill: `@hub-ml-auditoria-skills`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md).

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

## Follow-ups úteis

- “Gere o plano de correção sem editar arquivos.”
- “Corrija apenas P0/P1 e valide novamente.”
- “Faça forward test com três prompts positivos e dois negativos.”
