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
| obra_01 | *Alma filipina* | Severino Reyes | 1911 | Comedia en un acto y en prosa | Imprenta Librería y Papelería de I. R. Morales, Manila | Main Library of the University of the Philippines, Diliman Campus / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/obra/alma-filipina---comedia-en-un-acto-y-en-prosa/ |
| obra_02 | *Flor del Carmelo* | Jesús Balmori | Interpretada por primera vez en 1934 | Poema dramático en cuatro jornadas, verso y prosa | Obra mecanografiada inédita | National Library of the Philippines, Manila / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc4j295 |
| obra_03 | *Brumas y voces* | Adelina Gurrea | Lectura pública en 1952 | Obra teatral en tres actos| Obra mecanografiada inédita | Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc059h1 |
| obra_04 | *El consejo de los dioses* | José Rizal; arreglada en forma teatral por Lope Blas Hucapte | 1880 (1915) | Alegoría arreglada en forma teatral | Imprenta y taller de encuadernación del *Día Filipino*, Manila | Project Gutenberg | https://www.gutenberg.org/ebooks/14796 |
| obra_05 | *La mejor ofrenda* | Rosa Sevilla de Alvero | 1917 | Fantástico melodrama en dos actos | Imprenta Sevilla, Manila | National Library of Australia | https://catalogue.nla.gov.au/catalog/634074 |
| obra_06 | *Fortalezas* | Adelina Gurrea | 1936 | Comedia en tres actos, en prosa | Obra mecanografiada inédita | Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmcsr0t7 |
| obra_07 | *José el Carpintero* | Juan Zulueta de los Ángeles | 1880 | Comedia en un acto y en verso de costumbres filipinas |Imprenta de la Oceanía Española, Manila | Biblioteca Nacional de Filipinas | https://nlpdl.nlp.gov.ph/JB02/1880/NLPJBBK31021f/bs/datejpg.htm |
| obra_08 | *Katipunan* | José Cruz Rivera | 1902 | Drama histórico filipino en tres actos y en prosa | Establecimiento Tipográfico de Pedro Toll, Barcelona | Biblioteca digital de la Universidad de Santo Tomás de Manila | https://digilib.ust.edu.ph/digital/collection/section5/id/30931/ |
| obra_09 | *La realización* | José B. Gamboa | 1910 | Drama en cuatro actos con un prólogo y en prosa | Imprenta de Juan Fajardo, Metro Manila | Biblioteca digital de la Universidad de Santo Tomás de Manila | http://digitallibrary.ust.edu.ph/cdm/compoundobject/collection/section5/id/245823/rec/14 |
| obra_10 | *Filipinas* | Adelina Gurrea | 1954 | Auto histórico satírico | Imprenta Agustiniana, Valladolid | Biblioteca Virtual Miguel de Cervantes | http://www.cervantesvirtual.com/nd/ark:/59851/bmcrn560 |
| obra_11 | *La ruta de Damasco* | Claro M. Recto | 1913 | Drama en un acto | Imprenta de Juan Fajardo, Metro Manila | Biblioteca Virtual Miguel de Cervantes | http://www.cervantesvirtual.com/nd/ark:/59851/bmc4j299 |
| obra_12 | *Prisionera de amor* | Rosa Sevilla de Alvero | 1922 | Drama lírico en tres actos | Imprenta Sevilla | National Library of the Philippines. Balmaceda Collection | https://nlpdl.nlp.gov.ph/JB02/1922/NLPJBBK31095f/bs/datejpg.htm |
| obra_13 | *El cablegrama fatal* | Severino Reyes | Obra escrita para la Compañía Torrijos-Blay, representada en el Teatro Zorrilla de Manila el 30 de diciembre de 1915. Edición de 1916 | Intermedio histórico | Imprenta Librería y Papelería de I. R. Morales, Manila | Main Library of the University of the Philippines, Diliman / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc0w065 |
| obra_14 | *Junto al Pásig* | José Rizal | Representada por primera vez el 8 de diciembre de 1880; editada en *Día Filipino* en 1915 | Melodrama en un acto y en verso | Imprenta y taller de encuadernación del *Día Filipino*, Manila | Project Gutenberg | https://www.gutenberg.org/cache/epub/14795/pg14795-images.html |
| obra_15 | *Ricos y pobres* | Isabelo de los Reyes | Publicada entre noviembre de 1903 y diciembre de 1904 | Zarzuela filipina en tres actos | Publicada por entregas en el periódico *La Redención del obrero* | Hemeroteca Digital de la Biblioteca Nacional de España | https://hemerotecadigital.bne.es/hd/es/card?sid=5c49e3b5-fbb1-4e94-9a90-16b4599a2082 |
| obra_16 | *Filipinizad a los filipinos* | Jesús Balmori | 1940 | Comedia en tres jornadas | Obra mecanografiada inédita | National Library of the Philippines/ Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc69901 |
| obra_17 | *Solo entre las sombras* | Claro M. Recto | 1917 | Drama en un acto y en prosa | Obra mecanografiada inédita | Biblioteca de filipiniana del Instituto Cervantes de Manila/ Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc5t5c4 |

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


