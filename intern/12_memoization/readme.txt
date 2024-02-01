Задание: @memoize
Ваша задача написать декоратор @memoize, который кэширует, 
какие аргументы были поданы на вход функции и что она вернула. 
Декоратор должен работать с любыми функциями :)

from typing import Callable


def memoize(func: Callable) -> Callable:
    """Memoize function"""
    ...