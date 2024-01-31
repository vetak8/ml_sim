from typing import List
from functools import reduce
import numpy as np

def avg_ndcg(list_relevances: List[List[float]], k: int, method: str = 'standard') -> float:
    """Average nDCG

    Parameters
    ----------
    list_relevances : `List[List[float]]`
        Video relevance matrix for various queries
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values ​​\
        `standard` - adds weight to the denominator\
        `industry` - adds weights to the numerator and denominator\
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    cum_score = 0
    n = len(list_relevances)
    for relevance in list_relevances:
        relevance_sorted = sorted(relevance, reverse=True)[:k]
        relevance = relevance[:k]
        if method == 'standard':
            def dcg_standard_acc(acc, idx):

                return acc + relevance[idx] / np.log2(idx + 2)
            dcg = reduce(dcg_standard_acc, range(len(relevance)), 0)
            relevance = relevance_sorted
            idcg = reduce(dcg_standard_acc, range(len(relevance)), 0)
        elif method == 'industry':
            def dcg_industry_acc(acc, idx):

                return acc + (2**relevance[idx] - 1) / np.log2(idx + 2)
            dcg = reduce(dcg_industry_acc, range(len(relevance)), 0)
            relevance = relevance_sorted
            idcg = reduce(dcg_industry_acc, range(len(relevance)), 0)
        else:
            raise ValueError
        score = dcg / idcg
        cum_score += score
    result = cum_score / n
    
    return result

