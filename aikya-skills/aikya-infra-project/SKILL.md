---
name: aikya-infra-project
description: Planifica, genera y valida artefactos de Terraform, Ansible, Docker/Compose y Kubernetes (Helm/YAML/Kustomize) desde Claude Code, con aprobación.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-infra-project — Infrastructure & DevOps

Argumentos: `$ARGUMENTS` (`plan`, `generate`, `validate`). Si faltan, pregunta el objetivo.

1. Trabaja en el directorio del proyecto Claude Code. Requiere `.harness/project-profile.json`, `aikya/scripts/harness/infrastructure.py` y, si existe, `aikya/docs/infrastructure/plan.md`. Si no está inicializado, usa `/aikya-init`.
2. **Plan:** ejecuta `python3 aikya/scripts/harness/infrastructure.py plan` y presenta rutas, dependencias, requisitos pendientes, seguridad, alternativas, efectos y aprobaciones. Este modo es de sólo lectura.
3. **Generate:** presenta primero el plan actual. Solicita consentimiento explícito para CREAR los archivos concretos; después ejecuta `python3 aikya/scripts/harness/infrastructure.py generate --approved`. Nunca interpretes un pedido de plan como consentimiento para generar. Conserva cualquier archivo preexistente y personalizado.
4. **Validate:** ejecuta `python3 aikya/scripts/harness/infrastructure.py validate`; indica PASSED, FAILED o NOT_CONFIGURED. Verifica sólo localmente: fmt, sintaxis Ansible, Compose config, Helm lint/template o Kustomize build. Una validación local no equivale a desplegar.
5. Los Dockerfiles se proponen solamente después del scaffold real y de confirmar manifiestos, lockfiles, runtimes y scripts. Los manifiestos Kubernetes requieren nombre de imagen con tag/digest y puerto real. Nunca generes recursos cloud falsos ni secretos.
6. No ejecutar `terraform apply/destroy/init` contra recursos remotos, playbooks contra hosts reales, Docker push, kubectl apply/delete o Helm install/upgrade/uninstall sin una autorización específica adicional.
7. Selecciona agentes y skills del catálogo `engineering/` según `infrastructure`: Terraform, Ansible, Docker/Compose, Kubernetes/Helm/Kustomize; no cargues todos.
8. Documenta cambios en `aikya/docs/infrastructure/`, `aikya/docs/operations/deployment.md` y `aikya/docs/changes/REQ-*.md`, ejecuta `/aikya-quality` y reporta evidencias verificadas.

## Inicialización por modo (v5.8)

- `development`: infraestructura es opcional. El código de aplicación se genera mediante /aikya-scaffold antes de derivar Dockerfile.
- `infrastructure`: Terraform/OpenTofu y/o Ansible sin aplicación. Nunca exijas Node, Java ni monorepo; no generes `apps/`.
- `devops`: origen código/imagen/chart/manifests. Compose puede basarse en una imagen existente sin Dockerfile. Kubernetes puede emplear YAML, Helm (nuevo o existente) o Kustomize. Para Helm existente comprueba `helm_chart_path` local, renderiza/lint sólo con la herramienta disponible y no sobrescribas el chart.
- `mode=new/existing` se elige después del modo y no es una cuarta categoría.
