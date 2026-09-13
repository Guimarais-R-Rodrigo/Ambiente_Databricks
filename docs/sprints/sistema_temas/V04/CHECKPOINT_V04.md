# Checkpoint V04 — componentes HTML e tabelas

## Estado vigente

V04 em branch `codex/temas-v04-html-20260912`. Foi iniciada sobre a `main`
`b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2` e reconciliada com a `main`
`d9da056c95bf5c4209b2f208de1c9a987580efe7`, que acrescentou a R04-B.
A reconciliação verde está no commit
`c2b91c5e3a3d80f754045dfc4fae8eb335e31bef`; a candidata final ainda precisa
incorporar documentação/derivados e repetir os gates.

| Gate | Estado |
|---|---|
| Implementação funcional | EM VALIDAÇÃO FINAL |
| Regressões automatizadas | EM VALIDAÇÃO FINAL |
| Documentação operacional | EM FINALIZAÇÃO |
| Reconciliação R04-B | PASS no run `34727070003` |
| Auditoria independente | PENDENTE |
| Avaliação com usuário iniciante | PENDENTE |
| Homologação visual/runtime Databricks | NÃO EXECUTADA |
| Aceite do mantenedor | PENDENTE |
| Integração Git | NÃO AUTORIZADA AINDA |
| Publicação Databricks | FORA DE ESCOPO |

A instrução para seguir à próxima etapa autorizou executar a V04; ela não é
tratada como aceite antecipado da candidata final.

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

## Critérios para considerar a candidata tecnicamente pronta

Todos devem estar satisfeitos na mesma árvore:

1. APIs legadas com assinaturas preservadas;
2. referência visual compatível com o legado;
3. 29 testes V04 sem falha ou skip oculto;
4. regressões V01–V03 e V00 aprovadas;
5. `validate_assistant.py --conferir-readme` aprovado;
6. `tools/ci_local.py --verbose` aprovado;
7. `__init__.py` regenerados pela ferramenta canônica de API;
8. `Novo_Ambiente_Simulado/` regenerado pelo renderer, nunca editado à mão;
9. documentação dos objetos reconciliada com o novo comportamento;
10. workflows transitórios ausentes da árvore candidata final;
11. `main` reconferida antes de abrir/congelar o PR;
12. nenhuma mudança acidental nos arquivos específicos da R04-B fora dos
    agregadores/documentos deliberadamente atualizados;
13. suplemento R04-B executado com Spark real na composição reconciliada.

## Critérios que permanecem humanos/operacionais

Mesmo com todos os testes verdes, continuam separados:

- leitura por usuário iniciante;
- julgamento de aparência no notebook real;
- contraste e acessibilidade percebida;
- comportamento no `displayHTML` do workspace-alvo;
- aprovação arquitetural/editorial da candidata;
- eventual publicação e rollback operacional.

Nenhum desses itens pode ser convertido em PASS porque um teste local terminou
com exit code 0.

## Recuperação

Antes do merge, a recuperação é simplesmente arquivar/fechar a candidata. Não há
nada a desfazer no Databricks.

Depois de eventual integração, qualquer reversão deve ser feita por PR sobre a
`main` vigente, preservando mudanças posteriores e repetindo os gates. Não usar
force-push nem publicar um pacote antigo para reverter uma mudança Git.

## Próximo ponto de parada

Quando a árvore final estiver verde, abrir/atualizar o PR da V04 com SHA, árvore,
runs e limites. **Parar para aceite explícito antes do merge.** V05 não começa
por conclusão automática da V04.

[Voltar à V04](README.md)
