---
name: aikya-skills-install
description: Gestiona desde Claude Code skills externas Ponytail, Graphify y UI UX Pro Max: estado, plan e instalación autorizada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-skills-install

Argumentos de la petición: `$ARGUMENTS`.
## Resolución y seguridad
- Trabaja en el directorio de proyecto abierto por Claude Code, NUNCA dentro del runtime global. Si falta `.harness/project-profile.json`, indica `/aikya-init` o `/aikya-answers` antes de continuar.
- No descargues dependencias, modifiques el SDK, realices despliegues, commits ni pushes sin autorización explícita. Conserva archivos y configuraciones ajenas.
- Lee sólo el perfil, los archivos directamente relacionados y las reglas estrictamente necesarias; evita grandes volcados de contexto.

1. Lee `aikya/docs/skills.md` si existe y el perfil del proyecto. Presenta un plan con fuentes, skills seleccionadas, ubicación, efectos y riesgos; verifica los repositorios de terceros antes de confiar en ellos.
2. **Obtén autorización explícita** antes de cada instalación o descarga. Para predefinidas (Ponytail, Graphify y UI UX Pro Max cuando corresponda) permite seleccionar `--only ponytail,graphify` u otras concretas; no instales otras por defecto cuando la solicitud fue específica.
3. Para una **skill nueva de GitHub**, confirma URL HTTPS `github.com/propietario/repositorio`, nombre del comando, ruta relativa de su carpeta y referencia Git. Ejecuta, sólo con aprobación, `python3 aikya/scripts/harness/external_skills.py install --yes --repo <url> --skill-path <ruta> --name <nombre> --ref <rama-o-tag>`; preferir commit verificado con `--commit <sha40>` si se ha fijado. No evalúes scripts de instalación adicionales y no sobrescribas skills existentes.
4. Para predefinidas, ejecuta `python3 aikya/scripts/harness/external_skills.py install --yes` sólo para las integraciones autorizadas. Nunca actualices SDK ni dependencias indirectas ocultas.
5. Tras instalar, verifica `python3 aikya/scripts/harness/external_skills.py status`, valida formato con `/aikya-quality` y comprueba que `aikya/docs/skills.md` registre **cada skill disponible en el proyecto** y el estado real (instalada, faltante o fallida), origen y finalidad. Si la documentación está personalizada, solicita editarla de manera conservadora.
6. Si se modifica configuración o código, registra el cambio en `aikya/docs/changes/REQ-*.md`. No afirmes que una skill se ejecutó porque esté instalada; no reindexes Graphify automáticamente.

## Instalación de un especialista del catálogo técnico de Aikya

- Si la petición pide una skill o agente del catálogo **incluido con Aikya**, previsualiza los nombres solicitados con `python3 aikya/scripts/harness/engineering_catalog.py plan --root . --names nombre1,nombre2`.
- Tras autorización explícita, utiliza `python3 aikya/scripts/harness/engineering_catalog.py install --root . --names nombre1,nombre2 --approved` desde el proyecto. Esta vía NO requiere red y conserva las personalizaciones.
- Si se solicitan todos los recomendados para el stack actual, usa `plan --root .` y, tras aprobación, `install --root . --approved`.
- Revisa `aikya/docs/agents.md`, `aikya/docs/skills.md` y `.harness/engineering-catalog.json` tras ejecutar; conserva documentación personalizada. No confundas disponibilidad con invocación real.
- No instales materiales de LinkedIn, derecho digital, SaaS ni propiedad intelectual desde el ZIP original.

- Las especialidades de lenguajes (Java, .NET, Python, React, Angular, Kotlin) y arquitecturas se componen por separado según el perfil; no presupongas microservicios ni event-driven.
