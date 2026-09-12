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
| Objeto | `README.md` na pasta do recurso | conceito aplicado, adequação, requisitos, interpretação e rota para exemplo |

Um nível aponta para o seguinte; não copia a explicação longa dele. Quando dois
documentos precisarem do mesmo fato mutável, um é declarado dono e o outro usa
link e síntese curta.

## Contrato de um README

As entradas agregadoras devem responder, nesta ordem sempre que aplicável:

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

- PT-BR na prosa; preserve nomes existentes de função, classe, parâmetro e
  coluna, inclusive quando forem portugueses. Não traduza APIs para uniformizar
  a documentação.
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

## README de objeto — R01

A escala Objeto segue `ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md`
e seu checklist editorial. É complemento do ADR-0007/0010, conforme proposta
ADR-0012. Novos snippets, scripts e prompts incluem README; legados têm dispensa
transitória rastreada, que só diminui. O gate mede estrutura, não qualidade da
explicação nem execução.

Pausar ao fim da sprint com checkpoint e diff. Template candidato em R01; piloto
e aceite antes de congelar 1.0. Documento pequeno não precisa de texto de
enchimento. Relatórios discriminam READMEs, outras documentações, ferramentas
e derivados. Preservar imagens e corpos históricos. Não carregar READMEs em
massa nas instruções nem criar outro catálogo ou glossário.
