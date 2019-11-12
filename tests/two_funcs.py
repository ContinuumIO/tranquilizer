from tranquilizer import tranquilize

@tranquilize()
def integer(i: int):
    '''Make an integer

    :param i: an integer
    :raises ValueError: not an integer'''
    return i

@tranquilize()
def order(cheese):
    '''I'd like to buy some cheese!

    :param cheese: What cheese would you like?'''
    return {'response':"I'm afraid we're fresh out of {}, Sir.".format(cheese)}

