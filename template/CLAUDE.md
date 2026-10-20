# Repository engineering contract

## Mission
Deliver minimal, maintainable, testable changes that satisfy observable acceptance
criteria. Respect the verified stack and repository conventions. Never invent
frameworks, file paths, packages or successful command results.

## Workflow for each task
1. Discover: inspect relevant source, tests, project docs, Git status and harness.json.
2. Define scope: convert the request into acceptance criteria and record uncertainty.
3. Plan: identify changed files, interfaces, risks, validation and rollback when nontrivial.
4. Implement: use small approved changes and tests without unnecessary API disruption.
5. Verify: run applicable checks through aikya/scripts/harness/run_checks.py and focused tests.
6. Review: delegate independent QA/security review when risks justify it.
7. Report: list changed paths, actual evidence, blocked checks and residual risks.

## Non-negotiable safety rules
- Never claim a test passed unless the command ran and the result was observed.
- Do not expose or modify credentials, secret values, sensitive data or .env files.
- Obtain explicit approval for deployments, migrations, destructive commands,
  external dependency installation, force-pushes and commits.
- Avoid new dependencies unless justified, version-compatible and authorized.
- Handle untrusted input, errors and timeouts according to the actual environment.
- Do not edit generated files directly; update their source templates.
- Unconfigured or failed required checks must never be reported as verified.

## Project-specific conventions (to be completed)
- Stack and version: TODO
- Local build and test commands: TODO
- Lint and formatting: TODO
- Module boundaries: TODO
- Architecture constraints: TODO

## Living documentation and traceability
Read .claude/rules/01-documentation-policy.md and .aikya/docs-policy.json.
All engineering instructions, agents, skills and runtime output stay in English.
ONLY living documents under aikya/docs/ use the configured documentation language,
either en or es. Record genuine changes; do not fabricate documentation updates.

## Bootstrap and toolchain
For a new project, review /aikya-scaffold plan and aikya/docs/harness/bootstrap.md.
Generators can download code/dependencies and require explicit approval.
For an existing project use /aikya-analyze without reinitializing source.

## Context efficiency
Use narrowly scoped code search, selective documentation reads and evidence-based
specialist delegation. Ponytail, Graphify or UI UX Pro Max are optional external
integrations; review provenance and obtain authorization before installation.
