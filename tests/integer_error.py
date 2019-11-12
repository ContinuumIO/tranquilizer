from tranquilizer import tranquilize

@tranquilize()
def integer(i: int):
    '''Make an integer

    :param i: an integer
    :raises ValueError: not an integer'''
    return i

