import numpy as np

def smape(y_true: np.array, y_pred: np.array, epsilon=1e-10) -> float:
    # Calculate absolute differences
    abs_diff = np.abs(y_true - y_pred)
    
    # Calculate denominator
    denominator = np.abs(y_true) + np.abs(y_pred)
    
    # Handle cases where both y_true and y_pred are zero
    zero_mask = np.isclose(y_true, 0) & np.isclose(y_pred, 0)
    denominator[zero_mask] = 1  # Set the denominator to a non-zero value
    
    # Calculate sMAPE
    result = np.mean(2 * abs_diff / denominator)
    
    return result
