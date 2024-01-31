import numpy as np

def turnover_error(y_true: np.array, y_pred: np.array) -> float:
    """
    Рассчитывает ошибку RSMLE (Root Squared Mean Logarithmic Error).

    Parameters:
    - y_true (numpy.ndarray): Истинные значения.
    - y_pred (numpy.ndarray): Предсказанные значения.

    Returns:
    - float: Значение ошибки RSMLE.
    """
    n = len(y_true)
    error = np.sqrt(
        np.sum((np.log(y_true) - np.log(y_pred))**2) / n
    )
    return error
