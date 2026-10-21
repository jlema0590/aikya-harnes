---
name: aikya-answers
description: Validate and apply an approved declarative Aikya technical profile while preserving existing-project files.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Declarative profile installation
1. Resolve the user-supplied JSON path, defaulting to .aikya/answers.json when configured.
2. Validate the legacy project profile without changing schema keys or enum values.
3. For mode: existing, use the restrictive adoption installer, or recommend /aikya-analyze for automatic discovery.
4. For mode: new, confirm the target is empty or contains verified Aikya-only bootstrap assets.
5. Honor explicit --docs-lang en|es solely for Aikya living docs and preserve established policy.
6. Preview file changes, obtain approval, install only approved harness components and report the results.

Never claim an external action or test was performed unless verified.

## Methodology preservation

Validate `methodology` as standard or sdd. Enable SDD only from a reviewed profile and explicit approval. Show the engine/generator upgrades and quality-gate backup before writes. Preserve an existing SDD selection; disabling it requires a separate migration. Never claim activation if a custom asset blocks installation.
