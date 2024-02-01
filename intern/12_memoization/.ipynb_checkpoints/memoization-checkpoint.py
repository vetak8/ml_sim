from typing import Callable
import json

def memoize(func: Callable):
    '''
    Memoize function
    Ввод:
    
    func: функция которую кэшируют
    args, kwargs: входные данные

    Выход:
    Если функция выполнялась с такими переменными, выводится кэшировавнный результат,
    иначе функция выполняется, кэшируется и выводится результат
    '''
    cache = {}
    def wrapped(*args, **kwargs):
        key = (json.dumps(args), json.dumps(kwargs))
        if key not in cache:
            result = func(*args, **kwargs)
            cache[key] = result
        return cache[key]
        
    return wrapped
