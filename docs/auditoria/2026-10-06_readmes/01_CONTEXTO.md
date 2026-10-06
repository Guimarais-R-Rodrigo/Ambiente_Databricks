# Readequação documental: contexto e escopo

Data de início: 06/10/2026. Autoria: Codex. Base integral e limpa: `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`, árvore `3f63fe2b23ac1b658fc11d061cc7f76f93c12d41`; 2.382 arquivos versionados e histórico completo.

A implementação segue o [plano aprovado](https://docs.google.com/document/d/1MEXcts9r006ShbxRoHPIKfxehX0nw_nWBNvZVxQ1TCs/edit), seus 497 registros de origem, 1.135 ações e mapa de 723 caminhos. O usuário autorizou implementar, commitar e fazer push, incluindo a alternativa de execução por GitHub após indisponibilidade da execução local anterior.

## Decisões de execução

- D1: separar uso de manutenção e mover conteúdo documental com preservação/referências. Pontes permanecem onde um contrato de pacote exige o caminho original.
- D2: projeção operacional de TOKENS separada da saída histórica; cópias do Manual sincronizadas; hashes derivados de arquivos documentais atualizados mecanicamente. Nenhum schema, default ou allowlist é alterado.
- D3: inconsistência textual de `known_debt` de Micromodelos registrada; policy e níveis permanecem byte-idênticos. A presença do adapter metadata-only não promove a skill.
- D4: algoritmos, células executáveis, magics, assinaturas e comportamento não mudam. Limitações existentes de exemplos são documentadas e discriminadas no relatório, não corrigidas por inferência.
- D5: nenhuma publicação Databricks, job remoto, treino remoto, tracking real, ACL, homologação corporativa ou promoção foi executada. Commit/push Git não equivalem a implantação.

## Organização e revisão

Lotes isolados por família, sempre sobre a mesma base. Fontes foram editadas antes de derivados. A revisão independente conferiu diffs completos, APIs, riscos, contas pequenas e preservação de evidência; a integração final confere pacote completo, manifests e matriz.

Pilotos: navegação das skills de manutenção e estado L3/audit por superfície de Criar Objeto. A revisão corrigiu o nome preciso do campo `scope_mode` e vinculou a qualificação B0 ao freeze efetivamente testado.

## Baseline local

Linux, Python 3.12.14; dependências de manutenção Python e Node/pnpm fixadas pelos arquivos do repositório. Validador inicial: zero falhas e avisos. Renderer sem escrita: PASS. CI local: 12/12 etapas PASS, com 11 casos temáticos e 7 de transição pulados conforme dependências opcionais. Esses skips não são homologação de runtime.

## Ajuste documental de regressão

Cinco verificações antigas em `test_temas_v08.py` exigiam rótulos de sprint na documentação de uso. O requisito do plano substitui narrativa de construção por capacidade, aplicação explícita, consumidor, fonte única e limites. Apenas essas assertivas positivas foram atualizadas:

| Verificação anterior | Obrigação conferida agora |
|---|---|
| Entrada contém V07 | ResolvedTheme, Visual Lab, opt-in, SHAP/Kaplan e rota de identidade |
| Padrão de identidade contém V07 | schema, representação validada, guia e ausência de aplicação/aprovação automáticas |
| Primeiro uso contém V07 | Visual Lab, rota `_resolvido`, opt-in, dependências e ausência de publicação |
| Manual contém título V00–V07 e V08 | capacidades atuais, schema, consumidores, exceções e invariância analítica |
| Índice de padrões contém V07 | fonte central, Visual Lab e nenhuma ativação/publicação implícita |

As negativas contra estados obsoletos permaneceram. Mutantes que removem cada capacidade/limite exigido reprovam. O revisor independente executou oito testes focais, todos PASS. Testes funcionais, snapshot V01 e saída histórica de `dictionary(schema)` permanecem preservados.
