import numpy as np

def ltv_error(y_true: np.array, y_pred: np.array) -> float:
    '''Функция вычисляет ошибку MSE
    
    Переменные:
    y_true: истинные значения
    y_pred: предсказанные значения

    Returns:
    float: значение ошибки MSE
    
    '''
    alpha = -1

    term1 = np.exp(alpha * (y_true - y_pred))
    term2 = alpha * (y_true - y_pred)
    error = np.mean((term1 - term2 - 1) / alpha**2)

    return error
    