# Matriz de auditoria R13

| Dimensão | Fonte de verdade | Verificação |
|---|---|---|
| Estrutura do README | `hub_padroes/readme/template_objeto.md` | versão 1.0.0 e 15 seções derivadas do template |
| Rubrica editorial | `hub_padroes/readme/checklist_objeto.md` | salvaguardas, estados e `A0_light` |
| Criação futura | `skills/hub-ml-criar-objeto/SKILL.md` | referência ao template/checklist, seis tipos e seis categorias |
| Gate estrutural | `tools/readme_objeto_contract.py` | descoberta, cobertura, links, artefatos e ratchet |
| Cobertura | árvore `.assistant` | 75/75 operacionais, 3/3 exemplares, 0 pendentes |
| Composição | árvore `.assistant` | 52 snippets, 7 scripts, 16 prompts |
| Navegação | seis índices R12 | filhos diretos = links dos índices |
| Manual | fonte + raiz | igualdade byte a byte e estado pós-migração |
| Espelho | `ambiente_fonte/` + simulado | equivalência byte a byte de arquivos publicáveis |
| Sensibilidade do gate | mutantes R13 | seis defeitos sintéticos devem ser rejeitados |
| Regressão | `tools/ci_local.py` | todas as etapas locais aprovadas |
| Homologação Databricks | fora do escopo | não inferida a partir dos testes locais |
