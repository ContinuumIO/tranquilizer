from tranquilizer.resource import  make_resource, make_parser
from tranquilizer.handler import ScriptHandler
from tranquilizer.decorator import publish, tranquilize
from tranquilizer.types import is_list_subclass
from flask_restx import Resource, Namespace
import typing
import datetime
import numpy
import PIL.Image
from os.path import dirname, join


def test_make_resource_method():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    funcs = script.tranquilized_functions
    ns = Namespace('/', description='Testing Tranquilized API')
    resource = make_resource(funcs[0], ns)
    assert issubclass(resource, Resource)
    assert hasattr(resource, 'get')

def test_make_resource_methods():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop_publish.py')
    script = ScriptHandler(fn)
    funcs = script.tranquilized_functions
    ns = Namespace('/', description='Testing Tranquilized API')
    resource = make_resource(funcs[0], ns)
    assert issubclass(resource, Resource)
    assert hasattr(resource, 'get')
    assert hasattr(resource, 'post')

def test_parser_list():
    def _func(
        l: list,
        L: typing.List,
        Ls: typing.List[str],
        Li: typing.List[int],
        Lf: typing.List[float],
        Lb: typing.List[bool],
        Ld: typing.List[datetime.date],
        Ldt: typing.List[datetime.datetime],
    ):
        pass

    decorated = tranquilize()(_func)
    parser = make_parser(decorated._spec, location='get', compat=False)
    assert len(parser.args) == 8

    assert all([a.action == 'append' for a in parser.args])

def test_parser_files():
    def _func(
        fnb: typing.BinaryIO,
        fnt: typing.TextIO,
        img: PIL.Image.Image,
        arr: numpy.ndarray,
    ):
        pass

    decorated = tranquilize()(_func)
    parser = make_parser(decorated._spec, location='get', compat=False)
    assert len(parser.args) == 4

    assert all([a.location[1] == 'files' for a in parser.args])

def test_parser_default():
    def _func(
        typed_default: str = 'python',
        untyped_default = None,
    ):
        pass

    decorated = tranquilize()(_func)
    parser = make_parser(decorated._spec, location='get', compat=False)
    assert len(parser.args) == 2

    defaults = {a.name:a for a in parser.args}
    assert defaults['untyped_default'].default is None
    assert defaults['typed_default'].default == 'python'

    assert all(a.required == False for a in defaults.values())

def test_parser_builtin():
    def _func(
        s: str,
        i: int,
        f: float,
        b: bool,
        d: datetime.date,
        dt: datetime.datetime,
    ):
        pass

    decorated = tranquilize()(_func)
    parser = make_parser(decorated._spec, location='get', compat=False)
    assert len(parser.args) == 6

    assert all([a.action == 'store' for a in parser.args])

def test_parser_untyped_publish():
    def _func(
        untyped
    ):
        pass

    decorated = publish()(_func)
    parser = make_parser(decorated._spec, location='get', compat=True)
    assert len(parser.args) == 1

    assert parser.args[0].action == 'append'

def test_parser_untyped():
    def _func(
        untyped
    ):
        pass

    decorated = tranquilize()(_func)
    parser = make_parser(decorated._spec, location='get', compat=False)
    assert len(parser.args) == 1

    assert parser.args[0].action == 'store'
    assert parser.args[0].type is str

def test_parser_docs():
    def _func(
        arg: str
    ):
        '''docstring
        
        :param arg: a string'''
        pass

    decorated = tranquilize()(_func)
    parser = make_parser(decorated._spec, location='get', compat=False)
    assert len(parser.args) == 1
    
    assert parser.args[0].help == 'a string'

def test_make_resource_docs():
    here = dirname(__file__)
    fn = join(here, 'integer_error.py')
    script = ScriptHandler(fn)
    funcs = script.tranquilized_functions
    ns = Namespace('/', description='Testing Tranquilized API')
    resource = make_resource(funcs[0], ns)
    assert resource.get.__doc__ == 'Make an integer\n\n    '
    assert resource.get.__apidoc__['responses'] == {500: 'ValueError:not an integer'}
