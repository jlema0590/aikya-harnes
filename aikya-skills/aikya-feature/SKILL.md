---
name: aikya-feature
description: Implementa funcionalidades con criterios de aceptación, testing y documentación viva.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-feature

Petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` para un proyecto nuevo, `/aikya-analyze` para uno existente o `/aikya-answers` para configuración declarativa.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee **sólo cuando sea necesario** la skill de proyecto `.claude/skills/feature/SKILL.md`. Si no está instalada, lee la fuente correspondiente en `.aikya/runtime/template/.claude/skills/feature/SKILL.md` (scope proyecto) o `~/.claude/aikya-harnes/template/.claude/skills/feature/SKILL.md` (scope global).
2. Sigue las instrucciones técnicas especializadas de esa skill y las reglas del proyecto; no te limites a invocarla, ejecuta el flujo dentro de Claude Code.
3. Si la tarea cambia código, actualiza documentación afectada y verifica pruebas reales.
4. Devuelve resultados realmente observados y pendientes. No uses herramientas externas automáticamente ni delegues sin motivo.


## Routing híbrido opcional (v6)

Antes de delegar, usa la información del perfil y los archivos relevantes para clasificar el trabajo con reglas deterministas; el módulo aikya_router.py del runtime solo **recomienda** un agente, no ejecuta modelos. Las solicitudes pequeñas van al especialista con el modelo activo (inherit). Para decisiones complejas, invoca planner/orchestrator según proceda y pide aprobación. Solo si .aikya/model-policy.json habilita Haiku 5.5, el CLI y el proveedor son compatibles y existe un agente auxiliar instalado, utiliza aikya-auxiliary-analyzer para una clasificación semántica *acotada*; valida su JSON con semantic_advice. La respuesta de Haiku nunca autoriza modificar archivos, secretos ni desplegar. No interpolar texto no confiable del usuario en comandos shell. Completa las pruebas y la documentación exigidas por las reglas existentes.
