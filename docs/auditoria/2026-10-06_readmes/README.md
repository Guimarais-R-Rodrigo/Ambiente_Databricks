# Readequação da documentação do Hub

Esta pasta registra a implementação do [plano aprovado](https://docs.google.com/document/d/1MEXcts9r006ShbxRoHPIKfxehX0nw_nWBNvZVxQ1TCs/edit). A documentação de uso está nas fontes do produto; relatórios, cronologia e reprodução de manutenção ficam aqui.

## Resultado por frente

- S1: entradas e estados administrativos reconciliados com Git e policy; histórico, FAILs e bloqueios preservados.
- S2: entrada do produto e Manual por tarefa; 25 intervenções no Manual, três cópias equivalentes e regras de autoria sem retrospectiva desnecessária.
- S3: catálogo, Micromodelos e oito guias de runners com preparação, chamadas, oráculos, efeitos, recuperação e conclusão.
- S4: briefings e scripts alinhados às skills, com overwrite e efeitos anteriores à execução, campos de retorno e evidência corretamente delimitados.
- S5: snippets gerais, temas e 80 tokens com APIs/limites reais; projeção operacional separada da emissão histórica.
- S6: 30 objetos ML e índice com contratos matemáticos, temporais, dependências, alinhamento e efeitos precisos.
- S7: 61 templates reconciliados, incluindo seis preservações; critérios do caso e evidência ausente/parcial não viram aprovação.
- S8: manifests documentais, pacote completo, cópias e inventário conferidos; imagens e licenças preservadas.

## Rastreabilidade

- [1.135 disposições com evidência específica](DISPOSICOES.json) e [índice CSV](DISPOSICOES.csv)
- [497 registros de origem lidos](FONTES_LIDAS.json)
- [723 caminhos: baseline e correspondência final](CAMINHOS.json)
- [Sete hashes documentais regenerados](HASHES_DOCUMENTAIS.json)
- [Contexto, decisões e adaptação dos testes editoriais](01_CONTEXTO.md)
- [Verificações e limites](TESTES.md)
- [Resumo estruturado](RESUMO.json)

Cada disposição conserva o ID original, ação, motivo e trecho final ou prova de preservação. Os arquivos `S*_CONTEUDO_REALOCADO.md` preservam conteúdo retirado do percurso de uso. Fontes novas de manutenção incluem o [molde de auditoria de sprint](../templates/auditoria_sprint.md), [checklist de contribuição](../../manutencao/CHECKLIST_OBJETO_NOVO.md) e [runbook do App](../../guias/temas/DEPLOY_ROLLBACK_APP.md).

## Limites que permanecem explícitos

A versão histórica exata do TabNet não foi registrada nas evidências acessíveis; reprodução específica daquela combinação permanece NÃO EXECUTADA. Limitações executáveis já existentes, como o exemplo de ranking no resumo técnico e um contraexemplo temporal, foram documentadas sem mudar o algoritmo ou fabricar saída. A descrição antiga de `known_debt` de Micromodelos permanece na policy, identificada como divergência textual; níveis e permissões não foram promovidos.

Nenhum PASS local comprova Databricks, Genie Code, acesso corporativo, tracking remoto ou publicação. O resultado prepara a documentação versionada; implantação e promoção requerem escopo próprio.

## Estado de encerramento

Conteúdo e evidências por ação receberam revisão independente. A certificação do pacote integrado é registrada em [TESTES.md](TESTES.md); o SHA publicado e sua árvore devem ser conferidos após o push. Esta entrega não autoriza merge ou publicação no workspace.
