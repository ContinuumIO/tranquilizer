from tranquil import tranquilize, ParsedDateTime, TypedList

def as_str(dt):
    return dt.strftime('%c')

@tranquilize('get')
def func1(a: str, b: ParsedDateTime, c: int = 10):
    '''test get'''
    return {'a':a, 'b':as_str(b), 'c':c}

@tranquilize('post')
def func2(d: ParsedDateTime, e: TypedList[float]):
    '''test post'''
    return {'d':d.isoformat(), 'e':e}
