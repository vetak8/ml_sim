from typing import List
from functools import reduce

def sales_with_tax(sales: List[float],
                   tax_rate: float,
                   threshold: float = 300) -> List[float]:
    '''Returns filtered sales with tax'''
    return list(map(lambda x: x+x*tax_rate, filter(lambda x: x>threshold, sales)))

def sum_sales(sales: List[float], threshold: float = 300) -> float:
    '''Returns filtered sum of sales'''
    return float(reduce(lambda x, y: x+y, filter(lambda x: x>threshold, sales)))

def average_age(ages: List[int], threshold: int = 30) -> float:
    '''Returns avg age'''
    filtered = list(filter(lambda x: x> threshold, ages))
    n = len(filtered)
    mean = reduce(lambda x, y: x+y, filtered) / n
    return mean

def increased_prices(prices: List[float], 
                     increase_rate: int = 0.2,
                     threshold: float = 300) -> List[float]:
    '''Returns increased prices'''
    mapped_prices = list(map(lambda x: x+x*increase_rate, prices))
    return list(filter(lambda x: x>threshold, mapped_prices))

def weighted_sale_price(sales: List[float]) -> float:
    '''Returns weighed sales price'''
    count_sales = reduce(lambda x, y: x+y[1], sales, 0)
    total_sales = reduce(lambda x, y: x+y, map(lambda x: x[0]*x[1], sales))
    return total_sales / count_sales
    