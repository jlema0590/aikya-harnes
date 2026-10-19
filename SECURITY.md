# Política de seguridad — Aikya Harness

La seguridad es una parte fundamental de Aikya Harness.

Nuestro objetivo es proporcionar un framework de automatización e ingeniería que permita trabajar con agentes de inteligencia artificial, desarrollo de software, infraestructura como código y herramientas DevOps de forma controlada y segura.

Agradecemos los reportes responsables de vulnerabilidades que puedan afectar al proyecto o a sus usuarios.

## 1. Versiones soportadas

Las correcciones de seguridad se priorizan para la versión estable más reciente publicada por el proyecto.

| Versión o rama | Política |
|---|---|
| Última versión estable publicada | Soporte prioritario |
| `develop` | Correcciones durante el desarrollo, sin garantía de estabilidad |
| Versiones antiguas | Evaluación caso por caso |

Las versiones antiguas pueden dejar de recibir correcciones de seguridad.

Consulta las releases y los avisos del repositorio para comprobar qué versiones están mantenidas.

## 2. Reportar una vulnerabilidad

**No publiques vulnerabilidades de seguridad en Issues públicos.**

Para reportar una vulnerabilidad, utiliza preferentemente la opción privada **Report a vulnerability** de GitHub, cuando esté habilitada.

También puedes comunicarla a:

**Contacto de seguridad:** [EMAIL_SEGURIDAD]

Incluye, cuando sea posible:

- Descripción de la vulnerabilidad.
- Componente y versión afectados.
- Pasos para reproducir el problema.
- Impacto potencial.
- Prueba de concepto no destructiva.
- Recomendaciones de mitigación, si las conoces.

No adjuntes credenciales reales, claves privadas ni datos personales innecesarios.

## 3. Gestión de reportes

Al recibir un reporte, las personas responsables del proyecto procurarán:

1. Confirmar su recepción.
2. Evaluar si la vulnerabilidad es reproducible.
3. Determinar el alcance y la gravedad.
4. Investigar las posibles mitigaciones.
5. Preparar una corrección cuando corresponda.
6. Coordinar una publicación responsable de los detalles.
7. Informar a la comunidad si el impacto lo justifica.

Los plazos dependerán de la complejidad y gravedad del problema y de la disponibilidad del equipo de mantenimiento.

## 4. Áreas de especial interés

Consideramos especialmente relevantes las vulnerabilidades relacionadas con:

### Ejecución de comandos

- Ejecución arbitraria de código.
- Inyección de comandos.
- Comandos destructivos ejecutados sin autorización.
- Elevación indebida de privilegios.

### Agentes y skills de IA

- Inyección de instrucciones maliciosas.
- Ejecución de herramientas no autorizadas.
- Manipulación de agentes o skills.
- Lectura o divulgación indebida de información.
- Instalación no autorizada de componentes externos.
- Alteración de mecanismos de aprobación.

### Sistema de archivos

- Path traversal.
- Sobrescritura de archivos ajenos al harness.
- Acceso no autorizado a archivos sensibles.
- Tratamiento inseguro de enlaces simbólicos.
- Migraciones destructivas o pérdida de configuraciones.

### Infraestructura y DevOps

- Exposición de credenciales cloud.
- Estados Terraform con información sensible.
- Playbooks Ansible inseguros.
- Configuraciones Docker con privilegios excesivos.
- Contenedores ejecutados innecesariamente como root.
- Permisos Kubernetes excesivos.
- Manifiestos que expongan servicios o secretos.
- Despliegues realizados sin confirmación.

### Cadena de suministro

- Dependencias comprometidas.
- Scripts de instalación inseguros.
- Agentes y skills de origen no verificado.
- Descargas automáticas no autorizadas.
- Modificaciones maliciosas en plantillas o configuraciones.

## 5. Investigación responsable

Si estás investigando una posible vulnerabilidad:

- Utiliza entornos propios o expresamente autorizados.
- Evita afectar a otras personas o sistemas.
- No realices pruebas destructivas.
- No extraigas datos que no sean necesarios para demostrar el problema.
- No intentes acceder a sistemas externos sin permiso.
- Comunica los hallazgos de manera privada.
- Da un margen razonable para investigar y corregir el problema antes de coordinar su publicación.

La comunicación de una vulnerabilidad no supone autorización para realizar actividades intrusivas.

## 6. Principios de seguridad del proyecto

Aikya Harness sigue estos principios:

**Mínimo privilegio:** los agentes y las herramientas deben disponer únicamente de los permisos necesarios para sus tareas.

**Aprobación explícita:** las operaciones que instalen software, modifiquen sistemas externos, utilicen credenciales o desplieguen infraestructura requieren autorización adecuada.

**No sobrescritura:** las configuraciones existentes y personalizadas deben preservarse siempre que sea posible.

**Separación de responsabilidades:** las operaciones de planificación, generación y despliegue deben mantenerse diferenciadas.

**Gestión segura de secretos:** las credenciales deben almacenarse mediante mecanismos apropiados y nunca incorporarse directamente a ejemplos públicos.

**Validación verificable:** no se debe afirmar que una configuración es segura o que un despliegue funciona sin disponer de evidencias suficientes.

## 7. Dependencias y componentes de terceros

Los agentes, skills, dependencias y herramientas externas deben revisarse antes de incorporarlos al proyecto.

Las vulnerabilidades de componentes de terceros deberán evaluarse según su impacto sobre Aikya Harness.

Cuando corresponda, también se recomienda informar al proyecto original del componente vulnerable.

## 8. Divulgación de vulnerabilidades

Cuando exista una corrección disponible, el proyecto podrá publicar un aviso de seguridad que incluya:

- Descripción general del problema.
- Versiones afectadas.
- Impacto.
- Medidas de mitigación.
- Versión que incorpora la corrección.
- Recomendaciones de actualización.

Se evitará divulgar innecesariamente información que facilite ataques antes de que exista una mitigación razonable.

## 9. Alcance y limitaciones

Aikya Harness proporciona herramientas para facilitar tareas de ingeniería y automatización.

Las configuraciones generadas no garantizan por sí mismas la seguridad del entorno donde se utilizarán.

Los usuarios deben revisar los permisos, dependencias, políticas, credenciales e infraestructura antes de ejecutar operaciones reales.

La licencia del proyecto establece las condiciones aplicables al software, incluyendo las limitaciones de garantía y responsabilidad.