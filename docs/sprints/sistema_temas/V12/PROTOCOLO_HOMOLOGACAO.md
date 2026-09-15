# V12 — protocolo de homologação controlada

Este procedimento prepara a execução humana e de ambiente. **Ele não concede autorização.** Pare antes de qualquer ação que altere Databricks até existir autorização explícita para aquela operação.

## 1. Preparar a sessão

Registre o SHA Git candidato e escolha apenas dados sintéticos. Defina uma classe sanitizada de ambiente (`databricks_free_lab`, `databricks_nonprod_authorized` ou `databricks_work_authorized_test`) sem versionar hostname, username, catálogo, schema, grupo ou path real.

Para toda mutação, registre antes:

- operação exata;
- ambiente;
- executor/papel, sem identidade pessoal no Git;
- risco;
- rollback;
- autorização explícita;
- evidência que será coletada.

Sem esses itens, estado `BLOQUEADO_AUTORIZACAO`.

## 2. Jornada documental

Entregue somente README/guia aplicável e não explique a próxima ação. Execute `DOC-02` e `DOC-03`. Registre tempo real e cada ajuda. A meta de 60 s é candidata e deve ser reportada como medição, não usada como SLA inventado.

## 3. Visual Lab V05

Pré-requisito: notebook/pacote já disponível em workspace de teste autorizado e destino de rascunhos seguro.

Observe, sem atalhos:

1. abrir launcher;
2. escolher base;
3. alterar e aplicar;
4. comparar com dados sintéticos invariantes;
5. desfazer/restaurar;
6. salvar sessão;
7. recarregar e reabrir;
8. conferir base, proposta, histórico e revisão;
9. exercitar teclado e zoom;
10. registrar browser/runtime e quaisquer intervenções.

Se for necessário publicar/copiar o Hub para criar o ambiente, essa publicação é uma operação separada e exige autorização própria.

## 4. Databricks App V10

Se não houver App de teste já implantado, **pare**: deploy é mutação real não autorizada por este protocolo.

Com App autorizado:

1. confirmar ambiente correto e `CAN USE` apropriado;
2. observar identidade encaminhada;
3. executar escolher → ajustar → comparar → salvar → reabrir;
4. com segunda identidade autorizada, verificar isolamento;
5. confirmar ausência de aprovar/rejeitar/publicar/promover;
6. revisar teclado, zoom, leitura e mensagens de erro;
7. registrar evidência sanitizada.

Não alterar ACL, grupos, Volume ou recursos para “fazer passar”.

## 5. AI/BI dashboard theme V11

### 5.1 Export — observação

Em dashboard **draft** de teste com dados sintéticos, use `Settings > Theme > Export theme`. Preserve os bytes originais e calcule SHA-256. O Hub não assume schema público.

### 5.2 Binding — Git/local

Um mantenedor revisa o export e aponta JSON Pointers **já existentes** apenas para:

- `widget.background`;
- `visualization.categorical_palette`;
- `widget.corner_radius`.

O binding precisa fixar o SHA-256 exato. Divergência de hash/path/tipo/colisão, tentativa de automatizar `approximated` ou `unsupported`, ou fixture sintético apresentado como arquivo nativo devem falhar fechado.

### 5.3 Import — mutação

Antes de `Import theme`, **pare e confirme autorização**. O dashboard precisa continuar draft; registre fingerprint/assinatura semântica antes.

Depois de import autorizado:

1. conferir aceitação/rejeição pelo produto;
2. verificar light/dark;
3. conferir datasets, queries, filtros, campos, agregações, unidades, ordenações e categorias;
4. recalcular a assinatura semântica;
5. registrar que publicação não ocorreu.

Se o arquivo for inválido, a documentação oficial afirma que o dashboard permanece inalterado; registre o erro, não afrouxe guardas.

## 6. Workspace theme

Essa jornada exige administrador e altera configuração do workspace. Use apenas ambiente de teste dedicado.

Antes da primeira alteração, obtenha autorização específica e rollback. Testar herança de dashboard novo e snapshot/reaplicação de dashboard existente não autoriza assumir propagação viva.

A documentação atual orienta `Publish` ao aplicar o workspace theme a um dashboard existente. Se a observação de snapshot exigir publicação, **pare novamente** e obtenha autorização própria de publicação. Sem ela, registre o subteste como bloqueado; não publique para fechar uma tabela.

## 7. Acessibilidade

No render real, registre:

- contraste medido sem arredondar para passar;
- teclado/foco;
- zoom e legibilidade;
- rótulos/mensagens/saída segura;
- ausência de dependência exclusiva de cor para estado;
- problemas encontrados.

`A11-01` mantém 4,5:1 para texto comum e 3:1 para texto grande somente quando a classificação se aplica.

## 8. UAT-01

Com iniciante autorizado, sem ajuda verbal inicial, pedir que execute a jornada prevista. Toda intervenção vira `help_event`. O oráculo canônico é: escolher, ajustar, comparar, desfazer e salvar sem alteração compartilhada acidental.

Não versione nome, e-mail ou username. Use alias `P-...`.

## 9. Registro e validação

Um registro sanitizado pode ser conferido por:

```bash
python -B tools/temas_v12_homologacao.py --validate <evidencia.json>
```

O validador checa coerência do registro; ele **não autentica** a pessoa nem o workspace e não converte documentação em fato observado.

## 10. Rollback/saída segura

Se houver qualquer divergência de ambiente, autorização, hash, semântica, identidade, permissão ou evidência, interrompa a jornada. Restaure somente pelo procedimento previamente autorizado da superfície; não force publicação, não ajuste hashes e não apague histórico para obter `PASS`.
