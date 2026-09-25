# Registro da autoria B1 — 24/09/2026

(ChatGPT) Implementadas as primeiras fachadas candidatas SER03/SER05, contexto temporal compartilhado, schemas fechados, manifesto de integridade da safra e testes nativos de domínio. A primitive de safra, Receipt V1, preflight SEF e B0 permanecem inalterados.

A integração final deste registro no CHANGELOG raiz acompanha o fechamento do pacote P1 e o render/validator completo. Este arquivo não afirma conclusão da sprint nem altera a policy.

(Codex) Integração P1 observada no checkout completo: 47/47 testes B1, integração pública 2/2, Temas V07/V07 mirror/V08 verdes, canal SE07 histórico classificado como `EXPECTED_TEMPORAL_FAIL`, validator e renderer canônicos aprovados. A autoria permanece não certificada; policy, B0, Databricks, Ready e merge não foram alterados.

(ChatGPT) P1 auditada independentemente a partir do bundle pós-import-path e do estado remoto: PR #115 draft, main preservada, 44 paths dentro do escopo e policy L0 mantida para SER03/SER05. Veredito P1: autoria integrada PASS, sem certificação.

(ChatGPT) P2 repo-side materializa a primeira campanha real governada em `tools/skill_enforcement/real_campaigns/b1/`: registry B1 fechado, release identity B1, adapter aditivo sobre launcher/verifier B0, DAG 2/1, coverage caso→teste→oráculo→command, auditorias de domínio e gerador mecânico de handoff. A campanha ainda não foi executada localmente.

(ChatGPT) Contraditório P2 endureceu a identidade antes do primeiro run: bindings exatos de todo o B0 qualificado na PR #113, preservação dos bytes funcionais P1, profile_digest obrigatório no handoff e evidence/output fora do repositório. Nenhum gate local foi executado por este commit.

(ChatGPT) Segundo contraditório P2: o handoff agora recusa divergência campaign↔release-spec e grava no execution_argv o python_executable real congelado, não o token simbólico {PYTHON}. O metateste cobre ambos.

(ChatGPT) Fechado o envelope P2 antes do run local: ADAPTER_RESULT persistido externamente e post_run_package_argv reutilizando RAW/SHARE + sanitização V2 + verificação B0; somente o ZIP SHARE deve ser enviado para auditoria, RAW permanece privado.

(ChatGPT) O retorno P2 foi fortalecido para AUDIT_BUNDLE.zip: SHARE sanitizado + RAW_SHARE_BINDING + ENVELOPE_VERIFICATION + AUDIT_CONTEXT + manifesto/scan do bundle público; RAW continua privado.

(ChatGPT) Autoridade ambiental fechada: P2 2/1 exige Windows+NTFS no preflight; Linux/Cloud ou Windows não-NTFS bloqueiam antes de prepare. Também removida inferência frágil do path RAW no AUDIT_CONTEXT.
