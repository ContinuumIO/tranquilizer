from tranquilizer import tranquilize

@tranquilize(requires_authentication=True)
def order(cheese):
    '''I'd like to buy some cheese!

    :param cheese: What cheese would you like?'''
    return {'response':"I'm afraid we're fresh out of {}, Sir.".format(cheese)}


@tranquilize()
def unspecified():
    return "Unspecified authorization"

@tranquilize(requires_authentication=False)
def no_auth():
    return "Disabled authorization"