from tranquilizer import tranquilize
from typing import List
from datetime import date

@tranquilize(method='get')
def dates(date: date):
    '''Extract components of a datetime string.

    :param date: parsible datetime'''

    response = {
            'month'  : date.month,
            'day'  : date.day,
            'year'  : date.year,
            'day_of_week'  : date.strftime('%A'),
    }

    return response

@tranquilize(method='post')
def vector_multiply(items: List[float], factor: int = 10):
    '''Multiply a list of floats by a factor

    :param items: list of floating point numbers
    :param factor: multiplicative factor (default 10)'''

    new_items = [i * factor for i in items]
    response = {
            'items': new_items
    }

    return response

