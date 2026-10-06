# Modelos inativos

Os JSONs são exemplos de estrutura do plano, não autorizações nem tasks executáveis. Campos nulos identificam o que a autoria terá que resolver; `launchable=false` é deliberado. O launcher de produção deve recusá-los como manifesto runtime.

O template de achado não afirma finding real. O template de gate humano não atribui consentimento. O registro de caso desta entrega não deve ser usado para emitir Receipt ou PASS de uma skill.

B0 já dispõe de [schemas de produção](../../../../../tools/skill_enforcement/parallel/schemas/). Estes modelos continuam deliberadamente incompletos, com `launchable=false`; não foram promovidos a campanha executável. Consulte o [fechamento B0](../B0/README.md) e use o schema adequado para preparar, validar e autorizar uma campanha nova.
