# Handoff — SE07, corretiva da observabilidade de cleanup (ChatGPT)

## Identidade, autorização e parada

Falha auditada na candidata técnica `1932866140a5ef0eceaf9932c26bb7853f108eac`,
árvore `ce47a97b8951160a6c56789dc16f1e073e635454`, do piloto README L3.
Antes da publicação da corretiva, a mesma review recebeu apenas o registro documental
do aceite humano em `44a587074736c45e5c268366a0688581e57b6069`; a corretiva é baseada
nesse SHA para preservar integralmente a decisão humana. Canônica aceita:
`d49c8728f0e47adc15f7f78293c9fcc58c809a15`. O usuário autorizou expressamente
implementar soluções encontradas após a auditoria. Esta corretiva não promove a
canônica, current_level, Free, Genie, PR, Actions, merge ou SE08.

A candidata original permanece **NAO_APTA**: o bundle final registra falha
obrigatória F-04. Seu FULL 16/16 posterior não apaga o vermelho. A nova implementação
é candidata corretiva, não auditoria independente de si mesma nem aceite humano.

## Achado e solução implementada

`TemporaryDirectory.__exit__` podia falhar depois de `_run` registrar o processo
como INTERRUPTED/130 e cleanup COMPLETE. A exceção de remoção escapava antes do
retorno ou relançamento de SystemExit; `main` respondia 2. O mesmo mascaramento
atingia SystemExit(8) e cancelamento durante Git opcional.

A reprodução usa processo real, prontidão observada e erro de cleanup
**sintético explicitamente identificado**. Não reproduz a causa nativa do WinError32.

A corretiva em `tools/skill_enforcement/certify_local.py`:

- distingue `process_cleanup`, `temporary_cleanup` e o `cleanup` agregado;
- só persiste COMPLETE agregado após o término do contexto e ausência observada
  do diretório temporário; antes disso usa PENDING;
- conserva exceção original de cleanup, tipo, errno, winerror, filename e stack;
- conserva também eventual erro do corpo/journal, saída parcial, resultado do
  processo e exit realmente observado;
- mantém INTERRUPTED/130 ou SystemExit não zero mesmo quando cleanup lança OSError;
- continua falhando quando um comando exit 0 sofre falha de cleanup.

Não há retry de remoção, `ignore_cleanup_errors`, aumento de timeout, dispensa de
asserção, alteração de thresholds, nova estratégia de kill ou mudança de APIs Win32.
A causa nativa do compartilhamento permanece **NÃO ESTABELECIDA**. Não declarar
WinError32 resolvido nem multiplataforma PASS por causa desta corretiva.

## Testes e alcance

Nova suíte: `python -B tools/tests/test_certify_storage_cleanup.py -v`.
São nove métodos; cancelamentos usam subcasos KeyboardInterrupt/SystemExit
0/None/8, no gate e Git opcional. Inclui controle positivo, comando exit 0,
comando exit 7, timeout real após ready, resíduo e erro simultâneo no journal.
O exit é observado em subprocesso; PIDs são conferidos por oráculo externo.

`test_validate_create_readme.py` foi ajustado para não chamar cleanup total de
COMPLETE no cenário de erro sintético: exige processo COMPLETE, temporário FAILED,
agregado FAILED, preservação de INTERRUPTED/130 e do WinError32 sintético.
O teste não foi dispensado ou convertido em skip.

O perfil FULL continua com os mesmos 16 gates. A nova suíte é gate separado
obrigatório nesta corretiva, assim como as duas suítes específicas do piloto.
Ver [matriz vigente](../sprints/skill_enforcement/SE07/TESTES.md).

A cópia auditada foi reconstruída por hashes e corresponde ao commit/árvore
originais, mas tem histórico Git raso. Não remover o marcador shallow para fingir
histórico completo. Ensaios repo-side em bancada com raiz Git sintética própria,
quando usados, devem ser rotulados como testes de código/fixtures, não FULL da
candidata publicada. Os logs externos identificam ambiente, SHA, árvore e escopo.
A primeira bancada sintética sem versão anterior à introdução do controle de
migração falhou no ratchet, como exigido. Seus logs foram preservados. Uma bancada
de testes com inventário anterior e introdução sintética do controle continua
sendo apenas fixture, nunca reconstrução da história real do projeto.

## Próximo gate

Codex deve revisar o commit corretivo publicado sem tratá-lo como aprovado e
executar os gates serializados sobre o SHA congelado em clone completo
Windows/NTFS/Python 3.12.14. Investigar separadamente o erro
nativo de compartilhamento; preservar toda recorrência e toda tentativa.

Se houver nova falha nativa, não repetir até ficar verde nem apagar seu efeito
sobre a prontidão. Registrar o que foi observado, o que não foi identificado e
submeter decisão explícita sobre dívida residual. Depois: nova auditoria externa
→ decisão humana. SE06 permanece 24/25, A1-R4 NOT_RUN, DoD INCOMPLETE e
FULLY_CERTIFIED=false. O produto e o manifest L3 não foram alterados nesta corretiva.
