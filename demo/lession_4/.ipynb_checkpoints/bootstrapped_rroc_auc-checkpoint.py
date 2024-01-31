from typing import Tuple
import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.metrics import roc_auc_score


def roc_auc_ci(
    classifier: ClassifierMixin,
    X: np.ndarray,
    y: np.ndarray,
    conf: float = 0.95,
    n_bootstraps: int = 10_000,
) -> Tuple[float, float]:
    '''
    Returns confidence bounds of ROC-AUC

    Input:
    classifier: classification model
    X: data
    y: target
    conf: confidence level
    n_bootstraps: count of bootstraps 

    Return:
    Tuple of confidence bounds
    '''

    auc_scores = np.zeros(n_bootstraps)

    def get_stratified_bootstrap_indices(bs):
        unique_strata, stratum_counts = np.unique(bs, return_counts=True)
        bs_index_list_stratified = np.concatenate([
            np.random.choice(np.where(bs == idx_stratum_var)[0], 
                             size=n_stratum_var,
                             replace=True)
            for idx_stratum_var, n_stratum_var in zip(unique_strata, stratum_counts)
        ])
        return bs_index_list_stratified
    predicts = classifier.predict_proba(X)[..., 1]
    
    for i in range(n_bootstraps):
        y = y.copy()
        indices = get_stratified_bootstrap_indices(y)
        y_true_bootstrap = y[indices]
        y_scores_bootstrap = predicts[indices]
        auc_scores[i] = roc_auc_score(y_true_bootstrap, y_scores_bootstrap)

    lower_percentile = (1 - conf) / 2 * 100
    upper_percentile = 100 - lower_percentile
    lcb, ucb = np.percentile(auc_scores, [lower_percentile, upper_percentile])
    
    return lcb, ucb
