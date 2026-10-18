# Instalar Aikya Harness directamente desde Claude Code

**El usuario interactúa solamente con Claude Code**. No necesita ejecutar personalmente comandos fuera de Claude. Claude solicitará permisos de acceso a Git, lectura/escritura e instalación. La primera instalación debe autorizar la descarga del código de un repositorio externo; revisa los cambios antes de ejecutarlos.

## Prompt para pegar en Claude Code (modo global)

> Instala Aikya Harness desde `https://github.com/jlema0590/aikya-harnes.git`, rama `develop`, en **modo global** para todos mis proyectos. Inspecciona primero el README y el instalador, confirma los comandos que vas a ejecutar y solicita mi aprobación antes de descargarlos o instalar. Clona el repositorio en un directorio temporal seguro y ejecuta `python3 aikya_setup.py --scope global` desde allí. No inicialices ningún proyecto todavía y no instales SDKs o dependencias externas sin mi permiso. Muéstrame cómo utilizar `/aikya-init`, `/aikya-answers` y `/aikya-doctor` en una nueva sesión.

## Prompt para pegar en Claude Code (modo proyecto)

> Instala Aikya Harness desde `https://github.com/jlema0590/aikya-harnes.git`, rama `develop`, en **modo proyecto**, únicamente en el directorio de trabajo actual. Antes de actuar, revisa la fuente, muestra el plan y pide confirmación. Clona Aikya temporalmente y desde esa copia ejecuta `python3 aikya_setup.py --scope project --target <directorio-de-trabajo-actual>`. No ejecutes la entrevista ni descargues SDKs todavía. Después explícame cómo iniciar `/aikya-init` en una sesión nueva.

**Precaución:** en el comando anterior, `<directorio-de-trabajo-actual>` significa la ruta real al repositorio en el que se está trabajando; no escribas los signos `<>` literalmente. Es recomendable fijar un commit o etiqueta verificada de Aikya para entornos corporativos, en lugar de seguir una rama mutable.

## Dentro de Claude Code: flujo de proyecto nuevo

1. Inicia Claude Code en la carpeta del proyecto deseado. Tras el bootstrap (y una sesión nueva para que Claude descubra las skills), ejecuta `/aikya-init`.
2. Claude ejecuta `aikya_cli.py probe` para detectar tecnologías existentes. Después **conversa** sobre backend, frontend, móvil, arquitectura, infraestructura y versiones, solicitando las decisiones necesarias.
3. Claude prepara `.aikya/answers.json` y muestra un resumen para aprobación. Puedes conservar o editar ese JSON.
4. Ejecuta desde Claude `aikya_cli.py requirements` para verificar herramientas reales. Registra estados `ok`, `missing`, `version_mismatch`, `unsupported_host`. Si faltan SDK, Claude te propone cómo instalar la versión solicitada, pero **no actualiza sin autorización**.
5. Cuando apruebes, Claude llama a `aikya_cli.py init --answers .aikya/answers.json --external plan`, genera el perfil, los agents, skills, hooks, carpeta `docs/` y `docs/harness/requirements.md`.
6. Después usa `/aikya-project-bootstrap` para planificar el scaffolding. Los generadores tienen un control adicional: no pueden ejecutarse si los requisitos elegidos están pendientes.

## Dentro de Claude Code: respuestas ya guardadas

- `/aikya-answers` utiliza `.aikya/answers.json` o `.harness/project-profile.json`, o la ruta JSON que le facilites.
- `/aikya-answers .aikya/runtime/examples/new-next-react.json` (modo proyecto; en global, ruta `~/.claude/aikya-harnes/examples/new-next-react.json`) utiliza una configuración reproducible, confirma los cambios y valida SDK antes de instalar.
- `/aikya-doctor` repite la comprobación de versiones sin modificar nada.

## Qué instala cada alcance

| Alcance | Runtime compartido | Skills iniciales | Cambios en repositorios |
|---|---|---|---|
| Global | `~/.claude/aikya-harnes/` | `~/.claude/skills/aikya-{init,answers,doctor}/` | Ninguno hasta ejecutar `/aikya-init` en un proyecto |
| Proyecto | `<repo>/.aikya/runtime/` | `<repo>/.claude/skills/aikya-{init,answers,doctor}/` | Sólo archivos de bootstrap, no se crea app ni docs hasta inicializar |

El bootstrap inicial exige Python ≥ 3.9, Git y acceso a GitHub (por parte del entorno de Claude). El código no instala Java, .NET, Node, Android Studio o Xcode automáticamente. Se reporta su disponibilidad antes de generar aplicaciones. iOS nativo necesita macOS y Xcode.

Tras instalar, inicia una nueva sesión de Claude Code si las nuevas skills aún no aparecen en el menú `/`.
