---
name: helm-deployment
description: "Crear, revisar y validar Helm charts y values por entorno sin desplegar cambios automáticamente."
---

# helm-deployment

Esta skill es una capacidad selectiva de Aikya Engineering: se activa según el stack y el perfil Infrastructure & DevOps. No ejecuta cambios remotos por sí sola.

## Diseño de charts
- Identifica imagen/tag o digest, puertos, namespace, dependencias, probes, secrets y valores por entorno.
- Usa `Chart.yaml`, `values.yaml`, `templates/`, valores override revisados y plantillas legibles.
- No copies credenciales a valores; admite integración de secretos aprobada.
- Incluye recursos, securityContext, RBAC mínimo, graceful shutdown cuando corresponda.
## Verificación
- Ejecuta `helm lint` y `helm template` en local, revisa YAML renderizado.
- Una plantilla que renderiza no garantiza validez en el cluster ni disponibilidad de recursos.
- No uses `helm upgrade`, `install`, `rollback` o `uninstall` sin autorización específica del cluster/namespace.
## Entrega
Documenta release, versiones, valores afectados, comparativa y rollback.

## Guardrails
- Analiza fuentes reales y declara hipótesis; no inventes pruebas ni métricas.
- No ejecutes herramientas remotas ni comandos destructivos sin consentimiento específico.
- Respeta archivos personalizados y produce documentación en `aikya/docs/infrastructure/` cuando cambia la infraestructura.
