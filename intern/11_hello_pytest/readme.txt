> Тесты для метрик
Ваш коллега написал код для подсчета нескольких бизнес метрик:

Общая прибыль
Маржинальность (отношение прибыли к выручке)
Средняя наценка (отношение прибыли к затратам)
Помогите ему написать для них юнит-тесты, используя Pytest.

Вот содержимое файла metrics.py:

from typing import List


def profit(revenue: List[float], costs: List[float]) -> float:
    return sum(revenue) - sum(costs)


def margin(revenue: List[float], costs: List[float]) -> float:
    return (sum(revenue) - sum(costs)) / sum(revenue)


def markup(revenue: List[float], costs: List[float]) -> float:
    return (sum(revenue) - sum(costs)) / sum(costs)
