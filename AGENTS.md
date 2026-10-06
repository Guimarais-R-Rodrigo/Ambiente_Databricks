# Ambiente Databricks — contrato comum de manutenção

Este repositório desenvolve o ecossistema `.assistant` do Databricks Genie Code.
A manutenção edita o Git, valida, gera o espelho e prepara publicação no Free e
replicação manual no trabalho. Cada efeito precisa estar no escopo autorizado.

## Invariantes

- Este Git é a fonte canônica. Edite o produto somente em `ambiente_fonte/`
  (`.assistant/` e sua instrução irmã); workspaces são cópias operacionais.
- `Novo_Ambiente_Simulado/` é derivado de `tools/render_simulado.py`: nunca
  edite à mão. `--write` substitui toda a árvore; inventarie extras, preserve
  conteúdo alheio e confirme o escopo antes de gerar, preferindo cópia isolada.
- `Ambiente_Antigo/` é quarentena local, congelada e read-only. Não versione,
  publique nem exponha seu conteúdo. Correções pertencem à fonte sanitizada.
- Nenhum identificador corporativo, username real do trabalho, path corporativo,
  PII ou segredo entra no Git, evidência compartilhada ou Free. Use placeholders
  e fixtures sintéticas. A única exceção de identidade é o nome da instituição
  na paleta visual (`AZUL_CAIXA` e afins, `PLANO_HUB.md` §2.2); `CORPORATE_RE`
  não deve proibi-la. A exceção não autoriza qualquer outro identificador.
- No Free, somente dados sintéticos. Dados reais ficam no ambiente corporativo
  autorizado, sob Unity Catalog, regras de PII, compliance e governança local.
- Instrução, skill, template, plano ou teste não concede autorização, ACL,
  ferramenta ou credencial. Permissões reais, políticas gerenciadas e instruções
  superiores prevalecem. Publicação, exclusão, instalação, login, settings,
  conexão/MCP, upload, produção, push e merge exigem escopo próprio autorizado.
- Preserve alterações do usuário e de outros agentes, MCP e arquivos não geridos.
  Não sobrescreva conflito nem escolha a regra mais permissiva: pare a parte
  dependente, mostre as fontes e peça a decisão necessária.
- Validação estática, render, execução, publicação, verificação remota e
  homologação são provas diferentes. Git integrado e transporte não ativam nem
  homologam Databricks, runtime, ACL, aparência, acessibilidade ou aceite humano.
- Use autoria real e papéis por capacidade/independência, sem papel fixo por
  fornecedor. Auxiliares na mesma sessão não são origens independentes.
- Antes de afirmar capacidade/limite de plataforma, consulte fonte oficial
  aplicável à superfície e data. Documento lido não prova cliente instalado;
  estado vivo vem do owner, não de contagem, cota ou resultado histórico.

## Fluxo seguro

1. Confira branch/SHA, diff e escopo autorizado; preserve trabalho alheio.
2. Leia a rota pertinente abaixo antes da ação; links não são imports automáticos.
3. Da raiz, `python tools/validate_assistant.py` valida a fonte localmente;
   `python tools/render_simulado.py` apresenta o plano local sem `--write`.
   Pré-requisitos e demais gates estão em [tools](tools/README.md).
4. Mudança de comportamento exige validação, render autorizado, changelog e
   ADR quando estrutural. Falta de dependência é BLOCKED; não instale nem
   relaxe o gate para mascará-la. Publicar/replicar nunca é continuação implícita.

## Conclusao

Toda sessão com alteração registra em `CHANGELOG.md` data, arquivos e autoria
reais, seguindo o [template](docs/ai/templates/changelog-entry.md). Não leia o
histórico inteiro por padrão; consulte o trecho relevante ao retomar/investigar.
Valide `ambiente_fonte/` antes de concluir e reporte comando, SHA, resultado,
limites e bloqueios: PASS só com observação; NOT_RUN e BLOCKED não são aprovação.
Entregue diff/arquivos, evidência, efeitos realizados e pendentes; mudanças de
arquitetura exigem ADR e a retomada incompleta exige handoff verificável.

## Leitura por tarefa

- Escolher procedimento/owner: [índice comum](docs/ai/README.md).
- Editar produto, Manual ou derivados: [fontes e efeitos](docs/ai/rules/fontes-e-derivados.md).
- Escrever README/relatório/ADR: [documentação](docs/ai/rules/documentacao.md).
- Coordenar, revisar, auditar ou retomar: [colaboração](docs/ai/rules/colaboracao.md).
- Usar Free/trabalho ou interpretar resultado: [ambientes](docs/ai/context/ambientes.md).
- Mudar afirmação Databricks: [referência oficial](docs/ai/references/databricks-genie-code.md).
- Validar, renderizar, publicar, testar roteamento ou replicar:
  [cinco skills do mantenedor](.agents/skills/README.md), nunca skills do runtime.

Este núcleo é independente dos adaptadores; a precedência real depende do
cliente. O contrato editorial não promete autoload nem suporte já demonstrado.
