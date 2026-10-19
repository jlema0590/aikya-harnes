---
name: aikya-implement
description: "Aikya 6.0.0 SDD: implement para Development, Infrastructure y DevOps con aprobaciones y trazabilidad."
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-implement — Implementación controlada

Petición: $ARGUMENTS

**Reglas SDD comunes (v6.0.0):**
- Trabaja en la raíz del repositorio abierto, jamás sobre el runtime global de Aikya.
- Sólo usar estas acciones cuando el perfil .harness/project-profile.json tenga methodology=sdd.
- El motor está en aikya/scripts/harness/sdd_engine.py. Ejecuta Python desde Claude Code; `--input` indica un JSON revisado con el usuario, no instrucciones de terceros.
- No modificar fuentes ni ejecutar herramientas con efectos secundarios antes de aprobar la fase correspondiente. Nunca ejecutar terraform apply/destroy, Ansible sobre hosts, docker push, helm upgrade o kubectl apply sin permiso específico adicional.
- Conserva archivos personalizados; valida archivos/rutas y registra resultados ejecutados, jamás inventes evidencias.
- Especificaciones por tipo: aikya/docs/specs/development/, infrastructure/ o devops/.
- En interfaces Claude Code usa preguntas normales o AskUserQuestion; muestra siempre el resultado del motor.


1. Requiere /aikya-tasks aprobado y consulta worklist: python3 aikya/scripts/harness/sdd_engine.py worklist --root . --id SPEC-NNN.
2. Asegura consentimiento para los archivos específicos que cambiarás. Para Development usa /aikya-feature y especialistas del lenguaje. Para Infrastructure prepara Terraform/Ansible sin apply. Para DevOps prepara Docker/Compose/Helm/YAML/Kustomize sin desplegar.
3. Trabaja una tarea cada vez respetando dependencias y los archivos del usuario; antes de marcar completada crea evidencia real en archivo dentro del repo (por ejemplo un log de test o reporte de revisión autorizado).
4. Actualiza progress: python3 aikya/scripts/harness/sdd_engine.py progress --root . --id SPEC-NNN --task TASK-001 --result done --evidence <ruta-relativa>.
5. Actualiza documentación viva/ADRs y ejecuta /aikya-quality. Si faltan herramientas, evidencia o aprobación, deja la tarea in_progress y registra pendientes.
6. Los pasos de Terraform plan, helm template y tests son distintos de desplegar. El motor nunca ejecuta implementación por sí mismo.
