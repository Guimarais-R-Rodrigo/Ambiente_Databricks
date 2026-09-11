# `ambiente_fonte/` — produto editável

Uma correção deve nascer no arquivo que a publicação utiliza, não numa cópia isolada do workspace. Este guia é para quem mantém o pacote: ele explica onde editar, o que é gerado e como conferir uma alteração. Para utilizar o Hub, comece pelo [guia do `.assistant`](../sprint-02-assistant/README.md).

> **Candidato para revisão, ainda não oficial.** Não publicar esta pasta de rascunhos. A revisão do conteúdo precede sua promoção para os destinos oficiais.

---

## Como as cópias do projeto se relacionam

**Fonte canônica** é a cópia versionada em que a equipe faz alterações. **Derivado** é um resultado gerado a partir dela. **Cópia operacional** é o material disponibilizado no workspace para uso. Corrigir apenas a cópia operacional permite que a publicação seguinte sobrescreva a correção do mesmo arquivo.

Nem todo documento de manutenção é publicável. O renderer e o publicador usam exatamente estes dois itens do produto:

```text
ambiente_fonte/.assistant_instructions.md
ambiente_fonte/.assistant/
```

O arquivo `ambiente_fonte/README.md`, destino deste guia, não integra esse plano de cópia. Uma alteração nele modifica a documentação do repositório, mas não deve ser descrita como mudança que precisa aparecer no workspace. Já uma alteração em `ambiente_fonte/.assistant/README.md` percorre o fluxo publicável. Essa distinção é verificável no [renderer](../../../tools/render_simulado.py) e no [publicador](../../../tools/publicar_free.py).

| Camada | Finalidade | Forma de alteração |
|---|---|---|
| `ambiente_fonte/` | Fonte editável do produto e guia de manutenção | Edição revisada no Git |
| `Novo_Ambiente_Simulado/` | Representação gerada da árvore publicável | Regeneração, nunca correção manual |
| Workspace | Cópia operacional de destino autorizado | Publicação e conferência |
| `tools/` e `docs/` | Ferramentas, governança e evidências do repositório | Manutenção própria; não presumir disponibilidade no workspace |

A imagem mostra verificações complementares de uma mudança publicável.

![Ciclo de edição, validação, geração, publicação e conferência, testes, registro e promoção.](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/03_ciclo_de_vida.png)

Uma falha exige retornar à fonte pertinente. Passar em validação estática não substitui a execução do helper no runtime, e publicar um arquivo não comprova que uma skill foi carregada na conversa.

---

## O que existe aqui

```text
ambiente_fonte/
├── README.md                    guia local; não publicado
├── .assistant_instructions.md   instruções pessoais publicáveis
└── .assistant/
    ├── README.md                guia de uso
    ├── GLOSSARIO.md
    ├── CATALOGO_HELPERS.md
    ├── skills/                  mecanismo nativo, conteúdo do Hub
    ├── hub_prompts/             briefings fornecidos como contexto
    ├── hub_snippets/            APIs reutilizáveis
    ├── hub_scripts/             utilitários com contratos próprios
    ├── hub_padroes/             moldes e exemplos de autoria
    └── hub_readmes_visual_assets/ figuras compartilhadas
```

Instruções e Agent Skills usam mecanismos da Genie Code. Os conteúdos do Hub não se tornam institucionais por utilizarem esses mecanismos. Coleções de código precisam estar acessíveis no ambiente que executa a chamada; arquivos visuais precisam acompanhar os documentos que os referenciam.

| Conteúdo | Consumidor | O que manter junto |
|---|---|---|
| Skill | Genie Code | Descrição, método, referências e testes de seleção |
| Snippet/script | Código consumidor | Implementação, API pública, exemplo e regressões |
| Prompt | Pessoa ou agente que recebe o briefing | Campos, contexto, exemplo e critérios de aceite |
| Padrão | Autor de objeto | Molde e exemplar consistente com o contrato |
| Figura | Leitor de README/notebook | Fonte autoral, PNG, metadados, licença e consumidores |

---

## Alterar do começo ao fim

### Antes de editar

Identifique o arquivo-fonte e seu destino. Leia o contrato que pode ser afetado. Confira se a alteração é apenas de explicação ou muda comportamento, retorno, dependência ou permissão. Essa classificação determina os testes adicionais; não é motivo para dispensar os checks comuns.

No caso desta rodada de revisão, os rascunhos ainda estão separados. Não copie um deles sobre um README oficial antes da aprovação correspondente. Seus links de revisão precisam ser recalculados para os destinos, sem copiar os PNGs para novas pastas.

### Fluxo

Execute comandos de manutenção na raiz de um checkout Git. Você precisa de Python e das dependências de teste declaradas em `tools/requirements-dev.txt`. A execução de publicação exige, além disso, CLI e autenticação no destino autorizado; não é pré-requisito para revisar texto localmente.

**Exemplo textual publicável.** Localize uma explicação em `ambiente_fonte/.assistant/README.md`, altere somente a frase necessária e confira o diff. Essa escolha é deliberada: ao contrário deste guia local, aquele README está dentro de `.assistant/`.

```powershell
python tools/validate_assistant.py
python tools/render_simulado.py
```

O primeiro comando confere estrutura, contratos, referências e higiene. Pare em qualquer falha e leia sua causa. O segundo mostra o plano de geração sem escrever. Só depois de revisar o plano, gere e confira o derivado:

```powershell
python tools/render_simulado.py --write
git diff -- ambiente_fonte/.assistant/README.md Novo_Ambiente_Simulado/
```

`--write` apaga e regenera a árvore derivada fixa, respeitando os guardrails do renderer. O diff esperado é a propagação da frase para a cópia do mesmo documento. Diferenças adicionais precisam de explicação antes de continuar. Para uma correção apenas em `ambiente_fonte/README.md`, não espere essa propagação.

**Publicação é uma decisão separada.** Consulte o [índice de playbooks](../../../docs/playbooks/README.md). No publicador de laboratório, o plano é o comportamento padrão e `--execute` é a ação de escrita; `--verify` confere o remoto. A escrita exige perfil e host explicitamente declarados. Não use valores fictícios nem presuma que o perfil ativo seja o destino correto.

```text
Plano: python tools/publicar_free.py --profile PERFIL_CONFIRMADO --expected-host HOST_CONFIRMADO
Escrita autorizada: o mesmo comando com --execute
Conferência: o mesmo comando com --verify
```

Essas linhas descrevem as três operações, não um bloco para colar sem adaptar. Confirme identidade, perfil e host pelos procedimentos do playbook. Overwrite não elimina necessariamente objetos obsoletos; a conferência de inventário, tipo e conteúdo continua necessária. Exclusão de obsoleto é ação própria, não autorização implícita deste tutorial.

| Etapa | O que altera | Evidência de saída |
|---|---|---|
| Validação | Não publica o produto | Resultado de checks e falhas identificadas |
| Render sem `--write` | Nada | Plano de origem e destino |
| Render com `--write` | Árvore derivada | Diff explicado e equivalência dos itens publicáveis |
| Publicação autorizada | Objetos no workspace de destino | Resultado do publicador |
| Verify | Leitura do remoto | Inventário, tipo e conteúdo conferidos |

### Como decidir quais testes repetir

Uma regressão local verifica o comportamento exercitado pelo teste. Um **smoke** executa operações representativas no runtime. Um teste positivo de skill verifica uma demanda pertinente; um negativo verifica a fronteira com outra tarefa; a seleção `@` verifica o caminho explícito. Esses testes respondem a perguntas diferentes.

| Mudança | Verificação adicional |
|---|---|
| Algoritmo ou contrato de helper | Regressões com casos normais, inválidos e de borda; runtime pertinente |
| Operações Spark ou dependências | Smoke no compute alvo e resultado inspecionado |
| Nome, descrição ou escopo de skill | Casos positivos, negativos e seleção explícita em conversa nova |
| Briefing | Pedido preenchido e resposta real revisada contra o aceite |
| Imagem ou caminho | Integridade do asset, referência e preview na largura de uso |
| Somente documento local de manutenção | Conteúdo e links; não inventar efeito de publicação |

**Exemplo contrastante.** Uma mudança de `temporal_split` não está concluída porque seu arquivo foi copiado. É preciso conferir divisão dos períodos, gaps, filtragem por entidade e erros de configuração com dados conhecidos. A biblioteca pode passar no teste local e ainda precisar de prova de integração no ambiente de consumo.

Ao encerrar, registre o que mudou, comandos realmente executados, ambiente, resultado e limitações. Não transforme “não executado” em “aprovado”. O commit deve conter apenas alterações revisadas e seu registro, sem arquivos locais ou segredos adicionados por engano.

---

## Limites

Editar o derivado perde a alteração na regeneração. A alternativa é corrigir a fonte e conferir o diff. Credenciais ou identificadores reais no Git permanecem no histórico; use mecanismos de autenticação e parâmetros locais, não documentos versionados.

Uma skill pode orientar ações, mas não amplia ACL. A Genie Code pode executar ferramentas conforme suas aprovações; o texto “aguarde aprovação” não substitui configuração e controle de acesso. Uma evidência de laboratório tem escopo e data: não homologa automaticamente outro runtime ou workspace.

Se o gate falhar por links de rascunhos, trate a localização física e o destino como contextos diferentes. Corrija a referência ou o mecanismo de preparação da versão candidata; não desligue globalmente a guarda de links para obter uma aprovação aparente.

---

## Onde continuar

Para usar o produto, abra o [tutorial do `.assistant`](../sprint-02-assistant/README.md). Para criar objetos, consulte [padrões](../sprint-08-padroes/README.md). Para publicar ou verificar o remoto, siga os [playbooks](../../../docs/playbooks/README.md). Para fontes de contratos, use o [Catálogo de Helpers](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md).

Procedência do escopo de publicação: [renderer](../../../tools/render_simulado.py), [publicador](../../../tools/publicar_free.py) e [gate local](../../../tools/ci_local.py). Capacidades de contexto e execução: [Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills) e [modo agente](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode), conferidos em 11/09/2026.
