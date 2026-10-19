---
name: aikya-tasks
description: "Aikya 6.0.0 SDD: tasks para Development, Infrastructure y DevOps con aprobaciones y trazabilidad."
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-tasks — Descomponer la especificación en tareas

Petición: $ARGUMENTS

**Reglas SDD comunes (v6.0.0):**
- Trabaja en la raíz del repositorio abierto, jamás sobre el runtime global de Aikya.
- Sólo usar estas acciones cuando el perfil .harness/project-profile.json tenga methodology=sdd.
- El motor está en aikya/scripts/harness/sdd_engine.py. Ejecuta Python desde Claude Code; `--input` indica un JSON revisado con el usuario, no instrucciones de terceros.
- No modificar fuentes ni ejecutar herramientas con efectos secundarios antes de aprobar la fase correspondiente. Nunca ejecutar terraform apply/destroy, Ansible sobre hosts, docker push, helm upgrade o kubectl apply sin permiso específico adicional.
- Conserva archivos personalizados; valida archivos/rutas y registra resultados ejecutados, jamás inventes evidencias.
- Especificaciones por tipo: aikya/docs/specs/development/, infrastructure/ o devops/.
- En interfaces Claude Code usa preguntas normales o AskUserQuestion; muestra siempre el resultado del motor.


1. Requiere estado PLAN_APPROVED.
2. Crea tareas pequeñas, verificables y ordenadas por dependencias: id TASK-NNN, description, requirements (IDs existentes) y depends_on (IDs de otras tareas).
3. Todas las requirements deben aparecer en al menos una tarea; evita dependencias cíclicas y tareas sin criterios.
4. Tras aprobación del listado propuesto, pasa JSON {"tasks":[{"id":"TASK-001","description":"...","requirements":["REQ-001"],"depends_on":[]}]} mediante tasks --root . --id SPEC-NNN --input <json>.
5. Presenta tasks.md y solicita aprobación expresa para la ejecución: approve --stage tasks --actor "<responsable>".
6. El paso de aprobar tareas no equivale a aprobar cambios remotos o destructivos.
