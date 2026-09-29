# Prompt: especificar micromodelo com objetivo conhecido

> **BRIEFING CUSTOMIZADO, USO MANUAL.** Preencha os campos e selecione
> `@hub-ml-micromodelos` no modo `OBJETIVO_CONHECIDO`. Este texto não concede
> acesso a dados, não aciona validação por si e não substitui a policy da skill.

## Quando usar

Há uma característica/decisão a definir, mas faltam especificação, fontes ou
plano de estudo. Para procurar oportunidades antes de definir uma característica,
use [descobrir_micromodelos](../descobrir_micromodelos/descobrir_micromodelos.md).

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo sintético |
|---|---|---|---|
| `{{DECISAO}}` | Decisão que a característica apoiará; não imponha solução. | Delimita utilidade e consumidor. | Priorizar revisão humana de contatos |
| `{{CARACTERISTICA}}` | O que se deseja inferir e definição preliminar. | Evita confundir objetivo e regra. | Interesse recente em canal digital |
| `{{ENTIDADE_GRAO}}` | Unidade, chave lógica e data de referência, se conhecidas. | Define uma avaliação interpretável. | Cliente por mês; chave pendente |
| `{{POPULACAO_HORIZONTE}}` | Elegibilidade e janela; use `PENDENTE` quando desconhecidos. | Controla alcance temporal e população. | População sintética; 30 dias |
| `{{FONTES}}` | Referências no catálogo lógico `CATALOGO_PRODUTO` e status observado/proposto. | Evita transformar fonte hipotética em descoberta. | Objeto sintético ainda a inspecionar |
| `{{DONO_USO}}` | Dono, consumidor, uso pretendido e uso proibido. | Explicita decisões humanas e limites. | Analista de laboratório; sem decisão automática |
| `{{RESTRICOES}}` | Permissão, privacidade, custo e ambiente E0/E1. | Define o que pode ser consultado. | E0; fixture sintética; metadata somente |
| `{{PEDIDO_ORIGINAL_REF}}` | Referência auditável ao pedido, sem PII em Git. | Permite rastrear intenção sem expor conteúdo. | ticket-sintetico-001 |

## Prompt pronto para colar

```text
Use @hub-ml-micromodelos no modo OBJETIVO_CONHECIDO.

BRIEFING
- Decisão a apoiar: {{DECISAO}}
- Característica e definição preliminar: {{CARACTERISTICA}}
- Entidade, grão, chave e data de referência: {{ENTIDADE_GRAO}}
- População e horizonte: {{POPULACAO_HORIZONTE}}
- Fontes conhecidas, referência lógica e estado de observação: {{FONTES}}
- Dono, consumidor, uso pretendido e usos proibidos: {{DONO_USO}}
- Ambiente, permissões, privacidade e orçamento: {{RESTRICOES}}
- Referência do pedido original: {{PEDIDO_ORIGINAL_REF}}

TAREFA
1. Confirme o ambiente e a rota efetivamente disponível da skill e policy atual.
2. Separe fato observado, inferência, proposta, aprovação e medição. Não invente
   fonte, target, valor, limiar, dono, permissão ou resultado de execução.
3. Se houver binding e autorização, comece pela metadata do catálogo
   configurado: faça shortlist antes de pedir colunas/tags/constraints. Se o
   briefing trouxer só fixture textual, não consulte catálogo; marque a
   metadata como `FORNECIDA`. Não consulte linhas, contagens ou valores neste modo.
4. Somente se o template/schema MM01 1.0.0 estiver realmente acessível,
   atualize progressivamente um único micromodelo.yaml, preservando pendências
   e estados válidos. Valide pela rota canônica disponível e reporte o resultado
   real. Sem template/schema, não invente YAML: entregue checklist textual de
   fatos e lacunas com `YAML_NAO_CRIADO` e `MM01_NAO_VALIDADO`.
5. Explicite hipóteses favoráveis, contra-hipóteses, semântica de
   TRUE/FALSE/INDETERMINADO e o que poderia invalidar a ideia. Não trate falta
   de evidência como FALSE. Sem evidência observada e rubrica explícita, marque
   `SCORE_INDETERMINADO`; não trate score 0-100 como probabilidade sem calibração.
6. Entregue plano de estudo e handoff às skills especialistas apropriadas,
   cada qual sob sua policy atual. Não publique nem avance fase por suposição.

SAÍDA
- Resumo da decisão, escopo observado e lacunas.
- YAML MM01 quando houver template/schema acessível, com resultado real da
  validação; caso contrário, checklist textual e `YAML_NAO_CRIADO`.
- Proveniência dos campos relevantes, incertezas e decisões pendentes.
- Próxima etapa, responsável sugerido e evidência E0/E1/E2 realmente obtida.
```

## O que conferir na resposta

Se houver YAML, confira grupos MM01, `CATALOGO_PRODUTO`, fase coerente e
proveniência sem `APROVADO`/`MEDIDO` fictícios. Sem schema acessível, confira
que não houve YAML inferido nem score sem base. Inspeção textual do briefing não
é teste conversacional. A execução E1 depende do usuário e E2 está fora do escopo.

## Limites

O briefing não autoriza leitura de registros, concede ACL, valida hipóteses ou
publica artefatos. O coletor E0 repo-side não é runtime transportado ao Free.
