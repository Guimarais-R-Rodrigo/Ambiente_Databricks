# Ferramentas dos recursos visuais

[Voltar às ferramentas](../README.md). Este é o dono único da receita de geração visual vigente. **Risco de remoção:** `--retire-legacy` altera/exclui apenas o escopo descrito abaixo; exige autorização de migração, inventário e backup. Não é flag de rotina.

Autoria, exportação e validação do conjunto v2 em `hub_readmes_visual_assets/`.
Os cabeçalhos e as cinco assinaturas aprovadas têm hashes de preservação. O
compositor de produção não depende da pasta temporária de protótipos para
regenerar os PNGs.

## V06 — gerar variante candidata a partir de tema resolvido

A rota V06 não substitui a produção ativa. Ela resolve um `theme_id` pelo núcleo
V02, aplica os tokens validados ao compositor v2 e grava a variante apenas em
`.artifacts/visual-v2/theme-variants/`. `SOURCE_DATE_EPOCH` é obrigatório para o
manifesto reproduzível.

```powershell
$env:SOURCE_DATE_EPOCH = '1700000000'
python tools/readme_visuals/theme_bridge.py --theme-id hub-legado-editorial --context readme
node tools/readme_visuals/theme_assets.mjs --theme-id hub-legado-editorial --family all
node tools/readme_visuals/theme_assets.mjs --theme-id hub-legado-editorial --verify
```

`theme_assets.mjs` recusa destino fora de `.artifacts`, confere os assets congelados
por SHA-256 e classifica mudanças paramétricas como `variant_review_required`.
Gerar ou verificar não aprova, não promove e não publica no Databricks.

## Produção v2 — caminho recomendado

```powershell
pnpm --dir tools/readme_visuals install --frozen-lockfile
node tools/readme_visuals/headers.mjs
node tools/readme_visuals/production.mjs --family all
node tools/readme_visuals/validate_production.mjs
python tools/validate_assistant.py
python tools/render_simulado.py --write
```

Para trabalhar por sprint, `--family` aceita `top`, `snippets`, `scripts`,
`skills` ou `prompts`. O manifesto global só é emitido quando os 21 metadados de
figura estiverem presentes; a validação global confere todos os consumidores.
Preparação parcial não é um pacote pronto para publicar.

As cinco assinaturas usam SVGs aprovados como entradas congeladas, com metadados
em `specs/approved_signatures.json`; os outros diagramas são gerados pelos
módulos `archetypes/top.mjs`, `snippets.mjs`, `scripts.mjs` e `methods.mjs`.
Para mudar uma assinatura, criar e aprovar a revisão antes de atualizar seu
registro; não relaxar o hash para fazer uma alteração passar.

Os cabeçalhos usam `headers/src/copy.json` e o original raster preservado.
`headers.mjs` gera os dois PNGs com tipografia determinística. O registro de
aprovação fica em `specs/approved_headers.json`. O código de autoria fica aqui;
as fontes e PNGs necessários à distribuição ficam na arquitetura do produto.

`--retire-legacy` é uma operação de migração: remove somente pares antigos
ausentes do novo manifesto e idênticos ao baseline íntegro da Sprint 0. Não é
necessário na regeneração diária. Se a pasta de baseline for retirada no futuro,
não usar esse flag; regeneração normal e validação continuam independentes dela.

## Publicação da camada visual ativa

Após validação e render do espelho, esta release pode ser enviada sem reimportar
helpers, skills executáveis ou notebooks. O escopo é fechado: cinco READMEs do
workspace e toda a pasta `hub_readmes_visual_assets/`. O README da raiz Git
permanece no repositório; não é uma sexta cópia no workspace.

```powershell
python tools/readme_visuals/publish_production.py
python tools/readme_visuals/publish_production.py --execute --retire-legacy --profile PERFIL --expected-host https://HOST
python tools/readme_visuals/publish_production.py --verify --profile PERFIL --expected-host https://HOST
python -m unittest discover -s tools/readme_visuals/tests -p "test_*.py"
```

Substitua `PERFIL` e `HOST` pelo destino autorizado. O plano é local e não grava
no remoto. A execução confere destino, QA e espelho; salva backup do escopo remoto;
recusa arquivos desconhecidos ou alterados independentemente; revalida antes de
escrever; envia assets antes dos READMEs; e exporta novamente para comparar os
bytes brutos de cada FILE. Não há execução de compute, modificação de ACL ou chat.

`--retire-legacy` autoriza somente os 12 arquivos antigos listados no código,
após comparação exata com o baseline e backup. Não existe deleção recursiva.
O recibo e os backups ficam em `.artifacts/visual-v2/publication/` (não versionados).
Como a API não oferece compare-and-swap neste fluxo, não edite os mesmos arquivos
durante a publicação. Em falha parcial, confira o recibo e corrija a causa antes
de repetir; não sobrescreva uma divergência remota desconhecida.

O publicador integral `tools/publicar_free.py` continua sendo a ferramenta para
instalar ou promover o produto completo. A conferência visual restrita não é
homologação de runtime nem substitui a verificação integral quando ela for necessária.

## Sprint 0 — referência histórica

As seções abaixo registram como a galeria foi preparada e publicada. Não executar
seu renderer sobre o pacote v2: ele foi desenhado para comparar o conjunto antigo
intacto, e essa premissa deixou de valer após a promoção. Para a produção, usar
os comandos da seção anterior.

## Entradas e saídas

- Conteúdo e papéis: `ambiente_fonte/.assistant/hub_readmes_visual_assets/specs/` e `visual_system/`.
- Layout: `lib.mjs` e `archetypes/signatures.mjs`.
- Pacote vigente: [contratos e transcrição](../../ambiente_fonte/.assistant/hub_readmes_visual_assets/CONTEUDO_FIGURAS.md).

O diretório de saída é fixo e o baseline vem de um commit explícito. O renderer recusa um baseline local adulterado. Os READMEs ativos não são escritos por estas ferramentas.

## Sequência local

```powershell
pnpm --dir tools/readme_visuals install --frozen-lockfile
node tools/readme_visuals/render.mjs
node tools/readme_visuals/document.mjs
node tools/readme_visuals/contact_sheet.mjs
node tools/readme_visuals/scale_samples.mjs
node tools/readme_visuals/validate.mjs
python tools/validate_assistant.py
python tools/render_simulado.py --write
```

Para validar a reprodução, executar `render.mjs` duas vezes e comparar hashes de SVG/PNG. Não editar `renders/`, `contracts/` nem `baseline/` à mão.

## Publicação isolada

O publicador não usa o publicador integral do ambiente, porque esta sprint é uma galeria de revisão. Ele envia apenas a pasta `sprint_0` sob a estrutura equivalente no diretório do usuário, no host explicitamente conferido.

```powershell
python tools/readme_visuals/publish_sprint0.py --profile PERFIL --expected-host https://HOST
python tools/readme_visuals/publish_sprint0.py --profile PERFIL --expected-host https://HOST --execute
python tools/readme_visuals/publish_sprint0.py --profile PERFIL --expected-host https://HOST --verify
```

Substitua `PERFIL` e `HOST` pelos valores autorizados. O primeiro comando só planeja. `--execute` importa e depois exporta cada objeto para comparar os bytes e o tipo. O visualizador é notebook Python SOURCE composto só de células Markdown; os demais itens são arquivos RAW. Nenhum notebook é executado, nenhum compute é iniciado, nenhuma permissão é alterada. Objetos remotos inesperados fazem o comando falhar; nunca são excluídos automaticamente.

O comprovante local fica em `.artifacts/sprint_0/publication.json`, fora do versionamento. Abrir o notebook no Databricks confirma renderização; a conferência por CLI confirma armazenamento, não aparência. São verificações diferentes.

Se a CLI retornar `PROTOCOL_ERROR` de HTTP/2, use `--http1` nos comandos de publicação/verificação. Essa opção aplica `GODEBUG=http2client=0` somente ao subprocesso da CLI; não altera configuração global nem desliga TLS ou validação de certificados. É um mecanismo de compatibilidade documentado pelo [Go](https://go.dev/doc/godebug). Na rodada desta sprint ele permitiu concluir o envio. Para exportar FILE, o publicador usa `AUTO`; `RAW` é utilizado apenas na importação.
