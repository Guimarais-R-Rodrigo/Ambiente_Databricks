# Primeiro uso — Aparência do Hub

**Estado:** guia de uma candidata em desenvolvimento. Não representa instalação
ou homologação no seu Databricks. O mantenedor precisa entregar a cópia e o
ambiente preparados. Você não precisa de Git, Node ou CLI para operar o painel.

## 1. Onde começar

Na cópia autorizada do Hub, abra a pasta `.assistant`, depois `hub_snippets`,
`visual` e `theme_lab`. Leia o [README](README.md) e abra
[exemplo_theme_lab.py](exemplo_theme_lab.py) como notebook, não como módulo a importar.
A forma de importá-lo é responsabilidade do mantenedor; não renomeie arquivos.

Não existe um menu nativo Databricks chamado Aparência do Hub. Esse nome identifica
a interface customizada deste projeto. Não procure o laboratório em Configurações
sem que o mantenedor tenha fornecido uma rota verificada.

## 2. O que o mantenedor deixa pronto

O pacote completo precisa estar disponível; copiar apenas `theme_lab.py` não basta.
A primeira célula Python do exemplo deve apontar para a pasta `.assistant` correta,
sem o placeholder `<username>`. As dependências precisam estar instaladas pela
política do ambiente. O notebook não instala nada nem consulta SQL para descobrir
usuário. O operador final recebe a célula preparada.

Para permitir Salvar, o mantenedor fornece pasta de rascunhos existente, fora da
fonte do Hub, com acesso controlado. Deve informar quem tem acesso, retenção e
local de recuperação. Sem essa preparação, Salvar fica desabilitado; não tente
usar uma pasta compartilhada arbitrária.

## 3. Primeira execução, célula a célula

Execute a preparação do caminho. Se a mensagem pedir um caminho autorizado, pare
e encaminhe ao mantenedor. Execute a célula Criar, experimentar e restaurar:
a saída deverá terminar com restauração verdadeira e JSON somente em memória.
Ela demonstra as operações sem salvar e deixa a base restaurada.

Execute Conferir os campos e depois Abrir o painel. Procure a mensagem
**Alterações aqui não mudam o padrão da equipe**. Confira o nome do ponto de
partida e o contexto notebook. A referência sintética empacotada não é tema aprovado.

A partir de agora, use os botões. Não execute novamente a criação do rascunho nem
Executar tudo enquanto houver trabalho a preservar. Isso cria outro estado em
memória. Abra somente um painel por rascunho; sessões simultâneas exigem avaliação
específica e não compartilham aprovação.

## 4. Mudar uma cor e aplicar

Na aba Escolher e ajustar, use Cor principal. Escolha no seletor ou digite `#`
seguido de seis dígitos hexadecimais. Letras minúsculas são normalizadas na aplicação.
O seletor e o texto representam o mesmo campo; nenhum deles publica uma alteração.

Clique Aplicar na prévia. Todos os campos habilitados são validados como conjunto.
Quando houver erro, corrija o campo indicado e aplique novamente. O rascunho válido
não deve mudar parcialmente. Não copie CSS, HTML, URLs ou código para campos de cor.

Abra Avançado para tamanhos e paletas. Limites e unidades vêm do contrato. Um campo
desabilitado não tem componente correspondente nesta galeria; o motivo aparece
junto dele. Não interprete sua presença como funcionalidade já integrada.

## 5. Comparar e interpretar

Abra a aba Comparar. O ponto de partida e a proposta possuem cabeçalho, KPI, barras,
série temporal, mapa de calor e tabela. A mudança é visual; os dados são fixos.
A paleta categórica controla séries, enquanto Cor principal controla títulos e
cabeçalhos. Mudar uma não harmoniza a outra automaticamente.

As barras apresentam quatro séries e quatro posições: N=16 representa os valores
sintéticos exibidos, não pessoas. Na série, N=5 conta posições, incluindo uma ausência.
No mapa, N=9 conta células de uma matriz sintética, não observações de uma estimação.
A tabela inclui negativos e nulos; os KPIs são rótulos ilustrativos, não cálculos de negócio.

A galeria usa modo light. Ela não homologa tema escuro, modo escuro da interface
Databricks, acessibilidade, imagens raster ou aparência de notebooks antigos.
Amostra editorial dinâmica ainda não está disponível nesta candidata.

## 6. Quando aparecem controles, mas não gráficos

Se aparecer apenas o texto Figura Plotly sintética dentro do painel, a capacidade
do frontend não foi comprovada. Não instale JavaScript nem altere permissões para
forçar a apresentação. Execute a célula Comparação fora do painel no mesmo notebook:
ela usa `compare_preview(rascunho)` e exibe as mesmas figuras por `.show()` e os
componentes HTML por `displayHTML`.

Não recrie o rascunho antes dessa comparação. Se nem a rota externa funcionar,
encaminhe versão do runtime, navegador e erro ao mantenedor. Não classifique o
painel como homologado apenas porque os testes Python passaram.

## 7. Desfazer, restaurar e cancelar

Desfazer retorna ao estado aplicado anterior; mantém até cem estados em memória.
Não revoga uma publicação. Restaurar este campo altera apenas o formulário;
clique Aplicar para efetivar aquela restauração na prévia.

Restaurar ponto de partida retorna à base inicial. Quando houver mudanças ou
campos pendentes, marque a caixa de confirmação antes de clicar. Deixá-la
 desmarcada cancela a ação e preserva seu trabalho. Após concluir, ela é desmarcada
novamente. Campos digitados, mas não aplicados, também exigem confirmação antes
de serem descartados por Desfazer.

## 8. Exportar e salvar são coisas diferentes

Antes de qualquer uma das duas ações, clique Aplicar na prévia. Se houver campos
pendentes, Salvar e Exportar recusam a operação, para evitar entregar uma revisão
antiga enquanto a tela mostra outros valores.

Exportar JSON na saída mostra texto canônico e seu hash. **Não cria arquivo.**
Copie somente o JSON completo, sem a linha do hash ou a mensagem explicativa,
conforme o procedimento autorizado pelo mantenedor. Não há persistência só porque
um texto apareceu na saída do notebook.

Salvar proposta só funciona com pasta preparada. Informe nome simples terminado
em `.json`, com letras minúsculas, números, ponto, hífen ou underscore. Não inclua
caminhos. Um nome já existente é recusado, nunca sobrescrito.

Sucesso mostra destino completo, revisão, tamanho e SHA-256. Registre esses dados
sem expor diretórios sensíveis a pessoas não autorizadas. Esse é um rascunho:
ninguém da equipe teve o tema alterado. Os botões Submeter e Publicar continuam
desabilitados porque os serviços não foram implementados.

## 9. Falha ao salvar

Com `LAB_SAVE_ROOT`, peça conferência da pasta existente e das permissões.
Com `LAB_SAVE_EXISTS`, escolha outro nome; o arquivo anterior permanece intacto.
Com `LAB_SAVE_IO`, não houve confirmação: pode existir arquivo parcial. Não o
reimporte como salvo nem apague arquivos para tentar resolver. O mantenedor deve
inspecionar o destino e decidir a recuperação. O laboratório não faz limpeza
recursiva, não apaga arquivos vazios preexistentes e não promete transação de disco.

## 10. Sem ipywidgets

O mantenedor prepara esta rota em células separadas no mesmo notebook, depois de
criar `rascunho`. São controles nativos de texto, não uma cópia completa do painel:

```python
from hub_snippets.visual.theme_lab import install_dbutils_fallback, apply_dbutils_fallback
nomes = install_dbutils_fallback(rascunho, dbutils)
```

Ajuste os sete campos primários no topo. Reexecute somente esta célula de aplicação:

```python
apply_dbutils_fallback(rascunho, dbutils)
```

Depois execute a comparação fora do painel. Reinstalar o fallback preserva os
valores já legíveis; não usa `removeAll()`. Não reutilize o mesmo prefixo para
outro rascunho no mesmo notebook. O mantenedor pode definir prefixo diferente,
igual na criação e na aplicação. Não leia esses widgets em threads ou jobs de
streaming: capture os valores no contexto principal.

A interface nativa exige confirmação visual da correspondência entre valores
impressos e campos. O comportamento de Executar tudo tem limitações documentadas;
esta rota também precisa ser homologada no ambiente-alvo.

## 11. Reabrir uma proposta em outra sessão

Encerrar a sessão pode perder rascunho, formulário e histórico. Um arquivo com
recibo confirmado permite reconstruir o tema, mas não o histórico dos botões.
O mantenedor prepara a leitura com o destino e o hash corretos:

```python
from hub_snippets.visual.tema import load_theme
from hub_snippets.visual.theme_lab import create_theme_lab, build_ipywidgets_lab

tema = load_theme(PASTA_AUTORIZADA, NOME_JSON, expected_sha256=HASH_DO_RECIBO,
                  expected_context="notebook")
rascunho = create_theme_lab(tema)
ui = build_ipywidgets_lab(rascunho)
display(ui.root)
```

As três variáveis em maiúsculas devem ser fornecidas pelo mantenedor; não são
valores a inventar. A pasta não pode mudar de proprietário ou virar atalho
simbólico. Divergência de hash bloqueia a leitura; nunca altere o hash só para abrir.
O arquivo é a nova base de trabalho, ainda sem aprovação ou publicação.

## 12. Teste por uma pessoa iniciante — pendente

A validação humana deve entregar apenas este guia e o notebook preparado. Registrar
se a pessoa encontra o início, muda uma cor, interpreta a comparação, corrige erro,
desfaz, restaura, salva, localiza o arquivo e explica quem foi afetado. Registrar
qualquer ajuda verbal. Testar também teclado, zoom, leitura de mensagens e reabertura.
Não preencher o registro com participante fictício nem converter teste Python em UAT.

[Voltar ao README](README.md)
