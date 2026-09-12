# ADR-0011 — README didático por pasta de objeto

Data: 2026-09-12
Status: Proposto — contrato candidato entregue na R01-A; aceite pendente
Autor: ChatGPT

## Contexto

O Hub organiza snippets e scripts em pastas com implementação, fachada pública
e notebook de exemplo. Prompts têm formulário e demonstração próprios. Esses
materiais ajudam a usar o recurso, mas um leitor que desconhece o conceito
precisa de uma entrada anterior: entender o que é, quando escolher e quando
não escolher aquele recurso.

O template de README vigente no commit de partida
`f748c144dbb6909c7437b53498b25dd4f4854ab7` distingue escalas agregadoras. O
ADR-0010 mantém no Manual o catálogo integrado e o índice de termos. Acrescentar
um documento local não deve reintroduzir catálogo concorrente, alterar código
nem transformar o notebook numa cópia da introdução.

## Decisão

Adicionar a escala **Objeto** ao tipo README, preservando a taxonomia de tipos
e as escalas Curta, Padrão e Longa. A unidade de documentação será a pasta de
snippet, script ou prompt, não cada arquivo Python, teste, imagem ou célula.

O README explicará conceito aplicado, adequação, entradas, saídas, limitações,
validação e rota de uso. O notebook continuará demonstrando; a implementação e
a fachada continuarão definindo o contrato real; o prompt conservará formulário,
bloco colável e seus controles. O Manual continuará dono do catálogo integrado.

O contrato de autoria terá um único endereço no produto:
`hub_padroes/readme/template_objeto.md`, selecionado pelo `template.md` geral.
O checklist de revisão ficará ao lado. Os títulos principais serão comuns;
subtópicos e profundidade dependerão do objeto. Não usar quota de palavras como
critério de qualidade nem replicar as seções em todas as skills.

Separar capacidade de biblioteca e capacidade implementada, ilustração e
execução, premissa e resultado, evidência histórica e verificação atual.
Afirmações materiais precisam de procedência; código existente não torna uma
explicação científica correta por definição. Achados funcionais serão
registrados, não corrigidos como efeito colateral desta migração.

### Adoção gradual e efeito desta proposta

A R01-A entrega somente contrato candidato, regra editorial, roteamento do
template e registros de governança. Não cria README operacional, não instala
novo gate, não altera APIs e não declara migração dos legados concluída.

A fundação restante fica dividida em R01-B (templates dos tipos), R01-C
(orquestração), R01-D (validação), R01-E (exemplares) e R01-F (auditoria da
fundação). Cada unidade tem relatório e parada. O piloto R02 estabiliza a
versão 1.0 antes da produção em lotes. Mudanças de contrato exigem registro e
reconciliação dos exemplares, não decisões independentes por redator.

A futura cobertura será progressiva: legado identificado, pendências
explicitadas e nenhum objeto aceito regredindo silenciosamente. Este ADR não
implementa essa guarda. Não confundir existência do documento com revisão,
revisão com aceite, ou aceite documental com homologação no Databricks.

### Relação com decisões anteriores

Complementa o ADR-0007 com a camada humana de documentação; não substitui sua
API pública, seus imports ou a pasta de objeto. Preserva o ADR-0010 e o corpo
dos ADRs aceitos. Se a proposta for aceita, registrar a ratificação sem apagar
este estado inicial. Não usar esta entrega para mudar localização do Manual,
identidade visual, política de skills ou publicação.

## Alternativas consideradas

- Um README por arquivo: fragmentaria a explicação da mesma capacidade.
- Somente ampliar o notebook: manteria a barreira de entrada conceitual e
  aumentaria a duplicação entre explicação e execução.
- Somente ampliar o Manual: não criaria uma entrada próxima de cada objeto.
- Um template inteiramente diferente por família: facilitaria deriva e
  dificultaria ao leitor localizar as mesmas respostas.
- Redação massiva antes do piloto: multiplicaria os efeitos de um contrato ruim.

## Consequências

Aumenta a descobribilidade e a possibilidade de decisão informada, ao custo de
mais documentos a manter junto às mudanças de API. Links e informação mutável
precisam de um dono e de revisão; a síntese local não autoriza duplicação longa.

A entrega ocorre em branch de revisão. A fonte permanece em `ambiente_fonte/`.
O simulado não é editado manualmente: sua regeneração e os gates integrais são
pré-requisitos da integração, e publicação no workspace requer autorização
própria. Uma revisão pela mesma IA não satisfaz auditoria independente.

## Referências

- [ADR-0007 — pasta de objeto](ADR-0007-catalogo-e-pasta-de-objeto.md).
- [ADR-0010 — Manual Técnico](ADR-0010-manual-tecnico-unificado.md).
- [Regra editorial](../../.claude/rules/docs-e-readmes.md).
- [Roteador de README](../../ambiente_fonte/.assistant/hub_padroes/readme/template.md).
- [Contrato candidato](../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md).
- [Checklist](../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md).
