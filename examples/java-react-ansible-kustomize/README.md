# java-react-ansible-kustomize

Monorepo Java Spring + React, Ansible y Kustomize on-premise. Las aplicaciones se generan por separado; los inventarios Ansible empiezan sin hosts y los manifiestos usan una imagen/puerto de ejemplo que hay que sustituir antes de desplegar.\n
Abre Claude Code, utiliza `/aikya-answers` con el archivo `answers.json` y revisa las decisiones. Después consulta `/aikya-infra-project plan`. La generación exige aprobación; no se realizan despliegues remotos.

Diagnostica el entorno con `/aikya-doctor` y revisa los especialistas activados mediante `/aikya-skills-status` antes de aprobar la creación de infraestructura.
