Esta herramienta convierte obras de teatro en formato de texto plano (.txt) a XML-TEI compatible con el esquema DraCor. Funciona íntegramente en local: no requiere conexión a internet, cuenta en ningún servicio externo ni clave de API.

PASO 1- Requisitos
1. Python 3.10 o superior instalado en el ordenador
2. Descargar el archivo tei_generator.py desde el repositorio y guardarlo en una carpeta de trabajo, por ejemplo "RegEx" en el escritorio
3. No es necesario instalar ninguna biblioteca adicional

PASO 2- Crear el script de conversión
El texto de entrada debe ser un archivo .txt en codificación UTF-8. Antes de convertir,conviene revisar que el .txt no tiene errores graves de OCR como palabras partidas, números de página aislados o caracteres extraños que puedan afectar al resultado.
Para cada obra, crea un archivo .py en la misma carpeta "RegEx" con el siguiente contenido (sustituye los datos en mayúsculas):
from tei_generator import generar_tei
from pathlib import Path

texto = Path("NOMBRE_ARCHIVO.txt").read_text(encoding="utf-8")
xml = generar_tei(texto,
                  titulo="TÍTULO DE LA OBRA",
                  autor="NOMBRE DEL AUTOR/A",
                  fecha="AÑO",
                  idioma="es")
Path("NOMBRE_SALIDA_tei.xml").write_text(xml, encoding="utf-8")
print("Listo")

PASO 3- Ejecutar desde la terminal
Abre la terminal, navega a la carpeta donde están los archivos y ejecuta el script:
cd ~/Desktop/regEx
python3 mi_script.py
El archivo XML-TEI se genera en la misma carpeta de forma instantánea.

Nota: la ruta ~/Desktop/regEx funciona en macOS y Linux. En Windows, usa cd%USERPROFILE%\Desktop\regEx
