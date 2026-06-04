# Resultados de evaluación

Esta carpeta contiene los resultados derivados de la comparación entre dos métodos de generación automática de marcado XML-TEI para un corpus de teatro filipino en español:

1. un sistema basado en expresiones regulares (**RegEx**);
2. un sistema basado en el modelo de lenguaje **Gemma**.

Los resultados se calculan tomando como referencia un **gold standard** XML-TEI marcado manualmente conforme a las directrices de DraCor y TEI-P5.

## Estructura de la carpeta

```text
results/
├── README.md
├── prompts/
│   └── claude_evaluation_prompt.md
├── results_manifest.json
├── tables/
│   ├── corpus_overview.csv
│   ├── global_comparison.csv
│   ├── per_label_metrics_all.csv
│   ├── error_typology.csv
│   ├── metric_definitions.csv
│   └── per_work/
│       ├── alma_filipina.csv
│       ├── brumas_y_voces.csv
│       ├── el_consejo_de_los_dioses.csv
│       ├── filipinas_auto_historico.csv
│       ├── filipinizad_a_los_filipinos.csv
│       ├── solo_entre_las_sombras.csv
│       ├── fortalezas.csv
│       ├── la_mejor_ofrenda.csv
│       └── jose_el_carpintero.csv
└── summaries/
    ├── evaluation_methodology.md
    ├── global_results_summary.md
    └── limitations.md
Archivos principales
tables/corpus_overview.csv

Relación de obras incluidas en el estudio, con título, autoría, año, editorial o fuente, ubicación y enlace.

tables/global_comparison.csv

Tabla resumen por obra. Incluye:

número total de elementos en el gold standard;
número de elementos generados por RegEx;
macro-F1 de RegEx;
número de elementos generados por Gemma;
macro-F1 de Gemma;
sistema ganador por obra.
tables/per_label_metrics_all.csv

Tabla agregada con las métricas por obra y por etiqueta. Incluye las columnas:

obra_id
obra_titulo
etiqueta
gold_n
regex_n
regex_precision
regex_recall
regex_f1
gemma_n
gemma_precision
gemma_recall
gemma_f1
tables/per_work/

Contiene una tabla CSV independiente para cada obra. Estas tablas reproducen las métricas por etiqueta empleadas para comparar RegEx y Gemma con el gold standard.

tables/error_typology.csv

Tipología de errores observados en ambos sistemas. Resume problemas de cobertura, fallos estructurales, clasificación errónea, invención o sobreinterpretación de etiquetas.

tables/metric_definitions.csv

Definiciones de las métricas empleadas en la evaluación: precisión, recall, F1, macro-F1 y aproximación de verdaderos positivos.

summaries/evaluation_methodology.md

Resumen metodológico de la evaluación.

summaries/global_results_summary.md

Resumen interpretativo de los resultados globales.

summaries/limitations.md

Limitaciones del cálculo y de los sistemas evaluados.

Métricas

La evaluación emplea tres métricas principales:

Precisión = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2·P·R / (P + R)

El cálculo se realiza sobre recuentos agregados por tipo de etiqueta. Los verdaderos positivos se aproximan como:

TP = min(pred, gold)

Por este motivo, los valores F1 deben interpretarse como un límite superior: si algunas etiquetas generadas coinciden en número pero no en posición o contenido textual, el F1 real sería inferior.

Resultado global

En el conjunto del corpus:

Gemma obtiene mejor resultado en 7 de las 9 obras.
RegEx obtiene mejor resultado en 2 de las 9 obras.
El promedio macro-F1 es 0.596 para RegEx y 0.818 para Gemma.

Estos resultados muestran que Gemma ofrece mayor flexibilidad ante estructuras textuales heterogéneas, mientras que RegEx funciona especialmente bien cuando la tipografía de la obra coincide con los patrones previstos.

Advertencia

Los resultados incluidos en esta carpeta deben interpretarse como datos de evaluación experimental. La validez filológica de los XML generados requiere revisión manual y validación contra el esquema DraCor antes de su integración en un corpus académico.

 ​:contentReference[oaicite:1]{index=1}

## Asistencia con modelo de lenguaje en la evaluación

El cálculo de las métricas y la elaboración de las tablas comparativas se realizaron con asistencia de Claude.ai, a partir de los archivos XML generados por los sistemas RegEx y Gemma y del gold standard XML-TEI marcado manualmente.

Claude.ai se utilizó como herramienta auxiliar para:

- comparar recuentos de etiquetas entre sistemas;
- organizar las métricas por obra y por tipo de etiqueta;
- calcular precisión, recall y F1;
- detectar discrepancias estructurales;
- sistematizar una tipología de errores.

Los resultados obtenidos fueron revisados por el equipo investigador antes de su incorporación al repositorio. Por tanto, las tablas deben entenderse como resultados de evaluación asistida por modelo de lenguaje y no como una validación automática independiente.

Para favorecer la transparencia y la reproducibilidad metodológica, el prompt utilizado se conserva en:

```text
results/prompts/claude_evaluation_prompt.md​
