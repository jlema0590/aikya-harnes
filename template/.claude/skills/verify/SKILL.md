---
name: verify
description: Ejecuta los quality gates del repositorio e informa evidencias y verificaciones pendientes.
---

# Verificar cambios

1. Confirma repositorio y archivo `harness.json`.
2. Ejecuta `python3 aikya/scripts/harness/run_checks.py` desde la raíz del repo.
3. Ejecuta las pruebas focalizadas pertinentes para el cambio, si están disponibles y son seguras.
4. Informa: comandos exactos, éxito/fallo, omitidos, bloqueantes y riesgos.
5. Si algún check obligatorio figura como `NOT_CONFIGURED` o falla, no declares entrega validada.
6. No hagas commit, push ni despliegue.
7. Ejecuta `python3 aikya/scripts/harness/docs_guard.py base` y revisa el estado de documentación de la petición antes de cerrar. No consideres aprobada la revisión si falta `aikya/docs/changes/REQ-*.md` cuando hay cambios técnicos.
