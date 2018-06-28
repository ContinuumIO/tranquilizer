'''execute the script file'''
import ast
from runpy import run_path

def parse_script(fn):
    with open(fn, 'r') as f:
        source = f.read()

    nodes = ast.parse(source, fn)
    return nodes


def _is_published(decorator):
    return hasattr(decorator, 'id') and (decorator.id in ('publish',))


def _is_decorated(item):
    if isinstance(item, ast.FunctionDef):
        return any([_is_published(d.func) for d in item.decorator_list])


def get_published_functions(fn):
    nodes = parse_script(fn)
    published = [f.name for f in nodes.body if _is_decorated(f)]

    module = run_path(fn)
    funcs = [module[f] for f in published]

    return funcs

