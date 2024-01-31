from typing import Tuple
from sklearn.metrics import precision_recall_curve, auc, roc_curve
import matplotlib.pyplot as plt
import numpy as np


def compute_precision_recall_threshold(y_true, y_prob, min_precision):
    precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
    precision = precision[:-1]
    recall = recall[:-1]
    return precision, recall, thresholds


def pr_threshold(y_true, y_prob, min_precision):
    precision, recall, thresholds = compute_precision_recall_threshold(y_true, y_prob, min_precision)
    valid_thresholds = thresholds[precision >= min_precision]
    
    if len(valid_thresholds) > 0:
        max_recall_index = np.argmax(recall[precision >= min_precision])
        threshold_proba = valid_thresholds[max_recall_index]
        max_recall = recall[precision >= min_precision][max_recall_index]
    else:
        threshold_proba = max_recall = 0.0
    
    return threshold_proba, max_recall


# def sr_threshold(
#     y_true: np.ndarray,
#     y_prob: np.ndarray,
#     min_specificity: float,
# ) -> Tuple[float, float]:
#     """Returns threshold and recall (from Specificity-Recall Curve) using optimization"""
#     fpr, recall, thresholds = roc_curve(y_true, y_prob)

#     # Calculate specificity in a vectorized way
#     specificity = 1 - fpr
#     valid_thresholds = thresholds[specificity >= min_specificity]


#     if len(valid_thresholds) > 0:
#         max_recall_index = np.argmax(recall[specificity >= min_specificity])
#         threshold_proba = valid_thresholds[max_recall_index]
#         max_recall = recall[specificity >= min_specificity][max_recall_index]
#     else:
#         threshold_proba = max_recall = 0.0
    
#     return threshold_proba, max_recall
#     return threshold_proba, max_recall

def sr_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    min_specificity: float,
) -> Tuple[float, float]:
    """Returns threshold and recall (from Specificity-Recall Curve) using optimization"""
    fpr, recall, thresholds = roc_curve(y_true, y_prob)

    # Calculate specificity in a vectorized way
    specificity = 1 - fpr
    valid_indices = np.where(specificity >= min_specificity)

    max_recall_index = np.argmax(recall[valid_indices])
    max_recall = recall[valid_indices][max_recall_index]
    threshold_proba = thresholds[valid_indices][max_recall_index]
    
    threshold_proba = max(0, min(1, threshold_proba))
    return threshold_proba, max_recall



def bootstrap_auc(y_true, y_prob, conf, n_bootstrap):
    np.random.seed(42)
    auc_values = []
    
    for _ in range(n_bootstrap):
        indices = np.random.choice(len(y_true), len(y_true), replace=True)
        y_true_bootstrap = y_true[indices]
        y_prob_bootstrap = y_prob[indices]
        precision, recall, _ = precision_recall_curve(y_true_bootstrap, y_prob_bootstrap)
        auc_values.append(auc(recall, precision))
    
    auc_values.sort()
    lower_percentile, upper_percentile = np.percentile(auc_values, [(1 - conf) / 2 * 100, 100 - (1 - conf) / 2 * 100])
    return lower_percentile, upper_percentile


def pr_curve(y_true, y_prob, conf=0.95, n_bootstrap=10_000):
    precision, recall, thresholds = compute_precision_recall_threshold(y_true, y_prob, conf)
    precision_lcb, precision_ucb = bootstrap_auc(y_true, y_prob, conf, n_bootstrap)
    return recall, precision, precision_lcb, precision_ucb


def sr_curve(y_true, y_prob, conf=0.95, n_bootstrap=10_000):
    precision, recall, thresholds = compute_precision_recall_threshold(y_true, y_prob, conf)
    specificity = 1 - np.array([np.sum((y_prob >= threshold) & (y_true == 0)) / np.sum(y_true == 0) for threshold in thresholds])
    specificity_lcb, specificity_ucb = bootstrap_auc(y_true, 1 - y_prob, conf, n_bootstrap)
    return recall, specificity, specificity_lcb, specificity_ucb


# Пример использования:
# y_true = ...
# y_prob = ...
# min_precision = ...
# min_specificity = ...
# conf = ...
# n_bootstrap = ...
# pr_threshold_result = pr_threshold(y_true, y_prob, min_precision)
# sr_threshold_result = sr_threshold(y_true, y_prob, min_specificity)
# pr_curve_result = pr_curve(y_true, y_prob, conf, n_bootstrap)
# sr_curve_result = sr_curve(y_true, y_prob, conf, n_bootstrap)
