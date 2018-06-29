from tranquilizer import tranquilize, ParsedDateTime, TypedList

@tranquilize(method='post')
def convert(string: str, date: ParsedDateTime, items: TypedList[float], factor: int = 10):
    '''Let's convert strings to something useful'''

    new_items = [i * factor for i in items]

    response = {
            'string': string.upper(),
            'date'  : date.strftime('%c'),
            'items' : new_items
    }

    return response

