from tranquilizer import tranquilize
from typing import List
from datetime import date

@tranquilize(method='get')
def dates(date: date):
    '''Extract components of a date string.'''

    response = {
            'month'  : date.month,
            'day'  : date.day,
            'year'  : date.year,
            'day_of_week'  : date.strftime('%A'),
    }

    return response

@tranquilize(method='post')
def vector_multiply(items: List[float], factor: int = 10):
    '''Multiply a list of floats by a factor'''

    new_items = [i * factor for i in items]
    response = {
            'items': new_items
    }

    return response

