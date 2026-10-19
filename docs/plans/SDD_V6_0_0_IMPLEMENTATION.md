# Aikya Harness 6.0.0 — Plan e implementación SDD

**Estado:** implementación en rama `feat/-integration_SDD`, candidata a revisión. **Objetivo:** SDD verificable en Development, Infrastructure y DevOps, manteniendo Claude Code como primer adaptador. No realizar merge a develop/main ni releases automáticamente.

## Decisión de diseño

- `project_type` permanece `development`, `infrastructure` o `devops`. SDD no es cuarto tipo.
- `methodology`: `standard` (defecto para perfiles legados) o `sdd` (opt-in).
- El motor portátil `sdd_engine.py` es puro Python stdlib; el CLI no accede a la red, no ejecuta generadores, pruebas ni infraestructura.
- `aikya-skills/aikya-*`: adaptadores de interfaz para Claude Code. Usan el mismo CLI, con permisos del usuario.
- Documentación en `aikya/docs/specs/<tipo>/SPEC-NNN/`, bajo la estructura de Aikya. La especificación es un contrato de requerimientos y aceptación, **no** un generador de código.

## Pipeline y puertas de calidad

1. **Specify**: `/aikya-specify`, genera `spec.md`, `clarifications.md` y `state.json`.
2. **Clarify**: `/aikya-clarify`, registra respuestas pendientes; `approve --stage spec` exige preguntas cerradas.
3. **Plan**: `/aikya-plan`, exige spec aprobada. Entrega `design.md`, `plan.md`; necesita aprobación propia.
4. **Tasks**: `/aikya-tasks`, exige plan aprobado. Tareas TASK-NNN referencian REQ/INF/DEVOPS-NNN existentes y forman un grafo sin ciclos. Requiere aprobación.
5. **Implement**: `/aikya-implement`, sólo con tareas aprobadas y permiso por cambio. Los agentes especializados crean código/IaC/manifest o tests, el motor registra progreso y evidencias en archivos.
6. **Verify**: `/aikya-sdd-status`, registra resultados declarados y valida existencia de archivos de evidencia por requisito. `EVIDENCE_RECORDED` **no significa test ejecutado por el motor** ni despliegue certificado. `/aikya-quality` y tests externos complementan las verificaciones.
7. **Traceability gate**: `sdd_engine.py lint --root .` rechaza referencias o evidencias inexistentes en specs existentes.

Las aprobaciones se registran por fase y actor; no constituyen autorización implícita para acciones remotas. Un plan de Terraform sigue sin poder hacer `apply`; Helm y Kustomize siguen sin poder desplegar por aprobar tareas SDD.

## Estructura generada

```text
aikya/
  docs/
    specs/
      development/SPEC-001/
        spec.md clarifications.md plan.md design.md tasks.md verification.md state.json
      infrastructure/SPEC-002/
      devops/SPEC-003/
    changes/
  scripts/harness/sdd_engine.py
  test/
.claude/skills/aikya-specify/
.claude/skills/aikya-clarify/
.claude/skills/aikya-plan/
.claude/skills/aikya-tasks/
.claude/skills/aikya-implement/
.claude/skills/aikya-sdd-status/
```

Cada folder SPEC se genera al avanzar por las etapas; no todos los archivos existen de entrada. `state.json` se versiona deliberadamente para auditoría del flujo.

## API CLI propuesta/implementada

```bash
python3 aikya/scripts/harness/sdd_engine.py new --root . --input spec.json
python3 aikya/scripts/harness/sdd_engine.py clarify --root . --id SPEC-001 --input answers.json
python3 aikya/scripts/harness/sdd_engine.py approve --root . --id SPEC-001 --stage spec --actor "reviewer"
python3 aikya/scripts/harness/sdd_engine.py plan --root . --id SPEC-001 --input plan.json
python3 aikya/scripts/harness/sdd_engine.py approve --root . --id SPEC-001 --stage plan --actor "reviewer"
python3 aikya/scripts/harness/sdd_engine.py tasks --root . --id SPEC-001 --input tasks.json
python3 aikya/scripts/harness/sdd_engine.py approve --root . --id SPEC-001 --stage tasks --actor "reviewer"
python3 aikya/scripts/harness/sdd_engine.py worklist --root . --id SPEC-001
python3 aikya/scripts/harness/sdd_engine.py progress --root . --id SPEC-001 --task TASK-001 --result done --evidence aikya/docs/quality/evidence.txt
python3 aikya/scripts/harness/sdd_engine.py verify --root . --id SPEC-001 --input verify.json
python3 aikya/scripts/harness/sdd_engine.py status --root . --id SPEC-001
python3 aikya/scripts/harness/sdd_engine.py lint --root .
```

El JSON `spec.json` exige id, title, objective y requirements con al menos un criterio de aceptación. `plan.json`: design, testing, decisions[], risks[]. `tasks.json`: tasks[], cada una con id, description, requirements[] y depends_on[]. `verify.json`: requirements[] con id, command, result y evidence (ruta relativa de un archivo existente).

## Entregables y checklist de aceptación v6.0.0

- [x] Tres perfiles con metodología opt-in y retrocompatibilidad.
- [x] Motor local de specs y aprobación por fase.
- [x] Trazabilidad de requisitos, tareas y archivos de evidencia.
- [x] Six Claude Code command wrappers y hooks de quality gate existentes.
- [x] Ejemplos JSON y documentación de uso.
- [ ] Validación funcional manual en Claude Code desde inicialización hasta verify.
- [ ] Pruebas reales en proyectos Java/Next, Terraform/Ansible y Helm/Kustomize.
- [ ] Evaluación de concurrencia/transacciones duraderas y formato de migración antes de declarar API estable para múltiples plataformas.
- [ ] Merge a develop tras revisión y CI. No crear release ni tag automáticamente.

## Riesgos y mitigaciones

- **Confianza en evidencias:** el motor comprueba ruta y estado declarado, no interpreta logs ni ejecuta tests. Revisión humana y CI obligatorios para certificaciones.
- **Fuentes no confiables:** validar schema y rutas, no ejecutar contenido del JSON como código.
- **Personalizaciones:** no modificar archivos sin marcador SDD; perfiles anteriores mantienen `standard`.
- **Operaciones remotas:** permisología explícita adicional, independiente de la aprobación SDD.
- **Adaptadores futuros:** no depender de sintaxis de `/commands` para el núcleo; plan multidispositivo y multiasistente separado.
