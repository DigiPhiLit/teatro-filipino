# Aplicación basada en RegEx

## Descripción

La herramienta desarrollada para esta parte del proyecto está implementada en Python como un script de línea de comandos (`tei_generator.py`) que expone una función principal, `generar_tei()`.

Su objetivo es generar una primera versión de marcado TEI-XML para obras teatrales a partir de archivos `.txt`, utilizando expresiones regulares. A diferencia de otros flujos de trabajo que requieren un preprocesamiento manual o un marcado intermedio simplificado, esta herramienta trabaja directamente sobre el texto plano.

El sistema está diseñado como una aproximación determinista, reproducible y ejecutable en local. Su finalidad no es producir una edición TEI definitiva, sino generar un primer marcado estructural que pueda ser validado, corregido y comparado con otros métodos de codificación automática o semiautomática.

## Funcionamiento

La transformación puede invocarse desde otro script de Python o integrarse en una interfaz de línea de comandos. En su versión actual, el archivo define las funciones necesarias para realizar la transformación, pero no implementa por sí mismo un parser de argumentos de terminal. Pasa como argumentos el texto fuente y los metadatos básicos de la obra: título, autoría, año e idioma.

El sistema no requiere conexión a internet ni autenticación. La transformación se realiza íntegramente en local, de forma determinista e inmediata.

El motor aplica diecisiete correcciones de calidad documentadas internamente como C-01 a C-17, organizadas en cinco categorías principales de detección:

* **Inicio del texto dramático**: una expresión regular detecta la primera señal estructural significativa, como `PERSONAJES`, `REPARTO`, `ACTO I`, `JORNADA PRIMERA`, `PRÓLOGO`, etc., para descartar la portada y los datos editoriales previos al cuerpo dramático.

* **Nombres de personaje**: se distinguen dos patrones principales: el encabezado de parlamento en línea, por ejemplo `NOMBRE.- texto del parlamento`, y el encabezado de parlamento aislado, es decir, el nombre del personaje en una línea propia seguido del texto en la línea siguiente. Ambos patrones exigen que el nombre esté íntegramente en mayúsculas, tenga entre una y cuatro palabras, no contenga dígitos ni signos de puntuación internos, y no pertenezca a una lista de palabras reservadas. Esta lista excluye encabezados estructurales, indicaciones escénicas genéricas y referencias a personajes históricos o literarios que son mencionados en el diálogo pero no intervienen como hablantes en la obra.

* **Acotaciones escénicas**: se detecta texto encerrado entre paréntesis o corchetes en línea propia, así como expresiones canónicas de dirección escénica, como `sale`, `entra`, `mutis`, `aparte`, `pausa` o `telón`. Estas indicaciones se codifican como `<stage type="action">`. Las acotaciones incrustadas dentro de un parlamento, especialmente los paréntesis de diez o más caracteres dentro del texto de un `<p>`, se marcan como `<stage type="action">` en el interior del propio elemento `<p>` según la corrección C-17.

* **Divisiones estructurales**: las líneas que comienzan por `ACTO` o `JORNADA`, seguidas de numerales romanos, arábigos u ordinales textuales como `PRIMERO`, `SEGUNDO` o `ÚNICO`, generan un `<div type="act">`. Las subdivisiones indicadas mediante `ESCENA`, `CUADRO` o `TABLEAU` generan un `<div type="scene">`, siempre anidado dentro del acto o jornada activa, según la corrección C-10.

* **Patrones especiales**: el sistema contempla varios casos específicos, como la aparición de `telón` al final de la obra como `<stage>` independiente fuera del último `<sp>` según C-12; las notas a pie de página que comienzan por `(N)` o `(*)`, codificadas como `<p>` independientes según C-13; los marcadores de paginación OCR, como líneas compuestas únicamente por dígitos o guiones, que se descartan; y las canciones o versos intercalados entre comillas angulares, que se marcan como `<sp>` del personaje que canta según C-11.

## Correcciones de calidad

El sistema aplica diecisiete correcciones de calidad, identificadas como C-01 a C-17, cotejadas con el Gold Standard:

- **C-01**: `xml:id` sin guiones bajos internos en el título.
- **C-02**: `<title type="main">` con capitalización tipo oración.
- **C-03**: `<forename>` y `<surname>` con mayúscula inicial, incluyendo tratamientos honoríficos como `Dr.`, `Fray` o `Don`.
- **C-04**: fuente digital de la Biblioteca Virtual Miguel de Cervantes incluida como primer `<bibl type="digitalSource">`.
- **C-05**: `<roleDesc>` nunca vacío si el texto fuente proporciona descripción; si no hay descripción, el elemento se omite.
- **C-06**: nombres de roles en `<castList>` en mayúsculas y con tildes.
- **C-07**: personajes históricos o literarios mencionados en diálogo, pero que no actúan en la obra, excluidos de `<listPerson>`.
- **C-08**: `<head>` de actos y escenas en mayúsculas y con tildes correctas.
- **C-09**: acotación inicial del acto codificada como un único `<stage type="action">`.
- **C-10**: escenas, `<div type="scene">`, siempre anidadas dentro del acto, `<div type="act">`.
- **C-11**: canciones o versos intercalados marcados como `<sp>` propio del personaje que canta.
- **C-12**: `TELÓN.` marcado como `<stage type="action">TELÓN.</stage>` independiente después del último `<sp>`.
- **C-13**: notas a pie de página como `<p>(N) texto…</p>` independientes.
- **C-14**: personajes sin texto hablado, solo con acotación, marcados como `<stage type="action">`, sin abrir `<sp>`.
- **C-15**: conservación de tildes y ortografía española en todos los elementos generados.
- **C-16**: parlamento de cada personaje en un único `<p>`, sin fragmentar.
- **C-17**: acotaciones internas dentro del `<p>` del parlamento, no como elementos hermanos.

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

## Entrada y salida

La herramienta está organizada como un módulo Python reutilizable. La función principal es `generar_tei()`, que recibe como entrada el contenido de una obra teatral en texto plano, junto con los metadatos básicos necesarios para construir el `teiHeader`.

### Entrada

La función `generar_tei()` espera los siguientes argumentos principales:

- `texto`: contenido de la obra en formato `.txt`.
- `titulo`: título de la obra.
- `autor`: autoría de la obra.
- `fecha`: fecha de publicación, representación o composición, si se conoce.
- `idioma`: código de lengua, por defecto `es`.
- `fuente_digital_titulo`: título de la fuente digital.
- `fuente_digital_url`: URL de la fuente digital.
- `fuente_digital_lugar`: lugar de publicación de la fuente digital.
- `fuente_digital_fecha`: fecha de la fuente digital.
- `fuente_impresa_lugar`: lugar de publicación de la fuente impresa.
- `fuente_impresa_editorial`: editorial o imprenta de la fuente impresa.
- `fuente_impresa_titulo`: título completo de la fuente impresa.
- `subgenero`: subgénero dramático, si se conoce.
- `forma`: forma textual, por defecto `prose`.
- `resp_stmt_resp`: tipo de responsabilidad secundaria, por ejemplo `arreglada en forma teatral por`.
- `resp_stmt_nombre`: nombre de la persona responsable de esa intervención secundaria.

### Salida

La función devuelve una cadena de texto con un documento TEI-XML completo. Este documento incluye:

- declaración XML;
- declaración `xml-model` asociada al esquema DraCor;
- elemento raíz `<TEI>`;
- `<teiHeader>` con metadatos bibliográficos, lingüísticos y de clasificación;
- `<listPerson>` con los personajes detectados;
- `<castList>` cuando se han identificado personajes;
- `<body>` con el cuerpo dramático segmentado en actos, jornadas, escenas, parlamentos y acotaciones.

El XML generado puede guardarse en disco mediante la función auxiliar `save_tei_to_file()`.

### Ejemplo de uso desde Python

```python
from tei_generator_regex import generar_tei, save_tei_to_file

with open("data/txt/alma_filipina.txt", "r", encoding="utf-8") as f:
    texto = f.read()

tei_xml = generar_tei(
    texto=texto,
    titulo="Alma filipina",
    autor="Severino Reyes",
    fecha="1911",
    idioma="es",
    fuente_digital_titulo="Biblioteca Virtual Miguel de Cervantes",
    fuente_digital_url="https://www.cervantesvirtual.com/obra/alma-filipina---comedia-en-un-acto-y-en-prosa/",
    fuente_digital_lugar="Alicante",
    fuente_digital_fecha="2013",
    fuente_impresa_lugar="Manila",
    fuente_impresa_editorial="Imprenta Librería y Papelería de I. R. Morales",
    fuente_impresa_titulo="Alma filipina",
    subgenero="comedy",
    forma="prose"
)

save_tei_to_file(tei_xml, "data/tei_regex/alma_filipina.xml")
