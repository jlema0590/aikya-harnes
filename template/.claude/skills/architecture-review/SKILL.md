---
name: architecture-review
description: Revisa stack, límites backend/frontend/mobile y riesgos de diseño respecto de la entrevista técnica.
---

1. Lee perfil, código, contratos y decisiones arquitectónicas existentes.
2. Identifica discrepancias entre decisiones y repositorio y delimita incertidumbres.
3. Solicita análisis al agente `architect` cuando sea necesario.
4. Evalúa despliegue, observabilidad, autenticación, persistencia y testing.
5. Emite decisiones propuestas y ADRs sin imponer patrones innecesarios.
Cuando exista un grafo Graphify vigente, consulta vínculos concretos de dependencias en vez de leer todo el código. Verifica decisiones críticas en código fuente y evita crear patrones sin requisitos.
