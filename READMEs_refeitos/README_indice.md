# READMEs refeitos — revisão conservadora

Esta pasta reúne a segunda versão dos rascunhos documentais. Cada arquivo usa o
README vigente como molde editorial: preserva a voz, a sequência narrativa, os
tópicos, os subtópicos, as analogias e os componentes visuais, corrigindo
afirmações técnicas e acrescentando explicações onde elas fortalecem o mesmo
storytelling.

Os arquivos originais permanecem inalterados enquanto o conteúdo é avaliado.

## Mapa dos rascunhos

| Sprint | Rascunho | Destino após aprovação | Situação |
|---|---|---|---|
| 1 | [`README_snippets.md`](README_snippets.md) | `ambiente_fonte/.assistant/hub_snippets/README.md` | concluída |
| 2 | [`README_scripts.md`](README_scripts.md) | `ambiente_fonte/.assistant/hub_scripts/README.md` | concluída |
| 3 | [`README_skills.md`](README_skills.md) | `ambiente_fonte/.assistant/skills/README.md` | concluída |
| 4 | [`README_prompts.md`](README_prompts.md) | `ambiente_fonte/.assistant/hub_prompts/README.md` | concluída |
| 5A | [`README_raiz.md`](README_raiz.md) | `README.md` | concluída |
| 5B | [`README_assistant.md`](README_assistant.md) | `ambiente_fonte/.assistant/README.md` | concluída |

Os links internos destes rascunhos foram escritos para funcionar a partir desta
pasta de revisão. Na promoção, eles deverão ser recalculados para a localização
definitiva e novamente validados.

## Critério editorial aplicado

- A organização atual é o ponto de partida, não algo a ser substituído.
- Analogias, quadros em texto, mapas mentais, fluxos Mermaid, catálogos
  narrativos e FAQ foram preservados e ampliados.
- **MECANISMO NATIVO DATABRICKS** distingue funcionalidades reconhecidas pela
  Genie Code de conteúdo **CUSTOMIZADO PELO HUB**.
- Ação manual — copiar, anexar, importar ou executar — é declarada sem alterar o
  tom didático do documento.
- Afirmações absolutas foram substituídas por contratos verificáveis e seus
  limites, sem remover a explicação que ajudava o leitor.
- Exemplos foram reconciliados com as assinaturas reais do código.
- Melhorias novas aparecem como aprofundamento dos mesmos temas: custo,
  dependências, aprovação, evidência e solução de problemas.

## Fontes de plataforma

As afirmações sobre Databricks foram reconciliadas principalmente com:

- [Genie Code — funcionalidades e capacidades](https://learn.microsoft.com/en-us/azure/databricks/genie-code/features-capabilities)
- [Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções customizadas](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Contexto e boas práticas de prompts](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Arquivos no workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace)
- [Dependências em compute serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)

## O que esta pasta não faz

Estes arquivos são rascunhos para revisão. Sua presença aqui não:

- substitui os READMEs atuais;
- altera o pacote implantável;
- comprova renderização no visualizador do Databricks;
- publica conteúdo em workspace;
- homologa bibliotecas ou permissões de um compute.

Nenhum README ativo foi substituído durante esta reescrita. O único arquivo de
controle alterado fora de `READMEs_refeitos/` é o `CHANGELOG.md` exigido pelo
processo de versionamento do projeto.
