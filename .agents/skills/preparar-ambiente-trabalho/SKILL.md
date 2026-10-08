---
name: preparar-ambiente-trabalho
description: Prepara a configuração individual do clone para Copilot no VS Code e Databricks CLI no trabalho, verificando perfil e destinos antes de planejar uma instalação pessoal.
---
# Preparar o computador do trabalho

Leia o [guia](../../../docs/playbooks/copilot-trabalho.md) e a
[configuração](../../../config/README.md). Confira branch, SHA e diff.

Use o modelo versionado para orientar o preenchimento local. Não peça ao usuário
que envie host, username, caminhos pessoais ou credenciais ao chat. Não leia nem
mostre o conteúdo completo do perfil de autenticação.

Execute `python -m tools.trabalho.workspace --check`; depois `--plan` se solicitado.
Esses comandos não conectam nem escrevem remotamente. Separe config válida,
autenticação observada, acesso à pasta e descoberta nativa do Copilot.
Falta de CLI/perfil bloqueia somente a fase dependente; não instale nem faça login
automaticamente. O guia explica as verificações no computador de destino.

Casos esperados: preparar um novo clone → verificar configuração; pedido de EDA
→ encaminhar ao produto; perfil ausente/host divergente → bloquear o uso remoto
e orientar correção local, sem revelar os valores.
