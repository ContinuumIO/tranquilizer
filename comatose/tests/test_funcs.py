from comatose import publish, ParsedDateTime, TypedList

def as_iso(dt):
    return dt.strftime('%c')

@publish('get')
def func1(a: str, b: ParsedDateTime, c: int = 10):
    '''test data types'''
    return {'a':a, 'b':as_iso(b), 'c':c}

@publish('post')
def func2(d: ParsedDateTime, e: TypedList[float]):
    '''test post'''
    return {'d':d, 'e':e}
