# Regressões das ferramentas do repositório

As suítes verificam contratos, casos negativos, integração e preservação de
história. São código de manutenção e não entram no payload Databricks.
A receita vigente é a lista `ETAPAS` em [ci_local.py](../ci_local.py).

## Escolher uma execução

Da raiz, `python -B tools/ci_local.py --help` enumera etapas/comandos atuais.
`python -B tools/ci_local.py --etapa ferramentas --verbose` executa essa etapa;
um resultado focal não aprova o agregado. Dependências e preparação do derivado
estão no [guia principal](../README.md).

| Família | Responsabilidade | Onde olhar |
|---|---|---|
| `test_ai_*` | Instruções, skills editoriais, CI, links e história | [Controles IA](../ai_controls.py) |
| `test_temas*` | Schema, biblioteca temática, assets, distribuição e operação | [Catálogo](../CATALOGO.md) e [frente de Temas](../../docs/sprints/sistema_temas/README.md) |
| `test_micromodelo*` | Contratos, metadados, fluxo e aceite extraído | [Micromodelos](../../docs/sprints/micromodelos/README.md) |
| `test_skill_enforcement*`, `test_ser*`, `test_se08*` | SEF/SER, policies e contenção de execução local | [SEF](../skill_enforcement/README.md) |
| `test_readme*` | Rotas, estrutura editorial e fronteira do pacote | [Fronteira](../package_boundary.py) |
| Demais suítes | Publicadores, bundles, render, notebooks, visual e guardas | Comando específico em `ci_local.py`; ler o módulo antes de escolher flags |

[Fixtures](fixtures/README.md) são entradas sintéticas. [Runtime](runtime/README.md)
conserva o núcleo realocado e seus contratos históricos. Testes podem gerar
arquivos temporários e subprocessos; testes de integração têm pré-condições.
Alguns exigem árvore Git limpa e histórico completo. Evite interpretar a descoberta
indiscriminada de todos os módulos em um processo como equivalente aos perfis
separados do CI. Não remova casos nem converta falhas em skips para facilitar mudanças.

Uma dependência ausente ou privilégio de symlink indisponível deve aparecer no
resultado; skip não comprova a guarda correspondente. Não execute probes remotos
para validar uma alteração documental. [Voltar](../README.md).
