from __future__ import annotations
import ast, fnmatch, json
from pathlib import Path

def methods_in_file(path:Path)->list[str]:
    try: tree=ast.parse(path.read_text(encoding='utf-8'))
    except (OSError,UnicodeDecodeError,SyntaxError): return []
    out=[]
    for node in tree.body:
        if isinstance(node,ast.ClassDef):
            for f in node.body:
                if isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef)) and f.name.startswith('test_'): out.append(f"{path.as_posix()}::{node.name}.{f.name}")
        elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name.startswith('test_'): out.append(f"{path.as_posix()}::{node.name}")
    return sorted(out)

def expand_patterns(repo:Path,patterns:list[str])->dict[str,list[str]]:
    files=[p for p in repo.rglob('*.py') if '.git' not in p.parts]
    result={}
    for pattern in patterns:
        matches=[p for p in files if fnmatch.fnmatch(p.relative_to(repo).as_posix(),pattern)]
        methods=[]
        for p in matches: methods.extend(methods_in_file(p))
        result[pattern]=sorted(methods)
    return result
