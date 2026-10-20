---
name: aikya-architecture-review
description: Assess system architecture from repository evidence, identify trade-offs and propose ADRs without modifying code by default.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Read-only architecture review
1. Inspect the actual technical profile, source boundaries, services and contracts.
2. Identify verified architectural patterns, dependencies, risks and unknowns.
3. Evaluate maintainability, reliability, security, cost and incremental options.
4. Do not infer deployment state from manifests. Do not edit code or deploy during a review.
5. Propose ADRs and a scoped implementation plan with alternatives and validation.
6. Only update aikya/docs/ in the configured language if the user separately requests documentation changes.

Preserve project instructions and customized assets. Never claim tests, security reviews or deployments succeeded without execution. Scope external operations separately. Living docs follow .aikya/docs-policy.json; other engineering text stays English.
