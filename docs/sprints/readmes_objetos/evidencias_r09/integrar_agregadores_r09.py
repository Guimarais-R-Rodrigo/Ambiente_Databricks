"""Integração transversal mínima da R09 após a recuperação de preservação."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
NOTES={
    'README.md':'\n> **READMEs R09 — candidata:** cinco guias de avaliação, drift e MLOps; cobertura alvo 60/75, sujeita ao freeze e aceite.\n',
    'docs/sprints/README.md':'\n### READMEs R09\nLeva de avaliação, drift e MLOps: cinco objetos; cobertura candidata 60/75, sujeita ao freeze e aceite.\n',
}
def main():
    # Manual Técnico, CLAUDE.md e PLANO_HUB.md ficam deliberadamente intactos:
    # já cobrem métricas/MLflow e não precisam de checkpoint redundante desta leva.
    for rel,note in NOTES.items():
        p=ROOT/rel; text=p.read_text(encoding='utf-8')
        if note.strip() not in text:
            p.write_text(text.rstrip()+note,encoding='utf-8')
if __name__=='__main__': main()
