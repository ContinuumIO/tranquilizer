from inspect import signature
import re

PARAM_REGEX = re.compile(r":param (?P<name>[\*\w]+): (?P<doc>.*?)"
                         r"(?:(?=:param)|(?=:return)|(?=:raises)|\Z)", re.S)
RAISE_REGEX = re.compile(r":raise[s]? (?P<name>[\*\w]+): (?P<doc>.*?)"
                         r"(?:(?=:param)|(?=:return)|(?=:raise[s]?)|\Z)", re.S)

def _prepare_arg(arg):
    '''Return a keyword arg spec (dict)'''
    _arg = {
        "name": arg.name,
    }

    if arg.annotation != arg.empty:
        try:
            name = str(arg.annotation.__name__)
        except AttributeError:
            name = str(arg.annotation._name)
        _arg["type"] = name
        _arg["annotation"] = arg.annotation

    if arg.empty is not arg.default:
        _arg['default'] = arg.default

    return _arg

def _prepare_arg_docs(docstring):
    args = re.findall(PARAM_REGEX, docstring)
    remainder = re.sub(PARAM_REGEX, '', docstring)

    if not args:
        return {}, remainder

    docs = {}
    for arg in args:
        docs[arg[0]] = arg[1].strip()

    return docs, remainder

def _prepare_error_docs(docstring):
    errors = re.findall(RAISE_REGEX, docstring)
    remainder = re.sub(RAISE_REGEX, '', docstring)

    if errors:
        messages = '\n'.join('{}:{}'.format(e,msg.strip()) for e,msg in errors)
        responses = {500:messages}
        return responses, remainder

    return {}, remainder

def _prepare(fn):
    """Inspects a function and return a function spec dict

    Output:
        dict containing the following info about f:

        - name: str -> name of the function
        - docstring: str -> docstring of the function
        - args: dict -> dict that holds info about the function arguments.
                    Keys: name of the argument
                    Values: Dict containing the following about the argument:
                        - name: str -> name of the argument
                        - default: any (optional) -> default value
                        - type: any (optional) -> type annotation (if available)

    """
    sig = signature(fn)
    _args = {}
    for k, v in sig.parameters.items():
        _args[k] = _prepare_arg(v)

    if fn.__doc__:
        param_docs, docstring = _prepare_arg_docs(fn.__doc__)
        error_docs, docstring = _prepare_error_docs(docstring)
    else:
        param_docs = {}
        error_docs = {}
        docstring = ''

    spec = {
        'name': fn.__name__,
        'docstring': docstring,
        'args': _args,
        'param_docs': param_docs,
        'error_docs': error_docs
    }

    return spec


def tranquilize(method='get', requires_authentication=None):
    """Decorator function that gets a function wraps it in order to
    append a function spec (see prepare function) and autocast args/kws
    to match types.

    Parameters
    ----------
    :param method: str, HTTP method for this function. (default: 'get')
    :param requires_authentication: boolean, When securing the API with --jwt-secret-key set
                                    to False to disable authorization for this endpoint.
                                    When set to None the endpoint is automatically protected
                                    when using --jwt-secret-key. (default: None)
    """

    #just to be safe
    method = method.lower()

    def _dart(f):
        f._spec = _prepare(f)
        f._method = method
        f._methods = None
        f._requires_authentication = requires_authentication
        return f

    return _dart


def publish(methods=['GET'], requires_authentication=None):
    """Decorator function that gets a function wraps it in order to
    append a function spec (see prepare function) and autocast args/kws
    to match types.

    Parameters
    ----------
    :param methods: list, HTTP methods for this function.
                    Provides compatibility with web-publisher.
                    Takes precedence over method. (default: None)
    :param requires_authentication: boolean, When securing the API with --jwt-secret-key set
                                    to False to disable authorization for this endpoint.
                                    When set to None the endpoint is automatically protected
                                    when using --jwt-secret-key. (default: None)
    """

    # just to be safe
    methods = [m.lower() for m in methods]

    def _dart(f):
        f._spec = _prepare(f)
        f._method = None
        f._methods = methods
        f._requires_authentication = requires_authentication
        return f

    return _dart
