---
name: aikya-tokens
description: Informe local de tokens por modelo y caché, sin almacenar mensajes ni prompts.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-tokens

Solicita al usuario una ruta concreta a las transcripciones JSONL del proyecto. Nunca escanees todos los proyectos globales ni envíes contenido de transcripciones a servicios externos. Ejecuta `python3 token_report.py --path <ruta-confirmada>` desde el runtime Aikya. Presenta input, output, cache creation y cache read por modelo. Si no hay acceso a métricas, informa que no se pueden medir; no inventes costes ni ahorros.
