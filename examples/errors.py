from tranquilizer import tranquilize

@tranquilize()
def test(number: int):
    '''testing types and errors

    Let's see if we can find a reasonable way to express
    exceptions and return codes.

    :raise ValueError: when number less than zero
    :raises TypeError: just because
    :param number: a positive integer
    '''

    if number < -1:
        raise TypeError('just wrong')
    elif number < 0:
        raise ValueError('{} is not positive'.format(number))
    elif number == 0:
        number = 10 / number

    return {'response':"{} received".format(number)}
