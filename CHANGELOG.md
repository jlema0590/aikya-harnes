# Changelog

## v5.9.0 — 2026-10-19

- Corregido `/aikya-infra-project validate` con Helm cuando la raíz del proyecto llega por un symlink (p. ej. `/var` → `/private/var` en macOS): ya no falla con `ValueError`. Los charts enlazados fuera del proyecto se rechazan como NOT_CONFIGURED.

- README reorganizado: inicio rápido, referencia única de comandos, catálogo completo de 27 agentes y 29 skills, y un solo apartado de seguridad.
- `INSTALL_FROM_CLAUDE.md` integrado en el README; auditorías movidas a `docs/audits/`.
- Eliminadas copias obsoletas de `/aikya-init`, `/aikya-answers` y `/aikya-doctor` en `.claude/skills/` del repositorio y el ejemplo sin uso `examples/existing-api.json`.

## v5.8.0 — 2026-10-18

- `/aikya-init`: primera selección `project_type` development, infrastructure o devops; luego nuevo/existente.
- Modo infrastructure sin SDKs de aplicación; Terraform/OpenTofu/Ansible individuales o combinados.
- Modo devops independiente: Docker/Compose desde código o imagen; Kubernetes con YAML, Helm (nuevo o reutilizado) y Kustomize.
- Kubernetes con chart/imagen existente no exige Docker local; perfiles legacy sin project_type siguen en development.
- Quality gates y documentación de infraestructura sin carpetas `apps/` ni tests ficticios; selección de agentes por especialidad.
- Plan de solo lectura, generación con aprobación y validación local; sin desplegar automáticamente.
- Nuevos ejemplos y regresiones de los tres modos.


## v5.7.0 — 2026-10-18

- Solucionado el parser de Node: detecta correctamente `v25.9.0` y otras versiones con prefijo `v`.
- Actualización segura de requisitos en runtime: copias gestionadas se migran; se conserva backup v5.6 y contenido personalizado.
- Perfil `infrastructure` opcional y validado en la entrevista técnica (provider, Terraform/OpenTofu, Ansible, Docker/Compose, Kubernetes con Helm/Kustomize/YAML, entornos, imagen y puerto).
- Cuatro agentes y tres skills de ingeniería añadidos; catálogo activado por selección explícita.
- Generador de infraestructura sin despliegue: `plan`, `generate --approved`, `validate` con protección de archivos.
- Dockerfile derivado del código real y runtime fijado; Kubernetes exige imagen versionada y puerto confirmado.
- Documentación viva, quality gates y ejemplos con Terraform/Helm y Ansible/Kustomize; pruebas automatizadas ampliadas.


## v5.6.0 — 2026-10-18

- Selección explícita de monorepo/singlerepo en entrevista y respuestas JSON.
- Sólo monorepo crea apps/, packages/ y contracts/. Singlerepo genera una aplicación en raíz mediante staging.
- Aikya concentra documentación, pruebas y scripts en aikya/docs/, aikya/test/ y aikya/scripts/.
- Bienvenida global en proyectos nuevos y existentes, sin duplicados cuando existe hook local.
- Migración conservadora de documentación previa y actualización de quality gates.


## v5.5.0 — 2026-10-18

- Se integran 11 agentes y 11 Agent Skills adicionales de lenguajes y arquitecturas dentro de `engineering/`.
- El catálogo tiene 23 agentes y 26 skills, selección por backend/frontend/Android y arquitectura/patrones explícitos.
- Se incorporan Python y Angular a la entrevista y detección; el scaffolding se mantiene guiado hasta validar generadores.
- Se añaden 7 ejemplos por stack con `answers.json` y README de uso desde Claude Code.
- Documentación de responsabilidades, activación selectiva, trazabilidad y auditoría ampliada.


## v5.4.0 — 2026-10-18 — Organización de comandos Aikya

- Renombrada la carpeta fuente `bootstrap_skills/` a `aikya-skills/`; sin cambios en los nombres de los comandos `/aikya-*`.
- Actualizados el bootstrap global/proyecto, el instalador y la documentación para usar la nueva ruta.
- Migración conservadora de runtimes existentes: se retiran sólo archivos legacy previamente gestionados y verificados; se conserva contenido personalizado.
- Pruebas de instalación limpia, actualización en ambos alcances y protección de contenido ajeno.

## v5.2.0 — 2026-10-18

- Renombrados comandos: `/aikya-infra-project`, `/aikya-skills-status`, `/aikya-skills-plan`, `/aikya-skills-install`.
- `/aikya-skills-install` admite skills GitHub adicionales con verificación de origen, ruta, nombre y commit opcional; sin sobrescribir.
- Nuevo `aikya/docs/skills.md`, inventario de skills disponibles del proyecto; generado en la entrevista y sincronizado tras instalaciones/estado.
- Migración conservadora de comandos renombrados; se preservan personalizaciones.


## v5.1.0 — 2026-10-18 — comandos Claude-native

- Comandos `/aikya-scaffold`, `/aikya-skills-status`, `/aikya-quality`, `/aikya-docs` y `/aikya-tests`, además de los comandos de desarrollo ya disponibles, invocables desde Claude Code.
- El bootstrap global/proyecto expone 16 skills de Aikya, todas con ejecución conversacional y autorización para acciones externas; conserva las skills personalizadas.
- README reorganizado para explicar sólo instalación y uso desde Claude Code: sin comandos manuales de Python, shell ni scaffolding fuera de Claude.
- Se preservan scripts internos y documentación viva obligatoria; validación de SDK antes de generar aplicaciones.


## v5.0.0 — 2026-10-18

- Instalación conversacional en Claude Code con scopes global/proyecto y comandos /aikya-init, /aikya-answers, /aikya-doctor.
- Prefijos Aikya para los ocho workflows existentes sin eliminar aliases antiguos.
- Preflight no destructivo de Java JDK, .NET SDK, Node.js, gestores web y SDKs móviles; guía oficial de actualización y bloqueo de scaffold sin requisitos.
- Hook SessionStart global/proyecto que invita automáticamente a /aikya-init en directorios no inicializados, sin iniciar turnos ni ejecutar descargas.
- Reutilización de perfiles JSON, onboarding global sin modificar proyectos, y referencia de instalación desde URL GitHub.
- Suite de pruebas de bootstrap y diagnóstico técnico.

## v4.1.0 — 2026-10-18

- Bienvenida al iniciar Claude Code con panel de texto, nombre local configurable, repositorio detectado y URL de Aikya.
- Hook `SessionStart` no intrusivo: mensaje visible al usuario sin añadir contexto al modelo, sin red y sin avisos en compactación.
- Soporte `--display-name` y `welcome_name` en `--answers`, identidad local ignorada por Git.
- README: referencia completa de comandos CLI y las ocho skills propias, cada una con ejemplo; vista previa del saludo.
- Hooks de bienvenida tanto para el propio repositorio Aikya como para proyectos instalados.

## v4.0.0 — 2026-10-18

- Entrevista y bootstrap v3 conservados: Java, .NET, Node, Next, Vue, React, Android, iOS y multiplataforma.
- Integración autorizada por el usuario de Ponytail, Graphify CLI sin MCP y UI UX Pro Max condicional por stack.
- `SessionStart` verifica skills sin red ni reindexación; gestora `external_skills.py` para plan/install/status.
- Verificador básico de Agent Skills, audit y reglas de carga progresiva para ahorrar tokens.
- `aikya/docs/design/design-system.md` condicional y validación documental de cambios de UI.
- Migración segura de archivos v3 originales con respaldo; archivos personalizados preservados.
- Suite de 32 pruebas automatizadas locales; se requieren pruebas externas en equipo con red.

## v3.0.0 — 2026-10-18

- Engineering Bootstrap, entrevista, scaffold asistido, infraestructura y documentación viva con hooks de trazabilidad.