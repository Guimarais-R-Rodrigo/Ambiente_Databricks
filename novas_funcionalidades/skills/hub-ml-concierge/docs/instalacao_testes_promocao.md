# Revisão, teste isolado e promoção

## 1. Estado desta entrega

O pacote está em `novas_funcionalidades/skills/hub-ml-concierge/`, fora da árvore canônica do produto. GitHub não é o workspace Databricks; versionar a pasta não instala a skill. A base de referência está registrada em [Fontes](fontes.md).

## 2. Revisão sem instalação

Leia o `SKILL.md`, os templates e a matriz de aceite. Execute o verificador estático e seus testes conforme `tests/README.md`. Para simular o comportamento, forneça explicitamente o `SKILL.md` e os recursos de contexto que o assistente precise ler.

Não chame esse ensaio de forward test: anexar instruções comprova somente que o procedimento foi fornecido, não que a plataforma selecionou a skill por relevância.

## 3. Teste pessoal no Databricks — depende de autorização

A criação deste pacote não executou os passos abaixo.

1. Confirme permissão e ambiente de teste. Use dados sintéticos e documentação autorizada; não use o workspace corporativo como primeiro laboratório.
2. No Genie Code, abra Settings -> Open skills folder, quando essa opção estiver disponível, e confira o escopo pessoal. A documentação oficial descreve `/Users/<username>/.assistant/skills/` para skills de usuário e `Workspace/.assistant/skills/` para escopo compartilhado.
3. Após autorização, crie apenas `hub-ml-concierge/` no destino pessoal. Copie `SKILL.md`, `references/`, `templates/` e, opcionalmente, README/docs/tests. Preserve a estrutura relativa. Não copie a pasta `novas_funcionalidades` inteira e não sobrescreva uma skill preexistente sem conferência e backup.
4. Forneça uma raiz de Hub acessível e sua versão, quando conhecida. Se não houver biblioteca publicada, use arquivos explicitamente anexados e registre cobertura parcial. Não alegue acesso por ter escrito um caminho.
5. Abra um chat novo e teste `@hub-ml-concierge`; depois rode os positivos e negativos sem menção. Alterações não devem ser avaliadas em um chat que carregou a versão anterior. Atualize a página se metadados antigos persistirem.
6. Registre separadamente a evidência de carregamento e a qualidade da resposta. Não confunda o nome impresso na resposta com ativação observada. Se a interface não permitir comprovar, marque `NÃO VERIFICADO`.

Os caminhos acima identificam objetos do workspace; não os transforme mecanicamente em paths de sistema de arquivos para comandos Python. O pacote não necessita de `%pip`, Spark ou import de helpers para orientar a busca. Disponibilidade das ferramentas de leitura e recursos do workspace deve ser conferida no destino.

## 4. Promoção ao produto — não realizada

Depois de aprovação explícita:

- Registrar a nova decisão arquitetural sem reescrever ADRs aceitos.
- Integrar seletivamente o pacote em `ambiente_fonte/.assistant/skills/`.
- Atualizar o inventário esperado em `tools/project_policy.py`, descrições e entradas pertinentes do README/Manual; não remover declarações de helpers dos especialistas.
- Sincronizar a cópia de leitura do Manual da raiz quando seu conteúdo mudar; gerar o simulado com o renderer, nunca à mão.
- Executar `python tools/validate_assistant.py`, CI aplicável e testes de roteamento da nova skill e das vizinhas; registrar o resultado real e eventuais bloqueios.
- Atualizar o changelog canônico e evidências; publicar somente por procedimento autorizado e conferir o que foi instalado.

Essas são mudanças futuras: nenhum desses arquivos foi modificado por este protótipo. O validador experimental não substitui o validador canônico.

## 5. Rollback

No teste pessoal, desative/remova somente a pasta de Concierge que foi criada, depois de confirmar identidade e backup. Preserve as demais skills, conectores e arquivos. Abra conversa nova para evitar contexto antigo.

Se houver promoção futura, reverta o commit de integração pelo fluxo do repositório e republique de forma autorizada. Apagar no Git não remove automaticamente uma cópia remota.

## 6. Evolução condicionada a evidência

Se houver falhas de recuperação, avaliar busca determinística derivada das fontes existentes. Se houver necessidade de API ou interface independente, reavaliar agente dedicado. Nenhuma evolução deve ser inferida apenas pelo crescimento do número de arquivos.
