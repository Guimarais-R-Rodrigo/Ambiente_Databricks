from pathlib import Path
ROOT=Path(__file__).resolve().parent
out=Path('/tmp/d05-validator.txt').read_text(encoding='utf-8').strip()
if 'APROVADO: 0 falha(s), 0 aviso(s)' not in out: raise SystemExit('validator D05 nao aprovado')
p=ROOT/'README.md'; t=p.read_text(encoding='utf-8')
start=t.find('### Estado verificável do gate local'); fence=t.find('```text\n',start); end=t.find('\n```',fence)
if min(start,fence,end)<0: raise SystemExit('snapshot raiz nao encontrado')
p.write_text(t[:fence+8]+out+t[end:],encoding='utf-8')
