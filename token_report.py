#!/usr/bin/env python3
"""Read-only, local Claude Code session usage report. No prompts are persisted."""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path

KEYS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")

def summarize(paths):
    totals = defaultdict(int)
    models = defaultdict(lambda: defaultdict(int))
    sessions = set()
    calls = set()
    for path in paths:
        try:
            with path.open(encoding="utf8") as fh:
                for line in fh:
                    try:
                        event = json.loads(line)
                    except (ValueError, UnicodeError):
                        continue
                    if not isinstance(event, dict):
                        continue
                    msg = event.get("message")
                    if not isinstance(msg, dict) or msg.get("role") != "assistant":
                        continue
                    usage = msg.get("usage")
                    if not isinstance(usage, dict):
                        continue
                    identity = msg.get("id") or event.get("uuid")
                    dedup = (str(path), str(identity)) if identity else None
                    if dedup and dedup in calls:
                        continue
                    if dedup:
                        calls.add(dedup)
                    sessions.add(str(path))
                    model = str(msg.get("model") or "unknown")
                    totals["calls"] += 1
                    for key in KEYS:
                        value = usage.get(key, 0)
                        if type(value) is int and value >= 0:
                            totals[key] += value
                            models[model][key] += value
        except (OSError, UnicodeError):
            continue
    return {"sessions_with_usage": len(sessions), "totals": dict(totals),
            "models": {key: dict(value) for key, value in sorted(models.items())},
            "note": "Reported usage may include cached and repeated transcript snapshots; no monetary cost inferred."}

def main():
    p = argparse.ArgumentParser(description="Aikya tokens: local usage, read only")
    p.add_argument("--path", type=Path, help="Explicit project transcript directory; never scans unrelated projects")
    args = p.parse_args()
    if args.path is None:
        p.error("--path is required to avoid reading unrelated projects")
    if not args.path.exists():
        p.error("transcript path not found")
    files = sorted(args.path.rglob("*.jsonl")) if args.path.is_dir() else [args.path]
    print(json.dumps(summarize(files), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
