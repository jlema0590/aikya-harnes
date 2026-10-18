---
name: aikya-skills-status
description: Gestiona desde Claude Code skills externas Ponytail, Graphify y UI UX Pro Max: estado, plan e instalación autorizada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-skills-status

Argumentos de la petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Comprueba el perfil e inventario actual. Ejecuta `python3 scripts/harness/external_skills.py status` desde el proyecto; se actualizará `docs/skills.md` si está generado por Aikya.
2. Describe skills habilitadas del proyecto, externas ausentes, fallidas y origen. Nunca confundas **disponible** con **ejecutada**.
3. No descargues ni instales nada ni leas instrucciones completas de skills ajenas para esta consulta.
