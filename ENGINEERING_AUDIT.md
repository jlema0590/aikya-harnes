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
7. **Trazabilidad**: `aikya/docs/agents.md`, `aikya/docs/skills.md` y `.harness/engineering-catalog.json` documentan la disponibilidad, no afirman invocaciones no verificadas.

## Pendiente de validación real

Probar invocación de subagentes con distintas versiones de Claude Code, versiones reales de los SDKs por stack, y verificar permisos/licencias de publicación de los textos suministrados en caso de distribuirlos públicamente.

## Ampliación de arquitecturas y lenguajes (v5.5)

Material aportado por el usuario: `claude-arquitecturas-lenguajes-agentes-skills.zip` (18/10/2026).
**Importados:** 11 agentes y 11 skills (5 arquitectos, 6 desarrolladores y sus 11 playbooks).
**Destino:** `engineering/agents/` y `engineering/skills/`; se han incorporado solamente los Markdown declarados en el manifiesto del ZIP, **no** su `install.sh`, `validate.py` ni otras utilidades que pudieran ejecutarse.
**Sin duplicaciones:** 23 agentes y 26 skills técnicos en total. Los 18 comandos de `aikya-skills/` no cambian.
**Selección contextual:** stack + arquitectura explícita + opción `architecture_patterns: ["event-driven"]`; event-driven no se impone a microservicios. Los proyectos existentes mantienen sus personalizaciones.
**Ámbitos excluidos:** LinkedIn, Derecho digital, contratos SaaS y propiedad intelectual.
**Licencias:** el ZIP no incluye una licencia de redistribución individual para los textos importados; antes de reutilizarlos comercialmente en un repositorio público, confirmar titularidad y permisos de redistribución con el autor.
**Validación pendiente:** integración interactiva de subagentes y SDK reales en Claude Code, y ejecución de compilaciones de los distintos ejemplos sobre proyectos generados.
