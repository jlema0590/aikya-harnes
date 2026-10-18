# Auditoría de integración del paquete de agentes y skills

Origen revisado: archivo de usuario `claude-agentes-y-skills-sin-linkedin.zip`, fechado en octubre de 2026.

## Inventario revisado

| Tipo | Total del ZIP | Excluidos | Duplicados | Integrados al catálogo |
|---|---:|---:|---:|---:|
| Agentes | 19 | 6 jurídicos | 1 `security-reviewer` | 12 |
| Agent Skills | 21 | 6 jurídicas | 0 | 15 |

**Exclusión completa:** directorio `agents/legal/`, skills `ecommerce-platform-terms`, `legal-research-es-eu`, `legal-risk-matrix`, `privacy-data-processing`, `saas-contract-review` y `software-ip-licensing`. No se incorporó ninguna publicación/skill de LinkedIn.

## Criterios de integración

1. **Compatible**: archivos Markdown de Claude Code, con frontmatter `name`/`description` y instrucciones de trabajo técnico.
2. **Sin duplicar**: Aikya conserva su `security-reviewer`; el material del agente importado no lo reemplaza.
3. **Cargado por stack**: sólo se activan agentes/skills útiles para la entrevista y los manifests detectados (Node, Next, Vue, Flutter, Astro, CI/CD, Docker, Kubernetes, Cloud).
4. **Dependencias externas opcionales**: las referencias a `frontend-design`, `web-design-guidelines`, `writing-plans`, `brainstorming`, `test-driven-development` y `systematic-debugging` se retiraron del preloading de los agentes para no exigir software ausente ni consumir contexto innecesario.
5. **Sin acciones ocultas**: se importa Markdown, no el `install.sh` del paquete original. El instalador local no ejecuta comandos de terceros ni actualiza SDKs.
6. **Idempotencia**: las instalaciones repetidas conservan archivos personalizados y rechazan nombres ajenos al catálogo.
7. **Trazabilidad**: `docs/agents.md`, `docs/skills.md` y `.harness/engineering-catalog.json` documentan la disponibilidad, no afirman invocaciones no verificadas.

## Pendiente de validación real

Probar invocación de subagentes con distintas versiones de Claude Code, versiones reales de los SDKs por stack, y verificar permisos/licencias de publicación de los textos suministrados en caso de distribuirlos públicamente.
