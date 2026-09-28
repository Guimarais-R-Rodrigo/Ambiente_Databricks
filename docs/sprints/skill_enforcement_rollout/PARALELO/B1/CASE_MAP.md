# Mapa de casos — alcance desta candidata

| Caso | Evidência nesta etapa | Limite |
|---|---|---|
| VF01 | Requests/fixtures, cálculo público e Receipt V1 validados no checkout completo | Perfil mensal/binário; não equivale a certificação |
| VF02–VF05 | Negativos de MOB, target, cumulatividade e duplicidade executados | Perfil mensal/binário |
| VF06–VF09 | Ausência, roster, periodicidade e maturidade executados | Recusa de trimestre não prova suporte trimestral |
| VF10 | Fingerprint de request, Receipt real e verifier exercitados, incluindo replay/tamper | Evidência local de autoria; campanha P2 não iniciada |
| VF11 | Semântica evento/cumulativo e gap com reentrada exercitados | Não inferir eventos em períodos não observados |
| VF12 | Estimando monetário bloqueado | Não há cálculo de perda monetária |
| CE01–CE02 | Contexto obrigatório e triestado exercitados | Identidades declaradas, não fonte lida |
| CE05–CE07 | Fronteira/fuso/empate/latência/bitemporalidade guardados | Metadados; sem provar seleção de linhas |
| CE08 | Binding do contexto implementado | Não é Receipt de join |
| CE10 | Contexto estático resolvido sem forçar PIT | Sem medir cobertura ou cardinalidade real |
| CE03–CE04/CE09/CE11/CE12 | Não executados | Dependem de SER06, Spark/output/Postflight ou integração cross-skill |

Todos os IDs Python estão em `tools/tests/test_ser_b1_domains.py`. Os casos com múltiplos estímulos usam `subTest`; número de métodos não equivale ao número de variantes nem a cumprimento de toda a obrigação do dossiê.
