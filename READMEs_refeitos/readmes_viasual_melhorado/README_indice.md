# READMEs refeitos — variante visual aprimorada

Esta subpasta reúne uma variante dos rascunhos documentais preparada para
avaliação visual no Databricks. Cada arquivo usa o README vigente como molde
editorial: preserva voz, sequência narrativa, tópicos, subtópicos e analogias,
mas melhora a navegação, reduz elementos excessivamente densos e acrescenta
legendas que ajudam o leitor a interpretar tabelas, fluxos e estados.

Os arquivos originais permanecem inalterados enquanto o conteúdo é avaliado.

## 🗺️ Mapa dos rascunhos

| Sprint | Rascunho | Destino após aprovação | Situação |
|---|---|---|---|
| 1 | [`README_snippets.md`](README_snippets.md) | `ambiente_fonte/.assistant/hub_snippets/README.md` | concluída |
| 2 | [`README_scripts.md`](README_scripts.md) | `ambiente_fonte/.assistant/hub_scripts/README.md` | concluída |
| 3 | [`README_skills.md`](README_skills.md) | `ambiente_fonte/.assistant/skills/README.md` | concluída |
| 4 | [`README_prompts.md`](README_prompts.md) | `ambiente_fonte/.assistant/hub_prompts/README.md` | concluída |
| 5A | [`README_raiz.md`](README_raiz.md) | `README.md` | concluída |
| 5B | [`README_assistant.md`](README_assistant.md) | `ambiente_fonte/.assistant/README.md` | concluída |

Os links entre estes rascunhos foram escritos para funcionar dentro desta pasta.
Referências à implementação aparecem como caminhos em código quando o destino
não acompanha a cópia isolada. Na promoção, todos os caminhos deverão ser
recalculados para a localização definitiva e novamente validados.

```text
README_raiz ── visão do projeto e ciclo de vida
      │
      └── README_assistant ── uso do ecossistema no workspace
                ├── README_skills   ── método
                ├── README_prompts  ── briefing
                ├── README_snippets ── código reutilizável
                └── README_scripts  ── diagnóstico
```

## 🎨 Critério editorial aplicado

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
- Navegações locais, tabelas estreitas e legendas textuais evitam depender
  apenas de cor, ícone ou memória do leitor.
- Diagramas foram mantidos quando expressam relações; conteúdo essencial também
  aparece em texto para continuar compreensível caso Mermaid não seja renderizado.

## 🔎 Roteiro de inspeção no Databricks

Ao abrir cada arquivo no workspace, verifique estes pontos antes de aprovar a
promoção:

| Elemento | O que observar | Resultado esperado |
|---|---|---|
| títulos e emojis | hierarquia e quebra de linha | leitura clara, sem símbolos corrompidos |
| navegação “Neste Guia” | abertura dos links internos | salto para a seção correta |
| Mermaid | fluxos, setas e rótulos | diagrama renderizado; se não, texto-base legível |
| tabelas | largura e quebra de conteúdo | sem perda de coluna ou leitura ambígua |
| blocos de código | indentação e destaque | exemplo copiável sem caracteres extras |
| avisos | contraste e ênfase | significado compreensível sem depender de cor |
| links entre READMEs | destino do clique | arquivo correto dentro desta subpasta |

> **Escopo do teste:** esta publicação serve para avaliar a experiência de
> leitura. Ela não ativa skills, não instala bibliotecas e não substitui o
> conteúdo operacional de `.assistant`.

## 📚 Fontes de plataforma

As afirmações sobre Databricks foram reconciliadas principalmente com:

- [Genie Code — funcionalidades e capacidades](https://learn.microsoft.com/en-us/azure/databricks/genie-code/features-capabilities)
- [Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções customizadas](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Contexto e boas práticas de prompts](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Arquivos no workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace)
- [Dependências em compute serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)

## 🚧 O que esta pasta não faz

Estes arquivos são rascunhos para revisão. Sua presença aqui não:

- substitui os READMEs atuais;
- altera o pacote implantável;
- comprova, por si só, que todos os elementos renderizam da mesma forma em cada
  superfície do Databricks;
- publica ou substitui o conteúdo operacional de `.assistant`;
- homologa bibliotecas ou permissões de um compute.

Nenhum README ativo foi substituído durante esta reescrita. O único arquivo de
controle alterado fora de `READMEs_refeitos/` é o `CHANGELOG.md` exigido pelo
processo de versionamento do projeto.
