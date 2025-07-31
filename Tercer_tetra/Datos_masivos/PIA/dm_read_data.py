import time
import multiprocessing as mp
from typing import Tuple, Dict
import attr
import psutil
import pandas as pd
import dask.dataframe as dd

def read_chunk(args: Tuple[str, Tuple[int, int]]) -> pd.DataFrame:
    """Lectura de CSV como  DataFrame.

    Args
    ----------
    args (tuple): tupla con dos elementos:
        - path : str
            Ruta al archivo CSV.
        - chunk : tuple of int
            Tupla con dos enteros (start_row, num_rows) indicando desde qué fila
            comenzar a leer (`skiprows`) y cuántas filas leer (`nrows`).

    Return:
        (pd.DataFrame):
                DataFrame que contiene las filas del archivo CSV sin encabezados.
    """
    path, chunk = args
    return pd.read_csv(path, skiprows=chunk[0], nrows=chunk[1], header=None)


@attr.s(auto_attribs=True, slots=True)
class DataReader:
    """ Clase para leer CSV utilizando métodos como (pandas, Dask, multiprocessing).
        Nos permite medir métricas de desempeño como tiempo, uso de CPU y memoria.

    Args
    path (str): Ruta del CSV..
    chunksize (int): optional: Número de filas por chunk al usar multiprocessing
                (por defecto 10,000).
    n_cores (int): Número de núcleos a usar en multiprocessing y Dask
                (por defecto todos los disponibles).
    """

    path: str
    chunksize: int = 10000
    n_cores: int = mp.cpu_count()

    def _run_metrics(
        self,
        start: float,
        metodo: str,
        cpu_using: float = None,
        memory_using: float = None,
        n_cores: int = 1
    ) -> Dict[str, float]:
        """Calcula y devuelve métricas de rendimiento para la lectura.

            Args
                start : float : Tiempo inicial en segundos.
                metodo (str) : Nombre del método de lectura utilizado.
                cpu_using (float) : optional; Porcentaje de CPU utilizada.
                memory_using (float) : optional: Porcentaje de memoria RAM utilizada
                n_cores (int): Número de núcleos utilizados.

            Return
                (Dict[str, float]): Diccionario métricas de ejecución"""
        end = time.time()
        cpu_using = cpu_using or psutil.cpu_percent(interval=1)
        memory_using = memory_using or psutil.virtual_memory().percent

        return {
            "método": metodo,
            "tiempo": round(end - start, 2),
            "cpu usada": cpu_using,
            "memoria usada": memory_using,
            "nucleos_disponibles": mp.cpu_count(),
            "nucleos_usados": n_cores
        }

    def read_with_pandas(self) -> Tuple[Dict[str, float], pd.DataFrame]:
        """Lee un CSV con pandas

        Return:
            (Tuple[Dict[str, float], pd.DataFrame]): Diccionario con métrica
            de rendimiento y el DataFrame resultante.
        """
        start = time.time()
        pd.read_csv(self.path)
        df = pd.read_csv(self.path)
        return self._run_metrics(start, "pandas", n_cores=1), df

    def read_with_dask(self) -> Tuple[Dict[str, float], pd.DataFrame]:
        """Lee un CSV con dask

        Return:
            (Tuple[Dict[str, float], pd.DataFrame]): Diccionario con métrica
            de rendimiento y el DataFrame resultante.
        """
        start = time.time()
        ddf = dd.read_csv(self.path)
        df = ddf.compute(num_workers=self.n_cores)
        return self._run_metrics(start, "dask", n_cores=self.n_cores), df

    def read_with_multiprocessing(self) -> Tuple[Dict[str, float], pd.DataFrame]:
        """Lee un CSV con chunks de multiprocessing

        Return:
            (Tuple[Dict[str, float], pd.DataFrame]): Diccionario con métrica
            de rendimiento y el DataFrame resultante.
        """
        start = time.time()

        total_rows = sum(1 for _ in open(self.path)) - 1
        chunks = [(self.path, (i, self.chunksize)) for i in range(1, total_rows, self.chunksize)]

        with mp.Pool(self.n_cores) as pool:
            dfs = pool.map(read_chunk, chunks)

        header = pd.read_csv(self.path, nrows=0).columns
        df = pd.concat(dfs, ignore_index=True)
        df.columns = header

        return self._run_metrics(start, "multiprocessing", n_cores=self.n_cores), df


lector = DataReader("External_data/tcc_ceds_music.csv", chunksize=10000, n_cores=6)

# recursos_pd, df1 = lector.read_with_pandas()
# print("Pandas:", recursos_pd)

# recursos_mp, df2 = lector.read_with_multiprocessing()
# print("Multiprocessing:", recursos_mp)

# recursos_dask, df3 = lector.read_with_dask()
# print("Dask:", recursos_dask)
# print(df3.shape)
#content_data = df3["track_name"].unique()
#print(content_data)
