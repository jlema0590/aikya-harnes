---
name: aikya-tokens
description: Informe local de tokens por modelo y caché, sin almacenar mensajes ni prompts.
disable-model-invocation: true
---
<!-- AIKYA BOOTSTRAP MANAGED -->
# /aikya-tokens

Solicita al usuario una ruta concreta a las transcripciones JSONL del proyecto. Nunca escanees todos los proyectos globales ni envíes contenido de transcripciones a servicios externos. Ejecuta `python3 token_report.py --path <ruta-confirmada>` desde el runtime Aikya. Presenta input, output, cache creation y cache read por modelo. Si no hay acceso a métricas, informa que no se pueden medir; no inventes costes ni ahorros.

## Tarifa de Haiku 5.5 (v6)

El informe puede ofrecer haiku_55_estimated_api_cost con el cálculo por mensaje, separado de las tarifas configurables por usuario. Un prompt de hasta 100.000 tokens y otro superior utilizan tramos distintos; se utiliza un rango cuando la escritura de caché puede ser de 5 minutos o de una hora. No presentes el rango como factura de Anthropic ni como ahorro medido, ni confundas el tokenizador de Haiku 5.5 con el de 4.5. La ausencia de transcripciones o de identificadores de mensaje impide verificar un total exacto.
