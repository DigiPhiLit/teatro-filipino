# Aplicación basada en RegEx

## Descripción

La herramienta desarrollada para esta parte del proyecto está implementada en Python como un script de línea de comandos (`tei_generator.py`) que expone una función principal, `generar_tei()`.

Su objetivo es generar una primera versión de marcado TEI-XML para obras teatrales a partir de archivos `.txt`, utilizando expresiones regulares. A diferencia de otros flujos de trabajo que requieren un preprocesamiento manual o un marcado intermedio simplificado, esta herramienta trabaja directamente sobre el texto plano.

El sistema está diseñado como una aproximación determinista, reproducible y ejecutable en local. Su finalidad no es producir una edición TEI definitiva, sino generar un primer marcado estructural que pueda ser validado, corregido y comparado con otros métodos de codificación automática o semiautomática.

## Funcionamiento

La transformación se invoca desde la terminal, pasando como argumentos el texto fuente y los metadatos básicos de la obra: título, autoría, año e idioma.

El sistema no requiere conexión a internet ni autenticación. La transformación se realiza íntegramente en local, de forma determinista e inmediata.

El motor aplica diecisiete correcciones de calidad documentadas internamente como C-01 a C-17, organizadas en cinco categorías principales de detección:

* **Inicio del texto dramático**: una expresión regular detecta la primera señal estructural significativa, como `PERSONAJES`, `REPARTO`, `ACTO I`, `JORNADA PRIMERA`, `PRÓLOGO`, etc., para descartar la portada y los datos editoriales previos al cuerpo dramático.

* **Nombres de personaje**: se distinguen dos patrones principales: el encabezado de parlamento en línea, por ejemplo `NOMBRE.- texto del parlamento`, y el encabezado de parlamento aislado, es decir, el nombre del personaje en una línea propia seguido del texto en la línea siguiente. Ambos patrones exigen que el nombre esté íntegramente en mayúsculas, tenga entre una y cuatro palabras, no contenga dígitos ni signos de puntuación internos, y no pertenezca a una lista de palabras reservadas. Esta lista excluye encabezados estructurales, indicaciones escénicas genéricas y referencias a personajes históricos o literarios que son mencionados en el diálogo pero no intervienen como hablantes en la obra.

* **Acotaciones escénicas**: se detecta texto encerrado entre paréntesis o corchetes en línea propia, así como expresiones canónicas de dirección escénica, como `sale`, `entra`, `mutis`, `aparte`, `pausa` o `telón`. Estas indicaciones se codifican como `<stage type="action">`. Las acotaciones incrustadas dentro de un parlamento, especialmente los paréntesis de diez o más caracteres dentro del texto de un `<p>`, se marcan como `<stage type="action">` en el interior del propio elemento `<p>` según la corrección C-17.

* **Divisiones estructurales**: las líneas que comienzan por `ACTO` o `JORNADA`, seguidas de numerales romanos, arábigos u ordinales textuales como `PRIMERO`, `SEGUNDO` o `ÚNICO`, generan un `<div type="act">`. Las subdivisiones indicadas mediante `ESCENA`, `CUADRO` o `TABLEAU` generan un `<div type="scene">`, siempre anidado dentro del acto o jornada activa, según la corrección C-10.

* **Patrones especiales**: el sistema contempla varios casos específicos, como la aparición de `telón` al final de la obra como `<stage>` independiente fuera del último `<sp>` según C-12; las notas a pie de página que comienzan por `(N)` o `(*)`, codificadas como `<p>` independientes según C-13; los marcadores de paginación OCR, como líneas compuestas únicamente por dígitos o guiones, que se descartan; y las canciones o versos intercalados entre comillas angulares, que se marcan como `<sp>` del personaje que canta según C-11.

## Pipeline

El flujo de transformación sigue seis etapas secuenciales:

1. **Normalización**: el archivo `.txt` se lee en UTF-8. Se unifican los saltos de línea, se eliminan espacios finales, se reconectan palabras partidas por guion procedentes de OCR y se colapsan las líneas en blanco múltiples.

2. **Separación de portada**: se localiza la primera señal de inicio dramático y se descarta todo el texto anterior como material editorial no codificable en el cuerpo dramático.

3. **Extracción de personajes**: se busca primero un bloque explícito de reparto, identificado mediante encabezados como `PERSONAJES`, `REPARTO` o `DRAMATIS PERSONAE`. Si no existe, el sistema recorre el cuerpo completo de la obra para extraer como alternativa todos los encabezados de parlamento detectados.

4. **Segmentación estructural**: el texto se recorre línea a línea manteniendo el estado de acto, escena y parlamento abiertos. Cada señal de acto, escena o cambio de personaje activa las funciones de cierre y apertura del elemento correspondiente.

5. **Ensamblaje XML**: los bloques generados se combinan con una plantilla de `<teiHeader>`, completada con los metadatos introducidos por el usuario. El documento resultante incorpora la declaración del modelo XML correspondiente al esquema de validación utilizado, por ejemplo:

   ```xml
   <?xml-model href="https://dracor.org/schema.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
   ```

6. **Exportación**: el documento se serializa y se escribe en disco en la ruta indicada por el usuario.

## Limitaciones

El marcado producido por esta herramienta debe considerarse una primera propuesta automática. El uso de expresiones regulares permite obtener resultados rápidos, reproducibles y explicables, pero presenta limitaciones ante variaciones tipográficas, inconsistencias editoriales, errores de OCR o estructuras dramáticas no convencionales.

Por este motivo, los archivos TEI-XML generados mediante este procedimiento requieren validación posterior y, en muchos casos, revisión manual o comparación con otros métodos de marcado.

