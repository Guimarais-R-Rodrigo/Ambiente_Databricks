# Checkpoint V05 — Visual Lab em desenvolvimento

## Estado vigente — 13/09/2026

V05 em desenvolvimento na branch `codex/temas-v05-visual-lab-20260912`.
A retomada preserva integralmente a main R07 `b73bbb91961f9ba5f9031d648c42ec0891b63347`
e acrescenta os sete arquivos da candidata `133966bf8ee7555d1d9dadd3922d2fc75a4641e9`.
Essa composição não é aprovação dos testes anteriores: exige nova rodada.

Rodrigo autorizou continuar o desenvolvimento. Não concedeu aceite à V05 nem
integração, publicação no Databricks ou início da V06.

## Bloqueios de fechamento

- Corrigir navegação do README dentro do produto publicado.
- Ajustar o notebook sem relaxar a guarda de contrato; registrar saída executada.
- Conferir e corrigir segurança de salvamento e comportamento da interface.
- Completar documentação de primeiro uso, catálogo integrado do Manual e índices.
- Registrar esta execução no CHANGELOG raiz sem truncar seu histórico.
- Gerar fachadas e espelho com as ferramentas canônicas.
- Recalcular o README pela execução na árvore final, sem reutilizar contagens antigas.
- Executar regressões e revisão sobre a composição final; depois solicitar aceite.

## Evidências anteriores

A execução `34733554922` da candidata `a45ebd6` aprovou os 31 casos V05,
329 casos de temas e 12 legados visuais V00, mas REPROVOU a validação documental.
Não é CI aprovado e não testa a composição R07. Consulte [TESTES.md](TESTES.md).

## Limites

Testes Python de objetos ipywidgets não comprovam a renderização nem callbacks
em Databricks. Acessibilidade, usuário iniciante, runtime do workspace, persistência
de sessão, permissões reais e auditoria independente permanecem pendentes.
O laboratório usa dados sintéticos; não aprova nem publica temas.

## Recuperação

Enquanto esta branch não for integrada, nenhuma reversão de main ou publicação
é necessária. Não fazer force-push, não alterar proteções e não sobrescrever
mudanças da frente R07. Preservar execuções reprovadas como evidência.

[Escopo V05](README.md)
