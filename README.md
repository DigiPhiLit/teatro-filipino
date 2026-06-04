# Teatro filipino en español: corpus, marcado TEI-DraCor y evaluación de métodos automáticos

[![DOI](https://zenodo.org/badge/1246490470.svg)](https://doi.org/10.5281/zenodo.20545041)
<img width="191" height="20" alt="image" src="https://github.com/user-attachments/assets/06cd607b-5c38-4ec6-8da2-5b369f818b9a" />


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

El corpus con el que trabajamos se compone de un conjunto de 9 obras teatrales escritas en lengua española por personas filipinas entre 1880 y 1954 coincidiendo con la época de mayor esplendor de la literatura filipina en lengua española llamada por Luis Mariñas Otero “Edad de oro” (1974). 

| Nº | Título | Autor/a | Fecha | Género / descripción | Fuente o edición de referencia | Localización / repositorio | URL |
|---:|---|---|---|---|---|---|---|
| obra_01 | *Alma filipina* | Severino Reyes | 1911 | Comedia en un acto y en prosa | Imprenta Librería y Papelería de I. R. Morales, Manila | Main Library of the University of the Philippines, Diliman Campus / Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/obra/alma-filipina---comedia-en-un-acto-y-en-prosa/ |
| obra_02 | *Brumas y voces* | Adelina Gurrea | Lectura pública en 1952 | Obra teatral en tres actos| Obra mecanografiada inédita | Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc059h1 |
| obra_03 | *El consejo de los dioses* | José Rizal; arreglada en forma teatral por Lope Blas Hucapte | 1880 (1915) | Alegoría arreglada en forma teatral | Imprenta y taller de encuadernación del *Día Filipino*, Manila | Project Gutenberg | https://www.gutenberg.org/ebooks/14796 |
| obra_04 | *La mejor ofrenda* | Rosa Sevilla de Alvero | 1917 | Fantástico melodrama en dos actos | Imprenta Sevilla, Manila | National Library of Australia | https://catalogue.nla.gov.au/catalog/634074 |
| obra_05 | *Fortalezas* | Adelina Gurrea | 1936 | Comedia en tres actos, en prosa | Obra mecanografiada inédita | Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmcsr0t7 |
| obra_06 | *José el Carpintero* | Juan Zulueta de los Ángeles | 1880 | Comedia en un acto y en verso de costumbres filipinas |Imprenta de la Oceanía Española, Manila | Biblioteca Nacional de Filipinas | https://nlpdl.nlp.gov.ph/JB02/1880/NLPJBBK31021f/bs/datejpg.htm |
| obra_07 | *Filipinas* | Adelina Gurrea | 1954 | Auto histórico satírico | Imprenta Agustiniana, Valladolid | Biblioteca Virtual Miguel de Cervantes | http://www.cervantesvirtual.com/nd/ark:/59851/bmcrn560 |
| obra_08 | *Filipinizad a los filipinos* | Jesús Balmori | 1940 | Comedia en tres jornadas | Obra mecanografiada inédita | National Library of the Philippines/ Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc69901 |
| obra_09 | *Solo entre las sombras* | Claro M. Recto | 1917 | Drama en un acto y en prosa | Obra mecanografiada inédita | Biblioteca de filipiniana del Instituto Cervantes de Manila/ Biblioteca Virtual Miguel de Cervantes | https://www.cervantesvirtual.com/nd/ark:/59851/bmc5t5c4 |

## Autores
A continuación se consigna una tabla con los autores de los textos

|Apellidos | Nombre | Fecha de nacimiento | Muerte | Género | Wikidata ID |
|---:|---|---|---|---|---|
| Balmori | Jesús | 1887 | 1948 | Hombre | https://www.wikidata.org/wiki/Q517332 |
| Gurrea | Adelina | 1896 | 1971 | Mujer | https://www.wikidata.org/wiki/Q2824209 |
| Recto | Claro M. | 1890 | 1960 | Hombre | https://www.wikidata.org/wiki/Q1095906 |
| Reyes | Severino | 1861 | 1942 | Hombre | https://www.wikidata.org/wiki/Q3548400 |
| Rizal | José | 1861 | 1896 | Hombre | https://www.wikidata.org/wiki/Q1500 |
| Sevilla de Alvero | Rosa | 1879 | 1954 | Mujer | https://www.wikidata.org/wiki/Q12970135 |
| Zulueta de los Ángeles | Juan | 1844 | 1896 | Hombre |  |

## Cita

Si utiliza este repositorio, cite el proyecto de la siguiente forma:

Álvarez, Andrea, Cristina Jiménez y Rocío Ortuño Casanova. Teatro filipino en español: corpus, marcado TEI-DraCor y evaluación de métodos automáticos. 
Repositorio GitHub, 2026. [https://github.com/DigiPhiLit/teatro-filipino]

## Licencia

Este repositorio se distribuye bajo la licencia CC BY-NC (Reconocimiento - NoComercial).

## Equipo

**Investigadora principal:** Rocío Ortuño Casanova
**Institución:** Laboratorio de Innovación en Humanidades Digitales (LINHD) de la UNED
**Equipo de investigación:** Andrea Álvarez y Cristina Jiménez
**Contacto:** info@linhd.uned.es

## Agradecimientos

Este repositorio forma parte del proyecto DigiPhiLit, desarrollado en el ámbito de las Humanidades Digitales y la literatura hispanofilipina.
Agradecemos a la Biblioteca Virtual Miguel de Cervantes, la Hemeroteca Digital de la Biblioteca Nacional de España, la National Library of the Philippines, la National Library of Australia, la Digital Library de la Universidad de Santo Tomas de Manila y la biblioteca del Instituto Cervantes de Manila por su apoyo en la digitalización y publicación online de las obras incluidas en este corpus.


