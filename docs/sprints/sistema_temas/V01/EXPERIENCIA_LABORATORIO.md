# Laboratório Visual — especificação textual da experiência

**Protótipo textual, não screenshot, notebook ou App instalado.** Os nomes de
controles abaixo são propostas a homologar na V05. Não há local de menu
Databricks inventado nesta documentação. A versão operacional deverá trocar
as indicações conceituais por nomes e capturas reais do ambiente validado.

## Entrada e orientação

O usuário encontrará um acesso “Aparência do Hub” na entrada autorizada do
produto, após integração. A página deve mostrar de início: versão do laboratório,
contexto escolhido, tema atual, revisão, escopo **prévia pessoal** e aviso
“Alterações aqui não mudam o padrão da equipe”. Deve existir link visível para
o guia de primeiro uso e saída para continuar a rotina anterior.

O painel terá quatro áreas: escolher ponto de partida; ajustar; comparar;
salvar proposta. Publicação aparece em área separada, condicionada a papel e
aprovação. Ausência de permissão não se resolve escondendo apenas um botão:
o servidor/processo também precisa negar a ação.

## Escolher

O início oferece “Atual preservado” como referência e propostas de executivo
claro/escuro conforme cobertura efetivamente homologada. As quatro fixtures da
V01 não constituem quatro temas prontos para uso; nenhuma receberá selo
“aprovado” só porque existe no pacote de testes.

Ao escolher contexto, mostrar componentes abrangidos e não suportados. Alterar
notebook para README não deve traduzir campos silenciosamente. A interface
apresentará outra configuração completa e perguntará pelo destino do rascunho
atual quando houver alterações não salvas. A opção “Cancelar” preservará o estado.

## Ajustar

Mostrar primeiro controles com efeito comprovado no contexto: cor principal,
texto, fundo, densidade e títulos. Expandir “Avançado” para paletas e propriedades
com explicação técnica assistida. Cada controle possui nome em português,
amostra, valor, unidade, limite, efeito previsto e comando de restaurar o valor
inicial. O usuário não deve ver somente um identificador como `brand.primary`.

Seletor e hexadecimal são duas formas de editar o mesmo valor. Normalização de
`#005ca9` para `#005CA9` deve ser mostrada; entrada inválida mantém a última
prévia válida e apresenta a correção junto ao campo. Não limpar o trabalho
inteiro nem converter erro em branco. Teclado e leitor de tela devem alcançar
rótulo, campo, mensagem e ação de desfazer.

Mudar a cor institucional não remapeia categorias de um gráfico sem aviso.
Uma opção “harmonizar paleta” futura deverá criar alterações explícitas e
revisáveis em todos os campos afetados. Uma propriedade não integrada aparece
desabilitada com a razão, não como seletor funcional sem consequência.

## Comparar

A galeria deve usar os mesmos adaptadores do produto, com dados sintéticos e
pequenos: barras, série temporal, mapa de calor, KPI, tabela e cabeçalho. Os
controles não podem treinar, consultar tabelas corporativas ou executar um
pipeline. Capturar métricas de chamadas para provar essa ausência, além de
inspecionar o código. Reexecução do notebook por widget deve continuar segura.

Comparação “Atual / Proposta” preserva dados, filtros, unidades, escalas e
mapeamento das categorias. Mostrar legenda, título longo, negativos, nulos e
múltiplas categorias. A prévia deve corresponder ao tamanho em que a saída será
usada, não apenas a um arquivo ampliado.

Uma área “Impacto” informa: adaptações dinâmicas nesta sessão; arquivos que
precisarão ser gerados de novo; variantes congeladas; consumidores ainda não
integrados. Para PNG/assinatura/fundo raster, não prometer mudança instantânea.
Mudança de template estrutural será outra proposta, não um controle de cor.

## Salvar e revisar

Ações com efeitos distintos:

| Rótulo proposto | Efeito esperado | O que não faz |
|---|---|---|
| Aplicar na prévia | Atualiza apenas a sessão e mantém dados sintéticos. | Não grava padrão nem consulta dados. |
| Desfazer | Retorna ao estado anterior do rascunho. | Não revoga publicação. |
| Restaurar ponto de partida | Retorna à configuração carregada, após proteger trabalho não salvo. | Não altera a versão aprovada. |
| Salvar/exportar proposta | Grava arquivo no destino informado e exibe confirmação. | Não submete, aprova ou publica. |
| Submeter para revisão | Congela a revisão e registra destino solicitado. | Não altera a equipe. |
| Publicar versão aprovada | Promove revisão verificada no destino autorizado. | Não aprova edições novas. |

Confirmação de publicação deve mencionar tema, revisão, destino, quem será
afetado e referência do backup. Cancelar não tem efeitos. Receber erro deve
mostrar o que foi feito, o que não foi feito e como pedir suporte.

## Estados problemáticos que precisam de desenho e teste

Sessão expirada, arquivo inválido, permissão negada, salvar sem destino, callback
repetido, clique duplo, proposta alterada após aprovação, revisão antiga do
destino, fonte indisponível e perda de rede devem ter resposta definida.
Rascunho volátil é identificado como tal; sem confirmação de gravação não há
promessa de persistência. Nunca afirmar publicação global só porque uma prévia
mudou.

No início, `ipywidgets` poderá ser a interface visual após homologação; widgets
nativos de seleção/texto constituem alternativa de menor dependência. O arquivo
de tema completo e seu núcleo não dependerão da biblioteca de interface.
Um App posterior reutilizará o contrato; configuração global de framework não
será reescrita a cada ajuste individual.

## Rubrica visual e orçamentos propostos

A aprovação verifica hierarquia, legibilidade, contraste dos pares reais,
indicação além da cor, estabilidade semântica, texto não cortado, alinhamento,
leitura de legenda e adequação à reunião/saída final. Cada item recebe PASS,
FAIL ou PENDENTE e evidência, não uma nota média que esconda falha crítica.

Invariantes aprováveis já na especificação: zero mudança de dados/cálculos;
zero consulta e treino ao ajustar a prévia; zero publicação sem ação explícita.
Orçamento de tempo de atualização, memória e número de pontos será definido
com medição no ambiente V05. Meta inicial para discutir: prévia simples em até
2 segundos no percentil 95 de pelo menos 20 ajustes, com ambiente e dataset
fixados. **Não foi medida nem homologada**. Não usar essa hipótese como resultado
de benchmark. A V12 revisará acessibilidade e usabilidade em situação real.

[Guia de primeiro uso](GUIA_PRIMEIRO_USO.md) · [Testes](TESTES_E_ACEITE.md)
