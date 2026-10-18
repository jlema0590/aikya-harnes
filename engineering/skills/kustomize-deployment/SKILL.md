---
name: kustomize-deployment
description: "Definir manifests Kubernetes con bases y overlays Kustomize por entorno, sin acceso a clústeres."
---

# kustomize-deployment

Esta skill es una capacidad selectiva de Aikya Engineering: se activa según el stack y el perfil Infrastructure & DevOps. No ejecuta cambios remotos por sí sola.

## Diseño
- Mantén `base/` libre de secretos y `overlays/<entorno>/` con diferencias mínimas.
- Usa `kustomization.yaml`, recursos versionados y transformaciones justificadas; no dupliques manifiestos enteros.
- Confirma imagen con tag/digest inmutable y puerto real; no supongas DNS, paths de probes o storage.
- Asegura requests/limits, capabilities mínimas, RBAC y namespaces existentes.
## Validación
- Ejecuta `kustomize build` en local y valida el YAML resultante con la herramienta de esquema disponible.
- No ejecutes `kubectl apply` ni acciones en clusters durante validación sin aprobación.
- Documenta diff de overlays, rollback y dependencias externas.

## Guardrails
- Analiza fuentes reales y declara hipótesis; no inventes pruebas ni métricas.
- No ejecutes herramientas remotas ni comandos destructivos sin consentimiento específico.
- Respeta archivos personalizados y produce documentación en `aikya/docs/infrastructure/` cuando cambia la infraestructura.
