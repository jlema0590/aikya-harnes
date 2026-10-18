# Instalar y usar Aikya Harness desde Claude Code

Todo el proceso comienza en **Claude Code**; los comandos de sistema son mecanismos internos que Claude utiliza tras la autorización pertinente.

## Iniciar la instalación

En una conversación de Claude Code, solicita:

> Instala Aikya Harness desde `https://github.com/jlema0590/aikya-harnes.git`, rama `develop`, en modo **global**. Revisa el repositorio, explica los cambios y solicita permiso antes de instalarlo. No instales SDKs ni herramientas externas sin mi autorización. Cuando esté listo, indícame cómo iniciar `/aikya-init`.

Si deseas usar Aikya sólo en el repositorio abierto, solicita **modo proyecto**. Aikya registra las skills y un aviso de bienvenida; no debe inicializar automáticamente otros repositorios.

## Flujo inicial

1. `/aikya-init`: entrevista conversacional para seleccionar proyecto nuevo o existente, backend, frontend, móvil, versiones, arquitectura, calidad y despliegue.
2. `/aikya-answers`: alternativa declarativa para instalar con decisiones JSON aprobadas.
3. `/aikya-doctor`: diagnóstico sin actualización silenciosa de SDKs.
4. `/aikya-scaffold plan`: plan de generación sin ejecutar acciones externas. Revisa el plan antes de aprobar la generación.
5. `/aikya-infra-project`: completa contratos, infraestructura y configuraciones específicas; confirma qué builds se ejecutaron realmente.
6. `/aikya-skills-status` y `/aikya-skills-plan`: revisión de skills externas. `/aikya-skills-install` pide consentimiento explícito antes de instalar.
7. `/aikya-tests`, `/aikya-quality` y `/aikya-docs`: pruebas, validación y actualización de la documentación afectada.

## Comandos de implementación

- `/aikya-feature`: desarrollo de funcionalidades.
- `/aikya-bugfix`: incidencias y regresiones.
- `/aikya-architecture-review`: arquitectura y ADR.
- `/aikya-mobile-feature`: Android/iOS.
- `/aikya-project-init`: planificación inicial.
- `/aikya-documentation-sync` y `/aikya-verify`: aliases compatibles para sincronización documental y verificación.

## Límites y seguridad

Aikya no puede iniciar autónomamente una entrevista desde el hook de inicio: muestra un aviso y el usuario decide qué comando ejecutar. No instala o actualiza SDKs, dependencias externas, generadores ni realiza cambios destructivos sin aprobación. No presume compilación, cobertura ni validaciones que no se hayan ejecutado.

La instalación global registra comandos en Claude Code, pero **no altera repositorios automáticamente**. En proyectos existentes respeta instrucciones, código, documentación y skills personalizados. Las decisiones confirmadas se guardan por proyecto y cada petición que cambia código debe actualizar su documentación y evidencias.

Volver al [README](README.md).

## Gestión de Skills con comandos Aikya

Desde Claude Code utiliza `/aikya-skills-status` para ver el inventario de skills en `docs/skills.md`, `/aikya-skills-plan` para estudiar compatibilidad y fuentes, y `/aikya-skills-install` para instalar las seleccionadas con aprobación. Para una skill GitHub nueva, proporciona URL HTTPS, nombre conforme a Agent Skills, carpeta que contiene `SKILL.md` y referencia (idealmente commit fijo). Aikya no instala ni ejecuta código remoto sin tu autorización.

Los comandos nuevos sustituyen a `/aikya-skills status`, `/aikya-skills plan`, `/aikya-skills install` y `/aikya-project-bootstrap`; este último pasa a `/aikya-infra-project`. La migración sólo retira wrappers gestionados sin personalizaciones.
