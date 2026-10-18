# Reglas de arquitectura

- Antes de introducir nuevas capas, evaluar si las actuales ya resuelven la necesidad.
- Mantener límites entre dominio, aplicación e infraestructura si el repositorio usa esas capas.
- Documentar los cambios en contratos públicos, esquemas de base de datos y protocolos entre servicios.
- Una dependencia externa nueva requiere explicación, versión y análisis de impacto.
- No imponer patrones (DDD, hexagonal, CQRS o microservicios) cuando no resuelvan un problema existente.
