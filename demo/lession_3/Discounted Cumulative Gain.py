from typing import List
from functools import reduce
import numpy as np

def discounted_cumulative_gain(relevance: List[float], k: int, method: str = "standard") -> float:
    """Discounted Cumulative Gain

    Parameters
    ----------
    relevance : List[float]
        Video relevance list
    k : int
        Count relevance to compute
    method : str, optional
        Metric implementation method, takes the values:
        'standard' - adds weight to the denominator
        'industry' - adds weights to the numerator and denominator
        'raise ValueError' - for any value

    Returns
    -------
    score : float
        Metric score
    """
    relevance = relevance[:k]

    if method == 'standard':
        def dcg_standard_acc(acc, idx):
            return acc + relevance[idx] / np.log2(idx + 2)
        score = reduce(dcg_standard_acc, range(len(relevance)), 0)

    elif method == 'industry':
        def dcg_industry_acc(acc, idx):
            return acc + (2**relevance[idx] - 1) / np.log2(idx + 2)
        score = reduce(dcg_industry_acc, range(len(relevance)), 0)

    else:
        raise ValueError("Invalid method")

    return score
