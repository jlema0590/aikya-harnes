# Routing y presupuesto de contexto (Harness v4)

- Para cambios de código: reutilización y mínima complejidad según Ponytail si está instalado; no sacrificar validación, seguridad, rendimiento ni accesibilidad.
- Para relaciones entre componentes en repositorios grandes: Graphify CLI local si índice presente y vigente. Consulta específica, valida contra archivos reales; nunca cargues todo `graph.json` ni el informe entero.
- Para cambios de interfaz web o móvil: UI UX Pro Max si está instalado; documenta decisiones de diseño en `aikya/docs/design/design-system.md`, comprueba accesibilidad y pruebas reales.
- Si una skill externa falta, continúa con las skills propias e informa cómo instalarla; nunca lances descargas silenciosas.
- Evita delegación y lecturas masivas si el alcance es reducido. Guía completa bajo `aikya/docs/harness/token-policy.md`, sólo si se necesita.
