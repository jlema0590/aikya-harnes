---
name: aikya-bugfix
description: Investiga y corrige incidencias con regresiones y trazabilidad.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-bugfix

Petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee **sólo cuando sea necesario** la skill de proyecto `.claude/skills/bugfix/SKILL.md`. Si no está instalada, lee la fuente correspondiente en `.aikya/runtime/template/.claude/skills/bugfix/SKILL.md` (scope proyecto) o `~/.claude/aikya-harnes/template/.claude/skills/bugfix/SKILL.md` (scope global).
2. Sigue las instrucciones técnicas especializadas de esa skill y las reglas del proyecto; no te limites a invocarla, ejecuta el flujo dentro de Claude Code.
3. Si la tarea cambia código, actualiza documentación afectada y verifica pruebas reales.
4. Devuelve resultados realmente observados y pendientes. No uses herramientas externas automáticamente ni delegues sin motivo.


## Routing híbrido opcional (v6)

En bugs locales, prefiere especialista (inherit) y validaciones dirigidas; no invoques Opus ni Haiku por sistema. Si faltan datos o hay ambigüedad, consulta el router determinista y, solo con opt-in y modelo Haiku 5.5 disponible, pide análisis breve al auxiliar instalado. Para secretos, autenticación, seguridad, producción o migraciones, preserva revisión/aprobación por el modelo principal; Haiku jamás decide permisos ni valida evidencia de tests. No pases el prompt a Bash sin control de inyección. Conserva trazabilidad y regresiones previas.
