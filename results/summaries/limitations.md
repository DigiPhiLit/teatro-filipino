# Limitaciones de los resultados

## Limitaciones del cálculo

- La evaluación se basa en recuentos agregados por etiqueta.
- No se realiza alineación posicional instancia a instancia.
- El F1 reportado puede ser superior al F1 real si las etiquetas generadas coinciden en número pero no en posición o contenido exacto.

## Limitaciones de RegEx

- Alta dependencia de convenciones tipográficas regulares.
- Menor capacidad para generalizar ante impresos, manuscritos o transcripciones heterogéneas.
- Dificultades con nombres de personajes no escritos en mayúsculas.
- Ausencia de algunas etiquetas como `<roleDesc>`, `<l>` o `<lg>`.

## Limitaciones de Gemma

- Posible sobreproducción de parlamentos.
- Riesgo de duplicación de personajes en `<particDesc>`.
- Posibles inconsistencias entre `xml:id` y `who`.
- Necesidad de validación y postprocesado.
- Dependencia de parámetros de generación, versión del modelo y entorno de ejecución.
