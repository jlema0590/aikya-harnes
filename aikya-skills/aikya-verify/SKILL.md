---
name: aikya-verify
description: Validate affected code, contracts, security and living documentation using reproducible checks.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Verification workflow
1. Read the diff, target stack and configured checks.
2. Run focused tests and locally available validation without unauthorized external operations.
3. Inspect actual exit status and evidence for all checks.
4. Verify changed documentation under aikya/docs/ with the docs guard.
5. Report failures, skipped checks and unresolved risks precisely.

Keep engineering instructions in English. Living documentation language is restricted to aikya/docs/.

## SDD evidence

For `methodology=sdd`, run the engine's `lint --root .` structural check and inspect the active specification with `/aikya-sdd-status`. Before claiming completion, require `completion --root . --id SPEC-NNN` plus separately observed technical checks. Draft validity is not completion; evidence records never certify tests or deployments independently.
