# GitHub Actions y comunidad — Aikya Harness

Estas plantillas se han adaptado al repositorio **`jlema0590/aikya-harness`** y su rama de integración **`develop`**.

## Archivos y comportamiento

| Archivo | Activación | Operación | Permisos |
|---|---|---|---|
| `workflows/tests.yml` | PR o push a `develop`/`main`, manual | Matriz Python 3.10–3.13; sintaxis y unit tests | Lectura |
| `workflows/smoke-stacks.yml` | Cambios relevantes en ejemplos, perfil, catálogo o generadores; manual | Valida todos los `examples/*/answers.json`, selección de agentes, planificación de scaffolding e infraestructura **sin escribir ni desplegar** | Lectura |
| `workflows/check-asset-sync.yml` | Cambios en agents/skills/código de registro; manual | Comprueba nombres, frontmatter, catálogo y los 18 comandos registrados | Lectura |
| `workflows/refresh-catalogs.yml` | Cada lunes y manual | Inventario local de SHA-256, recuentos y recordatorios de licencias; genera artefacto de revisión **sin importar nada** | Lectura |
| `workflows/bump-versions.yml` | **Sólo manual en `develop`** | Prepara un PR de `CHANGELOG.md` con la versión; no publica nada | Escritura sólo en este job |
| `workflows/release.yml` | **Sólo manual en `main`** | Verifica pruebas y crea ZIP de código fuente y `SHA256SUMS`; **no crea release ni tag** | Lectura |

### Rutas auxiliares obligatorias

Los workflows necesitan estos scripts en **la raíz del proyecto**:

- `scripts/ci/check_assets.py`
- `scripts/ci/smoke_profiles.py`
- `scripts/ci/catalog_review.py`
- `scripts/ci/prepare_release.py`

No hay dependencias PyPI, herramientas cloud ni secretos nuevos para las pruebas.

## Cómo instalar

1. Crea las carpetas `.github/workflows/`, `.github/ISSUE_TEMPLATE/` y `scripts/ci/` si no existen.
2. Copia **todo el contenido de este paquete** en la raíz del repositorio.
3. **Importante:** `.github/workflows/tests.yml` reemplaza el workflow de pruebas actual de Aikya. Guarda copia del anterior o revisa el diff antes del commit.
4. Haz commit en una rama de trabajo y crea un PR dirigido a `develop`.
5. Revisa que pasen las pruebas Python, smoke de perfiles y contratos de catálogo.
6. Configura las reglas de protección de rama según los nombres de jobs visibles en GitHub Actions.

## Preparación manual de versiones

1. Documenta los cambios bajo `## Sin publicar` en `CHANGELOG.md`.
2. Ejecuta **Aikya | Prepare changelog release PR (manual)** desde `develop`, con `version=vX.Y.Z`.
3. Revisa y fusiona el PR hacia `develop`. La organización debe permitir a GitHub Actions crear PRs para este flujo; si no, realiza el cambio manualmente.
4. Después de validar y promover cambios a `main`, ejecuta **Aikya | Release package (manual)** desde `main`, con la **misma versión**.
5. Descarga el artefacto de CI, verifica el fichero `SHA256SUMS` y **publica la GitHub Release manualmente** cuando corresponda.
6. Este paquete exige un `LICENSE` en la raíz para permitir el empaquetado público. Revisa además las licencias y atribuciones de terceros antes de distribuir agentes y skills.

## Limitaciones deliberadas

- No se instalan SDKs ni se ejecutan `terraform apply/destroy`, playbooks Ansible, Docker push, Helm install/upgrade ni `kubectl apply`.
- El smoke de DevOps analiza archivos **propuestos**, no despliega clústeres ni verifica conectividad cloud.
- El catálogo es curado manualmente: `refresh-catalogs.yml` **no descarga material externo**, no sustituye skills y no audita jurídicamente las licencias.
- No se publica a NPM ni se modifica automáticamente `main`.
- Para producción, recomienda fijar las acciones de GitHub a SHA completos verificados y habilitar protecciones de rama, especialmente para release.
