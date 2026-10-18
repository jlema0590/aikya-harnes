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
