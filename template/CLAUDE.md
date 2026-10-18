# Contrato de desarrollo del repositorio

## Misión

Entregar cambios mínimos, comprobables y mantenibles que satisfagan los criterios de aceptación.
Respetar el stack y las convenciones reales del repositorio; **no asumir** framework, rutas, paquetes ni comandos.

## Protocolo por tarea

1. **Descubrir**: revisar `README`, documentación, dependencias, estructura, tests, estado Git y `harness.json`.
2. **Aclarar alcance**: escribir criterios de aceptación; si falta un dato, asumir lo mínimo y registrar la hipótesis.
3. **Planificar**: para cambios no triviales, proponer archivos afectados, impacto, riesgos y plan de pruebas.
4. **Implementar**: cambios pequeños, pruebas junto al cambio, no alterar APIs públicas innecesariamente.
5. **Verificar**: ejecutar `python3 scripts/harness/run_checks.py` y las pruebas relevantes del área afectada.
6. **Revisar**: delegar a `qa-reviewer` y/o `security-reviewer` cuando haya riesgo; usar `architect` para cambios de diseño significativos.
7. **Informar**: enumerar archivos modificados, evidencia de tests, riesgos y verificaciones omitidas.

## Reglas no negociables

- Nunca afirmar que una prueba pasó si no se ejecutó y se vio su resultado.
- No modificar secretos, `.env`, claves, credenciales ni datos personales; no mostrarlos en respuestas.
- No desplegar, ejecutar migraciones destructivas, borrar recursos, forzar push ni hacer commits sin aprobación explícita.
- No añadir dependencias nuevas salvo que estén justificadas y compatibles con el proyecto.
- Preservar compatibilidad y manejar errores, timeouts y entrada no confiable cuando corresponda.
- Preferir pruebas deterministas y cambios fáciles de revertir.
- No editar archivos generados: cambia sus fuentes y regenera con el comando del proyecto.
- Si una comprobación obligatoria no está configurada o falla, informar **NO VERIFICADO** o **FALLÓ**; jamás marcar entrega como completamente validada.

## Uso de agentes

- `architect`: evaluación de contratos, modularidad y decisiones importantes (lectura).
- `developer`: implementación acotada con pruebas, coordinada por el agente principal.
- `qa-reviewer`: cobertura, regresiones, límites, fallos y criterios de aceptación (lectura y comandos).
- `security-reviewer`: superficie de ataque, secretos, autorizaciones y dependencias (lectura y comandos).

## Convenciones del proyecto (completar)

- Stack y versión: TODO
- Comandos de arranque: TODO
- Normas de lint/formato: TODO
- Organización de carpetas: TODO
- Estrategia de tests: TODO
- Restricciones de arquitectura: TODO

## Documentación viva y trazabilidad (OBLIGATORIO)

Antes y después de cualquier implementación, revisa `docs/README.md`, `docs/overview.md` y `.claude/rules/01-documentation-policy.md`. Cada petición que modifique código, tests o infraestructura requiere actualizar la documentación afectada y crear `docs/changes/REQ-*.md` con cambios, evidencias reales y documentos actualizados. `UserPromptSubmit` registra la petición y `Stop` verifica la cobertura. No asumir que una edición sin tests ni documentación está lista.

## Ingeniería Bootstrap

En un proyecto nuevo consulta `python3 scripts/harness/scaffold.py plan` y `docs/harness/bootstrap.md`. Los generadores remotos se ejecutan sólo tras aprobación; verificar toolchains, dependencias, módulos, Docker y pipelines reales antes de dar el scaffold por completo. Actualizar `harness.json` tras generar la aplicación.

## Skills y coste de contexto

Aplica `.claude/rules/02-context-budget.md`: Ponytail para cambios mínimos, Graphify (sin MCP) para navegación de dependencias con consultas puntuales y UI UX Pro Max sólo al trabajar con interfaces. Revisa disponibilidad al iniciar sesión; instalaciones de terceros únicamente con aprobación.

## Aikya v5: inicio desde Claude Code
- La entrevista inicial se realiza con `/aikya-init` **en Claude**, no con preguntas de `install.py` en terminal.
- `/aikya-answers` utiliza el perfil JSON aprobado y `/aikya-doctor` verifica SDKs antes de scaffold.
- Prefiere comandos `/aikya-feature`, `/aikya-bugfix`, `/aikya-scaffold`, `/aikya-skills-status`, `/aikya-tests`, `/aikya-docs` y `/aikya-quality`; aliases heredados disponibles. Todo el flujo de usuario ocurre dentro de Claude Code; los scripts se ejecutan internamente cuando corresponda.
- Nunca actualices SDK, interpretes que el build pasó ni ejecutes generadores remotos sin autorización.
