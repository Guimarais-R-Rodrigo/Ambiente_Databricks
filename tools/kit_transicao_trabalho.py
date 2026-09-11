"""Monta kit offline para a UI corporativa, sem publicar ou usar credenciais.

Mantém o payload do Hub separado do material de aceite. Usa o bundle mínimo,
fixa identidade por commit+SHA256 e embute o núcleo de testes no notebook IPYNB.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def notebook(commit: str, manifest_sha: str, core: str) -> bytes:
    """Notebook sem outputs, sem configuração corporativa e sem instalação automática."""
    cells = []
    def md(text):
        cells.append({"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)})
    def code(text, hidden=False):
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {"jupyter": {"source_hidden": hidden}},
                      "outputs": [], "source": text.splitlines(True)})
    short = commit[:12]
    md("# Aceite do Hub no Databricks do trabalho\n\n"
       "Execute **célula por célula**, em sessão nova. Este notebook não instala o Hub, não instala bibliotecas, "
       "não apaga arquivos e não grava tabelas. Os testes Spark usam dados sintéticos e views temporárias próprias. "
       "MLflow e acesso a uma tabela corporativa exigem habilitação explícita.\n\n"
       f"**Commit do kit:** `{commit}`. Abra `GUIA_TRANSICAO.md` e `CHECKLIST.md` nesta pasta. "
       "Preencher configurações no destino não autoriza enviar este notebook preenchido ao GitHub.\n\n"
       "**Estados:** PASS = teste executado e conferido; FAIL = reprovação; BLOQUEADO = pré-requisito falhou; "
       "NAO_TESTADO/PENDENTE = sem evidência, nunca aprovação. `warn` ou `fail` devolvido pelo helper pode ser "
       "o resultado correto de um teste negativo.\n\n"
       "A leitura de arquivos não consulta tabelas; a sessão/compute escolhida pode ainda gerar custos da plataforma.")
    md("## 1. Configuração local\n\nPreencha `USER_HOME` copiando o caminho da sua pasta no workspace e acrescentando "
       "`/Workspace` quando necessário. Não use o usuário do laboratório. Mantenha `PHASE='staging'` para a pasta "
       "de conferência e use `final` somente após a promoção manual. Reinicie Python ao mudar de fase; não reutilize "
       "módulos importados da pasta anterior. Os controles extras começam desligados.")
    code(f'''from pathlib import Path
USER_HOME = Path("/Workspace/Users/<username-trabalho>")
PHASE = "staging"  # depois da promoção: "final", em sessão Python nova
STAGING_ROOT = USER_HOME / "hub_staging_{short}"
KIT_DIR = USER_HOME / "aceite_hub_{short}"  # pasta extraída do ZIP 02
PRODUCT_ROOT = STAGING_ROOT if PHASE == "staging" else USER_HOME
EXECUTAR_SPARK = False  # True somente após conferir arquivos, compute e escopo sintético
WORKSPACE_HOST = ""  # URL HTTPS do workspace conferida no navegador; só necessária para API/MLflow
CONSULTAR_TIPOS_VIA_API = False  # metadados de notebooks; não altera objetos/permissões
TESTAR_MLFLOW = False  # gera e exclui logicamente UM run em experimento pessoal existente
EXPERIMENTO_TEMPORARIO = ""  # preencher só no destino, por /Users/...
TESTAR_LEITURA_UC = False  # uma consulta limitada em UMA tabela explicitamente autorizada
TABELA_AUTORIZADA = ""  # catalog.schema.table; nunca versionar o valor corporativo
EXPECTED_COMMIT = "{commit}"
EXPECTED_MANIFEST_SHA256 = "{manifest_sha}"
''')
    md("## 2. Carregar o mecanismo de testes\n\nO código abaixo veio do kit e só define funções/classes; "
       "não lê o Hub nem inicia Spark. Não precisa importar `tools/` ou baixar qualquer arquivo da internet.")
    code(core, hidden=True)
    code('''aceite = AcceptanceSession(PRODUCT_ROOT, KIT_DIR / "MANIFEST.json",
                           EXPECTED_MANIFEST_SHA256, EXPECTED_COMMIT, PHASE)
print("Sessão de aceite criada. Dados corporativos e credenciais não são exibidos.")
''')
    md("## 3. Identidade e integridade dos arquivos\n\nEsperado: manifesto e todos os FILEs iguais ao pacote, "
       "incluindo instruções, manual, módulos e PNGs. Notebook importado pode mudar representação: "
       "o hash dos NOTEBOOKs não é aprovado por este teste. Confira tipo e abertura pela UI; API opcional abaixo "
       "confere todos os tipos, mas não atesta igualdade das células. Se um FILE divergir, reimporte do pacote: "
       "não edite o manifesto para fazê-lo passar.")
    code('''aceite.run("manifesto", aceite.check_manifest)
aceite.run("arquivos", aceite.check_files, ("manifesto",))
''')
    md("## 4. Tipos de notebook e dependências\n\nA API é opcional; sem autorização ou SDK, mantenha-a desligada "
       "e faça a conferência de tipo pela interface. A lista de versões é inventário: pacote instalado não significa "
       "que todos os seus recursos funcionem. Não execute `%pip install` indiscriminadamente.")
    code('''if CONSULTAR_TIPOS_VIA_API:
    aceite.run("tipos_api", lambda: aceite.check_notebook_types(WORKSPACE_HOST), ("arquivos",))
else:
    aceite.skip("tipos_api", "Conferir tipos e abrir exemplos pela UI; API opcional não executada.")
print(json.dumps(aceite.dependency_inventory(), indent=2))
''')
    md("## 5. Imports e contrato Python\n\nEsperado: seis módulos da instalação conferida; formatação brasileira "
       "correta. `ModuleNotFoundError` é problema de pacote/caminho, não autorização para instalar tudo. "
       "Se já havia módulos Hub em cache, reinicie Python e recomece. O teste não executa os notebooks de exemplo.")
    code('''aceite.run("imports", aceite.check_imports, ("arquivos",))
aceite.run("python", aceite.check_python, ("imports",))
''')
    md("## 6. Compute e ação Spark mínima\n\nHabilite `EXECUTAR_SPARK` no começo e recomece em sessão nova. "
       "Use o ambiente aprovado pela organização. Em serverless não instale PySpark nem use RDD, internos JVM, "
       "cache/persist. Este caso retorna somente N=20 e soma=190.")
    code('''if EXECUTAR_SPARK:
    aceite.run("spark", lambda: aceite.check_spark(globals().get("spark")), ("imports",))
else:
    aceite.skip("spark", "Ação sintética ainda não autorizada na configuração.")
''')
    cases = [("7. Qualidade: aviso esperado", "dq_aviso", "aceite.check_dq(spark)",
              "Esperado: teste PASS, pois o helper devolve warn, score95 e 5% de nulos. Não usa o relógio."),
             ("8. Qualidade: defeito injetado", "dq_falha", "aceite.check_dq(spark, duplicate=True)",
              "Esperado: teste PASS, pois o helper detecta uma duplicidade e devolve fail. Isso testa a detecção do defeito."),
             ("9. RFV sem evento futuro", "rfv", "aceite.check_rfv(spark)",
              "Esperado: valor30, frequência2, recência5. O evento futuro de valor999 deve ficar fora."),
             ("10. Point-in-time e preservação de linhas", "pit", "aceite.check_pit(spark)",
              "Esperado: duas linhas preservadas com valor10. Valor99 não estava disponível na data da decisão."),
             ("11. PSI de identidade", "psi", "aceite.check_psi(spark)",
              "Esperado: PSI zero. O teste não afirma que exista um threshold universal de estabilidade.")]
    for title, key, expr, explain in cases:
        md("## " + title + "\n\n" + explain)
        code(f'aceite.run("{key}", lambda: {expr}, ("spark",))\n')
    md("## 12. Visualização\n\nO objeto Plotly deve ser criado e os dois valores devem ser 10 e 20. "
       "Execute a segunda célula para conferir a renderização; abra também os READMEs e as imagens no próprio "
       "workspace. Hash correto não garante boa aparência. Não foram alterados os widgets/layouts escolhidos.")
    code('aceite.run("visual_objeto", aceite.check_visual_object, ("python",))\n')
    code('''if aceite.results.get("visual_objeto", {}).get("status") == "PASS":
    display(aceite.figure)
''')
    md("## 13. Extensões opcionais: MLflow e leitura governada\n\n"
       "**MLflow:** só habilite para um experimento pessoal temporário JÁ EXISTENTE, autorizado para criação e "
       "exclusão lógica de run. Faz round-trip de parâmetro/métrica; não testa log de modelo, registro Unity Catalog "
       "ou serving. Não encerra run de outro fluxo. Se a limpeza falhar, consulte `aceite.mlflow_run_id` apenas no "
       "destino e remova somente o run criado por este teste. Não exclua o experimento.\n\n"
       "**UC:** opcional `SELECT 1 ... LIMIT 1` em uma tabela especificada. Pode consumir compute/leitura e a política "
       "precisa permitir a consulta. Não lista catálogos nem mostra valores. Não comprova permissões de escrita.\n\n"
       "Recusa inesperada é FAIL da extensão, nunca um bloqueio do Free interpretado como PASS no trabalho.")
    code('''if TESTAR_MLFLOW:
    aceite.run("mlflow", lambda: aceite.check_mlflow(EXPERIMENTO_TEMPORARIO, WORKSPACE_HOST), ("arquivos", "python"))
else:
    aceite.skip("mlflow", "Tracking/modelos não homologados por este aceite básico.")
if TESTAR_LEITURA_UC:
    aceite.run("unity_catalog", lambda: aceite.check_uc(spark, TABELA_AUTORIZADA), ("spark",))
else:
    aceite.skip("unity_catalog", "Leitura corporativa não autorizada; somente dados sintéticos foram usados.")
''')
    md("## 14. Aceite humano — não é automatizável por este notebook\n\n"
       "Siga `TESTES_GENIE.md`. Confirme backup, tipos de objetos, arquivo aberto em Settings, imagens, "
       "roteamento EDA sem @, seleção explícita baseline/criar-objeto, uso seletivo de contexto e proveniência. "
       "Resposta em português ou o agente afirmar que carregou algo não é evidência isolada suficiente. "
       "Preencha somente após observar: CONFIRMADO / PENDENTE / REPROVADO. A declaração fica separada dos testes automáticos.")
    code('CONFIRMACOES = {\n' + ''.join(f'    "{x}": "PENDENTE",\n' for x in
         ("backup", "tipos_ui", "instrucoes_ui", "imagens_ui", "genie_eda", "genie_baseline", "genie_criar_objeto", "genie_contexto", "proveniencia")) + '}\n')
    md("## 15. Resultado consolidado e registro sanitizado\n\n"
       "PRONTO_PARA_PILOTO_BASICO não significa homologação dos 58 helpers, modelos em produção ou todas as "
       "permissões. NAO_TESTADO não é PASS. Staging nunca é instalação ativa.\n\n"
       "O JSON abaixo omite caminhos, usuários, host, nomes de tabela/experimento e exceções brutas. "
       "Ainda revise antes de compartilhar, seguindo a política corporativa. Não exporte o notebook preenchido "
       "com configurações pessoais nem backups para Git/serviços pessoais. A célula não grava arquivos.")
    code('print(json.dumps(aceite.receipt(CONFIRMACOES), ensure_ascii=False, indent=2))\n')
    return json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {
        "display_name": "Python 3", "language": "python", "name": "python3"}},
        "cells": [{**c, "id": f"c{i:03d}"} for i, c in enumerate(cells)]}, ensure_ascii=False, indent=2).encode()


def build_kit(output: Path) -> dict:
    """Só produz pacote de checkout limpo; não confunde origem com homologação."""
    git = lambda *a: subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()
    commit = git("rev-parse", "HEAD")
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("Checkout deve estar limpo para gerar um kit distribuível.")
    output = output.resolve()
    if output.exists():
        raise ValueError("Destino já existe; use diretório novo.")
    if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT / ".artifacts"):
        raise ValueError("Dentro do repositório, use apenas .artifacts/ para a saída.")
    output.mkdir(parents=True)
    product_zip = output / f"01_IMPORTAR_HUB_{commit[:12]}.zip"
    subprocess.run([sys.executable, str(ROOT / "tools/bundle_implantacao.py"), "--output", str(product_zip)],
                   cwd=ROOT, check=True)
    with zipfile.ZipFile(product_zip) as z:
        manifest_raw = z.read("MANIFEST.json")
    manifest = json.loads(manifest_raw)
    digest = hashlib.sha256(manifest_raw).hexdigest()
    nb = notebook(commit, digest, (ROOT / "tools/aceite_trabalho.py").read_text(encoding="utf-8"))
    root_dir = f"aceite_hub_{commit[:12]}"
    guide = (ROOT / "docs/playbooks/replicacao-trabalho.md").read_text(encoding="utf-8")
    guide = guide.replace("(checklist-replicacao.md)", "(CHECKLIST.md)").replace("(testes-genie-trabalho.md)", "(TESTES_GENIE.md)")
    checklist = (ROOT / "docs/playbooks/checklist-replicacao.md").read_text(encoding="utf-8").replace("(replicacao-trabalho.md)", "(GUIA_TRANSICAO.md)")
    human = (ROOT / "docs/playbooks/testes-genie-trabalho.md").read_text(encoding="utf-8").replace("(replicacao-trabalho.md)", "(GUIA_TRANSICAO.md)")
    test_zip = output / f"02_IMPORTAR_ACEITE_{commit[:12]}.zip"
    with zipfile.ZipFile(test_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in {"01_ACEITE_TECNICO.ipynb": nb, "MANIFEST.json": manifest_raw,
                           "GUIA_TRANSICAO.md": guide.encode(), "CHECKLIST.md": checklist.encode(),
                           "TESTES_GENIE.md": human.encode()}.items():
            z.writestr(root_dir + "/" + name, data)
    (output / "GUIA_TRANSICAO.md").write_text(guide, encoding="utf-8")
    (output / "CHECKLIST.md").write_text(checklist, encoding="utf-8")
    (output / "TESTES_GENIE.md").write_text(human, encoding="utf-8")
    (output / "01_ACEITE_TECNICO.ipynb").write_bytes(nb)
    (output / "COMECE_AQUI.md").write_text(
        f"# Kit de transição para o trabalho\n\nCommit: `{commit}`. Não é homologação do destino.\n\n"
        f"Leia [o guia](GUIA_TRANSICAO.md). Importe `{product_zip.name}` numa pasta pessoal vazia "
        f"`hub_staging_{commit[:12]}`, nunca sobre o ambiente ativo. Importe `{test_zip.name}` na raiz "
        f"do seu usuário: ele cria `{root_dir}/`. Abra o notebook dentro dessa pasta e configure USER_HOME.\n\n"
        "O ZIP externo que reúne este kit NÃO é importável como produto. Extraia-o no computador autorizado "
        "e importe os dois ZIPs internos nos locais indicados. Não descompacte/recompacte perdendo arquivos ocultos.\n\n"
        "O notebook avança de identidade para arquivos, imports, Spark e contratos. "
        "MLflow e tabela corporativa começam desligados. Depois, promova manualmente só o escopo do Hub, "
        "preservando MCP e skills alheias. Rode de novo na instalação final, em sessão nova, "
        "e execute os testes humanos da Genie e das imagens.\n\n"
        "SHA256 detecta alteração acidental quando comparado a uma referência confiável; não é assinatura digital.\n",
        encoding="utf-8")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.is_file()}
    (output / "SHA256SUMS.txt").write_text("".join(f"{sha}  {name}\n" for name, sha in hashes.items()), encoding="utf-8")
    return {"commit": commit, "product_files": len(manifest["files"]), "manifest_sha256": digest, "files": hashes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build_kit(args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print("FAIL:", str(exc)); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
