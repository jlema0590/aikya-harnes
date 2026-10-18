# Changelog

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
