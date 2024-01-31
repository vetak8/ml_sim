def sr_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    min_specificity: float,
) -> Tuple[float, float]:
    """Returns threshold and recall (from Specificity-Recall Curve) using optimization"""
    fpr, recall, thresholds = roc_curve(y_true, y_prob)

    specificity = 1 - fpr
    valid_indices = np.where(specificity >= min_specificity)

    max_recall_index = np.argmax(recall[valid_indices])
    max_recall = recall[max_recall_index]
    threshold_proba = thresholds[max_recall_index]
    
    threshold_proba = max(0, min(1, threshold_proba))
    return threshold_proba, max_recall
