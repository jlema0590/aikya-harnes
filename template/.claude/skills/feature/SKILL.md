---
name: feature
description: Construye una feature desde requisitos hasta pruebas y revisión, sin desplegar ni hacer commits.
disable-model-invocation: true
---

# Feature workflow

Solicitud: $ARGUMENTS

1. Inspecciona el código y traduce la solicitud a criterios de aceptación observables.
2. Si es un cambio no trivial, pide a `architect` una revisión de diseño en solo lectura.
3. Presenta un plan de implementación breve; implementa por pasos pequeños directamente o con `developer` si conviene aislamiento. Evita modificar los mismos archivos en paralelo.
4. Crea/actualiza pruebas que demuestren el comportamiento solicitado.
5. Ejecuta `/verify` o `python3 aikya/scripts/harness/run_checks.py` y pruebas focalizadas.
6. Usa `qa-reviewer`, y `security-reviewer` si toca autorización, red, datos o infraestructura.
7. Entrega resumen, comandos/resultados reales, limitaciones y riesgos. No hagas push ni despliegues.
8. Actualiza `aikya/docs/features/index.md` y `aikya/docs/plan/roadmap.md` con alcance/estado; si cambia arquitectura o seguridad actualiza sus páginas y ADR. Crea `aikya/docs/changes/REQ-*.md` para esta petición con archivos concretos y evidencias.
**Contexto eficiente:** aplica reutilización Ponytail si está instalada; usa consultas puntuales de Graphify para dependencias complejas (si existe índice); para cambios visuales web/móvil usa UI UX Pro Max y actualiza `aikya/docs/design/design-system.md`. No abras graph.json completo.
