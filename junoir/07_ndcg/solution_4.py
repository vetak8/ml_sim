from typing import List

import numpy as np


def normalized_dcg(relevance: List[float], k: int, method: str = "standard") -> float:
    """Normalized Discounted Cumulative Gain.

    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : int
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    sorted_relevance_k = np.sort(relevance)[::-1][:k]
    relevance = np.array(relevance[:k])
    logs = np.log2(np.arange(2, k+2))
    if method == 'industry':
        dcg = np.sum((2 ** relevance - 1) / logs)
        idcg = np.sum((2 ** sorted_relevance_k - 1) / logs)
    elif method == 'standard':
        dcg = np.sum(relevance / logs)
        idcg = np.sum(sorted_relevance_k / logs)
    else:
        raise ValueError("Invalid method provided. Please use 'standard' or 'industry'.")

    if idcg == 0:
        return 0
    else:
        ndcg = dcg / idcg

    return ndcg
    