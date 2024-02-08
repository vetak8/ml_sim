import numpy as np

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
