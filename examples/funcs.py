from tranquilizer import tranquilize, ParsedDateTime, TypedList

from factor import factor

def as_str(dt):
    return dt.strftime('%c')

@tranquilize('get')
def func1(a: str, b: ParsedDateTime, c: int = 10):
    '''test get'''
    return {'a':a, 'b':as_str(b), 'c':c * factor}

@tranquilize('post')
def func2(d: ParsedDateTime, e: TypedList[float]):
    '''test post'''
    return {'d':d, 'e':e}

