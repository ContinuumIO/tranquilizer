from tranquilizer.decorator import publish

@publish(methods=['GET','POST'])
def order(cheese):
    '''I'd like to buy some cheese!

    :param cheese: What cheese would you like?'''
    return {'response':"I'm afraid we're fresh out of {}, Sir.".format(cheese)}

