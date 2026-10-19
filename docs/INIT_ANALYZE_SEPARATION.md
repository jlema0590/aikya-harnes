# ADR: Separate greenfield initialization from existing-project adoption (v6.0.0)

Status: Implemented on feature branch; draft PR pending release acceptance.

## Decision

- /aikya-init: only empty/new projects; Claude Code performs a technical interview and produces mode=new.
- /aikya-analyze: only repositories with existing code or infrastructure; deterministic read-only discovery, no interview. A first invocation produces a plan, and a subsequent CLI --approved execution creates Aikya-owned assets.
- Shared install.validated(), install.install(), doc_bootstrap.pages() and engineering_catalog modules continue to accept legacy mode=existing.
- CLI init refuses an existing profile without writing; declarative CLI answers continues to accept legacy mode=existing with a warning.
- The installer receives adopt_existing=True and skips .gitignore writes, infrastructure/CI template creation, migration of pre-existing v5.5 configs, writes to existing Claude settings, and overwrites of existing profile documents.

## How to use

New project: /aikya-init in an empty directory (or approved Aikya-only bootstrap).

Existing Java/Docker, Vue, Angular, Flutter, Python/Node, Terraform/Azure, DevOps:

1. /aikya-analyze or /aikya-analyze --focus security.
2. Internally, python3 aikya_cli.py analyze --target . --dry-run.
3. Review detected technologies, all planned Aikya paths and any undecided choices.
4. With explicit authorization, python3 aikya_cli.py analyze --target . --approved.
5. Continue with /aikya-feature, /aikya-bugfix, /aikya-quality, /aikya-docs.

Optional flags: --scope relative/path, --focus security|architecture|infrastructure|operations,
--report-only, --dry-run, --refresh. If detection is partial or ambiguous, do not invent
a primary framework; no installation occurs.

## Architecture and evidence

project_discovery.scan(root, scope) inspects bounded manifest names and limited JSON/Terraform provider declarations without running project scripts, Docker or Terraform. It excludes vendor directories and ignores harness-generated files. profile_builder.build(root,inventory) projects an unambiguous application or infrastructure into the historical schema. Unsupported combinations return PARTIAL and the evidence is still visible in the preview.

aikya_analyze.execute() orchestrates the preview, file-level installation list and consent-controlled adoption. analysis_manifest.py records ownership hashes for analysis assets, avoids user-modified documents and supports --refresh. It never asserts tests, remote state or CVEs are verified.

Routing models remain independent of onboarding: deterministic parsing first, auxiliary Haiku 5.5 only with user approval and compatible Claude Code. The primary user model performs technical/security review; Planner/Orchestrator are optional for high complexity. No global model change is made.

## Compatibility and limitations

- Keep mode=new/existing accepted by install.validated and doc_bootstrap.
- Keep infrastructure.iac=existing, Helm chart mode=existing, source_kind=image and deployment protections.
- Preserve v5.9.1 project-profile schema v1, answers.json, existing user Claude instructions and prior model policies, including Haiku 4.5.
- Do not run installers, cloud calls or project scripts during analysis.
- Python CLI --approved represents explicit consent; automated systems must not add it implicitly.
- Multi-backend projects without an unambiguous principal return PARTIAL rather than a fabricated primary technology.
- A manifest/path-only inventory is not a full dependency audit or executable architecture graph.
- Existing-file conflicts require user review. Imported Aikya copies are managed according to pre-existing installer semantics; new analysis files use content hashes.
- A read-only dry-run does not guarantee that the user's Python installation will avoid external telemetry configured outside Aikya. Aikya itself makes no external calls.

## QA acceptance

Tests must cover four original cases: Node and Python security; Vue and Angular structure; Terraform plus scripts (Azure); Java plus Docker. Also include Flutter, monorepo, symlink traversal, existing profiles and Haiku policy, approval gates, dry-run, report-only, idempotence, custom analysis report conflicts, existing CI/.gitignore preservation and Python 3.10-3.13. Release workflow remains unchanged and PR stays draft until final verification.
