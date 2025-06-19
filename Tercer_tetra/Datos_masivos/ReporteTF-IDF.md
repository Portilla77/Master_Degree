<h1 align="center">Cálculo de TF-IDF usando MapReduce</h1>

<p align="center"><strong>Nombre:</strong> Jorge Ramón Flores Portilla</p>
<p align="center"><strong>Matrícula:</strong> 1550162</p>
<p align="center"><strong>Maestro:</strong> Christian Aguilar Fuster</p>
<p align="center"><strong>Materia:</strong> Datos Masivos</p>


## Introducción

El crecimiento exponencial de los datos textuales ha hecho necesario desarrollar métodos eficientes para su análisis. Uno de los enfoques más comunes para representar documentos en tareas de procesamiento de lenguaje natural (**NLP**) es el cálculo del TF-IDF (**Term Frequency – Inverse Document Frequency**), el cual permite ponderar la importancia de cada palabra en un documento considerando su frecuencia en el conjunto completo de documentos.

Sin embargo, cuando la cantidad de archivos de texto es elevada, el procesamiento secuencial puede volverse lento e ineficiente. Para abordar este problema, en esta tarea se implementa una solución basada en el paradigma **MapReduce** con la ayuda del módulo multiprocessing en Python. Esta estrategia permite distribuir el cálculo del TF entre múltiples núcleos de CPU y acelerar el procesamiento de grandes volúmenes de datos.

El trabajo incluye la lectura controlada de archivos .txt desde un archivo .zip, la extracción de palabras clave, el cómputo del TF-IDF para cada documento, y la generación de resultados en formato .json, con un enfoque flexible y adaptable al rendimiento del sistema disponible.

## Planteamiento

El análisis de grandes volúmenes de texto mediante la métrica TF-IDF puede ser intensivo en recursos, especialmente cuando se manejan miles de archivos. Ejecutar este tipo de procesamiento de forma secuencial puede no ser viable en términos de tiempo, por lo que resulta necesario explorar enfoques paralelos como MapReduce en Python.

Antes de aplicar la solución paralela, se evaluaron los recursos del equipo utilizando las bibliotecas psutil y multiprocessing. El objetivo fue conocer las capacidades reales del entorno para asignar de forma óptima los procesos de trabajo. Los resultados de esta evaluación fueron los siguientes:

```json
{
  "Cores disponibles": 12,
  "Frecuencia CPU (MHz)": 0.0,
  "Memoria RAM total (GB)": 7.45,
  "Memoria RAM disponible (GB)": 6.82,
  "Uso actual de CPU (%)": 0.0,
  "Uso actual de RAM (%)": 8.4
}
```
Estos valores sugieren que el sistema cuenta con una cantidad considerable de núcleos y memoria disponible, lo cual es ideal para realizar procesamiento como el ya mencionado. Con esta información, se determinó un punto de partida para experimentar con distintos niveles de paralelismo (num_workers) y observar el impacto en el tiempo total de ejecución al procesar $n$ documentos.

## Solución propuesta

La solución consiste en implementar un enfoque MapReduce en Python para calcular la métrica **TF-IDF** sobre una colección de archivos .txt, aprovechando la biblioteca multiprocessing para distribuir el procesamiento entre varios núcleos del procesador.

El procedimiento general consta de los siguientes pasos:

1. **Extracción de archivos**: A partir de un archivo ZIP (DocumentosTarea2.zip), se extraen los primeros $N$ archivos .txt desde una subcarpeta específica (Docs1, Docs2, etc.) hacia una ruta local (documentos_extraidos).

2. **Cálculo del TF (Term Frequency)**:
   - Para cada documento, se contabilizan las palabras y se normaliza la frecuencia relativa.
   - Esta operación se distribuye en paralelo entre *num_workers* procesos usando un `Pool`.
#### 1. **TF (Term Frequency)**

La **frecuencia de término (TF)** mide la proporción de veces que una palabra aparece en un documento respecto al total de palabras en ese documento. Su fórmula es:

$TF(t, d) = \frac{f_{t,d}}{ \sum_{w \in d} f_{w,d}}$

- $t$: término (palabra)
- $d$: documento
- $f_{t,d}$: número de veces que el término $t$ aparece en el documento $d$
- El denominador representa el total de palabras en el documento $d$

#### 2. **IDF (Inverse Document Frequency)**

La **frecuencia inversa de documentos (IDF)** mide qué tan común o rara es una palabra en toda la colección de documentos:

$IDF(t) = \log\left( \frac{N}{1 + df(t)} \right)$

- $N$: número total de documentos
- $df(t)$: número de documentos donde aparece el término $t$
- Se suma $1$ en el denominador para evitar división entre cero

#### 3. **TF-IDF**

El valor final del término en el documento se obtiene multiplicando ambas métricas:

$TF\text{-}IDF(t, d) = [TF(t, d)][IDF(t)]$

Enseguida se muestra el código realizado para dicha ejecución:

```python
import json
import time
import psutil
import multiprocessing
import re
import math
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from multiprocessing import Pool

ZIP_PATH = Path("test/resources/DocumentosTarea2.zip").resolve()
EXTRACT_PATH = Path("test/resources/documentos_extraidos").resolve()
FOLDER_NAME = "Docs1"
NUM_DOCS = 2000
NUM_WORKERS = 5

def extract_first_txt_files(zip_path: Path, extract_path: Path, max_files: int = NUM_DOCS) -> None:
    """
    Extrae los primeros archivos .txt desde un archivo .zip hacia un directorio destino.

    Args:
        zip_path (Path): Ruta al archivo ZIP.
        extract_path (Path): Carpeta donde se extraerán los archivos.
        max_files (int): Número máximo de archivos a extraer.
    """
    extract_path.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, 'r') as zip_ref:
        txt_files = [
            f for f in zip_ref.namelist()
            if f.startswith(f"{FOLDER_NAME}/") and f.endswith('.txt')
        ]
        for f in txt_files[:max_files]:
            zip_ref.extract(f, extract_path)
    print(f"Extracción finalizada: {min(max_files, len(txt_files))} archivos .txt.")

def map_tf(file_path: Path) -> tuple[str, dict[str, float]]:
    """
    Calcula la frecuencia relativa de términos (TF) en un archivo .txt.

    Args:
        file_path (Path): Ruta al archivo de texto.

    Return:
        tuple: Nombre del archivo y diccionario con TF por palabra.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()
        words = re.findall(r'\b\w+\b', text)
        total_words = len(words)
        if total_words == 0:
            return Path(file_path).name, {}
        word_counts = Counter(words)
        tf = {word: count / total_words for word, count in word_counts.items()}
        return Path(file_path).name, tf
    except Exception as e:
        print(f"Error al extraer el archivo: {file_path}: {e}")
        return Path(file_path).name, {}

def map_all_documents(folder_name: str, num_documents: int = NUM_DOCS, num_workers: int = 4) -> dict[str, dict[str, float]]:
    """
    Aplica `map_tf` a varios documentos usando procesamiento paralelo.

    Args:
        folder_name (str): Carpeta con los archivos .txt.
        num_documents (int): Número de archivos a procesar.
        num_workers (int): Núcleos de CPU para procesamiento en paralelo.

    Return:
        dict: Diccionario con TF por documento.
    """
    folder_path = EXTRACT_PATH / folder_name
    txt_files = sorted(folder_path.glob("*.txt"))[:num_documents]
    print(f"Procesando {len(txt_files)} documentos de '{folder_name}' con {num_workers} núcleos...")

    with Pool(processes=num_workers) as pool:
        results = pool.map(map_tf, txt_files)

    tf_por_doc = {doc_name: tf for doc_name, tf in results if tf}
    print(f"Procesamiento completo. Documentos válidos: {len(tf_por_doc)}")
    return tf_por_doc

def compute_idf(tf_docs: dict[str, dict[str, float]]) -> dict[str, float]:
    """
    Calcula el Inverse Document Frequency (IDF) para todas las palabras.

    Args:
        tf_docs (dict): Diccionario de TFs por documento.

    Return:
        dict: Diccionario con valores IDF por palabra.
    """
    N = len(tf_docs)
    df_counts = Counter()
    for tf in tf_docs.values():
        for word in tf.keys():
            df_counts[word] += 1
    idf = {word: math.log(N / (1 + df)) for word, df in df_counts.items()}
    return idf

def compute_tfidf(tf_docs: dict[str, dict[str, float]],
     idf_dict: dict[str, float]) -> dict[str, dict[str, float]]:
    """
    Calcula el TF-IDF combinando el TF de cada palabra con su IDF.

    Args:
        tf_docs (dict): Diccionario de TFs por documento.
        idf_dict (dict): Diccionario con valores IDF por palabra.

    Return:
        dict: Diccionario con TF-IDF por documento.
    """
    tfidf_docs = {}
    for doc_name, tf in tf_docs.items():
        tfidf = {word: tf_val * idf_dict[word] for word, tf_val in tf.items()}
        tfidf_docs[doc_name] = tfidf
    return tfidf_docs

if __name__ == "__main__":
    start = time.time()

    extract_first_txt_files(ZIP_PATH, EXTRACT_PATH, max_files=NUM_DOCS)
    tf_docs = map_all_documents(
        folder_name=FOLDER_NAME,
        num_documents=NUM_DOCS,
        num_workers=NUM_WORKERS
    )
    idf_dict = compute_idf(tf_docs)
    tfidf_docs = compute_tfidf(tf_docs, idf_dict)

    output_path = Path("tfidf_resultado.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tfidf_docs, f, indent=2, ensure_ascii=False)

    end = time.time()
    print(f"\nTF-IDF calculado para {len(tfidf_docs)} documentos.")
    print(f"Archivo guardado: {output_path.resolve()}")
    print(f"Tiempo total de ejecución: {end - start:.2f} segundos")

```
5. **Exportación de resultados**:
   - Los resultados finales (una estructura {documento: {palabra: tfidf}}) se almacenan en un archivo JSON llamado tfidf_resultado.json.

Este flujo fue encapsulado en un único script, optimizado para permitir la configuración dinámica del número de documentos y núcleos de procesamiento. De esta forma, se puede analizar el impacto que tiene el paralelismo sobre el tiempo total de ejecución de la tarea.

### Tabla de Tiempos de Ejecución según Núcleos Utilizados

| Núcleos (workers) | Documentos Procesados | Tiempo Total (segundos) |
|-------------------|------------------------|--------------------------|
| 1                 | 1000                   | 18.76                    |
| 2                 | 1000                   | 10.15                    |
| 3                 | 1000                   | 8.93                     |
| 4                 | 1000                   | 7.12                     |
| 5                 | 1000                   | 6.45                     |
| 1                 | 2000                   | 19.64                    |
| 2                 | 2000                   | 13.93                    |
| 3                 | 2000                   | 13.39                    |
| 4                 | 2000                   | 13.10                    |
| 5                 | 2000                   | 12.37                    |

## Análisis de Resultados

Los experimentos muestran una clara mejora en los tiempos de ejecución al incrementar el número de núcleos utilizados para el procesamiento paralelo de archivos .txt. Esta mejora es particularmente notable al pasar de **1 a 2 núcleos**, donde el tiempo para 1000 documentos se reduce de **18.76** a **10.15 segundos**, una mejora del **45.9%** aproximadamente.

Sin embargo, a medida que se incrementa el número de núcleos más allá de 3, los beneficios marginales comienzan a disminuir. Por ejemplo:

- De **3 a 4 núcleos**: el tiempo disminuye de **8.93** a **7.12 segundos**.
- De **4 a 5 núcleos**: apenas baja a **6.45 segundos**.

Este comportamiento es consistente con el principio de *rendimientos decrecientes* en la computación paralela, donde la sobrecarga de coordinar múltiples procesos limita la escalabilidad lineal.

Para **2000 documentos**, la tendencia se mantiene:

- De **1 a 2 núcleos**: mejora de **19.64 a 13.93 segundos**.
- De **3 a 5 núcleos**: los tiempos convergen alrededor de **13 segundos**.

### Conclusión

Los resultados obtenidos permiten identificar un patrón común en sistemas de procesamiento paralelo: la existencia de **rendimientos decrecientes**. Este principio, derivado de la teoría económica y ampliamente aplicado en computación, establece que al aumentar los recursos (como núcleos de CPU), las mejoras en rendimiento no crecen de forma proporcional una vez alcanzado cierto umbral.

Parte de la tarea, si bien consistia en realizar una experimentación de paramétros en un MapReduce,los siguientes conceptos forman parte de lo investigado para poder entender más a fondo lo anterior.

- **Overhead de sincronización**: cada nuevo proceso que se añade debe ser gestionado, coordinado y sincronizado con los demás. Esto implica costos computacionales extra, conocidos como *overhead*.
- **I/O Bound**: el cuello de botella puede estar en la velocidad de lectura/escritura del disco duro al procesar muchos archivos simultáneamente. Es decir, aunque se tengan más núcleos, el tiempo de acceso al disco puede no ser suficientemente rápido.
- **Limitaciones del entorno de ejecución**: en algunos sistemas operativos (como WSL2 o versiones de Windows), la gestión de procesos en paralelo puede no ser tan eficiente como en entornos Linux nativos, lo que limita el aprovechamiento real de todos los núcleos disponibles.

Por tanto, desde el punto de vista práctico y teórico, usar entre **3 y 5 núcleos** representa un **equilibrio óptimo** entre paralelismo, eficiencia y control de nuestros recursos computacionales disponibles.

Este tipo de análisis es consistente con el concepto de **speedup** en computación paralela, donde:

$\text{Speedup} = \frac{T_1}{T_p}$

Donde:
- $T_1$: Tiempo con 1 procesador.
- $T_p$: Tiempo con $p$ procesadores.

Y está limitado por la **ley de Amdahl**, que establece que la ganancia máxima está acotada por la parte del código que puede paralelizarse.

Finalmente, esta experimentación validó la lógica del modelo TF-IDF, aplicado mediante una estrategia MapReduce sobre un conjunto real de documentos, y permitió identificar, mediante observación empírica, que el rendimiento del sistema se estabiliza a partir de cierto número de núcleos. Con ello, se logró una implementación funcional y eficiente que cumple con los requerimientos del proyecto.

