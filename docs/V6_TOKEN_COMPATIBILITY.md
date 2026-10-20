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
- The v2 policy defaults to Haiku 5.5 (`claude-haiku-5-5`) with auxiliary delegation disabled. v1 policies, including explicitly approved Haiku 4.5 IDs, remain valid and are never migrated without renewed consent. The runtime must verify Claude Code >= 2.1.293 and user/provider access before selecting an auxiliary. Fallback remains the user's inherited model.

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
| Legacy v1 Haiku 4.5 policy | Preserve schema, model, consent and behavior until explicit migration |
| v2 Haiku 5.5 no CLI / disallowed provider | No auxiliary delegation; inherit and report what needs configuration |
| v2 Haiku 5.5 approved | Only read-only tasks from allowed_tasks; max delegation depth 1 |
| JSONL missing/malformed | Report gracefully; never transmit or save prompts |
| CI and release flow | Existing 5.9.1 version/tag integrity checks must remain active |

## Known limitations to resolve before a non-draft PR

1. Full suite and installer smoke tests have not yet been run in a fresh checkout by this integration.
2. Managed legacy agents installed in 5.9.1 require a documented migration that distinguishes prior managed content from user customizations before applying the new default routing.
3. Report attribution must handle repeated/streamed messages correctly and include tool-output sizes/Stop hook events in the final benchmark.
4. Establish baseline A/B measurements and price configuration by model/provider, without implying monetary savings from token counts alone.
5. Haiku 5.5 CLI and provider authorization require real-world verification; a stored access confirmation is not API evidence. On Bedrock, Foundry or Google Cloud, Claude Code model routing may require provider-specific deployment IDs/profiles that are not guessed by Aikya.
6. Check semantically ambiguous requests against untrusted output validation, and test the legacy v1 policies unchanged.

## Haiku 5.5: local migration procedure (no silent upgrade)

1. Open the existing `.aikya/model-policy.json` and record its schema version without changing it.
2. For v1 configs, keep Haiku 4.5 and `user_approved` unchanged; explicitly offer migration to v2.
3. Before committing a new policy, verify that the actual Claude Code CLI is at least 2.1.293 and the user's account permits `claude-haiku-5-5` on the selected provider. A provider alias `haiku` alone is insufficient.
4. Create v2 only after approval; use `auxiliary_enabled=false` until access has been confirmed. Limit approved tasks to extraction, classification, routing, documentation and log-summary, all read-only.
5. Validate policy offline, generate only the selected auxiliary agent definitions; preserve customized files under `.claude/agents` and their manifest hashes.
6. Confirm the subagent's effective model in `/tasks`. If the requested model was substituted by the organization/provider, fall back to `inherit` and notify the user before further delegation.

Current model documentation: https://platform.claude.com/docs/es/models/overview and https://code.claude.com/docs/en/model-config.

## New-project vs existing-project entry contract (v6.0.0)

- /aikya-init always uses new projects and requests the technical interview.
- /aikya-analyze is the new existing-repository entry: discovery, inventory, compatible profile and approved Aikya-only adoption without an interview.
- The shared validator/installer keeps mode=existing for backward compatibility. Existing architecture, Terraform/OpenTofu, Helm chart and Docker source-kind options remain valid.
- aikya_cli.py init refuses mode=existing without writing. Declarative answers with mode=existing continue on their legacy route with deprecation guidance.
- Existing v5.9.1 profiles and Haiku 4.5 policies are preserved, not overwritten or silently migrated.
- The brownfield installer skips user .gitignore, CI workflows, Terraform, Docker, operational scripts and pre-existing Claude settings; analysis state is maintained under .aikya/analysis/ with managed hashes.
- --dry-run and --report-only never install; --refresh only updates analysis-owned assets with hashes matching their previous managed version.
- Ambiguous monorepos are PARTIAL and require inspection rather than an invented backend.

Full ADR and user guidance: docs/INIT_ANALYZE_SEPARATION.md.
