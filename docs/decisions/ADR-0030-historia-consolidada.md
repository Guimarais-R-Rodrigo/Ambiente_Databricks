# ADR-0030 — Entrada única da construção histórica

Data: 07/10/2026. Estado: execução local autorizada pelo usuário. Autoria: Codex.
Base examinada: `6ac0060dfcd09134634abe204474debb5757e231`.

## Contexto

O CHANGELOG já sintetizava os marcos após a reorganização de 06/10. O plano
mantinha 911 linhas, misturando intenção de agosto, etapas concluídas e
checkpoints posteriores. Duas entradas exigiam reconciliação de estados antigos
por quem assumisse a manutenção, inclusive uma LLM.

## Decisão

1. Manter `CHANGELOG.md` como nome canônico, compatível com o protocolo de
   registro existente, e apresentá-lo como construção histórica consolidada.
   Integrar intenção, etapas e aprendizados do plano numa síntese cronológica;
   preservar os marcos já publicados, com data, autoria e limites.
2. Transferir a decisão vigente da paleta para seção própria no consolidado.
   Manter `PLANO_HUB.md` somente como localizador, inclusive a âncora da §2.2.
   Não criar outro diário nem carregar a história inteira no núcleo AGENTS.
3. Preservar plano integral pelo commit e hash abaixo; não copiar suas centenas
   de linhas para outra entrada ativa. O snapshot integral do changelog, seu
   manifesto, ADRs aceitos e evidências encerradas continuam byte a byte intactos.
4. Aposentar apenas a exceção de `historical_exceptions` que autorizava uma
   referência antiga em `PLANO_HUB.md`: esse trecho não existe mais no
   localizador. Nenhuma outra exceção, origem congelada ou guarda é relaxada.
5. O template mantém o critério de marcos materiais e explicita a síntese da
   trajetória. As metas editoriais passam a 200 linhas e 16 KiB na entrada
   consolidada; ultrapassá-las exige snapshot verificável dos marcos, preservando
   a trajetória. São metas de leitura, não autorização para excluir fatos.
6. Owners e contratos vigentes continuam responsáveis por estado e operação.
   A síntese não promove policy, certifica runtime nem autoriza publicação.

## Recuperação do plano integral

[Texto congelado](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd/PLANO_HUB.md).

- Commit de origem: `09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd`.
- Path: `PLANO_HUB.md`.
- SHA-256 dos bytes Git: `4307e9c3dd6301b7b04733f6ebaebaa8d6ab41215550e6817bb0b68b39ac125f`.
- Blob Git: `3b739b4f0246405df044cc8e6ffe9e9bce906ac2`.
- Tamanho: 49279 bytes; 911 linhas.
- Exceção aposentada: linha declarada no mapa 614, SHA-256
  `2d792709ad83cb7e6debcf34ecc0366dde6302e7cb327e42f7ba4e339dc39ecc`, referência ao antigo arquivo `genie-code-oficial.md` da pasta de regras Claude.
  A identidade é o hash do trecho; cabeçalhos posteriores deslocaram sua linha.

Em checkout completo, conferir o hash sem transformação de encoding/newlines:

```sh
python -c "import subprocess,hashlib; b=subprocess.check_output(['git','show','09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd:PLANO_HUB.md']); print(hashlib.sha256(b).hexdigest())"
```

Para ler: `git show 09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd:PLANO_HUB.md`.
A evidência integral exige o histórico Git; um ZIP somente com a árvore atual
contém a síntese e o link congelado, não todos os bytes históricos.

## Consequências e verificação

A leitura inicial passa a ter uma única narrativa e os mesmos marcos. O nome
`CHANGELOG.md` conserva o protocolo de manutenção e `PLANO_HUB.md` conserva o
caminho de entrada antigo. Referências históricas continuam datadas: o localizador
permite chegar ao texto integral para consultar seções diferentes da §2.2.

## Verificações locais — 07/10/2026

Executadas sobre a base examinada com o diff desta decisão; repetição do validador
após o fechamento documental antes do commit.

| Verificação | Resultado e alcance |
|---|---|
| Preservação da cronologia | todos os marcos anteriores preservados; só a introdução geral foi reposicionada |
| Recuperação do plano | bytes idênticos na base examinada e no merge público indicado; SHA-256 conferido |
| `python -B tools/tests/test_ai_history.py -v` | 17 testes aprovados, incluindo ordem/hashes dos 198 registros e negativos das exceções |
| `python -B tools/ai_controls.py --check` | PASS; 215 requisitos, cinco skills, 708 pares de produto, zero avisos |
| `python -B tools/package_boundary.py` | PASS; zero erros de fronteira |
| `python -B tools/ci_workflows.py --check` | PASS; nomes dos checks, receitas e dependências preservados |
| `python -B tools/validate_assistant.py` | APROVADO; zero falhas e zero avisos na fonte |

Produto, workflows, adapters, arquivos Git, AGENTS e os ADRs anteriores foram
comparados com a base: 775 arquivos preservados byte a byte. O mapa IA difere
somente pela exceção obsoleta explicitada nesta decisão.
Os gates são locais; CI remoto, Databricks e carregamento nativo do Copilot
não são certificados por esta mudança documental.

[História consolidada](../../CHANGELOG.md) · [Índice de decisões](README.md)
