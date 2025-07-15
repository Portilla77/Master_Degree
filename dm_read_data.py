import attr
import time
import psutil
import pandas as pd
import dask.dataframe as dd
import multiprocessing as mp
from typing import Tuple, Dict

def read_chunk(args: Tuple[str, Tuple[int, int]]) -> pd.DataFrame:
    path, chunk = args
    return pd.read_csv(path, skiprows=chunk[0], nrows=chunk[1], header=None)


@attr.s(auto_attribs=True, slots=True)
class DataReader:
    """D
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
        start = time.time()
        pd.read_csv(self.path)
        df = pd.read_csv(self.path)
        return self._run_metrics(start, "pandas", n_cores=1), df

    def read_with_dask(self) -> Tuple[Dict[str, float], pd.DataFrame]:
        start = time.time()
        ddf = dd.read_csv(self.path)
        df = ddf.compute(num_workers=self.n_cores)
        return self._run_metrics(start, "dask", n_cores=self.n_cores), df

    def read_with_multiprocessing(self) -> Tuple[Dict[str, float], pd.DataFrame]:
        start = time.time()

        total_rows = sum(1 for _ in open(self.path)) - 1
        chunks = [(self.path, (i, self.chunksize)) for i in range(1, total_rows, self.chunksize)]

        with mp.Pool(self.n_cores) as pool:
            dfs = pool.map(read_chunk, chunks)

        header = pd.read_csv(self.path, nrows=0).columns
        df = pd.concat(dfs, ignore_index=True)
        df.columns = header

        return self._run_metrics(start, "multiprocessing", n_cores=self.n_cores), df


lector = DataReader("Tercer_tetra/Datos_masivos/tcc_ceds_music.csv", chunksize=10000, n_cores=6)

# recursos_pd, df1 = lector.read_with_pandas()
# print("Pandas:", recursos_pd)

# recursos_mp, df2 = lector.read_with_multiprocessing()
# print("Multiprocessing:", recursos_mp)

# recursos_dask, df3 = lector.read_with_dask()
# #print("Dask:", recursos_dask)
# #print(df3.columns)
# content_data = df3["track_name"].unique()
# print(content_data)
