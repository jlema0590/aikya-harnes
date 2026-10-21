---
name: aikya-infra-project
description: Plan, generate with approval and locally validate Terraform, Ansible, Docker and Kubernetes resources.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Infrastructure engineering
1. Read project profile and real Terraform, Ansible, Docker or Kubernetes files.
2. Plan is read-only and must list files, risks, prerequisites, providers and environments.
3. Generate only named files after explicit approval; never overwrite existing infrastructure or secret files.
4. Validate locally using configured tools when available; distinguish NOT_CONFIGURED from PASS.
5. Never execute terraform apply/destroy, remote init, cluster writes or production deploy without separate approval.
6. Update relevant aikya/docs/infrastructure and operations pages in the selected docs language.

Preserve project instructions and customized assets. Never claim tests, security reviews or deployments succeeded without execution. Scope external operations separately. Living docs follow .aikya/docs-policy.json; other engineering text stays English.

## SDD generation context

In `methodology=sdd`, pass `--spec-id SPEC-NNN --task-id TASK-NNN` for the active approved task when invoking the underlying generator. Stop on a failed authorization check. Plan remains read-only; generator approval is separate from SDD approval and does not authorize remote operations.
