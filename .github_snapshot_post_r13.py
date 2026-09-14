from pathlib import Path
out=Path('/tmp/postr13-validator.txt').read_text(encoding='utf-8').strip()
assert 'APROVADO: 0 falha(s), 0 aviso(s)' in out
p=Path('README.md'); t=p.read_text(encoding='utf-8')
a=t.find('### Estado verificável do gate local'); b=t.find('```text\n',a); c=t.find('\n```',b)
assert min(a,b,c)>=0
p.write_text(t[:b+8]+out+t[c:],encoding='utf-8')
