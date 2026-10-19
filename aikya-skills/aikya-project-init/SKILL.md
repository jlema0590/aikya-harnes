---
name: aikya-project-init
description: Define la estructura inicial y el plan técnico de un proyecto Aikya.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-project-init

Petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee **sólo cuando sea necesario** la skill de proyecto `.claude/skills/project-init/SKILL.md`. Si no está instalada, lee la fuente correspondiente en `.aikya/runtime/template/.claude/skills/project-init/SKILL.md` (scope proyecto) o `~/.claude/aikya-harnes/template/.claude/skills/project-init/SKILL.md` (scope global).
2. Sigue las instrucciones técnicas especializadas de esa skill y las reglas del proyecto; no te limites a invocarla, ejecuta el flujo dentro de Claude Code.
3. Si la tarea cambia código, actualiza documentación afectada y verifica pruebas reales.
4. Devuelve resultados realmente observados y pendientes. No uses herramientas externas automáticamente ni delegues sin motivo.

## SDD v6.0.0

Si `methodology=sdd`, la planificación inicial parte de requisitos aprobados en SPEC-NNN; no generes módulos ni decisiones de arquitectura definitivas antes de `/aikya-specify` y `/aikya-clarify`. Conserva los documentos de roadmap y ADR existentes sin sobrescrituras silenciosas.
