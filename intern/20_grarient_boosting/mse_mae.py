from typing import Tuple
import numpy as np

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, np.ndarray]:
    """Mean squared error loss function and gradient."""
    error = y_pred - y_true
    loss = np.mean(error ** 2)
    grad = np.mean(error) 
    return loss, grad

def mae(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, np.ndarray]:
    """Mean absolute error loss function and gradient."""
    error = y_pred - y_true
    loss = np.mean(np.abs((error)))
    grad = np.sign((error))
    return loss, grad
    