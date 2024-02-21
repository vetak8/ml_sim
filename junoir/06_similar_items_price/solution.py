from typing import Dict, Tuple, List
import numpy as np
from scipy.spatial.distance import cosine
from itertools import combinations
from functools import  reduce


class SimilarItems: 
    @staticmethod
    def similarity(embeddings: Dict[int, np.ndarray]) -> Dict[Tuple[int, int], float]:
        """Calculate pairwise similarities between each item
        in embedding.

        Args:
            embeddings (Dict[int, np.ndarray]): Items embeddings.

        Returns:
            Dict[Tuple[int, int], float]:
            Keys are in form of (i, j) - combinations pairs of item_ids
            with i < j.
            Round each value to 8 decimal places.
        """
        combs = combinations(embeddings, 2)
        pair_sims = {(i, j): round(1 - cosine(embeddings[i], embeddings[j]), 8) for i, j in combs}
        return pair_sims

    @staticmethod
    def knn(
        sim: Dict[Tuple[int, int], float], top: int
    ) -> Dict[int, List[Tuple[int, float]]]:
        """Return closest neighbors for each item.
    
        Args:
            sim (Dict[Tuple[int, int], float]): <similarity> method output.
            top (int): Number of top neighbors to consider.
    
        Returns:
            Dict[int, List[Tuple[int, float]]]: Dict with top closest neighbors
            for each item.
        """
        knn_dict = {}
        for (item1, item2), similarity_score in sim.items():
            knn_dict.setdefault(item1, []).append((item2, similarity_score))
            knn_dict.setdefault(item2, []).append((item1, similarity_score))

        for item_id, neighbors in knn_dict.items():
            neighbors.sort(key=lambda x: x[1], reverse=True)
            knn_dict[item_id] = neighbors[:top]

        return knn_dict

    @staticmethod
    def knn_price(
        knn_dict: Dict[int, List[Tuple[int, float]]],
        prices: Dict[int, float],
    ) -> Dict[int, float]:
        """Calculate weighted average prices for each item.
        Weights should be positive numbers in [0, 2] interval.

        Args:
            knn_dict (Dict[int, List[Tuple[int, float]]]): <knn> method output.
            prices (Dict[int, float]): Price dict for each item.

        Returns:
            Dict[int, float]: New prices dict, rounded to 2 decimal places.
        """
        norm_knn_dict = {}
        for item_id, neighbors in knn_dict.items():
            # min_sim = min(neighbors, key=lambda x: x[1])[1] 
            # max_sim = max(neighbors, key=lambda x: x[1])[1] 
            sum_sim = reduce(lambda x, y: x+y[1] + 1, neighbors, 0)
            normed_neighbors = [(pair[0], (pair[1] + 1) / sum_sim) for pair in neighbors]
            norm_knn_dict[item_id] = normed_neighbors

        knn_price_dict = {}
        for item_id, neighbors in norm_knn_dict.items():
            weighed_price = round(sum([prices[item[0]] * item[1] for item in neighbors]), 2)
            knn_price_dict[item_id] = weighed_price

        return knn_price_dict

    @staticmethod
    def transform(
        embeddings: Dict[int, np.ndarray],
        prices: Dict[int, float],
        top: int,
    ) -> Dict[int, float]:
        """Transforming input embeddings into a dictionary
        with weighted average prices for each item.

        Args:
            embeddings (Dict[int, np.ndarray]): Items embeddings.
            prices (Dict[int, float]): Price dict for each item.
            top (int): Number of top neighbors to consider.

        Returns:
            Dict[int, float]: Dict with weighted average prices for each item.
        """
        pair_sims = SimilarItems.similarity(embeddings)
        knn_dict = SimilarItems.knn(pair_sims, top)
        knn_price_dict = SimilarItems.knn_price(knn_dict, prices)

        return knn_price_dict
        