---
name: aikya-quality
description: Ejecuta desde Claude Code los quality gates de Aikya, lint, seguridad, estado documental y CI sin falsos positivos.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-quality

Objetivo: evaluar calidad del repositorio actual, no instalar dependencias.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee `harness.json` y las reglas del proyecto. Si no hay checks configurados, informa explícitamente de que no pueden considerarse verificados.
2. Ejecuta `python3 aikya/scripts/harness/run_checks.py` y registra fallos, omisiones, checks `NOT_CONFIGURED` y aprobados con comando y evidencia.
3. Ejecuta `python3 aikya/scripts/harness/skills_lint.py` y `python3 aikya/scripts/harness/docs_guard.py base` si existen. Para cobertura de la petición, utiliza `/aikya-docs`; no fuerces una validación de sesión equivocada.
4. Revisa seguridad o CI/CD del área afectada cuando el cambio lo justifique, evitando scans costosos no autorizados. No confundir archivos de CI generados con pipelines ejecutados.
5. Actualiza `aikya/docs/quality/testing.md` con resultados comprobados sólo si hay cambios de código/proceso que afecten documentación, y registra evidencias en `aikya/docs/changes/` si hubo cambios técnicos. Nunca declares éxito si un gate requerido falló o no estaba configurado.
6. Devuelve resumen de QA con estado `APROBADO`, `FALLÓ` o `NO VERIFICADO`, lista de riesgos y próximos pasos.
