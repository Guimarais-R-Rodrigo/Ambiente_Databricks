# Handoff — R01-A: contrato de README de objeto

Data: 2026-09-12
Autor: ChatGPT
Base: `f748c144dbb6909c7437b53498b25dd4f4854ab7`
Branch: `docs/readmes-objetos-r01a`
Estado: implementação documental candidata; integração e aceite pendentes

## Pedido e fronteira

Executar somente a primeira micro-sprint da decomposição autorizada: ADR,
template geral, contrato de objeto, checklist e regra editorial. Pausar antes
da R01-B. Não gerar os READMEs operacionais nesta entrega.

A base posterior ao planejamento contém o Concierge experimental em
`novas_funcionalidades/`. Essa entrega é preservada, assim como o produto fora
dos templates de README. Nenhuma mudança de API, comportamento analítico,
formulário colável, instrução operacional de skill ou publicação é autorizada
por este trabalho documental.

## Arquivos deste bloco

| Situação | Arquivo | Alteração |
|---|---|---|
| Novo | `docs/decisions/ADR-0011-readmes-de-objeto.md` | proposta de camada documental por pasta; adoção gradual e limites |
| Novo | `ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md` | contrato candidato com abertura, quinze seções e critérios de conteúdo |
| Novo | `ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md` | revisão manual técnica/didática e bloqueios de aceite |
| Atualizado | `.claude/rules/docs-e-readmes.md` | nível Objeto, fonte única do contrato, transição e preservação de identificadores |
| Atualizado | `ambiente_fonte/.assistant/hub_padroes/readme/template.md` | rota para escala Objeto sem substituir as escalas agregadoras |
| Atualizado | `docs/decisions/README.md` | entrada do ADR-0011 como proposto |
| Atualizado | `CLAUDE.md` | rota para proposta e este checkpoint, sem marcar decisão como aceita |
| Novo | `docs/handoffs/2026-09-12-r01a-contrato-readmes.md` | este registro de execução, limites e continuidade |

Não foram criados READMEs de objetos operacionais nem dos exemplares. Os quatro
arquivos preexistentes acima foram reconstruídos para edição somente após
conferência de seus Git blob SHAs com a base lida pelo conector. O diff das
alterações é parte da revisão; a lista não inclui arquivos apenas consultados.

## Decisões do contrato candidato

As quinze perguntas são comuns, mas subtópicos e profundidade são condicionais.
Não há quota de palavras nem lista artificial de alternativas. A abertura dá
acesso direto ao exemplo. O README ensina e ajuda a escolher; notebook,
implementação, formulário e Manual mantêm responsabilidades próprias.

O checklist separa texto escrito, revisado e aceito; revisão documental e teste
operacional; fonte histórica e verificação atual. Erros materiais não podem
ser compensados por uma nota de estilo. A versão permanece
`objeto-v0.1-candidata`; somente o piloto R02 poderá estabilizá-la.

## Verificações e limites

Leituras do GitHub foram fixadas no commit de base. A reprodução dos quatro
arquivos editados foi conferida pelo hash de blob Git. Foi preparada conferência
local de escopo, quinze títulos/ordem, cercas Markdown, links introduzidos e
consistência do estado candidato. Essa conferência é específica desta entrega,
não substitui nem altera `tools/validate_assistant.py` ou `tools/ci_local.py`.
O resultado efetivamente obtido deve acompanhar o relatório de entrega.

O clone via Git não funcionou neste ambiente: `Could not resolve host:
github.com`. A leitura e escrita pelo conector continuam possíveis, mas não
houve checkout integral para executar o renderer ou os gates locais do projeto.
Não foi executado notebook, Spark, teste conversacional, teste no workspace,
publicação ou auditoria independente. Uma autorrevisão não é A1+.

## Pendências obrigatórias antes de integração

1. Incorporar a entrada desta sessão no `CHANGELOG.md` da raiz sem modificar o
   histórico. A entrada e seu patch aditivo estão no pacote de entrega. O arquivo
   extenso da raiz foi preservado: o conector expõe substituição integral, não
   aplicação de patch; não foi feita reconstrução manual do histórico.
   Este handoff não substitui a obrigação de registrar o changelog.
2. Em checkout integral, aplicar a inserção aditiva conferindo a base, executar
   `python tools/validate_assistant.py`, regenerar exclusivamente por
   `python tools/render_simulado.py` e executar `python tools/ci_local.py`.
   Resolver diferenças documentais/contagens produzidas pelos gates no escopo
   autorizado; não editar o simulado manualmente nem inventar saídas aprovadas.
3. Registrar o resultado real da CI do PR. A existência do workflow não é prova
   de execução nem de aprovação. Não fazer merge com pendências materiais.
4. Obter revisão/aceite do contrato R01-A antes de iniciar R01-B. Manter ADR-0011
   como proposto até ratificação real; preservar o registro desta condição.

A branch é de revisão e não representa pacote publicável. O Manual e suas
cópias ficaram intactos. O simulado não foi alterado: sua diferença em relação
aos templates de autoria é pendência explícita, não regeneração presumida.

## Retomada

Primeiro fechar as pendências de integração da R01-A, sem refazer textos
aprovados ou ampliar o escopo. Depois da autorização, R01-B atualiza somente
os templates de snippet, script, prompt e notebook. R01-C trata orquestração;
R01-D, validação; R01-E, exemplares; R01-F, auditoria da fundação. O piloto de
objetos operacionais continua na R02. Não executar a próxima micro-sprint como
efeito colateral do aceite deste checkpoint.

## Referências

- [Decisão proposta](../decisions/ADR-0011-readmes-de-objeto.md).
- [Contrato candidato](../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md).
- [Checklist de revisão](../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md).
