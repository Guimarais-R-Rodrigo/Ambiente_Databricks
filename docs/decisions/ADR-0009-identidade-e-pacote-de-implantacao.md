# ADR-0009 — Identidade neutra e pacote mínimo de implantação

Data: 2026-08-20

Status: Aceito
Autor: Codex, por solicitação de Rodrigo

## Contexto

O ambiente simulado e o roteiro de forward test continham o e-mail pessoal usado
no workspace Free. O identificador não era corporativo nem secreto, mas tornava
o material pouco portável e contrariava a política textual que proibia dados
pessoais no conteúdo ativo. Além disso, os meios de transporte descritos para o
ambiente de trabalho levavam o repositório inteiro, incluindo histórico de
auditoria e material congelado que não é necessário para implantar o produto.

## Decisão

1. Conteúdo ativo e derivado usa identidades neutras. O ambiente simulado é
   renderizado em `Users/usuario-free/`; documentos usam placeholders explícitos.
2. A implantação usa um ZIP mínimo, gerado por
   `tools/bundle_implantacao.py`, com os arquivos do produto e um manifesto de
   hashes. O repositório completo não é o artefato padrão de implantação.
3. `tools/validate_assistant.py` verifica identificadores no conteúdo ativo e
   derivado. Material congelado continua fora do pacote e pode ser coberto pelo
   modo de segurança do bundle de auditoria.
4. Qualquer exceção futura para identidade real exige decisão registrada e
   finalidade explícita; não nasce de uma diferença acidental entre regexes.

## Alternativas consideradas

- Registrar uma exceção para o e-mail pessoal atual — rejeitada: resolveria a
  contradição local, mas manteria o produto acoplado a uma pessoa.
- Transportar o repositório completo — rejeitada como padrão: amplia a superfície
  de exposição e mistura implantação com evidência histórica.
- Excluir todo conteúdo congelado da auditoria — rejeitada: ele permanece útil
  para segurança e forense, desde que não integre o artefato implantável.

## Consequências

- A camada derivada muda de caminho sem alterar o conteúdo funcional.
- O pacote de implantação fica reproduzível e verificável por hash.
- O workspace real é informado somente no momento da publicação, por parâmetro
  explícito; não é persistido no repositório.
- Clone completo continua possível quando deliberadamente autorizado, mas deixa
  de ser o caminho recomendado para implantação.
- A árvore corrente fica neutra, mas commits anteriores ainda retêm o antigo
  path pessoal. Git completo fica bloqueado para transporte corporativo até
  reescrita coordenada/auditoria do histórico; o ZIP mínimo não leva a história.
