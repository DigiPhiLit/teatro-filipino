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

## Instalación y uso básico

Esta herramienta convierte obras de teatro en formato de texto plano (`.txt`) a XML-TEI compatible con el esquema DraCor. Funciona íntegramente en local: no requiere conexión a internet, cuenta en ningún servicio externo ni clave de API.

### Paso 1. Requisitos

Para utilizar la herramienta se necesita:

1. Tener instalado Python 3.10 o superior.
2. Descargar el archivo `tei_generator.py` desde el repositorio y guardarlo en una carpeta de trabajo, por ejemplo `RegEx`.
3. Disponer de uno o varios archivos `.txt` codificados en UTF-8.
4. No es necesario instalar bibliotecas adicionales, ya que el script utiliza únicamente módulos estándar de Python.

### Paso 2. Preparar el texto de entrada

El texto de entrada debe ser un archivo `.txt` en codificación UTF-8.

Antes de la conversión, se recomienda revisar que el archivo no contiene errores graves de OCR o transcripción que puedan afectar al marcado automático, por ejemplo:

* palabras partidas incorrectamente;
* números de página aislados;
* caracteres extraños;
* encabezados o pies de página repetidos;
* cortes de línea que separen indebidamente nombres de personaje, actos o escenas.

El sistema incorpora algunas reglas para limpiar y normalizar el texto, pero la calidad del XML generado depende en gran medida de la regularidad del archivo de entrada.

### Paso 3. Crear el script de conversión

Para cada obra, se puede crear un archivo `.py` en la misma carpeta de trabajo. Por ejemplo, `convertir_obra.py`.

El archivo debe contener un código como el siguiente, sustituyendo los datos en mayúsculas por los datos de cada obra:

```python
from pathlib import Path
from tei_generator import generar_tei

texto = Path("NOMBRE_ARCHIVO.txt").read_text(encoding="utf-8")

xml = generar_tei(
    texto=texto,
    titulo="TÍTULO DE LA OBRA",
    autor="NOMBRE DEL AUTOR/A",
    fecha="AÑO",
    idioma="es"
)

Path("NOMBRE_SALIDA_tei.xml").write_text(xml, encoding="utf-8")

print("Listo")
```

Por ejemplo:

```python
from pathlib import Path
from tei_generator import generar_tei

texto = Path("alma_filipina.txt").read_text(encoding="utf-8")

xml = generar_tei(
    texto=texto,
    titulo="Alma filipina",
    autor="Severino Reyes",
    fecha="1911",
    idioma="es"
)

Path("alma_filipina_tei.xml").write_text(xml, encoding="utf-8")

print("Listo")
```

### Paso 4. Ejecutar la conversión desde la terminal

Abra la terminal y navegue a la carpeta donde se encuentran el script de conversión, el archivo `.txt` y `tei_generator.py`.

En macOS o Linux:

```bash
cd ~/Desktop/RegEx
python3 convertir_obra.py
```

En Windows:

```bash
cd %USERPROFILE%\Desktop\RegEx
python convertir_obra.py
```

El archivo XML-TEI se generará en la misma carpeta, con el nombre indicado en la línea final del script:

```python
Path("NOMBRE_SALIDA_tei.xml").write_text(xml, encoding="utf-8")
```

### Entrada y salida de la función

La herramienta está organizada como un módulo Python reutilizable. La función principal es `generar_tei()`, que recibe como entrada el contenido de una obra teatral en texto plano y los metadatos básicos necesarios para construir el `teiHeader`.

Los argumentos mínimos son:

- `texto`: contenido de la obra en formato `.txt`.
- `titulo`: título de la obra.
- `autor`: autoría de la obra.
- `fecha`: fecha de publicación, representación o composición, si se conoce.
- `idioma`: código de lengua, por defecto `es`.

La función también permite añadir metadatos bibliográficos más detallados, como la fuente digital, la URL de referencia, la fuente impresa, el subgénero, la forma textual o una responsabilidad secundaria.

La salida de `generar_tei()` es una cadena de texto con un documento TEI-XML completo. Este documento incluye la declaración XML, el elemento raíz `<TEI>`, el `<teiHeader>`, la lista de personajes detectados y el cuerpo dramático segmentado en actos, jornadas, escenas, parlamentos y acotaciones.

El XML puede guardarse en disco mediante `Path(...).write_text()` o mediante la función auxiliar `save_tei_to_file()`, si se desea utilizarla.

### Resultado esperado

Tras ejecutar el script, la carpeta de trabajo debería contener al menos estos archivos:

```text
RegEx/
├── tei_generator.py
├── NOMBRE_ARCHIVO.txt
├── convertir_obra.py
└── NOMBRE_SALIDA_tei.xml
```
El archivo `NOMBRE_SALIDA_tei.xml` contiene el marcado TEI-XML generado automáticamente a partir del texto plano.

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
