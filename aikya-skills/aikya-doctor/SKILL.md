---
name: aikya-doctor
description: Diagnostica versiones y requisitos de Java, .NET, Node, Android o iOS de un proyecto Aikya desde Claude Code, sin instalar nada.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-doctor — Revisión de SDKs

1. Resuelve el CLI Aikya igual que en `/aikya-init`, priorizando `.aikya/runtime/aikya_cli.py`, luego `aikya_cli.py`, luego `$HOME/.claude/aikya-harnes/aikya_cli.py`.
2. Ejecuta `python3 <cli> requirements --target .` (si hay JSON aún no aplicado, añade `--answers .aikya/answers.json`).
3. Expón versiones instaladas, versiones solicitadas, rutas oficiales y bloqueos. Para proyectos existentes comprueba también los manifiestos y versiones indicadas por el proyecto.
4. No instales ni actualices SDKs sin permiso. No afirmes que una app compila a partir de `--version`; si faltan herramientas, no ejecutes el scaffolding.

5. Para infraestructura revisa únicamente las herramientas seleccionadas en `infrastructure`. Node `v25.9.0` debe detectarse como `25.9.0`, pero que esté instalado no implica compatibilidad con la versión de Next/Angular: contrasta engines y versiones solicitadas. No confundas un bug de parseo con una incompatibilidad real.
6. Tras actualizar una instalación anterior, confirma que el detector del runtime y `aikya/scripts/harness/aikya_requirements.py` estén sincronizados; no edites directamente copias gestionadas ni omitas restricciones de seguridad.
