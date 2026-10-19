---
name: bugfix
description: Diagnostica y corrige un bug con reproducción y prueba de regresión.
disable-model-invocation: true
---

Problema: $ARGUMENTS

1. Localiza el comportamiento y reproduce el fallo (o explica qué falta para reproducirlo).
2. Formula hipótesis y contrástalas con trazas o tests, evitando cambios especulativos.
3. Antes de corregir, escribe una prueba que falle cuando sea viable.
4. Implementa la corrección mínima y comprueba la regresión.
5. Ejecuta `/verify` o `python3 aikya/scripts/harness/run_checks.py` y comunica resultados, riesgos y pruebas pendientes.
6. Actualiza `aikya/docs/bugs/index.md` con síntoma, causa raíz confirmada/hipótesis y prueba de regresión. Revisa si seguridad, feature o arquitectura también se ven afectados. Crea `aikya/docs/changes/REQ-*.md`.
**Contexto eficiente:** usa análisis mínimo y Ponytail para evitar correcciones especulativas; consulta Graphify sólo para rutas de dependencias transversales si el índice existe. En bugs de interfaz usa UI UX Pro Max sólo cuando afecte el diseño/UX.
