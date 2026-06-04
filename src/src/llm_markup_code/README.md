# Aplicación basada en Gemma para marcado XML-TEI

## Descripción

Esta carpeta contiene el código utilizado para automatizar la conversión de obras de teatro filipino en formato de texto plano (`.txt`) a XML-TEI compatible con el esquema DraCor mediante el modelo de lenguaje `gemma-4-26b-a4b-it`.

El sistema está diseñado para el procesamiento de textos dramáticos y genera automáticamente una propuesta de estructura TEI que incluye actos, escenas, parlamentos, personajes y acotaciones.

La herramienta forma parte del proyecto **DigiPhiLit - Teatro filipino en español** y se ha desarrollado para comparar el marcado XML-TEI generado mediante modelos de lenguaje con el marcado producido mediante expresiones regulares y con un gold standard revisado manualmente.

La salida generada debe entenderse como una primera propuesta automática de marcado. Por tanto, los archivos XML resultantes requieren validación posterior contra el esquema DraCor y revisión humana antes de considerarse versiones finales.

## Requisitos

Para ejecutar la aplicación se necesita:

* Python 3.10 o superior.
* Los archivos `main.py` y `tei_generator.py`.
* Una carpeta de trabajo, por ejemplo `app_tei_gemma`.
* La biblioteca `google-genai`.
* Una API Key de Google AI Studio.
* Un archivo de entrada en formato `.txt`, preferentemente codificado en UTF-8.

La interfaz gráfica utiliza `tkinter`, que suele venir incluido en la instalación estándar de Python.

## Instalación

Descargue los archivos `main.py` y `tei_generator.py` desde el repositorio y guárdelos en una misma carpeta de trabajo. Por ejemplo:

```text
app_tei_gemma/
├── main.py
└── tei_generator.py
```

Abra una terminal dentro de esa carpeta e instale la biblioteca necesaria:

```bash
pip install google-genai
```

## Configuración de la API Key

Para obtener una API Key de Google AI Studio:

1. Acceda a Google AI Studio: `https://aistudio.google.com/`
2. Inicie sesión con una cuenta de Google.
3. Vaya a la sección **Get API Key**.
4. Seleccione **Create API Key**.
5. Copie la clave generada.

En la versión actual del código, la clave debe introducirse en el archivo `tei_generator.py`, en la línea correspondiente a la creación del cliente:

```python
client = genai.Client(api_key="TU_API_KEY")
```

También puede aparecer como:

```python
API_KEY = "PON AQUÍ TU API KEY"
client = genai.Client(api_key=API_KEY)
```

En ese caso, sustituya `"PON AQUÍ TU API KEY"` por su clave real.

> Importante: no suba nunca al repositorio una API Key real. Si va a publicar o compartir el código, elimine la clave antes de hacer `commit`.

Para una versión más segura del código, se recomienda usar una variable de entorno:

```python
import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
```

En macOS o Linux, la clave puede definirse así:

```bash
export GOOGLE_API_KEY="SU_CLAVE"
python3 main.py
```

En Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="SU_CLAVE"
python main.py
```

## Ejecución

Una vez configurada la API Key, ejecute la aplicación desde la terminal:

```bash
python3 main.py
```

En Windows:

```bash
python main.py
```

Se abrirá una interfaz gráfica titulada **Generador TEI con Gemma**.

El flujo de uso es el siguiente:

1. Pulse **Cargar archivo .txt**.
2. Seleccione la obra teatral en texto plano.
3. Compruebe que el texto aparece correctamente en el área de entrada.
4. Pulse **Generar TEI**.
5. Espere a que el modelo devuelva el XML generado.
6. Pulse **Guardar XML** para exportar el resultado como archivo `.xml`.


## Archivos incluidos

La carpeta contiene dos archivos principales:

```text
llm_markup_code/
├── main.py
└── tei_generator.py
```

### `main.py`

Archivo principal de la aplicación gráfica. Implementa una interfaz con `tkinter` que permite:

* cargar un archivo `.txt`;
* visualizar el texto de entrada;
* enviar el texto al generador TEI;
* mostrar el XML-TEI producido;
* guardar el resultado como archivo `.xml`.

La generación se ejecuta en un hilo separado para evitar que la interfaz gráfica se bloquee durante la llamada al modelo.

### `tei_generator.py`

Módulo encargado de construir el prompt, llamar al modelo Gemma y devolver el XML generado.

Incluye las siguientes funciones:

* `build_tei_prompt(texto)`: construye el prompt de transformación de texto dramático a XML-TEI DraCor.
* `generate_tei_xml(texto)`: envía el prompt al modelo y devuelve la respuesta generada.
* `generate_tei_xml_largo(texto)`: función envoltorio para textos largos. En la versión actual llama directamente a `generate_tei_xml(texto)`.
* `save_tei_to_file(tei_xml, filename)`: guarda el XML generado en disco.

## Uso básico

Ejecute la aplicación desde la terminal:

```bash
python3 main.py
```

En Windows:

```bash
python main.py
```

Se abrirá una interfaz gráfica titulada **Generador TEI con Gemma**.

El flujo de uso es el siguiente:

1. Pulse **Cargar archivo .txt**.
2. Seleccione una obra teatral en texto plano.
3. Revise que el texto se ha cargado correctamente en el área de entrada.
4. Pulse **Generar TEI**.
5. Espere a que la aplicación devuelva el XML generado.
6. Pulse **Guardar XML** para exportar el resultado como archivo `.xml`.

## Entrada y salida

### Entrada

La entrada del sistema es un texto dramático en formato `.txt`, codificado preferiblemente en UTF-8.

El texto puede contener:

* encabezados de actos o jornadas;
* encabezados de escenas;
* nombres de personajes;
* parlamentos;
* acotaciones entre paréntesis;
* listas iniciales de personajes;
* texto en verso o en prosa.

No se requiere un marcado previo. Sin embargo, se recomienda revisar el texto antes de la transformación, especialmente si procede de OCR o transcripción automática.

Conviene comprobar:

* errores graves de OCR;
* caracteres extraños;
* números de página aislados;
* encabezados o pies de página repetidos;
* cortes de línea que dividan nombres de personajes;
* fragmentos incompletos o duplicados.

### Salida

La salida esperada es un documento XML-TEI compatible con el esquema DraCor.

El resultado debe incluir, idealmente:

* declaración XML;
* declaración `xml-model` asociada al esquema DraCor;
* elemento raíz `<TEI>`;
* `<teiHeader>` con información bibliográfica;
* `<profileDesc>` con información lingüística y clasificación textual;
* `<particDesc>` con lista de personajes;
* `<front>` con la lista de personajes si aparece en la fuente;
* `<body>` con actos, escenas, parlamentos y acotaciones;
* `<sp>` para cada parlamento;
* `<speaker>` para la forma textual del hablante;
* `<p>` para el contenido verbal del parlamento;
* `<stage type="action">` para acotaciones.

## Modelo utilizado

La aplicación utiliza el modelo:

```text
gemma-4-26b-a4b-it
```

En el contexto metodológico del proyecto, Gemma se emplea como alternativa a modelos propietarios de acceso cerrado o dependientes de APIs comerciales generalistas. El interés principal de este enfoque es explorar un modelo de generación TEI que sea más reproducible, auditable y sostenible que los sistemas basados en modelos cerrados.

La llamada al modelo se realiza mediante la biblioteca `google-genai`:

```python
from google import genai
from google.genai import types
```

La configuración actual utiliza:

```python
max_output_tokens=65536
temperature=0.1
```

El valor bajo de `temperature` busca reducir la variabilidad de la respuesta y favorecer una salida más estable y consistente. El límite de `max_output_tokens` establece la longitud máxima de la respuesta generada por el modelo.

## Prompt de transformación

La función `build_tei_prompt(texto)` construye el prompt que se envía al modelo.

El prompt indica al modelo que convierta el texto dramático a XML-TEI DraCor y que devuelva únicamente XML, sin explicaciones ni texto adicional.

La estructura básica solicitada es:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://dracor.org/schema.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="es" xml:id="apellido-titulo">
  <teiHeader>...</teiHeader>
  <text>
    <front>...</front>
    <body>
      <div type="act" n="1">
        <head>ACTO</head>
        <div type="scene" n="1">
          <head>ESCENA</head>
          <stage type="action">acotación</stage>
          <sp who="#id">
            <speaker>NOMBRE</speaker>
            <p>texto</p>
          </sp>
        </div>
      </div>
    </body>
  </text>
</TEI>
```

El prompt incluye las siguientes reglas principales:

* `<stage>` debe llevar siempre `type="action"`.
* `<div type="scene">` debe estar dentro de `<div type="act">`.
* Debe generarse un único `<p>` por parlamento.
* Deben conservarse tildes y signos propios del español.
* En `<particDesc>` deben incluirse todos los personajes detectados.
* No deben usarse comentarios abreviados como `<!-- más personajes -->` o `<!-- resto de personajes -->`.

## Funcionamiento interno

El funcionamiento de la versión actual puede resumirse en cinco pasos:

1. El usuario carga o pega un texto dramático en la interfaz.
2. `main.py` recoge el texto del área de entrada.
3. La función `generate_tei_xml_largo(texto)` envía el texto a `tei_generator.py`.
4. `tei_generator.py` construye el prompt y llama al modelo Gemma.
5. La respuesta del modelo se muestra en la interfaz y puede guardarse como `.xml`.

El proceso se ejecuta en segundo plano mediante `threading.Thread`, para que la interfaz gráfica no se congele mientras se genera el XML.

## Gestión de errores y reintentos

La aplicación incluye un mecanismo básico de reintentos en caso de error de cuota.

Si la llamada al modelo devuelve errores relacionados con `429` o `RESOURCE_EXHAUSTED`, la aplicación:

1. espera 40 segundos;
2. reintenta la llamada;
3. repite el proceso hasta un máximo de tres intentos.

Si los tres intentos fallan, muestra un mensaje de error indicando que se ha excedido la cuota.

Este mecanismo está implementado en `generate_in_background()` dentro de `main.py`.

## Pipeline metodológico

Desde el punto de vista metodológico, el sistema se inscribe en un flujo más amplio de generación y evaluación de XML-TEI para teatro filipino en español.

El pipeline previsto para el enfoque basado en Gemma puede describirse así:

1. **Preparación del texto**
   Se parte de una obra teatral en texto plano (`.txt`), preferentemente revisada para eliminar errores graves de OCR.

2. **Construcción del prompt**
   Se genera una instrucción que especifica la estructura TEI-DraCor esperada, las reglas mínimas de marcado y el texto que debe codificarse.

3. **Llamada al modelo**
   El texto se envía al modelo `gemma-4-26b-a4b-it` mediante la biblioteca `google-genai`.

4. **Generación del XML**
   El modelo devuelve una propuesta de XML-TEI.

5. **Revisión de la salida**
   La salida debe revisarse para comprobar que no contiene texto introductorio, bloques Markdown, etiquetas sin cerrar, identificadores duplicados o referencias `who` no declaradas.

6. **Validación**
   El archivo resultante debe validarse contra el esquema DraCor.

7. **Postprocesado y corrección**
   En caso necesario, deben corregirse duplicados de personajes, identificadores inconsistentes, numeración de actos o escenas y omisiones de atributos obligatorios.

## Ejemplo de uso del módulo desde Python

Aunque la forma principal de uso es la interfaz gráfica, también es posible importar directamente las funciones desde otro script:

```python
from pathlib import Path
from tei_generator import generate_tei_xml_largo, save_tei_to_file

texto = Path("obra.txt").read_text(encoding="utf-8")

tei_xml = generate_tei_xml_largo(texto)

save_tei_to_file(tei_xml, "obra_tei_gemma.xml")
```

## Validación del XML generado

El XML generado debe validarse antes de considerarse resultado final.

Se recomienda comprobar:

* que el documento está bien formado;
* que valida contra el esquema DraCor;
* que todos los `xml:id` son únicos;
* que todos los valores de `who="#..."` remiten a personajes declarados;
* que no hay personajes duplicados en `<particDesc>`;
* que las escenas están anidadas dentro de actos;
* que todos los `<stage>` tienen el atributo `type="action"`, si se sigue esta regla del proyecto;
* que no hay introducciones generadas por el modelo, como “Aquí tienes el XML”;
* que no aparecen bloques de código Markdown;
* que no hay comentarios abreviados del tipo `<!-- más personajes -->`.

## Problemas frecuentes

### El modelo devuelve texto antes del XML

Puede ocurrir que el modelo devuelva una frase introductoria antes del XML. Por ejemplo:

```text
Aquí tienes el XML generado:
```

En ese caso, debe eliminarse manualmente o mediante un paso de limpieza automática.

### El modelo devuelve un bloque Markdown

A veces el modelo puede envolver el XML en un bloque como:

````text
```xml
...
````

````

Estos marcadores deben eliminarse antes de validar el documento.

### Hay personajes duplicados

Puede ocurrir que el modelo declare dos veces el mismo personaje en `<particDesc>`. Esto invalida el XML si se repite el mismo `xml:id`.

### Hay referencias `who` no declaradas

El modelo puede usar en un `<sp>` un identificador que no aparece en `<listPerson>`, por ejemplo:

```xml
<sp who="#sor-teresita">
````

sin que exista:

```xml
<person xml:id="sor-teresita">
```

Estas divergencias deben corregirse antes de validar el XML.

### Se repite el encabezado TEI

En procesos por fragmentos, el modelo puede repetir:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI>
```

en fragmentos intermedios. La versión actual no fragmenta automáticamente el texto, pero este problema debe tenerse en cuenta si se amplía el sistema.

### El XML es demasiado largo o se corta

El límite de salida del modelo puede hacer que una obra larga se genere de forma incompleta. Para estos casos se recomienda implementar procesamiento por fragmentos y posterior ensamblado.

## Limitaciones

La salida generada por esta aplicación debe considerarse una propuesta automática de marcado, no una edición TEI definitiva.

Entre las principales limitaciones se encuentran:

* dependencia de una clave de API;
* posible variabilidad de las respuestas del modelo;
* riesgo de XML incompleto en textos largos;
* posible aparición de identificadores inconsistentes;
* duplicación de personajes;
* omisión de atributos obligatorios;
* fragmentación indebida de parlamentos;
* necesidad de validación posterior;
* necesidad de revisión filológica humana.

Además, aunque el proyecto se orienta hacia la reproducibilidad y el uso de modelos abiertos o de pesos abiertos, la versión actual depende de una llamada mediante `google-genai`, por lo que la reproducibilidad completa exige documentar la versión exacta del modelo, la configuración de generación, la fecha de ejecución y las condiciones de acceso.

## Recomendaciones de uso

Para obtener mejores resultados:

* use archivos `.txt` limpios y codificados en UTF-8;
* revise encabezados de actos, jornadas y escenas;
* conserve los nombres de personajes de forma clara;
* evite enviar textos excesivamente largos si no se ha implementado fragmentación;
* valide siempre el XML generado;
* compare la salida con el texto fuente;
* revise manualmente `<listPerson>`, `<castList>` y los valores `who`;
* documente la fecha de generación, el modelo usado y la configuración de inferencia;
* no considere la salida como edición definitiva sin revisión humana.

## Cita

Si utiliza esta herramienta, cite el repositorio del proyecto:

```text
Andrea Alejandra Álvarez et al.. Teatro filipino en español: corpus, marcado TEI-DraCor y evaluación de métodos automáticos. GitHub.
```

También se recomienda citar DigiPhiLit, DraCor y TEI-P5 cuando se utilice el marcado generado como parte de una investigación académica.

## Licencia

https://creativecommons.org/licenses/by-nc/4.0/deed.es

## Advertencia metodológica

Los XML generados por esta aplicación son resultados experimentales de marcado automático. Deben validarse, revisarse y corregirse antes de su integración en un corpus académico, repositorio público o infraestructura como DraCor.
