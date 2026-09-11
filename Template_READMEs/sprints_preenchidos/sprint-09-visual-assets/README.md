<a id="hub-readme-visual-assets"></a>

# Hub README Visual Assets

> **CONTEÚDO CUSTOMIZADO PELO HUB** — esta pasta não é uma estrutura nativa da
> Databricks e não é descoberta automaticamente pela Genie Code.

> **Rascunho de sprint 9 — não publicado.** Destino previsto:
> `ambiente_fonte/.assistant/hub_readmes_visual_assets/README.md`.

**Asset visual**, aqui, é um arquivo de figura (PNG publicado, SVG gerado ou
congelado) usado pelos READMEs e pelos cabeçalhos. **Usar** a imagem pronta é
referenciá-la no Markdown. **Alterar** a composição é trabalho de autoria no
repositório, com compositor e aprovação — não é editar o PNG no workspace.

---

<a id="organização"></a>

## Organização

```text
hub_readmes_visual_assets/
├── README.md
├── manifest.yaml
├── CONTEUDO_FIGURAS.md
├── headers/          identidade compartilhada (CRM / Squad)
├── specs/            contratos e microcopy
├── visual_system/
├── licenses/
├── qa/
└── readmes/          raiz assistant snippets scripts skills prompts
```

**Raster (PNG)** é o que o Databricks e o GitHub mostram no README. **Vetor
(SVG)** em `sources/` é gerado, com tipografia em paths. A pasta chama-se
`sources/`, mas **nem todo SVG é a fonte autoral editável**: os diagramas novos
nascem do compositor em `tools/readme_visuals/`; cinco **assinaturas** têm SVG
congelado com hash. Editar o SVG gerado “no olho” cria cópia divergente.

Em `headers/src/`, o fundo é **raster**; `copy.json` tem o texto; os SVGs
tipográficos são só uma camada.

---

<a id="cabeçalhos-reutilizáveis"></a>

## Cabeçalhos reutilizáveis

| Uso | Arquivo canônico |
|---|---|
| README ou notebook geral | [CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png) |
| Notebook da Squad | [Squad](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_squad.png) |

Um cabeçalho por documento. Não copie o PNG para cada notebook: aponte para
cá. Caminho relativo depende da pasta do consumidor.

- Deste README: `headers/png/cabecalho_crm.png`
- De `hub_snippets/README.md`: `../hub_readmes_visual_assets/headers/png/cabecalho_crm.png`

Guia completo: [headers/README.md](../sprint-10-cabecalhos/README.md).

---

<a id="como-manter"></a>

## Como manter

<a id="quero-apenas-usar-uma-imagem"></a>

### Quero apenas usar uma imagem

1. Abra o README que já a referencia.
2. Confira o caminho relativo.
3. No preview, a figura deve carregar. Se quebrar, o arquivo não foi publicado
   junto ou o caminho está errado — não regenere arte por isso.

<a id="quero-alterar-uma-figura"></a>

### Quero alterar uma figura

1. Leia o contrato em `specs/` e a transcrição em `CONTEUDO_FIGURAS.md`.
2. Se for assinatura aprovada, a alteração exige nova revisão do hash — não
   “passe” relaxando o manifesto.
3. Altere o compositor (`tools/readme_visuals/archetypes/`) ou a entrada
   congelada, na máquina de autoria.
4. Gere, valide, regenere o simulado. Comandos na **raiz do repositório**:

```powershell
node tools/readme_visuals/headers.mjs
node tools/readme_visuals/production.mjs --family all
node tools/readme_visuals/validate_production.mjs
python tools/validate_assistant.py
python tools/render_simulado.py --write
```

Essas ferramentas **não** estão no compute do leitor no workspace. Não rode
`tools/render_readme_visuals.mjs` (pacote v1) sobre o v2.

<a id="como-conferir-um-link-quebrado"></a>

### Como conferir um link quebrado

O validador de Markdown resolve o caminho com caixa exata. No Databricks o
sistema de arquivos distingue maiúsculas. Ajuste o `![alt](caminho)` no README
consumidor; não duplique o PNG.

<a id="como-evitar-versões-concorrentes"></a>

### Como evitar versões concorrentes

| Papel | Onde |
|---|---|
| Autoria | `tools/readme_visuals/` + specs/hashes |
| Saída gerada | `readmes/*/png` e `sources` |
| Consumidor | `![...](...)` nos READMEs |

O manifesto lista o conjunto **vigente**. Histórico antigo fica no Git, não
neste pacote ativo.

---

<a id="qualidade-editorial"></a>

## Qualidade editorial

A figura permanece se esclarece relação, sequência, hierarquia ou decisão. Também
precisa de contraste e hierarquia para apresentação. Impacto ≠ decoração.

O texto ao redor é o contrato semântico: leitores com tecnologia assistiva e a
Genie Code não dependem de OCR do PNG.

**Exemplo.** Localizar `01_mapa_ecossistema.png` a partir do README raiz, abrir
`CONTEUDO_FIGURAS.md` na entrada correspondente, planejar a troca de um rótulo
identificando compositor + consumidores. Não edite só o PNG.

**Se não funcionou.** Preview sem imagem: caminho ou pacote incompleto. QA local
reprovando hash de assinatura: a figura aprovada foi alterada sem revisão.

---

<a id="qualidade-critérios-observáveis"></a>

## Qualidade — critérios observáveis

- Uma pergunta por figura.
- Legenda e equivalente textual no README.
- Cor nunca é o único sinal (rótulo + traço).
- Tipografia legível na largura do README.

<a id="exemplo-acompanhado-localizar-a-autoria-sem-alterar-a-figura"></a>

### Exemplo acompanhado: localizar a autoria sem alterar a figura

Partindo do README raiz, a referência da figura `01_mapa_ecossistema.png` chega a `ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/`. A coleção correspondente é `readmes/raiz`, mas o compositor está em `tools/readme_visuals/` na raiz do repositório. Consulte `manifest.yaml`, procure a entrada `raiz` e confira a transcrição em [CONTEUDO_FIGURAS.md](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/CONTEUDO_FIGURAS.md).

Para mudar um rótulo, registre primeiro o texto atual e o proposto, a fonte autoral indicada no manifesto e os READMEs consumidores. Depois da aprovação, regenere apenas pelo compositor apropriado, confira a transcrição e abra o PNG na largura de leitura. Uma alteração de hash prova que bytes mudaram; não prova que a nova redação é correta. Nesta revisão editorial os assets existentes foram reutilizados, sem recriar ilustrações ou inserir uma segunda cópia.
