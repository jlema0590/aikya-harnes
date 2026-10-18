---
name: aikya-scaffold
description: Prepara o ejecuta scaffolding backend, frontend y móvil desde Claude Code, con validación previa de SDKs y consentimiento.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-scaffold

Solicita el alcance de `$ARGUMENTS` (por ejemplo: `plan`, `backend`, `frontend` o `móvil`).
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Comprueba el perfil técnico y lee `docs/harness/bootstrap.md` y `docs/harness/requirements.md` cuando existan. Ejecuta `/aikya-doctor` o la validación interna del detector si no hay informe reciente; si hay SDK ausentes o incompatibles, BLOQUEA generación y solicita autorización para resolverlos.
2. Ejecuta **sólo para planificar** `python3 scripts/harness/scaffold.py plan`. Explica qué generadores se usarían, versiones, archivos afectados, efectos de red y pasos manuales. No ejecutes `apply` solo porque el usuario diga «planifica».
3. Si `mode: existing`, no ejecutes `scaffold.py apply`: revisa el repositorio y plantea migraciones incrementales con autorización separada.
4. Si `mode: new`, genera únicamente tras aprobación inequívoca del plan específico. Dentro de Claude Code ejecuta `python3 scripts/harness/scaffold.py apply --yes` y revisa el resultado. No saltes bloqueos por faltantes ni borres directorios para reintentarlo.
5. Verifica builds y pruebas REALES según el stack. Ajusta `harness.json` sin falsear checks. Actualiza `docs/architecture/`, `docs/plan/`, `docs/features/`, `docs/quality/testing.md`, `docs/harness/bootstrap.md` y registro `docs/changes/REQ-*.md` según corresponda.
6. Entrega lista de generadores ejecutados, resultados, pendientes manuales, versiones y riesgos; ofrece `/aikya-quality` para revisión completa.
