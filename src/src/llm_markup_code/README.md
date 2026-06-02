Este proyecto automatiza la conversión de obras de teatro filipino en formato de texto plano (.txt) a XML-TEI compatible con el esquema DraCor mediante el modelo de lenguaje de Gemma 4 26B (Google DeepMind).

El sistema está diseñado para el procesamiento de textos dramáticos y genera automáticamente una estructura TEI completa que incluye actos, escenas, parlamentos, personajes y acotaciones. 

 Los requisitos son los siguientes: 
 - Pyhton 3.10 o superior
 - Descargar el código main.py y tei_generator.py, guardarlos en una carpeta titulada "app_tei_gemma" o similiar en tu ordenador
 - Biblioteca google-genai: Abrir una terminal dentro de la carpeta creada y luego instalar la biblioteca -->"pip install google genai".

Para obtener la API Key de Google debes:
 - Acceder a: https://aistudio.google.com/.
 - Iniciar seción con una cuenta Google
 - Ir a la sección Get API Key
 - Seleccionar Create API Key
 - Copiar la clave generada y pegarla en el código dentro de: client = genai.Client(api_key="TU_API_KEY")
