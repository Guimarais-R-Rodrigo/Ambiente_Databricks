<!-- Template: explicação de notebook inteiro (skill hub-ml-tutor-databricks) -->

# Explicação do notebook: [NOME_DO_NOTEBOOK]

| Campo | Valor |
|-------|-------|
| **Autor** | [nome do autor, se identificável no notebook] |
| **Status** | [DESENVOLVIMENTO | HOMOLOGAÇÃO | PRODUÇÃO | EXPLORATÓRIO | NÃO INFORMADO — citar evidência se conhecido] |
| **Linguagem principal** | [Python | SQL | Misto] |
| **Complexidade estimada** | [Baixa | Média | Alta] |

## 1. Objetivo geral

[4 a 8 linhas: propósito do notebook, contexto, escopo.]

## 2. Mapa das etapas

[Incluir somente etapas presentes no código. As linhas abaixo são exemplos, não evidência de execução; distinguir operação prevista de resultado observado.]

| # | Etapa | O que faz |
|---|-------|-----------|
| 1 | Configuração | [imports, widgets, parâmetros] |
| 2 | Leitura | [tabelas/volumes lidos] |
| 3 | Validação inicial | [schema, contagem, nulos críticos] |
| 4 | Transformação | [lógica principal] |
| 5 | Validação final | [regras de negócio, integridade] |
| 6 | Escrita | [destino e modo] |
| 7 | Log e métricas | [tabela de log, estatísticas] |
| 8 | Resumo executivo | [síntese final] |

## 3. Fluxo de dados

```
[Tabela A] ──┐
             ├──> join ──> filtro ──> agregação ──> [Tabela Gold]
[Tabela B] ──┘                                              │
                                                            ├──> log
                                                            └──> métricas
```

## 4. Explicação por seção

### 4.1 [Etapa 1]
- **Objetivo**: ...
- **Lógica**: ...
- **Entradas**: ...
- **Saídas**: ...
- **Validações**: ...
- **Riscos**: ...

### 4.2 [Etapa 2]
- ...

(Repetir para cada etapa.)

## 5. Conceitos técnicos principais

- **[Conceito 1]**: por que aparece, como é usado.
- **[Conceito 2]**: ...
- **[Conceito 3]**: ...

## 6. Pontos críticos

- 🔴 [Trecho 1: descrição do risco/sensibilidade].
- 🔴 [Trecho 2].

## 7. Melhorias possíveis

| # | Melhoria | Por quê | Trade-off |
|---|----------|---------|-----------|
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |

## 8. Resumo executivo

[O que o código pretende entregar, a relevância de negócio e o próximo passo. Resultado observado somente com evidência; caso contrário, não informado.]
