# Identidade visual — contrato central de temas

Esta pasta contém a **fonte técnica dos campos de aparência** que o Sistema de Temas poderá usar. Ela não muda cores sozinha e não é uma tela de configuração.

## Para quem nunca entrou no Hub

Você não precisa editar estes arquivos para usar o Hub hoje. A V02 instala apenas o núcleo que sabe ler e validar um tema. Se nenhum tema for informado, os notebooks continuam no comportamento legado.

O arquivo `theme.schema.json` define quais campos podem existir, tipos, limites e combinações permitidas. `TOKENS.md` é a referência humana derivada desse contrato. O schema 0.1.0 foi promovido da V01 **sem alterar seus bytes**, para preservar a decisão aceita e permitir comparar evidências. Por esse motivo, metadados históricos do próprio JSON ainda usam a palavra `candidate`; o estado vigente da decisão é registrado no ADR-0013 e no checkpoint da V02, não inferido desse rótulo histórico.

## O que existe nesta sprint

- schema instalado junto do produto;
- núcleo `hub_snippets.visual.tema` para carregar, validar e resolver um JSON local;
- erros com código e orientação curta;
- ausência de tema preserva a rota antiga;
- nenhuma aplicação automática em Plotly, HTML, imagens ou sessão.

## O que não fazer

- não coloque `approved`, papel, permissão, destino ou regra de negócio dentro do tema;
- não adicione CSS, código, URL de fonte ou caminho livre de asset;
- não edite o schema diretamente para fazer uma proposta inválida passar;
- não trate uma configuração válida como publicada ou homologada;
- não copie um tema para `themes/latest` ou equivalente: esta versão não possui alias de produção.

## Onde continuar

- Núcleo executável: `../../hub_snippets/visual/tema/README.md`.
- Decisão aceita: `../../../../docs/decisions/ADR-0013-sistema-de-temas.md` no repositório de engenharia.
- Execução da V02: `../../../../docs/sprints/sistema_temas/V02/README.md` no repositório de engenharia.
