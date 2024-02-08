import numpy as np

def split(X: np.ndarray, y: np.ndarray, feature: int) -> float:
    """Find the best split for a node (one feature)"""
    best_threshold = None
    best_metric = float('inf')

    for split_value in np.unique(X[:, feature]):
        left_indices = X[:, feature] <= split_value
        right_indices = X[:, feature] > split_value

        # Разделяем целевую переменную на две части
        left_y, right_y = y[left_indices], y[right_indices]

        # Оцениваем качество разбиения
        metric = weighted_mse(left_y, right_y)

        if metric < best_metric:
            best_metric = metric
            best_threshold = split_value
    return best_threshold

def mse(y: np.ndarray) -> float:
    """Compute the mean squared error of a vector."""
    squared_error = np.square(y - np.mean(y))
    return np.mean(squared_error)


def weighted_mse(y_left: np.ndarray, y_right: np.ndarray) -> float:
    """Compute the weighted mean squared error of two vectors."""
    n = len(y_left) + len(y_right)
    mse_left = mse(y_left)
    mse_right = mse(y_right)
    return (mse_left * len(y_left)) / n + (mse_right * len(y_right)) / n