# Modelos inativos

Os JSONs são exemplos de estrutura do plano, não autorizações nem tasks executáveis. Campos nulos identificam o que a autoria terá que resolver; `launchable=false` é deliberado. O launcher de produção deve recusá-los como manifesto runtime.

O template de achado não afirma finding real. O template de gate humano não atribui consentimento. O registro de caso desta entrega não deve ser usado para emitir Receipt ou PASS de uma skill.

Na implementação B0, estes exemplos serão substituídos por exemplos válidos contra os schemas de produção, com dados sintéticos explícitos e nenhum segredo. Os schemas runtime ainda precisam ser implementados e adversarialmente testados.
