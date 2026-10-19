---
name: ansible-automation
description: "Gestionar configuración de servidores con Ansible: roles, inventories, idempotencia, Vault y validación segura."
---

# ansible-automation

Esta skill es una capacidad selectiva de Aikya Engineering: se activa según el stack y el perfil Infrastructure & DevOps. No ejecuta cambios remotos por sí sola.

## Diagnóstico
- Identifica hosts, sistema operativo, conectividad, privilegios y alcance del inventario sin ejecutar tareas remotas.
- Reutiliza roles y colecciones existentes; evita duplicar configuraciones.
## Diseño
- Roles idempotentes con módulos fully-qualified, handlers y separación de variables por entorno.
- Nunca incluyas secretos en inventarios versionados; usa Vault o gestor aprobado.
- No desactives host-key checking, no uses shell indiscriminadamente, no aceptes escalación implícita.
## Verificación
- Primero `ansible-playbook --syntax-check` y `ansible-lint` si están disponibles.
- `--check` también puede conectar a servidores y no implica ausencia total de efectos: pide autorización específica.
- Antes de ejecutar un playbook, muestra inventario, límite, tags, posible elevación de privilegios y plan de recuperación.
## Entrega
Informe de archivos, hosts objetivo, tareas, verificación real y pasos pendientes.

## Guardrails
- Analiza fuentes reales y declara hipótesis; no inventes pruebas ni métricas.
- No ejecutes herramientas remotas ni comandos destructivos sin consentimiento específico.
- Respeta archivos personalizados y produce documentación en `aikya/docs/infrastructure/` cuando cambia la infraestructura.
