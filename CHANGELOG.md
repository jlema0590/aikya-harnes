# Changelog

## v5.2 — 2026-10-18

- Renombrados comandos: `/aikya-infra-project`, `/aikya-skills-status`, `/aikya-skills-plan`, `/aikya-skills-install`.
- `/aikya-skills-install` admite skills GitHub adicionales con verificación de origen, ruta, nombre y commit opcional; sin sobrescribir.
- Nuevo `docs/skills.md`, inventario de skills disponibles del proyecto; generado en la entrevista y sincronizado tras instalaciones/estado.
- Migración conservadora de comandos renombrados; se preservan personalizaciones.


## v5.1 — comandos Claude-native

- Comandos `/aikya-scaffold`, `/aikya-skills-status`, `/aikya-quality`, `/aikya-docs` y `/aikya-tests`, además de los comandos de desarrollo ya disponibles, invocables desde Claude Code.
- El bootstrap global/proyecto expone 16 skills de Aikya, todas con ejecución conversacional y autorización para acciones externas; conserva las skills personalizadas.
- README reorganizado para explicar sólo instalación y uso desde Claude Code: sin comandos manuales de Python, shell ni scaffolding fuera de Claude.
- Se preservan scripts internos y documentación viva obligatoria; validación de SDK antes de generar aplicaciones.


## v5 — 2026-10-18

- Instalación conversacional en Claude Code con scopes global/proyecto y comandos /aikya-init, /aikya-answers, /aikya-doctor.
- Prefijos Aikya para los ocho workflows existentes sin eliminar aliases antiguos.
- Preflight no destructivo de Java JDK, .NET SDK, Node.js, gestores web y SDKs móviles; guía oficial de actualización y bloqueo de scaffold sin requisitos.
- Hook SessionStart global/proyecto que invita automáticamente a /aikya-init en directorios no inicializados, sin iniciar turnos ni ejecutar descargas.
- Reutilización de perfiles JSON, onboarding global sin modificar proyectos, y referencia de instalación desde URL GitHub.
- Suite de pruebas de bootstrap y diagnóstico técnico.

## v4.1 — 2026-10-18

- Bienvenida al iniciar Claude Code con panel de texto, nombre local configurable, repositorio detectado y URL de Aikya.
- Hook `SessionStart` no intrusivo: mensaje visible al usuario sin añadir contexto al modelo, sin red y sin avisos en compactación.
- Soporte `--display-name` y `welcome_name` en `--answers`, identidad local ignorada por Git.
- README: referencia completa de comandos CLI y las ocho skills propias, cada una con ejemplo; vista previa del saludo.
- Hooks de bienvenida tanto para el propio repositorio Aikya como para proyectos instalados.

## v4 — 2026-10-18

- Entrevista y bootstrap v3 conservados: Java, .NET, Node, Next, Vue, React, Android, iOS y multiplataforma.
- Integración autorizada por el usuario de Ponytail, Graphify CLI sin MCP y UI UX Pro Max condicional por stack.
- `SessionStart` verifica skills sin red ni reindexación; gestora `external_skills.py` para plan/install/status.
- Verificador básico de Agent Skills, audit y reglas de carga progresiva para ahorrar tokens.
- `docs/design/design-system.md` condicional y validación documental de cambios de UI.
- Migración segura de archivos v3 originales con respaldo; archivos personalizados preservados.
- Suite de 32 pruebas automatizadas locales; se requieren pruebas externas en equipo con red.

## v3

- Engineering Bootstrap, entrevista, scaffold asistido, infraestructura y documentación viva con hooks de trazabilidad.

## v5.3 — Integración de catálogo técnico

- Revisados 19 agentes y 21 skills del ZIP externo del usuario. Excluidos 6 agentes jurídicos, 6 skills jurídicas y todos los componentes de LinkedIn.
- Integrados 12 agentes nuevos y 15 skills técnicas; se conserva el agente de seguridad ya presente en Aikya.
- Activación progresiva según stack y gestión mediante `/aikya-skills-plan`, `/aikya-skills-install` y `/aikya-skills-status` dentro de Claude Code.
- Nuevo `docs/agents.md` junto al inventario existente `docs/skills.md`, y auditoría en `ENGINEERING_AUDIT.md`.
- Integración idempotente que evita sobrescrituras y no ejecuta contenido ajeno.
