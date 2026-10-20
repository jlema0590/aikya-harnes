---
name: documentation-sync
description: Synchronize impacted living docs with actual code changes and per-request evidence.
disable-model-invocation: true
---

# Documentation synchronization
1. Determine real changed files and active request ID, without storing prompt contents.
2. Do not create artificial changes for a read-only request.
3. Read .aikya/docs-policy.json and use the chosen locale exclusively under aikya/docs/.
4. Update affected pages and a REQ-*.md log with complete Changes/Evidence/Updated documents (en) or Cambios/Evidencias/Documentos actualizados (es) headings.
5. Validate docs_guard and disclose missing checks.

