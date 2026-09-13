"""Completa a explicação da seção 9 de três READMEs R09 sem mudar APIs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'ambiente_fonte/.assistant/hub_snippets/ml'
EDITS={
'curves_plotly':('fig.show()\n```\n\n## 10.','fig.show()\n```\n\nA chamada acima usa todos os elementos de `y_true` e `y_prob`; `n`, quando informado, só muda o texto do rodapé. Em base grande, faça a redução de volume antes de chamar o helper.\n\n## 10.'),
'mlflow_run':('    run.modelo(modelo, exemplo_entrada=X_val[:5])\n```\n\n## 10.','    run.modelo(modelo, exemplo_entrada=X_val[:5])\n```\n\nO bloco produz efeitos no backend MLflow configurado para a sessão. Antes de executar, confirme o experimento/tracking autorizado e use o flavor adequado ao tipo real do modelo; o atalho `run.modelo()` é sklearn.\n\n## 10.'),
'performance_monitor':('print(monitor.get_current_status())\n```\n\n## 10.','print(monitor.get_current_status())\n```\n\nO exemplo cria apenas estado em memória. Para uma rotina operacional, persista métricas e períodos fora da classe e interprete qualquer trigger como pedido de investigação, não como autorização de retreino.\n\n## 10.')}
def main():
 for obj,(old,new) in EDITS.items():
  p=BASE/obj/'README.md'; t=p.read_text(encoding='utf-8'); assert t.count(old)==1,(obj,t.count(old)); p.write_text(t.replace(old,new),encoding='utf-8')
if __name__=='__main__': main()
