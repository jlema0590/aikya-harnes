---
name: aikya-documentation-sync
description: Sincroniza la documentación obligatoria de cada cambio.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-documentation-sync

Petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee **sólo cuando sea necesario** la skill de proyecto `.claude/skills/documentation-sync/SKILL.md`. Si no está instalada, lee la fuente correspondiente en `.aikya/runtime/template/.claude/skills/documentation-sync/SKILL.md` (scope proyecto) o `~/.claude/aikya-harnes/template/.claude/skills/documentation-sync/SKILL.md` (scope global).
2. Sigue las instrucciones técnicas especializadas de esa skill y las reglas del proyecto; no te limites a invocarla, ejecuta el flujo dentro de Claude Code.
3. Para scaffolding ejecuta `/aikya-scaffold`; para documentar ejecuta `/aikya-docs`; para pruebas ejecuta `/aikya-tests`.
4. Devuelve resultados realmente observados y pendientes. No uses herramientas externas automáticamente ni delegues sin motivo.

Si la petición afecta skills de Claude Code, sincroniza `docs/skills.md` sin registrar como ejecutadas las skills sólo disponibles.
