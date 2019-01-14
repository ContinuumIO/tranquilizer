'''execute the script file'''
import ast
from runpy import run_path
from abc import ABC, abstractmethod
from os.path import dirname, join, basename
import os

def _is_tranquilized(decorator):
    return hasattr(decorator, 'id') and (decorator.id in ('tranquilize',))

def _is_decorated(item):
    if isinstance(item, ast.FunctionDef):
        return any([_is_tranquilized(d.func) for d in item.decorator_list])

class BaseHandler(object):

    def parse(self):
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

        #maybe not the best idea, but works
        directory = dirname(self.fn)
        script_name = basename(self.fn) + '.py'
        script_file = join(directory, script_name)
        with open(script_file, 'w') as f:
            f.write(source)

        self.nodes = ast.parse(source, script_file)
        self.module = run_path(script_file)

        os.remove(script_file)
