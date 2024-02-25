from typing import List

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
        Metric implementation method, takes the values
        'standard' - adds weight to the denominator
        'industry' - adds weights to the numerator and denominator
        'raise ValueError' - for any value

    Returns
    -------
    score : float
        Metric score
    """
    relevance = np.array(relevance[:k])
    logs = np.log2(np.arange(2, k+2))
    if method == 'industry':
        score = np.sum((2 ** relevance - 1) / logs)
    elif method == 'standard':
        score = np.sum(relevance / logs)
    else:
        raise ValueError("Invalid method provided. Please use 'standard' or 'industry'.")

    return score
