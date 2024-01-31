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

    def get_stratified_bootstrap_indices(bs):
        unique_strata, stratum_counts = np.unique(bs, return_counts=True)
        bs_index_list_stratified = []

        for idx_stratum_var, n_stratum_var in zip(unique_strata, stratum_counts):
            data_index_stratum = np.where(bs == idx_stratum_var)[0]
            bs_index_list_stratified.extend(np.random.choice(data_index_stratum, 
                                                             size=n_stratum_var,
                                                             replace=True))
        return np.array(bs_index_list_stratified)
        
    auc_scores = []
    indices = get_stratified_bootstrap_indices(y)
    
    for _ in range(n_bootstraps):
        bs_indices = np.random.choice(indices, size=len(indices), replace=True)
        y_true_bootstrap = y[bs_indices]
        y_scores_bootstrap = classifier.predict_proba(X[bs_indices])[:, 1]

        # Добавленная проверка на наличие обоих классов
        unique_classes = np.unique(y_true_bootstrap)
        if len(unique_classes) > 1:
            auc_scores.append(roc_auc_score(y_true_bootstrap, y_scores_bootstrap))

        # Проверка количества выборок в auc_scores
        if len(auc_scores) >= n_bootstraps:
            break

    # Проверка и генерация дополнительных выборок, если необходимо
    while len(auc_scores) < n_bootstraps:
        bs_indices = np.random.choice(indices, size=len(indices), replace=True)
        y_true_bootstrap = y[bs_indices]
        y_scores_bootstrap = classifier.predict_proba(X[bs_indices])[:, 1]

        unique_classes = np.unique(y_true_bootstrap)
        if len(unique_classes) > 1:
            auc_scores.append(roc_auc_score(y_true_bootstrap, y_scores_bootstrap))

    lower_percentile = (1 - conf) / 2 * 100
    upper_percentile = 100 - lower_percentile
    lcb = np.percentile(auc_scores, lower_percentile)
    ucb = np.percentile(auc_scores, upper_percentile)
    
    return (lcb, ucb)
