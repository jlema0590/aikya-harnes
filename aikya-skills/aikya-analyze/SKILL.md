---
name: aikya-analyze
description: Adopt an existing repository without a technical interview, using read-only discovery followed by approved Aikya installation.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Existing project adoption
1. Resolve project-scoped Aikya CLI; do not execute application scripts during discovery.
2. Accept --focus, --scope, --dry-run, --report-only, --refresh and --docs-lang en|es.
3. When no locale is configured, ask only for living documentation language en or es; no project interview.
4. First run CLI analyze --dry-run with the requested scope, focus and locale, and present the full file plan.
5. Stop on PARTIAL or NEEDS_REVIEW; never invent the stack or override customized documents.
6. After explicit approval, run CLI analyze --approved and the same --docs-lang. Analysis reports outside aikya/docs/ stay English.
7. Do not build, execute Terraform, run Docker or deploy during onboarding. Changing an existing documentation language requires a separate approved migration.

Respect user approvals, preserve custom files, do not install dependencies or access external systems without separate authorization. Report tests actually executed, blocked checks and evidence. Living documentation under aikya/docs/ follows .aikya/docs-policy.json; all other content is English.

## Optional SDD adoption

Accept `--methodology sdd` only as an explicit choice, include it in the dry-run preview and preserve it on the approved call. Without that option retain an existing methodology; newly adopted repositories default to standard. Do not add a technical interview or overwrite custom profiles, generators or quality gates. Changes requiring manual integration must return NEEDS_REVIEW, not successful activation. Disabling an existing SDD methodology requires a separately reviewed migration.
