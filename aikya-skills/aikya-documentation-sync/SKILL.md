---
name: aikya-documentation-sync
description: Update required living documentation and per-request change records following a material code or infrastructure change.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->

# Documentation synchronization
1. Determine the actual files changed in the current request.
2. If no material change occurred, do not create artificial documentation updates.
3. Read .aikya/docs-policy.json and write solely under aikya/docs/ in the configured en or es locale.
4. Update the relevant feature, defect, security, architecture, deployment and testing pages.
5. Write a REQ-*.md log with Changes/Evidence/Updated documents for en or Cambios/Evidencias/Documentos actualizados for es.
6. Run docs_guard and disclose failures without inventing successful tests.

All instructions, reports and software-development assets outside aikya/docs/ remain in English.
