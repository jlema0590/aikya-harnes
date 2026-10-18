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
3. Entrevista técnica por turnos, agrupando preguntas: **nuevo/existente y nombre**, backend (Java Spring Boot/Quarkus/Micronaut, .NET ASP.NET Core, Node/Nest/Fastify/Express, Next), frontend (React/Vue/ninguno), móvil (Android Kotlin/Java, iOS SwiftUI/UIKit, ambos, Flutter, React Native), framework, arquitectura, API, autenticación, base de datos, versiones de SDK, pruebas, observabilidad, despliegue, CI, gestor de paquetes. Pregunta sólo campos importantes faltantes. Nunca inventes versiones ni respuestas del usuario.
4. Construye en el directorio de proyecto `.aikya/answers.json` con esquema compatible con los ejemplos de `examples/` en el runtime. Si contiene información existente, reutilízala tras validarla. Respuestas sin secretos y con `mode: new` sólo si el directorio está vacío salvo `.git`, `.aikya/answers.json` y bootstrap Aikya. Enseña resumen y pide **confirmación explícita**.
5. Ejecuta `python3 <cli> requirements --target . --answers .aikya/answers.json`. Si faltan SDKs o versiones no coinciden, muestra lo detectado, versión solicitada y URLs oficiales; **solicita permiso** para cualquier cambio de herramientas. Si no están listos, podrás instalar el harness, pero NO ejecutar scaffold/builds hasta resolverlos. En macOS/iOS confirma Xcode; en Linux/Windows no finjas compilar iOS localmente.
6. Con aprobación, `python3 <cli> init --target . --answers .aikya/answers.json --external plan`. Si el usuario desea ejecutar descargas de terceros, explícitas y por separado: `--external install`; NUNCA como predeterminado. Si el usuario pide sólo plan, añade `--dry-run`.
7. Confirma artefactos creados, documentación `docs/`, `docs/harness/requirements.md`, pendiente de SDKs, y comandos `/aikya-project-bootstrap`, `/aikya-feature`, `/aikya-verify` disponibles tras instalar. Pide aprobación antes de ejecutar generadores de código.

Si quieres reiniciar la entrevista sin perder cambios, mantén los archivos del usuario y usa `mode: existing`; el instalador preserva personalizaciones.
