# Plano de retirada do localizador do Hub

Data: 08/10/2026. Autor: Codex. Estado: PLANEJADO; inventário concluído.
Base: `041ac7afac1a14763facd173d1fe665b6340ab4b`.
Branch examinada: `codex/organizacao-tools-20261007`, inicialmente limpa.
Escopo desta entrega: análise e plano. Exclusão, migração de referências,
implementação de resolver, push e merge não foram executados.

## Objetivo e conclusão

É viável eliminar `PLANO_HUB.md` da árvore corrente. A construção já está no
[CHANGELOG consolidado](../../CHANGELOG.md), e a decisão vigente tem a âncora
[paleta institucional](../../CHANGELOG.md#paleta-institucional).
O arquivo deixou de conter informação exclusiva; restam referências e
compatibilidade de navegação a tratar antes da exclusão.

O critério de conclusão é **zero dependência vigente do arquivo local**, com
história recuperável. Não é zero ocorrência textual do nome: apagar o nome de
inventários, citações, comandos Git e relatos encerrados falsificaria a história.

## Inventário e método

`git grep -n -i` com os termos `PLANO_HUB`, `plano hub` e `plano do hub`
identificou **106 linhas em 53 arquivos** na base. São linhas correspondentes,
não quantidade de tokens ou chamadas executáveis. Há quatro links Markdown
locais diretos ao arquivo: dois em índices vivos e dois em documentos datados.
Não há referência no produto, workflows ou skills rastreados. Em `tools/`,
existem somente duas menções no validador: um comentário de regra vigente e
uma docstring histórica. Os três scripts em evidências R06/R07/R08 pertencem
a campanhas antigas; devem ser analisados como código histórico, não como
ferramentas atuais. Não havia arquivos novos não ignorados no checkout.

A busca cobriu arquivos rastreados, inclusive fontes Python, JSON e CSV. Não
varreu a quarentena nem dados ignorados. Na execução, repetir a busca também
por variantes de caixa, `plano[_ -]?hub`, links/âncoras, paths construídos e
consumidores indiretos; inventariar arquivos novos permitidos pelo Git.
O derivado deve ser conferido pelo renderer, sem edição ou varredura indiscriminada.
Resultados de busca são candidatos: classificar contexto antes de substituir.

## Sprint 1 — fechar classificação e prova de recuperação

**Situação:** mapeamento inicial concluído nesta entrega.

1. Registrar cada ocorrência com path, linha, classe, ação, destino e hash da
   fonte. Separar regra vigente, índice vivo, link local histórico, citação
   congelada, URL Git e script de campanha encerrada.
2. Reconfirmar bytes do plano integral no commit público
   `09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd`, conforme o
   [ADR-0030](../decisions/ADR-0030-historia-consolidada.md).
3. Conferir a âncora da paleta no consolidado e os destinos históricos §12.2/§12.3
   no plano integral. Não redirecionar relato de dívida antiga para regra atual.
4. Registrar decisão sucessora do ADR-0030, pois ele explicitamente conserva
   o localizador. Utilizar o próximo número disponível no início da execução.

**Saída:** matriz fechada, decisão de retirada e inventário de bytes protegidos.
**Aceite:** toda ocorrência tem tratamento; nenhum relato é tratado como regra.

## Sprint 2 — migrar regras e navegação vigentes

| Arquivo / trecho | Alteração planejada |
|---|---|
| `AGENTS.md:19` | trocar a referência da §2.2 pela âncora de paleta do CHANGELOG, mantendo integralmente o alcance da exceção |
| `docs/ai/rules/fontes-e-derivados.md:27` | usar a mesma âncora vigente para evitar segunda fonte de regra |
| `tools/validate_assistant.py:52` | atualizar apenas o comentário da regra; não alterar regex ou comportamento |
| `docs/sprints/README.md:24` | orientar a leitura pela trajetória consolidada e pelo plano integral congelado para as tabelas antigas |
| `docs/auditoria/README.md:79` | substituir o link local por rota consolidada + origem congelada para os registros das sprints |

Revisar `docs/ai/control-map.json`, o inventário de loaders e a rastreabilidade
após a mudança do núcleo. A citação da origem de `O-C02-22` é congelada e fica
intacta. Ajustar somente registros correntes cuja identidade/roteamento realmente
mude; se necessário, acrescentar revisão encadeada em vez de alterar snapshots.
Regenerar apenas adaptadores geridos que dependam dessa mudança, pelo gerador,
e conferir o diff. Não gerar produto ou simulado como efeito automático.

**Aceite:** as regras vigentes apontam para a mesma decisão, sem ampliação da
exceção institucional; controles IA e navegação continuam aprovados.

## Sprint 3 — resolver os dois links históricos locais

Fontes a preservar:

- `docs/handoffs/2026-09-09_plano-consolidado.md:87`.
- `docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md:12`.

**Recomendação:** manter esses relatos byte a byte e reconhecer exatamente esses
links como referências históricas recuperáveis pelo Git, com um manifesto
específico da retirada. O relatório de 07/10 dizendo que o arquivo era necessário
é um diagnóstico daquela base, substituído pela decisão sucessora; não reescrever
sua conclusão retroativamente.

O resolver atual em `tools/historical_links.py` é restrito ao commit da faxina,
a determinados tipos de fonte e a três classes de destino. Ele **não aceita**
hoje o destino `PLANO_HUB.md`, nem os dois tipos de fonte acima. Acrescentar um
contrato separado e estreito, com fontes explicitamente allowlisted, commits
congelados de fonte e destino, href original, hashes e blob do plano integral.
Usar o plano público integral, não o localizador de 15 linhas. Não adicionar
exclusão genérica para `docs/handoffs/` ou `docs/manutencao/`.

Preservar as 30 referências e o manifesto da faxina existente. O novo conjunto
terá apenas os dois pares de fonte/href aprovados, caso a revarredura confirme
este inventário. O validador deve informar que a recuperação é histórica no Git;
isso não torna o href um link local clicável num ZIP. O índice histórico deve
explicar a rota para consultar a versão integral. Checkout completo permanece
pré-requisito; ausência de commit/blob deve falhar.

Testes específicos: aceitar os dois pares aprovados e rejeitar fonte alterada,
hash errado, origem/target trocado, blob ausente, referência inventada, entrada
obsoleta e tentativa de permitir outra fonte/diretório. Uma fixture positiva
isolada não substitui conferência dos blobs reais do checkout.

**Aceite:** recuperação demonstrada e negativos aprovados; fontes antigas
intactas. Os 30 pares anteriores continuam verificáveis com o mesmo contrato.

## Sprint 4 — revisar citações e código histórico

- Manter quotes, datas, autoria, hashes e URLs congeladas nas auditorias,
  matrizes R00–R13, changelog integral, evidências e ADRs aceitos.
- Manter `CHANGELOG.md` e ADR-0030 como relatos do que ocorreu em 07/10; registrar
  a retirada com nova data, sem reescrever que o localizador foi criado.
- Na docstring histórica `tools/validate_assistant.py:188`, preservar o relato
  dos 11 notebooks e acrescentar, se necessário, uma rota de recuperação com
  commit explícito. Não alterar a regra de saída colada.
- Os scripts de evidência R06/R07/R08 listam arquivos em receitas daquela
  campanha. Verificar se algum teste, ferramenta ou instrução corrente os executa.
  Se não houver consumidor vigente, conservar seus bytes e sinalizar o escopo
  histórico no índice responsável. Se houver, migrar o consumidor atual para
  receita suportada ou documentar sua reprodução em checkout congelado.
- Preservar menções de catálogo como nome de arquivo que existia na época.

**Aceite:** todo resultado residual da busca é citação histórica, link Git ou
referência resolvida pelo manifesto; nenhum fluxo corrente abre o arquivo local.

## Sprint 5 — excluir, validar e entregar

1. Confirmar hashes das fontes protegidas, snapshot de 198 registros e plano
   recuperável; conferir diff e extras antes de excluir o único localizador.
2. Remover `PLANO_HUB.md` somente após as sprints anteriores.
3. Repetir busca e classificar os resíduos. Validar âncoras manualmente ou por
   check específico: existência de um arquivo não garante seu fragmento HTML.
4. Executar os comandos abaixo e os novos negativos do resolver; atualizar o
   snapshot de contagens do README com a saída real. Conferir os 708 pares de
   produto pela ferramenta; não presumir que a contagem continuará igual.
5. Registrar marco datado no consolidado e resultados no owner desta execução.
   A entrada de história está próxima da meta de 200 linhas: avaliar snapshot
   verificável dos marcos recentes, preservando a síntese e a reversibilidade.
6. Fazer revisão A0 de contexto completo declarada, entregar diff, SHA, arquivos,
   resultados e limites. Push, PR/merge e replicação seguem escopos próprios.

```sh
python -B tools/ai_controls.py --check
python -B tools/tests/test_ai_history.py -v
python -B tools/tests/test_ai_historical_links.py -v
python -B tools/package_boundary.py
python -B tools/ci_workflows.py --check
python -B tools/validate_assistant.py --conferir-readme
git diff --check
```

**Aceite final:** arquivo ausente; zero dependência local vigente; todos os links
antigos tratados; snapshots e citações preservados; plano integral recuperável;
gates locais aprovados sem dispensa ampla. Runtime, CI remoto, Copilot e Databricks
não são certificados por esses comandos.

## Rollback e parada

Executar em branch com commits pequenos. Antes da exclusão, os lotes podem ser
revertidos separadamente. Se falhar o resolver, reverter a exclusão restaura a
compatibilidade enquanto se corrige a migração; não afrouxar o validador. Não
usar reset destrutivo nem sobrescrever alterações alheias. Dependência ausente,
história Git indisponível ou conflito bloqueia somente a parte dependente.

## Inventário completo da base

As linhas abaixo pertencem ao SHA inicial, antes de criar este plano. A categoria
é preliminar onde depender de consumidor; Sprint 1 fecha a classificação.

| Arquivo | Linhas encontradas | Tratamento |
|---|---|---|
| `AGENTS.md` | 19 | Migrar rota vigente; conservar relatos datados do índice |
| `CHANGELOG.md` | 4, 42, 118, 133 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `PLANO_HUB.md` | 1, 9 | Excluir ao final |
| `docs/ai/control-map.json` | 1142 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/ai/rules/fontes-e-derivados.md` | 27 | Migrar rota vigente; conservar relatos datados do índice |
| `docs/auditoria/2026-08-18_consistencia-e-didatica/01_rodada_e_consenso.md` | 111 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-08-19_leitura-contexto-longo/01_rodada_e_consenso.md` | 16, 62, 69, 129, 130 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-08-20_segunda-origem-codex/01_rodada.md` | 361 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_ai-instrucoes/reference-scan.json` | 185 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_ai-instrucoes/source-controls.json` | 14 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_ai-instrucoes/traceability.csv` | 44, 57 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_ai-instrucoes/traceability.json` | 2640, 2641, 2654, 2656, 2659, 2666, 3562, 3584, 3599, 3601, 3604, 3606 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_readmes/DISPOSICOES.csv` | 700 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_readmes/DISPOSICOES.json` | 23003, 23015, 23020, 23357, 23374 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/2026-10-06_readmes/S5_CONTEUDO_REALOCADO.md` | 1298, 1350 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/auditoria/README.md` | 71, 79 | Migrar rota vigente; conservar relatos datados do índice |
| `docs/decisions/ADR-0007-catalogo-e-pasta-de-objeto.md` | 89 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/decisions/ADR-0008-criterios-de-conferencia-da-publicacao.md` | 87 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/decisions/ADR-0030-historia-consolidada.md` | 20, 26, 37, 40, 51, 54, 61 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/handoffs/2026-09-09_plano-consolidado.md` | 87 | Preservar bytes; resolver href histórico específico |
| `docs/historico/changelog/2026-08-13_a_2026-10-06.md` | 2576, 2628, 2648, 2660, 2758, 2763, 2868, 2972, 3185, 3287, 3401, 3403, 3470, 3555, 3558 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md` | 12, 174 | Preservar bytes; resolver href histórico específico |
| `docs/sprints/README.md` | 24 | Migrar rota vigente; conservar relatos datados do índice |
| `docs/sprints/readmes_objetos/EVIDENCIAS_R02.json` | 166 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/INTEGRACAO_R02.md` | 76 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R01.md` | 42 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R02.md` | 30 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R03A.md` | 38 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R03B.md` | 24 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R04A.md` | 24 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R04B.md` | 40 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R05.md` | 40 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R06.md` | 38 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R07.md` | 52 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R08.md` | 23, 68 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R09.md` | 24 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/MATRIZ_INTEGRACAO_R02.md` | 77 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R03A.md` | 53 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R03B.md` | 49 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R04A.md` | 47 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R04B.md` | 36 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R05.md` | 48 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R06.md` | 53 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R07.md` | 48 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R08.md` | 17 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/RELATORIO_R09.md` | 15 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/readmes_objetos/evidencias_r06/aplicar_r06.py` | 194 | Verificar consumidores; preservar script de campanha |
| `docs/sprints/readmes_objetos/evidencias_r07/aplicar_r07.py` | 196 | Verificar consumidores; preservar script de campanha |
| `docs/sprints/readmes_objetos/evidencias_r08/aplicar_r08.py` | 203, 315, 355 | Verificar consumidores; preservar script de campanha |
| `docs/sprints/sprint-10-readmes-de-topo.md` | 157 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/sprint-12-fechamento.md` | 7, 128, 129 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `docs/sprints/sprint-9-constants-visual-display.md` | 172 | Preservar citação/registro congelado; conferir ausência de dependência viva |
| `tools/validate_assistant.py` | 52, 188 | Comentário vigente + docstring histórica; tratar separadamente |

## Evidência desta entrega de planejamento

Inventário por `git grep`, árvore inicialmente limpa e leitura dos owners/resolver.
Validação da fonte local: `python -B tools/validate_assistant.py`, exit 0,
APROVADO com zero falhas e zero avisos. O README recebeu as contagens observadas
(1.770 arquivos de identidade e 2.107 links externos à raiz de produto); executar
`--conferir-readme` no fechamento. Revisão própria de contexto completo, nível
A0; nenhuma origem independente presumida. Os testes novos e a exclusão das
sprints futuras são NOT_RUN nesta entrega, pois seu escopo é somente o plano.
