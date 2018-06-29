import ast
import json
from inspect import signature
from collections import Mapping, Sequence

def _prepare_arg(arg):
    '''Return a keyword arg spec (dict)'''
    _arg = {
        "name": arg.name,
    }

    if arg.annotation != arg.empty:
        _arg["type"] = str(arg.annotation.__name__)
        _arg["annotation"] = arg.annotation

    if arg.empty != arg.default:
        _arg['default'] = arg.default

    return _arg

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

    spec = {
        'name': fn.__name__,
        'docstring': fn.__doc__,
    }
    spec['args'] = _args

    return spec


def tranquilize(method='get'):
    """Decorator function that gets a function wraps it in order to
    append a function spec (see prepare function) and autocast args/kws
    to match types.
    """

    #just to be safe
    method = method.lower()

    def _dart(f):
        f._spec = _prepare(f)
        f._method = method
        return f

    return _dart

