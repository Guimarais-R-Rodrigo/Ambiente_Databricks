# Registro de padrões oficiais

[registry.json](registry.json) vincula cada claim à URL, revisão, produto/superfície,
paráfrase, testes e snapshot curto. Os snapshots são resumos de pesquisa; seu hash
não é apresentado como hash da página original. A pesquisa do plano aprovado foi
consultada em 06/10/2026 e preservada com essa data, sem renovação automática.

DOCUMENTED significa documentação consultada. OBSERVED exige ensaio real na versão,
modo e ambiente identificados. SUPPORTED exige a interseção dos requisitos e provas
obrigatórias. Nenhum perfil desta entrega é declarado SUPPORTED.

## Atualizar sem prometer suporte

1. Reconsultar a fonte oficial quando mudar versão, provider, superfície, modo,
   descoberta, frontmatter ou configuração que afete o carregamento; também antes
   de promover uma declaração de suporte.
2. Comparar semanticamente, classificar a mudança e registrar owner, impacto e testes.
3. Criar snapshot datado, preservar o anterior e atualizar bindings. Editar só a data
   não é revisão e falha na conferência de vinculação.
4. Rodar check, negativos afetados e sessões nativas novas. Revisão independente
   deve conferir a fonte e a evidência antes de mudar o estado.
5. Com mais de 30 dias o claim fica STALE para nova declaração de suporte.
   --check normal avisa; --check --release reprova. Trabalho de produto não
   relacionado não é bloqueado por idade. Mudança material conhecida invalida antes.

O gate é offline e não percebe sozinho se um fornecedor mudou. Não instala
clientes, não chama API/modelo e não cria monitor ou atualizador externo.

## Promoção de estado nesta campanha

O formato atual aceita somente DOCUMENTED. OBSERVED e SUPPORTED são reservados
para futura evolução revisada que valide SHA, status e superfície de cada prova.
Uma string não vazia em observed_evidence não autoriza promoção e falha fechada.
