# Aikya Harness v6.0.0 — Compatibility & migration from v5.9.1

## Branch and release contract

Source branch: `develop` (v5.9.1 at branch creation). Feature branch: `feat/token-efficiency-observability`. Version: `6.0.0`. No tags/releases are created on a feature branch; follow the v5.9.1 release workflow after a reviewed PR into `main`. Before promoting `develop` to `main`, reconcile existing divergence caused by the 5.9.1 tag recovery; never move existing tags to make v6 pass.

## Preserved behavior

- Existing `answers.json` and `.harness/project-profile.json` schemas remain unchanged.
- `project_type` still defaults to `development` for legacy profiles; infrastructure and DevOps remain isolated.
- No automatic SDK installation, remote download, production deploy, git commit or push in install.
- Existing `/aikya-*` commands and compatibility aliases must continue working.
- Installer/bootstrap preserve modified local files, and the new policy lives separately at `.aikya/model-policy.json`.
- No modification to the global Claude Code model. The actual model available depends on the user's account, CLI and provider.
- If no policy exists, planner/orchestrator default to `opus`; all other newly managed engineering agents resolve to `inherit`.
- Auxiliary Haiku is disabled until explicitly approved. The pinned ID `claude-haiku-4-5-20251001` must be tested against the actual provider before use; fallback is the user model.

## Pre-release acceptance matrix

| Case | Required assertion |
|---|---|
| Clean v5.9.1 development profile | Same project structure, commands, hooks, docs and checks, plus optional v6 modules |
| Existing customized agent/skill | No clobber; preserve exact file bytes |
| Infrastructure-only profile | No app scaffolding or language agents |
| DevOps-only profile | No application generation or forced SDK |
| Model policy absent | v5.9.1 answers read unchanged and conservative defaults |
| Model policy invalid | Validation fails visibly; no silent privilege or model change |
| Auxiliary enabled without consent | Rejected |
| Haiku 4.5 unavailable | Fail closed/fallback to inherit, report mismatch |
| JSONL missing/malformed | Report gracefully; never transmit or save prompts |
| CI and release flow | Existing 5.9.1 version/tag integrity checks must remain active |

## Known limitations to resolve before a non-draft PR

1. Full suite and installer smoke tests have not yet been run in a fresh checkout by this integration.
2. Managed legacy agents installed in 5.9.1 require a documented migration that distinguishes prior managed content from user customizations before applying the new default routing.
3. Report attribution must handle repeated/streamed messages correctly and include tool-output sizes/Stop hook events in the final benchmark.
4. Establish baseline A/B measurements and price configuration by model/provider, without implying monetary savings from token counts alone.
5. Review compatibility and retirement status of Haiku 4.5 before enabling it on supported installations.
