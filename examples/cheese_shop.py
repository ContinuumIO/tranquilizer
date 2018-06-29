from tranquilizer import tranquilize

@tranquilize()
def order(cheese):
    '''I'd like to buy some cheese!

    :param cheese: What cheese would you like?'''
    return {'response':"I'm afraid we're fresh out of {}, Sir.".format(cheese)}

