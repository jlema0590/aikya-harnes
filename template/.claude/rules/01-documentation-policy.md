# Política obligatoria de documentación viva (todas las peticiones)

Para cada solicitud, consulta primero `docs/README.md` y `docs/overview.md` cuando la tarea afecte al producto. **Si editas código, tests, infraestructura, contratos, seguridad o arquitectura**, debes actualizar los documentos afectados y crear `docs/changes/REQ-*.md` asociado al ID notificado por el hook `UserPromptSubmit`. En consultas de solo lectura no fuerces documentación artificial.

- Features: actualizar `docs/features/index.md`, y el plan `docs/plan/roadmap.md` cuando cambien alcance/prioridad.
- Bugs: registrar reproducción, causa y regresión en `docs/bugs/index.md`.
- Seguridad: actualizar controles y riesgos en `docs/security/security.md`.
- Arquitectura: actualizar `docs/architecture/overview.md` y registrar ADR si se adopta una decisión irreversible.
- Infra/CI/CD: `docs/operations/deployment.md`; telemetría: `docs/operations/observability.md`.
- Tests: `docs/quality/testing.md` cuando cambia estrategia/cobertura.
- Cambios en Agent Skills (añadir, configurar, sustituir): actualizar `docs/skills.md` mediante `/aikya-skills-status` y comprobar procedencia.
- Cambios amplios: revisar y actualizar `docs/overview.md`.

La bitácora de cada petición incluye **## Cambios**, **## Evidencias** y **## Documentos actualizados**, con rutas y pruebas realmente ejecutadas. No pegues el prompt completo ni datos sensibles. Ejecuta `python3 scripts/harness/docs_guard.py base` y revisa resultados en el hook Stop. Si una regla documental no encaja en un cambio, explica por qué en la bitácora y ajusta la validación mediante revisión de código, no con un bypass silencioso.
