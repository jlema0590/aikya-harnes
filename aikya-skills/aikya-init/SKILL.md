---
name: aikya-init
description: Inicia Aikya Harness EN CLAUDE CODE para un proyecto nuevo o existente; entrevista técnica, diagnóstico de SDK y aplicación controlada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-init — Entrevista conversacional dentro de Claude Code

**NO inicies `install.py` sin `--answers` ni abras un cuestionario interactivo de Python.** Todo el diálogo de entrevista y consentimiento ocurre en esta conversación de Claude Code; usa AskUserQuestion si está disponible o preguntas normales. No ejecutes comandos de instalación de SDK, npx, git remoto ni generación de aplicaciones sin aprobación explícita.

1. Determina el directorio actual como destino (`pwd`), no `~/.claude` aunque Aikya sea global. Resuelve el CLI comprobando sucesivamente estas rutas existentes: `.aikya/runtime/aikya_cli.py` (bootstrap local), `aikya_cli.py` (fuente Aikya abierta en Claude) y `$HOME/.claude/aikya-harnes/aikya_cli.py` (instalación global). Si ninguna existe, solicita instalar Aikya desde GitHub primero.
2. Ejecuta `python3 <ruta-al-aikya_cli.py> probe --target <directorio-del-proyecto>` para ver manifiestos y perfil previo. Si se trata de un repo existente, lee el README y las versiones declaradas (`global.json`, `.nvmrc`, `pom.xml`, Gradle, package.json). **No presupongas tecnologías detectadas**: confirma con usuario.
3. **PRIMERA PREGUNTA OBLIGATORIA:** selección `project_type`: **development**, **infrastructure** o **devops**. Sólo después pregunta `mode` (nuevo o existente). Si no existe `project_type` en JSON heredado, usar development.
   - **development:** entrevista actual completa de stack y arquitectura. Infraestructura/DevOps son opcionales adicionales. Continúa con las preguntas técnicas indicadas abajo.
   - **infrastructure:** no preguntes backend, frontend, móvil, arquitecturas de aplicación ni monorepo/singlerepo. Pregunta cloud/on-prem/híbrido, Terraform/OpenTofu y/o Ansible, entornos, módulos, backend de estado, seguridad y restricciones. `backend`, `frontend`, `mobile` y campos no aplicables son `none`; `repository_layout=singlerepo` técnico sin aplicación.
   - **devops:** no preguntes por tecnologías de desarrollo salvo para inspeccionar fuentes existentes para Dockerfile. Pregunta origen (código, imagen, chart, manifests), Dockerfile y Compose de forma independiente, destino, Kubernetes: YAML, Helm o Kustomize. Con Helm pregunta crear chart o **usar chart existente** y su ruta relativa segura. Confirma imagen versionada/puerto si se requieren manifests. Kubernetes desde imagen no requiere Docker instalado.
   - **Para Infrastructure y DevOps:** prepara perfil con `project_type`, `mode`, `infrastructure`; ejecuta la validación, el plan y pide consentimiento antes de generar. No generes `apps/`, `contracts/`, `packages/`, tests o scaffolding de aplicación, ni cargues agentes de lenguajes.
4. **Sólo en development:** entrevista por turnos, agrupando preguntas: **nombre y organización monorepo/singlerepo**, backend (Java Spring Boot/Quarkus/Micronaut, .NET ASP.NET Core, Node/Nest/Fastify/Express, Next), frontend (React/Vue/ninguno), móvil (Android Kotlin/Java, iOS SwiftUI/UIKit, ambos, Flutter, React Native), framework, arquitectura, API, autenticación, base de datos, versiones de SDK, pruebas, observabilidad, despliegue, CI, gestor de paquetes; **Infrastructure & DevOps**: AWS/Azure/GCP/on-prem/híbrido, Terraform/OpenTofu, Ansible, Docker y Compose, Kubernetes y estrategia Helm/Kustomize/YAML, entornos, imagen y puerto. Si no se requiere infraestructura, guarda opciones `none`/desactivadas. Pregunta sólo campos importantes faltantes. Nunca inventes versiones ni respuestas del usuario.
5. **Sólo en development:** confirma monorepo (apps/, packages/, contracts/) o singlerepo (una sola aplicación en raíz), y explica los límites de una sola aplicación antes de continuar. En Kubernetes selecciona exactamente una vía (Helm, Kustomize o YAML); confirma proveedor, entornos y gestión de secretos sin solicitarlos en el chat.
6. Incluye la clave opcional `infrastructure` validada por `infrastructure_profile.py` en `.aikya/answers.json`: provider, iac, configuration_management, containers.enabled/compose, orchestration, deployment_method, environments, image_repository y container_port. No inventes imágenes, puertos, credenciales ni backend Terraform. Los JSON antiguos sin esa clave siguen siendo válidos.
7. Construye en el directorio de proyecto `.aikya/answers.json` con esquema compatible con los ejemplos de `examples/` en el runtime. Si contiene información existente, reutilízala tras validarla. Respuestas sin secretos y con `mode: new` sólo si el directorio está vacío salvo `.git`, `.aikya/answers.json` y bootstrap Aikya. Enseña resumen y pide **confirmación explícita**.
8. Ejecuta `python3 <cli> requirements --target . --answers .aikya/answers.json`. Si faltan SDKs o versiones no coinciden, muestra lo detectado, versión solicitada y URLs oficiales; **solicita permiso** para cualquier cambio de herramientas. Si no están listos, podrás instalar el harness, pero NO ejecutar scaffold/builds hasta resolverlos. En macOS/iOS confirma Xcode; en Linux/Windows no finjas compilar iOS localmente.
9. Con aprobación, `python3 <cli> init --target . --answers .aikya/answers.json --external plan`. Si el usuario desea ejecutar descargas de terceros, explícitas y por separado: `--external install`; NUNCA como predeterminado. Si el usuario pide sólo plan, añade `--dry-run`.
10. Confirma artefactos creados, documentación `aikya/docs/`, `aikya/docs/harness/requirements.md`, pendiente de SDKs, y comandos `/aikya-infra-project`, `/aikya-feature`, `/aikya-verify` disponibles tras instalar. Pide aprobación antes de ejecutar generadores de código.

Si quieres reiniciar la entrevista sin perder cambios, mantén los archivos del usuario y usa `mode: existing`; el instalador preserva personalizaciones.

## Activación de especialistas de ingeniería

- Tras confirmar el stack, Aikya selecciona automáticamente los agentes/skills técnicos pertinentes desde su catálogo incluido, sin descarga ni ejecución de scripts externos.
- Consulta `aikya/docs/agents.md` y `aikya/docs/skills.md`; instala especialistas opcionales únicamente a petición y con aprobación mediante `/aikya-skills-install`.
- Excluye agentes y skills de LinkedIn, derecho digital, SaaS y propiedad intelectual.

La bienvenida mediante SessionStart aparece al comenzar una NUEVA sesión de Claude Code. Tras inicializar, previsualiza el panel desde el hook welcome.py con --preview para que el usuario lo vea también en esta conversación.

## Infrastructure & DevOps después del init

- Si el perfil seleccionó infraestructura, enseña `aikya/docs/infrastructure/plan.md` y ejecuta `/aikya-infra-project plan`. Sólo tras la aprobación específica del plan ejecuta `/aikya-infra-project generate`.
- El scaffolding de la aplicación precede a la generación de Dockerfile: confirmar runtime, manifiestos, lockfiles y comando de arranque reales.
- Nunca realices Terraform apply/destroy, Ansible contra hosts, push de imágenes ni deploy/helm/kubectl contra clústeres sin permiso separado.


## Selección de modelos (Aikya v6)

Después de confirmar el tipo de proyecto y antes de instalar, ofrece configurar modelos con `/aikya-models`: recomienda Opus para planner/orchestrator y `inherit` para desarrolladores y revisores. Si la sesión usa Opus, recomienda Sonnet para tareas rutinarias, pero no la cambies sin autorización. Haiku solo como auxiliar opt-in y tras validar disponibilidad. Guarda la política por separado en `.aikya/model-policy.json`; para respuestas 5.9.1 sin política, preserva el comportamiento existente sin añadir preguntas obligatorias ni alterar el esquema de `answers.json`.
