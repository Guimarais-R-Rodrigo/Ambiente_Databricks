from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "ambiente_fonte/.assistant"


def rw(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f"substituicao nao unica em {path}: {old[:120]!r} -> {text.count(old)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

p = A / "hub_padroes/identidade_visual/README.md"
rw(p,"> **PADRÃO TRANSVERSAL DO HUB · V02 CANDIDATA.** Não é um novo tipo de objeto,\n> App ou configuração ativa de todos os notebooks. Nada muda na rotina legada.","> **PADRÃO TRANSVERSAL DO HUB · V02 INTEGRADA; CONSUMO OPT-IN ATÉ V04.** Não é um novo tipo de objeto,\n> App ou configuração ativa de todos os notebooks. Nada muda na rotina legada.")
rw(p,"leia o [objeto `visual.tema`](../../hub_snippets/visual/tema/README.md).","leia o [objeto `visual.tema`](../../hub_snippets/visual/tema/README.md).\n\n**Estado vigente no Git:** V02 integrou o núcleo de carga/validação/resolução; V03 acrescentou o adaptador Plotly opt-in; V04 estendeu a mesma arquitetura aos componentes HTML, estilos compartilhados e tabela pandas por rotas `_resolvido`. As APIs legadas permanecem o default. Integração Git não equivale a publicação no workspace, homologação visual/runtime, acessibilidade ou aprovação de uma identidade.")
rw(p,"continuam sendo as entradas gerais. A publicação e sua homologação são gates\nseparados; esta sprint não oferece comando para publicar um tema.","continuam sendo as entradas gerais. A publicação e sua homologação são gates\nseparados; V00–V04 integradas no Git não oferecem, por si só, comando ou autorização para publicar um tema.")

p = A / "hub_padroes/identidade_visual/GUIA_OPERACIONAL.md"
rw(p,"O que existe nesta V02 é um verificador com exemplo guiado, não um painel de cores.\nSeu notebook atual continua igual. A candidata precisa ser instalada e homologada\npelo mantenedor antes de ser usada no workspace de trabalho. Não publique arquivos\npor conta própria para experimentar uma cor.","O núcleo V02 está integrado no Git como verificador com exemplo guiado, não como painel de cores. V03 e V04 acrescentam consumidores opt-in, sem trocar o caminho legado por padrão.\nSeu notebook atual continua igual. Para usar o pacote no workspace de trabalho, a revisão integrada ainda precisa ser instalada/publicada pelo procedimento autorizado e homologada no destino. Não publique arquivos por conta própria para experimentar uma cor.")
rw(p,"Não confunda `export_theme` com salvar: ele devolve bytes em memória. Salvar em\numa pasta, compartilhar, aprovar e publicar são ações distintas. O laboratório\ne a gestão dessas ações serão entregues em sprints posteriores.","Não confunda `export_theme` com salvar: ele devolve bytes em memória. Salvar em\numa pasta, compartilhar, aprovar e publicar são ações distintas. Essas operações permanecem fora de V00–V04 integradas; uma etapa futura só pode ser considerada disponível quando estiver efetivamente integrada e homologada no escopo correspondente.")

p = A / "hub_padroes/README.md"
rw(p,"O [padrão de identidade visual](identidade_visual/README.md) define configurações\ncompletas e sua validação. É transversal, não um sétimo tipo de objeto. A V02\nnão instala painel nem altera automaticamente as cores dos consumidores.","O [padrão de identidade visual](identidade_visual/README.md) define configurações\ncompletas e sua validação. É transversal, não um sétimo tipo de objeto. V02 integra o núcleo; V03 e V04 acrescentam consumidores opt-in. Não há painel, tema global, migração automática de notebooks ou publicação implícita.")

p = A / "hub_snippets/README.md"
rw(p,"**Novo núcleo candidato:** [`visual.tema`](visual/tema/README.md) confere configurações\ncompletas e isoladas, sem aplicar cores ou alterar consumidores legados.","**Núcleo de temas integrado no Git:** [`visual.tema`](visual/tema/README.md) confere configurações completas e isoladas. V03 conecta Plotly por opt-in e V04 estende a rota explícita a HTML/estilos/tabela pandas; consumidores legados permanecem o default e nenhuma dessas integrações publica ou homologa aparência no Databricks.")

p = A / "MANUAL_TECNICO.md"
rw(p,"## Sistema de Temas — V04 (candidata)\n\nA V04 estende o tema validado aos componentes HTML e à tabela pandas sem mudar o\ncaminho atual por padrão.","## Sistema de Temas — V04 integrada no Git\n\nA V04 foi aceita e integrada no Git. Isso confirma a disponibilidade das rotas opt-in no produto versionado; não confirma publicação no workspace, homologação visual/runtime, acessibilidade ou aprovação de uma identidade.\n\nA V04 estende o tema validado aos componentes HTML e à tabela pandas sem mudar o\ncaminho atual por padrão.")
shutil.copyfile(p, ROOT / "MANUAL_TECNICO.md")
print("D05 produto: documentação viva do Sistema de Temas reconciliada")
