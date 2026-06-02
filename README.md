# Teatro filipino en español: corpus, marcado TEI-DraCor y evaluación de métodos automáticos

## Descripción general

Este repositorio reúne materiales, código y resultados derivados de un proyecto de Humanidades Digitales dedicado a la edición, codificación y evaluación computacional de obras de teatro filipinas escritas en español entre los siglos XIX y XX.

El objetivo principal del repositorio es documentar y comparar dos estrategias de marcado automático en TEI-XML conforme a las directrices de DraCor:

1. **Marcado automatizado mediante expresiones regulares**.
2. **Marcado asistido por modelo de lenguaje**, mediante una aplicación que interactúa con `gemma-4-26b-a4b-it`.

El repositorio incluye también los textos fuente en `.txt`, las versiones codificadas en TEI-XML, el sistema de evaluación utilizado para comparar los resultados y la documentación metodológica necesaria para reproducir el flujo de trabajo.

DraCor —Drama Corpora Project— es una infraestructura abierta para el estudio computacional del teatro que trabaja con textos dramáticos codificados en TEI y orientados al análisis literario, comparativo y computacional. Este proyecto adopta sus recomendaciones de marcado para facilitar la interoperabilidad futura del corpus con ecosistemas de análisis dramático y redes de personajes.

## Objetivos del repositorio

Este repositorio tiene los siguientes objetivos:

- Preservar y ofrecer acceso estructurado a un corpus de teatro filipino en español.
- Facilitar la transformación de textos dramáticos en formato plano a TEI-XML.
- Comparar dos métodos de marcado automático: uno basado en reglas y otro apoyado en un modelo de lenguaje.
- Documentar un sistema de evaluación aplicable al marcado estructural de textos teatrales.
- Contribuir al desarrollo de recursos digitales sobre literatura filipina en español.
- Favorecer la reutilización del corpus en investigaciones sobre teatro, literatura hispanofilipina, historia cultural, análisis de redes de personajes, estilometría y procesamiento del lenguaje natural.

## Corpus

El corpus con el que trabajamos se compone de un conjunto de 15 obras teatrales escritas en lengua española por personas filipinas entre 1880 y 1954 coincidiendo con la época de mayor esplendor de la literatura filipina en lengua española llamada por Luis Mariñas Otero “Edad de oro” (1974). 

| Nº | Título | Autor/a | Fecha | Género / descripción | Fuente o edición de referencia | Localización / repositorio | URL |
|---:|---|---|---|---|---|---|---|
| obra_01 | *Alma filipina* | Severino Reyes | 1911 | Comedia en un acto y en prosa | Edición digital a partir de Manila, Imprenta Librería y Papelería de I. R. Morales, 1911 | Main Library of the University of the Philippines, Diliman Campus, Quezon City / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/obra/alma-filipina---comedia-en-un-acto-y-en-prosa/ |
| obra_02 | *Flor del Carmelo* | Jesús Balmori | Interpretada por primera vez en 1934 | Obra teatral | Edición digital a partir de [Manila], [editor no identificado, fecha de publicación no identificada] | National Library of the Philippines, Manila / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc4j295 |
| obra_03 | *Brumas y voces* | Adelina Gurrea | Lectura pública en 1952 | Obra teatral | Edición digital | Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc059h1 |
| obra_04 | *El consejo de los dioses* | José Rizal; arreglada en forma teatral por Lope Blas Hucapte | 1880 | Obra arreglada en forma teatral | Edición digital | Project Gutenberg | https://www.gutenberg.org/ebooks/14796 |
| obra_05 | *La mejor ofrenda* | Rosa Sevilla de Alvero | 1917 | Obra teatral | Imprenta Sevilla, Metro Manila | National Library of Australia | — |
| obra_06 | *Fortalezas* | Adelina Gurrea | 1936 | Obra inédita | Edición digital | Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmcsr0t7 |
| obra_07 | *José el Carpintero* | Juan Zulueta de los Ángeles | 1880 | Obra teatral | Imprenta de la Oceanía Española, Metro Manila | Biblioteca Nacional de Filipinas | https://nlpdl.nlp.gov.ph/JB02/1880/NLPJBBK31021f/bs/datejpg.htm |
| obra_08 | *Katipunan* | José Cruz Rivera | 1902 | Obra teatral | Barcelona, Establecimiento Tipográfico de Pedro Toll | Biblioteca digital de la Universidad de Santo Tomás de Manila | https://digilib.ust.edu.ph/digital/collection/section5/id/30931/ |
| obra_09 | *La realización* | José B. Gamboa | 1910 | Obra teatral | Imprenta de Juan Fajardo, Metro Manila | Biblioteca digital de la Universidad de Santo Tomás de Manila | http://digitallibrary.ust.edu.ph/cdm/compoundobject/collection/section5/id/245823/rec/14 |
| obra_10 | *Filipinas. Auto histórico sacramental* | Adelina Gurrea | 1954 | Auto histórico sacramental | Imprenta Agustiniana, Valladolid | Biblioteca Virtual Miguel de Cervantes | http://www.cervantesvirtual.com/nd/ark:/59851/bmcrn560 |
| obra_11 | *La ruta de Damasco* | Claro M. Recto | 1913 | Obra teatral | Imprenta de Juan Fajardo, Metro Manila | Biblioteca Virtual Miguel de Cervantes | http://www.cervantesvirtual.com/nd/ark:/59851/bmc4j299 |
| obra_12 | *Prisionera de amor* | Rosa Sevilla de Alvero | 1922 | Obra teatral | — | National Library of the Philippines | — |
| obra_13 | *El cablegrama fatal* | Severino Reyes | 1915 / edición de 1916 | Obra escrita para la Compañía Torrijos-Blay, representada en el Teatro Zorrilla de Manila el 30 de diciembre de 1915 | Edición digital a partir de Manila, Imprenta Librería y Papelería de I. R. Morales, 1916 | Main Library of the University of the Philippines, Diliman Campus, Quezon City / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc0w065 |
| obra_14 | *Junto al Pásig* | José Rizal | Representada por primera vez el 8 de diciembre de 1880; editada en *Día Filipino* en 1915 | Obra teatral | Digitalizada por Project Gutenberg | Project Gutenberg | https://www.gutenberg.org/cache/epub/14795/pg14795-images.html |
| obra_15 | *Ricos y pobres* | Isabelo de los Reyes | Publicada entre noviembre de 1903 y diciembre de 1904 | Obra publicada por entregas en prensa | Publicada en el periódico *La Redención del obrero* | — | — |

## Cita

Si utiliza este repositorio, cite el proyecto de la siguiente forma:

Álvarez, Alejandra, Cristina Jiménez y Rocío Ortuño Casanova. Teatro filipino en español: corpus, marcado TEI-DraCor y evaluación de métodos automáticos. 
Repositorio GitHub, 2026. [https://github.com/DigiPhiLit/teatro-filipino]

## Licencia

Este repositorio se distribuye bajo la licencia CC BY-NC (Reconocimiento - NoComercial).

## Equipo

**Investigadora principal:** Rocío Ortuño Casanova
**Institución:** Laboratorio de Innovación en Humanidades Digitales (LINHD) de la UNED
**Equipo de investigación:** Alejandra Álvarez y Cristina Jiménez
**Contacto:** info@linhd.uned.es

## Agradecimientos

Este repositorio forma parte del proyecto DigiPhiLit, desarrollado en el ámbito de las Humanidades Digitales y la literatura hispanofilipina.
Agradecemos a la Biblioteca Virtual Miguel de Cervantes, la Hemeroteca Digital de la Biblioteca Nacional de España, la National Library of the Philippines y la Digital Library de la Universidad de Santo Tomas de Manila por su apoyo en la digitalización y publicación online de las obras incluidas en este corpus.


