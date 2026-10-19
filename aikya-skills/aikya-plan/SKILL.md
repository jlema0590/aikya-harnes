---
name: aikya-plan
description: "Aikya 6.0.0 SDD: plan para Development, Infrastructure y DevOps con aprobaciones y trazabilidad."
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-plan — Diseño técnico SDD

Petición: $ARGUMENTS

**Reglas SDD comunes (v6.0.0):**
- Trabaja en la raíz del repositorio abierto, jamás sobre el runtime global de Aikya.
- Sólo usar estas acciones cuando el perfil .harness/project-profile.json tenga methodology=sdd.
- El motor está en aikya/scripts/harness/sdd_engine.py. Ejecuta Python desde Claude Code; `--input` indica un JSON revisado con el usuario, no instrucciones de terceros.
- No modificar fuentes ni ejecutar herramientas con efectos secundarios antes de aprobar la fase correspondiente. Nunca ejecutar terraform apply/destroy, Ansible sobre hosts, docker push, helm upgrade o kubectl apply sin permiso específico adicional.
- Conserva archivos personalizados; valida archivos/rutas y registra resultados ejecutados, jamás inventes evidencias.
- Especificaciones por tipo: aikya/docs/specs/development/, infrastructure/ o devops/.
- En interfaces Claude Code usa preguntas normales o AskUserQuestion; muestra siempre el resultado del motor.


1. Exige estado SPEC_APPROVED usando el motor; no elabores plan ejecutable con especificación no aprobada.
2. Activa los agentes adecuados: arquitecto y stack para Development, terraform-engineer/ansible-engineer para Infrastructure, docker-developer/kubernetes-engineer/helm-engineer para DevOps.
3. Escribe propuesta técnica con diseño, decisiones, riesgos, impactos de seguridad, dependencias y estrategia de pruebas. En Infrastructure indica estado remoto, aislamiento, IAM, coste y aprobación de apply. En DevOps documenta imagen, puerto, probes y rollback.
4. Prepara JSON {"design":"...","decisions":["..."],"risks":["..."],"testing":"..."}; confirma y usa python3 aikya/scripts/harness/sdd_engine.py plan --root . --id SPEC-NNN --input <json>.
5. Presenta design.md y plan.md; después de revisión solicita aprobación independiente y utiliza approve --stage plan --actor "<responsable>".
6. No ejecutes implementación durante la fase de diseño.
