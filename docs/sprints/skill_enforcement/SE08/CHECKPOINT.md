# SE08 — checkpoint pós-certificação local

**Estado atual:** candidata técnica R5 certificada localmente no Windows/NTFS e pronta para revisão de integração. Isso não equivale a certificação global da SE08 nem autoriza promoção ao trabalho.

## Identidade técnica certificada

A campanha Windows R5 testou exatamente:

- SHA: `ee1cf04b031497bb5b7ddfa47ce28b8015d15668`;
- tree: `d29fb8221c08ab3ea1fb0198004d4720d4785f92`;
- Windows 11 build 26200;
- Python 3.12.14;
- filesystem NTFS;
- worktree inicial/final limpa.

Resultado local:

- windows corrective: PASS 10/10;
- storage standalone: PASS 9/9;
- certifier standalone: exit 0, 51 métodos, 1 skip de escopo;
- CI local: PASS 10/10 etapas;
- FULL SE08 local: PASS 21/21 gates;
- `release_clean_certification=true`;
- `DERIVED_STALE=false`;
- WinError32 nativo: não reproduzido nessa campanha.

Bundle externo:

- `SEF_SE08_R5_WINDOWS_ee1cf04b_20260922.zip`;
- SHA-256: `215176bd9804ab38b2d55678778f1d0defaa334c5040aa13ce5810a43d105d03`;
- manifesto interno: 1628/1628 hashes válidos;
- ZIP CRC: íntegro.

A ausência de WinError32 na R5 não reclassifica as ocorrências históricas das R2–R4 como corrigidas causalmente.

## Estado das camadas

### Concluído

- implementação repo-side SE08;
- materialização derivada;
- snapshot README reconciliado;
- regressões policy I/O e operacionais;
- storage cleanup integrado ao perfil FULL;
- instrumentação Windows fail-closed;
- CI repo-side/GitHub Actions;
- campanha Windows/NTFS R5;
- FULL SE08 local no SHA técnico acima.

### Ainda pendente

- atualização documental final desta fase, em SHA posterior e somente documental;
- recertificação mínima do SHA documental final;
- revisão/integração da PR final;
- publicação/verificação Free por conteúdo, se exigida pelo Plano Mestre;
- homologação Genie Code;
- decisão humana explícita sobre qualquer promoção ao workspace corporativo.

## Dívidas históricas preservadas

- SE06: 24/25; `S06-A1-R4=NOT_RUN`; `SE06_DOD=INCOMPLETE`;
- SE07: encerrada com residual aceito; `SE07_FULLY_CERTIFIED=false`;
- storage cleanup histórico 8/9 e WinError32 históricos permanecem evidência passada;
- `hub-ml-criar-objeto` permanece L2 global;
- `PROMOCAO_TRABALHO=BLOQUEADA`.

## Próximo gate

Como este documento atualiza o SHA após a certificação técnica R5, a candidata documental final deve receber uma recertificação Windows mínima no SHA exato: identidade, CI local e FULL SE08. Nenhuma alteração de produto está autorizada nessa etapa.

Depois disso, a frente repo-side pode seguir para revisão final de integração. Free/Genie e promoção são gates separados.
