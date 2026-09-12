# Regra — sistema editorial e READMEs

A documentação precisa permitir duas leituras sem criar duas verdades: uma pessoa
deve achar a próxima ação em menos de um minuto, e uma IA deve localizar o
documento que é dono de cada afirmação sem atravessar duplicações.

## Hierarquia editorial

| Nível | Documento de entrada | É dono de |
|---|---|---|
| Repositório | `README.md` | finalidade, arquitetura, estado dos gates e ciclo de contribuição |
| Governança | `docs/README.md` | rota para decisões, auditorias, testes, playbooks e histórico |
| Produto publicado | `ambiente_fonte/.assistant/README.md` | instalação e uso do ecossistema no Databricks |
| Coleção | `README.md` dentro da coleção | catálogo local, contrato, exemplo mínimo e limites |
| Objeto | `README.md` na pasta de snippet, script ou prompt | conceito aplicado, adequação, requisitos, interpretação e rota de uso |

Um nível aponta para o seguinte; não copia a explicação longa dele. Quando dois
documentos precisarem do mesmo fato mutável, um é declarado dono e o outro usa
link e síntese curta.

## Contrato de um README

Nos READMEs agregadores, responda nesta ordem sempre que aplicável. Para a
escala Objeto, use o contrato específico indicado abaixo, cuja abertura mantém
a rota rápida para o exemplo:

1. **o que é e para quem é**;
2. **qual é a próxima ação**, por objetivo do leitor;
3. **o que acontece automaticamente e o que exige ação manual**;
4. **um exemplo copiável** ou uma rota explícita para o exemplo;
5. **limites, estado verificável e onde continuar**.

Use Mermaid somente quando relações ou sequência ficarem mais claras que em
prosa. Use tabela para comparação e catálogo, não para transformar parágrafos em
células. Registros históricos preservam o relato datado; o redesenho atua na
entrada, no sumário e na navegação, sem reescrever evidência antiga.

## Linguagem e precisão

- PT-BR na prosa. Preserve nomes reais de funções, classes, parâmetros e
  colunas, inclusive identificadores existentes em português; não traduza API
  para adequá-la ao texto. Constantes de domínio mantêm seu referente.
- Distinga visualmente interfaces **nativas da Databricks** de conteúdo
  **customizado pelo Hub**. O prefixo `hub_`/`hub-` marca autoria local, mas uma
  skill `hub-ml-*` usa o mecanismo nativo de Agent Skills.
- Não transforme observação de uma execução em regra universal da plataforma.
  Declare ambiente e data, e aponte a evidência.
- Não documente capacidade não verificada como existente. Use `PENDENTE`,
  `BLOQUEADO` ou `PLANEJADO` e diga qual evidência falta.
- Evite contagens e nomes de versão em mais de um lugar. Se uma contagem precisar
  aparecer no README raiz, ela deve ser conferida por gate.
- Números narrativos usam padrão brasileiro (`3.375.674`, `92,8%`).

## Manutenção

- Todo diretório de primeiro nível tem uma entrada que explique papel, uso e
  limites. Prefira `README.md`; um índice canônico com outro nome é válido
  quando a escolha estiver explícita e não houver navegação concorrente.
- Links relativos precisam funcionar tanto no Git quanto no arquivo publicado
  quando o documento fizer parte de `ambiente_fonte/`.
- O corpo decisório de um ADR aceito é imutável. Erratas factuais, ratificações e
  mudanças de status podem ser anexadas, com data e sem apagar o texto original.
  Uma mudança de decisão exige novo ADR que superseda o anterior.


## Manual Técnico

O Manual Técnico é a explicação aprofundada para leitores não técnicos e o dono
do inventário integrado de helpers e termos (ADR-0010). Edite em
`ambiente_fonte/.assistant/MANUAL_TECNICO.md`; sincronize a cópia de leitura
`MANUAL_TECNICO.md` da raiz e gere o simulado pelo renderer. As três cópias devem
conservar o mesmo conteúdo. Não reintroduza catálogo ou glossário independentes.

## README de objeto — transição R01-A

A unidade é a pasta de objeto, não cada arquivo físico. O README introduz e
ajuda a decidir; o notebook demonstra; implementação e fachada definem a API
real; o prompt conserva seu formulário e bloco colável. O Manual continua dono
do catálogo integrado. Não copie capítulos nem crie catálogo concorrente.

O contrato único está em
`ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md`, roteado pelo
`template.md` da mesma pasta. A revisão usa `checklist_objeto.md`. Não copie as
quinze seções em skills ou outros templates: referencie o contrato.

A R01-A entrega versão candidata, ligada ao ADR-0011 proposto. Ela não declara
migração concluída, exigência automática instalada ou cobertura retroativa.
Os gates e a adoção pelos templates dos tipos pertencem às próximas
micro-sprints; a versão estável depende do piloto R02. Não rotule um legado
como defeituoso somente pela ausência de README durante essa transição.

Preserve os títulos principais; adapte subtópicos e profundidade. Não imponha
mínimo de palavras, exemplos irrelevantes ou alternativas artificiais. Explique
termos e motivos, sem infantilizar nem usar “obviamente” ou “basta” para ocultar
passos. Conceito geral, capacidade implementada, premissa, exemplo ilustrativo
e resultado observado precisam ser distinguíveis.

Uma passagem pela mesma IA é autorrevisão, não auditoria independente. Registre
arquivos efetivamente alterados, verificações, bloqueios e o checkpoint. Não
atribua ao validador qualidade didática, comprovação de execução ou cobertura
que ele ainda não verifica.
