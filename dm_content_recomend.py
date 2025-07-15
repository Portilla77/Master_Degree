import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from scipy.stats import pearsonr
from typing import List, Literal
from dm_read_data import DataReader


class BasedRecommender(DataReader):
    """Algoritmo de recomendación basado en contenido. Calcula similitudes
        entre elementos usando las siguientes métricas:
        - Coseno
        - Euclidiana
        - Correlación de Pearson
        - Jaccard
    """

    def _cosine_similarity(self, matrix: np.ndarray) -> np.ndarray:
        """D"""
        return cosine_similarity(matrix)

    def _euclidean_similarity(self, matrix: np.ndarray) -> np.ndarray:
        """D"""
        distances = euclidean_distances(matrix)
        return 1 / (1 + distances)

    def _pearson_similarity(self, matrix: np.ndarray) -> np.ndarray:
        """D"""
        n_items = matrix.shape[0]
        sim = np.zeros((n_items, n_items))
        for i in range(n_items):
            for j in range(n_items):
                if i != j:
                    sim[i, j], _ = pearsonr(matrix[i], matrix[j])
                else:
                    sim[i, j] = 1.0
        return sim

    def _jaccard_similarity(self, matrix: np.ndarray) -> np.ndarray:
        """D"""
        matrix_bin = (matrix > 0).astype(int)
        n_items = matrix_bin.shape[0]
        sim = np.zeros((n_items, n_items))
        for i in range(n_items):
            for j in range(n_items):
                intersection = np.logical_and(matrix_bin[i], matrix_bin[j]).sum()
                union = np.logical_or(matrix_bin[i], matrix_bin[j]).sum()
                sim[i, j] = intersection / union if union != 0 else 0.0
        return sim

    def recommend(
        self,
        df: pd.DataFrame,
        item_id_column: str,
        features: List[str],
        target_id,
        top_k: int = 5,
        metric: Literal['coseno', 'euclidean', 'pearson', 'jaccard'] = 'coseno'
    ) -> pd.DataFrame:
        """Recomendaciones para un ítem dado según una métrica de similitud."""
        df = df.dropna(subset=features + [item_id_column])
        matrix = df[features].to_numpy()

        if metric == 'coseno':
            similarity_matrix = self._cosine_similarity(matrix)
        elif metric == 'euclidean':
            similarity_matrix = self._euclidean_similarity(matrix)
        elif metric == 'pearson':
            similarity_matrix = self._pearson_similarity(matrix)
        elif metric == 'jaccard':
            similarity_matrix = self._jaccard_similarity(matrix)
        else:
            raise ValueError("Métrica no válida. Usa 'coseno', 'euclidean', 'pearson' o 'jaccard'.")

        target_index = df.index[df[item_id_column] == target_id].tolist()
        if not target_index:
            raise ValueError(f"ID {target_id} no encontrado en la columna {item_id_column}.")
        target_index = target_index[0]

        sim_scores = similarity_matrix[target_index]
        top_indices = np.argsort(sim_scores)[::-1][1:top_k + 1]

        return df.iloc[top_indices][[item_id_column] + features].copy()


recommender = BasedRecommender("Tercer_tetra/Datos_masivos/tcc_ceds_music.csv", chunksize=10000, n_cores=6)

_, df = recommender.read_with_dask()
df = df.sample(10, random_state=42).reset_index(drop=True)

target_id = df["track_name"].iloc[0]
print(target_id)

recs = recommender.recommend(
    df=df,
    item_id_column='track_name',
    features=[
        'danceability', 'energy', 'len', 'romantic',
        'violence', 'music', 'movement/places'
    ],
    target_id=target_id,
    top_k=5,
    metric='pearson'
    #metric = 'euclidean'
    #metric = 'coseno'
    #metric= 'jaccard'
)
print("Recomendaciones:")
print(recs)