# Checklist — transição pessoal para o Databricks do trabalho

Procedimento dono: [guia de transição](replicacao-trabalho.md). Versão 11/09/2026. Não preencher identificadores corporativos nesta cópia versionada; anotações reais ficam no ambiente autorizado.

## Origem e pacote

- [ ] Confirmar o commit escolhido e checkout limpo; manter README/widgets, Manual e instruções aprovados.
- [ ] Executar renderer, gate local e testes do kit. Não interpretar teste local como teste do trabalho.
- [ ] Gerar `tools/kit_transicao_trabalho.py --output .artifacts/kit-trabalho` em diretório novo ou baixar o artefato do workflow.
- [ ] Levar ZIP 01, ZIP 02, guias e SHA256SUMS pelo canal corporativo permitido; não levar Git/histórico/segredos.
- [ ] Conferir hashes e commit. Não misturar releases; não importar o ZIP externo de download.

## Destino, backup e staging

- [ ] Confirmar autorização de upload, Workspace Files, compute e Genie. Não presumir autorização para produção.
- [ ] Copiar o caminho do usuário pela UI e preencher somente no notebook do trabalho.
- [ ] Backup de `.assistant` em **Zip - Source (notebook + files only)**; instruções exportadas separadamente.
- [ ] Abrir o backup, conferir módulos/Markdown/imagens/notebooks e recuperação em local isolado. DBC sozinho não serve.
- [ ] Guardar backup/configurações dentro do ambiente corporativo; separar Hub de skills/arquivos de terceiros.
- [ ] Criar `hub_staging_<commit>` e importar ZIP 01 dentro dela, conferindo a camada de diretório.
- [ ] Importar ZIP 02 na raiz do usuário; abrir `aceite_hub_<commit>/01_ACEITE_TECNICO`.

## Notebook técnico em staging

- [ ] Sessão Python nova; preencher USER_HOME/KIT_DIR; `PHASE="staging"`; opções extras desligadas.
- [ ] Manifesto PASS e todos os FILEs SHA256 PASS. Não editar o manifesto para contornar erro.
- [ ] Conferir tipos de arquivos/notebooks pela UI; metadata via API é opcional e não atesta células.
- [ ] Conferir dependências necessárias e compute autorizado. Nenhuma instalação indiscriminada.
- [ ] Habilitar Spark sintético; recomeçar em sessão nova; imports e Python PASS.
- [ ] Spark mínimo, DQ aviso, DQ duplicidade, RFV, PIT, PSI e objeto Plotly PASS.
- [ ] Veredito `STAGING_TECNICO_APROVADO_NAO_ATIVADO`. Nenhuma alegação de Genie ativa nesta fase.

## Promoção seletiva

- [ ] Reservar janela sem alteração simultânea; preparar rollback fora da descoberta de skills.
- [ ] Substituir cinco pastas Hub: padrões, prompts, recursos visuais, scripts e snippets.
- [ ] Substituir apenas skills declaradas do Hub, sem apagar `skills/` inteira; reconciliar legado identificado.
- [ ] Preservar `.mcp_servers.json`, skills alheias, segredos, permissões e instruções administrativas.
- [ ] Atualizar README e Manual; retirar catálogo/glossário independentes somente se forem Hub-owned.
- [ ] Atualizar `.assistant_instructions.md` na raiz do usuário por último e confirmar pelo Settings da Genie.

## Aceite final e piloto

- [ ] Reiniciar Python; `PHASE="final"`; conferir FILEs e testes novamente após a movimentação.
- [ ] Abrir READMEs renderizados, imagens, links e os exemplos FILE/NOTEBOOK indicados.
- [ ] Rodar roteiro humano: instruções, EDA sem @, baseline com @, criar objeto com @, contexto proporcional e proveniência.
- [ ] Declarar confirmações humanas somente com observação. PENDENTE não é PASS.
- [ ] MLflow opcional: experimento pessoal existente autorizado; round-trip e limpeza do run próprio confirmados.
- [ ] Leitura UC opcional: consulta limitada à tabela autorizada; não confundir com permissão de escrita.
- [ ] Registrar JSON final sanitizado dentro do ambiente autorizado; revisar antes de compartilhar.
- [ ] `PRONTO_PARA_PILOTO_BASICO` somente no escopo testado. Modelos/serving/produção continuam em gates próprios.

## Se houver falha

- [ ] Interromper promoção ou uso do componente afetado; localizar ID do teste, causa e correção no guia.
- [ ] Conferir se MLflow deixou run próprio pendente de limpeza.
- [ ] Restaurar só o escopo substituído pelo backup, sem sobrescrever mudanças alheias posteriores.
- [ ] Reiniciar Python/chat; registrar motivo e retestar. Levar correções à fonte sem identificadores do trabalho.
