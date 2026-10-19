#!/usr/bin/env python3
"""Aikya v6 model policy: conservative, explicit and backwards compatible."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

DEFAULT = {"schema_version": 1, "planning_model": "opus", "orchestration_model": "opus",
           "routine_model": "inherit", "auxiliary_model": "inherit",
           "auxiliary_enabled": False, "user_approved": False}
ALLOWED = {"opus", "sonnet", "haiku", "inherit"}

def validated(raw: dict | None) -> dict:
    if raw is None:
        return dict(DEFAULT)
    if not isinstance(raw, dict):
        raise ValueError("model policy must be an object")
    unknown = set(raw) - set(DEFAULT)
    if unknown:
        raise ValueError("unknown model policy fields: " + ", ".join(sorted(unknown)))
    result = dict(DEFAULT)
    result.update(raw)
    if type(result["schema_version"]) is not int or result["schema_version"] != 1:
        raise ValueError("unsupported model policy schema")
    for key in ("planning_model", "orchestration_model", "routine_model", "auxiliary_model"):
        if result[key] not in ALLOWED:
            raise ValueError("unsupported model selection: " + key)
    for key in ("auxiliary_enabled", "user_approved"):
        if type(result[key]) is not bool:
            raise ValueError(key + " must be boolean")
    if result["auxiliary_enabled"] and not result["user_approved"]:
        raise ValueError("auxiliary delegation requires explicit user approval")
    return result

def resolved_agent_model(role: str, policy: dict) -> str:
    p = validated(policy)
    if role == "planner":
        return p["planning_model"]
    if role == "orchestrator":
        return p["orchestration_model"]
    if role in {"log-summarizer", "repository-explorer", "docs-indexer"} and p["auxiliary_enabled"]:
        return p["auxiliary_model"]
    return p["routine_model"]

def main() -> int:
    parser = argparse.ArgumentParser(description="Aikya model policy validation")
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--role", default="developer")
    args = parser.parse_args()
    policy = validated(json.loads(args.policy.read_text(encoding="utf8")) if args.policy else None)
    print(json.dumps({"policy": policy, "role": args.role,
                      "resolved_routing": resolved_agent_model(args.role, policy)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
