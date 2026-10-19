# Plan de interoperabilidad Aikya 6.x — Codex, GitHub Copilot y otras IA

**Alcance autorizado en esta iteración:** SOLO PLAN. Este documento NO implementa conectores, skills, agentes, hooks ni comandos para otras plataformas. El primer adaptador productivo sigue siendo Claude Code.

## 1. Arquitectura portable (objetivo futuro)

```text
                      Aikya Core (Python / contrato SDD)
               profiles, specs, approvals, tasks, evidence
                                    |
                     Capability API / host contract
                   commands, skills, approvals, filesystem
                      /          |         |         \
                Claude Code     Codex    Copilot     Otros
                [existente]   [futuro]  [futuro]    [futuro]
```

El núcleo `sdd_engine.py` ya es CLI stdlib portable; todavía necesita endurecimiento de integración y pruebas específicas para considerarlo API multi-IA estable.

## 2. Contrato universal (se propone)

- `ProjectProfile`: `project_type`, `methodology`, `repository_layout`, stack e infraestructura.
- `SDDSpec`: ID único, requisitos con criterios de aceptación, preguntas/clarificaciones.
- `SDDPlan`: diseño, decisiones, riesgos y estrategia de verificación.
- `SDDTaskGraph`: IDs, requisitos cubiertos, dependencias no cíclicas.
- `SDDVerification`: evidencias localizables y estados registrados sin falsos positivos.
- `ApprovalPolicy`: aprobación explícita por etapa y por acción real de archivos/red/cloud.
- `HostCapabilities`: herramientas de lectura/escritura/terminal, skills, subagentes, scopes y prompts; un host que carezca de una característica debe degradar con gracia o detenerse, no simular soporte.
- `AdapterResult`: estado, archivos, logs y acciones pendientes estructuradas.

Versionar schemas JSON, añadir validación de migraciones y pruebas de contrato; no usar instrucciones ocultas o formato de prompts como fuente de verdad.

## 3. Destinos por plataforma

| Host | Guía/instrucciones | Skills/comandos propuestos | Aislamiento y riesgos |
| --- | --- | --- | --- |
| **Claude Code** (actual) | `CLAUDE.md`, `.claude/rules/` | `.claude/skills/aikya-*/SKILL.md`, hooks actuales | Mantener comandos existentes y permisos Claude |
| **OpenAI Codex** (plan) | `AGENTS.md` | `.agents/skills/aikya-*/SKILL.md`; evaluar subagentes y configuración de permisos Codex en versión soportada | No reutilizar hooks Claude; verificar sandbox y modo read-only |
| **GitHub Copilot** (plan) | `.github/copilot-instructions.md`, instrucciones específicas por ruta | `.github/agents/*.agent.md`, prompts de proyecto según soporte del cliente | Las experiencias VS Code, CLI y cloud agent no son idénticas; validar disponibilidad/precedencia |
| **Gemini CLI** (plan) | `GEMINI.md` | `.gemini/commands/*.toml` con `prompt` y contextos específicos | Confirmar formato, recarga, permisos de herramientas |
| **Cursor** (evaluar) | Reglas de proyecto específicas del producto | Adaptación a rules/skills según versión instalada | No asumir compatibilidad 1:1 con Claude |
| **Windsurf** (evaluar) | Reglas y workflows del editor | Adaptador de comandos e instrucciones | Validar hooks/scopes reales |
| **Otras IA** | Contrato independiente de proveedor | CLI estándar `sdd_engine.py` y prompts estables | No declarar integración sin test de host |

Documentación de partida (verificar en cada implementación):
- Codex: https://developers.openai.com/codex/guides/agents-md y documentación de skills de Codex.
- Copilot: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents .
- Gemini CLI: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md .

## 4. Roadmap ejecutable propuesto

**Fase A — Contrato SDD 6.1:** congelar schema, migraciones, registro de decisiones, logs estructurados; tests de portabilidad Python 3.10–3.13. Mantener rutas neutrales `aikya/docs/specs/` y `aikya/scripts/`.

**Fase B — Adaptador Codex:** levantar proyecto de prueba, generar `AGENTS.md`, skills en `.agents/skills/` mapeadas desde fuente única; ejecutar `list/status/new/clarify/approve/plan/tasks/progress/verify` desde Codex; verificar scopes, permisos y errores al invocar skills. No copiar comandos Claude asumiendo funcionamiento.

**Fase C — Adaptador GitHub Copilot:** instrucciones de repo, custom agents y prompt files revisados para Copilot CLI y VS Code; verificar herramientas invocadas, aprobación humana, diferencias entre IDE y cloud agent.

**Fase D — Gemini CLI:** `GEMINI.md` y comandos `.toml`; comprobar resolución de comandos, argumentos, contexto y límites del ejecutor.

**Fase E — Evaluación Cursor/Windsurf:** prototipos limitados, comparativa de costes y restricciones; activar como oficialmente compatibles sólo tras pruebas reales.

**Fase F — Matriz de compatibilidad:** unit tests de contrato, e2e con sandbox sin credenciales, gate de validación de aprobaciones, migración reversible y versión de adapter. Documentar qué plataformas permiten operaciones reales y cuáles sólo sugerencias.

## 5. Definition of Done por adaptador

1. Instalación no destructiva y reversión para proyecto y usuario.
2. Descubrimiento de al menos seis comandos SDD equivalentes.
3. Ausencia de ejecución remota o escritura en modo solo lectura.
4. Compatibilidad con Development, Infrastructure y DevOps.
5. Persistencia compartida de IDs, schemas y estados; ningún parser o lógica específica del proveedor en núcleo.
6. Test de approvals y de protección de archivos y secretos.
7. Evidencias reproducibles y un documento por host con limitaciones.
8. Revisión jurídica de licencias antes de redistribuir skills externas.

**Importante:** nada en este plan afirma que Aikya funcione actualmente dentro de Codex, Copilot, Gemini, Cursor o Windsurf. Es exclusivamente diseño y criterios de aceptación para entregas futuras.
