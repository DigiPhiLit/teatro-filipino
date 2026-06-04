# Metodología de evaluación

La evaluación se basa en la comparación de las salidas generadas por dos sistemas automáticos con un gold standard XML-TEI marcado manualmente.

## Sistemas evaluados

1. **RegEx**: sistema determinista basado en expresiones regulares.
2. **Gemma**: sistema basado en modelo de lenguaje.

## Dimensiones de evaluación

La evaluación contempla tres dimensiones:

1. **Exactitud de etiquetas**: compara el número de etiquetas generadas por cada sistema con el gold standard.
2. **Corrección estructural**: comprueba si el XML está bien formado y si la jerarquía TEI respeta la estructura esperada.
3. **Fidelidad textual**: evalúa si el contenido textual se conserva sin adiciones, omisiones o transformaciones indebidas.

## Métricas

Las métricas principales son:

- **Precisión**: `P = TP / (TP + FP)`
- **Recall**: `R = TP / (TP + FN)`
- **F1**: `F1 = 2·P·R / (P + R)`

En esta evaluación, los verdaderos positivos se aproximan como `TP = min(pred, gold)`, ya que el cálculo se realiza sobre recuentos agregados por tipo de etiqueta y no mediante alineación posicional instancia a instancia. Por ello, los valores F1 deben interpretarse como límite superior.

## Tablas incluidas

Los resultados están disponibles en formato CSV dentro de `tables/`.
