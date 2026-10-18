---
name: aikya-docs
description: Mantiene documentación viva de Aikya y trazabilidad de cada petición desde Claude Code.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-docs

Sincroniza la documentación afectada por la tarea `$ARGUMENTS` y valida sus evidencias.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee `.claude/rules/01-documentation-policy.md` y `docs/README.md`. Identifica cambios reales en Git y estado de la petición en `.harness/state/` (sin exponer información sensible).
2. Actualiza únicamente documentos pertinentes: `docs/overview.md`, `docs/plan/roadmap.md`, `docs/features/`, `docs/bugs/`, `docs/security/`, `docs/architecture/`, `docs/decisions/`, `docs/design/`, `docs/operations/`, `docs/quality/`, `docs/harness/` y `docs/skills.md` si cambian las skills.
3. Si hubo cambios de código, tests, infra o configuración técnica, crea/actualiza `docs/changes/REQ-YYYYMMDD-xxxxxxxx.md` con **## Cambios**, **## Evidencias** y **## Documentos actualizados**; no inventes pruebas, ni copies secretos o el prompt original.
4. Ejecuta `python3 scripts/harness/docs_guard.py base` y, si el identificador de sesión está disponible, `python3 scripts/harness/docs_guard.py status --session <id>`. No confundas pasar el esquema con veracidad del contenido: revisa las afirmaciones manualmente.
5. No hagas cambios documentales artificiales ante consultas informativas sin cambios técnicos. Resume exactamente qué páginas cambiaste y qué validaciones se ejecutaron.
