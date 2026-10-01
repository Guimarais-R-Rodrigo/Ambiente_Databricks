# Autoria de skill: estrutura e JSONs SEF

Este roteiro complementa o [molde de skill](../../../hub_padroes/skill/template.md).
Use-o ao criar uma skill na fonte canônica do Hub. Ele descreve a **forma** e as
verificações; não concede autorização de escrita, promoção de policy ou uso no
Databricks. Leia os arquivos reais da revisão em que está trabalhando.

## 1. Delimitar a capacidade

Procure uma skill ou helper existente antes de criar outra pasta. Defina pedido
positivo, pedido que deve ir a uma especialista vizinha, entradas, saída e
efeitos permitidos. Execute o preflight L2 de `hub-ml-criar-objeto` com
`operation=create`, `object_type=skill`, nome `hub-ml-<tema>` e o contexto
exigido pelo [SKILL.md](../SKILL.md). PASS do preflight resolve tipo, nome,
molde e destino; não cria nem certifica a skill. A rota determinística
`object_validation` desta versão **não suporta** `object_type=skill`.

## 2. Escrever o contrato mínimo L1

Crie `skills/hub-ml-<tema>/SKILL.md` pelo molde: frontmatter com somente
`name` e `description`, depois as cinco seções e referências relativas
necessárias. A descrição deve incluir quando usar e o limite que evita colisão.

Crie `skills/hub-ml-<tema>/execution_contract.json`. Comece pelo formato da
skill existente de escopo mais próximo; este exemplo é **esqueleto L1**, não
um contrato aprovado para um domínio novo:

```json
{
  "schema_version": "0.1",
  "skill": "hub-ml-<tema>",
  "mode": "audit",
  "metadata": {
    "se07": {
      "enforcement_level": "L1",
      "scope": "stage_specific",
      "runtime_gate": false,
      "static_invariants": ["invariante_especifico_verificavel"]
    }
  },
  "resources": [],
  "templates": []
}
```

Substitua os placeholders antes de validar. `resources` identifica helpers
realmente usados, com módulo, símbolo, política e evidência compatíveis com o
contrato; não declare import ou chamada apenas porque o caminho existe.
`templates` lista somente recursos relativos da própria skill que serão
consultados. O contrato de `hub-ml-micromodelos` é um exemplo real de L1;
o de `hub-ml-baseline-ml` mostra campos adicionais de uma candidata executável.
Os JSONs de SEF não são o `micromodelo.schema.json`: este valida o YAML de
um micromodelo, não a estrutura de uma Agent Skill.

## 3. Registrar a entrada na policy central

Adicione **uma entrada** à lista `skills` de
`hub_padroes/skill_enforcement/policy.json`, mantendo os demais registros.
Escolha `risk_class`, `scope_mode`, superfícies e dívida pelo risco da nova skill.
Para L1, `current_level=L1` exige `SKILL.md` e `execution_contract.json`
presentes. `target_level` pode apontar uma evolução aceita, mas não prova que
ela já existe. Cada `protected_surface` declara `id`, `level`, `evidence` e
`rationale`; superfícies futuras podem constar com nível acima do atual, desde
que não excedam o target e não sejam descritas como executadas.

```json
{
  "skill": "hub-ml-<tema>",
  "risk_class": "high",
  "current_level": "L1",
  "target_level": "L1",
  "scope_mode": "stage_specific",
  "rollout_mode": "audit",
  "policy_status": "defined",
  "rationale": "Motivo específico da proteção.",
  "implemented_artifacts": [
    "skills/hub-ml-<tema>/SKILL.md",
    "skills/hub-ml-<tema>/execution_contract.json"
  ],
  "protected_surfaces": [
    {
      "id": "superficie_especifica",
      "level": "L1",
      "evidence": "static",
      "rationale": "O que o contrato estático protege."
    }
  ],
  "known_debt": []
}
```

Isto é **um item da lista**, não o arquivo inteiro. Os valores de risco e
rollout são escolhas de projeto a justificar, não defaults a copiar. Não use
`enforce` nem eleve `current_level` para refletir intenção futura.

## 4. Acrescentar execução somente quando existir

| Nível presente | Artefato e evidência necessária |
|---|---|
| L1 | Contrato estruturado e referências existentes. |
| L2 | `scripts/preflight.py` devolve diagnóstico antes da superfície protegida. |
| L3 | `scripts/run.py` chama uma rota determinística; Receipt vincula entradas, release, efeitos e resultado, com verificação apropriada. |
| L4 | `scripts/run_enforced.py` e `scripts/postflight.py`: Postflight independente e fail-closed antes de declarar conclusão homologada. |

Desenhe inputs, efeitos, erros e estado de cleanup antes do runner. Não copie
o JSON de uma skill vizinha mudando só o nome: perfis, schemas de entrada,
invariantes, versões de Receipt e superfícies variam. Registre `NOT_RUN` ou
`NOT_AVAILABLE` onde não há execução, em vez de criar evidência fictícia.

`release_manifest.json` **não é um JSON universal obrigatório para L1**.
Crie-o quando a rota executável/validador da skill exigir identidade de release.
Nesse caso, liste os artefatos protegidos usados pela rota, com caminhos
relativos à raiz `.assistant`, papéis e `git_blob_sha1` calculados dos bytes
finais. Inclua scripts, contrato, orientação e dependências que o runner fixa;
se qualquer byte mudar, atualize o manifesto e repita os testes pertinentes.
Não copie hashes ou Receipts de outra release. O manifesto de
`hub-ml-criar-objeto` é um exemplo concreto, não uma licença para promover
outra skill ao mesmo nível.

## 5. Fechar os inventários e verificar

Atualize os índices `skills/README.md`, `.assistant/README.md`, Manual e o mapa
de roteamento das instruções quando a skill nova mudar a escolha do usuário.
Complete o [checklist único](../templates/checklist-objeto-novo.md), registre
`CHANGELOG.md`, gere o derivado pelo renderer e confira o diff; jamais edite
`Novo_Ambiente_Simulado/` à mão.

No checkout do repositório, execute:

```text
python -B tools/skill_enforcement/se07_policy.py
python -B tools/validate_assistant.py
python -B tools/render_simulado.py --write
```

Depois faça testes proporcionais do preflight/runner/verifier que **existirem**.
Um JSON válido e um validator verde não provam roteamento no Genie: prepare
casos positivo, negativo e `@menção` em chats novos e registre carregamento
observado separadamente da qualidade da resposta. Free e trabalho têm aceites
próprios; publicação, promoção da policy e merge são decisões separadas.
