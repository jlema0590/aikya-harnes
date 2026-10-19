---
name: aikya-specify
description: "Aikya 6.0.0 SDD: specify para Development, Infrastructure y DevOps con aprobaciones y trazabilidad."
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-specify — Specify

Petición: $ARGUMENTS

**Reglas SDD comunes (v6.0.0):**
- Trabaja en la raíz del repositorio abierto, jamás sobre el runtime global de Aikya.
- Sólo usar estas acciones cuando el perfil .harness/project-profile.json tenga methodology=sdd.
- El motor está en aikya/scripts/harness/sdd_engine.py. Ejecuta Python desde Claude Code; `--input` indica un JSON revisado con el usuario, no instrucciones de terceros.
- No modificar fuentes ni ejecutar herramientas con efectos secundarios antes de aprobar la fase correspondiente. Nunca ejecutar terraform apply/destroy, Ansible sobre hosts, docker push, helm upgrade o kubectl apply sin permiso específico adicional.
- Conserva archivos personalizados; valida archivos/rutas y registra resultados ejecutados, jamás inventes evidencias.
- Especificaciones por tipo: aikya/docs/specs/development/, infrastructure/ o devops/.
- En interfaces Claude Code usa preguntas normales o AskUserQuestion; muestra siempre el resultado del motor.


1. Comprueba proyecto inicializado y SDD habilitado (en caso contrario solicita /aikya-init o /aikya-answers, sin activarlo sin consentimiento).
2. Pregunta objetivo, actores, interfaces, riesgos y restricciones; distingue tipo Development, Infrastructure o DevOps.
3. Genera o revisa JSON en una ruta temporal dentro del proyecto, con campos id=SPEC-NNN, title, objective, requirements (id REQ-NNN, INF-NNN o DEVOPS-NNN; description y acceptance no vacíos), nonfunctional y questions.
4. Asegura criterios de aceptación observables y no inventes proveedores, CIDR, cuentas, puertos, endpoints, secretos ni resultados.
5. Tras confirmación explícita del contenido del JSON, ejecuta python3 aikya/scripts/harness/sdd_engine.py new --root . --input <ruta-json>.
6. Muestra spec.md y clarifications.md. No apruebes la especificación en el mismo paso por defecto. Si hay preguntas usa /aikya-clarify.
