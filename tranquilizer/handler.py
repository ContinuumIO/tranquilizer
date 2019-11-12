'''execute the script file'''
import ast
from runpy import run_path
from unittest.mock import MagicMock
from os.path import dirname, join, basename
import tempfile

def _is_tranquilized(decorator):
    return hasattr(decorator, 'id') and (decorator.id in ('tranquilize', 'publish'))

def _is_decorated(item):
    if isinstance(item, ast.FunctionDef):
        return any([_is_tranquilized(d.func) for d in item.decorator_list])


class BaseHandler(object):

    def parse(self): # pragma no cover
        raise NotImplementedError()

    @property
    def tranquilized_functions(self):
        self.parse()

        tranquilized = [f.name for f in self.nodes.body if _is_decorated(f)]
        functions = [self.module[f] for f in tranquilized]

        return functions


class ScriptHandler(BaseHandler):
    def __init__(self, fn):
        self.fn = fn

    def parse(self):
        with open(self.fn, 'r') as f:
            source = f.read()

        self.nodes = ast.parse(source, self.fn)
        self.module = run_path(self.fn)


class NotebookHandler(BaseHandler):
    def __init__(self, fn):
        self.fn = fn

    def parse(self):
        from nbconvert import ScriptExporter

        exporter = ScriptExporter()
        source, _ = exporter.from_filename(self.fn)

        self.nodes = ast.parse(source, self.fn)

        with tempfile.NamedTemporaryFile(mode='w', dir=dirname(self.fn), delete=True) as tmp:
            tmp.write(source)
            tmp.flush()
            self.module = run_path(tmp.name, init_globals={'get_ipython':MagicMock()})

