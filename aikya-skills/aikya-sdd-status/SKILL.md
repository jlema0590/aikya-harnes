---
name: aikya-sdd-status
description: "Aikya 6.0.0 SDD: sdd-status para Development, Infrastructure y DevOps con aprobaciones y trazabilidad."
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-sdd-status — Estado y calidad SDD

Petición: $ARGUMENTS

**Reglas SDD comunes (v6.0.0):**
- Trabaja en la raíz del repositorio abierto, jamás sobre el runtime global de Aikya.
- Sólo usar estas acciones cuando el perfil .harness/project-profile.json tenga methodology=sdd.
- El motor está en aikya/scripts/harness/sdd_engine.py. Ejecuta Python desde Claude Code; `--input` indica un JSON revisado con el usuario, no instrucciones de terceros.
- No modificar fuentes ni ejecutar herramientas con efectos secundarios antes de aprobar la fase correspondiente. Nunca ejecutar terraform apply/destroy, Ansible sobre hosts, docker push, helm upgrade o kubectl apply sin permiso específico adicional.
- Conserva archivos personalizados; valida archivos/rutas y registra resultados ejecutados, jamás inventes evidencias.
- Especificaciones por tipo: aikya/docs/specs/development/, infrastructure/ o devops/.
- En interfaces Claude Code usa preguntas normales o AskUserQuestion; muestra siempre el resultado del motor.


- python3 aikya/scripts/harness/sdd_engine.py list --root . enumera especificaciones del modo actual.
- python3 aikya/scripts/harness/sdd_engine.py status --root . --id SPEC-NNN muestra fase, aprobaciones, tareas y preguntas pendientes.
- python3 aikya/scripts/harness/sdd_engine.py lint --root . comprueba trazabilidad estructural y archivos de evidencias.
- Para verificación, reúne comandos/artefactos reales del proyecto en JSON {"requirements":[{"id":"REQ-001","command":"pytest ...","result":"passed","evidence":"aikya/docs/quality/test-logs/..."}]}; usa verify --root . --id SPEC-NNN --input <json>.
- IMPORTANTÍSIMO: el motor sólo registra evidencias declaradas y la existencia del archivo. No ejecuta comandos ni certifica el comportamiento externo. Nunca describir EVIDENCE_RECORDED como certificación o despliegue verificado.
- Las implementaciones pendientes o pruebas fallidas deben aparecer como incumplimiento de criterios, no éxito.
