from google import genai
from google.genai import types

API_KEY = "AIzaSyCVItBlmYGatWzQzTEGTa-TGiZH0vn9oMk"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemma-4-26b-a4b-it"


def build_tei_prompt(texto: str) -> str:
    return f'''Convierte este texto dramático a XML-TEI DraCor. Devuelve SOLO el XML.

Estructura:
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://dracor.org/schema.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="es" xml:id="apellido-titulo">
<teiHeader>...(título, autor, fuentes, personajes)...</teiHeader>
<text><front>...(dramatis personae si existe)...</front>
<body>
  <div type="act" n="1"><head>ACTO</head>
    <div type="scene" n="1"><head>ESCENA</head>
      <stage type="action">acotación</stage>
      <sp who="#id"><speaker>NOMBRE</speaker><p>texto</p></sp>
    </div>
  </div>
</body></text></TEI>

Reglas: <stage> siempre type="action". <div type="scene"> dentro de <div type="act">. Un <p> por parlamento. Conserva tildes y signos españoles.
En <particDesc> incluye TODOS los personajes que aparecen en el texto, cada uno con su elemento <person> completo. NO abrevies con comentarios como "<!-- más personajes -->", "<!-- resto de personajes -->" o similares. Escribe TODOS los <person> uno por uno.

TEXTO:
{texto}'''


def generate_tei_xml(texto: str) -> str:
    prompt = build_tei_prompt(texto)
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=65536,
            temperature=0.1,
        )
    )
    print(f"finish_reason: {response.candidates[0].finish_reason if response.candidates else 'N/A'}")
    print(f"caracteres recibidos: {len(response.text) if response.text else 0}")
    return response.text or ""


def generate_tei_xml_largo(texto: str) -> str:
    return generate_tei_xml(texto)


def save_tei_to_file(tei_xml: str, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tei_xml)
