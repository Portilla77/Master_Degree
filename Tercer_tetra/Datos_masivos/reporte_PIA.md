<h1 align="center">Proyecto Final Datos Masivos</h1>
<h2 align="center">Algoritmo de recomendación basado en contenido</h2>
<p align="center"><strong>Equipo:</strong> Jorge Ramón Flores Portilla 1550162 y Luis Edgar Rodriguez Lerma 1620401</p>
<p align="center"><strong>Maestro:</strong> Christian Aguilar Fuster</p>
<p align="center"><strong>Materia:</strong> Datos Masivos</p>

### Introducción

En este proyecto se desarrolló una aplicación en Python orientada a la recomendación de productos, enfocándose concretamente en canciones. Se eligió el enfoque basado en contenido, lo que implica que las recomendaciones se generan analizando las características propias de cada ítem, sin necesidad de depender de opiniones o interacciones previas de usuarios. Es decir, el sistema compara la información interna de cada canción, como su nivel de energía, la presencia de elementos románticos, la violencia en su contenido, la presencia de música o lugares, su duración (representada como "len") y su grado de movimiento.

El objetivo principal fue implementar un sistema que pudiera identificar qué canciones son más similares entre sí utilizando estas características numéricas. Esto permite, por ejemplo, que al seleccionar una canción, el sistema pueda devolver un conjunto de canciones que comparten un perfil similar desde el punto de vista de sus atributos musicales y temáticos.

Además del diseño del algoritmo de recomendación, se consideró como parte fundamental del proyecto la forma en que los datos son procesados y cargados en memoria, especialmente debido al volumen del conjunto de datos utilizado, que contiene más de 28,000 registros. Por esta razón, se integraron diferentes técnicas de lectura de datos masivos. Se exploraron tres enfoques principales para ello: la lectura secuencial utilizando pandas, el uso de procesamiento en paralelo a través de la librería multiprocessing y la computación distribuida utilizando Dask. Si bien esta parte no constituye el núcleo del sistema de recomendación, fue clave para mejorar el rendimiento general y reducir los tiempos de ejecución, especialmente en las pruebas con conjuntos de datos grandes.

También se implementaron múltiples métricas de similitud para comparar los resultados y determinar cuál ofrecía mejores recomendaciones y rendimiento. Las métricas utilizadas fueron la similitud del coseno, la distancia euclidiana inversa, la correlación de Pearson y la similitud de Jaccard. Estas fueron probadas bajo diferentes tamaños de muestra para analizar su comportamiento en términos de precisión y costo computacional.

En conjunto, este proyecto permitió integrar conocimientos de estructuras de datos, manejo eficiente de archivos masivos, programación concurrente y fundamentos de sistemas de recomendación, generando una herramienta funcional y analíticamente respaldada para la recomendación de canciones.

---

### Planteamiento del problema

Actualmente los usuarios estamos constantemente expuestos a grandes volúmenes de información y productos, lo que hace cada vez más difícil encontrar contenido relevante o de interés personal de forma eficiente. Este fenómeno es especialmente evidente en plataformas de streaming de música, donde los catálogos pueden contener cientos de miles de canciones. En este contexto, los sistemas de recomendación se han convertido en herramientas fundamentales para personalizar la experiencia del usuario y facilitar el descubrimiento de nuevos contenidos.

El desarrollo de un sistema de recomendación efectivo implica varios retos. En primer lugar, la naturaleza masiva de los datos representa una carga considerable para los sistemas de procesamiento tradicionales. A medida que el volumen de datos crece, el tiempo necesario para analizarlos y generar recomendaciones también aumenta, afectando directamente la escalabilidad del sistema. Esto hace necesario explorar técnicas de procesamiento paralelo y distribuido que permitan optimizar los tiempos de lectura y cálculo, especialmente al trabajar con archivos CSV de gran tamaño, como ocurre en este proyecto.

Por otro lado, existen distintos enfoques para implementar sistemas de recomendación. Los sistemas colaborativos, por ejemplo, requieren información sobre la interacción entre usuarios e ítems (como calificaciones, clics o compras). Sin embargo, en muchos casos reales, dichos datos no están disponibles o son insuficientes para construir modelos precisos. Por esta razón, el enfoque basado en contenido resulta una alternativa más viable. Este enfoque se fundamenta en describir los ítems mediante un conjunto de características numéricas, y luego calcular la similitud entre ellos para encontrar elementos que se parezcan al ítem de referencia.

En el caso de la música, es posible representar cada canción como un vector de características como danceability, energy, len, romantic, violence, music, y movement/places. Estas variables permiten capturar distintos aspectos musicales y emocionales de las canciones, lo que facilita la comparación entre ellas.

A pesar de lo anterior, surge un nuevo reto: la elección de la métrica de similitud adecuada. Esta decisión no solo afecta la calidad de las recomendaciones, sino también el rendimiento computacional del sistema. Métricas como la similitud del coseno, la distancia euclidiana, la correlación de Pearson o el índice de Jaccard tienen diferentes comportamientos frente a datos con distintas escalas, distribuciones o niveles de dispersión. Por lo tanto, es necesario comparar su desempeño tanto en términos cualitativos (calidad de las recomendaciones) como en términos cuantitativos (tiempo de ejecución y consumo de recursos).

En resumen, el problema a resolver consiste en desarrollar un sistema de recomendación basado en contenido que sea capaz de:
- Procesar eficientemente un conjunto de datos masivo utilizando estrategias de paralelismo y lectura optimizada.
- Generar recomendaciones precisas a partir de características numéricas.
- Evaluar el impacto de diferentes métricas de similitud sobre el rendimiento y la calidad del sistema.

Este planteamiento integra aspectos de ingeniería de datos, optimización de recursos y aprendizaje automatizado, alineándose con los objetivos del curso de Datos Masivos.

---

### Solución propuesta

Para resolver el problema planteado se diseñó una solución en dos frentes principales:

1. Optimizar la lectura de datos masivos usando técnicas paralelas.
2. Implementar un sistema de recomendación basado en contenido con diferentes métricas de similitud para evaluar su desempeño.

**Lectura eficiente de datos**

Dado que el archivo de entrada (tcc_ceds_music.csv) contiene más de 23,000 canciones, leer el archivo completo puede ser costoso en tiempo y recursos. Para mitigar este problema se implementaron tres métodos distintos:

**Pandas**
- Lectura tradicional del archivo con pandas.read_csv(). Es secuencial y de un solo hilo. Se utilizó como línea base de comparación.

**Multiprocessing**
- Implementamos una lectura por chunks usando el módulo multiprocessing. El archivo se divide en bloques de tamaño definido (chunksize), y cada bloque se lee en paralelo usando múltiples núcleos. Esto mejora significativamente la lectura en comparación con el enfoque secuencial.

**Dask**
- Dask es una librería que permite computación paralela sobre estructuras similares a NumPy y Pandas. Su ventaja es que maneja automáticamente la distribución de tareas y aprovecha múltiples núcleos para procesar datos más grandes que la memoria.
En nuestro proyecto, read_with_dask() logró los mejores tiempos de lectura y fue seleccionado como el método final para cargar los datos antes del proceso de recomendación.

---

**Sistema de recomendación basado en contenido**

Una vez cargados los datos, el sistema de recomendación opera bajo un enfoque basado en contenido. Este enfoque consiste en:

- Representar cada ítem (canción) como un vector de características numéricas.
- Calcular la similitud entre canciones.
- Retornar las canciones más similares al ítem objetivo.

Las columnas numéricas utilizadas como características fueron:

- danceability
- energy
- len (longitud de la canción en segundos)
- romantic
- violence
- music
- movement/places

---

**Métricas de similitud utilizadas**

A continuación se presentan las métricas evaluadas, sus fórmulas y cómo fueron aplicadas específicamente en nuestro conjunto de datos:

---

**1. Similitud del coseno**

Fórmula general:

$sim_{\text{coseno}}(A, B) = \frac{A \cdot B}{\|A\| \cdot \|B\|}$


Donde:
- A y B son vectores de características de dos canciones.
- $A \cdot B$ es el producto punto.
- $\|A\|$ es la norma (magnitud) del vector A.

**Aplicación en el proyecto:**

Cada vector $A$ y $B$ representa una canción, descrita por las columnas:

El producto punto y norma se calcula directamente entre estos vectores para obtener su similitud.

---

**2. Distancia euclidiana (convertida a similitud)**

Fórmula general:

$\text{dist}_{\text{euclidiana}}(A, B) = \sqrt{\sum (A_i - B_i)^2}$

$sim_{\text{euclidiana}}(A, B) = \frac{1}{1 + \text{dist}_{\text{euclidiana}}(A, B)}$


**Aplicación en el proyecto:**

Se calcula la distancia entre dos canciones $A$ y $B$ utilizando las mismas columnas numéricas. Luego se transforma en una medida de similitud inversa (a menor distancia, mayor similitud).

---

**3. Correlación de Pearson**

Fórmula general:

$sim_{\text{pearson}}(A, B) = \frac{\text{cov}(A, B)}{\sigma_A \cdot \sigma_B}$


Donde:
- $\text{cov}(A, B)$ es la covarianza entre $A$ y $B$.
- $\sigma_A$, $\sigma_B$ son las desviaciones estándar de $A$ y $B$.

**Aplicación en el proyecto**:

Se toma cada fila del DataFrame como un vector de características de una canción. La correlación de Pearson se calcula entre cada par de vectores (filas), considerando las mismas 7 columnas mencionadas anteriormente.

---

**4. Índice de Jaccard**

Fórmula general (para vectores binarios):

$sim_{\text{jaccard}}(A, B) = \frac{|A \cap B|}{|A \cup B|}$


**Aplicación en el proyecto**:

- Primero, cada valor numérico se convierte a binario: $1$ si es mayor que $0$, $0$ si no.
- Luego se calculan la intersección (coincidencias en $1$) y la unión (presencia de $1$ en al menos uno).
- Se aplica la fórmula de Jaccard sobre los vectores binarizados de las características de las canciones.

---

**Fórmula general del algoritmo basado en contenido**

La lógica general del algoritmo se puede describir como:

$\text{similaridad}(i, j) = \text{métrica}( \vec{v}_i, \vec{v}_j )$

$\text{recomendaciones}(i) = \text{top}_k \left( \text{similaridad}(i, j) \right), \quad \text{para todo } j \neq i$


Donde:
- $vector_i$ es la representación de características de la canción objetivo.
- $similaridad(i, j)$ es la similitud calculada entre la canción $i$ y otra $j$.
- $top_k(...)$ selecciona los $k$ ítems más similares.

---

Esta solución aprovecha el procesamiento paralelo en la lectura de datos, y explora distintas métricas de similitud para evaluar qué tan eficientemente se pueden generar recomendaciones de calidad sobre un conjunto masivo de canciones.

---

## Experimentación

Se realizaron pruebas con muestras de **100**, **500**, **1000** y **todas las 28,372 canciones**, usando cada una de las métricas de similitud. Para cada combinación se registraron las recomendaciones generadas.

### Objetivo de las pruebas

El objetivo fue analizar cómo el tamaño de la muestra y la métrica de similitud influyen en la calidad y estabilidad de las recomendaciones generadas. Además, se buscó observar si las canciones recomendadas cambiaban drásticamente al aumentar el número de muestras.

### Evaluación de resultados

Dado que no se cuenta con un conjunto de validación con ratings explícitos, la evaluación fue principalmente cualitativa y comparativa. Se analizó si las recomendaciones parecían consistentes (en estilo o tema) con la canción objetivo, y si se mantenían similares entre diferentes tamaños de muestra.

### Recomendaciones generadas por tamaño de muestra

| Métrica        | Muestra | Canción objetivo | Recomendaciones (Top 5)                                                                 |
|----------------|---------|------------------|------------------------------------------------------------------------------------------|
| Coseno         | 100     | velvet light     | seven sisters, one more time, unchained melody, love., i’ve been in love before         |
| Coseno         | 500     | velvet light     | love., i’ve been in love before, one more time, seven sisters, unchained melody         |
| Coseno         | 1000    | velvet light     | love., seven sisters, i’ve been in love before, unchained melody, one more time         |
| Coseno         | 28372   | velvet light     | minstrel gigolo, thank you, love buzz, love me, poor boy                                |
| Euclidiana     | 100     | velvet light     | seven sisters, unchained melody, i’ve been in love before, one more time, love.         |
| Euclidiana     | 500     | velvet light     | unchained melody, one more time, love., seven sisters, i’ve been in love before         |
| Euclidiana     | 1000    | velvet light     | one more time, love., seven sisters, unchained melody, i’ve been in love before         |
| Pearson        | 100     | velvet light     | i’ve been in love before, unchained melody, one more time, love., seven sisters         |
| Pearson        | 500     | velvet light     | love., seven sisters, one more time, unchained melody, i’ve been in love before         |
| Pearson        | 1000    | velvet light     | unchained melody, seven sisters, one more time, love., i’ve been in love before         |
| Jaccard        | 100     | velvet light     | seven sisters, unchained melody, love., one more time, i’ve been in love before         |
| Jaccard        | 500     | velvet light     | unchained melody, love., one more time, i’ve been in love before, seven sisters         |
| Jaccard        | 1000    | velvet light     | love., unchained melody, one more time, i’ve been in love before, seven sisters         |

**Nota**: En las métricas distintas a coseno, se notó una mayor sensibilidad al tamaño de la muestra, lo que sugiere que el rendimiento y estabilidad de algunas métricas como Jaccard podrían verse afectadas por la escasez de datos binarios significativos en muestras pequeñas.

---

## Análisis de Resultados

El sistema fue evaluado utilizando cuatro métricas de similitud: Coseno, Euclidiana, Pearson y Jaccard, aplicadas sobre diferentes tamaños de muestra (100, 500, 1000 y 28,372 canciones). A continuación, se detallan las observaciones clave para cada métrica:

### 1. Similitud del Coseno

- Fue la más robusta y eficiente en todos los tamaños de muestra, destacándose especialmente en el caso de la muestra completa.
- Captura bien las relaciones angulares entre vectores, lo cual es útil cuando se trabaja con características numéricas escaladas como danceability o energy.
- Su rendimiento fue sobresaliente en términos de velocidad de cómputo y calidad de recomendaciones, manteniendo coherencia entre las canciones recomendadas incluso al aumentar la muestra.

Conclusión: Funcionó en escenarios con muchos datos y características continuas. Es computacionalmente barata gracias a implementaciones vectorizadas (como en sklearn).

---

### 2. Índice de Jaccard

- Requiere binarizar las características numéricas, lo que puede reducir la riqueza de información.
- La operación de comparar intersecciones y uniones entre vectores binarios es computacionalmente costosa, especialmente cuando se calcula contra todos los ítems.
- En las pruebas, la ejecución con los 28,372 ítems sin paralelismo superó por mucho el tiempo usado en otras métricas, lo que demuestra su baja escalabilidad.
- Es más adecuada cuando las características ya son binarias o categóricas.

Conclusión: Su uso en datos numéricos binarizados puede ser forzado y costoso. Parece ser recomendable en datasets pequeños o ya binarios.

---

### 3. Correlación de Pearson

- Mide la correlación lineal entre vectores, útil cuando se desea capturar la relación proporcional entre características.
- Requiere computar la correlación entre cada par de ítems, lo que lo hace más costoso que el coseno.
- A pesar de su fundamento estadístico sólido, puede ser sensible a valores extremos y a la falta de varianza en las columnas.

Conclusión: Es útil cuando se quiere entender relaciones estadísticas profundas entre características, pero su alto costo computacional exige optimización si se desea aplicar en conjuntos de datos grandes.

---

### 4. Distancia Euclidiana

- Calcula la distancia "geométrica" entre puntos en un espacio de características.
- Tiende a funcionar mejor cuando todas las variables están en la misma escala, lo cual no siempre se cumple si no se normaliza previamente.
- Es computacionalmente ligera, pero menos efectiva en capturar similitud semántica entre canciones cuando las características tienen diferentes rangos.

## Conclusión

El presente trabajo implementó un sistema de recomendación basado en contenido, en el cual los ítems (canciones) fueron representados como vectores en un espacio métrico, utilizando sus atributos numéricos. Para identificar ítems similares, se evaluaron múltiples métricas de similitud: **coseno**, **euclidiana**, **correlación de Pearson** y **Jaccard**.

Desde el punto de vista matemático, el problema se modeló como la búsqueda de los ítems $j$ más similares a un ítem objetivo $i$, calculando:

$\text{similaridad}(i, j) = \text{métrica}( \vec{x}_i, \vec{x}_j ), \quad \forall j \ne i$

donde $\vec{x}_i \in \mathbb{R}^n$ es el vector de características del ítem $i$, y la función de similitud depende de la métrica elegida:

- **Coseno**: mide el ángulo entre vectores, apropiado para datos numéricos normalizados.
- **Euclidiana**: mide la distancia real en el espacio, útil pero sensible a escalas distintas.
- **Pearson**: evalúa correlación estadística entre vectores; robusto a traslaciones y escalas.
- **Jaccard**: aplica sobre vectores binarizados, midiendo el grado de coincidencia entre conjuntos de características activas.

Además, se exploraron estrategias de procesamiento de datos masivos, utilizando:

- **Pandas** para lectura secuencial.
- **Multiprocessing** para paralelizar la lectura en múltiples chunks.
- **Dask** como alternativa escalable para computación distribuida con un enfoque tipo Map-Reduce.

### Análisis final:

- Se trabajó con tamaños de muestra de 100, 500, 1000 y 28,372 (total), lo cual permitió medir el desempeño de cada métrica tanto en tiempo computacional como en precisión de resultados.
- El cálculo de la matriz de similitud tiene una complejidad de:

$\mathcal{O}(n^2 \cdot d)$

donde $n$ es el número de ítems y $d$ la dimensionalidad del vector de características, lo que implica un crecimiento cuadrático con el tamaño de los datos. Este hecho motivó la optimización de los métodos, en especial para Pearson y Jaccard.

- Se observó que la métrica del coseno fue la más eficiente y escalable, gracias a su vectorización interna (usa álgebra lineal optimizada por NumPy y scikit-learn).
- **Jaccard** fue la más costosa, por su implementación binarizada y la necesidad de comparar todos los pares mediante operaciones lógicas, lo que implica una carga $\mathcal{O}(n^2 \cdot d)$ sin soporte vectorizado.
- **Pearson**, aunque estadísticamente interesante, fue ineficiente computacionalmente debido a su implementación secuencial (scipy.stats.pearsonr), pero podría acelerarse mediante **multiprocessing** o **Numba**.
- El enfoque **basado en contenido** demostró ser efectivo en contextos donde los ítems tienen descripciones numéricas bien definidas y comparables. No depende de las preferencias de usuarios previos, lo que lo hace ideal cuando no se cuenta con historial de interacciones.

En resumen, el proyecto integró conceptos fundamentales de álgebra lineal, estadística y computación paralela, permitiendo abordar un problema de recomendación a gran escala con rigor técnico y eficiencia computacional.

---

## Bibliografía

1. R. Baeza-Yates and B. Ribeiro-Neto, *Modern Information Retrieval: The Concepts and Technology behind Search*, 2nd ed. Addison-Wesley, 2011.

2. C. C. Aggarwal, *Recommender Systems: The Textbook*. Springer, 2016. doi: [10.1007/978-3-319-29659-3](https://doi.org/10.1007/978-3-319-29659-3)

3. S. Ghemawat, H. Gobioff, and S.-T. Leung, “The Google File System,” *ACM SIGOPS Operating Systems Review*, vol. 37, no. 5, pp. 29–43, 2003. doi: [10.1145/1165389.945450](https://doi.org/10.1145/1165389.945450)

4. M. Zaharia et al., “Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing,” in *Proc. 9th USENIX Conf. on Networked Systems Design and Implementation (NSDI)*, 2012. [https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)

5. W. Xu, J. Zhang, and W. Lu, “A Survey on Recommender Systems for Large-Scale Data: Challenges and Solutions,” *ACM Trans. Intell. Syst. Technol.*, vol. 11, no. 2, pp. 1–37, 2020. doi: [10.1145/3372346](https://doi.org/10.1145/3372346)

6. C. D. Manning, P. Raghavan, and H. Schütze, *Introduction to Information Retrieval*. Cambridge University Press, 2008. [https://nlp.stanford.edu/IR-book/](https://nlp.stanford.edu/IR-book/)

7. J. Porto, “Music mood classification dataset (Version 1),” *Mendeley Data*, 2020. [https://data.mendeley.com/datasets/3t9vbwxgr5/1](https://data.mendeley.com/datasets/3t9vbwxgr5/1)
