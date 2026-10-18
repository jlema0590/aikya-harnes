---
name: aikya-skills-plan
description: Gestiona desde Claude Code skills externas Ponytail, Graphify y UI UX Pro Max: estado, plan e instalación autorizada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-skills-plan

Argumentos de la petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Ejecuta `python3 scripts/harness/external_skills.py plan`; muestra las integraciones conocidas, fuentes y riesgos.
2. Si se solicita una **nueva skill de GitHub**, confirma URL pública HTTPS de GitHub, carpeta interna con SKILL.md, nombre propuesto y ref/commit antes de sugerir instalación. Lee/revisa las instrucciones y código de la fuente si es accesible.
3. Evalúa necesidad por stack, coste de contexto, permisos y condiciones de licencia. No instales ni descargues automáticamente.
4. Sugiere `/aikya-skills-install` para la instalación aprobada, `/aikya-skills-status` para consultar inventario.

## Catálogo técnico Aikya integrado (sin descargas)

- Además de terceros, lista los **26 playbooks técnicos y 23 especialistas** incluidos en Aikya con `python3 scripts/harness/engineering_catalog.py list`.
- Para mostrar qué especialistas corresponden al stack ya entrevistado, ejecuta `python3 scripts/harness/engineering_catalog.py plan --root .`; no modifica el proyecto.
- El catálogo instala sólo los componentes pertinentes a frontend, backend, Flutter, Docker, CI/CD o Cloud. Evita precargar skills no usadas para reducir contexto.
- **Excluidos** de este catálogo: LinkedIn, derecho digital, contratos SaaS y propiedad intelectual. No sugieras recuperarlos desde el paquete original.

- Las especialidades de lenguajes (Java, .NET, Python, React, Angular, Kotlin) y arquitecturas se componen por separado según el perfil; no presupongas microservicios ni event-driven.
