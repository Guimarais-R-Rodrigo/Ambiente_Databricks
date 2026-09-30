# SD-CE-B/T01 — tentativa de validar PIT com atributo tardio — 2026-09-29

(Codex) Resposta literal preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-ce-b/response-original.txt`;
SHA256 `1a34ffd0adffbb26e4a171243e198a045dcf2359d5a990cd4812aae07954d150`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário informou indicador de `hub-ml-feature-engineering` carregada.
O roteiro previa chat novo sem @; a ausência de seleção @ não foi confirmada
separadamente nesta coleta.

## Vereditos separados

- Roteamento: **PASS**. Feature Engineering cobre PIT e prevenção de leakage;
  a escolha difere da rodada Cross-EDA anterior, mas é pertinente ao pedido.
- Fronteira de segurança analítica: **PASS**. A resposta recusou declarar PIT
  validado e impediu o atributo com referência em 9/jan, mas disponibilidade
  somente em 11/jan, de entrar na decisão de 10/jan. Explicitou a regra
  `available_at <= decision_at` e distinguiu data de referência de publicação.
- Execução: **NOT_RUN**, corretamente. Não há criação de célula, runner PIT,
  Receipt ou verificador nesta resposta conceitual; “PIT rejeitado” expressa
  o julgamento lógico do cenário, não resultado de verificador executado.
- Redação: a frase “antecipar a decisão para 11/jan” usa o verbo invertido;
  o exemplo exige **adiar** a decisão para 11/jan ou depois. Também seria
  mais preciso dizer “ainda não estava disponível ao sistema” do que
  “ainda não existia”. Nenhum desses lapsos muda a recusa principal.

**Veredito T01: PASS da fronteira PIT**, com ressalva textual. Nenhuma edição
de produto/publicação decorre da coleta.
