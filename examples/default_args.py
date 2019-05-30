from tranquilizer import tranquilize


@tranquilize(method='get')
def defaults(a, s: str = 'a', x: int = None, l: list = None):
    '''handle None as default

    :param a: a
    :param b: a string'''

    if x:
        return s*x
    else:
        return l
