# Aikya Harness

**One engineering workflow. Multiple AI agents. Consistent quality.**

![Aikya Harness](./Aikya-Harness.png)

Aikya Harness is a Claude Code engineering environment combining safe project
onboarding, application scaffolding, infrastructure-as-code planning, curated
subagents, Agent Skills, quality gates, observability and living documentation.

Supported stacks include Java, .NET, Node.js, Next.js and Python backends;
React, Vue, Angular and Astro frontends; Android, iOS, Flutter and React Native
applications; and standalone infrastructure and DevOps repositories.

**All interactions are initiated through Claude Code.** The harness maintains
its supporting Python scripts internally and requests approval before writes,
third-party downloads, SDK installation or external operations.

## 1. Quick start

Open Claude Code in the target project and request:

> Install Aikya Harness from https://github.com/jlema0590/aikya-harness.git,
> branch develop, in global scope. Review the source and request approval before
> any downloads or configuration changes. Register its skills, hooks and
> welcome message without changing unrelated repositories or installing SDKs.
> Then explain /aikya-init and /aikya-analyze.

Start a new Claude Code session to load the commands and welcome hook.

Choose one onboarding flow:

- **New project:** /aikya-init — interview and creation of the new technical profile.
- **Existing repository:** /aikya-analyze — evidence-based detection and safe adoption
  without a project interview.

| Installation scope | Behavior |
|---|---|
| Global | Registers commands for the current Claude Code user with a shared runtime; does not initialize projects. |
| Project | Registers only within the current repository with a local runtime under .aikya/runtime/. |

Both modes preserve customized skills and configurations.

### Documentation language

Only Aikya living docs under **aikya/docs/** can be generated in English or Spanish:

- **en** (English, default)
- **es** (Spanish)

The choice is requested during /aikya-init. For existing projects,
use /aikya-analyze --docs-lang en or /aikya-analyze --docs-lang es;
without a configured preference, the Claude Code command asks this single
language question before an approved installation.

The preference is stored in .aikya/docs-policy.json, not in the legacy
technical profile. All agents, skills, source, CLI, hooks, project rules,
root documentation and files outside aikya/docs/ remain **English**.
Spanish/English user requests are both supported by task classifiers.

Changing an existing documentation language is a separate reviewed migration:
it is never triggered silently by refreshing Aikya.

## 2. Onboarding modes and project types

**/aikya-init is exclusively for new projects.** It always selects
mode=new and uses an interview to establish project_type and required choices.

**/aikya-analyze is exclusively for existing projects.** It discovers the
stack and architecture from repository evidence, chooses mode=existing and
previews Aikya-only file changes. It never invents an ambiguous backend.

| Project type | Technical intake | Result |
|---|---|---|
| development | Stack, application layout, architecture, testing and optional platform support | Application plan, Aikya quality/docs and scoped infrastructure |
| infrastructure | Terraform/OpenTofu, Ansible, provider, environments and constraints | Infrastructure planning without invented application modules |
| devops | Docker, image/source, existing Helm chart, Kubernetes, YAML/Kustomize | Container and delivery plans without replacing existing resources |

Existing v5.9.1 profiles without project_type remain compatible as development
profiles. The internal installer continues accepting mode=existing for legacy
declarative configuration, but /aikya-init no longer exposes that option.

### Existing repositories: safety-first adoption

/aikya-analyze --dry-run previews detection without installing anything.
/aikya-analyze --report-only returns a report without writing artifacts.
/aikya-analyze --refresh updates only verifiably managed analysis assets.

Optional focus values: security, architecture, infrastructure or operations.
Use --scope with a relative project path to inspect one component of a monorepo.
Ambiguous repositories return PARTIAL or NEEDS_REVIEW. Approval is required
before incorporation; application code, Terraform, Docker, GitHub workflows
and customized configurations are not overwritten.

The discovery phase does not build applications, run Terraform, contact
cloud infrastructure, execute application scripts or deploy containers.

## 3. Claude Code commands

| Command | Purpose |
|---|---|
| /aikya-init | Interview and initialize a brand-new project |
| /aikya-analyze | Discover and adopt an existing repository |
| /aikya-answers | Apply a validated declarative technical profile |
| /aikya-doctor | Diagnose SDK and runtime prerequisites locally |
| /aikya-project-init | Plan a new project or module |
| /aikya-infra-project | Plan, generate with approval and validate infrastructure |
| /aikya-scaffold | Plan and execute approved application generators for new projects |
| /aikya-feature | Implement a scoped feature with tests |
| /aikya-bugfix | Investigate defects and add regression evidence |
| /aikya-architecture-review | Review architecture and propose ADRs |
| /aikya-mobile-feature | Deliver validated mobile features |
| /aikya-skills-status | Inspect registered Agent Skills |
| /aikya-skills-plan | Assess external skill sources and installation impact |
| /aikya-skills-install | Install reviewed external skills after approval |
| /aikya-quality | Run available quality gates |
| /aikya-docs | Maintain evidence-backed living documentation |
| /aikya-tests | Run focused and regression tests |
| /aikya-documentation-sync | Synchronize impacted docs and request traceability |
| /aikya-verify | Validate technical changes and results |
| /aikya-models | Review optional model routing policy |
| /aikya-tokens | Inspect token usage and estimated API costs |

The project-local skills architecture also includes base feature, bugfix,
verification, documentation and architecture-review workflows. Do not invoke
optional external tools automatically.

## 4. Generated project structure

- .aikya/answers.json — technical decisions for compatible profiles.
- .aikya/docs-policy.json — living documentation language (en/es).
- .aikya/model-policy.json — optional per-role model policy.
- .aikya/analysis/ — English evidence-based inventory for existing repositories.
- .harness/project-profile.json — legacy-compatible normalized profile.
- .harness/engineering-catalog.json — managed skill/agent provenance.
- .claude/agents/ and .claude/skills/ — selected specialists and capabilities.
- .claude/rules/ and CLAUDE.md — English engineering contracts.
- aikya/docs/ — living docs in the selected en/es language.
- aikya/scripts/ and aikya/test/ — internal harness utilities and tests.
- harness.json — configured quality checks, including NOT_CONFIGURED behavior.

For a new monorepo, application workspaces can be planned under apps/ with
shared packages/ and contracts/. A singlerepo keeps its single application
at the root. Existing projects are not reorganized automatically.

## 5. Infrastructure and DevOps

The infrastructure workflows support Terraform/OpenTofu, Ansible, Docker,
Docker Compose, Kubernetes YAML, Helm and Kustomize. Plan is read-only;
generate requires explicit approval; validate only reports verified local
results. Applying cloud infrastructure, remote state migrations or cluster
deployments requires separate authorization.

In DevOps-only profiles, an existing versioned image or Helm chart may be used
without creating a fictional application or Dockerfile. Infrastructure manifests
are not evidence that cloud resources are deployed.

## 6. Engineering agents and Agent Skills

Aikya provides a curated technical catalog spanning architecture, Java, .NET,
Python, Kotlin, Flutter, Node, Vue, Angular, React, Astro/Next.js, cloud,
Terraform, Ansible, Docker, Kubernetes, CI/CD, security, testing and review.

Planner and Orchestrator are used selectively for complex cross-stack work.
Architecture and security reviewers are read-only. Code-modifying specialists
only change approved scope; independent operations still require authorization.

Agent definitions and Agent Skills follow Claude Code's local file format.
Agents and skills are selected by the actual stack, not installed indiscriminately.
An installed agent is not proof that it has been invoked.

### External skills

Ponytail, Graphify CLI and UI UX Pro Max are optional. Source provenance,
license, tools, network access and version/commit must be reviewed before
installation. /aikya-skills-plan provides a preview; /aikya-skills-install
requires explicit approval. Never execute third-party installer hooks silently.

## 7. Model and token policy (v6.0.0)

Aikya retains the user's active Claude Code model by default. Opus may be
recommended for genuinely complex planning/orchestration; routine agents
inherit their configured role model. Haiku 5.5 is optional for bounded extraction,
routing advice and documentation drafts only, subject to explicit user approval,
provider access and compatible client capabilities.

Haiku must not be the final authority for security findings, critical
architectural decisions or production operations. Token reports distinguish
actual usage records from estimated API prices and uncertain caching effects.
Existing v5.9.1 policy v1 and Haiku 4.5 choices are preserved.

Managed Agents API and a custom Messages API tool-use loop are not part of Aikya.

## 8. Versioning and publication

VERSION and CHANGELOG.md define version candidates and release notes.
Pull requests into develop run tests and smoke checks; an approved merge into
main uses guarded release workflows for tags, checksums and GitHub Releases.
No workflow should reuse an existing version tag pointing to a different commit.
The release contract preserves legacy Spanish changelog headings while English
Unreleased is the standard for new notes.

See .github/workflows.md and docs/INIT_ANALYZE_SEPARATION.md for details.

## 9. Safety guarantees and limits

- Preserve custom project files, agents, skills, instructions and secrets.
- No automatic SDK installation, dependency download or production deployment.
- No Terraform apply/destroy, remote cluster writes or destructive migration without approval.
- Report actual PASS, FAIL, SKIPPED and NOT_CONFIGURED outcomes; never invent results.
- Keep source and infrastructure evidence separate from live production state.
- Guard documentation changes through project-specific policies and traceability.
- Assess optional vendors before installation and do not expose credentials.

## 10. Examples

Example decision files are provided for Java/React, Python/Angular,
Next.js/React, .NET/Vue, Node/React microservices, Android/Kotlin and
infrastructure-only and DevOps-only profiles.

Browse [examples](examples/README.md) for scenario descriptions and
approved /aikya-answers usage. They are **decision examples**, not claims
that applications, SDKs or cloud resources have been created or verified.

## 11. Further documentation

- [Changelog](CHANGELOG.md)
- [Contribution guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Init/analyze separation](docs/INIT_ANALYZE_SEPARATION.md)
- [v6 model and compatibility policy](docs/V6_TOKEN_COMPATIBILITY.md)
- [GitHub workflow contracts](.github/workflows.md)
