---
name: project-init
description: Convierte las decisiones de la entrevista en un plan ejecutable para crear un proyecto o módulo nuevo.
disable-model-invocation: true
---
# Inicialización guiada del proyecto
Solicitud: $ARGUMENTS

1. Lee `.harness/project-profile.json`, `.claude/rules/00-project-profile.md` y `docs/harness/bootstrap.md`.
2. Distingue decisiones confirmadas de opciones pendientes (framework Node, versiones LTS, gestor, esquema móvil, CI).
3. Antes de ejecutar un generador remoto, consulta al usuario y explica artefactos que se crearán.
4. Usa los generadores oficiales vigentes y ejecuta en carpetas vacías; evita sobrescribir código del usuario.
5. Configura scripts reales de pruebas y adapta `harness.json` (no uses checks inventados).
6. Ejecuta quality gates y presenta evidencia; no despliegues ni publiques.
7. Genera `docs/` (si aún no existe) y sincroniza overview, roadmap, arquitectura, despliegue, observabilidad, decisiones ADR y la bitácora de petición al finalizar el scaffold. Prefiere `/project-bootstrap` para planificar y ejecutar generadores con consentimiento.
