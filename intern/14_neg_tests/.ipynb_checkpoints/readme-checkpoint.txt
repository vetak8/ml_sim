Перед вами пример хорошей функции, вычисляющей конверсию в файле metrics.py

def ctr(clicks: int, views: int) -> float:
    """Click-through Rate."""

    # Check that the values are integers
    if not isinstance(clicks, int):
        raise TypeError("clicks must be an integer")

    if not isinstance(views, int):
        raise TypeError("views must be an integer")

    # Check that the values are positive
    if clicks < 0:
        raise ValueError("clicks must be positive")

    if views < 0:
        raise ValueError("views must be positive")

    # Check if clicks are greater than views
    if views < clicks:
        raise ValueError("clicks must be less than or equal to views")

    # Calculate the clickthrough rate
    if views:
        return clicks / views
    else:
        raise ZeroDivisionError("views must be greater than zero")


Она обрабатывает разные сценарии неправильных данных на входе и выплёвывает ошибки в зависимости от проблемы,
если где-то в коде мы неправильно используем данную функцию.

Допишите 5 негативных тестов на каждый из сценариев неправильных данных (1-й даём как шаблон):

Шаблон файла test_metrics.py (не изменяйте формат импорта и использования функции, 
это критически важно для проверяющей системы).

import metrics


def test_non_int_clicks():
    try:
        metrics.ctr(1.5, 2)
    except TypeError:
        pass
    else:
        raise AssertionError("Non int clicks not handled")


def test_non_int_views():
    pass


def test_non_positive_clicks():
    pass


def test_non_positive_views():
    pass


def test_clicks_greater_than_views():
    pass


def test_zero_views():
    pass
