# Guia de primeiro uso — App de Gestão Visual V10

Este guia é para quem nunca usou o Sistema de Temas. Ele descreve o que a interface faz sem pressupor conhecimento de Python.

## Antes de abrir

Confirme com o responsável pelo ambiente que:

1. você recebeu acesso ao Databricks App de autoria visual;
2. o App está ligado ao Unity Catalog Volume de sessões;
3. você está no ambiente correto;
4. ninguém pediu que você publique ou altere o padrão da equipe — a V10 não faz isso.

Se o App exibir erro de identidade ou armazenamento, não tente contornar o bloqueio. Copie somente o código da mensagem e procure o mantenedor; não envie tokens nem dados internos.

## Tela 1 — escolher uma base

Na barra lateral, escolha um **ponto de partida**. As referências empacotadas aparecem como **demonstração**. Isso significa apenas que podem ser usadas para experimentar; não são temas aprovados.

Clique em **Abrir novo rascunho**. Se já havia alterações não salvas na sessão atual, abrir outro rascunho abandona apenas o estado em memória dessa tela; uma sessão salva anteriormente continua no Volume.

## Tela 2 — ajustar

Os controles principais aparecem primeiro. Abra **Controles avançados** somente quando precisar de opções adicionais.

Clique em **Aplicar e validar proposta**. O App valida a configuração inteira antes de trocar o estado. Se um valor for inválido, a última proposta válida continua ativa e nenhuma parte da alteração inválida é gravada.

Use:

- **Desfazer último ajuste** para retornar ao último estado válido;
- **Restaurar base** para voltar ao ponto de partida da sessão.

## Tela 3 — comparar

A comparação mostra **Base** e **Proposta** com os mesmos dados sintéticos. O objetivo é comparar aparência, não resultado analítico.

Verifique cabeçalho, KPI, barras, série temporal, heatmap e tabela. Negativos, nulos e múltiplas categorias fazem parte da galeria de teste.

Não interprete essa comparação como certificação de acessibilidade ou como renderização homologada em todos os notebooks.

## Tela 4 — salvar

Digite um nome simples para a sessão, por exemplo:

```text
proposta-dashboard-risco
```

Clique em **Salvar sessão**. O sucesso precisa mostrar nome, revisão, profundidade do histórico e prefixo do hash do manifesto. Sem confirmação, não considere a sessão salva.

O App não sobrescreve uma sessão com o mesmo nome. Escolha outro nome para criar uma nova sessão rastreável.

## Retomar uma sessão

Na barra lateral, a seção **Retomar** lista apenas sessões do namespace derivado da sua identidade atual. Escolha uma sessão e clique em **Reabrir sessão**.

A reabertura confere os hashes antes de reconstruir base, proposta e histórico. Arquivo adulterado ou sessão incompleta é recusado em vez de ser reparado silenciosamente.

## O que você não encontrará

Não existe botão para:

- aprovar;
- rejeitar;
- publicar;
- promover;
- ativar como padrão;
- apagar histórico.

Essas ausências são intencionais. A política de papéis do projeto separa autoria, aprovação e publicação; a V10 implementa somente autoria/persistência.

## Se aparecer erro

Mensagens que começam com `APP_` pertencem à camada do App. Mensagens `LAB_` pertencem ao Visual Lab reutilizado.

- `APP_IDENTITY_MISSING`: o proxy não entregou identidade e o App recusou operar.
- `APP_STORAGE_MISSING`: o recurso de persistência não foi configurado.
- `APP_STORAGE_NOT_VOLUME`: a produção recebeu caminho fora de Unity Catalog Volume.
- `APP_STORAGE_UNAVAILABLE`: o Volume não está acessível como esperado.
- `LAB_SESSION_EXISTS`: já existe sessão com esse nome.
- `LAB_SESSION_HASH`: a sessão foi alterada e não corresponde ao manifesto.

Não corrija hashes, não troque caminho para `/tmp` e não habilite modo local em produção para “fazer passar”.

## Encerrar

Fechar a página não publica nada. Alterações apenas em memória desaparecem com a sessão; sessões explicitamente salvas permanecem no Volume conforme a política administrativa do destino.
