'''execute the script file'''
import ast
from runpy import run_path

def _parse_script(fn):
    with open(fn, 'r') as f:
        source = f.read()

    nodes = ast.parse(source, fn)
    return nodes


def _is_tranquilized(decorator):
    return hasattr(decorator, 'id') and (decorator.id in ('tranquilize',))


def _is_decorated(item):
    if isinstance(item, ast.FunctionDef):
        return any([_is_tranquilized(d.func) for d in item.decorator_list])


def get_tranquilized_functions(fn):
    nodes = _parse_script(fn)
    tranquilized = [f.name for f in nodes.body if _is_decorated(f)]

    module = run_path(fn)
    funcs = [module[f] for f in tranquilized]

    return funcs

