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
