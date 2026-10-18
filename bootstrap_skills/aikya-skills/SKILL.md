---
name: aikya-skills
description: Gestiona desde Claude Code skills externas Ponytail, Graphify y UI UX Pro Max: estado, plan e instalación autorizada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-skills

Argumentos admitidos: `$ARGUMENTS` = `status` (predeterminado), `plan` o `install`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Obtén el perfil activo y determina qué skills corresponden al stack: Ponytail y Graphify si aportan valor; UI UX Pro Max sólo en proyectos con frontend o móvil. No cargues por defecto las instrucciones extensas de las skills.
2. Comprueba que está `scripts/harness/external_skills.py`; si falta, ejecuta `/aikya-init` para configurar el proyecto. Para `status`, ejecuta `python3 scripts/harness/external_skills.py status` y resume sólo faltantes/estado.
3. Para `plan`, ejecuta `python3 scripts/harness/external_skills.py plan`. Explica proveedor, fuente, descargas, modificaciones y riesgos. Revisa el código y origen externo antes de confiar en él.
4. Para `install`, muestra el plan y **obtén autorización explícita** para cada grupo de instaladores. Sólo después ejecuta `python3 scripts/harness/external_skills.py install --yes` desde la raíz y presenta fallos por skill. `--yes` únicamente representa autorización previamente dada por el usuario en Claude.
5. Nunca instales en segundo plano, cargues índices Graphify enteros en contexto ni generes/reindexes grafos automáticamente. No registres credenciales. Tras instalar, verifica `status`, usa `/aikya-quality` para validar el formato y documenta cambios de configuración relevantes en `docs/harness/` y `docs/changes/`.
