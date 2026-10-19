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
    calls = {}
    contexts = []
    tool_outputs = []
    tool_events = set()
    stop_blocks = 0
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
                    if not isinstance(msg, dict):
                        continue
                    if msg.get("role") == "user":
                        content = msg.get("content", [])
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "tool_result":
                                    size = len(str(block.get("content", "")).encode("utf8"))
                                    tool_id = str(block.get("tool_use_id", "unknown"))
                                    marker = (str(path), str(event.get("uuid") or ""), tool_id)
                                    if marker not in tool_events:
                                        tool_events.add(marker)
                                        tool_outputs.append({"bytes": size, "tool_use_id": tool_id})
                    # Count only explicitly recorded stop-hook decisions, never infer them.
                    if event.get("hook_event_name") == "Stop" and event.get("decision") == "block":
                        stop_blocks += 1
                    if msg.get("role") != "assistant":
                        continue
                    usage = msg.get("usage")
                    if not isinstance(usage, dict):
                        continue
                    identity = msg.get("id") or event.get("uuid")
                    dedup = (str(path), str(identity)) if identity else None
                    model = str(msg.get("model") or "unknown")
                    # Streamed transcript snapshots reuse the same message id.
                    # Keep the largest cumulative usage per category.
                    current = {k: v for k in KEYS
                               if type(v := usage.get(k, 0)) is int and v >= 0}
                    if dedup:
                        old = calls.get(dedup, {})
                        for key, value in current.items():
                            delta = max(0, value - old.get(key, 0))
                            totals[key] += delta
                            models[model][key] += delta
                        if not old:
                            totals["calls"] += 1
                        calls[dedup] = {key: max(current.get(key, 0), old.get(key, 0))
                                        for key in KEYS}
                    else:
                        totals["calls"] += 1
                        for key, value in current.items():
                            totals[key] += value
                            models[model][key] += value
                    sessions.add(str(path))
                    if "input_tokens" in current:
                        context = sum(current.get(k, 0) for k in (
                            "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
                        contexts.append(context)
        except (OSError, UnicodeError):
            continue
    return {
        "sessions_with_usage": len(sessions),
        "totals": dict(totals),
        "models": {key: dict(value) for key, value in sorted(models.items())},
        "context_observations": {
            "first": contexts[0] if contexts else None,
            "mean": round(sum(contexts) / len(contexts)) if contexts else None,
            "max": max(contexts) if contexts else None,
            "note": "Per transcript occurrence, not a distinct request or window-size guarantee."
        },
        "largest_tool_results": sorted(tool_outputs, key=lambda v: v["bytes"], reverse=True)[:10],
        "stop_blocks_explicitly_recorded": stop_blocks,
        "note": "Local usage estimates only. No content is printed; model/provider prices and actual invoice are not inferred."
    }

def estimate_cost(report: dict, price_catalog: dict) -> dict:
    """Opt-in USD estimates from explicitly provided per-million-token rates."""
    if not isinstance(price_catalog, dict) or not isinstance(price_catalog.get("models"), dict):
        raise ValueError("price catalog must contain a models mapping")
    rates = {"input_tokens": "input", "output_tokens": "output",
             "cache_creation_input_tokens": "cache_creation",
             "cache_read_input_tokens": "cache_read"}
    values = {}
    missing = []
    for model, usage in report["models"].items():
        price = price_catalog["models"].get(model)
        if not isinstance(price, dict) or any(
            not isinstance(price.get(k), (int, float)) or price[k] < 0 for k in rates.values()
        ):
            missing.append(model)
            continue
        values[model] = round(sum(usage.get(key, 0) * price[label] / 1_000_000
                                  for key, label in rates.items()), 8)
    return {"currency": "USD", "by_model_estimated": values,
            "total_estimated": round(sum(values.values()), 8) if not missing else None,
            "models_missing_prices": missing,
            "note": "Not a provider bill; assumes supplied rates and transcript usage are comparable."}


def main():
    p = argparse.ArgumentParser(description="Aikya tokens: local usage, read only")
    p.add_argument("--path", type=Path, help="Explicit project transcript directory; never scans unrelated projects")
    p.add_argument("--prices", type=Path, help="Optional user-provided USD/MTok JSON rate catalog")
    args = p.parse_args()
    if args.path is None:
        p.error("--path is required to avoid reading unrelated projects")
    if not args.path.exists():
        p.error("transcript path not found")
    files = sorted(args.path.rglob("*.jsonl")) if args.path.is_dir() else [args.path]
    report = summarize(files)
    if args.prices:
        report["cost"] = estimate_cost(report, json.loads(args.prices.read_text(encoding="utf8")))
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
