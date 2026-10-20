# Routing y presupuesto de contexto (Harness v4)

- Para cambios de código: reutilización y mínima complejidad según Ponytail si está instalado; no sacrificar validación, seguridad, rendimiento ni accesibilidad.
- Para relaciones entre componentes en repositorios grandes: Graphify CLI local si índice presente y vigente. Consulta específica, valida contra archivos reales; nunca cargues todo `graph.json` ni el informe entero.
- Para cambios de interfaz web o móvil: UI UX Pro Max si está instalado; documenta decisiones de diseño en `aikya/docs/design/design-system.md`, comprueba accesibilidad y pruebas reales.
- Si una skill externa falta, continúa con las skills propias e informa cómo instalarla; nunca lances descargas silenciosas.
- Evita delegación y lecturas masivas si el alcance es reducido. Guía completa bajo `aikya/docs/harness/token-policy.md`, sólo si se necesita.

## Higiene de salidas de herramientas (Aikya v6)

- Antes de volcar contenido, usa `rg`, `Glob`, rangos de `Read` o `sed -n`; evita imprimir archivos enteros cuando solo necesitas una sección.
- En `gh api` utiliza `--jq` con campos explícitos; para Git usa `git diff --stat` y diffs por ruta antes del diff completo.
- En logs y tests preserva errores y su contexto, filtra ruido y acota la salida por bytes o líneas sin ocultar fallos.
- Si la salida puede ser grande, divide en lotes y resume con evidencia verificable; no delegues a un modelo si un filtro determinista resuelve la tarea.
- La compactación es una decisión por límite de contexto y fase, no un umbral universal; conserva requisitos, decisiones y pruebas pendientes.
