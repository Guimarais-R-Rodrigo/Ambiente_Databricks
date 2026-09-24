from __future__ import annotations
import json, sys

def main(argv=None) -> int:
    args=list(sys.argv[1:] if argv is None else argv)
    if args not in (["pass"],["fail"],["global_fail"]):
        print(json.dumps({"status":"BLOCKED","reason":"UNKNOWN_CASE"})); return 2
    case=args[0]
    if case=="pass": print(json.dumps({"status":"PASS","case":case})); return 0
    print(json.dumps({"status":"FAIL","case":case,"deliberate":True})); return 7

if __name__=="__main__": raise SystemExit(main())
