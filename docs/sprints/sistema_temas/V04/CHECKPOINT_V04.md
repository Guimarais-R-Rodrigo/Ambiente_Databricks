# Checkpoint V04 — componentes HTML e tabelas

## Estado vigente

A V04 foi iniciada sobre a `main`
`b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2` e reconciliada sucessivamente com
R04-B, R05 e R06. A reconciliação final foi validada no run `34731698772` sobre
a base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. Rodrigo concedeu aceite
explícito em 12/09/2026 com a instrução `Aceito, siga`, e a V04 foi integrada
pelo PR #21 no commit `5a7b33d7137f88c1ec80315de1b422293b3ba206`.

A árvore do merge é `d2364100d3ed92d1a912f2261ffa2c9f25fc2a8c`, exatamente a mesma árvore da
candidata final validada. Os seis workflows permanentes executados após o merge
na própria `main` concluíram com `success`.

| Gate | Estado |
|---|---|
| Implementação funcional | ACEITA E INTEGRADA |
| Regressões automatizadas | PASS na candidata (`34731698772`) e 6/6 checks pós-merge `success` |
| Documentação operacional | PARCIALMENTE RECONCILIADA — documentos de estado atualizados; rótulo do Manual e nota pré-merge do CHANGELOG ainda exigem sincronização integral segura |
| Reconciliação R04-B | PASS no run `34727070003` |
| Reconciliação R05/R06 | PASS no run `34731698772` |
| Auditoria independente | PENDENTE |
| Avaliação com usuário iniciante | PENDENTE |
| Homologação visual/runtime Databricks | NÃO EXECUTADA |
| Aceite do mantenedor | ACEITO — 12/09/2026 (`Aceito, siga`) |
| Integração Git | CONCLUÍDA — PR #21 / `5a7b33d7137f88c1ec80315de1b422293b3ba206` |
| Publicação Databricks | FORA DE ESCOPO / NÃO EXECUTADA |

O aceite explícito autorizou a integração Git da V04. Ele não autoriza publicação
Databricks, homologação visual/runtime, auditoria independente nem reclassifica
SKIP, PENDENTE, BLOQUEADO ou NÃO TESTADO como PASS.

### Pendência documental mecânica

O estado corrente da V04 é definido por este checkpoint, pelo README V04, pelos
índices da iniciativa e pelo `CLAUDE.md`. O Manual Técnico integrado ainda contém
o rótulo textual histórico `V04 (candidata)` na seção acrescentada pela sprint, e
o `CHANGELOG.md` mantém a nota pré-merge de que a V04 era candidata. O conteúdo
funcional desses registros não muda o código integrado, mas os rótulos precisam
ser sincronizados em uma operação que preserve integralmente os arquivos grandes.

A conexão GitHub desta sessão oferece substituição integral, não patch parcial,
para esses arquivos. Não se reescreveu nem truncou o Manual/CHANGELOG apenas para
alterar uma linha. Até essa sincronização, não trate os rótulos antigos como estado
vigente nem declare a documentação integralmente reconciliada.

## O que muda para quem usa o Hub hoje

Nada é obrigatório. As funções sem sufixo `_resolvido` continuam sendo o caminho
legado. Não existe tema global ativo, seletor instalado ou alteração automática
de notebooks.

Quem optar pela V04 precisa primeiro obter um `ResolvedTheme` notebook pelo
núcleo V02 e passá-lo explicitamente à função nova. Exemplo:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.badge import badge_status_resolvido

tema = load_reference_theme("notebook")
html = badge_status_resolvido("Conferido", tema, "ok")
```

## Critérios técnicos satisfeitos para a integração

A árvore integrada preserva os critérios definidos para a candidata:

1. APIs legadas com assinaturas preservadas;
2. referência visual compatível com o legado;
3. 29 testes V04 sem falha ou skip oculto;
4. regressões V01–V03 e V00 aprovadas;
5. `validate_assistant.py --conferir-readme` aprovado;
6. `tools/ci_local.py --verbose` aprovado;
7. `__init__.py` regenerados pela ferramenta canônica de API;
8. `Novo_Ambiente_Simulado/` derivado da fonte, sem edição editorial independente;
9. documentação dos objetos reconciliada com o novo comportamento;
10. workflows transitórios ausentes da árvore final;
11. `main` reconferida antes do merge;
12. mudanças específicas R04-B/R05/R06 preservadas fora dos agregadores deliberadamente reconciliados;
13. bateria final de reconciliação concluída antes de congelar a candidata;
14. árvore do merge idêntica à árvore candidata;
15. seis workflows permanentes pós-merge concluídos com `success`.

## Critérios que permanecem humanos/operacionais

Mesmo com a integração Git concluída, continuam separados:

- leitura por usuário iniciante;
- julgamento de aparência no notebook real;
- contraste e acessibilidade percebida;
- comportamento no `displayHTML` do workspace-alvo;
- auditoria independente;
- eventual publicação e rollback operacional.

Nenhum desses itens é convertido em PASS porque os testes Git/local terminaram
com exit code 0.

## Recuperação

Como a V04 já está integrada, qualquer reversão deve ser feita por PR sobre a
`main` vigente, preservando mudanças posteriores e repetindo os gates. Não usar
force-push nem publicar um pacote antigo para reverter uma mudança Git.

## Próximo ponto de parada

A V04 está formalmente aceita, integrada e revalidada no Git. O próximo
desenvolvimento planejado da iniciativa é a V05. Este fechamento documental não
inicia a V05, não publica no Databricks e não encerra os gates humanos/operacionais
pendentes acima. A sincronização segura do Manual/CHANGELOG permanece uma pendência
de documentação, não uma pendência funcional da integração V04.

[Voltar à V04](README.md)
