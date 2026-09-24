# 13 — Minuta do adendo operacional ao Skill Enforcement Rollout

**Estado: FORMALIZADO PELO ADR-0023 NA CANDIDATA B0; QUALIFICAÇÃO TÉCNICA PENDENTE.**

O ADR-0023 formaliza esta mudança operacional e complementa o ADR-0022 sem reescrever seu corpo decisório. Este documento permanece como explicação operacional longa; em caso de divergência normativa, o ADR-0023 é o registro decisório.

## Contexto

A SER01 foi integrada. O usuário aprovou substituir execução estritamente sequencial por autoria repo-side, execução local paralela governada, auditorias independentes e integração serializada. A ordem histórica das sprints não constitui dependência funcional universal.

## Decisão

1. Preservar nomes e objetivos SER02–SER16, targets, fonte única, evidência por SHA e host, dados sintéticos e proibição de promoção corporativa.
2. Permitir autoria e execução de frentes independentes contra uma base identificada, mediante manifesto e DAG aprovados. A exigência de começar cada execução somente após integrar a anterior deixa de valer para essas tarefas independentes.
3. Manter as dependências próprias L2→L4: L4 não é certificado/promoção aceita antes do L2 correspondente aceito e de contratos compartilhados prontos.
4. Permitir integração de lotes pequenos nominalmente definidos. A ordem SER numérica é rastreabilidade, não autorização tácita nem obrigação de esperar uma frente independente bloqueada.
5. Centralizar implementação, schemas, casos, oráculos, command registry e correções na autoria repo-side. Workers locais executam/auditam tarefas fechadas e não alteram critérios ou produto.
6. Reservar integrador/publicador como escritores exclusivos dos espaços compartilhados. O integrador local executa somente preparação mecânica aprovada; decisão funcional volta à autoria.
7. Separar diagnóstico de certificação. Diagnóstico agrega falhas independentes; certificação usa candidata congelada, uma tentativa por rodada, sem reparo/retry-until-green.
8. Preservar FAILs e estados históricos. Introduzir critérios atuais vinculados à projeção de policy aprovada, não ao resultado que o código gostaria de declarar. Nenhum gate SEF é omitido sem mapeamento explícito.
9. Preservar autorização de efeitos, promoção e merge como gates humanos distintos. O aceite desta direção não aceita candidatas futuras nem autoriza publicação geral.
10. Exigir qualificação do mecanismo, isolamento e dois pilotos sem colisão antes de ampliar concorrência. Limites de cliente e permissões efetivas são medidos; nomes de modelos não substituem essas provas.
11. Classificar evidência pela observação disponível. Declaração de intenção/uso por modelo não equivale a ferramenta chamada, e hash não autentica pessoa.
12. Confirmar pacote publicado e claims pós-policy separadamente do merge. Qualquer capacidade não disponível permanece explicitamente fora da promoção efetiva.

## Consequências

O processo reduz handoffs e repetição de infraestrutura sem permitir que agentes paralelos alterem o contrato que os avalia. A responsabilidade de autoria cresce na preparação: cada pacote deve chegar ao laboratório com implementação e testes realmente prontos. Falha compartilhada bloqueia os consumidores afetados; falha de domínio não precisa interromper todas as frentes independentes.

A formalização não modifica policy nem atribui resultados de runtime. As seis skills já no target entram em regressão. MM/PSEF mantêm suas branches/decisões próprias; cardinalidade ou engine comum não podem mudar incidentalmente durante uma campanha congelada.

## Critério de vigência executável

O adendo pode registrar a decisão operacional antes do código. A execução paralela só é liberada após B0 qualificado, perfil completo, autorização local delimitada e release verificada. A vigência documental não equivale à prontidão técnica da infraestrutura.
