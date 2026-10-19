# Contribuir a Aikya Harness

¡Gracias por tu interés en contribuir a Aikya Harness!

Aikya Harness es un proyecto open source orientado a mejorar los flujos de ingeniería de software mediante inteligencia artificial, automatización, arquitectura de software, infraestructura como código y prácticas DevOps.

Valoramos las contribuciones que mejoren la calidad, seguridad, documentación, extensibilidad y experiencia de los desarrolladores.

## 1. Formas de contribuir

Puedes colaborar mediante:

- Reportes de errores.
- Mejoras de documentación.
- Nuevos agentes y Engineering Skills.
- Mejoras en comandos `/aikya-*`.
- Soporte para lenguajes, frameworks y arquitecturas.
- Nuevas integraciones de infraestructura y DevOps.
- Tests, validaciones y automatización.
- Mejoras de seguridad y rendimiento.
- Propuestas de funcionalidades y ejemplos de configuración.

## 2. Antes de empezar

Antes de realizar cambios importantes:

1. Revisa el README y la documentación disponible.
2. Comprueba si existe un Issue relacionado.
3. Si el cambio es significativo, abre un Issue para discutir su alcance.
4. Evita introducir funcionalidades duplicadas.
5. Comprueba que el cambio es compatible con la arquitectura del harness.

Los cambios deben tener una finalidad clara y mantener la coherencia con los objetivos del proyecto.

## 3. Estructura del proyecto

Los principales directorios y archivos son:

| Ubicación | Responsabilidad |
|---|---|
| `aikya-skills/` | Comandos y flujos de trabajo de Aikya |
| `engineering/agents/` | Agentes especializados de ingeniería |
| `engineering/skills/` | Skills técnicas reutilizables |
| `template/` | Plantillas y herramientas del harness |
| `examples/` | Configuraciones de referencia |
| `tests/` | Pruebas automatizadas |
| `install.py` | Inicialización de proyectos |
| `aikya_setup.py` | Instalación y configuración de Aikya |
| `engineering_catalog.py` | Descubrimiento y selección de especialistas |

En los proyectos inicializados por Aikya, la documentación y las herramientas internas se organizan en `aikya/docs/`, `aikya/test/` y `aikya/scripts/`.

## 4. Flujo de desarrollo

La rama principal de integración de contribuciones es `develop`.

Crea tus cambios en una rama independiente:

```bash
git clone https://github.com/jlema0590/aikya-harnes.git
cd aikya-harnes

git switch develop
git pull origin develop

git switch -c feat/descripcion-del-cambio
```

Para corregir errores puedes usar el prefijo `fix/`.

No realices cambios directamente sobre `main`.

## 5. Convenciones de desarrollo

Procura seguir estos principios:

- Código legible y mantenible.
- Responsabilidades claramente definidas.
- Cambios pequeños y verificables.
- Compatibilidad con configuraciones existentes.
- Sin sobreescrituras destructivas de archivos del usuario.
- Validación de entradas y rutas.
- Dependencias justificadas y documentadas.
- Mensajes de error útiles para el desarrollador.
- Separación entre planificación y ejecución.
- Documentación actualizada cuando cambie el comportamiento.

En los flujos de IA, los resultados generados deben revisarse antes de considerarse correctos.

## 6. Contribuir con agentes y skills

Los nuevos agentes y skills deben:

1. Tener una responsabilidad concreta.
2. Utilizar nombres descriptivos y consistentes.
3. Evitar duplicar especialidades existentes.
4. Incluir instrucciones claras y verificables.
5. Definir correctamente su configuración y metadatos.
6. Respetar el mecanismo de descubrimiento e instalación selectiva.
7. Evitar operaciones destructivas o remotas sin autorización.
8. Mantener la compatibilidad con los comandos existentes.
9. Incorporar pruebas cuando modifiquen el comportamiento del harness.

Los archivos de skills deben utilizar la estructura `SKILL.md` compatible con el entorno de ejecución al que estén destinados.

No deben incluirse credenciales, claves privadas ni instrucciones destinadas a evadir controles de seguridad.

## 7. Infrastructure & DevOps

Las contribuciones relacionadas con Terraform, OpenTofu, Ansible, Docker, Docker Compose, Kubernetes, Helm o Kustomize deben cumplir estos requisitos:

- No ejecutar despliegues reales de forma automática.
- No incluir credenciales ni secretos.
- No generar recursos cloud ficticios presentándolos como configuraciones operativas.
- Validar los parámetros de entrada.
- Separar entornos cuando corresponda.
- Preservar configuraciones existentes.
- Documentar permisos, requisitos y operaciones necesarias.
- Mantener separados los procesos `plan`, `generate` y `validate`.
- Solicitar autorización específica antes de ejecutar cambios sobre recursos externos.

La creación de archivos declarativos no equivale a un despliegue exitoso.

## 8. Pruebas

Antes de enviar un Pull Request, ejecuta la suite de pruebas automatizadas:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Además:

- Añade pruebas para funcionalidades nuevas.
- Incluye pruebas de regresión cuando corrijas errores.
- Comprueba que los ejemplos JSON siguen siendo válidos.
- Verifica la compatibilidad con los proyectos existentes.
- Documenta las comprobaciones que no hayas podido ejecutar.

No afirmes que una prueba ha pasado si no se ha ejecutado.

Los cambios significativos deberían contar también con una revisión manual en Claude Code cuando afecten a la interacción con agentes o skills.

## 9. Documentación

Los cambios que afecten al comportamiento del proyecto deben actualizar la documentación correspondiente.

Revisa, según el alcance:

- `README.md`
- `CHANGELOG.md`
- Documentación de agentes y skills.
- Ejemplos y archivos `answers.json`.
- Instrucciones de instalación.
- Pruebas y procedimientos de validación.

La documentación debe reflejar el comportamiento real del código.

## 10. Commits y Pull Requests

Recomendamos utilizar mensajes de commit siguiendo Conventional Commits:

```text
feat: add terraform module support
fix: correct node version detection
docs: improve installation guide
test: add infrastructure regression tests
refactor: simplify engineering catalog
```

Los Pull Requests deben dirigirse a la rama `develop`.

Cada Pull Request debería incluir:

- Descripción del cambio.
- Problema que resuelve.
- Archivos o componentes afectados.
- Pruebas ejecutadas y resultados.
- Impacto sobre compatibilidad y seguridad.
- Documentación actualizada, cuando corresponda.
- Referencias a Issues relacionados.

Los cambios serán revisados antes de incorporarse.

## 11. Seguridad y divulgación responsable

No publiques vulnerabilidades de seguridad sin seguir el procedimiento de `SECURITY.md`.

No incluyas secretos, datos personales ni información confidencial en Issues, commits, ejemplos, capturas o Pull Requests.

## 12. Licencias y propiedad intelectual

Al contribuir, confirmas que tienes los derechos necesarios para enviar tu contribución y que puedes distribuirla bajo la licencia MIT del proyecto.

No envíes código, agentes, skills, documentación ni otros materiales de terceros sin comprobar que su licencia permite su incorporación y redistribución.

Cuando utilices componentes externos:

- Identifica su origen.
- Conserva los avisos de copyright y licencia exigidos.
- Documenta las dependencias y condiciones relevantes.
- Declara cualquier incompatibilidad de licencia antes de proponer el cambio.

Los componentes de terceros conservan sus propias condiciones cuando corresponda.

## 13. Código de conducta

Todas las personas colaboradoras deben respetar el documento `CODE_OF_CONDUCT.md`.

Queremos mantener una comunidad técnica abierta, respetuosa y orientada a la colaboración.

## 14. Agradecimientos

Gracias por ayudar a mejorar Aikya Harness.

Cada contribución, desde una corrección documental hasta una nueva integración de infraestructura, ayuda a construir una plataforma de ingeniería más sólida y útil para la comunidad.