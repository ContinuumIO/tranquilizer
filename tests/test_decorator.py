from tranquilizer.decorator import tranquilize, publish
from tranquilizer.decorator import _prepare, _prepare_arg, _prepare_arg_docs
from tranquilizer.decorator import _prepare_error_docs
from inspect import signature
import datetime
import typing
import PIL.Image
import numpy

def test_attributes():

    def _func():
        return 0

    decorated = tranquilize()(_func)
    assert hasattr(decorated, '_spec')
    assert hasattr(decorated, '_method')
    assert hasattr(decorated, '_methods')
    assert hasattr(decorated, '_requires_authentication')
    assert decorated._methods is None


def test_publish_attributes():

    def _func():
        return 0

    decorated = publish()(_func)
    assert hasattr(decorated, '_spec')
    assert hasattr(decorated, '_method')
    assert hasattr(decorated, '_methods')
    assert hasattr(decorated, '_requires_authentication')
    assert decorated._method is None


def test_method():

    # separate functions are used for
    # get and post. Calling the decorator
    # a second time updates the original
    # function
    def _funcg():
        return 0

    get = tranquilize(method='GET')(_funcg)
    assert get._method == 'get'

    def _funcp():
        return 0

    post = tranquilize(method='PosT')(_funcp)
    assert post._method == 'post'

    def _funcput():
        return 0

    post = tranquilize(method='pUt')(_funcput)
    assert post._method == 'put'


def test_methods():

    # separate functions are used for
    # get and post. Calling the decorator
    # a second time updates the original
    # function
    def _funcg():
        return 0

    get = publish(methods=['GET'])(_funcg)
    assert get._methods == ['get']

    def _funcp():
        return 0

    post = publish(methods=['PosT'])(_funcp)
    assert post._methods == ['post']

    def _funcpg():
        return 0

    post_get = publish(methods=['GET', 'PosT'])(_funcpg)
    assert post_get._methods == ['get', 'post']


def test_protected():
    def _func():
        return 0

    protected = tranquilize(requires_authentication=True)(_func)
    assert protected._requires_authentication == True

    unprotected = tranquilize(requires_authentication=False)(_func)
    assert protected._requires_authentication == False

    unspecified = tranquilize()(_func)
    assert protected._requires_authentication is None

    protected_p = publish(requires_authentication=True)(_func)
    assert protected_p._requires_authentication == True

    unprotected_p = publish(requires_authentication=False)(_func)
    assert protected_p._requires_authentication == False

    unspecified_p = publish()(_func)
    assert protected_p._requires_authentication is None


def test_prepare():
    def _func(arg: float):
        '''docstring

        :param arg: number
        :raises ValueError: not a number'''
        return arg
    
    spec = _prepare(_func)   

    assert isinstance(spec, dict)
    assert spec.keys() == set(['name','docstring','args', 
                               'param_docs','error_docs'])
    assert spec['name'] == '_func'
    assert spec['docstring'] == 'docstring\n\n        '

def test_prepare_no_docstring():
    def _empty(arg: float):
        pass

    spec = _prepare(_empty)
    assert spec['param_docs'] == {}
    assert spec['error_docs'] == {}
    assert spec['docstring'] == ''


def test_prepare_args():
    def _func(
        s: str,
        i: int,
        f: float,
        b: bool,
        d: datetime.date,
        dt: datetime.datetime,
        l: list,
        L: typing.List,
        Ls: typing.List[str],
        Li: typing.List[int],
        Lf: typing.List[float],
        Lb: typing.List[bool],
        Ld: typing.List[datetime.date],
        Ldt: typing.List[datetime.datetime],
        fnb: typing.BinaryIO,
        fnt: typing.TextIO,
        img: PIL.Image.Image,
        arr: numpy.ndarray,
        untyped,
        untyped_default = None,
        typed_default: str = 'python'
        
    ):
        pass

    sig = signature(_func)
    assert _prepare_arg(sig.parameters['s']) == {'name':'s','type':'str','annotation':str}
    assert _prepare_arg(sig.parameters['i']) == {'name':'i','type':'int','annotation':int}
    assert _prepare_arg(sig.parameters['f']) == {'name':'f','type':'float','annotation':float}
    assert _prepare_arg(sig.parameters['b']) == {'name':'b','type':'bool','annotation':bool}
    assert _prepare_arg(sig.parameters['d']) == {'name':'d','type':'date','annotation':datetime.date}
    assert _prepare_arg(sig.parameters['dt']) == {'name':'dt','type':'datetime','annotation':datetime.datetime}
    assert _prepare_arg(sig.parameters['l']) == {'name':'l','type':'list','annotation':list}
    assert _prepare_arg(sig.parameters['L']) == {'name':'L','type':'List','annotation':typing.List}
    assert _prepare_arg(sig.parameters['Ls']) == {'name':'Ls','type':'List','annotation':typing.List[str]}
    assert _prepare_arg(sig.parameters['Li']) == {'name':'Li','type':'List','annotation':typing.List[int]}
    assert _prepare_arg(sig.parameters['Lf']) == {'name':'Lf','type':'List','annotation':typing.List[float]}
    assert _prepare_arg(sig.parameters['Lb']) == {'name':'Lb','type':'List','annotation':typing.List[bool]}
    assert _prepare_arg(sig.parameters['Ld']) == {'name':'Ld','type':'List','annotation':typing.List[datetime.date]}
    assert _prepare_arg(sig.parameters['Ldt']) == {'name':'Ldt','type':'List','annotation':typing.List[datetime.datetime]}
    assert _prepare_arg(sig.parameters['fnb']) == {'name':'fnb','type':'BinaryIO','annotation':typing.BinaryIO}
    assert _prepare_arg(sig.parameters['fnt']) == {'name':'fnt','type':'TextIO','annotation':typing.TextIO}
    assert _prepare_arg(sig.parameters['img']) == {'name':'img','type':'Image','annotation':PIL.Image.Image}
    assert _prepare_arg(sig.parameters['arr']) == {'name':'arr','type':'ndarray','annotation':numpy.ndarray}
    assert _prepare_arg(sig.parameters['untyped']) == {'name':'untyped'}
    assert _prepare_arg(sig.parameters['untyped_default']) == {'name':'untyped_default', 'default': None}
    assert _prepare_arg(sig.parameters['typed_default']) == {'name':'typed_default', 'type':'str', 'annotation':str, 'default': 'python'}

def test_prepare_arg_docs():
        doc = '''docstring

        docstring

        :param arg1: number
        :param arg2: string
        :raises ValueError: not a number'''

        param_docs, remainder = _prepare_arg_docs(doc)
        
        assert param_docs == {'arg1': 'number', 'arg2': 'string'}
        assert remainder == 'docstring\n\n        docstring\n\n        :raises ValueError: not a number'

def test_prepare_arg_doc_noargs():
        doc = '''docstring

        docstring

        :raises ValueError: not a number'''

        param_docs, remainder = _prepare_arg_docs(doc)

        assert param_docs == {}
        assert remainder == doc

def test_prepare_error_docs():
        doc = '''docstring

        docstring

        :param arg1: number
        :param arg2: string
        :raises ValueError: not a number'''

        error_docs, remainder = _prepare_error_docs(doc)
        
        assert error_docs == {500:'ValueError:not a number'}
        assert remainder == 'docstring\n\n        docstring\n\n        :param arg1: number\n        :param arg2: string\n        '

def test_prepare_error_noerror():
        doc = '''docstring

        docstring

        :param arg1: number
        :param arg2: string'''

        error_docs, remainder = _prepare_error_docs(doc)
        
        assert error_docs == {}
        assert remainder == doc