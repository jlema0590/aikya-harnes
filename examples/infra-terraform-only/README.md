# infra-terraform-only

Terraform-only para infraestructura AWS sin código de aplicación. Aikya prepara la estructura, no crea redes, permisos ni recursos cloud sin especificaciones.

Abre el proyecto desde Claude Code y solicita `/aikya-answers` para cargar las decisiones del ejemplo. Ejecuta `/aikya-doctor` y consulta `/aikya-skills-status` para verificar las herramientas y los especialistas seleccionados. Luego usa `/aikya-infra-project plan`. Autoriza por separado la generación (`generate`) y valida con `/aikya-infra-project validate`; nunca despliegues automáticamente.

El JSON es un ejemplo de configuración. No contiene credenciales, aplicaciones compiladas ni recursos cloud reales.
