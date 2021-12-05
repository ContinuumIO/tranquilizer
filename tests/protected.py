from tranquilizer import tranquilize

@tranquilize(protected=True)
def order(cheese):
    '''I'd like to buy some cheese!

    :param cheese: What cheese would you like?'''
    return {'response':"I'm afraid we're fresh out of {}, Sir.".format(cheese)}


@tranquilize()
def unspecified():
    return "Unspecified authorization"

@tranquilize(protected=False)
def no_auth():
    return "Disabled authorization"