# `tools/` — gates e automação do repositório

> **MANUTENÇÃO · NÃO PUBLICADO.** Estes arquivos rodam na máquina que mantém o
> Git. O usuário do `.assistant` no Databricks não recebe esta pasta.

As ferramentas convertem regras editoriais e arquiteturais em verificações que
podem reprovar uma mudança.

## Comandos por objetivo

| Objetivo | Comando |
|---|---|
| validar fonte e repositório | `python tools/validate_assistant.py` |
| conferir saídas coladas no README | `python tools/validate_assistant.py --conferir-readme` |
| regenerar o derivado | `python tools/render_simulado.py --write` |
| publicar no Free | `python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>` |
| conferir o remoto (inventário e tipos) | `python tools/publicar_free.py --verify --profile <free> --expected-host <url-free>` |
| conferir o remoto **por conteúdo** | `python tools/publicar_free.py --verify --conteudo --profile <free> --expected-host <url-free>` |
| executar smoke no Databricks | importar/submeter `tools/spark_smoke_test.py` |
| criar pacote de auditoria | `python tools/bundle_para_auditoria.py --mode canonical` |
| criar ZIP de implantação | `python tools/bundle_implantacao.py` |

## Ciclo mínimo

```powershell
python tools/validate_assistant.py
python tools/render_simulado.py --write
python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>
python tools/publicar_free.py --verify  --profile <free> --expected-host <url-free>
```

`--execute` altera o workspace e recusa espelho desatualizado antes de escrever.
`--verify` é leitura. Sem `--conteudo` ele compara inventário e tipos: um módulo
com o mesmo nome e o mesmo tipo, porém conteúdo diferente, passaria. Com
`--conteudo` cada objeto é exportado e comparado byte a byte na representação
canônica — só então é possível afirmar equivalência entre local e remoto. A
saída declara o alcance da comparação em toda rodada. Publicar sem verificar não
fecha o gate.

A normalização da comparação é mínima e declarada: fim de linha, e fim de arquivo
apenas em notebook. Comentário, espaço e linha em branco **não** são removidos —
fazê-lo mascararia diferença real. Por isso a saída registra dois hashes: o bruto,
que identifica os bytes do pacote, e o normalizado, que é o único comparável com
o remoto.

## Inventário

| Arquivo | Responsabilidade |
|---|---|
| `validate_assistant.py` | estrutura, YAML, links, Python, contratos, identidade e consistência |
| `render_simulado.py` | recriar o espelho de workspace a partir da fonte |
| `publicar_free.py` | plano, publicação protegida e conferência remota |
| `spark_smoke_test.py` | chamadas funcionais no runtime Databricks |
| `api_publica.py` | extrair API pública por AST e gerar `__init__.py` |
| `notebook_marker.py` | distinguir módulo Python de notebook Databricks |
| `project_policy.py` | centralizar identidade neutra, skills e diretórios gerenciados |
| `bundle_para_auditoria.py` | pacote canônico, de segurança ou completo para revisão |
| `bundle_implantacao.py` | ZIP mínimo sanitizado com manifesto SHA-256 |

Os três módulos de apoio evitam que render, publicação e validação inventem
definições diferentes para o mesmo objeto.

## O que cada gate prova

```mermaid
flowchart LR
  V["validação local"] --> VP["forma, links,<br/>contratos e higiene"]
  R["verify remoto"] --> RP["inventário, tipos,<br/>ausentes e obsoletos"]
  S["smoke Spark"] --> SP["execução real<br/>no runtime"]
  F["forward tests"] --> FP["roteamento<br/>da skill"]
```

Nenhum gate substitui o outro:

| Gate | Não prova |
|---|---|
| validação local | execução em Spark ou comportamento conversacional |
| verify remoto | correção do código |
| smoke | ACLs, políticas e runtime do trabalho |
| forward test | qualidade da resposta ou resultado numérico |

## Pacotes de auditoria e implantação

`bundle_para_auditoria.py`:

- `canonical`: fonte e governança vigentes;
- `security`: acrescenta manifesto de todos os caminhos versionados;
- `full`: inclui material congelado permitido pela política.

`bundle_implantacao.py` leva apenas o produto sanitizado e o manifesto. Por
padrão, ambos recusam worktree sujo para não atribuir conteúdo novo ao commit
anterior.

`.artifacts/` é saída local e não fonte de verdade. Um ZIP citado em relatório
datado representa aquele commit; não existe alias “latest”. Para implantar,
gere o bundle novamente em HEAD limpo e confira `source_commit` e os hashes do
`MANIFEST.json`.

## Acrescentar uma verificação

1. Registre no docstring qual defeito real a guarda previne.
2. Construa um mutante que viole a propriedade.
3. Prove que o mutante reprova e que o caso válido passa.
4. Exponha contagem ou evidência que revele varredura vazia.
5. Atualize teste, documentação e `CHANGELOG.md`.

Uma contagem não substitui identidade exata, e “alguma exceção” não substitui a
assinatura esperada do erro.

## Onde continuar

- [Ciclo de vida](../docs/playbooks/ciclo-de-vida.md)
- [Testes e evidências](../docs/testes/README.md)
- [Decisões arquiteturais](../docs/decisions/README.md)
- [Skills operacionais](../.claude/skills/README.md)
