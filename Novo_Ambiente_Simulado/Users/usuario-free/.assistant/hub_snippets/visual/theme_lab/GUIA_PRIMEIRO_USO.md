# Primeiro uso — Aparência do Hub

**Estado:** guia da candidata V05. Não representa instalação ou homologação no seu Databricks. O mantenedor entrega o pacote e as dependências preparados. O operador não precisa de Git, Node ou CLI para usar o painel.

## 1. Onde começar

Na cópia autorizada do Hub, abra `.assistant/hub_snippets/visual/theme_lab/`. Leia [README.md](README.md) e execute [exemplo_theme_lab.py](exemplo_theme_lab.py) como notebook. Não existe um menu nativo do Databricks chamado “Aparência do Hub”; esta é uma interface customizada do projeto.

## 2. O que o mantenedor prepara

O pacote completo precisa estar disponível; copiar apenas `theme_lab.py` não basta. O caminho `.assistant` deve estar configurado no notebook e as dependências instaladas pelo mecanismo permitido no ambiente.

Para preservar sessões, o mantenedor fornece uma pasta regular já existente, fora da fonte do Hub, com acesso controlado. O laboratório não cria a pasta, não descobre ACL e não publica nada por causa desse caminho.

## 3. Abrir a entrada guiada

A rota recomendada para um usuário iniciante é `build_theme_lab_launcher()`.

```python
from hub_snippets.visual.theme_lab import build_theme_lab_launcher

launcher = build_theme_lab_launcher(save_root=PASTA_DE_RASCUNHOS)
display(launcher.root)
```

`PASTA_DE_RASCUNHOS` é fornecida pelo mantenedor. Sem ela, o laboratório continua permitindo prévia, mas persistência/reabertura ficam indisponíveis.

A tela deve informar que escolher uma opção **não a torna aprovada** e que nada será publicado.

## 4. Escolher o ponto de partida

O dropdown **Ponto de partida** mostra as opções preparadas. As referências empacotadas de demonstração aparecem marcadas como **demonstração**; isso é proposital. Elas servem para testar o laboratório e compatibilidade, não para afirmar que existe um tema operacional aprovado.

Selecione uma opção e clique **Abrir ponto de partida**. O editor aparece abaixo. Um preset inexistente ou incompatível não é substituído silenciosamente por outro.

## 5. Mudar uma cor e aplicar

Em **Escolher e ajustar**, use **Cor principal**. Se digitar HEX, use `#` mais seis dígitos. Clique **Aplicar na prévia**.

Todos os campos habilitados são validados em conjunto. Um erro preserva o último rascunho válido. Campos desabilitados não possuem consumidor correspondente nesta galeria; o motivo é exibido junto ao controle.

## 6. Comparar

Abra **Comparar**. Base e proposta usam os mesmos dados sintéticos em cabeçalho, KPI, barras, série temporal, heatmap e tabela. Mudanças permitidas são visuais; valores, nomes e ordem dos dados devem permanecer iguais.

A galeria completa usa `mode=light`. Tema escuro e alto contraste não são simulados como se estivessem homologados, porque o adaptador Plotly V03 ainda os recusa.

Se os controles aparecerem, mas o frontend não renderizar as figuras, use `compare_preview(draft)` fora do painel e registre runtime/navegador. Não instale JavaScript arbitrário para forçar a saída.

## 7. Desfazer e restaurar

**Desfazer** volta ao estado aplicado anterior. **Restaurar este campo** muda somente o formulário até clicar Aplicar. **Restaurar ponto de partida** volta à base original e pede confirmação quando há trabalho a descartar.

O histórico em memória é limitado. Para continuar em outra sessão, use o salvamento rastreável descrito abaixo.

## 8. JSON avulso e sessão rastreável são diferentes

**Exportar JSON** ou `save_proposal()` preserva apenas a configuração atual. É útil quando o entregável desejado é o JSON canônico da proposta.

**Salvar sessão rastreável** preserva também a origem e o histórico necessários para continuar a autoria. O laboratório cria uma pasta com:

```text
<nome-da-sessao>/
  base.json
  proposal.json
  history-000.json ...
  session.json
```

`session.json` é gravado por último e registra hashes da base, proposta e histórico, além da revisão. Ele não contém aprovação, usuário autenticado ou autorização de publicação.

## 9. Salvar uma sessão

Depois de aplicar todos os campos, informe um nome simples em **Sessão** e clique **Salvar sessão rastreável**.

Uma sessão existente nunca é sobrescrita. Se houver campos digitados mas ainda não aplicados, a operação é recusada para impedir que a tela mostre uma proposta enquanto outra revisão é salva.

Após sucesso, o dropdown de sessões é atualizado. O recibo confirma a sessão local e sua linhagem; não significa submissão ou aprovação.

## 10. Reabrir sem escrever código

Em outra execução do launcher, escolha a sessão no dropdown **Sessão salva** e clique **Reabrir sessão**.

O laboratório confere o manifesto e os hashes, revalida `base.json`, `proposal.json` e o histórico e restaura:

- a base original;
- a proposta atual;
- o histórico salvo;
- o número de revisão.

A proposta **não vira uma nova base**. Se `proposal.json` ou outro arquivo não corresponder ao hash, a reabertura falha. Não altere o hash para “consertar”. Uma pasta parcial sem `session.json` não aparece como sessão disponível.

## 11. Falhas de gravação

- `LAB_SAVE_ROOT` / `LAB_SESSION_ROOT`: peça conferência da pasta e permissões;
- `LAB_SAVE_EXISTS` / `LAB_SESSION_EXISTS`: escolha outro nome; nada existente é sobrescrito;
- `LAB_SAVE_IO` / erros de sessão: não houve confirmação de sucesso; peça inspeção ao mantenedor;
- `LAB_SESSION_HASH`: os bytes não correspondem à sessão registrada; não reabra como válida.

O laboratório não é uma sandbox contra outro processo hostil e não substitui controles de acesso do ambiente.

## 12. Sem ipywidgets

O fallback com `dbutils.widgets` cobre os campos primários, não a experiência completa do launcher:

```python
from hub_snippets.visual.theme_lab import install_dbutils_fallback, apply_dbutils_fallback

nomes = install_dbutils_fallback(rascunho, dbutils)
# ajuste os widgets e depois reexecute:
apply_dbutils_fallback(rascunho, dbutils)
```

Essa rota exige reexecução da célula de aplicação e não oferece catálogo de sessões/presets com a mesma ergonomia.

## 13. O que continua fora da V05

A V05 não implementa submissão, aprovação ou publicação compartilhada. Não recolore PNGs, não migra notebooks antigos, não configura Databricks App e não altera dashboards AI/BI.

Também permanecem pendentes como homologação separada: frontend Databricks real, teclado/leitor de tela, zoom, contraste percebido, p95 da prévia, permissões reais do destino e teste por usuário iniciante sem ajuda.

## 14. Teste de primeiro uso — pendente

O UAT deve entregar este guia e o notebook preparado, sem ajuda verbal inicial. Registrar se a pessoa consegue escolher uma base, alterar e comparar, salvar sessão, encerrar/reabrir, explicar qual era a base original e dizer corretamente quem foi afetado pela mudança.

Teste Python automatizado não substitui esse UAT.

[Voltar ao README](README.md)
