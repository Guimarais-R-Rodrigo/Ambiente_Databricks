# ADR-0003 — Quarentena local do Ambiente_Antigo (fora do git)

Data: 2026-08-13
Status: Aceito
Autor: Claude (pendente de ratificação por Rodrigo)

## Contexto

O export original do ambiente do trabalho (`Ambiente_Antigo/`, 153 arquivos)
contém o identificador corporativo real do usuário (username de rede + domínio
do banco) em pelo menos 7 arquivos. O repositório GitHub é privado, mas:
(1) subir identificador corporativo de banco para GitHub pessoal pode violar
política interna; (2) histórico git torna a remoção posterior trabalhosa
(rewrite + force push). Os arquivos já estavam staged e foram retirados do stage
antes do primeiro commit.

## Decisão

`Ambiente_Antigo/` permanece **local-only**, listado no `.gitignore`. A
rastreabilidade histórica no git é dada por `Ajustes_Codex/` (que descreve e
corrige o original e foi verificado como livre de identificadores).

## Alternativas consideradas

- Versionar como está — rejeitada: risco de compliance sem benefício
  proporcional.
- Versionar cópia sanitizada (substituir o identificador por placeholder) —
  viável; adotar apenas se a rastreabilidade local se mostrar insuficiente.
  Reverte esta decisão via novo ADR.

## Consequências

- O ambiente antigo não acompanha clones do repositório; análises comparativas
  exigem esta máquina (ou a criação futura da cópia sanitizada).
- Checks de identificadores pessoais em `tools/validate_assistant.py` cobrem o
  restante do repositório para impedir reintrodução.

## Ratificação de 2026-08-20

Rodrigo confirmou que o projeto será compartilhado com outras pessoas. O
ADR-0009 complementa esta decisão: identidades reais também saem do conteúdo
ativo e derivado, e o transporte padrão passa a ser um pacote mínimo sanitizado.
A quarentena de `Ambiente_Antigo/` permanece inalterada.
