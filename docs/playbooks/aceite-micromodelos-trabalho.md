# Micromodelos — aceite sintético do Hub no trabalho

Este guia acompanha a candidata local de Micromodelos. Use-o depois de conferir `GUIA_TRANSICAO.md` do kit geral. O ZIP 01 transporta o módulo em `.assistant/hub_micromodelos/`, com contratos, execução e exemplo sintético. O ZIP 02 contém o notebook de aceite, fora do produto. A instalação em staging ainda não ativa a skill pessoal.

O primeiro resultado esperado é um aceite sintético em staging. Ele não certifica o runtime corporativo inteiro, Genie Code, permissões Unity Catalog, dados reais, MLflow institucional ou publicação. A promoção da skill segue o gate SE08 e decisão própria.

## Preparação e integridade

1. Use o mesmo commit indicado em `COMECE_AQUI.md` para os dois ZIPs. Compare o SHA-256 de cada ZIP com `SHA256SUMS.txt`, recebido pelo canal autorizado. Um hash no mesmo pacote detecta alteração acidental, mas não substitui a confiança no canal.
2. Confirme com a política local o transporte, a importação para a pasta pessoal e o compute. Faça o backup indicado no guia geral antes de substituir qualquer arquivo pessoal. Mantenha o Hub anterior e conteúdo alheio intactos.
3. Importe o ZIP 01 em `hub_staging_<commit>` e o ZIP 02 em `aceite_hub_<commit>`, como no guia geral. Confirme que `hub_micromodelos/` está diretamente em `hub_staging_<commit>/.assistant/`.
4. Antes de executar, confira tipos na UI: os `.py`, `.json`, `.yaml` e `.md` do módulo devem estar acessíveis como arquivos. A importação do ZIP por si só não prova que o runtime consegue lê-los com `Path`.

Use uma sessão Python nova no compute autorizado. Abra `02_ACEITE_MICROMODELOS.ipynb` do ZIP 02, ajuste `PACKAGE_ROOT` para a raiz extraída do ZIP 01 e execute as células. O notebook fixa commit e hash do manifesto do Hub, confere os arquivos Micromodelos antes dos imports e exige `status=PASS`. Em caso de falha, leia os estágios impressos e interrompa. O código do aceite está embutido no notebook e não depende do checkout Git no destino.

O aceite geral confere todos os FILEs do manifesto; o aceite Micromodelos reconfere os seus próprios arquivos antes de importá-los. Se faltar arquivo, houver hash divergente ou dependência ausente, registre a etapa e interrompa esse ensaio. Não edite o manifesto nem copie arquivos avulsos de outra revisão para obter PASS. Reimporte a versão íntegra ou abra uma correção de origem.

O modo padrão usa somente fixtures sintéticas. `testar_mlflow=False` e `testar_metadata=False` permanecem desligados. Ativar qualquer teste institucional requer configuração e autorização específicas no destino; um resultado `NOT_RUN` ou `UNAVAILABLE` não se transforma em PASS. Não há criação automática de tabela, experimento, registro de modelo ou publicação neste roteiro.

## Leitura do resultado

Registre commit, hash do ZIP e o status de cada etapa: integridade, dependências, MM01 YAML/schema/template, MM02 fingerprint, MM03/MM04 descoberta e objetivo conhecido com metadata sintética, MM09 estudo e classificação, MM10 handoff e reconciliação. As contagens sintéticas esperadas são `TRUE=1`, `FALSE=2`, `INDETERMINADO=3`, população `6` e `scores_emitidos=4`. O handoff deve ficar em rascunho, sem publicação. Agregados fornecidos permanecem `SUPPLIED_UNVERIFIED` até medição governada. O resultado não comprova holdout real.

Se houver erro de dependência, anote o pacote ausente e as versões permitidas. Os módulos de contrato usam `PyYAML`, `regex` e `jsonschema`; o runtime autorizado decide a instalação. Não instale bibliotecas em massa nem transplante pins do Free. Depois de qualquer instalação permitida, reinicie a sessão Python e reexecute o aceite desde a verificação de integridade.

A combinação local exercitada em 2026-09-29 foi Python 3.12.10, PyYAML 6.0.3, regex 2026.9.10 e jsonschema 4.26.0. Essas versões observadas não são lock do ambiente corporativo. O Hub contém também o helper de tracking compartilhado para uma etapa posterior; o aceite padrão não o importa nem cria runs.

## Diagnóstico e retorno

No computador do trabalho, preserve logs completos somente no canal institucional autorizado. Para solicitar uma sprint de correção local, envie apenas esta ficha sanitizada:

```text
commit e SHA-256 do pacote:
etapa/caso:
esperado:
observado, sem dados ou identificadores reais:
código de erro sanitizado:
características genéricas do runtime/dependências:
reprodução possível com fixture sintética:
classificação inicial — pacote / produto / runtime / permissão / decisão:
```

Não envie linhas de tabela, nomes de catálogo, paths reais, host, usuário, tokens, notebook preenchido, backup nem logs brutos ao repositório pessoal. Para defeito de produto, a correção volta à fonte canônica; o novo pacote terá commit/hash próprios. Reteste no destino o caso corrigido e as etapas que dependem dele.

## Parada e rollback

Falha de integridade, import, dependência ou autorização interrompe a etapa dependente. O produto fica em staging e pode permanecer para diagnóstico conforme a política local. Qualquer remoção deve limitar-se aos arquivos próprios criados pelo ensaio, depois de conferir seu conteúdo e preservar evidência necessária. A eventual promoção da skill usa o backup e rollback de `GUIA_TRANSICAO.md`; este aceite não promove nem substitui a instalação pessoal.
