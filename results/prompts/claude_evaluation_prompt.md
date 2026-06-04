# Prompt de evaluación XML-TEI

Este documento contiene el prompt utilizado para evaluar los sistemas de etiquetado automático XML-TEI (**RegEx** y **Gemma**) contra el **Gold Standard**, usando **Claude.ai**.

## Cómo usarlo

1. Ve a `https://claude.ai`.
2. Abre una conversación nueva.
3. Copia el prompt de abajo.
4. Sustituye `[gold standard]` y `[xml a evaluar]` por el contenido de tus archivos.
5. Envía el mensaje.

## Prompt

```text
Tengo dos archivos XML-TEI. El primero es el Gold Standard, siguiendo las directrices de DraCor. El segundo es el XML generado automáticamente por [RegEx/Gemma] que quiero evaluar.

Compara ambos archivos y calcula las siguientes métricas para cada tipo de etiqueta TEI:

- Precisión (P) = TP / (TP + FP)
- Cobertura/Recall (R) = TP / (TP + FN)
- F1 = 2·P·R / (P + R)
- Macro-F1: promedio de los F1 de todas las etiquetas

Para calcular los verdaderos positivos usa la aproximación TP = min(n_pred, n_gold), ya que la evaluación es a nivel de recuento agregado de instancias por etiqueta, no de alineación posicional.

Las etiquetas que debes evaluar son: <sp>, <speaker>, <p>, <stage>, <div>, <head>, <person>, <persName>, <castItem>, <role>, <roleDesc>, <personGrp>, <actor>, <l>, <lg>.

Solo incluye en la tabla las etiquetas que aparecen en al menos uno de los dos archivos. Redondea a 3 decimales.

Presenta los resultados en una tabla con estas columnas:

Etiqueta | Gold (n) | Pred (n) | P | R | F1

Al final añade una fila Macro con el macro-F1.

[gold standard]

[xml a evaluar]
```

## Nota metodológica

- Cada obra se evaluó por separado en una conversación independiente.
- Los resultados de cada tabla se extrajeron manualmente y se incorporaron al artículo y a las tablas de resultados del repositorio.
- La evaluación se basa en recuentos agregados por etiqueta. Por tanto, los valores de F1 deben interpretarse como una aproximación y no como una alineación posicional exacta entre ambos XML.
