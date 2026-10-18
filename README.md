# Aikya Harness

**One engineering workflow. Multiple AI agents. Consistent quality.**

Aikya Harness es un entorno de ingeniería asistida por IA para **Claude Code**. Reúne entrevista técnica, bootstrap y scaffolding de aplicaciones, agentes especializados, Agent Skills, controles de calidad, pruebas y documentación viva por petición. Funciona con backend Java, .NET, Node.js y Next.js; frontend React y Vue; y aplicaciones Android, iOS, Flutter o React Native.

> **Todo el flujo de usuario se inicia y se dirige desde Claude Code.** No necesitas ejecutar instaladores, verificadores ni generadores en una terminal externa. Claude utiliza los scripts internos del repositorio cuando corresponde, con tu autorización para las acciones que modifican el entorno o descargan dependencias.

## Organización de skills en el repositorio

- **`aikya-skills/`**: comandos nativos de operación de Aikya, como `/aikya-init`, `/aikya-skills-install` y `/aikya-quality`. Se registran desde Claude Code en modo global o proyecto.
- **`engineering/agents/`** y **`engineering/skills/`**: catálogo técnico especializado que Aikya activa de forma selectiva según las decisiones del proyecto.

El nombre anterior `bootstrap_skills/` se migra de forma conservadora al actualizar Aikya: se limpian sólo archivos gestionados y verificados, manteniendo intactas las personalizaciones.

## 1. Instalar Aikya desde Claude Code

Abre una conversación de **Claude Code** en la carpeta en la que quieras trabajar y envía esta solicitud. Puedes elegir **global** para habilitar los comandos en todos los proyectos, o **proyecto** para habilitarlos sólo en el repositorio actual.

> **Instala Aikya Harness** desde `https://github.com/jlema0590/aikya-harnes.git`, rama `develop`, en **modo global**. Revisa la fuente antes de instalar y pide mi aprobación para cualquier descarga o cambio de configuración. Registra sus skills, hooks y bienvenida, sin modificar otros repositorios ni instalar SDKs automáticamente. Después explícame cómo usar `/aikya-init`.

Para instalar en el repositorio actual sustituye **modo global** por **modo proyecto**.

- **Global**: registra los comandos `/aikya-*` en el perfil de Claude Code del usuario, mantiene el runtime compartido y no inicializa proyectos sin intervención.
- **Proyecto**: registra los mismos comandos en el repositorio actual y guarda el runtime local. No sobrescribe skills o configuraciones personalizadas.
- **Nuevo o existente**: tras el registro inicial, usa `/aikya-init` o `/aikya-answers` **dentro de Claude Code**. Si la sesión no detecta skills recién instaladas, inicia una nueva sesión de Claude Code.

El hook de bienvenida muestra el nombre configurado, el repositorio actual y un recordatorio de inicialización. Un hook de inicio no abre por sí mismo una conversación: el desarrollador debe elegir el comando.

## 2. Entrevista y decisiones técnicas

| Comando de Claude Code | Qué hace | Ejemplo en la conversación |
|---|---|---|
| `/aikya-init` | Entrevista técnica para aplicación nueva o existente; confirma tecnologías, arquitectura y despliegue. | `/aikya-init Quiero una API Java 21 con React` |
| `/aikya-answers` | Reutiliza decisiones de un archivo de respuestas aprobado. | `/aikya-answers .aikya/answers.json` |
| `/aikya-doctor` | Diagnostica SDKs, gestores y versiones requeridas sin modificarlas. | `/aikya-doctor Revisa si tengo el SDK .NET adecuado` |
| `/aikya-project-init` | Define alcance, estructura, roadmap y ADR inicial. | `/aikya-project-init Planifica una API de inventario` |

Claude pregunta únicamente por las decisiones que faltan, inspecciona la estructura de un proyecto existente y muestra el resumen antes de aplicar cambios. Valida versiones de JDK, .NET, Node.js, gestores de paquetes, Android SDK, Xcode y Flutter según el stack escogido. **Si falta un requisito, el scaffold se detiene** hasta que lo resuelvas con autorización; nunca se actualizan SDKs de forma silenciosa.

## 3. Inicialización y scaffolding de aplicaciones

| Comando de Claude Code | Qué hace | Ejemplo en la conversación |
|---|---|---|
| `/aikya-scaffold` | Previsualiza y, con aprobación, ejecuta generadores oficiales por módulo. | `/aikya-scaffold Planifica backend .NET y frontend Vue` |
| `/aikya-infra-project` | Completa contratos, infraestructura inicial, CI, observabilidad y quality gates después del scaffold. | `/aikya-infra-project Configura el proyecto recién generado` |

**Flujo recomendado:** `/aikya-init` → `/aikya-doctor` → `/aikya-scaffold plan` → revisar el plan y autorizar su ejecución → `/aikya-infra-project` → `/aikya-quality`.

Aikya nunca asume que un generador externo, un build o un pipeline de CI se ejecutó correctamente por el hecho de estar configurado. Los proyectos existentes se amplían de manera incremental: no se ejecuta un scaffold destructivo sobre su estructura.

## 4. Gestión de Agent Skills externas

La integración de terceros es **optativa y supervisada**: [Ponytail](https://github.com/DietrichGebert/ponytail), [Graphify](https://github.com/Graphify-Labs/graphify) (CLI local, sin MCP) y [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) para trabajos de interfaz.

| Comando de Claude Code | Qué hace | Ejemplo en la conversación |
|---|---|---|
| `/aikya-skills-status` | Muestra skills disponibles y sincroniza `docs/skills.md`. | `/aikya-skills-status` |
| `/aikya-skills-plan` | Prepara un plan de integración y comprueba necesidades del stack. | `/aikya-skills-plan` |
| `/aikya-skills-install` | Instala skills autorizadas (incluidas **nuevas skills de GitHub** mediante URL HTTPS, nombre, carpeta y ref/commit), valida la procedencia y actualiza `docs/skills.md`. | `/aikya-skills-install Sólo Ponytail y Graphify` |

Al inicializar un proyecto se genera `docs/skills.md`, que inventaría las skills registradas en `.claude/skills/`, su disponibilidad y origen. La instalación de nuevas skills lo sincroniza; **estar disponible no implica haber sido ejecutada**. **Ejemplo para una skill nueva en Claude Code:**

> `/aikya-skills-install Quiero incorporar una skill desde https://github.com/ORGANIZACION/REPOSITORIO.git. Revisa primero su SKILL.md y licencia, identifica la carpeta skills/NOMBRE, verifica el commit exacto, explícame los permisos y solicita mi aprobación antes de instalarla. Registra el resultado en docs/skills.md.`

**Ejemplo para consultar el inventario:** `/aikya-skills-status Revisa las skills del proyecto y su origen.`

La selección es contextual para no cargar instrucciones innecesarias. Graphify trabaja con consultas concretas, no con volcados completos del grafo. No se descarga ni indexa nada de forma automática al iniciar Claude Code. Consulta [SKILLS_AUDIT.md](SKILLS_AUDIT.md) para criterios de compatibilidad y carga progresiva.

## 5. Calidad, documentación viva y pruebas

| Comando de Claude Code | Qué hace | Ejemplo en la conversación |
|---|---|---|
| `/aikya-quality` | Ejecuta quality gates, lint de skills, revisión documental y controles pertinentes. | `/aikya-quality Revisa el estado del proyecto` |
| `/aikya-tests` | Ejecuta pruebas focalizadas o de regresión según el stack. | `/aikya-tests Ejecuta los tests del módulo login` |
| `/aikya-docs` | Actualiza documentación afectada y bitácora por petición. | `/aikya-docs Documenta la autenticación JWT` |
| `/aikya-documentation-sync` | Comando histórico compatible para sincronización documental. | `/aikya-documentation-sync Revisa la documentación de seguridad` |
| `/aikya-verify` | Comando histórico compatible de validación integral. | `/aikya-verify Comprueba la última feature` |

Cada cambio técnico debe revisar y actualizar **los documentos realmente afectados** de `docs/`: overview, roadmap, features, bugs, security, architecture/ADRs, design, operations, testing y `docs/skills.md` cuando se incorporen o retiren skills. El cambio se registra en `docs/changes/REQ-*.md` con evidencias ejecutadas. Los hooks de Aikya ayudan a detectar documentación faltante antes del cierre de una tarea; el contenido técnico sigue necesitando revisión.

Un check requerido que no está configurado, falla o no pudo ejecutarse se informa como **NO VERIFICADO** o **FALLÓ**; nunca se declara aprobado por omisión.

## 6. Skills de desarrollo invocables desde Claude Code

| Comando de Claude Code | Qué hace | Ejemplo en la conversación |
|---|---|---|
| `/aikya-feature` | Implementa funcionalidad con criterios de aceptación y pruebas. | `/aikya-feature Crea GET /health` |
| `/aikya-bugfix` | Reproduce y corrige un error con pruebas de regresión. | `/aikya-bugfix Corrige el error 401 del login` |
| `/aikya-architecture-review` | Revisa límites de módulos, contratos y decisiones arquitectónicas. | `/aikya-architecture-review Revisa la división de servicios` |
| `/aikya-mobile-feature` | Desarrolla cambios Android/iOS con requisitos nativos. | `/aikya-mobile-feature Añade login biométrico en Android` |

Todas las skills anteriores están disponibles como **comandos de Claude Code** después del bootstrap global o local. Los proyectos inicializados incluyen también las skills originales sin prefijo (por compatibilidad). Los comandos de desarrollo comprueban la inicialización del repositorio antes de actuar.

## 7. Cómo se organiza un proyecto Aikya

Tras la entrevista y la instalación aprobada, Aikya crea o completa la estructura del proyecto conservando los archivos que ya existen:

- `.claude/`: agentes, skills, reglas y hooks de Claude Code.
- `.aikya/`: decisiones de entrevista y runtime local cuando corresponda.
- `.harness/` y `harness.json`: perfil técnico, estado de petición y controles de calidad.
- `docs/`: documentación viva, inventario `docs/skills.md`, ADRs, guías de operación y registro de cambios.
- `apps/`, `infra/` y configuración de CI: sólo cuando son adecuados para el stack y se autoriza el scaffold.

**Para empezar:** instala Aikya mediante una petición a Claude Code, ejecuta `/aikya-init` y continúa usando exclusivamente los comandos `/aikya-*` descritos aquí.

### Documentación adicional

- [Instalación y primeros pasos dentro de Claude Code](INSTALL_FROM_CLAUDE.md)
- [Auditoría de skills y política de contexto](SKILLS_AUDIT.md)
- [Historial de versiones](CHANGELOG.md)

## 8. Catálogo técnico de agentes y skills integrados

Aikya incorpora **12 subagentes técnicos nuevos** y **15 Agent Skills especializadas**, adaptados de un paquete de desarrollo proporcionado para el proyecto. Se mantiene el `security-reviewer` existente de Aikya, sin crear un duplicado. **No se incluyen** agentes ni skills de LinkedIn, derecho digital, contratos SaaS o propiedad intelectual.

| Dominio | Agentes disponibles | Skills relevantes |
|---|---|---|
| Coordinación y planificación | `planner`, `orchestrator` | Reutiliza el flujo de Aikya |
| Node.js / APIs | `node-backend-developer` | `node-api-design` |
| Next.js | `nextjs-developer` | `nextjs-architecture` |
| Vue 3 | `vue-developer` | `vue-architecture` |
| Flutter | `flutter-developer` | `flutter-architecture` |
| Astro | `astro-tailwind-developer` | `astro-performance` |
| Calidad | `code-reviewer`, `test-engineer` | `code-review`, `testing-strategy`, `security-audit` |
| Infraestructura y Cloud | `cicd-engineer`, `docker-developer`, `cloud-architect` | `cicd-pipelines`, `docker-best-practices`, `kubernetes-operations`, `cloud-architecture` |
| Especialidades opcionales | Agentes existentes según perfil | `terraform-iac`, `cloud-security`, `finops-optimization` |

**Activación progresiva:** `/aikya-init` incorpora los componentes adecuados al stack. Los demás quedan en un catálogo local para activarse, con aprobación, mediante `/aikya-skills-install`. Esto reduce instrucciones irrelevantes y evita instalar una especialidad Cloud en un proyecto web sencillo. El catálogo local no requiere descargas; las Agent Skills externas conservan su flujo de consentimiento.

Ejemplos dentro de Claude Code:

> `/aikya-skills-plan Muéstrame las skills y agentes técnicos que convienen a este proyecto Next.js.`

> `/aikya-skills-install Instala también terraform-iac y cloud-security desde el catálogo Aikya; presenta el plan antes de proceder.`

> `/aikya-skills-status Comprueba los agentes y skills disponibles y actualiza docs/skills.md.`

La inicialización genera `docs/agents.md`, `docs/skills.md` y `.harness/engineering-catalog.json`, con procedencia y componentes instalados. Estar registrado no demuestra uso efectivo de un agente o skill. Los archivos personalizados existentes no se sobrescriben.
