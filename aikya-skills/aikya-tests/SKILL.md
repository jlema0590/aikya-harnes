---
name: aikya-tests
description: Ejecuta pruebas focalizadas y de regresión desde Claude Code, documentando resultados verificables.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-tests

Pruebas para el alcance `$ARGUMENTS`: unidad, integración, e2e, móvil u otro módulo.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` para un proyecto nuevo, `/aikya-analyze` para uno existente o `/aikya-answers` para configuración declarativa.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee el perfil, `harness.json` y `aikya/docs/quality/testing.md`; determina los comandos ya existentes para ese stack. No inventes comandos ni dependencias.
2. Empieza por tests focalizados relacionados con el cambio, usando la herramienta del proyecto. Pide permiso si requieren red, servicios externos, datos de producción o migraciones de base de datos.
3. Cuando corresponda, ejecuta la suite de regresión/quality gates con `python3 aikya/scripts/harness/run_checks.py`. Distingue `PASS`, `FAIL`, `SKIP`, `NOT_CONFIGURED`, timeout y pruebas que no se pudieron ejecutar.
4. Actualiza documentación de pruebas y `aikya/docs/changes/REQ-*.md` con evidencias reales, sin afirmar cobertura porcentual no medida. Para validación integral utiliza `/aikya-quality`.
5. Reporta los comandos reales, duración si está disponible, fallos reproducibles y riesgos pendientes.
