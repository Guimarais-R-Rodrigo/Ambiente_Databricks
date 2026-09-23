# SER01 — criar-objeto: validação determinística antes da promoção

Estado: **IN_PROGRESS / A1_PREPARED_NOT_CERTIFIED**. Base de autoria: `dedde0741ed4c387c3a500adfbf7de2c6166aba5` (merge da SER00/PR #101). A autorização de início foi dada em 2026-09-23. Ela não autoriza promoção de policy, merge ou SER02.

Este primeiro recorte implementa uma ferramenta **repo-side** para validar pacotes propostos em clone isolado. Não publica uma API nova no Databricks, não aplica arquivos ao produto original e não transforma o piloto antigo em L3 global.

A próxima ação é a execução delegada da campanha A1 no checkout integral. Arquitetura, implementação e revisão continuam com o executor desta frente; o agente Cloud apenas prepara o ambiente, materializa as duas atualizações documentais autorizadas, executa os comandos e devolve evidência.

## Navegação

- [Desenho e limites](DESENHO_TECNICO.md)
- [Matriz operação, tipo, host e efeito](MATRIZ_OPERACAO_TIPO_HOST_EFEITO.md)
- [Testes e missão do laboratório](TESTES.md)
- [Resultados de desenvolvimento](RESULTADOS.md)
- [Checkpoint e condições de parada](CHECKPOINT.md)
- [Entrada preparada de changelog](ENTRADA_CHANGELOG.md)

## O que existe na candidata A1

`tools/skill_enforcement/ser01_object_validation.py` aceita um pacote JSON, chama o preflight canônico, exige base limpa e histórico completo, cria overlay descartável, coloca os arquivos novos no índice **somente do overlay**, executa as ferramentas existentes e emite um registro vinculado aos bytes. A ferramenta não executa os módulos ou notebooks propostos.

`verify_record` confere integridade e bindings. Retorna explicitamente `INTEGRITY_ONLY` e `execution_reverified=false`: não prova por si só que um terceiro executou o validador nem autentica autorização humana.

## O que ainda não está entregue

Integração real desse componente em checkout completo, ligação da nova etapa à skill publicada, protocolo final de Receipt de domínio, tratamento prospectivo das assertions históricas SE08 antes da promoção, evidência Free/Genie aplicável e aceite da promoção. A1 não é a SER01 concluída.

```text
CURRENT_LEVEL = L2_UNCHANGED
TARGET_LEVEL = L3_UNCHANGED
ROLLOUT_MODE = audit_UNCHANGED
PRODUCT_CHANGES = 0
MERGE = NOT_AUTHORIZED
SER02 = NOT_STARTED
```

Nenhum teste sintético ou PASS de integridade autoriza mudar esses estados. A fonte operacional dos níveis permanece a policy do produto.
