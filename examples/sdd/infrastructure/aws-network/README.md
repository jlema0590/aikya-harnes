# Ejemplo SDD — Red AWS con Terraform

`project_type=infrastructure`; activa `methodology=sdd` en /aikya-init o usa /aikya-answers con un perfil revisado.

Este escenario **no ejecuta herramientas**. Orden: especificar con spec.json, aclarar con clarify.json, aprobar spec, crear plan.json, aprobar plan, definir tasks.json y aprobar tasks. El agente implementa la tarea con permiso y aporta evidencias reales; el motor sólo registra estados.

Archivos JSON son ejemplos orientativos: las decisiones cloud/CIDR e IAM requieren validación humana. No se incluyen pruebas ejecutadas ni resultados inventados.
