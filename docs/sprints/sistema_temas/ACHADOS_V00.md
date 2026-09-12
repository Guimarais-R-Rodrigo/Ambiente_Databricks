# Achados V00 — não corrigir o legado silenciosamente

## A01 — Baseline avançou depois do planejamento

O plano consultou `f748c144`; a main atual observada foi `8744157`. O commit novo
integra a Concierge. O gate executável atual contém sete etapas, não quatro.
Fonte: `tools/ci_local.py` e histórico do commit base. A execução usa o estado
atual sem mesclar outras frentes nem remover etapas.

## A02 — R01 separada e numeração de decisão em colisão

O PR #5 está draft, aberto e não mesclado na consulta de 12/09/2026. A R01 propõe
ADR-0011 para READMEs, enquanto a main já usa ADR-0011 para Concierge. Isto exige
reconciliação na integração pertinente, não renumeração automática nesta sprint.
A V01 deverá verificar novamente a numeração disponível antes de criar decisão.

## A03 — Comando geral de renderer divergente

`tools/README.md` apresenta `tools/render_readme_visuals.mjs` como comando geral.
`tools/readme_visuals/README.md` e `package.json` identificam a produção v2.
V00 registra a divergência. Não executa o renderer antigo sobre o pacote ativo.
A reconciliação editorial fica separada do diagnóstico para não alterar sua base.

## A04 — Validação visual não é operação somente leitura

`tools/readme_visuals/validate_production.mjs` grava QA em
`ambiente_fonte/.assistant/hub_readmes_visual_assets/qa/validation.json` e compara
parte do produto com o commit editorial `f5461d8`. Uma alteração legítima posterior
pode falhar nesse contrato histórico. A execução usa worktrees descartáveis e
registra separadamente a falha na base e na candidata; não atualiza hashes para
fazer passar nem chama uma validação falha de sucesso.

## A05 — Guia de validação com contagem histórica

`.claude/skills/validar-assistant/SKILL.md` ainda descreve treze skills em sua tabela,
enquanto a integração da Concierge alterou o conjunto ativo. A saída executada e
a política atual, não a tabela desatualizada, determinam o que o gate verifica.
Reconciliar na manutenção documental pertinente, sem certificar plataforma remota.

## A06 — Cobertura automática não substitui revisão nominal

O inventário separa candidatos e mantém `revisado: false`. Regex não pode decidir
sozinho se uma cor significa alerta, classe estatística ou identidade de marca.
Imports dinâmicos e relativos exigem completar o grafo. Nenhuma afirmação de
“todos os consumidores revisados” está autorizada por esse JSON.

## A07 — Ambiente real e independência da auditoria

Testes executados em runner GitHub não são testes no Free ou no trabalho. Não há
capturas reais de navegador Databricks nesta execução. A revisão do próprio autor
não será denominada auditoria independente. Ambos são pendências de saída.

## A08 — Falha global observada e anterior à V00

Na rodada 34703259496, o validador global falhou tanto na base quanto na candidata
com ENOENT ao tentar ler `ambiente_fonte/.assistant/CATALOGO_HELPERS.md`, arquivo
retirado pela consolidação do Manual. O QA versionado anterior não é resultado
desta execução. V00 não recria um catálogo concorrente nem altera o validador
histórico para esconder essa falha. A segunda rodada executa também cada família,
com alcance explícito; PASS de famílias não equivale a aprovação global.

## A09 — Contagens locais do README afetadas pela nova documentação

O gate da base passou. Na primeira candidata, a inclusão dos instrumentos e
documentos aumentou as contagens locais de arquivos e links. A correção limita-se
às duas linhas da saída local do README raiz, obtidas de nova execução real.
Não altera bloco remoto, resultado analítico, instrução de produto ou gate.

## A10 — Contagem de skips na primeira instrumentação

A primeira versão do agregador contou duas vezes sete skips, porque o gate imprime
novamente o resumo unittest. A rodada inicial registrou 14; o número real era 7.
A correção usa somente a linha original de unittest e acrescenta teste para a
repetição. Evidência inicial é histórica, não uma segunda execução dos skips.
