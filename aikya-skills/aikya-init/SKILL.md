---
name: aikya-init
description: Inicia exclusivamente un proyecto nuevo desde cero mediante entrevista técnica y generación autorizada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-init — solo proyectos nuevos

Este comando es exclusivo para proyectos nuevos. No ofrece ni pregunta modo (new/existing): fija mode: new. Un repositorio que ya contiene código, infraestructura o manifiestos de usuario pertenece a /aikya-analyze. No fuerces new, no sobrescribas archivos y no conviertas un proyecto en nuevo para evitar la protección.

1. Determina la carpeta de trabajo de Claude Code, no el runtime global. Resuelve el CLI por .aikya/runtime/aikya_cli.py, aikya_cli.py o ~/.claude/aikya-harnes/aikya_cli.py. Si no existe, explica cómo instalar Aikya con permiso.
2. Ejecuta python3 <cli> probe --target . antes de la entrevista. Si detecta código, manifiestos o infraestructura ajena al bootstrap gestionado Aikya, termina sin escribir y recomienda /aikya-analyze. Los symlinks y los objetos de usuario no son un directorio nuevo.
3. PRIMERA PREGUNTA: project_type (development, infrastructure o devops). El modo es siempre new, sin segunda pregunta de modalidad.
4. Para development entrevista únicamente el nuevo proyecto: nombre, monorepo/singlerepo, backend, frontend, móvil, frameworks, lenguaje, arquitectura, API, seguridad, base de datos, SDKs, testing, observabilidad, CI, despliegue y patrones, solo en la medida necesaria. No presupongas versiones.
5. Para infrastructure pregunta proveedor, Terraform/OpenTofu, Ansible, entornos, módulos y backend de estado nuevo. No preguntes backend/frontend ni generes apps/. Para devops pregunta origen, Docker/Compose, destino, Helm/Kustomize/YAML, imágenes y puertos; no generes código de aplicación si solo hay infraestructura de despliegue.
6. Genera .aikya/answers.json conforme al esquema legado con project_type, mode: new y las decisiones confirmadas. No solicites credenciales en el chat. Revisa el resumen y pide consentimiento explícito antes de instalar.
7. Comprueba requisitos: python3 <cli> requirements --target . --answers .aikya/answers.json; informa SDKs faltantes, sin instalarlos.
8. Previsualiza python3 <cli> init --target . --answers .aikya/answers.json --dry-run --external plan. Tras aprobación ejecuta init sin --dry-run y sin instalaciones externas automáticas. Solicita consentimiento por separado para descargar dependencias, scaffolding de aplicación, docker build, Terraform init/plan/apply, CI/CD o despliegues.
9. Devuelve los archivos creados, requisitos pendientes y comandos para continuar: /aikya-scaffold plan, /aikya-doctor, /aikya-quality, /aikya-feature. Las pruebas deben reflejar resultados reales, nunca inferidos.
10. Selecciona automáticamente solo agentes y skills relevantes del catálogo. Ofrece /aikya-models como opción separada; por defecto Opus para planner/orchestrator e inherit para ingenieros, Haiku 5.5 deshabilitado salvo autorización explícita y acceso compatible.

No escribas código de proyecto ni cambies permisos cuando el usuario solo pidió plan. Conserva la semántica de infrastructure y devops sin forzar aplicaciones.
