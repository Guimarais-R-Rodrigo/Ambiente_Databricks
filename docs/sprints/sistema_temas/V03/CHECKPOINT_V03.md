# Checkpoint V03 — desenvolvimento

## Estado

V03 iniciada a partir da `main` verde `6085eabd4ca715ea2566336aaeb91e2778d76c77`, após encerramento funcional e documental da V02. Ainda não há aceite, merge ou publicação.

## Garantias que a candidata deve preservar

1. nenhuma chamada legada muda de assinatura;
2. `legado_notebook` mapeia exatamente para `get_tema_eda()`;
3. nova aplicação é explícita por figura e não altera `pio.templates.default`;
4. registro configurado usa namespace `hub-*`, não sobrescreve por padrão e só ativa globalmente com `ativar=True`;
5. dados, eixos e cores explícitas dos traces permanecem intactos;
6. temas não-notebook ou modo ainda não suportado falham sem fallback;
7. resultado V02 adulterado é rejeitado por revalidação de integridade;
8. nenhum consumidor existente é migrado implicitamente.

## Pendências antes de aceite

Executar a suíte V03, regressões V00/V01/V02, CI geral, renderer e validação documental. Atualizar README operacional, exemplo e Manual. Fazer code review da árvore final. Avaliação visual real no Databricks e teste com usuário iniciante continuam gates separados e não devem ser marcados como PASS por testes Python.

## Próxima ação

Completar implementação e documentação, gerar o espelho pelo renderer, abrir PR candidata e revalidar o head remoto. Não iniciar V04 antes da decisão sobre V03.
