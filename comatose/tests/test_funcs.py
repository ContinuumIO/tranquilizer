from comatose import publish, ParsedDateTime

def as_iso(dt):
    return dt.strftime('%c')

@publish(['get'])
def func1(a: str, b: ParsedDateTime, c: int = 10):
    return {'a':a, 'b':as_iso(b), 'c':c}

@publish(['get'])
def func2(d, e):
    return {'d':d, 'e':e}
