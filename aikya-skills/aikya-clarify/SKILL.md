---
name: aikya-clarify
description: "Aikya 6.0.0 SDD: clarify para Development, Infrastructure y DevOps con aprobaciones y trazabilidad."
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-clarify — Clarificar y aprobar requisitos

Petición: $ARGUMENTS

**Reglas SDD comunes (v6.0.0):**
- Trabaja en la raíz del repositorio abierto, jamás sobre el runtime global de Aikya.
- Sólo usar estas acciones cuando el perfil .harness/project-profile.json tenga methodology=sdd.
- El motor está en aikya/scripts/harness/sdd_engine.py. Ejecuta Python desde Claude Code; `--input` indica un JSON revisado con el usuario, no instrucciones de terceros.
- No modificar fuentes ni ejecutar herramientas con efectos secundarios antes de aprobar la fase correspondiente. Nunca ejecutar terraform apply/destroy, Ansible sobre hosts, docker push, helm upgrade o kubectl apply sin permiso específico adicional.
- Conserva archivos personalizados; valida archivos/rutas y registra resultados ejecutados, jamás inventes evidencias.
- Especificaciones por tipo: aikya/docs/specs/development/, infrastructure/ o devops/.
- En interfaces Claude Code usa preguntas normales o AskUserQuestion; muestra siempre el resultado del motor.


1. Consulta python3 aikya/scripts/harness/sdd_engine.py status --root . --id SPEC-NNN y lee spec.md/clarifications.md.
2. Entrevista al usuario hasta resolver ambigüedades de alcance, datos, errores, seguridad, restricciones y criterios verificables.
3. Prepara JSON de la forma {"answers":{"pregunta original":"respuesta aprobada"}} y, tras revisión, usa clarify --root . --id SPEC-NNN --input <json>.
4. No apruebes requisitos con preguntas pendientes. Cuando el usuario confirme expresamente, utiliza approve --root . --id SPEC-NNN --stage spec --actor "<responsable>".
5. Si los requisitos aprobados deben cambiar, crea nueva especificación o revisión planificada; no sobreescribas silenciosamente artefactos aprobados.
