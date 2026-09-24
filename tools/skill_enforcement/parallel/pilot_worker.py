from __future__ import annotations
import argparse
import json

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["pass", "fail"])
    a = p.parse_args()
    payload = {"mode": a.mode, "synthetic": True, "writes_product": False}
    print(json.dumps(payload, sort_keys=True))
    return 0 if a.mode == "pass" else 7

if __name__ == "__main__":
    raise SystemExit(main())
