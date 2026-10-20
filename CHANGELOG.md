# Changelog

## Unreleased

- English-only engineering core with configurable English/Spanish living documentation under aikya/docs/.
- Claude Code Agent Skills and subagent quality, permissions and routing standardization.

## v6.0.0 — Token Efficiency & Observability (in development)

- Conservative validated per-role model policy: Opus for planning/orchestration, inherit for routine work, and user-approved optional Haiku.
- /aikya-models and /aikya-tokens for explicit selection and local usage reports, without changing global configuration.
- v5.9.1 profile compatibility, customized-asset preservation and regression coverage.
- Context hygiene rules for CLI output, diffs and logs.
- Separate public commands: /aikya-init for new projects and /aikya-analyze for interview-free existing-project adoption.
- Deterministic multistack discovery, compatible profile projection, reviewable file plan, ownership hashes and approved read-only analysis.
- Restrictive adopt_existing policy preserves infrastructure, scripts, CI/CD and .gitignore during onboarding; idempotence and migration tests.
- Optional Haiku 5.5 for bounded extraction, classification, routing and documentation drafts; Haiku 4.5 policy compatibility.
- Deterministic hybrid router with advisory suggestions and Planner/Orchestrator only for genuinely complex tasks.
- Clearly labeled Haiku 5.5 estimated API costs, without inventing measured token savings.

## v5.9.1 — GitHub Actions fixes and automation

- Automated tags and GitHub Releases after merging an approved version into main.
- SemVer VERSION contract, auditable release notes and tag-to-merge-commit validation.
- Separate tests, reproducible ZIP packaging, SHA-256 checksums and idempotent publishing.
- Version validation for pull requests targeting main, with controlled preparation on develop.
- Expanded CI and regression tests for publishing workflows and release scripts.
- Catalog and profile workflows remain read-only; no remote deployments.

## v5.9.0 — 2026-10-19

- Fixed /aikya-infra-project validate with Helm on symlinked project roots (for example macOS /var pointing to /private/var). Out-of-project linked charts remain rejected as NOT_CONFIGURED.
- Reorganized README with quick start, command reference, technical catalog and security.
- Merged INSTALL_FROM_CLAUDE.md into README and moved audits into docs/audits/.
- Removed obsolete repository-local command copies and unused examples/existing-api.json.

## v5.8.0 — 2026-10-18

- Introduced project_type selection for development, infrastructure and devops; originally also supported a new/existing interview choice.
- Infrastructure-only support without application SDKs, using Terraform/OpenTofu/Ansible independently or together.
- DevOps-only workflows with Docker/Compose from source or image, Kubernetes YAML, Helm and Kustomize.
- Existing Helm chart or image does not require local Docker; historical profiles without project_type remain development.
- Infrastructure quality gates and documentation without invented applications or tests; specialist selection by stack.
- Read-only plans, approved artifact generation and local validation; no automatic deployment.
- New example profiles and regressions for all three project types.

## v5.7.0 — 2026-10-18

- Corrected Node version parsing for v25.9.0 and other v-prefixed versions.
- Safe runtime requirements updates with managed-file migration and preservation of v5.6 backups and custom content.
- Optional infrastructure profile: provider, Terraform/OpenTofu, Ansible, Docker/Compose, Kubernetes, environments, image and port.
- Four infrastructure agents and three engineering skills added, activated by explicit selection.
- Infrastructure generator with plan, generate --approved and validate modes and no automatic deployment.
- Dockerfile derived from actual application code; Kubernetes requires a versioned image and confirmed port.
- Living docs, quality checks and examples for Terraform/Helm and Ansible/Kustomize.

## v5.6.0 — 2026-10-18

- Explicit monorepo/singlerepo selection during technical intake and in JSON answers.
- Monorepos alone create apps/, packages/ and contracts/; singlerepos stage a single root application.
- Consolidated Aikya documentation, tests and scripts under aikya/docs/, aikya/test/ and aikya/scripts/.
- Global welcome in new and existing projects without duplicate local hooks.
- Conservative historical-document migration and quality-gate updates.

## v5.5.0 — 2026-10-18

- Integrated 11 additional technical agents and 11 Agent Skills for languages and architectural patterns.
- At this historical version, the catalog held 23 agents and 26 skills, selected by backend/frontend/mobile and architecture.
- Added Python and Angular to the technical interview and stack detection; framework scaffolding remained guided.
- Added seven stack-specific examples with answers.json and Claude Code usage guides.
- Expanded documented responsibilities, selective activation and traceability.

## v5.4.0 — 2026-10-18 — Aikya command organization

- Renamed bootstrap_skills/ to aikya-skills/ without changing public /aikya-* command identities.
- Updated global/project bootstrap, installer and documentation paths.
- Conservatively migrated known managed legacy runtimes; customized files were preserved.
- Added fresh-install, scope-upgrade and unrelated-content protection tests.

## v5.2.0 — 2026-10-18

- Renamed /aikya-infra-project, /aikya-skills-status, /aikya-skills-plan and /aikya-skills-install.
- Allowed additional GitHub skills with source, path, name and optional commit verification, avoiding overwrite.
- Added the project skills availability inventory in aikya/docs/skills.md.
- Conservatively migrated renamed commands while preserving customizations.

## v5.1.0 — 2026-10-18 — Claude-native commands

- Added /aikya-scaffold, /aikya-skills-status, /aikya-quality, /aikya-docs and /aikya-tests alongside development commands.
- Global/project bootstrap exposed 16 conversational Aikya skills with approval for external actions and protection of user skills.
- README described installation and use from Claude Code without mandatory manual scripts.
- Preserved internal scripts and living documentation, with SDK checks before scaffolding.

## v5.0.0 — 2026-10-18

- Claude Code conversational global/project install and /aikya-init, /aikya-answers, /aikya-doctor.
- Added Aikya command prefixes without breaking previous aliases.
- Non-destructive JDK, .NET SDK, Node, web package manager and mobile SDK checks.
- Non-intrusive SessionStart reminders in uninitialized directories without automatic downloads.
- Reused JSON profiles and preserved user projects during global onboarding.
- Added bootstrap and toolchain regression tests.

## v4.1.0 — 2026-10-18

- Claude Code session welcome with local name, repository and Aikya URL.
- Non-intrusive SessionStart hook with visible message, no network or compaction notifications.
- Added --display-name and local welcome_name; identity state ignored by Git.
- Expanded command/skill examples and welcome preview in README.
- Supported welcome hooks for Aikya itself and installed projects.

## v4.0.0 — 2026-10-18

- Preserved v3 interview/bootstrap for Java, .NET, Node, Next, Vue, React, Android, iOS and cross-platform.
- User-approved Ponytail, Graphify CLI (without MCP) and conditional UI UX Pro Max integrations.
- Offline SessionStart skill checks, external skill plan/install/status management.
- Basic Agent Skills validation and progressive context-loading policies.
- Conditional design-system docs and UI change-validation gates.
- Backed up original v3 managed files; preserved customized files.
- Local suite originally contained 32 tests; networked team validation remained necessary.

## v3.0.0 — 2026-10-18

- Engineering bootstrap, technical interview, assisted scaffolding, infrastructure and
  living documentation with traceability hooks.
