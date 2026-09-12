# Reprodução e manutenção da V01

## 1. Onde executar e o que esperar

Este guia é para quem mantém o repositório. O usuário não técnico apenas lê o
[guia de primeiro uso](GUIA_PRIMEIRO_USO.md), sem instalar Python ou executar células.
A V01 valida uma especificação e seus exemplos. Não aplica temas, não acessa
bases, não instala Apps e não publica arquivos no workspace. `tools/` não é produto.

Use uma cópia Git isolada, com histórico completo. O contrato de READMEs consulta
o histórico das dispensas: clone raso é recusado e não deve ser transformado em
aprovação retirando a guarda. Confira `git rev-parse --is-shallow-repository`;
a saída esperada é `false`. Caso seja `true`, obtenha um clone completo no ambiente
autorizado. Não limpe nem sobrescreva o trabalho de outra pessoa.

A base desta composição é `b88a9ccdde6e61892bc25eb7cf4f4b2577badb23`, que integra
READMEs, Concierge e a V00. A candidata local anterior não era esta composição;
seus logs permanecem históricos. As evidências desta rodada têm registro próprio.

## 2. Preparar o ambiente

Na raiz do checkout, confira `git status --short` e `git rev-parse HEAD`.
Python e Git devem estar instalados no ambiente de desenvolvimento autorizado.
Crie um ambiente virtual e instale as dependências de manutenção:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r tools/requirements-dev.txt -r tools/requirements-temas-dev.txt
```

No Linux/macOS, a ativação correspondente é `source .venv/bin/activate`.
Não altere políticas de segurança do PowerShell para contornar bloqueio: use o
interpretador autorizado diretamente ou peça apoio ao mantenedor. Exemplo sem
ativação: `.venv\Scripts\python.exe -B tools/temas_v01_contract.py`.

`jsonschema` e `referencing` são dependências adicionais da **manutenção**; não
são instaladas no Databricks por esta entrega. As versões medidas constam no
relatório, não representam uma versão de Databricks Runtime.

## 3. Executar e interpretar

Execute os comandos separadamente e confira os resumos e o código de saída:

```powershell
python -B tools/temas_v01_contract.py
python -B -m unittest discover -s tools/tests -p "test_temas_v01*.py" -v
python -B tools/tests/test_inventario_visual.py
python -B tools/tests/test_visual_legado_v00.py
python -B tools/tests/test_baseline_visual_runner.py
python -B -m unittest discover -s tools/readme_visuals/tests -p "test_*.py" -v
python -B tools/ci_local.py --verbose
python -B tools/validate_assistant.py --conferir-readme
```

No PowerShell, `$LASTEXITCODE` informa o código do último executável: zero é o
resultado esperado. No terminal POSIX, use `echo $?` imediatamente após o comando.
O contrato retorna `PASS_CONTRATO_LOCAL` e explicita runtime não implementado,
autorização real não testada e usabilidade pendente. Uma suíte com zero casos
não serve como evidência. Não somar subtestes como novos métodos de teste.

O CI vigente mantém oito etapas. O workflow V01 acrescenta verificação separada,
sem retirar gates de READMEs, Concierge ou V00. Ausência de Spark é SKIP, não PASS
de Spark. A validação editorial Node exige suas próprias dependências e comandos;
leia [o guia editorial vigente](../../../../tools/readme_visuals/README.md).
Não use logs Node antigos como prova de uma rodada nova.

## 4. Conferir preservação

Inspecione o diff contra a base real desta candidata, inclusive arquivos adicionais:

```powershell
git diff --name-status b88a9ccdde6e61892bc25eb7cf4f4b2577badb23 -- ambiente_fonte Novo_Ambiente_Simulado MANUAL_TECNICO.md tools/ci_local.py
```

Na V01, a saída esperada é vazia. Não mude a referência para HEAD para ocultar
diferenças. Os hashes de todos os caminhos protegidos e as capturas legadas
sintéticas são conferidos na execução da entrega. Essa restrição vale para o
escopo V01, não proíbe alterações legítimas de sprints futuras com nova aprovação.

## 5. Alterar o contrato sem duplicá-lo

Edite o schema, confira unidade/origem/consumidor e atualize as fixtures completas.
Inclua um caso válido e um mutante que falhe pelo motivo correto. Para gerar a
referência em UTF-8 sem depender da codificação de redirecionamento do PowerShell:

```powershell
python -B -c "import sys; from pathlib import Path; sys.path.insert(0, 'tools'); import temas_v01_contract as c; Path('TOKENS.v01.tmp.md').write_text(c.dictionary(c.read_json(c.PACKAGE / 'theme.schema.json')), encoding='utf-8')"
```

Compare `TOKENS.v01.tmp.md` com `docs/sprints/sistema_temas/V01/TOKENS.md`.
Após revisar, substitua o derivado e remova somente esse temporário conhecido.
Não edite a tabela para mascarar divergência do schema. Uma fixture é entrada de
teste, não tema aprovado. A referência de assets deve concordar com os manifestos
oficiais; não remova um item ou troque seu hash para aceitar uma alteração.

## 6. Erros e suporte

`JSON_*`: sintaxe, codificação, duplicatas ou limite de entrada. `SCHEMA_*`:
verifique campos e tipos; não desative `additionalProperties`. `ENGINE_VERSION`:
o protocolo é candidato; não presuma engine instalado. `ASSET_HASH` ou
`ASSET_REGISTRY`: pare e confira o baseline e os registros oficiais. `PATH_*`:
corrija a referência sem ampliar a raiz. `POLICY_*`: a governança foi alterada;
exige revisão. `TOKEN_DOC_DRIFT`: regere o derivado. `DOC_LINK`/`DOC_ANCHOR`:
conserte o destino ou a seção. Dependência ausente deve ser informada como tal.

Registre commit, comando, ambiente, código de saída e mensagem sem dados sensíveis.
Preserve tentativas malsucedidas e a rodada final com nomes distintos. Reexecução
própria não é auditoria independente e links válidos não provam compreensão humana.

## 7. Revisão, integração e retorno

Esta branch parte da main integrada. Antes de qualquer merge, reconfira se a main
avançou, faça a composição sem sobrescrever outra frente e repita os gates.
O ADR-0013 permanece proposto até aceite explícito. O pedido para continuar a
implementação não autoriza publicação Databricks nem homologação fictícia.

Sem merge, retorno significa arquivar a candidata. Após eventual integração,
use um PR de reversão revisado, preservando mudanças posteriores. Não use
force-push, reset destrutivo ou cópia de pastas por cima da main. A V02 só começa
após revisão do contrato e do checkpoint desta sprint.

[Voltar à V01](README.md) · [Testes e aceite](TESTES_E_ACEITE.md)
