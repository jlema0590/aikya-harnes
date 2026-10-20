---
name: aikya-analyze
description: Incorpora Aikya a un repositorio existente mediante descubrimiento automático, sin entrevista ni modificar código o infraestructura.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-analyze — adopción de proyectos existentes

Argumentos opcionales: --dry-run, --report-only, --refresh, --focus security|architecture|infrastructure|operations, --scope ruta/relativa. Solo utiliza estos argumentos explícitos; no interpretes texto como comandos shell. No inventes decisiones ni variantes de infraestructura.

1. Trabaja en el proyecto actual, nunca en el runtime global. Resuelve el CLI como en /aikya-init: .aikya/runtime/aikya_cli.py, aikya_cli.py o ~/.claude/aikya-harnes/aikya_cli.py. No ejecutes archivos del repositorio ni scripts de bootstrap de terceros.
2. Ejecuta SIEMPRE primero el análisis sin escritura: python3 <cli> analyze --target . --dry-run, añadiendo solo --focus, --scope, --refresh permitidos. Este comando inspecciona nombres y manifiestos; no instala nada.
3. Si devuelve EMPTY, explica que /aikya-init es la entrada para un proyecto nuevo. Si devuelve PARTIAL o NEEDS_REVIEW, enumera evidencias y decisiones pendientes; no fuerces una tecnología o aprobación. Para proyectos con archivos personalizados, jamás elimines su contenido.
4. Presenta el resultado de detección y el listado de operaciones propuestas. Indica expresamente que se creará SOLO el entorno de Aikya, que no se realizarán builds, scans remotos, docker build, terraform init/plan/apply, cambios de SDK, redes, despliegues ni operaciones con scripts.
5. Si el usuario pide --report-only, responde en conversación sin escribir archivos. Si pide --dry-run, termina tras la simulación. Para incorporación real, solicita autorización clara para escribir los objetos del harness. Una aprobación anterior a ejecutar /aikya-analyze no equivale a aprobar despliegues ni instalaciones externas.
6. Tras esa autorización, ejecuta python3 <cli> analyze --target . --approved, con el mismo --focus/--scope/--refresh. No uses --approved en ausencia de consentimiento explícito.
7. Muestra los archivos creados, los preservados, cualquier conflicto, el estado READY/PARTIAL/NEEDS_REVIEW y qué comprobaciones no se ejecutaron. Una inspección de manifiestos nunca demuestra ausencia de CVEs ni corrección de arquitectura.
8. Si el proyecto ya tiene Aikya v5.9.1, conserva su esquema, comandos, hooks, documentos, modelos y agentes personalizados. No migres Haiku 4.5 a 5.5 sin autorización independiente. Si el repositorio tiene una estructura no representable por el esquema anterior, devuelve PARTIAL en lugar de fabricar un backend principal.
9. Después de READY, ofrece /aikya-feature, /aikya-bugfix, /aikya-architecture-review, /aikya-quality, /aikya-docs y /aikya-infra-project plan. Para seguridad utiliza la skill security-audit mediante el modelo principal, nunca Haiku como autoridad final.

El motor de analyze es Python determinista y no llama modelos por sí mismo. Haiku 5.5 es opcional para resúmenes/extracción posterior según la política v2 aprobada. Los validadores deterministas y las restricciones de permisos tienen prioridad.
