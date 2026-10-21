---
name: aikya-docs
description: Synchronize evidence-based living documentation after approved technical changes; avoid unnecessary documentation writes.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Living documentation maintenance
1. Read only the affected source and Aikya pages.
2. For informational requests with no changes, do not create artificial docs updates.
3. Use .aikya/docs-policy.json to select en or es exclusively under aikya/docs/.
4. Update affected overview, security, architecture, operations, quality and change-log pages from verified evidence.
5. Record performed tests; preserve modified team docs and stable filenames/links.
6. Validate docs with the local docs guard and show any failing gates.

Preserve project instructions and customized assets. Never claim tests, security reviews or deployments succeeded without execution. Scope external operations separately. Living docs follow .aikya/docs-policy.json; other engineering text stays English.

## SDD evidence

For `methodology=sdd`, run the engine's `lint --root .` structural check and inspect the active specification with `/aikya-sdd-status`. Before claiming completion, require `completion --root . --id SPEC-NNN` plus separately observed technical checks. Draft validity is not completion; evidence records never certify tests or deployments independently.
