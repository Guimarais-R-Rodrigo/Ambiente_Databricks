---
name: render-simulado
description: >-
  Confere o plano local e regenera .artifacts/simulado/ a partir de
  ambiente_fonte/ após edição aprovada, com inventário e autorização de
  substituição. Não publica no Databricks nem edita o espelho à mão.
---

# Renderizar o ambiente simulado

## Intenção e pré-condições

Use para preparar o espelho após mudança aprovada na fonte e antes de publicar
ou replicar. Um pedido para apenas conferir diferenças permite preparar o
plano; não implica executar `--write`. Para publicar no Free, siga depois a
[skill própria](../publicar-free/SKILL.md).

O [renderer](../../../tools/render_simulado.py) é o owner. Precisa do checkout
completo e de fonte válida, conferida pela
[validação local](../validar-assistant/SKILL.md). O renderer **não executa o
validador por conta própria**. Fonte inválida ou pré-requisito ausente bloqueia
escrita; relatório antigo não valida mudanças posteriores.

## Plano local e preflight obrigatório

```sh
python tools/validate_assistant.py
python tools/render_simulado.py
```

Sem flags, o renderer mostra origem, destino e dois itens de cópia, terminando
com `DRY-RUN: nada foi escrito. Use --write para executar.` Não acessa Databricks.
O plano não inventaria extras nem concede permissão para removê-los.

Antes de qualquer escrita:

1. Confirme checkout/branch/SHA, mudanças alheias e raiz resolvida do destino.
   O script deriva a raiz do próprio arquivo; o padrão é `.artifacts/simulado/`,
   não a pasta corrente do shell. `--output-root .artifacts/<destino>` seleciona
   outro subdiretório gerado da mesma raiz; escapes e symlinks são recusados.
2. Inventarie **toda** essa árvore, inclusive arquivos ocultos, ignorados e não
   rastreados, diretórios extras/vazios, outros usuários e links simbólicos.
   Compare caminhos e hashes com os dois itens publicáveis de `ambiente_fonte/`,
   com `README_GERADO.md` e com os filtros `IGNORAR` do owner. `git status` sozinho
   não mostra tudo que será removido.
3. Classifique diferenças esperadas do derivado e extras de origem incerta.
   Registre o escopo de substituição. Havendo conteúdo não gerido, divergência
   inexplicada, symlink/escape ou trabalho alheio, pare e reconcilie com o dono;
   não transforme “regenerar” em autorização para perder esse conteúdo.
4. Confirme que a autorização cobre a substituição de **toda a árvore** do
   destino e que conteúdo a preservar tem backup recuperável fora dela.
   Permissão para ler, validar ou selecionar esta skill não cobre exclusão.
5. Para testar o procedimento, use fixture/clone descartável autorizado. Não
   execute `--write` no simulado de trabalho só para provar que funciona. Use
   `--output-root` para saída isolada autorizada. Não há flag `--output` ou
   `--dry-run`: o modo sem flag já é o plano local.

## Escrita e resultado esperado

Somente após o preflight e a autorização suficientes:

```sh
python tools/render_simulado.py --write
```

**Efeito destrutivo:** se o destino existe, `shutil.rmtree` remove
a raiz selecionada inteira (padrão `.artifacts/simulado/`) antes de recriá-la. Extras e edições manuais
seriam perdidos; a operação não é atualização incremental nem transação atômica.
Interrupção pode deixar saída parcial. Pare, inventarie novamente e recupere
conteúdo preservado antes de qualquer retry autorizado.

O placeholder padrão é `usuario-free`, de
[project_policy.py](../../../tools/project_policy.py). Não persista username
real. `--username` aceita componente neutro validado, mas não muda a abrangência
da remoção; prefira o padrão. O mapeamento para a home real ocorre na implantação,
conforme [ADR-0009](../../../docs/decisions/ADR-0009-identidade-e-pacote-de-implantacao.md).

```text
.artifacts/simulado/
├── README_GERADO.md
└── Users/usuario-free/
    ├── .assistant_instructions.md
    └── .assistant/
```

Os dois itens de produto são copiados **byte a byte**, sem headers injetados.
O marcador fica fora do payload. Caches/bytecode e demais padrões `IGNORAR`
não entram na cópia; `ambiente_fonte/README.md` também não é item publicável.
Após exit 0 e `OK: N arquivos renderizados em .artifacts/simulado/`, confira
inventário, hashes fonte/espelho, ausência de extras e diff autorizado. Execute
`python tools/render_simulado.py --check` (com o mesmo `--output-root`, se usado):
o gate exige inventário não vazio e igualdade de paths, bytes/hashes e tipos
FILE/NOTEBOOK. Como a saída é ignorada no Git, `git diff` não prova paridade. Contagem
isolada não comprova igualdade. Nunca edite o derivado à mão; ajuste a fonte.

Registre comando, SHA, preflight, autorização, resultado e diferenças na
evidência datada da tarefa, junto à mudança que motivou o render. A raiz recebe
apenas o marco pertinente, conforme o [critério](../../../docs/ai/templates/changelog-entry.md).
Render concluído não é publicação nem homologação de runtime.

## Casos de aceitação do procedimento

- **Positivo:** fonte válida e pedido explícito de regenerar destino gerido.
  Preparar plano/inventário; só então executar a substituição autorizada.
- **Negativo de intenção:** “Confira apenas o que seria copiado.” Mostrar plano
  sem `--write`, sem exclusão e sem publicação.
- **Pré-requisito ausente:** fonte inválida, extra alheio ou autorização de
  substituição insuficiente. Bloquear escrita e informar o item a resolver.
