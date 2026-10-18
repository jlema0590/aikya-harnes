# Ejemplos Aikya

Cada carpeta contiene `answers.json` con `repository_layout` (`monorepo` o `singlerepo`) y su README técnico. Usa `/aikya-answers` dentro de Claude Code para revisar un ejemplo; no se instalan dependencias ni se generan apps sólo por abrirlo.

- `next-react`: singlerepo, Next.js + React integrado en la raíz.
- `android-kotlin`: singlerepo, Android nativo.
- `existing-java-api`: singlerepo, sólo se analiza el repositorio existente sin reorganizarlo.
- `java-react-clean`, `dotnet-vue`, `python-angular`, `node-react-microservices`: monorepos con apps separadas.

- `next-react-terraform-helm`: singlerepo, Next.js/React, Terraform, Docker/Compose y Helm.
- `java-react-ansible-kustomize`: monorepo Java/React con Ansible y Kustomize.

En estos dos ejemplos, los archivos de despliegue se generan sólo tras la aprobación del plan y cuando los requisitos de imágenes/puertos y versiones están confirmados.

## Modos autónomos v5.8

- `infra-terraform-only`: Terraform AWS sin aplicación.
- `infra-ansible-only`: Ansible on-prem sin aplicación.
- `devops-docker-compose`: Compose sobre una imagen existente.
- `devops-helm-existing`: reutilización de chart local; requiere Chart.yaml existente en el proyecto destino.
- `devops-kustomize`: Kubernetes con overlays y una imagen existente.

Elige el tipo de proyecto antes del resto de la entrevista. Los perfiles legacy siguen correspondiendo a development. Ningún ejemplo realiza despliegues.
