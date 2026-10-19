---
name: documentation-sync
description: Sincroniza documentación por petición y genera trazabilidad verificable. Se ejecuta antes de cerrar un cambio de código o infraestructura.
---
# Sincronizar documentación por petición

1. Revisa `.harness/state/` (estado de la sesión activa) para localizar `request_id`.
2. Identifica módulos y contratos cambiados; decide qué documentación está afectada, sin actualizar páginas innecesarias.
3. Actualiza el contenido técnico real en `aikya/docs/overview.md`, `aikya/docs/plan/roadmap.md`, `aikya/docs/features/index.md`, `aikya/docs/bugs/index.md`, `aikya/docs/security/security.md`, `aikya/docs/architecture/overview.md`, `aikya/docs/operations/`, `aikya/docs/quality/testing.md` y ADR cuando aplique.
4. Crea `aikya/docs/changes/REQ-YYYYMMDD-xxxxxxxx.md` con encabezados **## Cambios**, **## Evidencias** y **## Documentos actualizados**. Incluye rutas concretas del código y los documentos; no inventes pruebas ejecutadas.
5. Si el proyecto ya tenía documentos o convenciones, preserva su información y enlaza el material nuevo.
6. Valida `python3 aikya/scripts/harness/docs_guard.py status --session <session_id>` si conoces session_id, o deja actuar al Stop hook. Para revisar plantilla: `python3 aikya/scripts/harness/docs_guard.py base`.
7. No registres prompts literales, secretos, datos personales ni credenciales.

El hook sólo verifica cobertura estructural y cambios reales por petición; **la veracidad técnica de los textos requiere revisión**.
**Regla de tokens:** no reproduzcas dumps de Graphify ni las salidas completas de UI UX Pro Max en docs. Registra decisiones y evidencias útiles y enlaza artefactos. Si cambian pantallas/diseño, actualiza `aikya/docs/design/design-system.md`.
