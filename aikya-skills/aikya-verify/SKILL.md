---
name: aikya-verify
description: Ejecuta verificaciones técnicas y quality gates en Claude Code.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-verify

Petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee **sólo cuando sea necesario** la skill de proyecto `.claude/skills/verify/SKILL.md`. Si no está instalada, lee la fuente correspondiente en `.aikya/runtime/template/.claude/skills/verify/SKILL.md` (scope proyecto) o `~/.claude/aikya-harnes/template/.claude/skills/verify/SKILL.md` (scope global).
2. Sigue las instrucciones técnicas especializadas de esa skill y las reglas del proyecto; no te limites a invocarla, ejecuta el flujo dentro de Claude Code.
3. Para scaffolding ejecuta `/aikya-scaffold`; para documentar ejecuta `/aikya-docs`; para pruebas ejecuta `/aikya-tests`.
4. Devuelve resultados realmente observados y pendientes. No uses herramientas externas automáticamente ni delegues sin motivo.

## Infrastructure & DevOps

- Si `infrastructure` está configurado y existen artefactos, ejecuta `python3 aikya/scripts/harness/infrastructure.py validate` además de los gates habituales. Distingue NOT_CONFIGURED de éxito. No accedas a clusters, cloud ni servidores durante checks locales.
- Documenta las evidencias en `aikya/docs/operations/deployment.md` y `aikya/docs/infrastructure/`.

## Comprobaciones SDD v6.0.0

Si el perfil tiene `methodology=sdd`:
- Ejecuta `python3 aikya/scripts/harness/sdd_engine.py lint --root .` para detectar evidencias no existentes y referencias inconsistentes.
- Para SPEC-NNN, usa `/aikya-sdd-status` y registra sólo comandos ejecutados y archivos de evidencia reales. El estado EVIDENCE_RECORDED no equivale a un certificado independiente ni a despliegue exitoso.
- Nunca declares todos los requisitos verificados si hay tareas incompletas, checks sin ejecutar o resultado failed.
