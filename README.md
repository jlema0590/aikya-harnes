# Aikya Harness

**One engineering workflow. Multiple AI agents. Consistent quality.**

Aikya Harness es un entorno de ingeniería asistida por IA para **Claude Code**. Reúne entrevista técnica, bootstrap y scaffolding de aplicaciones, agentes especializados, Agent Skills, controles de calidad, pruebas y documentación viva por petición. Funciona con backend Java, .NET, Node.js, Next.js y Python; frontend React, Vue y Angular; y aplicaciones Android, iOS, Flutter o React Native.

> **Todo el flujo de usuario se inicia y se dirige desde Claude Code.** No necesitas ejecutar instaladores, verificadores ni generadores en una terminal externa. Claude utiliza los scripts internos del repositorio cuando corresponde, con tu autorización para las acciones que modifican el entorno o descargan dependencias.

## Organización de skills en el repositorio

- **`aikya-skills/`**: comandos nativos de operación de Aikya, como `/aikya-init`, `/aikya-skills-install` y `/aikya-quality`. Se registran desde Claude Code en modo global o proyecto.
- **`engineering/agents/`** y **`engineering/skills/`**: catálogo técnico especializado que Aikya activa de forma selectiva según las decisiones del proyecto.

El nombre anterior `bootstrap_skills/` se migra de forma conservadora al actualizar Aikya: se limpian sólo archivos gestionados y verificados, manteniendo intactas las personalizaciones.

## Aikya v5.8 — Tres tipos de proyecto desde /aikya-init

**Primera decisión obligatoria:** `project_type` = `development`, `infrastructure` o `devops`. Después pregunta si el repositorio es nuevo o existente (`mode`). Un perfil antiguo sin `project_type` sigue siendo `development`.

| Modo | Preguntas de inicialización | Artefactos |
|---|---|---|
| **Desarrollo** (`development`) | Stack, monorepo/singlerepo, arquitectura, calidad; infraestructura y DevOps opcionales | Aplicaciones donde corresponda, `aikya/`, infra opcional |
| **Infraestructura** (`infrastructure`) | Terraform/OpenTofu y/o Ansible, cloud/on-prem, entornos y restricciones | `infra/terraform/` o `infra/ansible/`, sin `apps/`, `packages/` ni `contracts/` |
| **DevOps** (`devops`) | Origen (código/imagen/chart/manifests), Docker y Compose opcionales, destino y Kubernetes | Dockerfile sólo si hay código verificable; Compose desde imagen; YAML, Helm **nuevo o existente** o Kustomize |

### Flujo común y autorizaciones

`/aikya-init` → escoger modo → nuevo/existente → entrevista específica → comprobar y guardar `.aikya/answers.json` → `/aikya-doctor` (sólo herramientas relevantes) → generar plan de sólo lectura → **autorizar creación** → `/aikya-infra-project generate` → `/aikya-infra-project validate` y `/aikya-quality`.

- Los modos Infrastructure y DevOps **no requieren backend, frontend ni móvil**; no ejecutan `/aikya-scaffold` ni generan tests de aplicación ficticios. Se mantiene `aikya/docs/`, `aikya/test/` y `aikya/scripts/` para el harness.
- **Terraform-only:** configuración modular y entornos sin ejecutar recursos cloud. **Ansible-only:** roles e inventarios sin contactos con servidores. Ambos son combinables dentro del modo Infrastructure.
- **DevOps con Docker/Compose:** si ya hay una imagen versionada, puede generar Compose sin crear Dockerfile. Para un Dockerfile desde fuentes, exige proyecto y runtime/lockfile/comando de inicio reales.
- **Kubernetes:** elegir exactamente un formato principal: YAML, Helm o Kustomize. Helm distingue `helm_chart_mode=create` y `helm_chart_mode=existing` con `helm_chart_path` relativo al proyecto. Un chart existente no se modifica automáticamente; se verifica con `helm lint`/`helm template` tras validar su ruta.
- Kubernetes desde una imagen existente **no exige Docker local**; requiere el motor de validación elegido (Helm/Kustomize/kubectl según el perfil), y no requiere Node o Java.
- No se realizan acciones remotas, instalaciones de dependencias, Terraform apply/destroy, playbooks sobre servidores, pushes ni despliegues Kubernetes sin autorización específica. Una validación estática nunca sustituye una prueba de despliegue.

Los especialistas se activan según el modo: Terraform/Ansible, Docker, Kubernetes, Helm/Kustomize, o lenguajes y arquitecturas sólo para Desarrollo. Se respeta el catálogo de 27 agentes y 29 skills.

## Infrastructure & DevOps desde Claude Code

La entrevista de `/aikya-init` incluye un bloque opcional **Infrastructure & DevOps** después de elegir stack, arquitectura y monorepo/singlerepo. Pregunta por proveedor (AWS, Azure, GCP, on-premise, híbrido), infraestructura como código (Terraform/OpenTofu), gestión de configuración con Ansible, Docker/Compose, Kubernetes y una sola estrategia de despliegue (**Helm, Kustomize o YAML nativo**). También confirma entornos, imagen y puerto cuando se conocen.

**Separación de carpetas:**
- `infra/terraform/`, `infra/ansible/`, `infra/helm/` o `infra/kubernetes/`: infraestructura desplegable del producto, sólo si fue seleccionada.
- `Dockerfile` y `.dockerignore`: junto a la aplicación existente (`apps/api`, `apps/web` o la raíz de un singlerepo); requieren runtime, lockfiles y comandos de aplicación confirmados.
- `compose.apps.yaml`: servicios de aplicaciones ya contenerizadas para desarrollo local; no equivale a un despliegue de producción.
- `aikya/docs/infrastructure/`: decisiones, plan y evidencias. `aikya/scripts/harness/infrastructure.py` es el generador/validador interno.

**Cómo funciona el flujo:**

1. `/aikya-init`: entrevista y perfil en `.aikya/answers.json`. El instalador crea el **plan** en `aikya/docs/infrastructure/plan.md` sin desplegar ni descargar nada.
2. `/aikya-doctor`: identifica herramientas y versiones seleccionadas; distingue errores de lectura (por ejemplo Node `v25.9.0`) de requisitos reales de compatibilidad.
3. `/aikya-scaffold`: genera código de aplicación sólo tras autorización. Entonces se conocen los manifiestos y scripts reales para contenerización.
4. `/aikya-infra-project plan`: muestra artefactos, dependencias, archivos ya existentes y bloqueos, sin modificar nada.
5. `/aikya-infra-project generate`: **solicita aprobación explícita** y crea únicamente archivos inexistentes. Se preservan configuraciones y manifiestos personalizados.
6. `/aikya-infra-project validate` y `/aikya-quality`: Terraform/OpenTofu fmt, sintaxis Ansible, Compose config, Helm lint/template o Kustomize build cuando las herramientas están disponibles. Una verificación local no prueba la infraestructura desplegada.

La incorporación de especialistas desde `engineering/agents/` y `engineering/skills/` es **selectiva**: se reutilizan `terraform-iac`, `docker-best-practices`, `kubernetes-operations`, `cicd-pipelines`; se añaden agentes de Terraform, Ansible, Helm y Kubernetes, y skills de Ansible, Helm y Kustomize. No se cargan perfiles innecesarios.

**Seguridad:** no se crean recursos cloud inventados, no se guardan secretos/credenciales o estados Terraform en Git y nunca se ejecuta Terraform apply/destroy, Ansible contra hosts, push de imágenes ni helm/kubectl contra clusters sin aprobación separada. Las plantillas sin imagen versionada, puerto o runtime probado permanecen como **pendientes**, no como validaciones satisfactorias.

### Ejemplos de infraestructura

Consulta `examples/next-react-terraform-helm/` (Next.js + React singlerepo con Terraform y Helm) y `examples/java-react-ansible-kustomize/` (monorepo Java/React con Ansible y Kustomize). Sus JSON son ejemplos de decisiones, no aplicaciones desplegadas.

## Elegir monorepo o singlerepo

Durante `/aikya-init` debes seleccionar la **topología del repositorio**; esta opción es independiente de la arquitectura Clean, monolítica, en capas, de microservicios o por eventos.

- **Monorepo:** genera `apps/`, `packages/` y `contracts/`. Aloja backend, frontend y clientes móviles en módulos independientes.
- **Singlerepo:** coloca la única aplicación **en la raíz**, sin crear `apps/`, `packages/`, `contracts/` ni un `package.json` artificial de workspaces. Es válido para Next.js + React integrado, backend-only, frontend-only y móvil único.
- **Múltiples aplicaciones:** selecciona monorepo (p. ej. Java + React independientes o dos aplicaciones nativas Android/iOS).
- **Proyectos existentes:** Aikya conserva el código y la organización encontrada; no mueve aplicaciones ni sobrescribe documentos propios.

En ambos modos, la estructura de Aikya en el proyecto queda unificada:

```text
aikya/
  docs/        # overview, roadmap, features, seguridad, ADR y bitácoras
  test/        # pruebas del propio harness
  scripts/     # validaciones, ingeniería y scaffolding
.claude/       # hooks y skills visibles para Claude Code
.aikya/        # runtime y respuestas locales del instalador
.harness/      # perfil, estados y manifiestos internos
```

En monorepo la app va a `apps/api`, `apps/web`, etc.; en singlerepo el scaffolding compatible prepara la app en un directorio temporal y copia a raíz sólo después de comprobar conflictos. Las comprobaciones de SDK siguen siendo obligatorias.

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
| `/aikya-skills-status` | Muestra skills disponibles y sincroniza `aikya/docs/skills.md`. | `/aikya-skills-status` |
| `/aikya-skills-plan` | Prepara un plan de integración y comprueba necesidades del stack. | `/aikya-skills-plan` |
| `/aikya-skills-install` | Instala skills autorizadas (incluidas **nuevas skills de GitHub** mediante URL HTTPS, nombre, carpeta y ref/commit), valida la procedencia y actualiza `aikya/docs/skills.md`. | `/aikya-skills-install Sólo Ponytail y Graphify` |

Al inicializar un proyecto se genera `aikya/docs/skills.md`, que inventaría las skills registradas en `.claude/skills/`, su disponibilidad y origen. La instalación de nuevas skills lo sincroniza; **estar disponible no implica haber sido ejecutada**. **Ejemplo para una skill nueva en Claude Code:**

> `/aikya-skills-install Quiero incorporar una skill desde https://github.com/ORGANIZACION/REPOSITORIO.git. Revisa primero su SKILL.md y licencia, identifica la carpeta skills/NOMBRE, verifica el commit exacto, explícame los permisos y solicita mi aprobación antes de instalarla. Registra el resultado en aikya/docs/skills.md.`

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

Cada cambio técnico debe revisar y actualizar **los documentos realmente afectados** de `aikya/docs/`: overview, roadmap, features, bugs, security, architecture/ADRs, design, operations, testing y `aikya/docs/skills.md` cuando se incorporen o retiren skills. El cambio se registra en `aikya/docs/changes/REQ-*.md` con evidencias ejecutadas. Los hooks de Aikya ayudan a detectar documentación faltante antes del cierre de una tarea; el contenido técnico sigue necesitando revisión.

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
- `aikya/docs/`: documentación viva, inventario `aikya/docs/skills.md`, ADRs, guías de operación y registro de cambios.
- `apps/`, `infra/` y configuración de CI: sólo cuando son adecuados para el stack y se autoriza el scaffold.

**Para empezar:** instala Aikya mediante una petición a Claude Code, ejecuta `/aikya-init` y continúa usando exclusivamente los comandos `/aikya-*` descritos aquí.

### Documentación adicional

- [Instalación y primeros pasos dentro de Claude Code](INSTALL_FROM_CLAUDE.md)
- [Auditoría de skills y política de contexto](SKILLS_AUDIT.md)
- [Historial de versiones](CHANGELOG.md)

## 8. Catálogo técnico de agentes y skills integrados

Aikya incorpora **27 agentes técnicos** y **29 Agent Skills especializadas**, integrados a partir de dos paquetes proporcionados para el proyecto (12 agentes/15 skills del paquete inicial y 11 agentes/11 skills adicionales). Se mantiene el `security-reviewer` existente de Aikya, sin crear un duplicado. **No se incluyen** agentes ni skills de LinkedIn, derecho digital, contratos SaaS o propiedad intelectual.

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

### Cómo funcionan `engineering/agents/` y `engineering/skills/`

**Separación de responsabilidades:** `aikya-skills/` contiene los comandos de control y orquestación (`/aikya-init`, `/aikya-feature`, `/aikya-skills-install`, etc.). `engineering/agents/` contiene subagentes que asumen una función especializada; `engineering/skills/` contiene métodos y checklists técnicos que un agente puede consultar o precargar. Una skill no sustituye a un subagente ni ejecuta código por sí sola.

**Selección y despliegue:** al confirmar la entrevista con `/aikya-init` o `/aikya-answers`, Aikya identifica el backend, frontend, móvil, arquitectura y patrones complementarios. El catálogo (`engineering_catalog.py`) selecciona los especialistas necesarios y los copia a `.claude/agents/` y `.claude/skills/` del proyecto. Se conservan los archivos personalizados. Los especialistas no seleccionados permanecen en el catálogo para instalarlos posteriormente con `/aikya-skills-install` **tras aprobación**. La instalación global mantiene el catálogo en el runtime compartido, pero no configura todos los repositorios automáticamente.

**Orquestación:** el agente principal coordina el flujo, el planificador o un arquitecto revisa diseños si hace falta, el desarrollador del lenguaje realiza los cambios, y los revisores comprueban calidad y seguridad. Los agentes de arquitectura importados están configurados para análisis en modo plan, mientras que los de desarrollo pueden editar según permisos y autorización. Los campos `skills:` de los agentes vinculan sus instrucciones técnicas; no hay necesidad de cargar las 29 skills en cada petición. La ejecución está sujeta a las herramientas y permisos efectivos de Claude Code.

**Arquitectura independiente del lenguaje:** un proyecto `java` con `architecture=clean` activa `java-developer`/`java-engineering` junto con `clean-architecture-architect`/`clean-architecture`. `modular-monolith` activa `monolith-architect` y `modular-monolith-architecture`; `microservices` activa su pareja correspondiente; `layered` también. El patrón `event-driven` se activa únicamente si el perfil lo solicita explícitamente en `architecture_patterns`, porque no equivale a usar microservicios. Un perfil `hexagonal` no se convierte silenciosamente en `clean`.

**Lenguajes adicionales:** se incluyen especialistas Java, .NET, Python, React, Angular y Kotlin. Java/.NET/React se activan según la entrevista; Kotlin se activa para Android nativo cuando procede. Python y Angular se han incorporado también a la entrevista, pero su scaffolding se documenta como **asistido/manual** hasta acordar generadores y versiones con el usuario. No se instalan dependencias de forma silenciosa.

| Dominio | Agentes | Skills |
|---|---|---|
| Arquitecturas | `clean-architecture-architect`, `layered-architecture-architect`, `monolith-architect`, `microservices-architect`, `event-driven-architect` | `clean-architecture`, `layered-architecture`, `modular-monolith-architecture`, `microservices-architecture`, `event-driven-architecture` |
| Lenguajes | `java-developer`, `dotnet-developer`, `python-developer`, `react-developer`, `angular-developer`, `kotlin-developer` | `java-engineering`, `dotnet-engineering`, `python-engineering`, `react-engineering`, `angular-engineering`, `kotlin-engineering` |

**Ejemplo dentro de Claude Code:** `/aikya-skills-plan Analiza el backend Java y el frontend React; recomiéndame los agentes de arquitectura y lenguaje, indicando cuáles ya están activos.` Luego `/aikya-skills-install Instala sólo los especialistas acordados. No sobrescribas los personalizados y sincroniza aikya/docs/agents.md y aikya/docs/skills.md.`

**Versiones y evidencias:** las skills no fijan por defecto versiones de los SDKs. Aikya debe contrastar los manifiestos reales, ejecutar `/aikya-doctor` y actualizar `aikya/docs/agents.md` y `aikya/docs/skills.md`. La disponibilidad no certifica invocación ni resultado de tests. Consulta [ENGINEERING_AUDIT.md](ENGINEERING_AUDIT.md) para las procedencias y limitaciones.

**Activación progresiva:** `/aikya-init` incorpora los componentes adecuados al stack. Los demás quedan en un catálogo local para activarse, con aprobación, mediante `/aikya-skills-install`. Esto reduce instrucciones irrelevantes y evita instalar una especialidad Cloud en un proyecto web sencillo. El catálogo local no requiere descargas; las Agent Skills externas conservan su flujo de consentimiento.

Ejemplos dentro de Claude Code:

> `/aikya-skills-plan Muéstrame las skills y agentes técnicos que convienen a este proyecto Next.js.`

> `/aikya-skills-install Instala también terraform-iac y cloud-security desde el catálogo Aikya; presenta el plan antes de proceder.`

> `/aikya-skills-status Comprueba los agentes y skills disponibles y actualiza aikya/docs/skills.md.`

La inicialización genera `aikya/docs/agents.md`, `aikya/docs/skills.md` y `.harness/engineering-catalog.json`, con procedencia y componentes instalados. Estar registrado no demuestra uso efectivo de un agente o skill. Los archivos personalizados existentes no se sobrescriben.

## 9. Ejemplos de entrevistas técnicas y perfiles por stack

Cada subcarpeta de `examples/` contiene `answers.json` (decisiones que valida Aikya) y `README.md` (cómo usarlas **desde Claude Code**, selección de especialistas y verificaciones). Son escenarios **simulados**, no aplicaciones compiladas ni desplegadas. Se conservan los ejemplos JSON anteriores para compatibilidad.

| Ejemplo | Contenido |
|---|---|
| [Next.js + React (aplicación nueva)](examples/next-react/README.md) | [`answers.json`](examples/next-react/answers.json) |
| [Spring Boot + React con Clean Architecture](examples/java-react-clean/README.md) | [`answers.json`](examples/java-react-clean/answers.json) |
| [ASP.NET Core + Vue (monolito modular)](examples/dotnet-vue/README.md) | [`answers.json`](examples/dotnet-vue/answers.json) |
| [Android nativo con Kotlin](examples/android-kotlin/README.md) | [`answers.json`](examples/android-kotlin/answers.json) |
| [FastAPI + Angular (aplicación nueva)](examples/python-angular/README.md) | [`answers.json`](examples/python-angular/answers.json) |
| [NestJS + React, microservicios y eventos](examples/node-react-microservices/README.md) | [`answers.json`](examples/node-react-microservices/answers.json) |
| [API Java existente (sin scaffolding destructivo)](examples/existing-java-api/README.md) | [`answers.json`](examples/existing-java-api/answers.json) |
| [Next.js + Terraform + Helm](examples/next-react-terraform-helm/README.md) | [`answers.json`](examples/next-react-terraform-helm/answers.json) |
| [Java/React + Ansible + Kustomize](examples/java-react-ansible-kustomize/README.md) | [`answers.json`](examples/java-react-ansible-kustomize/answers.json) |
| [infra-terraform-only](examples/infra-terraform-only/README.md) | [`answers.json`](examples/infra-terraform-only/answers.json) |
| [infra-ansible-only](examples/infra-ansible-only/README.md) | [`answers.json`](examples/infra-ansible-only/answers.json) |
| [devops-docker-compose](examples/devops-docker-compose/README.md) | [`answers.json`](examples/devops-docker-compose/answers.json) |
| [devops-helm-existing](examples/devops-helm-existing/README.md) | [`answers.json`](examples/devops-helm-existing/answers.json) |
| [devops-kustomize](examples/devops-kustomize/README.md) | [`answers.json`](examples/devops-kustomize/answers.json) |

**Uso:** abre Claude Code con Aikya instalado y solicita `/aikya-answers Usa las decisiones del ejemplo examples/next-react/answers.json, enséñame primero el plan y valida requisitos antes de generar código.` Cambia la ruta por otro ejemplo si lo necesitas. El desarrollador no tiene que ejecutar instaladores o scripts en una terminal externa.

### Pantalla de bienvenida

El hook `SessionStart` muestra un panel de bienvenida en sesiones nuevas de Claude Code, con el nombre del desarrollador (configuración local o Git) y el repositorio. La instalación global también saluda en proyectos ya inicializados; cuando hay hook local se evita duplicar la salida. Una instalación ejecutada en una sesión abierta **no lanza** el hook retroactivamente: abre una sesión nueva. Si no se visualiza, solicita a Claude que previsualice `welcome.py --preview` en modo lectura y comprueba el evento `SessionStart`.
