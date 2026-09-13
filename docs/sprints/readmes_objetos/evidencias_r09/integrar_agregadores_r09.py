"""Integração mínima dos agregadores R09; sem reescrever seções históricas."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[4]
ASSISTANT=ROOT/'ambiente_fonte/.assistant'
MANUAL_MARK='**Manutenção de uma única redação:**'
MANUAL_NOTE='**Checkpoint R09:** os guias locais de `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor` documentam avaliação, mudança de distribuição e monitoramento. `n` em `curves_plotly` não subamostra; `ks_pct` usa escala 0–100; drift não prova queda de performance; `should_retrain()` não autoriza retreino; observações de runtime MLflow são datadas.\n\n'
NOTES={
'README.md':'\n> **READMEs R09 — candidata:** cinco guias de avaliação, drift e MLOps; cobertura alvo 60/75, sujeita ao freeze e aceite.\n',
'CLAUDE.md':'\n<!-- R09 -->\nCheckpoint documental R09: cinco guias de avaliação/drift/MLOps; 60/75 na candidata, sujeito ao validador e aceite.\n',
'PLANO_HUB.md':'\n### Checkpoint READMEs R09\nCinco objetos de avaliação, drift e MLOps entram na candidata documental. Meta 60/75 e 15 pendências; sem mudança funcional.\n',
'docs/sprints/README.md':'\n### READMEs R09\nLeva de avaliação, drift e MLOps: cinco objetos; cobertura candidata 60/75, sujeita ao freeze e aceite.\n'}
CHANGE='- R09: cinco READMEs de avaliação, drift e MLOps; notebooks recebem apenas backlinks/erratas Markdown explicitamente autorizadas; meta 60/75.'
def main():
 manual=ASSISTANT/'MANUAL_TECNICO.md'; text=manual.read_text(encoding='utf-8')
 if MANUAL_NOTE not in text:
  assert text.count(MANUAL_MARK)==1
  manual.write_text(text.replace(MANUAL_MARK,MANUAL_NOTE+MANUAL_MARK),encoding='utf-8')
 shutil.copyfile(manual,ROOT/'MANUAL_TECNICO.md')
 for rel,note in NOTES.items():
  p=ROOT/rel; text=p.read_text(encoding='utf-8')
  if note.strip() not in text: p.write_text(text.rstrip()+note,encoding='utf-8')
 p=ROOT/'CHANGELOG.md'; text=p.read_text(encoding='utf-8')
 if CHANGE not in text: p.write_text(text.rstrip()+'\n'+CHANGE+'\n',encoding='utf-8')
if __name__=='__main__': main()
