import numpy as np

def smape(y_true: np.array, y_pred: np.array) -> float:
    '''Calculate sMAPE'''
    abs_diff = np.abs(y_true - y_pred)
    # Вычисляем знаменатель
    denominator = np.abs(y_true) + np.abs(y_pred)
    # Для случая, когда и y_pred и y_true близки к нулю
    zero_mask = np.isclose(y_true, 0) & np.isclose(y_pred, 0)
    denominator[zero_mask] = 1  #Установим в ненулувое значние
    # Calculate sMAPE
    result = np.mean(2 * abs_diff / denominator)
    
    return result