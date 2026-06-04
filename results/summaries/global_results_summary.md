# Resumen global de resultados

La evaluación compara dos métodos de generación de marcado XML-TEI para obras dramáticas filipinas en español: un sistema basado en expresiones regulares y un sistema basado en Gemma.

## Resultado global

- Gemma obtiene mejor macro-F1 en 7 de las 9 obras.
- RegEx obtiene mejor macro-F1 en 2 de las 9 obras: *Brumas y voces* y *Filipinizad a los filipinos*.
- El promedio macro-F1 del corpus es 0.596 para RegEx y 0.818 para Gemma.
- El caso de mayor diferencia a favor de Gemma es *Filipinas. Auto histórico sacramental*, donde RegEx produce un fallo estructural casi completo.
- El caso más favorable a RegEx es *Filipinizad a los filipinos*, cuyo formato tipográfico se ajusta bien a las reglas implementadas.

## Interpretación general

RegEx ofrece un comportamiento determinista y muy sólido cuando la tipografía de entrada coincide con los patrones previstos. Gemma es más flexible ante heterogeneidad textual, pero puede sobreproducir parlamentos, duplicar personajes o generar referencias `who` inconsistentes si no se aplica validación y postprocesado.
