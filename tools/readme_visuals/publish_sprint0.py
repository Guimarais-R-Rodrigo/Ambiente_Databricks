"""Publish only the isolated Sprint 0 gallery; never change the active assistant.

Default is a read-only plan. --execute uploads, then verifies type and bytes.
--verify repeats the remote audit without mutation. Credentials stay in the CLI.
"""
from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
RELATIVE = "READMEs_refeitos/readmes_viasual_melhorado/sprint_0"
LOCAL = ROOT / RELATIVE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--expected-host", required=True)
    parser.add_argument("--http1", action="store_true", help="Use HTTP/1.1 in this CLI subprocess only; keep HTTPS/TLS verification.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    cli_environment = os.environ.copy()
    if args.http1:
        settings = [s for s in cli_environment.get("GODEBUG", "").split(",") if s and not s.startswith("http2client=")]
        cli_environment["GODEBUG"] = ",".join([*settings, "http2client=0"])

    def cli(*command):
        process = subprocess.run(["databricks", *command, "--profile", args.profile,
                                  "--output", "json"], capture_output=True, text=True,
                                 encoding="utf-8", timeout=90, env=cli_environment)
        if process.returncode:
            diagnostic = re.sub(r"[\w.+-]+@[\w.-]+", "<user>", process.stderr)
            diagnostic = re.sub(r"(?i)(bearer\s+|dapi)[A-Za-z0-9._-]+", "<redacted>", diagnostic)
            diagnostic = diagnostic.replace(str(ROOT), "<repo>")
            raise RuntimeError(f"Databricks CLI failed: {' '.join(command[:2])}: {diagnostic[:700]}")
        return json.loads(process.stdout) if process.stdout.strip() else {}

    auth = cli("auth", "describe")
    host = auth["details"]["host"].rstrip("/")
    if host != args.expected_host.rstrip("/"):
        raise RuntimeError("Profile host differs from --expected-host; no writes.")
    user = cli("current-user", "me")["userName"]
    if not user.lower().endswith("@gmail.com") or any(c in user for c in "/\\"):
        raise RuntimeError("This isolated publisher is restricted to the project laboratory account.")
    destination = f"/Users/{user}/{RELATIVE}"
    records = []
    for file in sorted(LOCAL.rglob("*")):
        if not file.is_file():
            continue
        if not file.resolve().is_relative_to(LOCAL.resolve()):
            raise RuntimeError("Source escapes isolated gallery.")
        relative = file.relative_to(LOCAL).as_posix()
        notebook = relative == "VISUALIZADOR_SPRINT_0.py"
        records.append({"relative": relative, "source": file, "target": destination + "/" + relative,
                        "type": "NOTEBOOK" if notebook else "FILE", "format": "SOURCE" if notebook else "RAW"})
    print(json.dumps({"mode": "execute_and_verify" if args.execute else "verify" if args.verify else "plan",
                      "destination": "$USER_ROOT/" + RELATIVE, "files": len(records),
                      "notebooks": sum(r["type"] == "NOTEBOOK" for r in records)}, ensure_ascii=False))
    if not args.execute and not args.verify:
        return
    qa = json.loads((LOCAL / "qa/validation.json").read_text(encoding="utf-8"))
    if qa["status"] != "passed":
        raise RuntimeError("Local visual validation did not pass.")

    if args.execute:
        directories = sorted({str(Path(r["relative"]).parent).replace("\\", "/") for r in records})
        for directory in directories:
            cli("workspace", "mkdirs", destination + ("/" + directory if directory != "." else ""))

        def upload(record):
            command = ["workspace", "import", record["target"], "--file", str(record["source"]),
                       "--format", record["format"], "--overwrite"]
            if record["type"] == "NOTEBOOK":
                command += ["--language", "PYTHON"]
            for attempt in range(3):
                try:
                    cli(*command)
                    return
                except RuntimeError as exc:
                    if attempt == 2:
                        raise RuntimeError(record['relative'] + ': ' + str(exc)) from exc
                    time.sleep(attempt + 1)
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(upload, records))
        print(f"Uploaded {len(records)} objects. Verifying type and exported bytes.", flush=True)

    def verify(record):
        info = cli("workspace", "get-status", record["target"])
        if info["object_type"] != record["type"]:
            raise RuntimeError("Wrong remote type: " + record["relative"])
        export_format = "SOURCE" if record["type"] == "NOTEBOOK" else "AUTO"
        remote = base64.b64decode(cli("workspace", "export", record["target"], "--format", export_format)["content"], validate=True)
        expected = record["source"].read_bytes()
        if record["type"] == "NOTEBOOK":
            # SOURCE export may normalize final newline; content/cell separators must match.
            remote = remote.replace(b"\r\n", b"\n").rstrip(b"\n")
            expected = expected.replace(b"\r\n", b"\n").rstrip(b"\n")
        if remote != expected:
            raise RuntimeError("Remote content mismatch: " + record["relative"])
        return {"path": record["relative"], "type": record["type"],
                "sha256": hashlib.sha256(expected).hexdigest(), "object_id": info["object_id"]}
    with ThreadPoolExecutor(max_workers=2) as pool:
        verified = list(pool.map(verify, records))
    actual = set()
    def visit(directory):
        response = cli("workspace", "list", directory)
        for obj in response if isinstance(response, list) else response.get("objects", []):
            if obj["object_type"] == "DIRECTORY":
                visit(obj["path"])
            else:
                actual.add(obj["path"])
    visit(destination)
    extras = sorted(actual - {r["target"] for r in records})
    if extras:
        raise RuntimeError(f"Unexpected remote objects: {len(extras)}. No deletion attempted.")
    notebook = next(v for v in verified if v["type"] == "NOTEBOOK")
    receipt = {"status": "verified", "destination": "$USER_ROOT/" + RELATIVE,
               "count": len(verified), "objects": verified,
               "notebook_url": f"{host}/#notebook/{notebook['object_id']}"}
    # Local operational receipt is intentionally outside versioned/public gallery.
    receipt_path = ROOT / ".artifacts/sprint_0/publication.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"verified": len(verified), "unexpected": 0, "notebook_url": receipt["notebook_url"]}))


if __name__ == "__main__":
    main()
