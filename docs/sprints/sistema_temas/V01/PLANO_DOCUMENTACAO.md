# Documentação como parte do produto

Status: plano de integração V01. O Manual Técnico e os READMEs operacionais
atuais não foram reescritos; os textos aqui descrevem uma capacidade candidata.
O [guia do usuário](GUIA_PRIMEIRO_USO.md) é um roteiro de primeira utilização,
não um glossário ou catálogo concorrente.

## Fontes únicas e escala de cada documento

| Assunto | Dono atual / destino | Quem mantém e como testar |
|---|---|---|
| Razão arquitetural | ADR-0013 proposto; aceito só por decisão explícita. | Responsável técnico; revisão independente e consistência com ADRs existentes. |
| Campos/limites/defaults | Schema candidato V01; promover após aceite para padrão de identidade visual. | Mantenedor; validação e mutantes do contrato. |
| Referência dos tokens | TOKENS.md derivado do schema. | Geração por ferramenta; comparação byte a byte. |
| Estados/papéis | Política de workflow candidata e sua explicação. | Dono do processo e segurança; revisão e testes de autorização real nas extensões. |
| Primeira utilização | README da futura entrada/laboratório, ligado ao Manual. | Dono da funcionalidade; iniciante deve executar sem instrução verbal. |
| Conceitos transversais e operação do Hub | Manual Técnico canônico no produto. | Editar a fonte, sincronizar raiz e gerar simulado; comparação entre três cópias. |
| Uso específico de componente | README junto ao objeto + exemplo existente. | Mantenedor do objeto; aplicar template efetivamente integrado na base atual. |
| Evidência de uma execução | Relatório e logs datados, imutáveis após fechamento. | Executor; identificar commit/ambiente/status e separar autoria de auditoria. |
| Implantação/retorno | Playbooks e kit já existentes. | Publicador; teste de integridade, execução, conferência visual e recuperação. |

No destino técnico planejado, `hub_padroes/identidade_visual/` abrigará o padrão
e `hub_snippets/visual/tema/` abrigará o núcleo. Ainda não existem por esta sprint.
Antes de mover documentos, gerar matriz antigo→novo, corrigir links e impedir
que duas fontes ativas sejam editadas para o mesmo fato. Evidência histórica
permanece histórica; não duplicar schemas ativos.

## Integração com o trabalho paralelo de READMEs

A main mudou durante a V01 e integrou R01/R02 com Concierge. O ADR-0012 foi
ocupado por essa frente. A candidata usa ADR-0013 e preserva o baseline local;
a reintegração precisa ler os templates e checkpoints da nova main. Não
copiar regras antigas sobre nomes de APIs nem criar um segundo template de
quinze seções. V01 cria documentos de governança, não um novo objeto operacional.

Em V02 e seguintes, novo objeto recebe README, exemplo, requisitos e limites
pelo contrato vigente no commit de integração. Alterar componente já existente
exige atualizar sua documentação na mesma sprint; nenhum texto pode prometer
parâmetro, botão, destino ou suporte ausente.

## Conteúdo mínimo por procedimento

Cada procedimento deve informar público, objetivo, pré-requisitos verificáveis,
ponto de entrada real, ação passo a passo, resultado esperado, alcance,
persistência, desfazer/recuperar e suporte. Variantes de ambiente e dependências
são explícitas. “Configure o ambiente” sem dizer o que conferir não é passo
operacional. “Execute tudo” não é orientação aceitável para trocar aparência.

Exemplos devem usar dados sintéticos. Capturas precisam corresponder à versão
homologada, mostrar o tamanho real de leitura, não conter informações sensíveis
e possuir descrição textual. Esta V01 não usa desenho de tela como prova de
execução. Caminhos fictícios só podem aparecer como proposta claramente marcada,
nunca como comando pronto do usuário.

## Revisões e atualização

V03/V04 atualizam helpers e exemplos ao adaptar. V05 transforma o roteiro em
guia de clique real, incluindo alternativa sem seletor visual. V06 documenta
assets e geração. V08 consolida ligações com skills/padrões/Manual. V09 integra
kit. V10/V11 recebem guias específicos de App e AI/BI sem confundir as superfícies.
V12 testa jornadas com pessoas; V13/V14 consolidam operação e suporte.

Não esperar V08 para documentar uma função já modificada. V08 é a integração
transversal, não uma licença para acumular dívida de documentação.

## Testes editoriais e aceite

Verificar links locais, headings, navegação e correspondência de nomes com
código. Testar blocos executáveis no ambiente declarado, não apenas sua sintaxe.
Verificar legibilidade e compreensão com iniciante: a estrutura de quinze
seções não prova qualidade didática. Registrar participante autorizado, versão
do documento, tarefa, duração observada e qualquer ajuda recebida; nunca
inventar tempos. Os registros humanos desta V01 permanecem vazios e pendentes.

Uma mudança na interface exige revisão da seção afetada, não apenas changelog.
Uma alteração no schema exige regenerar TOKENS, rever exemplos, mensagens e
matriz de testes. Novos tokens exigem consumidor real ou indicação inequívoca
de cobertura adiada; controles sem efeito não entram como funcionalidade pronta.

[Voltar à V01](README.md)
