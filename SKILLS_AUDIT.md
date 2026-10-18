# Auditoría de skills y estrategia de consumo de tokens — Harness v4

Fecha de revisión: 2026-10-18. Fuentes: documentación publicada en GitHub por los mantenedores y [Agent Skills Specification](https://agentskills.io/specification). Revisión del harness local y pruebas sintácticas incluidas. No se han ejecutado los instaladores upstream por no disponer de conectividad saliente en el entorno donde se preparó este ZIP.

## 1. Comparativa con la especificación

| Requisito Agent Skills | Harness original v3 | v4 |
|---|---|---|
| Carpeta por skill con `SKILL.md` | Sí, 8 skills | Sí, 8 propias + externas instalables |
| YAML frontmatter en primera línea | Sí | Sí, validador de sintaxis básica |
| Nombre válido y coincidente con carpeta | Sí | Sí, verificación automática |
| Descripción no vacía (`description`) | Sí | Sí, verificación automática |
| Funcionalidad específica de Claude Code | `disable-model-invocation: true` | Conservada como extensión, identificada explícitamente |
| Carga progresiva de referencias | Básica, skills breves | Guías largas bajo `aikya/docs/harness` y metadatos breves en skills |
| Validación con `skills-ref` oficial | No incluida | Comando documentado, no ejecutado ni instalado; se usa un linter propio más limitado |

En v3 las ocho skills son: `architecture-review`, `bugfix`, `documentation-sync`, `feature`, `mobile-feature`, `project-bootstrap`, `project-init` y `verify`. Las ocho cumplen el contrato mínimo de directorio/nombre/descripción. La función de `.claude/agents/*.md` no es equivalente a Agent Skills: son **subagentes** con prompt y herramientas, conservados como tales.

## 2. Encaje y activación selectiva

| Operación | Ponytail | Graphify | UI UX Pro Max | Documentación |
|---|---|---|---|---|
| Crear backend o API | Reutilizar código y evitar abstraer prematuramente | Sólo si existen dependencias relevantes en proyecto grande | No | Features, arquitectura, testing |
| Corregir bug | Cambio y regresión mínimos | Dependencias complejas bajo demanda | Sólo bugs visuales | Bugs, pruebas y seguridad si aplica |
| Refactorización o revisión arquitectónica | Simplificar sin romper contratos | Consultas concretas de relaciones | Normalmente no | Arquitectura y ADR |
| Crear pantalla React/Vue/Next | Simplificar componentes, reutilizar | Dependencias si hacen falta | Sí, design system y accesibilidad | Design system, features y pruebas |
| UI Android/iOS/Flutter/RN | Evitar complejidad innecesaria | Opcional para módulos complejos | Sí, con convenciones específicas de plataforma | Design system y pruebas por plataforma |
| Infra, SRE, CI/CD | Evitar complejidad sin necesidad | Mapa de dependencias sólo si aporta valor | No | Deploy, observabilidad, seguridad |
| Consulta sin modificaciones | Sólo si pertinente | Consultas focalizadas si hay grafo | No por defecto | No forzar cambios documentales |

## 3. Política operativa para reducir tokens

- **Evita cargas completas**: Graphify se consulta con una pregunta acotada y se comprueba el código fuente; nunca se vuelca `graph.json` a la conversación.
- **No reindexar por prompt**: indexar código una vez y actualizar cuando haya cambios relevantes. Generar aikya/docs/PDFs semánticos puede usar el modelo y no es «gratis».
- **No invocar las tres skills siempre**: sus descripciones breves pueden estar disponibles, pero el contenido completo sólo cuando una tarea las necesita.
- **Evitar especialización innecesaria**: subagentes sólo si hay un análisis complejo o revisión independiente que justifica coste adicional.
- **Mantener pruebas y seguridad**: un menor número de líneas o tokens no equivale a mejor calidad sin evidencia.

### Benchmark propuesto

Medir un conjunto estable de tareas (por ejemplo 10 bugs, 10 features y 10 peticiones UI), con cuatro variantes: harness sin externos, +Ponytail, +Graphify, +UI Pro Max cuando aplique. Para cada una registrar tokens de entrada/salida, coste, duración, tests/quality gates reales, fallos funcionales, regresiones, accesibilidad y cambios documentales. Comparar medianas y distribución, no un caso aislado.

## 4. Procedencia y amenazas

| Integración | Procedencia | Dependencia ejecutable | Instalación en la v4 |
|---|---|---|---|
| Ponytail | `DietrichGebert/ponytail` | Sólo Git para la descarga; se copia el directorio de skill sin ejecutar su código en la instalación | SHA de commit en lock, plugin/band no incluidos |
| Graphify | `Graphify-Labs/graphify`; PyPI `graphifyy` (doble y) | CLI instalado con `uv` o `pipx` | CLI local y skill project-scoped; sin MCP ni Cloud |
| UI UX Pro Max | `nextlevelbuilder/ui-ux-pro-max-skill`; npm `ui-ux-pro-max-cli` | `npx`, con ejecución de paquete upstream | Sólo si existe frontend o móvil en perfil |

Cualquier skill externa puede introducir instrucciones adversas o depender de software vulnerable. Ejecutar los instaladores requiere aprobación explícita; `.harness/external-skills-lock.json` documenta resultados. El instalador respeta directorios preexistentes y los comandos se ejecutan **sin shell**. Las instalaciones npm/PyPI sin versiones fijadas no son bit a bit reproducibles; para empresas se recomiendan espejos de paquetes controlados y versiones/hashes auditados.

## 5. Enlaces oficiales consultados

- [Agent Skills: specification](https://agentskills.io/specification)
- [Agent Skills: source and documentation](https://github.com/agentskills/agentskills)
- [Claude Code: skills](https://code.claude.com/aikya/docs/en/skills)
- [Ponytail](https://github.com/DietrichGebert/ponytail)
- [Graphify](https://github.com/Graphify-Labs/graphify)
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

## Inventario y gobernanza en Aikya v5.2

Cada proyecto inicializado incluye `aikya/docs/skills.md`, generado a partir de `.claude/skills/*/SKILL.md` y del estado de integraciones externas. `/aikya-skills-status` lo sincroniza; `/aikya-skills-plan` analiza dependencias y `/aikya-skills-install` instala únicamente con autorización. El registro indica **disponibilidad y origen**, no ejecución real. Para nuevas fuentes GitHub se exige ruta, nombre que coincida con `SKILL.md` y revisión de su contenido; se recomienda fijar commit. Las skills globales no se atribuyen a un proyecto hasta incorporarlas explícitamente.
