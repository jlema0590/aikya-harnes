# Aikya Harness — Engineering Bootstrap, Agent Skills y Documentación viva

> One engineering workflow. Multiple AI agents. Consistent quality.

**Aikya Harness v4.1** es un framework de ingeniería asistida por IA para Claude Code.



Harness de desarrollo para Claude Code. Entrevista técnica, instalación reproducible, perfiles de backend/frontend/móvil, scaffolding asistido con generadores oficiales, infraestructura inicial y documentación viva por petición. **Sin MCP** y **Python 3.9+** para el instalador, hooks y verificadores. Las integraciones de terceros requieren Git, uv/pipx o Node/npm según la herramienta, red y aprobación explícita.

## Novedades v4.1 — bienvenida a Aikya Harness

Al abrir `claude` en este repositorio o en cualquier proyecto donde hayas instalado Aikya, el hook de inicio presenta un mensaje con la identidad local, el repositorio actual, el enlace al proyecto original y los comandos más habituales:

```text
+-------------------------------------------------------------+
| Bienvenido a Aikya Harness                                  |
| Desarrollador: Juan                                         |
| Repositorio: jlema0590/aikya-harnes                         |
| Proyecto Aikya: https://github.com/jlema0590/aikya-harnes   |
| Comandos: /feature · /bugfix · /verify · /project-bootstrap |
| Guía completa: README.md                                    |
+-------------------------------------------------------------+
```

Este es un **ejemplo ilustrativo**: el nombre y el repositorio se resuelven en tu entorno. Para automatizaciones, la respuesta `--answers` también admite `"welcome_name": "Juan"` sin incorporarlo al perfil técnico versionado. La bienvenida es texto presentado por Claude Code; no es una ventana gráfica independiente.

## 📚 Referencia completa de comandos (con ejemplos)

Todos los comandos de esta sección se ejecutan **desde la raíz del repositorio correspondiente**, salvo los ejemplos de instalación que se ejecutan desde el repositorio `aikya-harnes`. Los comandos que dependen de SDK, Internet o skills externas requieren esas herramientas previamente instaladas. Los ejemplos `/...` se escriben **dentro de la interfaz de Claude Code**, no en Bash.

### 1. Instalar o actualizar Aikya Harness

| Comando | Para qué sirve | Ejemplo sencillo |
|---|---|---|
| `git clone -b develop` | Clonar el harness desde su rama de desarrollo. | `git clone -b develop https://github.com/jlema0590/aikya-harnes.git` |
| `python3 install.py --target` | Entrevista técnica e instalación en un proyecto nuevo o existente. | `python3 install.py --target ~/proyectos/mi-api` |
| `python3 install.py --answers` | Instalar con decisiones reproducibles sin entrevista. | `python3 install.py --target /tmp/demo-next --answers examples/new-next-react.json --external plan` |
| `python3 install.py --dry-run` | Revisar el plan sin modificar archivos. | `python3 install.py --target /tmp/demo-next --answers examples/new-next-react.json --dry-run` |
| `python3 install.py --external plan` | Mostrar dependencias externas previstas sin descargarlas. | `python3 install.py --target /tmp/demo-next --answers examples/new-next-react.json --external plan` |
| `python3 install.py --external skip` | Instalar el harness omitiendo las herramientas externas. | `python3 install.py --target /tmp/demo-next --answers examples/new-next-react.json --external skip` |
| `python3 install.py --external install` | Instalar también skills externas con autorización explícita en el comando. | `python3 install.py --target /tmp/demo-next --answers examples/new-next-react.json --external install` |
| `python3 install.py --display-name` | Personalizar el saludo para este usuario sin versionar su nombre. | `python3 install.py --target ~/proyectos/mi-api --display-name "Juan"` |

> **Importante:** `--answers` con `mode: new` exige un directorio vacío. En instalaciones ya existentes, utiliza `mode: existing`. La instalación de terceros ejecuta software externo; revisa sus fuentes antes de aprobarla.

### 2. Iniciar Claude Code y ver la bienvenida

| Comando | Para qué sirve | Ejemplo sencillo |
|---|---|---|
| `claude` | Iniciar la interfaz de Claude Code y mostrar la bienvenida en sesiones nuevas. | `cd ~/proyectos/mi-api && claude` |
| `python3 .claude/hooks/welcome.py --preview` | Previsualizar el saludo **sin** iniciar Claude Code. | `python3 .claude/hooks/welcome.py --preview` |
| `AIKYA_DISPLAY_NAME=... claude` | Cambiar el nombre temporalmente sólo para esta sesión (shell compatible). | `AIKYA_DISPLAY_NAME="Juan" claude` |

En el **repositorio fuente** de Aikya (no en un proyecto instalado), la previsualización está en `python3 template/.claude/hooks/welcome.py --preview` y `.claude/settings.json` registra su hook de inicio. Los proyectos instalados utilizan `.claude/hooks/welcome.py` y su propio `.claude/settings.json`.

La bienvenida usa un `systemMessage` del hook `SessionStart` de Claude Code. Es un **panel de texto**, no una ventana gráfica emergente: Claude Code controla cómo lo presenta en cada terminal/versión. Incluye nombre del desarrollador, repositorio Git detectado desde `origin` (o nombre de carpeta si no existe), URL del proyecto Aikya y atajos. No carga el texto completo en el contexto del modelo, no se conecta a la red y no se repite al compactar el contexto o ejecutar `/clear`.

Prioridad para el nombre mostrado: variable de entorno `AIKYA_DISPLAY_NAME`, archivo local `.harness/welcome.json`, `git config user.name` y finalmente `Desarrollador`. **No guardes nombres personales en el perfil de proyecto compartido**; `.harness/welcome.json` se excluye mediante `.gitignore`.

### 3. Inicialización y scaffolding de aplicaciones

| Comando | Para qué sirve | Ejemplo sencillo |
|---|---|---|
| `python3 scripts/harness/scaffold.py plan` | Mostrar generadores recomendados según la entrevista; no ejecuta descargas. | `python3 scripts/harness/scaffold.py plan` |
| `python3 scripts/harness/scaffold.py apply` | Ejecutar los generadores después de confirmar cada acción. | `python3 scripts/harness/scaffold.py apply` |
| `python3 scripts/harness/scaffold.py apply --yes` | Autorizar ejecución no interactiva, útil en entornos controlados. | `python3 scripts/harness/scaffold.py apply --yes` |

Los generadores pueden requerir Java SDK, .NET SDK, Node.js, Android Studio, Xcode o Flutter y acceso a Internet. No despliegan aplicaciones de forma automática.

### 4. Gestión de Agent Skills externas

| Comando | Para qué sirve | Ejemplo sencillo |
|---|---|---|
| `python3 scripts/harness/external_skills.py plan` | Ver las integraciones previstas (Ponytail, Graphify y UI UX si corresponde). | `python3 scripts/harness/external_skills.py plan` |
| `python3 scripts/harness/external_skills.py status` | Comprobar qué integraciones están instaladas o pendientes. | `python3 scripts/harness/external_skills.py status` |
| `python3 scripts/harness/external_skills.py install --yes` | Aprobar e instalar herramientas externas en el proyecto. | `python3 scripts/harness/external_skills.py install --yes` |
| `python3 scripts/harness/skills_lint.py` | Validar estructura y metadatos de las skills locales. | `python3 scripts/harness/skills_lint.py` |
| `python3 scripts/harness/skills_lint.py --include-vendor` | Incluir las skills de terceros instaladas en la validación. | `python3 scripts/harness/skills_lint.py --include-vendor` |
| `python3 scripts/harness/skills_lint.py --root` | Validar skills dentro de otro repositorio. | `python3 scripts/harness/skills_lint.py --root ~/proyectos/mi-api` |

**Graphify, si está instalado:** `graphify . --no-viz` crea el primer índice; `graphify query "¿Qué depende del módulo auth?"` consulta relaciones acotadas. No se indexa al iniciar cada sesión ni se inyecta el grafo completo al modelo.

### 5. Calidad, documentación viva y pruebas

| Comando | Para qué sirve | Ejemplo sencillo |
|---|---|---|
| `python3 scripts/harness/docs_guard.py base` | Verificar que existe la estructura documental obligatoria. | `python3 scripts/harness/docs_guard.py base` |
| `python3 scripts/harness/docs_guard.py status` | Revisar los documentos pendientes de la petición activa, cuando hay una sesión registrada. | `python3 scripts/harness/docs_guard.py status` |
| `python3 scripts/harness/docs_guard.py status --session` | Consultar la validación de una sesión específica. | `python3 scripts/harness/docs_guard.py status --session ID_DE_SESION` |
| `python3 scripts/harness/docs_guard.py ci --base` | Validar en CI los cambios documentales desde un commit base. | `python3 scripts/harness/docs_guard.py ci --base origin/main` |
| `python3 scripts/harness/run_checks.py` | Ejecutar quality gates de `harness.json`. | `python3 scripts/harness/run_checks.py` |
| `python3 -m unittest discover` | Ejecutar las pruebas automatizadas del propio repositorio Aikya. | `python3 -m unittest discover -s tests -p 'test_*.py' -v` |

`run_checks.py` marca como pendientes/fallidos los checks obligatorios sin configurar. `docs_guard.py status` necesita un estado de sesión generado por Claude Code; puede fallar si aún no existe una petición.

### 6. Skills invocables desde Claude Code (`/...`)

Estas **ocho skills** existen en `.claude/skills/<nombre>/SKILL.md` de cada proyecto instalado. Abre Claude Code desde el proyecto antes de usarlas:

| Comando en Claude Code | Uso | Ejemplo de petición |
|---|---|---|
| `/project-init` | Inicializar proyecto o módulos según decisiones del perfil. | `/project-init Prepara una API REST con el stack del perfil y tests iniciales` |
| `/project-bootstrap` | Planificar scaffold, infraestructura y módulos con confirmación. | `/project-bootstrap Planifica apps/api y apps/web sin sobrescribir código` |
| `/feature` | Implementar una funcionalidad, pruebas y docs afectadas. | `/feature Añade GET /health y un test de respuesta 200` |
| `/bugfix` | Investigar un fallo, corregirlo y documentar regresión. | `/bugfix El login devuelve 500 cuando la contraseña está vacía` |
| `/architecture-review` | Revisar arquitectura y registrar decisiones cuando proceda. | `/architecture-review Evalúa dependencias entre API y dominio` |
| `/mobile-feature` | Implementar una funcionalidad Android/iOS si el proyecto es móvil. | `/mobile-feature Añade pantalla de perfil en Android Kotlin` |
| `/documentation-sync` | Sincronizar overview, features, bugs, seguridad y bitácora. | `/documentation-sync Revisa documentación tras el cambio de autenticación` |
| `/verify` | Ejecutar verificaciones reales y reportar evidencias. | `/verify Comprueba lint, tests, build y documentación` |

Las skills externas se gestionan mediante `external_skills.py` y sólo aparecen cuando se instalan correctamente; sus comandos y opciones específicos dependen de la versión publicada por cada proveedor. Los comandos integrados de Claude Code (por ejemplo, `/help`) no los implementa Aikya.

---

## Novedades v4: integración de skills oficiales, sin MCP

Se han contrastado las **ocho skills propias v3** con la [especificación Agent Skills](https://agentskills.io/specification) (repositorio [agentskills/agentskills](https://github.com/agentskills/agentskills)). Se conserva la convención `SKILL.md` con `name` y `description` en YAML; `disable-model-invocation` es una extensión Claude Code y no un campo portable. El validador incluido comprueba formato y convenciones básicas; opcionalmente se puede ejecutar el `skills-ref validate` oficial si está instalado. No sustituimos un analizador YAML completo.

| Skill externa | Fuente verificada | Integración v4 | Activación útil |
|---|---|---|---|
| **Ponytail** | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Clona temporalmente la fuente oficial y copia **únicamente** `skills/ponytail` como skill de proyecto. Registra SHA del commit; **no** instala el plugin completo ni sus extras de band/telemetría. | Antes de implementar o revisar para reutilizar código y reducir complejidad sin reducir seguridad/tests. |
| **Graphify** | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Instala el CLI `graphifyy` (doble `y`) con `uv`/`pipx`, luego `graphify install --project --platform claude`; **sin MCP ni Graphify Cloud**. | Consultas acotadas de arquitectura y dependencias. Construir/actualizar el grafo cuando sea relevante, nunca automáticamente cada turno. |
| **UI UX Pro Max** | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Instala la skill con `npx --yes ui-ux-pro-max-cli init --ai claude` sólo si la entrevista selecciona frontend web o app móvil. | Diseño de interfaces React/Vue/Next.js, Android, iOS, design systems y revisión UX/accesibilidad. |

**Se necesita Internet para descargar terceros.** Durante la entrevista interactiva el instalador enseña el plan y **pregunta** si autorizas la ejecución. La respuesta predeterminada es **No** (no ejecuta código ajeno por accidente). En una instalación automatizada con `--answers`, deja las skills externas en modo **plan**, salvo que el operador pase `--external install`, lo que supone autorización explícita de esa ejecución externa. El código de proyecto y la documentación se instalan aunque no haya red.

```bash
# Instalación interactiva con entrevista + consentimiento para skills externas
python3 install.py --target /ruta/mi-repositorio

# Preparar un entorno (CI / no interactivo) SIN descargas de terceros
python3 install.py --target /ruta/proyecto \
  --answers examples/new-next-react.json --external plan

# Instalar skills autorizadas una vez que el harness ya existe
cd /ruta/proyecto
python3 scripts/harness/external_skills.py plan
python3 scripts/harness/external_skills.py install --yes
python3 scripts/harness/external_skills.py status

# Calidad del contrato Agent Skills local
python3 scripts/harness/skills_lint.py
```

Para instalar terceros ya durante el setup automatizado, usa `--external install` junto a `--answers`. Si una descarga falla, el instalador registra el error en `.harness/external-skills-lock.json` y devuelve código **3**; puedes reintentar sin reinstalar el harness. Las instalaciones no se actualizan automáticamente y se preservan skills ajenas o personalizadas.

**Avisos de seguridad:** `git clone`, `uv/pipx` y `npx` confían en software de terceros; revisa sus licencias, contenido, versiones, dependencias y permisos antes de aprobarlo. Ponytail queda fijado en el commit registrado tras la instalación, pero el origen inicial se sigue desde la rama predeterminada; las instalaciones PyPI/npm sin versión explícita son variables en el tiempo. Para controles de cadena de suministro estrictos, fija versiones y hashes en un repositorio interno antes de ejecutar instalaciones.

### Activación por contexto y consumo de tokens

- **Inicio de sesión:** hook `SessionStart` sólo verifica presencia de skills y emite un aviso mínimo si falta alguna; no consulta la red, no instala y no reindexa.
- **Ponytail:** prioriza examinar y reutilizar código real en cambios de funcionalidad, refactor o revisión; no elimina validaciones críticas.
- **Graphify:** consulta relaciones a través de `graphify query "pregunta concreta"` cuando el grafo existe y está vigente. No vuelques `graphify-out/graph.json` ni reportes completos al contexto. Comandos de primer índice: `graphify . --no-viz`; para revisar novedades consulta la ayuda de `graphify update .` según versión instalada.
- **UI UX Pro Max:** sólo al diseñar/implementar pantallas o estilos, no para tareas exclusivas de API/infraestructura. Las decisiones aprobadas se documentan en `docs/design/design-system.md`.
- **Verificación:** no se afirma ningún porcentaje de reducción de tokens. Hay que comparar tareas equivalentes, con/sin cada integración, y medir tokens, latencia, coste, calidad, pruebas y correcciones.

Análisis completo de compatibilidad: [SKILLS_AUDIT.md](SKILLS_AUDIT.md). Políticas completas en `docs/harness/token-policy.md`, `docs/harness/skills-comparison.md` y `.claude/rules/02-context-budget.md` del repositorio instalado.

## 1. Instalar en un proyecto nuevo o existente

```bash
# Extrae el ZIP fuera del repositorio de destino
python3 install.py --target /ruta/mi-repo

# Sin preguntas: perfil reproducible
python3 install.py --target /ruta/proyecto-nuevo \
  --answers examples/new-fullstack-mobile.json

# Previsualiza sin escribir nada
python3 install.py --target /ruta/proyecto-nuevo \
  --answers examples/new-fullstack-mobile.json --dry-run
```

**Proyecto nuevo:** el destino debe estar vacío; entrevista para elegir Java/Spring/Quarkus/Micronaut, .NET/ASP.NET Core, Node/NestJS/Fastify/Express/Hono, Next, React, Vue, Android Kotlin/Java, iOS SwiftUI/UIKit y Flutter/React Native; arquitectura, DB, auth, CI, deploy, OTel y tests. La instalación crea el harness, documentación y assets de infraestructura, pero **no ejecuta** los generadores de aplicaciones sin permiso.

**Proyecto existente:** detección conservadora de manifiestos, entrevista editable, preservación de archivos de usuario y fusión no destructiva de `.claude/settings.json`. `CLAUDE.md` existente se conserva y la política obligatoria se carga mediante `.claude/rules/01-documentation-policy.md`. Si ya existe `harness.json`, se conserva: añade manualmente el gate documental si procede. Las configuraciones actuales de agentes/skills se preservan.

## 2. Carpetas que se crean

```text
mi-repositorio/
├── CLAUDE.md
├── harness.json
├── .harness/
│   ├── project-profile.json
│   └── state/                         # efímero, ignorado en Git
├── .claude/
│   ├── settings.json                  # hooks SessionStart, UserPromptSubmit + Stop
│   ├── agents/                        # architect, backend, frontend, mobile, QA, security, docs
│   ├── skills/                        # skills propias y externas opcionales, feature, bugfix,
│   │                                  # mobile-feature, documentation-sync, verify, etc.
│   ├── rules/
│   └── hooks/
├── docs/
│   ├── README.md                      # índice y política
│   ├── overview.md                    # propósito, contexto, stack y estado
│   ├── plan/roadmap.md                # planes, prioridades, hitos
│   ├── features/index.md              # catálogo de features
│   ├── bugs/index.md                  # incidencias y regresiones
│   ├── security/security.md           # controles, amenazas, riesgos
│   ├── architecture/overview.md       # módulos, límites y contratos
│   ├── decisions/README.md            # registro ADR
│   ├── decisions/0001-entrevista-stack.md
│   ├── operations/deployment.md
│   ├── operations/observability.md
│   ├── quality/testing.md
│   ├── changes/README.md              # un documento por petición con cambios técnicos
│   ├── design/design-system.md         # sólo si hay frontend o móvil
│   └── harness/                      # bootstrap, skills-comparison, token-policy
├── infra/
│   ├── docker/README.md
│   └── observability/{README.md,otel.env.example}
├── .github/workflows/harness.yml      # sólo con CI github-actions
├── compose.yaml                       # sólo para DB compatible (Postgres/MySQL/Mongo)
└── scripts/harness/
    ├── scaffold.py
    ├── docs_guard.py
    ├── skills_lint.py
    ├── external_skills.py
    └── run_checks.py
```

Las carpetas `apps/api`, `apps/web`, `apps/mobile`, `apps/android` o `apps/ios` **no se crean vacías**: se crean cuando ejecutas los generadores correspondientes. Se preservan documentos `docs/` que ya existían.

## 3. Engineering Bootstrap (generación asistida)

Tras la instalación, desde la raíz del destino:

```bash
python3 scripts/harness/scaffold.py plan
# Genera una lista de comandos, sin cambiar el proyecto ni necesitar red.

python3 scripts/harness/scaffold.py apply
# Revisa los comandos, pide confirmación y ejecuta los generadores soportados.
```

La ejecución utiliza argumentos de `subprocess` sin `shell`, comprueba dependencias y evita sobrescribir directorios de aplicación existentes. Los comandos **pueden descargar archivos** y requieren SDKs/herramientas instaladas.

| Stack | Scaffolding automatizable desde CLI | Trabajo pendiente tras generar |
|---|---|---|
| .NET | `dotnet new webapi/web` | SDK, tests, auth, Dockerfile y API |
| Next.js | `create-next-app` | SSR/API, tests, CI/observabilidad |
| React / Vue | Vite oficial | Tests, contratos API, build |
| Node NestJS | CLI Nest | Instalar deps y gates |
| Java Spring/Quarkus/Micronaut | Guía del generador oficial; no auto-descarga | Inicialización asistida, versiones, SDK |
| Node Express/Fastify/Hono | Guía manual segura | Framework, dependencias y tests |
| Android / iOS nativos | Guías Android Studio / Xcode | IDE, signing, variantes, simuladores |
| Flutter | `flutter create` | Toolchain, testing, mobile CI |
| React Native | `create-expo-app` | Confirmar Expo/bare, toolchains |

El scaffold es **asistido**, no implica una aplicación funcional completa, builds correctos o la integración automática de OpenTelemetry. Las guías `docs/harness/bootstrap.md`, `infra/observability/README.md` y `infra/docker/README.md` establecen los siguientes pasos. `compose.yaml`, cuando se crea, proporciona **sólo base de datos para desarrollo local** con credenciales exigidas por variables de entorno; no despliega la app.

## 4. Política de documentación por cada petición

1. **Antes de la petición**: `UserPromptSubmit` registra un identificador (`REQ-YYYYMMDD-xxxxxxxx`), categoría y snapshot de archivos relevantes. Nunca guarda el texto del prompt; guarda un hash SHA-256.
2. **Durante la tarea**: Claude lee docs, implementa y actualiza la documentación afectada: features y plan, bugs, seguridad, arquitectura/ADR, despliegue, observabilidad o testing.
3. **Bitácora por petición**: si hubo cambios técnicos, se crea `docs/changes/REQ-....md` con encabezados `## Cambios`, `## Evidencias`, `## Documentos actualizados`, rutas concretas y pruebas realmente ejecutadas.
4. **Antes de responder**: el hook `Stop` compara huellas SHA-256 y devuelve `decision: block` si falta documentación afectada o la bitácora. No exige modificar docs cuando la petición sólo lee datos y no toca código.
5. **En PR**: `python3 scripts/harness/docs_guard.py ci --base <SHA_base>` verifica el diff contra Git y requiere al menos un documento temático y bitácora. Exige docs específicos cuando las rutas sugieren seguridad, infraestructura o tests. El CI se incluye automáticamente si se eligió GitHub Actions, pero su extensión con los SDKs del stack queda pendiente.

Comandos de validación:

```bash
python3 scripts/harness/docs_guard.py base
python3 scripts/harness/docs_guard.py status
python3 scripts/harness/run_checks.py
```

**Garantía realista:** se obliga a **editar** y **referenciar** los documentos pertinentes con estructura suficiente, pero un script no puede certificar su exactitud técnica. Los hooks pueden deshabilitarse o ser eludidos fuera de Claude Code: protegen el flujo interactivo, y CI protege PRs cuando está configurado. Una revisión de PR sigue siendo imprescindible. La comprobación no inspecciona archivos `.env`.

**Ejemplo de nueva feature:** si se añade `apps/api/catalog.ts`, Claude actualiza `docs/features/index.md` y `docs/plan/roadmap.md`, y crea `docs/changes/REQ-....md` enlazando los archivos y verificaciones.

**Ejemplo de bug:** cambio en `apps/api/auth.ts` para corregir login; se actualizan `docs/bugs/index.md`, `docs/security/security.md` y la bitácora con test de regresión.

## 5. Calidad / CI / seguridad

- `harness.json` contiene checks necesarios por módulo. Si un check obligatorio tiene `command: null` retorna `NOT_CONFIGURED` y fallo intencionado (no hay falsos verdes).
- `scripts/harness/run_checks.py` no ejecuta comandos mediante shell y valida directorios relativos del proyecto.
- `.gitignore` añade `.harness/state/` y `.env` de forma no destructiva; la instalación evita imprimir el contenido de archivos privados.
- El hook Stop es un control de completitud documental, no un analizador de seguridad ni sustituto de validación de builds.
- El YAML GitHub Actions inicial verifica la documentación; los jobs de Node, Java, .NET, Android/iOS se configuran después de generar módulos reales, toolchains y tests.

## 6. Trabajar desde Claude Code

Desde la raíz del proyecto abre `claude` y utiliza:

- `/project-bootstrap` para planificar el scaffold y, con aprobación, ejecutarlo.
- `/feature` para implementar con pruebas y actualizar docs.
- `/bugfix` para corregir, registrar causa raíz y regresión.
- `/documentation-sync` para revisar el impacto documental y bitácora.
- `/verify` para ejecutar checks y reportar evidencias.

## 7. Validaciones del paquete

```bash
cd aikya-harnes
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Incluye pruebas de instalación nueva/existente, detección, preservación de archivos, doc gate, hooks, CI y scaffold sin sobrescritura. La suite de pruebas automatizadas incluyen casos v3, skills propias, migración exacta v3→v4, rutas de diseño y consentimientos. Las pruebas externas de descargas se realizan mediante simulación, pues requieren acceso a GitHub/PyPI/npm desde la máquina de instalación. Las pruebas automatizadas **no** cubren builds de todos los SDKs ni sustituyen una ejecución end-to-end en una instalación real de Claude Code.

## 8. Actualizar una instalación v3

Ejecuta este instalador v4 sobre el mismo repositorio con **mode=existing**. Si un archivo gestionado coincide exactamente con el hash de la plantilla v3, se actualiza a v4 y se guarda copia en `.harness/backup-v3/`; los archivos que hayas personalizado se conservan. Los settings se fusionan sin eliminar tus hooks, y se añade el hook `SessionStart`. El `CLAUDE.md` existente se conserva y las reglas de contexto se activan desde `.claude/rules/02-context-budget.md`. Revisa manualmente `harness.json` existente para incorporar el check `skills:format` si lo deseas; no se sobrescribe para proteger tus quality gates.

Comprueba primero con `--dry-run` y realiza copia de seguridad/versiona el repositorio.
