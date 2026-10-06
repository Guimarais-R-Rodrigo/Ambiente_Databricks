# Concierge — localizador do protótipo

Para usar ou manter o Concierge, abra a
[versão canônica do produto](../../ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md).
A integração segue o [ADR-0011](../decisions/ADR-0011-concierge-hub.md); descoberta
opcional não executa helpers nem comprova homologação conversacional.

O [protótipo 0.1.0](../../novas_funcionalidades/README.md) permanece em seu caminho
original somente para consulta histórica. Não instalar as duas cópias, não usar
os comandos antigos como receita corrente e não promover o protótipo novamente.

O [inventário de retenção](concierge-manifest.json) fixa os 19 arquivos e hashes
na base `126a2e125cca2251527f187a58696243414c6859`. Somente o README de entrada
recebe navegação vigente; os demais arquivos permanecem intactos. O conteúdo
anterior do README pode ser recuperado no commit indicado no manifesto.

Não houve remoção ou realocação física: ferramentas de inventário visual, testes
e relatórios ainda referenciam esses caminhos. Um corte futuro exige classificar
todos os consumidores, preservar prova/licenças, demonstrar equivalência e prever
rollback. Ausência de import não prova ausência de dependência.

[Voltar ao histórico](README.md)
