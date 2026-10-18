---
name: project-bootstrap
description: Prepara un monorepo, propone scaffolding oficial de backend, web y móvil, y alinea documentación, Docker, CI/CD, testing y OpenTelemetry.
---
# Engineering Bootstrap

1. Lee `.harness/project-profile.json`, `docs/overview.md`, `docs/harness/bootstrap.md` y `docs/architecture/overview.md`.
2. No reemplacemos repositorios existentes: examina tecnologías y estructura; solicita aprobación para instalaciones, migraciones o llamadas a generadores externos.
3. Para proyectos nuevos, ejecuta `python3 scripts/harness/scaffold.py plan` para conocer acciones soportadas y requisitos de SDK. **No ejecutes** `apply` sin autorización expresa.
4. Cuando el usuario apruebe, ejecuta `python3 scripts/harness/scaffold.py apply` (usa subprocess sin shell), y completa el bootstrap manual donde no haya generador CLI seguro soportado.
5. Verifica versiones/SDK, instala dependencias con aprobación, genera contratos de API, healthchecks, configuración de aplicación, Dockerfiles reales según stack, pipeline de CI/CD, pruebas y configuración OpenTelemetry según código generado. No declares integración efectiva antes de ejecutar los builds.
6. Sustituye checks sin configurar de `harness.json` por comandos que realmente existan, crea README por módulo, documenta decisiones ADR y actualiza docs afectados y docs/changes/REQ-*.md.
7. Verifica `python3 scripts/harness/run_checks.py`; informa por separado checks configurados, ejecutados y pendientes.
