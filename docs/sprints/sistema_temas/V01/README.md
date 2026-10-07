# Sistema de Temas — V01: contrato e experiência proposta

> **Nota administrativa — 06/10/2026.** Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência. O [Visual Lab](../../../../ambiente_databricks/.assistant/hub_snippets/visual/theme_lab/README.md) é a rota de uso atual, distinta da especificação histórica.

## Registro histórico preservado

> **V01 COM ACEITE DE RODRIGO · CONTRATO 0.1.0 · AUTORIA CODEX · 12/09/2026.**
> O seletor de temas **não está instalado**. Esta sprint entrega decisões,
> especificações, exemplos de configuração e verificações de manutenção.
> Não é um pacote de implantação Databricks nem um novo manual do Hub.

## Sua próxima ação

Você não precisa abrir o Databricks nem escrever código para revisar esta entrega.
Para entender o que poderá fazer, abra o [guia de primeiro uso](GUIA_PRIMEIRO_USO.md).
Ele descreve a experiência planejada, identifica o que ainda não existe e permite
avaliar se experimentar uma cor, salvar uma proposta e publicar ficaram claros.

Para saber o resultado desta execução, leia o [relatório V01](RELATORIO_V01.md).
Para revisar tecnicamente a decisão, comece pelo
[ADR-0013](../../../decisions/ADR-0013-sistema-de-temas.md), seguido do
[contrato](CONTRATO_TEMAS.md). Quem mantém código encontra comandos reproduzíveis
no [guia do mantenedor](GUIA_MANTENEDOR.md).

## O que existe e o que ainda será entregue

Existe um contrato JSON fechado, com 48 definições para notebook e 32 para
materiais editoriais, quatro exemplos completos e um verificador local. Existe
uma especificação de papéis e transições, não um serviço de autenticação.
Os exemplos são **fixtures**: entradas de teste, não temas já aprovados ou
instalados. A versão-alvo de mecanismo 1.0.0 é uma referência do contrato, não
um anúncio de software disponível.

O núcleo que aplica configurações é V02; os adaptadores são V03/V04/V06/V07;
o laboratório em notebook é V05. Apps e AI/BI seguem extensões posteriores.
Não foram mudados gráficos, imagens, cálculos, imports, widgets, Manual Técnico
ou pastas do produto nesta V01. Você pode continuar usando o Hub como antes.

## Como navegar na especificação

| Documento | Pergunta que responde |
|---|---|
| [CONTRATO_TEMAS.md](CONTRATO_TEMAS.md) | O que um tema contém e o que é proibido? |
| [TOKENS.md](TOKENS.md) | Qual parâmetro tem qual significado, unidade, origem e consumidor? |
| [GOVERNANCA.md](GOVERNANCA.md) | Quem pode propor, aprovar, publicar e desfazer? |
| [EXPERIENCIA_LABORATORIO.md](EXPERIENCIA_LABORATORIO.md) | Como serão os controles, os estados e os erros? |
| [PLANO_DOCUMENTACAO.md](PLANO_DOCUMENTACAO.md) | Onde cada explicação será mantida, sem duplicar o Manual? |
| [TESTES_E_ACEITE.md](TESTES_E_ACEITE.md) | O que os testes provam e quais avaliações faltam? |
| [LEITURAS_E_DEPENDENCIAS.md](LEITURAS_E_DEPENDENCIAS.md) | Quais fontes, versões e mudanças paralelas foram consideradas? |

O schema é a fonte dos campos. A tabela TOKENS é gerada dele; não é outra
configuração independente. A política é a fonte das transições propostas.
Os documentos explicam esses arquivos sem autorizar ações operacionais.

## Status de aceite

Auditoria independente: **PENDENTE**. Revisão com usuário iniciante: **PENDENTE**.
Homologação Databricks: **NÃO EXECUTADA**. Composição com a base `b88a9cc`: ver [checkpoint](CHECKPOINT_V01.md).
Rodrigo concedeu o aceite da V01 e solicitou testar e aplicar. O PR #10 registra
a integração Git após os checks; o [checkpoint vigente](CHECKPOINT_V01.md) explica
o alcance da autorização. Aceite e integração não equivalem a publicação.

A V00 histórica permanece em [seu registro de integração](../INTEGRACAO_V00.md). Os resultados
novos não reescrevem suas evidências. A V02 não faz parte desta entrega.

[Voltar à frente de temas](../README.md) · [Documentação geral](../../../README.md)
