from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except (OSError, ValueError):
        return False


def _write_intent(mode, flags) -> bool:
    text = mode if isinstance(mode, str) else ""
    if any(ch in text for ch in ("w", "a", "x", "+")):
        return True
    if isinstance(flags, int):
        mask = 0
        for name in ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"):
            mask |= int(getattr(os, name, 0))
        return bool(flags & mask)
    return False


def install_policy(scratch: Path) -> None:
    scratch = scratch.resolve()
    mutation_events = {
        "os.remove", "os.rmdir", "os.mkdir", "os.rename", "os.replace",
        "os.chmod", "os.chown", "os.truncate", "os.utime", "os.link", "os.symlink",
    }

    def require_write_path(value) -> None:
        if isinstance(value, int):
            return
        try:
            path = Path(os.fspath(value))
        except (TypeError, ValueError):
            raise PermissionError("SANDBOX_PATH_UNRESOLVED")
        if not path.is_absolute():
            path = Path.cwd() / path
        if not _is_relative_to(path, scratch):
            raise PermissionError("SANDBOX_WRITE_DENIED")

    def audit(event, args):
        if event == "open":
            path = args[0] if args else None
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else None
            if _write_intent(mode, flags):
                require_write_path(path)
            return
        if event in mutation_events:
            if event in {"os.rename", "os.replace"}:
                if args:
                    require_write_path(args[0])
                if len(args) > 1:
                    require_write_path(args[1])
            elif args:
                require_write_path(args[0])
            return
        if event in {"subprocess.Popen", "os.system", "os.posix_spawn", "os.posix_spawnp"}:
            raise PermissionError("SANDBOX_SUBPROCESS_DENIED")
        if event in {"socket.connect", "socket.bind"}:
            raise PermissionError("SANDBOX_NETWORK_DENIED")

    sys.addaudithook(audit)


def _execute_python(argv: list[str]) -> None:
    if not argv or Path(argv[0]).resolve() != Path(sys.executable).resolve():
        raise RuntimeError("SANDBOX_ONLY_CURRENT_PYTHON_SUPPORTED")
    tokens = list(argv[1:])
    while tokens and tokens[0] in {"-B", "-E", "-s", "-S", "-u"}:
        tokens.pop(0)
    if len(tokens) >= 2 and tokens[0] == "-m":
        module = tokens[1]
        sys.argv = [module, *tokens[2:]]
        runpy.run_module(module, run_name="__main__", alter_sys=True)
        return
    if tokens and tokens[0].endswith(".py"):
        script = Path(tokens[0])
        if not script.is_absolute():
            script = ROOT / script
        sys.argv = [str(script), *tokens[1:]]
        runpy.run_path(str(script), run_name="__main__")
        return
    raise RuntimeError("SANDBOX_PYTHON_ARGV_UNSUPPORTED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--probe-target", type=Path)
    parser.add_argument("argv_json")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    os.environ["TEMP"] = str(scratch)
    os.environ["TMP"] = str(scratch)
    if args.probe_target is not None:
        os.environ["SER_B0_SANDBOX_PROBE_TARGET"] = str(args.probe_target.resolve())
    install_policy(scratch)
    argv = json.loads(args.argv_json)
    if not isinstance(argv, list) or not argv or any(not isinstance(x, str) or not x for x in argv):
        raise RuntimeError("SANDBOX_ARGV_INVALID")
    _execute_python(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
