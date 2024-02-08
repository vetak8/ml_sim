import pandas as pd
import numpy as np

def r_squared(y_true, y_pred):
    mean_y = np.mean(y_true)
    ss_total = np.sum((y_true - mean_y) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    r2 = 1 - (ss_residual / ss_total)
    return r2

def elasticity_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    # Группируем данные по SKU
    grouped = df.groupby('sku')

    # Для каждого SKU строим модель и рассчитываем эластичность
    for sku, group in grouped:
        # Преобразуем данные для удобства
        X = group['price']
        y = np.log(group['qty'] + 1)  # Преобразуем продажи к логарифмической шкале

        # Вычисляем коэффициенты альфа и бета
        beta, alpha = np.polyfit(X, y, 1)

        # Прогнозируем значения y
        y_pred = beta * X + alpha

        # Оцениваем эластичность
        r2 = r_squared(y, y_pred)

        results.append({'sku': sku, 'elasticity': r2})

    return pd.DataFrame(results)
