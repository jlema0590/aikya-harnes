---
name: aikya-models
description: Selecciona modelos por rol, con Haiku 5.5 opcional y compatibilidad v5.9.1.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-models — Model routing v6

1. Preserva el modelo principal y permisos de Claude Code. Recomienda Sonnet 5.5 para trabajo habitual si la sesión utiliza Opus. No cambies /model ni settings globales por tu cuenta.
2. Planner y Orchestrator recomiendan Opus, solo cuando hace falta planificación/coordinación compleja. Ingenieros, QA, seguridad e infraestructura heredan el modelo activo.
3. Ofrece Haiku 5.5 para extracción, clasificación, routing como sugerencia, documentación borrador y resúmenes de logs. Es opt-in: por defecto auxiliary_enabled=false.
4. Verifica proveedor, claude --version (Claude Code >= 2.1.293), acceso real y políticas organizacionales. En Anthropic utiliza el ID exacto claude-haiku-5-5; el alias haiku puede resolver a 4.5 en otros proveedores. No inventes deployment IDs ni ARNs.
5. Muestra primero al usuario los cambios propuestos en .aikya/model-policy.json. Tras aprobación, guarda esquema v2 con auxiliary_model=claude-haiku-5-5, model_provider=anthropic solo si procede, model_access_confirmed únicamente tras confirmación real, require_read_only=true, max_delegation_depth=1, routing_mode=hybrid, fallback_model=inherit. allowed_tasks admite extraction, classification, routing, documentation y log-summary.
6. Política v1 existente: conserva intacto Haiku 4.5, aliases y los permisos; solicita autorización explícita para migrar al esquema v2. Nunca alteres .aikya/answers.json ni .harness/project-profile.json de v5.9.1.
7. Valida con python3 aikya/scripts/harness/token_policy.py --policy .aikya/model-policy.json o el runtime global equivalente. Previsualiza routing con aikya_router.py --request (simulación offline, no invoca LLM).
8. Verifica el modelo realmente ejecutado en /tasks. Si no hay soporte o permisos, retorna inherit sin llamadas caras ni cambios silenciosos.
